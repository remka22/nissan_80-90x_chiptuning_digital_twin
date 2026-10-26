/* ============================================================================
   J30 — ДИСПЛЕЙ НА ТЕЛЕФОН ЧЕРЕЗ WI-FI
   21.09.26, ревизия 23.09.26. Отдельный скетч, НЕ мост.
   ТОЛЬКО СЛУШАЕТ — в ЭБУ не передаёт ничего.

   ЗАЧЕМ: открыть в машине браузером на телефоне и видеть живые параметры,
   НЕ ОТКЛЮЧАЯ FTDI от компа. Приём — высокоомный вход, на одну линию TX можно
   повесить сколько угодно слушателей; передатчик ЭБУ этого не замечает.

                    ┌── FTDI ── USB ── комп (панель логгера)
      ЭБУ TX ───────┤
                    └── ESP32 GPIO16 ── Wi-Fi ── телефон

   ⚠ ПОДКЛЮЧЕНИЕ:
     GPIO16 <- TX ЭБУ, ЧЕРЕЗ ДЕЛИТЕЛЬ: 10к последовательно + 20к на массу.
               У ЭБУ 0-5 В, у ESP32 входы 3.3 В и пятивольтовые НЕ терпят.
     TX ЭБУ НЕ ПОДКЛЮЧАТЬ (в ECU.begin передатчик отключён: -1). Два передатчика
               на одной линии подерутся, и связь сломается и у нас, и у FTDI.
     ЗЕМЛЯ    общая с ЭБУ и FTDI, иначе кольцо по земле и наводки.
     GPIO26 <- ШДК (RS232 через MAX3232). Не подключён — AFR покажет прочерк.

   ЭКРАН: две страницы, листаются пальцем влево-вправо.
     1) крупные блоки в два столбца (как верхняя строка датчиков в панели)
     2) полная таблица параметров (как таблица справа в панели)
   Карт и онлайн-тюнинга здесь НЕТ намеренно — только просмотр.

   СКОРОСТЬ:
     ЭБУ отдаёт кадр примерно раз в 400 мс (2.5 Гц) — это потолок свежести,
     и он же 80% всей задержки. Страница опрашивает каждые 150 мс.
     ШДК AEM 30-0300 шлёт 10 Гц, ASCII "NN.N\r\n" (см. базу знаний).

   ДАННЫЕ ИЗ ПРОШИВКИ: карта смеси и её оси вшиты ниже из
     логер/j30_v42_3_шов-УОЗ-и-прогрев-яч7_01.09.26_1230 ИИ.bin
     ⚠ СМЕНИЛ ПРОШИВКУ — ОБНОВИ ЭТИ ТАБЛИЦЫ, иначе «AFR цель» будет от старой.
   ============================================================================ */

/* ⚠ ЭТО .cpp, А НЕ .ino — И ЭТО ВАЖНО.
   Препроцессор .ino (и в Arduino IDE, и в PlatformIO) не понимает сырые
   строковые литералы R"HTML(...)HTML". Он лезет разбирать JavaScript внутри
   страницы как код C++ и валится с «'function' does not name a type».
   В .cpp никакой предобработки нет — собирается как есть.
   Платой за это стал явный #include <Arduino.h> ниже: в .ino его добавляли
   автоматически. */
#include <Arduino.h>
#include <WiFi.h>
#include <Preferences.h>
#include <ESPmDNS.h>

// ---------------- настройки ----------------
static const char*    AP_NAME    = "J30-DASH";
static const char*    AP_PASS    = "12345678";   // минимум 8 символов
static const int      PIN_ECU_RX = 16;
static const int      PIN_WBL_RX = 26;
static const uint32_t ECU_BAUD   = 15625;        // проверено по коду панели
static const uint32_t WBL_BAUD   = 9600;         // AEM 30-0300

/* ---------------- ДВА ВХОДА ОДНОВРЕМЕННО (режим AP_STA) ----------------
   1) СВОЯ ТОЧКА «J30-DASH» — работает ВСЕГДА, адрес 192.168.4.1.
      Запасной вход: модем можно вообще не включать.
   2) КЛИЕНТ РЕЖИМА МОДЕМА айфона — чтобы телефон остался на сотовой связи
      и не терял интернет. Адрес выдаёт телефон, поэтому ищем по имени
      через mDNS: http://j30.local

   Плата пробует подключиться к модему раз в STA_RETRY_MS, НЕ БЛОКИРУЯ приём
   кадров. Модем включили через час — прицепится на ближайшей проверке сама.

   ⚠ РАДИО ОДНО: когда клиент цепляется к модему, точка доступа перескакивает
   на канал модема. Кто в этот момент сидел на «J30-DASH» — на секунду отвалится
   и переподключится. Один раз, дальше стабильно.

   ⚠ КИРИЛЛИЦА В ИМЕНИ СЕТИ — известное больное место ESP32. Имя уходит как
   UTF-8 байты, и обычно работает, но если подключения нет, а пароль точно
   верный — ПЕРВОЕ, что надо попробовать: переименовать айфон латиницей
   (Настройки → Основные → Об этом устройстве → Имя). */
static const char*    STA_NAME   = "iPhone (Михаил)";
static const char*    STA_PASS   = "tasar232";
static const char*    MDNS_NAME  = "j30";        // -> http://j30.local
/* ⚠⚠ ПАУЗА МЕЖДУ ПОПЫТКАМИ ОБЯЗАНА БЫТЬ БОЛЬШЕ, ЧЕМ ДЛИТСЯ САМА ПОПЫТКА.
   Подключение к пропавшей сети отваливается по своему таймауту через 10-15 с.
   Стояло 10 с — и новая попытка стартовала ПОВЕРХ незавершённой предыдущей,
   без просвета. Драйвер не выходил из состояния «подключаюсь», а в режиме
   точка+клиент это ДУШИТ ТОЧКУ НАСМЕРТЬ: её просто нет в эфире.
   Дома этого не видно (телефон рядом, цепляемся с первой попытки), а в машине
   без раздачи плата выглядела сдохшей. Ниже 25 с НЕ СТАВИТЬ. */
static const uint32_t STA_RETRY_MS = 30000;
// сколько направленных попыток подряд терпим, прежде чем решить, что телефон
// сменил канал и адрес в памяти протух (30 с x 6 = три минуты)
static const uint8_t  STA_FAIL_MAX = 6;
// сторожевой срок на одну попытку: дольше этого она висеть не должна
static const uint32_t STA_BUSY_MS  = 20000;

// Состояние поиска телефона. Объявлено здесь, потому что адрес /sta в
// обработчике запросов сбрасывает счётчик, а он живёт ниже по файлу.
static uint32_t sta_next  = 0;              // время следующей попытки
static uint8_t  sta_fail  = 0;              // направленных попыток подряд впустую
static bool     sta_busy  = false;          // попытка прямо сейчас в ходу
static uint32_t sta_busy_t = 0;             // когда она началась
static uint8_t  sta_ch    = 0;              // канал телефона
static bool     sta_known = false;          // адрес телефона известен
static Preferences prefs;                   // постоянная память платы

HardwareSerial ECU(2);
HardwareSerial WBL(1);
WiFiServer     http(80);

/* ---------------- таблицы из прошивки ----------------
   Карта смеси $7D00 + оси: обороты $7B00, нагрузка $7AF0.
   Нужны для «AFR цель» — её панель берёт из карты по текущей ячейке.
   ⚠ Копия из v44_5 (оси под 1 бар, 25.10.26). Сменил карту смеси в блоке —
   обнови и здесь, иначе цель на телефоне соврёт. */
static const uint8_t FUEL[256] PROGMEM = {
  192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192,   6,  13,  11,  36,  36,
  192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192,   8,  16,  11,  36,  36,
  192, 192, 194, 194, 193, 193, 192, 192, 192,   7,  11,  16,  16,  77,  77,  77,
  192, 192, 192, 192, 192, 192, 192, 192, 192,   7,  11,  16,  16,  77,  77,  77,
  192, 192, 192, 192, 192, 192, 192, 192, 192,   6,   7,  16,  20,  30,  36,  36,
  191, 191, 191, 191, 191, 191, 191, 191, 191,   6,   7,  16,  28,  26,  36,  36,
  191, 191, 191, 191, 191, 190, 190, 190, 191, 191,   6,  11,  30,  28,  36,  36,
  190, 190, 190, 190, 190, 190, 189, 192, 193, 193,   6,  11,  28,  33,  36,  36,
  191, 191, 191, 192, 192, 192, 192, 192, 193,   5,   7,  10,  30,  37,  37,  37,
  192, 192, 192, 192, 192, 192, 192, 192,   4,   5,   7,  10,  30,  42,  42,  42,
  192, 192, 192, 192, 192, 192, 192, 192,   5,  10,  12,  22,  34,  42,  42,  42,
  192, 192, 192, 192, 192, 192,   4,   7,  10,  14,  18,  23,  38,  49,  49,  49,
  192, 192, 192, 192, 192,   8,   8,   8,  18,  23,  28,  31,  38,  52,  52,  52,
   12,  12,  12,  12,  12,  14,  16,  18,  22,  28,  34,  34,  39,  63,  63,  63,
   16,  16,  16,  16,  16,  18,  20,  22,  24,  26,  36,  41,  52,  49,  49,  49,
   22,  22,  22,  22,  22,  22,  25,  28,  32,  35,  39,  42,  56,  49,  49,  49,
};
static const uint8_t  FRAX[16] PROGMEM = {8,10,16,24,32,40,48,56,64,72,80,88,96,104,112,120};
static const uint8_t  FCAX[16] PROGMEM = {16,20,24,28,32,36,40,48,56,64,72,80,96,135,170,210};
static const uint16_t BIN_K  = 345;     // $7F2B — K форсунок
static const uint8_t  BIN_KM = 128;     // $4A12 — КМ (ДАД)

// значение карты смеси -> AFR (формула M30-XDF, как в панели)
static float afr_of(uint8_t x) {
  return (x >= 128) ? (1881.6f / (float(x) - 64.0f)) : (1881.6f / (float(x) + 128.0f));
}
static uint8_t nearest(uint8_t v, const uint8_t* ax) {
  uint8_t bi = 0; int bd = 1000;
  for (uint8_t i = 0; i < 16; i++) {
    int d = abs(int(v) - int(pgm_read_byte(ax + i)));
    if (d < bd) { bd = d; bi = i; }
  }
  return bi;
}

/* Температура ОЖ в градусах — ЗАВОДСКОЙ ТАРИРОВКОЙ САМОГО БЛОКА.
   Сырьё АЦП $004C блок прогоняет через таблицу $FB30 (бин 0x7B30, 32 точки) и
   кладёт в $140C. Таблица ПЕРЕВОРАЧИВАЕТ направление: сырьё при прогреве
   падает, а $140C растёт. Градусы = $140C - 50 (стандарт Nissan, как Consult).
   «-50» — так таблица описана и в определениях M30 («°C=X-50»), и совпадает с
   независимой кривой термистора: +10...+125 C — расхождение 0-2 C.
   Таблица вшита из логер/j30_v42_3_...bin; в стоке она такая же.
   ⚠ СМЕНИЛ ПРОШИВКУ — сверь эту таблицу (как и карту смеси выше).

   Интерполяция — ровно подпрограмма блока $80A9, с тем же округлением вниз.
   Разница с $140C только в гистерезисе: блок сбрасывает температуру с
   запаздыванием на 2 единицы. На экране это незаметно.

   Окно годности сырья в блоке — 3...241 ($B264), вне его блок подставляет
   заглушку. Мы зажимаем к краю окна и на экране приписываем знак «<» / «>».
   ⚠ ОБРЫВ ПРОВОДА НЕОТЛИЧИМ ОТ СИЛЬНОГО МОРОЗА: оба гонят сырьё к 255, блок
   их тоже не различает. На прогретом моторе «<» значит провод, а не погоду. */
static const uint8_t ECT_TAB[32] PROGMEM = {
  255, 241, 200, 174, 160, 149, 141, 134, 128, 122, 118, 113, 109, 105, 101,  97,
   93,  90,  86,  82,  78,  74,  70,  66,  61,  57,  51,  45,  38,  27,   8,   0};

static uint8_t fb30(uint8_t raw) {              // подпрограмма блока $80A9
  uint8_t a = raw > 0xF8 ? 0xF8 : raw;
  uint8_t i = a >> 3, f = (a & 7) << 5;
  uint8_t t0 = pgm_read_byte(ECT_TAB + i);
  if (f == 0) return t0;
  uint8_t t1 = pgm_read_byte(ECT_TAB + i + 1);
  if (t1 == t0) return t0;
  if (t1 > t0) return t0 + uint8_t((uint16_t(t1 - t0) * f) >> 8);          // растущий участок
  return t1 + uint8_t((uint16_t(t0 - t1) * (256 - f)) >> 8);               // убывающий
}

static int ect_c(uint8_t adc) {
  if (adc > 241) adc = 241;                       // зажим к краю окна годности
  if (adc < 3)   adc = 3;
  return int(fb30(adc)) - 50;
}

// ---------------- живые значения ----------------
struct Live {
  uint16_t rpm_raw = 0;      // $140A:$140B
  uint8_t  load = 0;         // $1482
  uint8_t  fill = 0;         // $1413
  uint8_t  lam = 100;        // $1431  x0.01
  uint16_t adc_map = 0;      // $1408:$1409
  uint8_t  kpa = 0;          // $00F7
  uint8_t  vbat = 0;         // $008F
  uint8_t  ect = 0;          // $004C
  uint8_t  o2 = 0;           // $1400
  uint8_t  tidx = 0;         // $00B1
  uint8_t  rxx = 0;          // $1402
  uint8_t  uoz_raw = 0;      // $140F  реально доставленный (70 - X = градусы)
  uint8_t  uoz_map = 0;      // $143B  из карты
  uint8_t  ch9 = 0;          // $17E0  сырьё канала 9 (ДТВ)
  uint8_t  tv = 0;           // $E2  ТВ, °C+50   (v44, считает блок)
  uint8_t  tz = 0;           // $E3  Т заряда, °C+50
  uint8_t  kv = 0;           // $E5  КВТЗ, ×128
  uint8_t  ktz = 0;          // $E4  КТЗ, ×128
  uint8_t  dead = 0;         // $142C
  uint8_t  tps = 0;          // $14A2
  uint16_t acc = 0;          // $1450:$1451
  uint8_t  ve = 0;           // $00FA  x0.0078125
  uint8_t  ktps = 0;         // $00FB
  uint16_t inj_raw = 0;      // $004D:$004E, тик 10 мкс
  uint8_t  corr = 128;       // $14EA  128 = нет поправки (см. ниже про знак)
  uint8_t  flow = 0;         // $144B

  float    afr = -1;         // ШДК, сглаженное — как на экране прибора
  float    afr_raw = -1;     // ШДК, как пришло в порт (мгновенный снимок)
  uint32_t afr_ms = 0;
  uint32_t frame_ms = 0;
  uint32_t frames = 0, bad = 0;
  uint32_t wok = 0, wbad = 0;
  int8_t   knock_min = 0;    // самый глубокий стук за сессию (минус), 0 = не было
  // Откаты угла за сессию. Откат = поправка ушла из 0/плюса в минус; пока не вернулась
  // к 0 — это тот же откат, его глубина = самый глубокий минус внутри.
  bool     k_in  = false;    // сейчас идёт откат
  int8_t   k_cur = 0;        // глубина текущего отката
  uint16_t k_cnt = 0;        // сколько откатов
  uint32_t k_sum = 0;        // сумма глубин ЗАКОНЧЕННЫХ откатов, градусы (модуль)
  uint8_t  kpa_min = 255;    // мин/макс давления ЗА СЕССИЮ (с включения платы)
  uint8_t  kpa_max = 0;
};
static Live L;

/* ---------------- разбор кадра ЭБУ ----------------
   AE 17 | addr_hi addr_lo | len | data[len] | chk,  chk = XOR(addr_hi..данные)
   Узкий кадр: адрес $FFF0, значения ПОЗИЦИОННО (порядок = NARROW_MAP в панели).
   Разбор адаптивный по длине — короткий кадр от старого бина не ломает.

   ⚠ Ложный старт возможен: если внутри данных попадётся пара AE 17, парсер
   поймает её за начало кадра. Контрольная сумма такой кадр отбракует и счётчик
   битых подрастёт — это НОРМА, а не поломка. */
static const uint16_t NARROW_ADDR = 0xFFF0;
enum {
  P_RPM_HI=0, P_RPM_LO=1, P_LOAD=2, P_FILL=3, P_LAM=4,
  P_ADC_HI=7, P_ADC_LO=8, P_KPA=9, P_VBAT=10, P_ECT=11, P_O2=12,
  P_TIDX=13, P_RXX=14, P_UOZRAW=15, P_UOZMAP=16, P_CH9=18,
  P_DEAD=20, P_TPS=21, P_ACC_HI=22, P_VE=23, P_KTPS=24,
  P_INJ_HI=25, P_INJ_LO=26, P_ACC_LO=29, P_CORR=30, P_FLOW=31,
  // v44: на местах онлайн-заливки блок отдаёт свой расчёт КТЗ. ТВ считает САМ БЛОК
  // той же тарировкой $FB30, что ДТОЖ (датчик такой же), в шкале °C+50.
  // ⚠ Только для прошивки v44 и новее: на старых здесь данные тени — будет мусор.
  P_TV=5, P_TZ=6, P_KV=27, P_KTZ=28
};

static uint8_t  fbuf[300];
static uint16_t flen = 0, fneed = 0;
static uint8_t  fstate = 0;
static uint16_t fdata = 0;                       // длина данных текущего узкого кадра

static inline uint8_t at(uint16_t i, uint8_t dflt) {
  return (i < fdata) ? fbuf[3 + i] : dflt;       // 3 = addr_hi, addr_lo, len
}

static void frame_done() {
  uint16_t addr = (uint16_t(fbuf[0]) << 8) | fbuf[1];
  uint8_t  len  = fbuf[2];
  uint8_t  chk  = 0;
  for (uint16_t i = 0; i < uint16_t(len) + 3; i++) chk ^= fbuf[i];
  if (chk != fbuf[3 + len]) { L.bad++; return; }
  L.frames++; L.frame_ms = millis();
  if (addr != NARROW_ADDR) return;

  fdata = len;
  L.rpm_raw = (uint16_t(at(P_RPM_HI,0)) << 8) | at(P_RPM_LO,0);
  L.load    = at(P_LOAD, L.load);
  L.fill    = at(P_FILL, L.fill);
  L.lam     = at(P_LAM,  L.lam);
  L.adc_map = (uint16_t(at(P_ADC_HI,0)) << 8) | at(P_ADC_LO,0);
  L.kpa     = at(P_KPA,  L.kpa);
  L.vbat    = at(P_VBAT, L.vbat);
  L.ect     = at(P_ECT,  L.ect);
  L.o2      = at(P_O2,   L.o2);
  L.tidx    = at(P_TIDX, L.tidx);
  L.rxx     = at(P_RXX,  L.rxx);
  L.uoz_raw = at(P_UOZRAW, L.uoz_raw);
  L.uoz_map = at(P_UOZMAP, L.uoz_map);
  L.ch9     = at(P_CH9,  L.ch9);
  L.tv      = at(P_TV,   L.tv);
  L.tz      = at(P_TZ,   L.tz);
  L.kv      = at(P_KV,   L.kv);
  L.ktz     = at(P_KTZ,  L.ktz);
  L.dead    = at(P_DEAD, L.dead);
  L.tps     = at(P_TPS,  L.tps);
  L.acc     = (uint16_t(at(P_ACC_HI,0)) << 8) | at(P_ACC_LO,0);
  L.ve      = at(P_VE,   L.ve);
  L.ktps    = at(P_KTPS, L.ktps);
  L.inj_raw = (uint16_t(at(P_INJ_HI,0)) << 8) | at(P_INJ_LO,0);
  L.corr    = at(P_CORR, L.corr);
  L.flow    = at(P_FLOW, L.flow);

  // запоминаем самый глубокий СТУК (отрицательную поправку) за сессию
  int c = int(L.corr) - 128;
  if (c < L.knock_min) L.knock_min = int8_t(c);

  // счёт откатов: новый — только после возврата поправки к 0 или в плюс
  if (c < 0) {
    if (!L.k_in) { L.k_in = true; L.k_cnt++; L.k_cur = int8_t(c); }
    else if (c < L.k_cur) L.k_cur = int8_t(c);
  } else if (L.k_in) {
    L.k_in = false; L.k_sum += uint32_t(-L.k_cur);
  }

  // мин/макс давления за сессию. Нули до первого кадра не считаем.
  if (L.kpa) {
    if (L.kpa < L.kpa_min) L.kpa_min = L.kpa;
    if (L.kpa > L.kpa_max) L.kpa_max = L.kpa;
  }
}

static void ecu_poll() {
  while (ECU.available()) {
    uint8_t b = ECU.read();
    switch (fstate) {
      case 0: if (b == 0xAE) fstate = 1; break;
      case 1: fstate = (b == 0x17) ? 2 : (b == 0xAE ? 1 : 0); flen = 0; fneed = 0; break;
      case 2:
        if (flen < sizeof(fbuf)) fbuf[flen++] = b;
        if (flen == 3) {
          fneed = uint16_t(fbuf[2]) + 4;
          if (fneed > sizeof(fbuf)) { fstate = 0; L.bad++; break; }
        }
        if (fneed && flen >= fneed) { frame_done(); fstate = 0; }
        break;
    }
  }
}

/* ---------------- разбор ШДК ----------------
   AEM 30-0300: 9600 8N1, ASCII "NN.N\r\n", ПОТОК 10 Гц.
   СТРОГО: строка обязана БЫТЬ числом целиком. Склеилась — выбрасываем.
   Почему — см. «j30/база знаний/ШДК AEM 30-0300 ... 02.09.26 ИИ.txt»:
   старый разбор выкусывал число из склейки ("13.0"+"12.7" -> 13.012) и врал. */
static char    wbuf[16];
static uint8_t wlen = 0;

/* ⭐ СГЛАЖИВАНИЕ AFR — ВАРИАНТ «В» (спокойный): медиана 9 + k 0.22, ~1.9 с до
   полного значения. Выбран пользователем 25.10.26 из трёх (А живой 3/0.60,
   Б средний 5/0.40, В спокойный 9/0.22), остальные убраны.

   ЗАЧЕМ СГЛАЖИВАТЬ ВООБЩЕ: в порт AEM отдаёт МГНОВЕННЫЕ снимки 10 раз в
   секунду, а на свой экран выводит отфильтрованное. Отсюда «на приборе ровные
   15, в порту 13...17» — его нормальное поведение, а не неисправность.

   ⚠ В базе знаний стоит вывод «сглаживать НЕ НАДО» — он УСТАРЕЛ. Писался,
   когда поток шёл 1 Гц из-за бага разбора: пять точек растянулись бы на пять
   секунд. Сейчас честные 10 Гц, те же пять точек — полсекунды.

   ДВА СЛОЯ:
   1) МЕДИАНА окном n убивает одиночные выбросы: значение-выброс оказывается с
      краю отсортированного окна и в середину не попадает вовсе. Обычное
      среднее вместо этого размазало бы его по всем точкам окна.
   2) ЭКСПОНЕНЦИАЛЬНОЕ СГЛАЖИВАНИЕ поверх убирает оставшиеся ступеньки: новое
      значение сдвигает показание на долю k от разницы, а не целиком.

   ⚠⚠ ФИЛЬТР СЧИТАЕТ ПО ОТСЧЁТАМ, А НЕ ПО ВРЕМЕНИ. Пока поток честные 10 Гц,
   задержки такие, как в таблице ниже. Если прибор начнёт слать реже, задержка
   вырастет ПРОПОРЦИОНАЛЬНО: при 1 Гц отстанет уже на двадцать секунд.
   Защиты от этого сейчас НЕТ (сброс окна при длинной паузе не сделан). */
struct Smooth {
  uint8_t n;          // окно медианы
  float   k;          // коэффициент экспоненциального сглаживания
  float   ring[9];
  uint8_t ri, rn;
  float   out;
};
// задержка до полного значения при потоке 10 Гц ~1.9 с
static Smooth SM = {9, 0.22f, {0}, 0, 0, -1};

static void smooth_feed(Smooth& sm, float v) {
  sm.ring[sm.ri] = v;
  sm.ri = (sm.ri + 1) % sm.n;
  if (sm.rn < sm.n) sm.rn++;

  float t[9];
  for (uint8_t i = 0; i < sm.rn; i++) t[i] = sm.ring[i];
  for (uint8_t i = 1; i < sm.rn; i++) {          // сортировка вставками
    float key = t[i]; int8_t j = int8_t(i) - 1;
    while (j >= 0 && t[j] > key) { t[j + 1] = t[j]; j--; }
    t[j + 1] = key;
  }
  float med = t[sm.rn / 2];
  sm.out = (sm.out > 0) ? (sm.out + sm.k * (med - sm.out)) : med;
}

static void wbl_line() {
  wbuf[wlen] = 0;
  if (!wlen) return;
  uint8_t digits = 0, dots = 0; bool bad = false;
  for (uint8_t i = 0; i < wlen; i++) {
    char c = wbuf[i];
    if (c >= '0' && c <= '9') digits++;
    else if (c == '.') { if (++dots > 1) { bad = true; break; } }
    else { bad = true; break; }
  }
  if (bad || !digits || digits > 4) { L.wbad++; return; }
  float v = atof(wbuf);
  if (v >= 0.50f && v <= 1.60f) v *= 14.7f;      // прибор в режиме Lambda
  if (v < 8.0f || v > 22.0f) { L.wbad++; return; }

  L.afr_raw = v;                                 // как пришло, без обработки
  L.afr_ms  = millis();
  L.wok++;

  smooth_feed(SM, v);
  L.afr = SM.out;                                // крупная цифра на экране
}

static void wbl_poll() {
  while (WBL.available()) {
    char c = WBL.read();
    if (c == '\r' || c == '\n') { wbl_line(); wlen = 0; }
    else if (wlen < sizeof(wbuf) - 1) wbuf[wlen++] = c;
    else wlen = 0;
  }
}

// ---------------- страница ----------------
/* ⚠ ДАННЫЕ ИДУТ ЧЕРЕЗ SSE (Server-Sent Events), а не опросом.
   Было: страница дёргала /d каждые 150 мс. На каждый запрос — новое TCP-соединение,
   плюс в среднем 75 мс ожидания своей очереди. Итого ~100-120 мс поверх кадра.
   Стало: одно открытое соединение, плата САМА выталкивает данные в тот момент,
   когда разобрала кадр. Задержка ~3-5 мс. Библиотек не нужно: EventSource у
   браузера встроен, со стороны платы это просто не закрывать клиента.
   /d оставлен запасным путём — если EventSource почему-то не поднимется. */
static const char PAGE[] PROGMEM = R"HTML(<!DOCTYPE html><html lang=ru><head>
<meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,maximum-scale=1">
<title>J30</title><style>
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:#0b0f14;color:#dfe8f0;font:14px/1.2 -apple-system,system-ui,sans-serif;overflow:hidden}
#hd{display:flex;justify-content:space-between;align-items:center;padding:6px 12px;font-size:12px;color:#7a8a99}
#dots{display:flex;gap:6px}
#dots i{width:6px;height:6px;border-radius:50%;background:#2a3a4a;display:block}
#dots i.on{background:#4ade80}
/* кнопка лога в шапке; во время записи — красная */
#lg{background:#1c2733;color:#dfe8f0;border:1px solid #2f4152;border-radius:6px;padding:3px 10px;font:inherit;font-size:12px}
#lg.rec{background:#3a1416;border-color:#f87171;color:#fca5a5}
/* плашка «есть недописанный лог» — поверх страницы, внизу */
#rv{display:none;position:fixed;left:8px;right:8px;bottom:8px;z-index:9;background:#1c2733;border:1px solid #fbbf24;
    border-radius:10px;padding:10px;font-size:13px}
/* крестики сброса (макс давления, откаты детонации) — в углу блока, под палец 32 px */
.x{position:absolute;top:0;right:0;width:32px;height:32px;border:0;background:none;color:#7a8a99;font-size:15px}
#rv button{margin:8px 8px 0 0;background:#141c26;color:#dfe8f0;border:1px solid #2f4152;border-radius:6px;padding:6px 12px;font:inherit}
#pg{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;height:calc(100vh - 34px);-webkit-overflow-scrolling:touch}
#pg::-webkit-scrollbar{display:none}
.p{min-width:100vw;scroll-snap-align:start;overflow-y:auto;padding:0 8px 16px}
.g{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.c{background:#141c26;border:1px solid #223040;border-radius:10px;padding:8px 10px}
.l{font-size:10px;color:#7a8a99;text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}
/* ЕДИНЫЙ ШРИФТ У ВСЕХ БЛОКОВ, включая тройку давления. 42px не годится: в
   треть ширины экрана «105.0» не влезает. 32 — компромисс между читаемостью
   и тем, чтобы страница не поехала. */
.v{font-size:32px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.1}
.u{font-size:12px;color:#7a8a99;font-weight:400}
/* тусклая приписка под значением — сырьё АЦП рядом с пересчитанной величиной */
.s{font-size:11px;color:#48555f;font-variant-numeric:tabular-nums;margin-top:2px}
/* строка давления: три блока мин / текущее / макс. Шрифт тот же, что везде,
   поля по бокам ужаты — иначе три числа в ряд не помещаются. */
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}
.g3 .c{padding:8px 6px}
.w{grid-column:1/-1}
.na{color:#48555f}.ok{color:#4ade80}.warn{color:#fbbf24}.bad{color:#f87171}
/* ДЕТОНАЦИЯ: мигает, пока блок снимает угол */
#knk.fire{animation:fire .45s steps(1) infinite;border-color:#f87171}
@keyframes fire{0%{background:#3a1416}50%{background:#141c26}}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-size:10px;color:#7a8a99;text-transform:uppercase;letter-spacing:.5px;
   padding:10px 6px 4px;border-bottom:1px solid #223040;background:#0b0f14}
td{padding:5px 6px;border-bottom:1px solid #161f29}
td.n{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
td.uu{color:#7a8a99;width:1%;white-space:nowrap;font-size:11px}
tr.top td{background:#111a24}
</style></head><body>
<div id=hd><span id=st class=na>подключение…</span><button id=lg>Логировать</button><span id=dots><i class=on></i><i></i></span></div>
<div id=rv><span id=rvt></span><br><button id=rvs>Скачать</button><button id=rvd>Удалить</button></div>
<div id=pg>

 <div class=p>
  <div class=g3>
   <div class=c><div class=l>Обороты</div><div class=v id=rpm>—</div></div>
   <div class=c><div class=l>УОЗ</div><div class=v id=uoz>—<span class=u> °</span></div></div>
   <div class=c><div class=l>Газ</div><div class=v id=tpsp>—<span class=u> %</span></div></div>
  </div>
  <div class=g3 style="margin:6px 0">
   <div class=c id=knk><div class=l>Детонация</div><div class=v id=corr>—<span class=u> °</span></div></div>
   <div class=c><div class=l>Откатов</div><div class=v id=kcnt>—</div></div>
   <!-- два числа в трети экрана на 32px не влезают — тут шрифт меньше -->
   <div class=c style="position:relative"><div class=l>Ср / макс</div><div class=v id=kam style="font-size:24px">—</div>
    <button id=knx class=x title="сбросить откаты">✕</button></div>
  </div>
  <div class=g style="margin-bottom:6px">
   <div class=c><div class=l>AFR цель</div><div class=v id=afrt>—</div></div>
   <div class=c><div class=l>AFR факт</div><div class=v id=afr>—</div></div>
  </div>
  <div class=g3 style="margin-bottom:6px">
   <div class=c><div class=l>мин</div><div class=v id=pmin>—</div></div>
   <div class=c><div class=l>давление кПа</div><div class=v id=kpa>—</div></div>
   <div class=c style="position:relative"><div class=l>макс</div><div class=v id=pmax>—</div>
    <button id=pmx class=x title="сбросить максимум">✕</button></div>
  </div>
  <div class=g>
   <div class=c><div class=l>Нагрузка TP</div><div class=v id=tp>—</div></div>
   <div class=c><div class=l>VE текущее</div><div class=v id=ve>—</div></div>
   <div class=c><div class=l>Впрыск</div><div class=v id=inj>—<span class=u> мс</span></div></div>
   <div class=c><div class=l>Форсунки</div><div class=v id=duty>—<span class=u> %</span></div></div>
   <div class=c><div class=l>Темп ОЖ</div><div class=v id=ect>—<span class=u> °C</span></div></div>
   <div class=c><div class=l>Темп воздуха</div><div class=v id=tv>—<span class=u> °C</span></div></div>
   <div class=c><div class=l>ALPHA</div><div class=v id=lam>—</div></div>
   <div class=c><div class=l>Напряжение</div><div class=v id=vb>—<span class=u> В</span></div></div>
  </div>
 </div>

 <div class=p><table id=tb></table></div>

</div>
<script>
const $=i=>document.getElementById(i);
function set(id,val,cls){const e=$(id);if(!e)return;const u=e.querySelector('.u');
 e.firstChild.nodeValue=val;e.className='v'+(cls?' '+cls:'');if(u)e.appendChild(u);}
/* тусклая приписка: сырьё АЦП под пересчитанной величиной */

/* ⚠ ЗНАК ПОПРАВКИ УГЛА ($14EA), подсказка панели дословно:
   «Плюс — блок ДОБАВИЛ угол, минус — СНЯЛ. Ноль — поправки нет.»
   Значит СТУК — это МИНУС. Плюс — интегратор наддаёт сверх карты, его потолок
   задан таблицей $FE70 по оборотам (до ~1845 об строго 0).
   Проверено на 27032 строках логов: положительных ниже 1845 об — НОЛЬ. */

/* ТАБЛИЦА — тот же порядок и тот же состав, что в панели на компе.
   Сверху сводка TOP (как липкие строки в панели), ниже — LABELS: параметры,
   потом сырьё АЦП. ['подпись','ключ','единица'], '' = заголовок раздела. */
const ROWS=[
 ['СВОДКА','',''],
 ['Обороты','rpm','об/мин'],
 ['Нагрузка TP','tp',''],
 ['VE текущее','ve','×'],
 ['AFR цель','afrt',''],
 ['AFR факт','afr',''],
 ['Ktps','ktps','×'],
 ['Давление','kpa','кПа'],
 ['Газ','tpsp','%'],
 ['УОЗ','uoz','°'],
 ['Впрыск','inj','мс'],
 ['Загрузка форсунок','duty','%'],
 ['Темп ОЖ','ect',''],
 ['Темп воздуха','tv','°C'],
 ['ALPHA','lam','×'],
 ['ПАРАМЕТРЫ','',''],
 ['Нагрузка (ось карт)','load',''],
 ['Наполнение мгновенное','fill',''],
 ['Дроссель открытие','tps',''],
 ['Мёртвое время форсунки','dead',''],
 ['Обогащение ускорения','acc',''],
 ['УОЗ сырьё','uozr',''],
 ['УОЗ из карты','uozm','°'],
 ['Поправка угла по детонации','corr','°'],
 ['Худший стук за сессию','kmin','°'],
 ['Откатов за сессию','kcnt','шт'],
 ['Средний откат','kavg','°'],
 ['Расход (прослойка)','flow',''],
 ['Т заряда','tz','°C'],
 ['КВТЗ','kv','×'],
 ['КТЗ','ktz','×'],
 ['Поправка VE (факт/цель)','vec','×'],
 ['Впрыск расчётный','injc','мс'],
 ['K форсунок','k',''],
 ['КМ (ДАД)','km',''],
 ['АЦП (СЫРЬЁ)','',''],
 ['АЦП Расходомер/ДАД','adc',''],
 ['Индекс температурных таблиц','tidx',''],
 ['РХХ / контур холостого','rxx',''],
 ['АЦП Напряжение борта','vbat',''],
 ['АЦП Температура ОЖ','ect',''],
 ['АЦП Лямбда','o2',''],
 ['АЦП канал 9 (ДТВ)','ch9',''],
 ['СВЯЗЬ','',''],
 ['Кадров принято','frames',''],
 ['Кадров битых','fbad',''],
 ['AFR мгновенное (из порта)','afrr',''],
 ['ШДК строк принято','wok',''],
 ['ШДК строк отброшено','wbad',''],
];
const FMT={rpm:0,tp:2,tpsp:0,inj:1,injc:1,duty:1,ve:1,ktps:3,lam:2,afrt:1,afr:1,afrr:1,vec:3,kv:3,ktz:3,kavg:1};
const TOPN=13;                 // сколько первых строк — сводка
let built=false;
function build(){let h='',n=0;
 for(const [name,k,u] of ROWS){
  if(!k){h+='<tr><th colspan=3>'+name+'</th></tr>';continue;}
  n++;
  h+='<tr'+(n<=TOPN?' class=top':'')+'><td>'+name+'</td><td class=n id="t_'+k+'">—</td><td class=uu>'+u+'</td></tr>';}
 $('tb').innerHTML=h;built=true;}

function paint(d){
 if(!built)build();
 lgRow(d);
 set('rpm',d.rpm);
 // цветом НЕ красим: богато/бедно — вопрос режима, а не порога
 set('afr', d.afr<0?'—':d.afr.toFixed(1), d.afr<0?'na':null);
 set('afrt',d.afrt.toFixed(1));
 set('tp',d.tp.toFixed(1));
 set('tpsp',d.tpsp.toFixed(0));
 set('inj',d.inj.toFixed(1));
 set('duty',d.duty.toFixed(0), d.duty>85?'bad':(d.duty>70?'warn':null));
 set('ve',d.ve.toFixed(1));
 set('uoz',d.uoz);
 set('lam',d.lam.toFixed(2));
 // Градусы — заводской тарировкой блока $FB30, вольты — оценка. Сырьё под ними
 // не выводим — оно в таблице АЦП.
 // Вне окна годности канала значение зажато к краю — приписываем знак.
 // Цветом не красим — так решено.
 set('ect', d.ect>241?'< '+d.ectc:(d.ect<3?'> '+d.ectc:''+d.ectc));
 // ТВ — как ТОЖ: в окне градусы из блока (v44), вне окна — край $FB30 со знаком
 // (блок в этот момент работает на подставных +20 °C)
 const tvT = d.ch9>241?'< '+d.tve:(d.ch9<3?'> '+d.tve:(d.tv<=-999?'—':''+d.tv));
 set('tv', tvT, tvT==='—'?'na':null);
 set('vb', d.vbv.toFixed(1));
 set('kpa',d.kpa); set('pmin',d.pmin); set('pmax',d.pmax);   // кПа — целые, 50...150
 // МИНУС = стук: мигаем красным. Плюс = блок добавил угол сверх карты.
 set('corr',(d.corr>0?'+':'')+d.corr, d.corr<0?'bad':(d.corr>0?'ok':null));
 $('knk').classList.toggle('fire', d.corr<0);
 // откаты за сессию: штуки и средняя / самая глубокая глубина
 set('kcnt', d.kcnt);
 set('kam', d.kcnt ? d.kavg.toFixed(1)+' / '+d.kmin : '—', d.kcnt?null:'na');

 for(const [,k] of ROWS){
  if(!k)continue; const e=$('t_'+k); if(!e)continue;
  let v=d[k];
  if(k==='tv'){e.className='n'+(tvT==='—'?' na':'');e.textContent=tvT;continue;}   // как на плитке
  if(v===undefined||(['afr','afrr','vec'].includes(k)&&v<0)||(k==='tz'&&v<=-999)||(k==='kavg'&&!d.kcnt)){e.textContent='—';e.className='n na';continue;}
  if(k==='corr'||k==='kmin'){e.className='n'+(v<0?' bad':(v>0?' ok':''));e.textContent=(v>0?'+':'')+v;continue;}
  e.className='n';
  e.textContent=(typeof v==='number'&&FMT[k]!==undefined)?v.toFixed(FMT[k]):v;
 }
 $('st').textContent = d.age>2000 ? ('нет кадров '+(d.age/1000|0)+' с') : ('кадров '+d.frames);
 $('st').className   = d.age>2000 ? 'bad' : 'ok';
}

/* ЛОГ СО СТРАНИЦЫ (25.10.26). Пишет БРАУЗЕР, а не плата: каждый новый кадр
   блока (d.frames изменился) — одна строка. «Стоп» отдаёт CSV тем же форматом,
   что панель логгера: разделитель «;», те же названия колонок — скрипты разбора
   едят без правок. Свои колонки — в конце.
   АВТОСОХРАНЕНИЕ: каждые 10 с (и сразу, когда страница уходит в фон) новые строки
   пишутся в IndexedDB браузера. Закрыл или обновил страницу посреди записи —
   при следующем открытии плашка предложит скачать недописанный лог.
   ⚠ На айфоне при погасшем экране Safari замирает — строк в это время нет. */
const LOGC=[['Время, с',''],['Обороты','rpm'],['Нагрузка (ось карт)','load'],['Наполнение мгновенное','fill'],
 ['Дроссель открытие','tps'],['Впрыск, мс','inj'],['Мёртвое время форсунки','dead'],['Обогащение ускорения','acc'],
 ['УОЗ сырьё','uozr'],['УОЗ из карты','uozm'],['Поправка угла по детонации, °','corr'],['Давление, кПа','kpa'],
 ['Расход (прослойка)','flow'],['VE (ДАД)','ve'],['Ktps (ДАД)','ktps'],['Коррекция по лямбде','lam'],
 ['Индекс температурных таблиц','tidx'],['РХХ / контур холостого','rxx'],['УОЗ, градусы','uoz'],['Нагрузка TP','tp'],
 ['Газ, %','tpsp'],['Темп ОЖ, °C','ectc'],['Темп воздуха, °C','tv'],['Т заряда, °C','tz'],['КВТЗ','kv'],['КТЗ','ktz'],
 ['Впрыск расчётный, мс','injc'],['Загрузка форсунок, %','duty'],['K форсунок','k'],['КМ (ДАД)','km'],
 ['AFR цель','afrt'],['AFR факт (ШДК)','afrr'],['Поправка VE (факт/цель)','vec'],
 ['АЦП Расходомер/ДАД','adc'],['АЦП Напряжение борта','vbat'],['АЦП Температура ОЖ','ect'],['АЦП Лямбда','o2'],
 ['АЦП канал 9 (свободный)','ch9'],
 ['AFR факт сглаженный','afr'],['Напряжение, В','vbv'],['Откатов за сессию','kcnt'],['Средний откат','kavg'],
 ['Худший стук за сессию','kmin'],['Часы','']];
const LG={on:false,t0:0,last:-1,rows:[],pend:[],sid:0,db:null,tm:null,warned:false};
function lgCell(k,v){
 if(v===undefined||v===null)return '';
 if((k==='tv'||k==='tz')&&v<=-999)return '';           // ТВ/ТЗ ещё не приходили
 if((k==='afr'||k==='afrr'||k==='vec')&&v<0)return '';   // ШДК молчит
 return typeof v==='number'?String(Math.round(v*1000)/1000):String(v);
}
function lgRow(d){
 if(!LG.on||d.frames===LG.last)return;
 LG.last=d.frames;
 const s=(performance.now()-LG.t0)/1000;
 const r=LOGC.map(([n,k])=>k?lgCell(k,d[k]):(n==='Часы'?new Date().toTimeString().slice(0,8):s.toFixed(2))).join(';');
 LG.rows.push(r);LG.pend.push(r);
 $('lg').textContent='Стоп · '+LG.rows.length+' · '+((s/60)|0)+':'+String((s%60)|0).padStart(2,'0');
}
// ---- IndexedDB: куски строк {sid, rows} ----
function idb(){return new Promise((ok,no)=>{let q;try{q=indexedDB.open('j30log',1);}catch(e){no(e);return;}
 q.onupgradeneeded=()=>q.result.createObjectStore('ch',{autoIncrement:true});
 q.onsuccess=()=>ok(q.result);q.onerror=()=>no(q.error);});}
function idbTx(db,mode,fn){return new Promise((ok,no)=>{const tx=db.transaction('ch',mode);const r=fn(tx.objectStore('ch'));
 tx.oncomplete=()=>ok(r&&r.result);tx.onerror=()=>no(tx.error);});}
function lgWarn(){if(LG.warned)return;LG.warned=true;
 alert('Автосохранение лога не работает в этом браузере. Запись идёт, но если закрыть страницу до «Стоп» — лог пропадёт.');}
async function lgFlush(){
 if(!LG.pend.length)return;
 const chunk={sid:LG.sid,rows:LG.pend};LG.pend=[];
 try{if(!LG.db)LG.db=await idb();await idbTx(LG.db,'readwrite',s=>s.add(chunk));}
 catch(e){console.error('автосохранение лога',e);lgWarn();}
}
function lgStamp(sid){const t=new Date(sid),p=x=>String(x).padStart(2,'0');
 return t.getFullYear()+p(t.getMonth()+1)+p(t.getDate())+'_'+p(t.getHours())+p(t.getMinutes())+p(t.getSeconds());}
function lgSave(rows,sid){
 const csv='﻿'+LOGC.map(c=>c[0]).join(';')+'\r\n'+rows.join('\r\n')+'\r\n';
 const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
 a.download='лог_ESP_'+lgStamp(sid)+'.csv';document.body.appendChild(a);a.click();
 setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},5000);
}
async function lgStart(){
 if($('rv').style.display==='block'){
  if(!confirm('Есть недописанный лог. Начать новую запись и удалить его?'))return;
  $('rv').style.display='none';
 }
 try{if(!LG.db)LG.db=await idb();await idbTx(LG.db,'readwrite',s=>s.clear());}
 catch(e){console.error('автосохранение лога',e);lgWarn();}
 Object.assign(LG,{on:true,t0:performance.now(),last:-1,rows:[],pend:[],sid:Date.now()});
 $('lg').className='rec';$('lg').textContent='Стоп · 0 · 0:00';
 LG.tm=setInterval(lgFlush,10000);
}
async function lgStop(){
 LG.on=false;clearInterval(LG.tm);
 $('lg').className='';$('lg').textContent='Логировать';
 if(!LG.rows.length){alert('Лог пустой: за время записи от блока не пришло ни одного кадра.');return;}
 lgSave(LG.rows,LG.sid);
 try{if(LG.db)await idbTx(LG.db,'readwrite',s=>s.clear());}catch(e){console.error('очистка лога',e);}
}
$('lg').onclick=()=>{LG.on?lgStop():lgStart();};
// сброс между заездами — счётчики хранит плата, сбрасывает тоже она
function rstBtn(id,url,what){$(id).onclick=async()=>{
 try{const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error(r.status);}
 catch(e){console.error('сброс',url,e);alert('Не удалось сбросить '+what+': нет связи с платой.');}
};}
rstBtn('pmx','/pmx','максимум давления');
rstBtn('knx','/knx','откаты детонации');
document.addEventListener('visibilitychange',()=>{if(document.hidden&&LG.on)lgFlush();});
// при открытии страницы: остался недописанный лог — предложить скачать
(async()=>{
 let ch;
 try{LG.db=await idb();ch=await idbTx(LG.db,'readonly',s=>s.getAll());}
 catch(e){console.error('проверка недописанного лога',e);return;}
 if(!ch||!ch.length)return;
 const rows=[].concat(...ch.map(c=>c.rows)),sid=ch[0].sid;
 $('rvt').textContent='Есть недописанный лог от '+new Date(sid).toLocaleString('ru')+': '+rows.length+' строк.';
 $('rv').style.display='block';
 $('rvs').onclick=async()=>{lgSave(rows,sid);try{await idbTx(LG.db,'readwrite',s=>s.clear());}catch(e){console.error(e);}
  $('rv').style.display='none';};
 $('rvd').onclick=async()=>{if(!confirm('Удалить недописанный лог без сохранения?'))return;
  try{await idbTx(LG.db,'readwrite',s=>s.clear());}catch(e){console.error(e);}$('rv').style.display='none';};
})();

// SSE: плата сама шлёт данные по приходу кадра
let es=null, poll=null;
function openSSE(){
 es=new EventSource('/s');
 es.onmessage=e=>{ if(poll){clearInterval(poll);poll=null;} paint(JSON.parse(e.data)); };
 es.onerror=()=>{ // не поднялось или оборвалось — переходим на опрос, EventSource сам переподключится
   if(!poll) poll=setInterval(async()=>{try{paint(await(await fetch('/d',{cache:'no-store'})).json());}catch(_){}},200);
 };
}
$('pg').addEventListener('scroll',()=>{const i=Math.round($('pg').scrollLeft/window.innerWidth);
 document.querySelectorAll('#dots i').forEach((e,n)=>e.className=n===i?'on':'');},{passive:true});
openSSE();
</script></body></html>)HTML";

// ---------------- сборка данных ----------------
static int build_json(char* b, size_t cap) {
  // Пересчёты — те же формулы, что в панели логгера.
  float rpm  = L.rpm_raw * 12.807f;
  float inj  = L.inj_raw * 0.010f;                                  // тик UPP 10 мкс
  float injc = (L.inj_raw / 1.25f + L.dead) / 2.0f * 0.010f;        // $1411 из $004D и $142C
  float duty = (rpm > 0) ? (inj * rpm / 1200.0f) : 0.0f;
  int   uoz  = 70 - int(L.uoz_raw);                                  // доставленный угол
  int   uozm = (L.uoz_map >= 128) ? (L.uoz_map - 128) : L.uoz_map;   // из карты
  int   corr = int(L.corr) - 128;    // ⚠ МИНУС = стук, ПЛЮС = блок добавил угол
  float tpsp = L.tps / 172.0f * 100.0f;                              // полный ход = 172
  if (tpsp > 100) tpsp = 100;
  float tp   = L.load / 8.0f;                                        // «Нагрузка TP» панели
  float ve   = L.ve   * 0.0078125f;
  float ktps = L.ktps * 0.0078125f;
  float lam  = L.lam  * 0.01f;
  bool  afr_ok = (L.afr > 0 && millis() - L.afr_ms < 2000);
  float afr    = afr_ok ? L.afr     : -1.0f;
  float afr_r  = afr_ok ? L.afr_raw : -1.0f;

  // AFR цель из вшитой карты смеси: ряды — обороты, колонки — нагрузка.
  // Зажим: rpm_raw/4 обязано влезть в байт оси, иначе каст завернётся.
  uint16_t rax = L.rpm_raw / 4; if (rax > 255) rax = 255;
  uint8_t fr = nearest(uint8_t(rax), FRAX);
  uint8_t fc = nearest(L.load, FCAX);
  float afrt = afr_of(pgm_read_byte(FUEL + fr * 16 + fc));
  float vec  = (afr > 0 && afrt > 0) ? (afr / afrt) : -1.0f;
  int   ectc = ect_c(L.ect);                     // градусы тарировкой блока $FB30
  // ТВ/ТЗ — как прислал блок. 0 = ещё не приходило (таблица $FB30 меньше 7 не даёт)
  int   tvc  = L.tv ? int(L.tv) - 50 : -999;
  int   tzc  = L.tz ? int(L.tz) - 50 : -999;
  // вне окна блок работает на подставных +20 — на экран, как у ТОЖ, край тарировки $FB30 со знаком
  int   tve  = ect_c(L.ch9);
  float vbv  = L.vbat * (14.0f / 175.0f);        // вольты: 175 отсчётов ~ 14 В (оценка)
  // средний откат, минусом; идущий сейчас откат входит в среднее по текущей глубине
  uint32_t ks  = L.k_sum + (L.k_in ? uint32_t(-L.k_cur) : 0);
  float kavg = L.k_cnt ? -float(ks) / L.k_cnt : 0.0f;

  return snprintf(b, cap,
    "{\"rpm\":%d,\"tp\":%.2f,\"load\":%u,\"fill\":%u,\"tps\":%u,\"tpsp\":%.1f,"
    "\"inj\":%.2f,\"injc\":%.2f,\"duty\":%.1f,\"dead\":%u,\"acc\":%u,"
    "\"uoz\":%d,\"uozr\":%u,\"uozm\":%d,\"corr\":%d,\"kmin\":%d,\"kcnt\":%u,\"kavg\":%.1f,"
    "\"kpa\":%u,\"pmin\":%u,\"pmax\":%u,\"flow\":%u,"
    "\"ve\":%.3f,\"ktps\":%.3f,\"lam\":%.2f,\"afrt\":%.1f,\"afr\":%.1f,\"afrr\":%.1f,"
    "\"vec\":%.3f,"
    "\"ectc\":%d,\"vbv\":%.1f,\"tv\":%d,\"tve\":%d,\"tz\":%d,\"kv\":%.3f,\"ktz\":%.3f,"
    "\"k\":%u,\"km\":%u,\"adc\":%u,\"tidx\":%u,\"rxx\":%u,\"vbat\":%u,\"ect\":%u,"
    "\"o2\":%u,\"ch9\":%u,\"frames\":%lu,\"fbad\":%lu,\"wok\":%lu,\"wbad\":%lu,\"age\":%lu}",
    int(rpm + 0.5f), tp, L.load, L.fill, L.tps, tpsp,
    inj, injc, duty, L.dead, L.acc,
    uoz, L.uoz_raw, uozm, corr, int(L.knock_min), unsigned(L.k_cnt), kavg,
    L.kpa, (L.kpa_min == 255 ? 0 : L.kpa_min), L.kpa_max, L.flow,
    ve, ktps, lam, afrt, afr, afr_r, vec,
    ectc, vbv, tvc, tve, tzc, L.kv / 128.0f, L.ktz / 128.0f,
    BIN_K, BIN_KM, L.adc_map, L.tidx, L.rxx, L.vbat, L.ect,
    L.o2, L.ch9, (unsigned long)L.frames, (unsigned long)L.bad,
    (unsigned long)L.wok, (unsigned long)L.wbad, (unsigned long)(millis() - L.frame_ms));
}

// ---------------- HTTP + SSE ----------------
static WiFiClient sse;          // постоянный клиент SSE, живёт между вызовами

// Выталкивание по приходу кадра. Зовётся из loop(), когда счётчик кадров вырос.
static void sse_push() {
  if (!sse || !sse.connected()) return;
  char b[900];
  int n = build_json(b, sizeof(b));
  if (n < 0 || n >= int(sizeof(b))) return;
  sse.print(F("data: "));
  sse.write((const uint8_t*)b, n);
  sse.print(F("\n\n"));
}

static void http_poll() {
  // подчистить отвалившегося слушателя
  if (sse && !sse.connected()) sse.stop();

  WiFiClient c = http.available();
  if (!c) return;

  // Первая строка запроса — в фиксированный буфер (String посимвольно
  // фрагментировал кучу: при частых запросах это заметно за час).
  char req[64]; uint8_t rl = 0; bool got = false;
  uint32_t t0 = millis();
  while (c.connected() && millis() - t0 < 400) {
    if (c.available()) {
      char ch = c.read();
      if (ch == '\n') { got = true; break; }
      if (ch != '\r' && rl < sizeof(req) - 1) req[rl++] = ch;
    } else { ecu_poll(); wbl_poll(); }     // не простаиваем: поток важнее
  }
  req[rl] = 0;
  if (!got) { c.stop(); return; }

  // Дочитать остаток заголовков. Без этого ESP32 закрывает сокет раньше, чем
  // браузер дочитал ответ, и страница иногда приходит обрезанной.
  uint8_t nl = 0;
  t0 = millis();
  while (c.connected() && millis() - t0 < 200 && nl < 2) {
    if (c.available()) { char ch = c.read(); if (ch == '\n') nl++; else if (ch != '\r') nl = 0; }
    else { ecu_poll(); wbl_poll(); }
  }

  /* Забыть запомненный адрес телефона и начать поиск заново. Кнопки на странице
     НЕТ: чтобы её нажать, надо сперва открыть страницу, а открыть её мешает
     ровно то, что кнопка чинила бы. Адрес оставлен на случай, когда телефон
     сменили совсем — дёргается руками из строки браузера.
     ⚠ ПРОВЕРЯТЬ СТРОГО ДО «/s», иначе его strstr поймает «/sta» себе. */
  if (strstr(req, "/sta")) {
    sta_known = false; sta_fail = 0; sta_next = millis();
    prefs.remove("ch");
    c.print(F("HTTP/1.1 200 OK\r\nContent-Type:text/plain; charset=utf-8\r\n"
              "Connection:close\r\n\r\nадрес телефона забыт, ищу заново"));
    c.flush(); delay(1); c.stop();
    return;
  }

  // Сброс максимума давления (крестик на странице). Новый максимум — с текущего
  // давления. Тоже ДО «/s» и «/d»: в «/pmx» их нет, но порядок держим единым.
  if (strstr(req, "/pmx")) {
    L.kpa_max = L.kpa;
    c.print(F("HTTP/1.1 200 OK\r\nContent-Type:text/plain; charset=utf-8\r\n"
              "Cache-Control:no-store\r\nConnection:close\r\n\r\nмаксимум сброшен"));
    c.flush(); delay(1); c.stop();
    return;
  }
  // Сброс откатов детонации (крестик): число, средний и худший — с нуля.
  if (strstr(req, "/knx")) {
    L.k_cnt = 0; L.k_sum = 0; L.k_in = false; L.k_cur = 0; L.knock_min = 0;
    c.print(F("HTTP/1.1 200 OK\r\nContent-Type:text/plain; charset=utf-8\r\n"
              "Cache-Control:no-store\r\nConnection:close\r\n\r\nоткаты сброшены"));
    c.flush(); delay(1); c.stop();
    return;
  }

  if (strstr(req, "/s")) {                 // ---- подписка SSE: НЕ ЗАКРЫВАЕМ ----
    if (sse) sse.stop();                   // пускаем одного слушателя
    sse = c;
    sse.print(F("HTTP/1.1 200 OK\r\nContent-Type:text/event-stream\r\n"
                "Cache-Control:no-cache\r\nConnection:keep-alive\r\n"
                "retry: 1000\r\n\r\n"));
    sse_push();                            // сразу отдать текущее состояние
    return;
  }

  if (strstr(req, "/d")) {                 // ---- запасной путь: разовый опрос ----
    char b[900];
    int n = build_json(b, sizeof(b));
    if (n > 0 && n < int(sizeof(b))) {
      c.print(F("HTTP/1.1 200 OK\r\nContent-Type:application/json\r\n"
                "Cache-Control:no-store\r\nConnection:close\r\nContent-Length:"));
      c.print(n); c.print(F("\r\n\r\n")); c.write((const uint8_t*)b, n);
    }
  } else {
    c.print(F("HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n"
              "Connection:close\r\n\r\n"));
    c.print(FPSTR(PAGE));
  }
  c.flush();
  delay(1);
  c.stop();
}

// ---------------- setup / loop ----------------
void setup() {
  Serial.begin(115200);
  delay(200);

  // Буферы приёма подняты: отдача страницы по Wi-Fi может занять дольше, чем
  // заполняется стандартный буфер 256 байт (на 15625 бод это всего ~164 мс).
  ECU.setRxBufferSize(1024);
  WBL.setRxBufferSize(512);

  // ⚠ ПЕРЕДАТЧИК ОТКЛЮЧЁН (-1). Только слушаем линию, которую читает FTDI.
  ECU.begin(ECU_BAUD, SERIAL_8N1, PIN_ECU_RX, -1);
  WBL.begin(WBL_BAUD, SERIAL_8N1, PIN_WBL_RX, -1, false);

  // Адрес телефона с прошлого раза. Он переживает снятие питания, поэтому
  // после первого удачного подключения перебор каналов больше не нужен.
  prefs.begin("j30", false);
  uint8_t ch = prefs.getUChar("ch", 0);
  sta_known  = (ch >= 1 && ch <= 14);
  if (sta_known) sta_ch = ch;

  // AP_STA: своя точка + клиент телефона ОДНОВРЕМЕННО, см. пояснение у настроек.
  WiFi.mode(WIFI_AP_STA);
  // ⭐ ТОЧКУ ПОДНИМАЕМ СРАЗУ НА КАНАЛЕ ТЕЛЕФОНА. Тогда подключение к нему не
  // двигает канал и никого с точки не выбивает. Канала не знаем — берём 6.
  WiFi.softAP(AP_NAME, AP_PASS, sta_known ? sta_ch : 6);
  WiFi.setSleep(false);          // без этого радио придерживает пакеты

  // первая попытка; дальше по таймеру в loop()
  if (sta_known) WiFi.begin(STA_NAME, STA_PASS, sta_ch);
  else           WiFi.begin(STA_NAME, STA_PASS);
  sta_next = millis() + STA_RETRY_MS;

  if (MDNS.begin(MDNS_NAME)) MDNS.addService("http", "tcp", 80);

  http.begin();
  http.setNoDelay(true);

  Serial.println();
  Serial.println(F("J30 дисплей на телефон"));
  Serial.print  (F("Своя точка : ")); Serial.print(AP_NAME);
  Serial.print  (F("  пароль ")); Serial.print(AP_PASS);
  Serial.print  (F("  ->  http://")); Serial.println(WiFi.softAPIP());
  Serial.print  (F("  канал ")); Serial.println(WiFi.channel());
  Serial.print  (F("Телефон    : ")); Serial.print(STA_NAME);
  Serial.print  (F("  ->  http://")); Serial.print(MDNS_NAME); Serial.println(F(".local"));
  if (sta_known) { Serial.print(F("  адрес из памяти, канал ")); Serial.println(sta_ch); }
  else             Serial.println(F("  адреса в памяти нет — первый поиск перебором"));
  Serial.println(F("ЭБУ: только приём, GPIO16, 15625 бод"));
  Serial.println(F("ШДК: GPIO26, 9600 бод, поток 10 Гц"));
}

/* ⭐ ГЛАВНОЕ ПРО РАДИО ESP32, ИЗ ЭТОГО РАСТЁТ ВСЁ ОСТАЛЬНОЕ:
   приёмопередатчик ОДИН, и канал у точки доступа и у клиентской части ОБЩИЙ.
   Дорого стоит не подключение к телефону, а ПОИСК: перебор всех каналов, на
   время которого своя точка ПРОПАДАЕТ ИЗ ЭФИРА на 2-3 секунды. Кто был
   подключён — отваливается, кто хотел подключиться — не видит сети.

   ПРАВИЛО ЭТОГО УЗЛА: СВОЯ ТОЧКА ВАЖНЕЕ ТЕЛЕФОНА. К J30-DASH должно быть
   можно подключиться в любую секунду, хочу — зашёл, хочу — вышел.

   КАК ЭТО ДОСТИГНУТО:

   1) АДРЕС ТЕЛЕФОНА (канал + MAC) ЛЕЖИТ В ПОСТОЯННОЙ ПАМЯТИ ПЛАТЫ и переживает
      снятие питания. Значит после первого же удачного подключения поиск больше
      не нужен никогда — есть куда идти сразу.

   2) СВОЯ ТОЧКА ПОДНИМАЕТСЯ СРАЗУ НА КАНАЛЕ ТЕЛЕФОНА. Тогда подключение к нему
      не двигает канал, и точка не моргает вообще. Раньше точка вставала на
      канал 1, а при коннекте переезжала на канал телефона — этот переезд и
      выбивал всех подключённых.

   3) ПОПЫТКИ ТОЛЬКО НАПРАВЛЕННЫЕ — на известный канал и MAC, без перебора.
      Радио остаётся на своём канале, точка В ЭФИРЕ ВСЁ ВРЕМЯ. Потому и можно
      долбиться каждые 10 секунд бесконечно, не мешая никому.

   4) ПОИСК ПЕРЕБОРОМ — только в двух случаях: адреса в памяти ещё нет
      (самый первый запуск) или направленные попытки не проходят две минуты
      подряд (телефон реально сменил канал). И ДАЖЕ ТОГДА — только если на
      точке НИКОГО НЕТ. Пока кто-то смотрит панель, перебор не запускается,
      плата ждёт, сколько понадобится.

   5) СДАВАТЬСЯ НЕКУДА: затухания нет, отказа нет. Потеряла телефон — пробует
      снова каждые 10 секунд, хоть весь день. */
/* Запомнить КАНАЛ телефона. Раньше сюда же писался его MAC и попытки шли
   строго по нему — лишняя жёсткость: iOS умеет менять адрес, и привязка
   ломалась насовсем. Канала достаточно, он экономит перебор, а промахнуться
   позволяет только на один раз. */
static void sta_remember() {
  uint8_t ch = WiFi.channel();
  if (ch < 1 || ch > 14) return;
  if (sta_known && ch == sta_ch) return;
  sta_ch = ch; sta_known = true;
  prefs.putUChar("ch", ch);
  Serial.print(F("канал телефона запомнен: ")); Serial.println(ch);
}

static void sta_poll() {
  static bool was = false;
  bool now = (WiFi.status() == WL_CONNECTED);

  if (now != was) {                       // состояние сменилось — сказать в монитор
    was = now;
    if (now) {
      sta_fail = 0; sta_busy = false;
      sta_remember();
      Serial.print(F("телефон: подключено, http://")); Serial.print(MDNS_NAME);
      Serial.print(F(".local  ("));
      Serial.print(WiFi.localIP()); Serial.println(F(")"));
      MDNS.end();                          // перезапустить, чтобы отвечать и в сети телефона
      if (MDNS.begin(MDNS_NAME)) MDNS.addService("http", "tcp", 80);
    } else {
      Serial.println(F("телефон: потерян, своя точка J30-DASH работает, пробую дальше"));
      // погасить фоновые попытки драйвера: иначе он перебирает каналы сам по
      // себе, помимо нашего таймера, и точка моргает не пойми когда
      WiFi.disconnect(false, false);
      sta_busy = false;
      sta_next = millis() + STA_RETRY_MS;
    }
  }
  if (now) return;

  /* ⭐ ПОПЫТКА В ХОДУ — НОВУЮ НЕ НАЧИНАЕМ. Ровно на этом всё и сломалось:
     вызов поверх незавершённого вызова держал радио в вечном «подключаюсь»
     и точка пропадала из эфира. Ждём, пока текущая честно закончится, и
     только ПОСЛЕ этого отсчитываем паузу — тогда наложение невозможно. */
  if (sta_busy) {
    wl_status_t s = WiFi.status();
    bool done = (s == WL_NO_SSID_AVAIL || s == WL_CONNECT_FAILED);
    if (!done && int32_t(millis() - sta_busy_t) < int32_t(STA_BUSY_MS)) return;
    sta_busy = false;
    WiFi.disconnect(false, false);          // снять повисшую попытку
    sta_next = millis() + STA_RETRY_MS;     // пауза от КОНЦА попытки, не от старта
    Serial.print(F("поиск телефона: мимо, следующая попытка через "));
    Serial.print(STA_RETRY_MS / 1000); Serial.println(F(" с"));
    return;
  }

  if (int32_t(millis() - sta_next) < 0) return;   // разностью, чтобы пережить перенос счётчика
  sta_next = millis() + STA_RETRY_MS;             // страховка, если попытка зависнет

  /* ⭐ ТРИ ПОПЫТКИ ПО ЗАПОМНЕННОМУ КАНАЛУ, КАЖДАЯ ЧЕТВЁРТАЯ — ПЕРЕБОРОМ.

     Раньше здесь был тупик, из которого плата не выходила сама: попытки шли
     строго по запомненному каналу, а сброс протухшего канала стоял под
     условием «на точке никого нет». Стоило подключиться к J30-DASH — и плата
     уже не могла ни зацепиться за телефон, ни переучиться. А раздача iPhone
     ВЫБИРАЕТ КАНАЛ ЗАНОВО ПРИ КАЖДОМ ВКЛЮЧЕНИИ, так что запомненный протухает
     постоянно.

     Теперь переучивание идёт само и не спрашивает разрешения: раз в четыре
     попытки радио всё-таки проходит по каналам и находит телефон, куда бы он
     ни переехал. Дыра в эфире на 2-3 секунды раз в две минуты — терпимо,
     вечный тупик — нет. */
  sta_fail++;
  bool sweep = !sta_known || (sta_fail % 4 == 0);

  sta_busy = true; sta_busy_t = millis();
  if (sweep) {
    Serial.println(F("поиск телефона: перебор каналов"));
    WiFi.begin(STA_NAME, STA_PASS);
  } else {
    WiFi.begin(STA_NAME, STA_PASS, sta_ch);   // быстро, точка не моргает
  }

  // Канал не сработал несколько раз подряд — считаем протухшим и забываем.
  // Никаких условий про клиентов: иначе плата опять попадёт в тупик.
  if (sta_known && sta_fail >= STA_FAIL_MAX) {
    Serial.print(F("канал ")); Serial.print(sta_ch);
    Serial.println(F(" не отвечает, забываю его"));
    sta_known = false; sta_fail = 0;
    prefs.remove("ch");
  }
}

void loop() {
  ecu_poll();      // поток ЭБУ в первую очередь
  wbl_poll();

  // ⭐ ВЫТАЛКИВАНИЕ ПО СОБЫТИЮ: как только разобрали новый кадр — сразу в SSE.
  // Именно это убирает ~100 мс, которые раньше уходили на ожидание опроса.
  static uint32_t seen = 0;
  if (L.frames != seen) { seen = L.frames; sse_push(); }

  http_poll();
  sta_poll();      // фоновая попытка зацепиться за модем

  static uint32_t t = 0;
  if (millis() - t > 5000) {
    t = millis();
    // Состояние радио в строке состояния: точка, канал, кто на ней сидит и чем
    // занят поиск телефона. Без этого «сеть пропала» приходится вычислять по
    // симптомам, а так видно сразу.
    const char* st = (WiFi.status() == WL_CONNECTED) ? "телефон+точка"
                   : sta_busy ? "точка, ищу телефон" : "точка, пауза";
    Serial.printf("[%s кан %d, на точке %u] кадров %lu (битых %lu)  ШДК %lu/%lu  "
                  "об %d  кПа %u  AFR %.1f  стук %d\n",
                  st, WiFi.channel(), WiFi.softAPgetStationNum(),
                  (unsigned long)L.frames, (unsigned long)L.bad,
                  (unsigned long)L.wok, (unsigned long)L.wbad,
                  int(L.rpm_raw * 12.807f + 0.5f), L.kpa, L.afr, int(L.knock_min));
  }
}
