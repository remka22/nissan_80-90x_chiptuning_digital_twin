# -*- coding: utf-8 -*-
"""
Билдер УЗКОГО (targeted) дампера v8 — шлёт только ключевые сигналы для лога.
Кадр: [AE 17][FF F0][len=13][13 байт значений][chk=XOR(FF,F0,len,data)].
Значения В ФИКС. ПОРЯДКЕ (ПК декодит по позиции), адреса в таблице ADDR.

Порядок 13 байт:
  0-1  $140A:$140B  обороты (16б)
  2    $1482        нагрузка Tp
  3    $1400        O2
  4-5  $144E:$144F  впрыск факт (16б)
  6-7  $1411:$1412  впрыск расчёт (16б)
  8    $1431        ALPHA
  9    $0015        дроссель (флаг)
  10   $004C        темп ОЖ сырьё
  11-12 $1408:$1409 MAF/давление (16б)

Скорость SCI: E/128 (RMCR=0x05, ~15625 при E=2МГц) — как v6, надёжно.
Врезка 83F8: JSR A99B -> JSR C600. Неблокирующе, 1 байт/вызов → кадр 18б за ~0.18с.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(HERE, "J30_vq_форсы_логер_20260731_1830.bin")
DST = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(HERE, "..", "логер", "J30_vq-форсы_v8-узкий_01.08.26 ИИ.bin")
ROM_BASE = 0x8000
CODE_ORG = 0xCD00   # перенесено с $C600 05.08.26: там ДАД (рутина $C700, VE $C900, Ktps $CB00)
CODE_WIN = 0x800    # сколько ПЗУ отдаём под код. Не граница железа, а наш ограничитель:
                    # за $CD00 свободно 8704 байта подряд до $EF00. Занятость проверяется
                    # побайтно при сборке, поэтому окно можно расширять без риска.
HOOK_CPU = 0x83F8
ORIG_CALL = 0xA99B

# Адреса значений В ПОРЯДКЕ КАДРА (ПК декодит по позиции). 16-бит = два адреса hi,lo.
# Все адреса ПОДТВЕРЖДЕНЫ дизасмом (трассы 01.08.26): каналы АЦП $B209, УОЗ $140F/$143B,
# флаги $0053/$0054, впрыск $1411 (НЕ $144E!), контур ХХ $142C/$4D/$144E.
# ФИНАЛЬНЫЙ логгер 02.08.26: убраны бесполезные каналы (разобрано дизасмом).
ADDR_LIST = [
    0x140A, 0x140B,   # обороты (16б)
    0x1482,           # нагрузка сглаж. (ось карт)
    0x1413,           # расход МГНОВЕННЫЙ (гэп к $1482 = транзит/газовка)
    0x1431,           # ALPHA (замкнутый цикл)
    # УБРАН $1411/$1412 «впрыск расчёт» — избыточен: восстанавливается панелью как
    # ($004D/1.25 + $142C)/2, оба входа в кадре остаются. Слоты отданы под сумму тени.
    0x17FA, 0x17FB,   # XOR тени / сумма тени (= CSX, CSS)
    # --- АЦП: только рабочие ---
    # ⚠ $1408 и $1409 — ТОЛЬКО ВМЕСТЕ. 10-битное значение лежит ПРИЖАТЫМ ВПРАВО:
    # 747 = $02EB, то есть в $1408 всего два старших бита, а восемь младших в $1409.
    # В v18 я выкинул $1409 «как ненужные два бита» — и потерял почти весь сигнал.
    0x1408, 0x1409,   # ch0 сырьё 10 бит: МАФ, на ДАД-бине — датчик давления
    0x00F7,           # ДАВЛЕНИЕ в кПа — его считает рутина ДАД ($C700), на MAF-бине мусор
    0x008F,           # ch1 напряжение борта
    0x004C,           # ch2 темп ОЖ
    0x1400,           # ch3 O2 (единственный рабочий из "плавающих"; лямбда, титан 0.4-1.5В)
    0x1492, 0x1493,   # ch6 TPS сырьё (16б)
    # УБРАНЫ: ch4 $1402 (только диагностика), ch5 $1401 (цель ХХ искрой),
    #         ch7 $1583 (вольт-фб $5000), ch8 $1574 (коррекция выключена $7EE1.0=0)
    # --- УОЗ ---
    0x140F,           # УОЗ финальный: °BTDC = 70 − байт (проверено: ХХ 55→15°)
    0x143B,           # УОЗ выбранной карты (≈градусы, база до коррекций)
    # --- ФЛАГИ: восемь полезных бит из пяти байт, собраны нами в один ($17FF) ---
    # Было пять слотов под смешанные байты, где полезны 1-2 бита, а остальное —
    # кухня планировщика. Стало два: упакованный + $0053 сырьём (в нём биты 0x08/0x40
    # выбирают таблицу порогов наката $7F40/$7F50, разобрать их ещё предстоит).
    0x17FF,           # упакованные флаги (= FLAGS, раскладка в PACKF)
    # АЦП канал 9: завод его НЕ опрашивает (карта каналов, трассы 02.08.26), софтом не занят.
    # Читаем сами и кладём в кадр — чтобы найти, выходит ли он на разъём: подать напряжение
    # на подозреваемую ногу и посмотреть, дрогнет ли. Каналы 3/4/5/8 отпадают — они шевелятся
    # от лямбды, то есть сидят на одном узле (наблюдение пользователя).
    0x17E0,           # сырьё АЦП канала 9 (= ADC9)
    0x0053,           # сырьё флагов угла — ради неразобранных бит
    0x142C,           # цель ХХ
    # УБРАНЫ: РХХ duty $004D/$004E, ошибка контура $144E (производная/если не работает — видно и так)
    # --- дроссель + обогащение ---
    0x14A2,           # TPS открытие (в панели → %, 172=100%)
    0x14DE,           # обогащение ускорения (старший байт)
    # УБРАНА: TPS скорость $14A3 (не нужна; факт обогащения виден по $14DE)
    # --- ДАД: реально выбранные из ОЗУ (пишет рутина C700; на MAF-бине = мусор) ---
    # ⚠ С v27 множители лежат в $FA/$FB (кэш, который считает основной цикл), а не
    # в $F8/$F9. Забыл поправить при переносе — в логе были нули, и разобраться,
    # какой из множителей врёт, стало нечем.
    0x00FA,           # VE выбранное (карта 0x4900, /128=1.0)
    0x00FB,           # Ktps выбранное (карта 0x4B00, /128=1.0)
    # --- РЕАЛЬНЫЙ впрыск в UPP (для ТОЧНОЙ загрузки форсунок) ---
    0x004D, 0x004E,   # $004D:$004E = длит. впрыска в отсчётах UPP; мс = ×0.010 (ТИК 10 мкс, испр. 04.08.26)
                      # впрыск последовательный (раз за цикл) -> загрузка форсунок = мс × об / 1200
    # $17F7 (результат peek) из кадра УБРАН: панель командой C6 не пользуется вообще,
    # всё чтение идёт дампом C9 и он быстрее (43 мс против кадра 400 мс). Команда в
    # прошивке осталась, просто её ответ больше не едет в каждом кадре.
    # --- ОБРАТНАЯ СВЯЗЬ: состояние тени (ЭБУ сам говорит, панель не гадает) ---
    # Раньше тут лежал указатель смеси целиком ($00CF/$00D0). Карт стало две, а тень одна,
    # поэтому в кадр идёт СОСТОЯНИЕ ТЕНИ — оно описывает любое число карт двумя байтами.
    0x17F8, 0x17F9,   # какая карта в тени (0/1/2) / вердикт по её указателю (0 ПЗУ, 1 тень, FF авария)
    0x141A,           # ЧТО ВЕРНУЛА карта топлива (результат выборки, b4b0)
    # --- ДЕТОНАЦИЯ: идёт откат угла или нет (разбор 06.08.26) ---
    # $14EA = интегратор детонации со смещением 128 (единственный писатель a1d1:
    # LDAA $1461; ADDA #$80; STAA $14EA). 128 = отката нет, меньше = блок снимает угол.
    # Сам счётчик событий $0080 логировать бесполезно: основной цикл чистит его каждый
    # проход (a0b5 CLR $0080), снимком не поймать. Интегратор же держит след ~10 проходов
    # (падает сразу на событие, возвращается по +26 из 256 за проход) — ловить надо его.
    0x14EA,           # откат по детонации; ° = 128 − байт
]
CONST2 = [0xFF, 0xF0, len(ADDR_LIST)]   # FF F0 <len>
assert len(ADDR_LIST) < 256
assert len(ADDR_LIST) <= 32, "снимок кадра рассчитан на 32 байта"

# ---- РАСКЛАДКА ПАМЯТИ — ИЗМЕРЕНА НА МАШИНЕ 04.08.26, не выдумана ----
# ОЗУ в блоке ВСЕГО 1280 байт: $0040-$013F (256 б внутри HD6303Y, верх занят стеком)
# и $1400-$17FF (1 КБ внутри HD63140). Отдельной микросхемы памяти в ЭБУ НЕТ.
# $1800-$1BFF — МЁРТВАЯ ЗОНА (читается FF), $1C00-$1FFF — ЗЕРКАЛО $1400-$17FF (A11 не
# декодируется). Версии v4-v15 клали тени и буферы в $1800+ — в никуда, отсюда все поломки.
# Замер: 23 метки из 24 уцелели за 12 с; единственная затёртая — $1600 нашим же peek.
#
#   $1400-$15FF  рабочие переменные завода
#   $1600-$16FF  ТЕНЬ КАРТЫ СМЕСИ (256 б) — единственное место, где помещается карта
#   $1700-$177F  заводская таблица самообучения (читается на ходу, база в $0074 из c1b7)
#   $1780-$17FF  наше служебное (128 б, замером подтверждено что завод не пишет)
#
# ⚠ Заводская контрольная сумма $15C0-$17FF накрывает и тень, и служебное: при каждом
# старте она не сойдётся и блок сбросит накопленное самообучение. Это известная плата.
SH_SS   = 0x1600                      # тень карты смеси, 256 б
RING, RING_MASK = 0x1780, 0x1F        # кольцо приёма 32 б   $1780-$179F
SNAP    = 0x17A0                      # снимок кадра 32 б    $17A0-$17BF
STAGE   = 0x17C0                      # буфер блока 32 б     $17C0-$17DF
BLK_MAX = 32                          # размер блока = размеру буфера
# переменные $17E0-$17FF
# УКАЗАТЕЛЬ КАРТЫ — в zero-page, во ВНУТРЕННЕМ ОЗУ процессора. Это единственная
# память, в надёжности которой сомнений нет. Завод занимает $40-$CE и там кончается;
# стек растёт вниз от $013F, до $0100 ему 64 байта и ещё 47 до $CF — переполниться
# должен на 111 байт, чтобы сюда дотянуться.
# ПОЧЕМУ ПЕРЕЕХАЛ: на v16 указатель лежал в $17E0. В топливном тракте мой патч меняет
# ровно одну инструкцию (b49e), поэтому кривая смесь могла идти только от указателя.
# Область $1780-$17FF я мерил на ЗАГЛУШЁННОМ моторе, на работающем — ни разу.
PTR_SS   = 0x00CF                     # указатель карты смеси ($16 = тень, $FD = ПЗУ)
RXSI     = 0x17E2                     # состояние автомата приёма
ADDR_PTR = 0x17E3                     # адрес для poke/peek (2 б)
SI       = 0x17E5                     # позиция в кадре
CHK      = 0x17E6                     # контрольная сумма кадра
RB_HEAD, RB_TAIL = 0x17E7, 0x17E8     # кольцо: голова/хвост
DMP_PRE, IDLE_CNT = 0x17E9, 0x17EA    # преамбула дампа / счётчик простоя
DMP_SRC  = 0x17EB                     # источник дампа (2 б)
DMP_CNT  = 0x17ED                     # осталось отдать байт
BLK_DST  = 0x17EE                     # адрес назначения блока (2 б)
BLK_PTR  = 0x17F0                     # указатель записи в буфер (2 б)
BLK_CNT  = 0x17F2                     # осталось принять
BLK_CHK  = 0x17F3                     # накопленная XOR-сумма блока
BLK_LEN  = 0x17F4                     # длина блока
ST_OK    = 0x17F5                     # счётчик принятых блоков
ST_BAD   = 0x17F6                     # счётчик отвергнутых блоков
PEEK_OUT = 0x17F7                     # результат peek (виден в кадре)
# --- выбор карты для тени (v18) ---
SEL      = 0x17F8                     # какая карта лежит в тени: 0 нет, 1 смесь, 2 угол
VERD     = 0x17F9                     # вердикт по указателю живой карты: 0 ПЗУ, 1 тень, FF авария
CSX      = 0x17FA                     # готовый XOR тени (публикуется раз в круг)
CSS      = 0x17FB                     # готовая сумма тени
CSI      = 0x17FC                     # индекс обхода тени, шаг 8
CSXW     = 0x17FD                     # накопитель XOR (незаконченный круг)
CSSW     = 0x17FE                     # накопитель суммы
ADC9     = 0x17E0                     # АЦП КАНАЛ 9 — единственный, который завод не опрашивает
FLAGS    = 0x17FF                     # УПАКОВАННЫЕ ФЛАГИ, собираем сами (см. PACKF)
PTR_SS = 0x00CF                       # (повтор для читаемости) указатель карты смеси
PTR_ADV  = 0x00D1                     # указатель карты УГЛА ($16 = тень, $FC = ПЗУ)
PTR_VE   = 0x00D3                     # указатель карты VE   (ДАД) — ОБЩИЙ с build_dad_ktps
PTR_KT   = 0x00D5                     # указатель карты Ktps (ДАД) — ОБЩИЙ с build_dad_ktps
ROM_SS = 0xFD00                       # карта смеси в ПЗУ
ROM_ADV  = 0xFC00                     # карта угла в ПЗУ
ROM_VE   = 0xC900                     # карта VE в ПЗУ   (кладёт build_dad_ktps)
ROM_KT   = 0xCB00                     # карта Ktps в ПЗУ (кладёт build_dad_ktps)
# Номера карт в команде CB. 0 = отцепить всё.
MAPS = ((1, PTR_SS, ROM_SS), (2, PTR_ADV, ROM_ADV), (3, PTR_VE, ROM_VE), (4, PTR_KT, ROM_KT))


# (метка|None, токен, операнд)
PROG = [
    (None,   "JSR",   ORIG_CALL),
    # --- одноразовый init SCI (если TE не стоит) ---
    (None,   "LDAAd", 0x11),
    (None,   "BITA#", 0x02),
    (None,   "BNE",   "PASS"),
    (None,   "LDAA#", 0x05),          # RMCR=0x05: E/128, внутр. клок, 8N async
    (None,   "STAAd", 0x10),
    (None,   "CLRe",  0x001E),        # TRCSR2=0 → 8N1
    (None,   "OIMd",  (0x1A, 0x11)),  # TE=1 + RE=1 + RIE=1 (приём + приёмное ПРЕРЫВАНИЕ)
    (None,   "LDAA#", 0x17),          # peek_ptr hi  (= PEEK_OUT >> 8)
    (None,   "STAAe", ADDR_PTR),
    (None,   "LDAA#", 0xF7),          # peek_ptr lo → указатель = PEEK_OUT ($17F7)
    (None,   "STAAe", ADDR_PTR + 1),
    (None,   "CLRe",  RXSI),        # rxsi = 0 (состояние приёма)
    (None,   "CLRe",  RB_HEAD),       # ring head = 0
    (None,   "CLRe",  RB_TAIL),       # ring tail = 0
    (None,   "CLRe",  DMP_CNT),       # dump-счётчик = 0 (дамп неактивен)
    (None,   "CLRe",  DMP_PRE),       # dump-преамбула = 0
    (None,   "CLRe",  IDLE_CNT),      # счётчик простоя приёма = 0 (ресинхрон)
    (None,   "CLRe",  ST_OK),         # счётчики блоков = 0 (ПК считает от нуля)
    (None,   "CLRe",  ST_BAD),
    (None,   "CLRe",  SEL),           # в тени ничего, обе карты на ПЗУ
    (None,   "CLRe",  VERD),
    (None,   "CLRe",  CSX),           # суммы тени и обход — с нуля
    (None,   "CLRe",  CSS),
    (None,   "CLRe",  CSI),
    (None,   "CLRe",  CSXW),
    (None,   "CLRe",  CSSW),
    (None,   "CLRe",  FLAGS),
    (None,   "CLRe",  ADC9),
    # --- раз за проход: досчитать кусок суммы тени и переосвидетельствовать указатель ---
    ("PASS", "JSR",   "CSUM"),
    (None,   "JSR",   "VERDCALC"),
    (None,   "JSR",   "PACKF"),
    (None,   "JSR",   "READ9"),
    # --- RX: дренаж кольца-буфера (наполняет MYRXISR по SCI-прерыванию). Тянем ВСЕ байты за проход. ---
    # состояние $F4; POKE ptr $F5:$F6; DUMP src/счётчик — во ВНЕШНЕМ ОЗУ ($17A9/$17AB),
    # чтобы не занимать $00F8/$00F9 — они идут в кадре как VE/Ktps (их пишет ДАД-рутина C700).
    # маркеры: C5=POKE C6=PEEK C7=карты→тень C8=карты→ПЗУ C9=дамп-региона[hi lo len].
    ("DUMP", "LDABe", RB_TAIL), # B = tail
    (None,   "LDAAe", RB_HEAD), # A = head
    (None,   "CBA",   None),          # A-B: Z=1 если tail==head (буфер пуст)
    (None,   "BNE",   "RXGO"),        # есть байт → разбор
    # --- пусто: РЕСИНХРОН. Молчание дольше ~1.1с посреди команды = протокол сбился → сброс автомата
    (None,   "LDAAe", RXSI),          # состояние != 0 (команда недобрана)?
    (None,   "BEQ",   "RXCOPY2"),     # нет — просто тишина, ничего не делаем
    (None,   "INCe",  IDLE_CNT),      # счётчик пустых проходов
    (None,   "LDAAe", IDLE_CNT),
    (None,   "CMPA#", 100),           # 100 × 11.4мс ≈ 1.1с
    (None,   "BCS",   "RXCOPY2"),
    (None,   "CLRe",  RXSI),        # автомат в исходное
    (None,   "CLRe",  IDLE_CNT),
    ("RXCOPY2","JMPe", "RXCOPY"),     # → peek+TX
    ("RXGO", "LDX#",  RING),          # база кольца ($1700, ВНЕ guard-окна)
    (None,   "ABX",   None),          # X = база + tail
    (None,   "LDAAx", 0x00),          # A = buf[tail] (принятый байт)
    (None,   "INCB",  None),          # tail++
    (None,   "ANDB#", RING_MASK),     # wrap 64
    (None,   "STABe", RB_TAIL), # сохранить tail
    (None,   "CLRe",  IDLE_CNT),      # байт пришёл → счётчик простоя сброшен
    (None,   "LDABe", RXSI),          # B = rxsi
    (None,   "CMPB#", 0),
    (None,   "BNE",   "RXS1"),
    (None,   "CMPA#", 0xC5),          # POKE?
    (None,   "BNE",   "RXCK6"),
    (None,   "LDAB#", 1),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXCK6","CMPA#", 0xC6),          # PEEK?
    (None,   "BNE",   "RXCK7"),
    (None,   "LDAB#", 4),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    # C7/C8 УБРАНЫ: они были прибиты к одной карте. Их место заняла CB с номером карты.
    ("RXCK7","CMPA#", 0xCB),          # CB = выбрать карту для тени [N]: 0 нет, 1 смесь, 2 угол
    (None,   "BNE",   "RXCK9"),
    (None,   "LDAB#", 14),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXCK9","CMPA#", 0xC9),          # C9 = дамп региона [hi lo len]
    (None,   "BNE",   "RXCKA"),
    (None,   "LDAB#", 6),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXCKA","CMPA#", 0xCA),          # CA = БЛОК с контрольной суммой [hi lo len данные chk]
    (None,   "BNE",   "DUMP"),        # неизвестный → тянуть дальше
    (None,   "LDAB#", 9),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS1", "CMPB#", 1),
    (None,   "BNE",   "RXS2"),
    (None,   "STAAe", ADDR_PTR),          # POKE: адрес hi
    (None,   "LDAB#", 2),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS2", "CMPB#", 2),
    (None,   "BNE",   "RXS3"),
    (None,   "STAAe", ADDR_PTR + 1),          # POKE: адрес lo
    (None,   "LDAB#", 3),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS3", "CMPB#", 3),
    (None,   "BNE",   "RXS4"),
    # GUARD АДРЕСА: писать МОЖНО только в тень $1800-$1FFF. Всё остальное — молча игнор.
    # Без этого сбой протокола (потерянный байт → сдвиг автомата) пишет в UPP $1000-$106F
    # (форсунки!), zero-page и живые переменные $1400-$15FF. Это тот класс, что убил машину.
    (None,   "LDABe", ADDR_PTR),          # B = старший байт адреса
    (None,   "CMPB#", 0x16),
    (None,   "BCS",   "RXPKEND"),     # < $1600 → НЕ писать
    (None,   "CMPB#", 0x17),
    (None,   "BCC",   "RXPKEND"),     # >= $1700 → НЕ писать (обучение завода и наше служебное)
    (None,   "LDXe",  ADDR_PTR),          # X = адрес ($F5:$F6)
    (None,   "STAAx", 0x00),          # [X] = значение → ЗАПИСЬ (только $1800-$1FFF)
    ("RXPKEND","CLRe", RXSI),       # rxsi = 0
    (None,   "JMPe",  "DUMP"),
    ("RXS4", "CMPB#", 4),
    (None,   "BNE",   "RXS5"),
    (None,   "STAAe", ADDR_PTR),          # PEEK: адрес hi
    (None,   "LDAB#", 5),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS5", "CMPB#", 5),
    (None,   "BNE",   "RXS6"),
    (None,   "STAAe", ADDR_PTR + 1),          # PEEK: адрес lo
    (None,   "CLRe",  RXSI),        # rxsi = 0
    (None,   "JMPe",  "DUMP"),
    ("RXS6", "CMPB#", 6),
    (None,   "BNE",   "RXS7"),
    (None,   "STAAe", DMP_SRC),       # DUMP: src hi
    (None,   "LDAB#", 7),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS7", "CMPB#", 7),
    (None,   "BNE",   "RXS8"),
    (None,   "STAAe", DMP_SRC + 1),   # DUMP: src lo
    (None,   "LDAB#", 8),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS8", "CMPB#", 8),
    (None,   "BNE",   "RXS9"),
    (None,   "STAAe", DMP_CNT),       # DUMP: len → активирует стрим
    (None,   "LDAB#", 2),
    (None,   "STABe", DMP_PRE), # преамбула 5A A5 (2 байта) перед данными → ПК синхронизируется
    (None,   "CLRe",  RXSI),        # rxsi = 0
    (None,   "JMPe",  "DUMP"),
    # --- БЛОК [CA][hi][lo][len][данные...][chk] : пишем в буфер, в тень — только при сошедшейся сумме ---
    ("RXS9", "CMPB#", 9),
    (None,   "BNE",   "RXS10"),
    (None,   "STAAe", BLK_DST),       # адрес назначения hi
    (None,   "LDAB#", 10),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS10","CMPB#", 10),
    (None,   "BNE",   "RXS11"),
    (None,   "STAAe", BLK_DST + 1),   # адрес назначения lo
    (None,   "LDAB#", 11),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("RXS11","CMPB#", 11),
    (None,   "BNE",   "RXS12"),
    (None,   "CMPA#", BLK_MAX),       # длина > буфера? отбросить команду
    (None,   "BHI",   "BLKRST"),
    (None,   "CMPA#", 0),             # длина 0? иначе счётчик уйдёт в 255 и съест 256 байт
    (None,   "BEQ",   "BLKRST"),
    (None,   "STAAe", BLK_CNT),       # осталось принять
    (None,   "STAAe", BLK_LEN),       # длина (для копирования)
    (None,   "CLRe",  BLK_CHK),       # сумма = 0
    (None,   "LDX#",  STAGE),
    (None,   "STXe",  BLK_PTR),       # указатель записи = начало буфера
    (None,   "LDAB#", 12),
    (None,   "STABe", RXSI),
    (None,   "JMPe",  "DUMP"),
    ("BLKRST","CLRe", RXSI),        # длина не влезает → сброс автомата
    (None,   "JMPe",  "DUMP"),
    ("RXS12","CMPB#", 12),
    (None,   "BNE",   "RXS13"),
    (None,   "LDXe",  BLK_PTR),       # данные → в ПРОМЕЖУТОЧНЫЙ буфер (не в карту!)
    (None,   "STAAx", 0x00),
    (None,   "INX",   None),
    (None,   "STXe",  BLK_PTR),
    (None,   "EORAe", BLK_CHK),       # сумма ^= байт
    (None,   "STAAe", BLK_CHK),
    (None,   "DECe",  BLK_CNT),
    (None,   "BNE",   "BLKMORE"),     # ещё не всё → ждём дальше
    (None,   "LDAB#", 13),            # всё принято → следующий байт = сумма
    (None,   "STABe", RXSI),
    ("BLKMORE","JMPe","DUMP"),
    ("RXS13","CMPB#", 13),
    (None,   "BNE",   "RXS14"),
    (None,   "CMPAe", BLK_CHK),       # принятая сумма == посчитанной?
    (None,   "BNE",   "BLKBAD"),
    (None,   "JSR",   "BLKCOPY"),     # ДА → применить блок в тень
    (None,   "INCe",  ST_OK),
    (None,   "CLRe",  RXSI),
    (None,   "JMPe",  "DUMP"),
    ("BLKBAD","INCe", ST_BAD),        # НЕТ → блок отброшен целиком, в карты не попало ничего
    (None,   "CLRe",  RXSI),
    (None,   "JMPe",  "DUMP"),
    # состояние 14: второй байт команды CB = номер карты. Разбирает DOCB (номер проверяется там).
    ("RXS14","JSR",   "DOCB"),
    (None,   "CLRe",  RXSI),
    (None,   "JMPe",  "DUMP"),
    # --- читаем *(указатель) → $1600 (видно в кадре как peek) ---
    ("RXCOPY","LDXe", ADDR_PTR),          # X = указатель
    (None,   "LDAAx", 0x00),          # A = *(указатель)
    (None,   "STAAe", PEEK_OUT),      # PEEK_OUT = прочитанный байт
    # --- TX: дамп-стрим (если активен) ИЛИ следующий байт кадра ---
    ("TXCHK","LDAAd", 0x11),
    (None,   "BITA#", 0x20),          # TDRE?
    (None,   "BNE",   "TXRDY"),
    (None,   "RTS",   None),           # TX занят → выход
    ("TXRDY","LDABe", DMP_CNT),       # dump-счётчик активен?
    (None,   "BEQ",   "CONT"),        # 0 → обычный кадр
    (None,   "LDABe", DMP_PRE), # преамбула осталась?
    (None,   "BEQ",   "TXDATA"),      # 0 → шлём данные
    (None,   "CMPB#", 2),
    (None,   "BNE",   "TXPA5"),
    (None,   "LDAA#", 0x5A),          # F2==2 → первый байт преамбулы
    (None,   "BRA",   "TXPEM"),
    ("TXPA5","LDAA#", 0xA5),          # F2==1 → второй байт
    ("TXPEM","STAAd", 0x13),          # TDR = байт преамбулы
    (None,   "DECB",  None),
    (None,   "STABe", DMP_PRE),
    (None,   "RTS",   None),
    ("TXDATA","LDXe", DMP_SRC),       # X = dump src
    (None,   "LDAAx", 0x00),          # A = *src
    (None,   "STAAd", 0x13),          # TDR = байт
    (None,   "INX",   None),          # src++
    (None,   "STXe",  DMP_SRC),
    (None,   "LDABe", DMP_CNT),
    (None,   "DECB",  None),          # len--
    (None,   "STABe", DMP_CNT),
    (None,   "BNE",   "TXDEND"),      # дамп ещё идёт
    # Дамп кончился. Кадр был оборван на середине, и его хвост ушёл бы из СТАРОГО снимка
    # (до 3 секунд давности), а ПК принял бы его за свежие данные. Начинаем кадр заново.
    (None,   "CLRe",  SI),        # si = 0 → следующий проход снимет новый снимок
    ("TXDEND","RTS",  None),
    ("CONT", "LDABe", SI),          # B = si
    (None,   "CMPB#", 0),
    (None,   "BNE",   "S1"),
    # si==0: НАЧАЛО КАДРА → снять ВСЕ значения в буфер ОДНОМОМЕНТНО (убирает разрыв 16-бит
    # и размазку: раньше каждый байт читался в момент своей отправки, врозь на 11.4мс).
    (None,   "JSR",   "SNAPSHOT"),
    (None,   "CLRe",  CHK),        # chk = 0
    (None,   "LDAA#", 0xAE),
    (None,   "BRA",   "EMITNC"),
    ("S1",   "CMPB#", 1),
    (None,   "BNE",   "S18"),
    (None,   "LDAA#", 0x17),
    (None,   "BRA",   "EMITNC"),
    ("S18",  "CMPB#", 5 + len(ADDR_LIST)),   # позиция чек-суммы = после всех данных
    (None,   "BNE",   "MID"),
    # si==chk: послать chk, si=0
    (None,   "LDAAe", CHK),
    (None,   "STAAd", 0x13),
    (None,   "CLRe",  SI),
    (None,   "BRA",   "DONE"),
    ("MID",  "CMPB#", 5),
    (None,   "BCS",   "CONST"),       # si 2..4 → константа
    # si 5..: значение из СНИМКА (снят целиком в начале кадра), а не чтение памяти на лету
    (None,   "SUBB#", 5),
    (None,   "LDX#",  SNAP),
    (None,   "ABX",   None),
    (None,   "LDAAx", 0x00),          # A = снимок[si-5]
    (None,   "BRA",   "EMITC"),
    ("CONST","SUBB#", 2),             # si 2,3,4 → CONST2[si-2] = FF,F0,len
    (None,   "LDX#",  "CONST2T"),
    (None,   "ABX",   None),
    (None,   "LDAAx", 0x00),
    # провал в EMITC (chk ^= A)
    ("EMITC","PSHA",  None),
    (None,   "EORAe", CHK),
    (None,   "STAAe", CHK),
    (None,   "PULA",  None),
    (None,   "STAAd", 0x13),
    (None,   "INCe",  SI),
    (None,   "BRA",   "DONE"),
    ("EMITNC","STAAd",0x13),
    (None,   "INCe",  SI),
    ("DONE", "RTS",   None),
]

# ---- Подпрограммы (ассемблируются за PROG): MYRXISR, my_init, DOC7, DOC8 ----
SUBS = [
    # MYRXISR: приёмное SCI-прерывание (вектор $FFF0). Хватает каждый байт СРАЗУ (не раз за проход),
    # кладёт в кольцо $1B00 (head $F0). Короткий — не блокирует крэнк/впрыск (в отличие от copy256).
    # Регистры A/B/X авто-сохранены аппаратно при входе в прерывание, RTI их вернёт.
    ("MYRXISR","LDAAd", 0x11),        # A = TRCSR (статус)
    (None,     "BITA#", 0x40),        # ORFE? переполнение/ошибка кадра
    (None,     "BNE",   "RXFLUSH"),   # да → байт битый: RDR прочитать, в кольцо НЕ класть
    (None,     "BITA#", 0x80),        # RDRF? байт реально принят
    (None,     "BNE",   "RXPUSH"),
    (None,     "RTI",   None),        # ни байта, ни ошибки → выход (не мусорить в кольцо)
    ("RXFLUSH","LDAAd", 0x12),        # чтение RDR снимает ORFE+RDRF
    (None,     "RTI",   None),
    ("RXPUSH", "LDAAd", 0x12),        # A = RDR (принятый байт, снимает RDRF)
    (None,     "LDABe", RB_HEAD), # B = head
    (None,     "LDX#",  RING),        # база кольца ($1700, ВНЕ guard-окна)
    (None,     "ABX",   None),        # X = база + head
    (None,     "STAAx", 0x00),        # buf[head] = байт
    (None,     "INCB",  None),        # head++
    (None,     "ANDB#", RING_MASK),   # wrap 64
    (None,     "CMPBe", RB_TAIL), # догнали tail? кольцо ПОЛНО
    (None,     "BEQ",   "RXFULL"),    # да → head НЕ двигаем: честная потеря вместо тихой порчи
    (None,     "STABe", RB_HEAD), # сохранить head
    ("RXFULL", "RTI",   None),
    # BLKCOPY: перенести принятый блок из буфера в тень. Зовётся ТОЛЬКО при сошедшейся сумме.
    # Guard: старший байт назначения $18..$1E (блок ≤64 б не может вылезти за $1FFF и задеть $2000,
    # куда завод пишет железо). Одиночный poke по-прежнему $18..$1F.
    ("BLKCOPY","LDAAe", BLK_DST),
    (None,     "CMPA#", 0x16),
    (None,     "BCS",   "BLKEND"),    # ниже тени → не копировать
    (None,     "CMPA#", 0x17),
    (None,     "BCC",   "BLKEND"),    # $1700 и выше → не копировать
    (None,     "LDX#",  STAGE),
    (None,     "STXe",  BLK_PTR),     # источник = начало буфера
    (None,     "LDAAe", BLK_LEN),
    (None,     "STAAe", BLK_CNT),     # счётчик копирования
    ("BLKLP",  "LDXe",  BLK_PTR),
    (None,     "LDAAx", 0x00),        # A = буфер[i]
    (None,     "INX",   None),
    (None,     "STXe",  BLK_PTR),
    (None,     "LDXe",  BLK_DST),
    (None,     "STAAx", 0x00),        # тень[i] = A
    (None,     "INX",   None),
    (None,     "STXe",  BLK_DST),
    (None,     "DECe",  BLK_CNT),
    (None,     "BNE",   "BLKLP"),
    ("BLKEND", "RTS",   None),
    # SNAPSHOT: снять все значения по таблице адресов в буфер $1740 ОДНОМОМЕНТНО.
    # Зовётся раз в кадр (раз в 38 проходов). 32 итерации, ~130 мкс, только ЧТЕНИЕ заводского ОЗУ.
    ("SNAPSHOT","CLRB", None),        # B = i
    ("SNAPLP", "PSHB",  None),        # сохранить i
    (None,     "ASLB",  None),        # ×2 (таблица 16-битная)
    (None,     "LDX#",  "ADDRTBL"),
    (None,     "ABX",   None),        # X = &ADDRTBL[i]
    (None,     "LDXx",  0x00),        # X = адрес значения
    (None,     "LDAAx", 0x00),        # A = значение
    (None,     "PULB",  None),        # B = i
    (None,     "LDX#",  SNAP),
    (None,     "ABX",   None),        # X = снимок + i
    (None,     "STAAx", 0x00),        # снимок[i] = значение
    (None,     "INCB",  None),
    (None,     "CMPB#", len(ADDR_LIST)),
    (None,     "BNE",   "SNAPLP"),
    (None,     "RTS",   None),
    # my_init: reset-хук. ВСЕГДА указатели карт = ПЗУ (безопасный дефолт, НЕ копия, без маркера).
    # Тень НЕ инициализируется на чипе — её заливает ПК poke'ом. Мотор всегда стартует стоково.
    # MYPTR: РАННЯЯ установка указателей — ДО того как завод сделает CLI.
    # Зачем: сброс обнуляет $0040-$013F (ae17..ae31), т.е. и наши указатели. Дальше завод
    # включает прерывания (ae44 / ae5a) и ТОЛЬКО потом доходит до my_init. В это окно
    # периодическая задача уже работает и читала бы карты по указателю $0000 — топливо и
    # угол из нулевой страницы. Встраиваемся в JSR $B00D (зовётся обоими путями ДО CLI).
    ("MYPTR", "JSR",  "ALLROM"),
    (None,    "JMPe", 0xB00D),         # → заводская рутина, её RTS вернёт куда надо
    ("MYINIT","JSR",  "ALLROM"),       # все карты = ПЗУ, безопасный дефолт
    (None,    "JMPe", 0xB0E2),         # → главный цикл
    # ALLROM: развести ВСЕ указатели по их базам в ПЗУ. Одна точка правды — используется
    # и при сбросе, и в начале каждой команды CB.
    ("ALLROM","LDX#", ROM_SS),
    (None,    "STXd", PTR_SS),
    (None,    "LDX#", ROM_ADV),
    (None,    "STXd", PTR_ADV),
    (None,    "LDX#", ROM_VE),
    (None,    "STXd", PTR_VE),
    (None,    "LDX#", ROM_KT),
    (None,    "STXd", PTR_KT),
    (None,    "RTS",  None),
    # DOCB: выбор карты для тени. A = номер (0 нет, 1 смесь, 2 угол).
    # СНАЧАЛА безусловно обе на ПЗУ, ПОТОМ выбранную на тень — промежуточных состояний нет,
    # накопленной ошибки нет, и чужой номер честно кладёт обе на ПЗУ.
    # Адреса ПЗУ зашиты здесь: ПК их не присылает и подсунуть свой не может.
    ("DOCB",  "PSHA", None),
    (None,    "JSR",  "ALLROM"),       # СНАЧАЛА безусловно все на ПЗУ
    (None,    "PULA", None),
    (None,    "CMPA#", 1),
    (None,    "BNE",  "CB2"),
    (None,    "LDX#", SH_SS),
    (None,    "STXd", PTR_SS),
    (None,    "BRA",  "CBOK"),
    ("CB2",   "CMPA#", 2),
    (None,    "BNE",  "CB3"),
    (None,    "LDX#", SH_SS),
    (None,    "STXd", PTR_ADV),
    (None,    "BRA",  "CBOK"),
    ("CB3",   "CMPA#", 3),
    (None,    "BNE",  "CB4"),
    (None,    "LDX#", SH_SS),
    (None,    "STXd", PTR_VE),
    (None,    "BRA",  "CBOK"),
    ("CB4",   "CMPA#", 4),
    (None,    "BNE",  "CB0"),
    (None,    "LDX#", SH_SS),
    (None,    "STXd", PTR_KT),
    (None,    "BRA",  "CBOK"),
    ("CB0",   "LDAA#", 0),             # номер не наш → в тени ничего
    ("CBOK",  "STAAe", SEL),
    (None,    "RTS",  None),
    # VERDCALC: раз за проход перечитать указатель ЖИВОЙ карты целиком и вынести вердикт.
    # Проверяются ОБА байта (порча младшего уводит базу карты незаметно — на это напоролись
    # на v16) и заодно что вторая карта стоит на ПЗУ (обе на тени = невозможное состояние).
    # VERDCALC: раз за проход обойти ВСЕ четыре указателя и вынести один вердикт.
    # Указатели лежат подряд ($00CF..$00D6), поэтому идём по ним индексом, а не веткой
    # на каждую карту — с четырьмя картами цепочка сравнений уже не влезала бы в ветвления.
    # Что проверяется у КАЖДОГО указателя:
    #   младший байт обязан быть нулём (порча младшего уводит базу карты незаметно — v16);
    #   старший = $16  -> карта смотрит в тень, и она ОБЯЗАНА быть той, что заявлена в SEL;
    #   старший >= $C0 -> нормальная база в ПЗУ, идём дальше;
    #   иначе          -> мусор, авария.
    ("VERDCALC","CLRe", VERD),         # по умолчанию 0 = живых нет, всё на ПЗУ
    (None,    "LDAB#", 0),             # B = смещение указателя (0,2,4,6)
    ("VDLP",  "PSHB",  None),
    (None,    "LDX#",  PTR_SS),
    (None,    "ABX",   None),          # X = адрес указателя карты
    (None,    "LDAAx", 1),             # младший байт
    (None,    "BNE",   "VDBADP"),
    (None,    "LDAAx", 0),             # старший байт
    (None,    "CMPA#", SH_SS >> 8),
    (None,    "BEQ",   "VDSH"),
    (None,    "CMPA#", 0xC0),          # все базы карт в ПЗУ выше $C000
    (None,    "BCS",   "VDBADP"),
    (None,    "BRA",   "VDNXT"),
    ("VDSH",  "PULB",  None),          # эта карта смотрит в тень
    (None,    "PSHB",  None),
    (None,    "LSRB",  None),          # B = индекс карты 0..3
    (None,    "INCB",  None),          # B = номер карты 1..4
    (None,    "CMPBe", SEL),
    (None,    "BNE",   "VDBADP"),      # в тени лежит НЕ та карта, что заявлена
    (None,    "LDAA#", 1),
    (None,    "STAAe", VERD),
    ("VDNXT", "PULB",  None),
    (None,    "ADDB#", 2),
    (None,    "CMPB#", 8),
    (None,    "BNE",   "VDLP"),
    (None,    "RTS",   None),
    ("VDBADP","PULB",  None),          # снять счётчик со стека и объявить аварию
    (None,    "LDAA#", 0xFF),
    (None,    "STAAe", VERD),
    (None,    "RTS",   None),
    # PACKF: восемь полезных бит из пяти смешанных байт — в один $17FF.
    # Зачем: в кадре эти байты занимали пять слотов, а несли по 1-2 бита; остальное —
    # флаги планировщика задач, к мотору отношения не имеющие. Все пять адресов лежат
    # в нулевой странице, поэтому читаются коротким TIM.
    #   бит0 отсечка топлива      $0054.01   (доказано: в этих строках впрыск ровно 0)
    #   бит1 впрыск разрешён      $0054.04   (8d4b: не стоит — расчёт пропускается)
    #   бит2 замкнутый цикл       $00AE.80
    #   бит3 крэнк                $0053.02   (подтверждено веткой удвоения впрыска 8d2c)
    #   бит4 нейтраль             $0053.04   (сошлось с $0015.20 строка в строку)
    #   бит5 холостой ход         $0053.01
    #   бит6 стартер              $0015.80
    #   бит7 неисправность TPS    $00B9.20
    # READ9: прочитать АЦП канал 9. Своих SEI/CLI не ставим — $B209 атомарна сама
    # (начинается SEI, кончается CLI) и канал задаёт при каждом вызове, так что
    # заводские замеры этим не портятся.
    ("READ9","LDAB#", 9),
    (None,  "JSR",   0xB209),
    (None,  "STABe", ADC9),
    (None,  "RTS",   None),
    ("PACKF","CLRB",  None),
    (None,  "TIMd",  (0x01, 0x54)), (None, "BEQ", "PF1"), (None, "ORAB#", 0x01),
    ("PF1", "TIMd",  (0x04, 0x54)), (None, "BEQ", "PF2"), (None, "ORAB#", 0x02),
    ("PF2", "TIMd",  (0x80, 0xAE)), (None, "BEQ", "PF3"), (None, "ORAB#", 0x04),
    ("PF3", "TIMd",  (0x02, 0x53)), (None, "BEQ", "PF4"), (None, "ORAB#", 0x08),
    ("PF4", "TIMd",  (0x04, 0x53)), (None, "BEQ", "PF5"), (None, "ORAB#", 0x10),
    ("PF5", "TIMd",  (0x01, 0x53)), (None, "BEQ", "PF6"), (None, "ORAB#", 0x20),
    ("PF6", "TIMd",  (0x80, 0x15)), (None, "BEQ", "PF7"), (None, "ORAB#", 0x40),
    ("PF7", "TIMd",  (0x20, 0xB9)), (None, "BEQ", "PF8"), (None, "ORAB#", 0x80),
    ("PF8", "STABe", FLAGS),
    (None,  "RTS",   None),
    # CSUM: XOR и сумма содержимого тени. Считаем по 8 байт за проход — за 32 прохода полный
    # круг, то есть свежая пара примерно раз в кадр. Индекс держим кратным 8 маской, иначе
    # одна порча CSI и круг никогда не замкнётся. Публикуем только по замыканию круга,
    # чтобы ПК не увидел половину старой и половину новой суммы.
    ("CSUM",  "LDABe", CSI),
    (None,    "LDX#",  SH_SS),
    (None,    "ABX",   None),          # X = тень + индекс
    (None,    "LDAB#", 8),
    ("CSLP",  "LDAAe", CSXW),
    (None,    "EORAx", 0x00),
    (None,    "STAAe", CSXW),
    (None,    "LDAAe", CSSW),
    (None,    "ADDAx", 0x00),
    (None,    "STAAe", CSSW),
    (None,    "INX",   None),
    (None,    "DECB",  None),
    (None,    "BNE",   "CSLP"),
    (None,    "LDAAe", CSI),
    (None,    "ADDA#", 8),
    (None,    "ANDA#", 0xF8),
    (None,    "STAAe", CSI),
    (None,    "BNE",   "CSEND"),       # круг не замкнулся
    (None,    "LDAAe", CSXW),
    (None,    "STAAe", CSX),
    (None,    "LDAAe", CSSW),
    (None,    "STAAe", CSS),
    (None,    "CLRe",  CSXW),
    (None,    "CLRe",  CSSW),
    ("CSEND", "RTS",   None),
]

# ---- In-place патчи заводского кода (редиректы + reset-хуки) ----
# (cpu_addr, ожидаемые_СТАРЫЕ_байты, новые_байты | "MYINIT")
INPLACE = [
    # LDX #imm → LDX расширенная: те же 3 байта, заполнитель не нужен. Форма проверена на v5 (мотор ехал).
    (0xB49E, [0xCE,0xFD,0x00], [0xDE, PTR_SS & 0xFF, 0x01]),          # сс:   LDX #FD00 → LDX $CF ; NOP
    (0xB728, [0xCE,0xFC,0x00], [0xDE, PTR_ADV & 0xFF, 0x01]),         # угол: LDX #FC00 → LDX $D1 ; NOP
    # K/гейт больше НЕ тенятся — читают ПЗУ ($FF2B/$FF91), редирект убран (нет загрузочной копии скаляров)
    (0xAE4E, [0x7E,0xB0,0xE2], "MYINIT"),                            # reset JMP b0e2 → JMP my_init
    (0xAE5B, [0x7E,0xB0,0xE2], "MYINIT"),
    # РАННИЙ хук: оба пути сброса зовут B00D ДО CLI → там и ставим указатели,
    # чтобы в окне «прерывания уже включены, my_init ещё не дошёл» карты не читались с $0000
    (0xAE41, [0xBD,0xB0,0x0D], "MYPTR"),                             # путь A (ae44 CLI)
    (0xAE57, [0xBD,0xB0,0x0D], "MYPTR"),                             # путь B (ae5a CLI)
]

LEN = {"JSR":3,"LDAAd":2,"LDAA#":2,"LDAAx":2,"LDABd":2,"LDXx":2,"LDX#":3,"BITA#":2,
       "CMPB#":2,"CMPA#":2,"LDAB#":2,"SUBB#":2,"ASLB":1,"ABX":1,"STAAd":2,"STAAe":3,"STABd":2,"STAAx":2,"LDXd":2,"EORAd":2,"CLRe":3,"INCe":3,
       "CLRB":1,"INCB":1,"LDAAe":3,"STXe":3,"STXd":2,"LDDe":3,"STDe":3,"JMPe":3,
       "LDXe":3,"DECe":3,"EORAe":3,"CMPAe":3,"LDABe":3,"STABe":3,"CMPBe":3,
       "PSHA":1,"PULA":1,"PSHB":1,"PULB":1,"CMPBd":2,"BHI":2,
       "OIMd":3,"RTS":1,"RTI":1,"CBA":1,"ANDB#":2,"DECB":1,"INX":1,"BNE":2,"BEQ":2,"BCC":2,"BCS":2,"BRA":2,
       "EORAx":2,"ADDAx":2,"ADDA#":2,"ANDA#":2,"LSRB":1,"ADDB#":2,"TIMd":3,"ORAB#":2}
BR = {"BNE":0x26,"BEQ":0x27,"BCC":0x24,"BCS":0x25,"BRA":0x20,"BHI":0x22}


def assemble(org):
    CODE = PROG + SUBS
    code_len = sum(LEN[op] for _, op, _ in CODE)
    addrtbl = org + code_len
    const2t = addrtbl + 2 * len(ADDR_LIST)
    datalabels = {"ADDRTBL": addrtbl, "CONST2T": const2t}
    # метки кода (PROG + подпрограммы SUBS)
    labels = {}; pc = org
    for lab, op, arg in CODE:
        if lab: labels[lab] = pc
        pc += LEN[op]
    alllab = dict(datalabels); alllab.update(labels)   # имена для JSR/LDX#
    # сборка кода
    out = bytearray(); pc = org
    for lab, op, arg in CODE:
        nxt = pc + LEN[op]
        if   op == "JSR":
            a = alllab[arg] if isinstance(arg, str) else arg
            out += bytes([0xBD, a >> 8, a & 0xFF])
        elif op == "LDAA#": out += bytes([0x86, arg & 0xFF])
        elif op == "LDAAd": out += bytes([0x96, arg & 0xFF])
        elif op == "LDAAx": out += bytes([0xA6, arg & 0xFF])
        elif op == "LDABd": out += bytes([0xD6, arg & 0xFF])
        elif op == "LDXx":  out += bytes([0xEE, arg & 0xFF])
        elif op == "LDX#":
            a = alllab[arg] if isinstance(arg, str) else arg
            out += bytes([0xCE, a >> 8, a & 0xFF])
        elif op == "BITA#": out += bytes([0x85, arg & 0xFF])
        elif op == "CMPB#": out += bytes([0xC1, arg & 0xFF])
        elif op == "SUBB#": out += bytes([0xC0, arg & 0xFF])
        elif op == "ASLB":  out += bytes([0x58])
        elif op == "ABX":   out += bytes([0x3A])
        elif op == "STAAd": out += bytes([0x97, arg & 0xFF])
        elif op == "STAAe": out += bytes([0xB7, arg >> 8, arg & 0xFF])
        elif op == "CMPA#": out += bytes([0x81, arg & 0xFF])
        elif op == "LDAB#": out += bytes([0xC6, arg & 0xFF])
        elif op == "STABd": out += bytes([0xD7, arg & 0xFF])
        elif op == "STAAx": out += bytes([0xA7, arg & 0xFF])
        elif op == "LDXd":  out += bytes([0xDE, arg & 0xFF])
        elif op == "EORAd": out += bytes([0x98, arg & 0xFF])
        elif op == "CLRe":  out += bytes([0x7F, arg >> 8, arg & 0xFF])
        elif op == "INCe":  out += bytes([0x7C, arg >> 8, arg & 0xFF])
        elif op == "CLRB":  out += bytes([0x5F])
        elif op == "INCB":  out += bytes([0x5C])
        elif op == "LDAAe": out += bytes([0xB6, arg >> 8, arg & 0xFF])
        elif op == "STXe":  out += bytes([0xFF, arg >> 8, arg & 0xFF])
        elif op == "STXd":  out += bytes([0xDF, arg & 0xFF])
        elif op == "LDDe":  out += bytes([0xFC, arg >> 8, arg & 0xFF])
        elif op == "STDe":  out += bytes([0xFD, arg >> 8, arg & 0xFF])
        elif op == "JMPe":
            a = alllab[arg] if isinstance(arg, str) else arg
            out += bytes([0x7E, a >> 8, a & 0xFF])
        elif op == "LDXe":  out += bytes([0xFE, arg >> 8, arg & 0xFF])
        elif op == "DECe":  out += bytes([0x7A, arg >> 8, arg & 0xFF])
        elif op == "EORAe": out += bytes([0xB8, arg >> 8, arg & 0xFF])
        elif op == "CMPAe": out += bytes([0xB1, arg >> 8, arg & 0xFF])
        elif op == "LDABe": out += bytes([0xF6, arg >> 8, arg & 0xFF])
        elif op == "STABe": out += bytes([0xF7, arg >> 8, arg & 0xFF])
        elif op == "CMPBe": out += bytes([0xF1, arg >> 8, arg & 0xFF])
        elif op == "PSHA":  out += bytes([0x36])
        elif op == "PULA":  out += bytes([0x32])
        elif op == "PSHB":  out += bytes([0x37])
        elif op == "PULB":  out += bytes([0x33])
        elif op == "CMPBd": out += bytes([0xD1, arg & 0xFF])
        elif op == "OIMd":  out += bytes([0x72, arg[0], arg[1]])
        elif op == "RTS":   out += bytes([0x39])
        elif op == "RTI":   out += bytes([0x3B])
        elif op == "CBA":   out += bytes([0x11])
        elif op == "ANDB#": out += bytes([0xC4, arg & 0xFF])
        elif op == "DECB":  out += bytes([0x5A])
        elif op == "INX":   out += bytes([0x08])
        elif op == "EORAx": out += bytes([0xA8, arg & 0xFF])
        elif op == "ADDAx": out += bytes([0xAB, arg & 0xFF])
        elif op == "ADDA#": out += bytes([0x8B, arg & 0xFF])
        elif op == "ANDA#": out += bytes([0x84, arg & 0xFF])
        elif op == "LSRB":  out += bytes([0x54])
        elif op == "ADDB#": out += bytes([0xCB, arg & 0xFF])
        elif op == "TIMd":  out += bytes([0x7B, arg[0], arg[1]])
        elif op == "ORAB#": out += bytes([0xCA, arg & 0xFF])
        elif op in BR:
            rel = labels[arg] - nxt
            assert -128 <= rel <= 127, "ветвление %s вне диапазона %d" % (arg, rel)
            out += bytes([BR[op], rel & 0xFF])
        else:
            raise ValueError(op)
        pc = nxt
    assert len(out) == code_len
    # таблицы данных
    for a in ADDR_LIST:
        out += bytes([a >> 8, a & 0xFF])
    out += bytes(CONST2)
    return out, addrtbl, const2t, labels


# ---- САМОПРОВЕРКА РАСКЛАДКИ (чтобы адрес в кадре не разошёлся с константой) ----
_LIVE = [(0x0040, 0x013F), (0x1400, 0x17FF)]          # ВСЯ реальная память блока, замер 04.08.26
def _alive(a): return any(lo <= a <= hi for lo, hi in _LIVE)
# PEEK_OUT в кадре БОЛЬШЕ НЕ НУЖЕН: панель командой C6 не пользуется, всё чтение
# идёт дампом C9 (быстрее). Команда в прошивке осталась, результат кладётся в
# $17F7 — прочитать его можно тем же дампом, если понадобится.
assert PEEK_OUT not in ADDR_LIST or True
assert SEL  in ADDR_LIST,     "номер карты в тени не попал в кадр — панель не узнает что живо"
assert VERD in ADDR_LIST,     "вердикт по указателю не попал в кадр — порча указателя будет не видна"
assert CSX  in ADDR_LIST and CSS in ADDR_LIST, "суммы тени не попали в кадр"
# Указатели ОБЯЗАНЫ лежать подряд по 2 байта от PTR_SS — VERDCALC ходит по ним индексом.
assert [p for _n, p, _r in MAPS] == [PTR_SS + 2 * i for i in range(len(MAPS))], \
    "указатели карт должны идти подряд по 2 байта от $%04X" % PTR_SS
assert PTR_SS >= 0x00CF and PTR_SS + 2 * len(MAPS) - 1 <= 0x00EE, \
    "указатели вышли за безопасный кусок zero-page $CF-$EE (дальше запас под стек)"
assert all(r >= 0xC000 for _n, _p, r in MAPS), \
    "VERDCALC считает признаком ПЗУ старший байт >= $C0 — база карты ниже сломает вердикт"
assert ADC9 < RXSI, "байт канала 9 залез в служебные переменные"
assert FLAGS <= 0x17FF, "служебные байты вышли за ОЗУ"
assert FLAGS in ADDR_LIST, "упакованные флаги не попали в кадр"
assert 0x1408 in ADDR_LIST and 0x1409 in ADDR_LIST, \
    "$1408 и $1409 только вместе: 10-битное значение прижато вправо, в $1408 лишь 2 бита"
for _n, _a, _sz in (("тень", SH_SS, 256), ("кольцо", RING, RING_MASK + 1), ("снимок", SNAP, len(ADDR_LIST)),
                    ("буфер блока", STAGE, BLK_MAX), ("переменные", RXSI, 0x1800 - RXSI),
                    ("указатель карты", PTR_SS, 2)):
    assert _alive(_a) and _alive(_a + _sz - 1), \
        "%s $%04X-$%04X вне реальной памяти ($1800+ НЕ СУЩЕСТВУЕТ)" % (_n, _a, _a + _sz - 1)
assert SNAP + len(ADDR_LIST) <= STAGE, "снимок кадра залезает в буфер блока"
assert STAGE + BLK_MAX <= RXSI,        "буфер блока залезает в переменные"
assert PTR_SS + 1 < 0x00CF + 0x20 and PTR_SS >= 0x00CF, "указатель карты должен быть в zero-page $CF+"
assert SH_SS + 256 <= 0x1700,          "тень залезает в таблицу самообучения завода"


def _check_dad_agreement():
    """Рутина ДАД читает базы VE/Ktps из НАШИХ указателей. Если адреса в двух билдерах
    разойдутся, ДАД будет брать карту по чужому адресу — мотор поедет на мусоре, и
    никакая проверка в бине этого не покажет. Поэтому сверяем исходники напрямую."""
    import re
    p = os.path.join(HERE, "..", "j30_дад", "build_dad_ktps ИИ.py")
    if not os.path.exists(p):
        return "билдер ДАД не найден, сверка адресов пропущена"
    src = open(p, encoding="utf-8").read()
    for name, want in (("PTR_VE", PTR_VE), ("PTR_KT", PTR_KT)):
        m = re.search(r"^%s\s*=\s*(0x[0-9A-Fa-f]+)" % name, src, re.M)
        assert m, "в билдере ДАД нет %s — он ещё не переведён на указатели" % name
        got = int(m.group(1), 16)
        assert got == want, "%s разъехался: тут $%04X, в билдере ДАД $%04X" % (name, want, got)
    for name, want in (("VEMAP", ROM_VE), ("KTPS", ROM_KT)):
        m = re.search(r"^%s\s*=\s*(0x[0-9A-Fa-f]+)" % name, src, re.M)
        assert m and int(m.group(1), 16) == want, \
            "%s в билдере ДАД не $%04X — база карты разъехалась" % (name, want)
    return "адреса карт ДАД сверены с билдером ДАД: ОК"


def main():
    rom = bytearray(open(SRC, "rb").read()); assert len(rom) == 32768
    print(" ", _check_dad_agreement())
    code, addrtbl, const2t, labels = assemble(CODE_ORG)
    off = CODE_ORG - ROM_BASE
    # Окно патча — 1 КБ от CODE_ORG. Мёртвая зона ПЗУ $C600-$EFFF заполнена 0x3F, по
    # дизассемблеру ни одна инструкция туда не адресуется (проверено 04.08.26).
    # ПЕРЕНЕСЕНО с $C600 на $CD00 (05.08.26): на $C600 старый логгер, на $C700 рутина ДАД,
    # на $C900 карта VE, на $CB00 Ktps. Раньше билдер писал поверх них МОЛЧА.
    assert len(code) <= CODE_WIN, "не влезает в окно $%04X-$%04X (%d байт)" % (
        CODE_ORG, CODE_ORG + CODE_WIN - 1, len(code))
    hoff = HOOK_CPU - ROM_BASE
    tgt = rom[hoff + 1] << 8 | rom[hoff + 2]
    assert rom[hoff] == 0xBD, "по 83F8 не JSR (в бине %02X)" % rom[hoff]
    assert tgt == ORIG_CALL or 0xC600 <= tgt <= 0xEFFF, \
        "по 83F8 JSR $%04X — это не заводской $A99B и не патч в мёртвой зоне" % tgt
    # ЗАНЯТОСТЬ ОКНА. Если хук уже смотрит в наше окно — там наша прошлая сборка, её
    # перезаписывать можно. Иначе окно обязано быть пустым (0x3F), иначе мы затрём
    # чужой патч и узнаем об этом только по мотору.
    if tgt != CODE_ORG:
        busy = [a for a in range(CODE_ORG, CODE_ORG + len(code)) if rom[a - ROM_BASE] != 0x3F]
        assert not busy, "окно $%04X занято: %d байт, первый $%04X — там чужой патч" % (
            CODE_ORG, len(busy), busy[0])
    rom[off:off + len(code)] = code
    rom[hoff + 1], rom[hoff + 2] = CODE_ORG >> 8, CODE_ORG & 0xFF
    # in-place патчи заводского кода (редиректы + reset-хуки) с проверкой СТАРЫХ байт
    myinit = labels["MYINIT"]
    for cpu, oldb, newb in INPLACE:
        o = cpu - ROM_BASE
        cur = list(rom[o:o + len(oldb)])
        assert cur == oldb, "in-place %04X: ожидал %s, в бине %s" % (cpu, [hex(b) for b in oldb], [hex(b) for b in cur])
        if newb == "MYINIT":                       # JMP my_init (заменяет заводской JMP)
            nb = [0x7E, myinit >> 8, myinit & 0xFF]
        elif newb == "MYPTR":                      # JSR my_ptr (заменяет заводской JSR — вызов!)
            mp = labels["MYPTR"]; nb = [0xBD, mp >> 8, mp & 0xFF]
        else:
            nb = newb
        rom[o:o + len(nb)] = bytes(nb)
    print("  my_init @ %04X; in-place патчей: %d" % (myinit, len(INPLACE)))
    # хук SCI-вектора $FFF0 (был → $ADAA заводской SCI-загрузчик) → наш MYRXISR
    rxisr = labels["MYRXISR"]
    vo = 0xFFF0 - ROM_BASE
    assert rom[vo] == 0xAD and rom[vo + 1] == 0xAA, "SCI-вектор $FFF0 не $ADAA (в бине %02X%02X)" % (rom[vo], rom[vo + 1])
    rom[vo], rom[vo + 1] = rxisr >> 8, rxisr & 0xFF
    print("  SCI-вектор $FFF0 → MYRXISR @ %04X" % rxisr)
    # чек-сумма
    s = x = 0
    for i in range(len(rom)):
        if i in (0x7F7A, 0x7F7B): continue
        s = (s + rom[i]) & 0xFF; x ^= rom[i]
    rom[0x7F7A], rom[0x7F7B] = s, x
    open(DST, "wb").write(rom)
    print("Готово:", os.path.basename(DST))
    print("  код+таблицы %d байт @ %04X..%04X" % (len(code), CODE_ORG, CODE_ORG + len(code) - 1))
    print("  ADDRTBL @ %04X, CONST2 @ %04X" % (addrtbl, const2t))
    print("  чек-сумма: %02X/%02X" % (s, x))


if __name__ == "__main__":
    main()
