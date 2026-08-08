/*
  J30 — беспроводной мост ЭБУ <-> ноутбук, с вклейкой AFR от широкополосника.

  ЗАЧЕМ: при прямом подключении ШДК к ноуту образуется кольцо по земле и наводки
  уводят показания смеси. Поэтому ноут к машине проводом не подключается вообще —
  ESP сидит в машине, а связь с панелью идёт по воздуху.

  СВЯЗЬ — ОБЕ СРАЗУ, выбираешь в панели какая удобнее:
    Bluetooth SPP  — имя "J30-LOGGER", на маке появляется как /dev/cu.*
    Wi-Fi          — точка доступа "J30-LOGGER", сокет на 192.168.4.1:2323
  Оба радио делят одну антенну по времени, но при 32 байтах раз в 400 мс это незаметно.

  ⚠ ИЗ-ЗА ДВУХ РАДИО НУЖНА РАЗМЕТКА huge_app (см. platformio.ini): в стандартную
  разметку 1.31 МБ Bluetooth и Wi-Fi вместе не влезают. Платой за это стало OTA —
  обновляться можно только по USB. Нам не мешает: плата и так на столе.

  ЖЕЛЕЗО (ESP32 DevKit, номера GPIO напечатаны на плате):
    GPIO16 (RXD_2) <- TX ЭБУ,  через делитель 10к последовательно + 20к на массу
    GPIO17 (TXD_2) -> RX ЭБУ,  напрямую (если блок не примет 3.3В — BC546B + 2 резистора)
    GPIO26         <- TX ШДК,  через 22к последовательно (у него RS232, ±12В!)
    GND            -> масса ЭБУ и ШДК
    VIN            <- +5В с LM2596
  GPIO1/GPIO3 (TXD_0/RXD_0) НЕ ТРОГАТЬ — это консоль USB, по ней плата шьётся.

  ФОРМАТ КАДРА ЭБУ (снят с парсера панели):
    AE 17 | addr_hi addr_lo | len | data[len] | chk,  chk = XOR(addr_hi..данные)

  КАК ОТДАЁТСЯ AFR: обычным кадром на псевдоадресе AFR_ADDR. Панель кладёт данные
  неизвестных адресов прямо в образ ОЗУ, поэтому со стороны панели нужна ровно одна
  строка в LABELS — парсер переделывать не надо.
*/

#include <BluetoothSerial.h>
#include <WiFi.h>

// ---------------- настройки ----------------
static const int PIN_ECU_RX = 16;
static const int PIN_ECU_TX = 17;
static const int PIN_WBL_RX = 26;
static const int PIN_LED    = 2;      // светодиод на плате

static const uint32_t ECU_BAUD = 15625;   // проверено по коду панели
static const uint32_t WBL_BAUD = 9600;    // ASCII "NN.N\r\n"

static const char* NET_NAME = "J30-LOGGER";
static const char* NET_PASS = "j30logger";   // не короче 8 символов, иначе точка не поднимется
static const uint16_t TCP_PORT = 2323;

static const uint16_t AFR_ADDR = 0x0200;  // псевдоадрес: реального ОЗУ там нет
                                          // (ОЗУ блока = $0040-$013F и $1400-$17FF)
static const uint32_t AFR_PERIOD_MS = 200;   // как часто отдавать AFR
static const uint32_t AFR_STALE_MS  = 3000;  // старее — считаем, что ШДК молчит
static const uint32_t QUIET_MS      = 800;   // тишина после команды в блок (см. ниже)

BluetoothSerial BT;
WiFiServer server(TCP_PORT);
WiFiClient  client;
HardwareSerial ECU(2);
HardwareSerial WBL(1);

// ---------------- отдача наружу ----------------
// Пишем в оба канала: кто подключён, тот и получит. Так panel-у всё равно,
// каким путём он пришёл, а переключаться можно на ходу.
static void out_write(const uint8_t* p, size_t n) {
  if (BT.hasClient()) BT.write(p, n);
  if (client && client.connected()) client.write(p, n);
  Serial.write(p, n);            // USB — третий равноправный канал
}

// ---------------- наблюдатель кадров ЭБУ ----------------
// Байты пересылаем СРАЗУ, пачкой за проход цикла — мост не должен ничего задерживать.
// Разбор идёт параллельно и нужен ровно для одного: знать, где кончился кадр,
// чтобы своё вклеивать ТОЛЬКО в стык. Вклейка в середину кадра сломала бы XOR
// и панель выбросила бы кадр целиком.
enum { S_AE, S_17, S_ADRH, S_ADRL, S_LEN, S_DATA, S_CHK };
static uint8_t  st = S_AE;
static uint8_t  need = 0;
static bool     at_boundary = false;

static void ecu_observe(uint8_t b) {
  switch (st) {
    case S_AE:   st = (b == 0xAE) ? S_17 : S_AE; break;
    case S_17:   st = (b == 0x17) ? S_ADRH : (b == 0xAE ? S_17 : S_AE); break;
    case S_ADRH: st = S_ADRL; break;
    case S_ADRL: st = S_LEN;  break;
    case S_LEN:  need = b; st = need ? S_DATA : S_CHK; break;
    case S_DATA: if (--need == 0) st = S_CHK; break;
    case S_CHK:  st = S_AE; at_boundary = true; break;   // кадр кончился — можно вклеивать
  }
}

// ---------------- разбор ШДК ----------------
static char    wbuf[12];
static char    wlast[12] = "";   // последняя пришедшая строка, как есть (для пульса)
static uint8_t wlen = 0;
static float   afr = 0.0f;
static uint32_t afr_ms = 0;

static void wbl_feed(char c) {
  if ((c >= '0' && c <= '9') || c == '.') {
    if (wlen < sizeof(wbuf) - 1) wbuf[wlen++] = c;
    return;
  }
  // любой другой символ — конец числа
  if (wlen) {
    wbuf[wlen] = 0;
    // ⚠ ТРЕБУЕМ форму NN.N — цифры, ровно одна точка, цифры после неё.
    // Раньше принималось любое число 7..25 без точки, и огрызок потерянной строки
    // ("9" от "19.2", "7" от "14.7") проходил как настоящее значение. Отсюда были
    // скачки и залипание на одной цифре. Панель разбирала строго, прошивка — нет.
    int dots = 0, before = 0, after = 0; bool bad = false;
    for (uint8_t i = 0; i < wlen; i++) {
      if (wbuf[i] == '.') { if (++dots > 1) { bad = true; break; } }
      else if (dots == 0) before++;
      else after++;
    }
    // Требуем РОВНО две цифры до точки. Формат ШДК — "NN.N", одна цифра там не
    // появляется никогда. А вот огрызок вида "8.3" от потерянного "18.3" по окну
    // 7..25 прошёл бы как настоящее значение — замечено по сырью в пульсе 08.08.26.
    if (!bad && dots == 1 && before == 2 && after >= 1) {
      float v = atof(wbuf);
      if (v >= 7.0f && v <= 25.0f) {   // то же окно, что и в панели
        afr = v;
        afr_ms = millis();
      }
    }
    // последняя строка как пришла — чтобы в пульсе было видно сырьё,
    // а не только результат: по нему сразу понятно, верна ли инверсия входа
    strncpy(wlast, wbuf, sizeof(wlast) - 1); wlast[sizeof(wlast) - 1] = 0;
    wlen = 0;
  }
}

// ---------------- отдача AFR ----------------
// value=0 — признак «ШДК молчит». Шлём его НАМЕРЕННО, а не просто перестаём слать:
// панель кладёт значение в образ ОЗУ, а оттуда оно само никогда не пропадает. Без
// этого нуля отвалившийся датчик писал бы в лог последнее число до конца заезда,
// и отличить его от настоящего было бы нельзя.
static void send_afr(float value) {
  uint16_t v = (uint16_t)(value * 100.0f + 0.5f);   // 14.70 -> 1470
  uint8_t f[8];
  f[0] = 0xAE; f[1] = 0x17;
  f[2] = AFR_ADDR >> 8; f[3] = AFR_ADDR & 0xFF;
  f[4] = 2;
  f[5] = v >> 8; f[6] = v & 0xFF;
  uint8_t c = 0;
  for (int i = 2; i <= 6; i++) c ^= f[i];            // XOR: адрес, длина, данные
  f[7] = c;
  out_write(f, 8);
}

// ---------------- счётчики для диагностики ----------------
// Без них мост — чёрный ящик: не видно ни идут ли кадры от блока, ни жив ли ШДК,
// ни подключился ли кто-нибудь. Печатаются в USB-консоль (UART0), к машине она
// не подключена, так что мешать обмену не может.
static uint32_t cnt_ecu = 0, cnt_wbl = 0, cnt_afr = 0;

// ---------------- setup ----------------
void setup() {
  pinMode(PIN_LED, OUTPUT);
  // ⚠ 15625, а НЕ 115200. USB — полноценный третий канал, и панель открывает порт
  // на скорости блока. Пока тут было 115200, по проводу шла каша и AFR не доезжал.
  Serial.begin(ECU_BAUD);
  delay(200);
  Serial.println();
  Serial.println(F("=== J30 мост ЭБУ<->ноут ==="));
  Serial.println(F("ЭБУ  : GPIO16 приём / GPIO17 передача, 15625 8N1"));
  Serial.println(F("ШДК  : GPIO26 приём, 9600 8N1, вход инвертирован (RS232)"));
  Serial.print  (F("BT   : ")); Serial.println(NET_NAME);
  Serial.print  (F("Wi-Fi: ")); Serial.print(NET_NAME);
  Serial.print  (F("  пароль ")); Serial.print(NET_PASS);
  Serial.print  (F("  сокет 192.168.4.1:")); Serial.println(TCP_PORT);
  ECU.begin(ECU_BAUD, SERIAL_8N1, PIN_ECU_RX, PIN_ECU_TX);
  // ⚠ последний параметр — ИНВЕРСИЯ. У ШДК RS232: покой это минус, а у TTL плюс.
  // Без инверсии на входе будет мусор вместо чисел.
  WBL.begin(WBL_BAUD, SERIAL_8N1, PIN_WBL_RX, -1, true);

  BT.begin(NET_NAME);
  WiFi.mode(WIFI_AP);
  WiFi.softAP(NET_NAME, NET_PASS);
  server.begin();
  server.setNoDelay(true);
}

// ---------------- loop ----------------
void loop() {
  static uint32_t last_cmd = 0, last_afr = 0, last_byte = 0;
  static uint8_t  obuf[256];

  // приём нового сетевого клиента (старого при этом закрываем — соединение одно)
  if (!client || !client.connected()) {
    WiFiClient nc = server.available();
    if (nc) { client.stop(); client = nc; client.setNoDelay(true); }
  }

  // ЭБУ -> наружу: пачкой за проход, байт в байт, ничего не меняя.
  // Копим в буфер, а не шлём по одному: по TCP каждый вызов write() ушёл бы
  // отдельным пакетом, и на 32 байта кадра получилось бы 32 пакета.
  size_t olen = 0;
  while (ECU.available() && olen < sizeof(obuf)) {
    uint8_t b = ECU.read();
    obuf[olen++] = b;
    ecu_observe(b);
    last_byte = millis();
    cnt_ecu++;
  }
  if (olen) out_write(obuf, olen);

  // наружу -> ЭБУ: команды C5/C6/C9/CA/CB идут насквозь, с любого из двух каналов
  while (BT.available()) { ECU.write((uint8_t)BT.read()); last_cmd = millis(); }
  if (client && client.connected()) {
    while (client.available()) { ECU.write((uint8_t)client.read()); last_cmd = millis(); }
  }
  while (Serial.available()) { ECU.write((uint8_t)Serial.read()); last_cmd = millis(); }

  // ШДК
  while (WBL.available()) { wbl_feed((char)WBL.read()); cnt_wbl++; }

  uint32_t now = millis();

  // Вклейка AFR. Три условия, все обязательны:
  //  1) стоим на стыке кадров — иначе порвём чужой кадр
  //  2) после команды в блок прошло QUIET_MS. Ответ на C9 идёт СЫРЫМ потоком,
  //     а не кадрами, и вклейка в него испортила бы дамп карты
  //  3) не чаще AFR_PERIOD_MS
  // Шлём ВСЕГДА, даже когда ШДК молчит — тогда нулём. Молча замолчать нельзя:
  // панель не умеет забывать once полученное значение (см. комментарий у send_afr).
  if (at_boundary && (now - last_cmd) > QUIET_MS && (now - last_afr) > AFR_PERIOD_MS) {
    bool fresh = afr_ms && (now - afr_ms) < AFR_STALE_MS;
    send_afr(fresh ? afr : 0.0f);
    cnt_afr++;
    last_afr = now;
    at_boundary = false;

    // Пульс печатаем ЗДЕСЬ ЖЕ, сразу за кадром AFR. Отдельным условием по
    // at_boundary он не работал: AFR шлётся каждые 200 мс, а стыки приходят раз
    // в ~400 мс, и свободных стыков пульсу не доставалось вообще.
    // Место безопасное — мы уже в стыке и вне окна после команды.
    static uint32_t last_beat = 0;
    if (now - last_beat > 2000) {
      last_beat = now;
      // Строка короткая НАМЕРЕННО: на 15625 бод каждый символ стоит 0.64 мс, и
      // длинный пульс заблокировал бы цикл на десятки миллисекунд.
      Serial.printf("[%lus ecu%lu wbl%lu \"%s\" afr%s bt%c net%c]\n",
                    now / 1000, cnt_ecu, cnt_wbl, wlast,
                    (afr_ms && (now - afr_ms) < AFR_STALE_MS) ? String(afr, 2).c_str() : "-",
                    BT.hasClient() ? '+' : '-',
                    (client && client.connected()) ? '+' : '-');
    }
  }

  // светодиод: горит, пока кадры от блока идут
  digitalWrite(PIN_LED, (now - last_byte) < 1000);
}
