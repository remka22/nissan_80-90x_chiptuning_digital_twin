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
CODE_ORG = 0xC600
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
    0x1411, 0x1412,   # ВПРЫСК факт (16б)
    # --- АЦП: только рабочие ---
    0x1408, 0x1409,   # ch0 MAF (16б)
    0x008F,           # ch1 напряжение борта
    0x004C,           # ch2 темп ОЖ
    0x1400,           # ch3 O2 (единственный рабочий из "плавающих"; лямбда, титан 0.4-1.5В)
    0x1492, 0x1493,   # ch6 TPS сырьё (16б)
    # УБРАНЫ: ch4 $1402 (только диагностика), ch5 $1401 (цель ХХ искрой),
    #         ch7 $1583 (вольт-фб $5000), ch8 $1574 (коррекция выключена $7EE1.0=0)
    # --- УОЗ ---
    0x140F,           # УОЗ финальный: °BTDC = 70 − байт (проверено: ХХ 55→15°)
    0x143B,           # УОЗ выбранной карты (≈градусы, база до коррекций)
    0x0053,           # флаги источника угла: б0=ХХ б1=крэнк б2=нейтраль (какая карта активна)
    # --- концевики / режим ---
    0x0015,           # банк концевиков: 0x80=СТАРТЕР (255=крутит стартером)
    0x0054,           # флаг ХХ/газ (б0)
    0x142C,           # цель ХХ
    # УБРАНЫ: РХХ duty $004D/$004E, ошибка контура $144E (производная/если не работает — видно и так)
    # --- дроссель + обогащение ---
    0x14A2,           # TPS открытие (в панели → %, 172=100%)
    0x14DE, 0x14DF,   # обогащение ускорения (было/не было при снапшоте AFR, 16б)
    0x00B9,           # флаг TPS: бит0x20 = ХХ/WOT/неисправность
    0x00AE,           # бит0x80 = вход в замкнутый цикл
    # УБРАНА: TPS скорость $14A3 (не нужна; факт обогащения виден по $14DE)
    # --- ДАД: реально выбранные из ОЗУ (пишет рутина C700; на MAF-бине = мусор) ---
    0x00F8,           # VE выбранное (карта 0x4900, /128=1.0)
    0x00F9,           # Ktps выбранное (карта 0x4B00, /128=1.0)
    # --- RX-ТЕСТ: последний принятый по SCI байт (патч кладёт сюда) ---
    0x1600,           # RX-тест: приём SCI. Буфер загрузчика — на ЗАГЛУШЁННОМ свободен
]
CONST2 = [0xFF, 0xF0, len(ADDR_LIST)]   # FF F0 <len>
assert len(ADDR_LIST) < 256

# (метка|None, токен, операнд)
PROG = [
    (None,   "JSR",   ORIG_CALL),
    # --- одноразовый init SCI (если TE не стоит) ---
    (None,   "LDAAd", 0x11),
    (None,   "BITA#", 0x02),
    (None,   "BNE",   "DUMP"),
    (None,   "LDAA#", 0x05),          # RMCR=0x05: E/128, внутр. клок, 8N async
    (None,   "STAAd", 0x10),
    (None,   "CLRe",  0x001E),        # TRCSR2=0 → 8N1
    (None,   "OIMd",  (0x0A, 0x11)),  # TE=1 + RE=1 (приём включён)
    (None,   "LDAA#", 0x16),          # peek_ptr hi = 0x16
    (None,   "STAAd", 0xF5),
    (None,   "CLRe",  0x00F6),        # peek_ptr lo = 0 → указатель = $1600
    (None,   "CLRe",  0x00F4),        # rxsi = 0 (состояние приёма)
    # --- RX: протокол команд. [C5 hi lo val]=POKE(запись), [C6 hi lo]=PEEK(указатель) ---
    # состояние в $F4, указатель адреса в $F5(hi):$F6(lo). Значение $1600 = *(указатель).
    ("DUMP", "LDAAd", 0x11),          # TRCSR
    (None,   "BITA#", 0x80),          # RDRF? принят байт
    (None,   "BEQ",   "RXCOPY"),      # нет байта → к чтению peek
    (None,   "LDAAd", 0x12),          # A = принятый байт (сброс RDRF)
    (None,   "LDABd", 0xF4),          # B = rxsi
    (None,   "CMPB#", 0),
    (None,   "BNE",   "RXS1"),
    (None,   "CMPA#", 0xC5),          # маркер POKE?
    (None,   "BNE",   "RXCK6"),
    (None,   "LDAB#", 1),
    (None,   "STABd", 0xF4),
    (None,   "BRA",   "RXCOPY"),
    ("RXCK6","CMPA#", 0xC6),          # маркер PEEK?
    (None,   "BNE",   "RXCOPY"),      # не команда → игнор байта
    (None,   "LDAB#", 4),
    (None,   "STABd", 0xF4),
    (None,   "BRA",   "RXCOPY"),
    ("RXS1", "CMPB#", 1),
    (None,   "BNE",   "RXS2"),
    (None,   "STAAd", 0xF5),          # POKE: адрес hi
    (None,   "LDAB#", 2),
    (None,   "STABd", 0xF4),
    (None,   "BRA",   "RXCOPY"),
    ("RXS2", "CMPB#", 2),
    (None,   "BNE",   "RXS3"),
    (None,   "STAAd", 0xF6),          # POKE: адрес lo
    (None,   "LDAB#", 3),
    (None,   "STABd", 0xF4),
    (None,   "BRA",   "RXCOPY"),
    ("RXS3", "CMPB#", 3),
    (None,   "BNE",   "RXS4"),
    (None,   "LDXd",  0xF5),          # X = адрес ($F5:$F6)
    (None,   "STAAx", 0x00),          # [X] = значение  → ЗАПИСЬ
    (None,   "CLRe",  0x00F4),        # rxsi = 0
    (None,   "BRA",   "RXCOPY"),
    ("RXS4", "CMPB#", 4),
    (None,   "BNE",   "RXS5"),
    (None,   "STAAd", 0xF5),          # PEEK: адрес hi
    (None,   "LDAB#", 5),
    (None,   "STABd", 0xF4),
    (None,   "BRA",   "RXCOPY"),
    ("RXS5", "STAAd", 0xF6),          # PEEK: адрес lo (rxsi==5)
    (None,   "CLRe",  0x00F4),        # rxsi = 0
    # --- читаем *(указатель) → $1600 (видно в кадре как peek) ---
    ("RXCOPY","LDXd", 0xF5),          # X = указатель
    (None,   "LDAAx", 0x00),          # A = *(указатель)
    (None,   "STAAe", 0x1600),        # $1600 = прочитанный байт
    # --- TX: передать следующий байт кадра ---
    ("TXCHK","LDAAd", 0x11),
    (None,   "BITA#", 0x20),          # TDRE?
    (None,   "BNE",   "CONT"),
    (None,   "RTS",   None),
    ("CONT", "LDABd", 0xFA),          # B = si
    (None,   "CMPB#", 0),
    (None,   "BNE",   "S1"),
    # si==0: chk=0, послать AE (без chk)
    (None,   "CLRe",  0x00FB),
    (None,   "LDAA#", 0xAE),
    (None,   "BRA",   "EMITNC"),
    ("S1",   "CMPB#", 1),
    (None,   "BNE",   "S18"),
    (None,   "LDAA#", 0x17),
    (None,   "BRA",   "EMITNC"),
    ("S18",  "CMPB#", 5 + len(ADDR_LIST)),   # позиция чек-суммы = после всех данных
    (None,   "BNE",   "MID"),
    # si==chk: послать chk, si=0
    (None,   "LDAAd", 0xFB),
    (None,   "STAAd", 0x13),
    (None,   "CLRe",  0x00FA),
    (None,   "BRA",   "DONE"),
    ("MID",  "CMPB#", 5),
    (None,   "BCS",   "CONST"),       # si 2..4 → константа
    # si 5..17: значение = *(ADDR[si-5])
    (None,   "SUBB#", 5),
    (None,   "ASLB",  None),          # ×2 (16-бит записи)
    (None,   "LDX#",  "ADDRTBL"),
    (None,   "ABX",   None),
    (None,   "LDXx",  0x00),          # X = адрес из таблицы
    (None,   "LDAAx", 0x00),          # A = байт по адресу
    (None,   "BRA",   "EMITC"),
    ("CONST","SUBB#", 2),             # si 2,3,4 → CONST2[si-2] = FF,F0,len
    (None,   "LDX#",  "CONST2T"),
    (None,   "ABX",   None),
    (None,   "LDAAx", 0x00),
    # провал в EMITC (chk ^= A)
    ("EMITC","PSHA",  None),
    (None,   "EORAd", 0xFB),
    (None,   "STAAd", 0xFB),
    (None,   "PULA",  None),
    (None,   "STAAd", 0x13),
    (None,   "INCe",  0x00FA),
    (None,   "BRA",   "DONE"),
    ("EMITNC","STAAd",0x13),
    (None,   "INCe",  0x00FA),
    ("DONE", "RTS",   None),
]

LEN = {"JSR":3,"LDAAd":2,"LDAA#":2,"LDAAx":2,"LDABd":2,"LDXx":2,"LDX#":3,"BITA#":2,
       "CMPB#":2,"CMPA#":2,"LDAB#":2,"SUBB#":2,"ASLB":1,"ABX":1,"STAAd":2,"STAAe":3,"STABd":2,"STAAx":2,"LDXd":2,"EORAd":2,"CLRe":3,"INCe":3,
       "PSHA":1,"PULA":1,"OIMd":3,"RTS":1,"BNE":2,"BEQ":2,"BCC":2,"BCS":2,"BRA":2}
BR = {"BNE":0x26,"BEQ":0x27,"BCC":0x24,"BCS":0x25,"BRA":0x20}


def assemble(org):
    # длина кода
    code_len = sum(LEN[op] for _, op, _ in PROG)
    addrtbl = org + code_len
    const2t = addrtbl + 2 * len(ADDR_LIST)
    datalabels = {"ADDRTBL": addrtbl, "CONST2T": const2t}
    # метки кода
    labels = {}; pc = org
    for lab, op, arg in PROG:
        if lab: labels[lab] = pc
        pc += LEN[op]
    # сборка кода
    out = bytearray(); pc = org
    for lab, op, arg in PROG:
        nxt = pc + LEN[op]
        if   op == "JSR":   out += bytes([0xBD, arg >> 8, arg & 0xFF])
        elif op == "LDAA#": out += bytes([0x86, arg & 0xFF])
        elif op == "LDAAd": out += bytes([0x96, arg & 0xFF])
        elif op == "LDAAx": out += bytes([0xA6, arg & 0xFF])
        elif op == "LDABd": out += bytes([0xD6, arg & 0xFF])
        elif op == "LDXx":  out += bytes([0xEE, arg & 0xFF])
        elif op == "LDX#":
            a = datalabels[arg] if isinstance(arg, str) else arg
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
        elif op == "PSHA":  out += bytes([0x36])
        elif op == "PULA":  out += bytes([0x32])
        elif op == "OIMd":  out += bytes([0x72, arg[0], arg[1]])
        elif op == "RTS":   out += bytes([0x39])
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
    return out, addrtbl, const2t


def main():
    rom = bytearray(open(SRC, "rb").read()); assert len(rom) == 32768
    code, addrtbl, const2t = assemble(CODE_ORG)
    off = CODE_ORG - ROM_BASE
    assert len(code) <= 0x180, "не влезает в C600-C77F"
    hoff = HOOK_CPU - ROM_BASE
    tgt = rom[hoff + 1] << 8 | rom[hoff + 2]
    assert rom[hoff] == 0xBD and tgt in (ORIG_CALL, CODE_ORG), "по 83F8 не JSR A99B/C600"
    rom[off:off + len(code)] = code
    rom[hoff + 1], rom[hoff + 2] = CODE_ORG >> 8, CODE_ORG & 0xFF
    # чек-сумма
    s = x = 0
    for i in range(len(rom)):
        if i in (0x7F7A, 0x7F7B): continue
        s = (s + rom[i]) & 0xFF; x ^= rom[i]
    rom[0x7F7A], rom[0x7F7B] = s, x
    open(DST, "wb").write(rom)
    print("Готово:", os.path.basename(DST))
    print("  код+таблицы %d байт @ C600..%04X" % (len(code), CODE_ORG + len(code) - 1))
    print("  ADDRTBL @ %04X, CONST2 @ %04X" % (addrtbl, const2t))
    print("  чек-сумма: %02X/%02X" % (s, x))


if __name__ == "__main__":
    main()
