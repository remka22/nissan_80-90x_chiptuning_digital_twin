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
ADDR_LIST = [
    0x140A, 0x140B,   # обороты (16б)
    0x1482,           # нагрузка сглаж. (ось карт)
    0x1413,           # расход МГНОВЕННЫЙ (гэп к $1482 = транзит/газовка)
    0x1431,           # ALPHA
    0x1411, 0x1412,   # ВПРЫСК факт (16б) — подтв. трассой обогащения
    # --- все 9 каналов АЦП ($B209) ---
    0x1408, 0x1409,   # ch0 MAF (16б)
    0x008F,           # ch1 напряжение борта
    0x004C,           # ch2 темп ОЖ
    0x1400,           # ch3 O2
    0x1402,           # ch4 (не опознан)
    0x1401,           # ch5 (не опознан)
    0x1492, 0x1493,   # ch6 (не опознан, 16б)
    0x1583,           # ch7 (не опознан)
    0x1574,           # ch8 (не опознан)
    # --- УОЗ ---
    0x140F,           # УОЗ финальный (доставленный на катушку)
    0x143B,           # УОЗ выбранной карты (на ХХ = из 0x76F0)
    0x0053,           # флаги источника угла: б0=ХХ б1=крэнк б2=нейтраль
    # --- дроссель / ХХ ---
    0x0015,           # концевик дросселя (сырой порт, бит 0x10)
    0x0054,           # флаг ХХ/газ (б0)
    # --- контур РХХ ---
    0x142C,           # цель ХХ
    0x004D, 0x004E,   # duty РХХ (16б)
    0x144E,           # ошибка контура ХХ (НЕ впрыск — исправлено)
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
    (None,   "OIMd",  (0x02, 0x11)),  # TE=1
    ("DUMP", "LDAAd", 0x11),
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
       "CMPB#":2,"SUBB#":2,"ASLB":1,"ABX":1,"STAAd":2,"EORAd":2,"CLRe":3,"INCe":3,
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
    assert len(code) <= 0x100, "не влезает в страницу C600"
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
