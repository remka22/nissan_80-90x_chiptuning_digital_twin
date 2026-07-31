# -*- coding: utf-8 -*-
"""
Билдер патча-ДАМПЕРА ОЗУ для J30.
Подпрограмма ходит указателем по ДВУМ диапазонам: внутренний ОЗУ 6303
$0040..$00FF (192 байта) + внешний ОЗУ HD63140 $1400..$17FF (1024 байта), и
шлёт их блоками по протоколу ramframe: [AE 17][addr_hi][addr_lo][16][данные×16]
[chk]. По байту за вызов (неблокирующе). Состояние в свободном внутр. ОЗУ
$00FA..$00FD (эти 4 байта тоже попадают в дамп — их значения там «живые»):
  $FA = si  (индекс байта в блоке 0..21)
  $FB = chk (накопитель контрольной суммы)
  $FC:$FD = ptr (текущий адрес ОЗУ, 16-бит)

Врезка: 83F8 JSR $A99B -> JSR C600; подпрограмма сама зовёт $A99B.
Кадр совпадает с логером/ramframe.py (BLK=16, SYNC=AE17, chk=XOR(addr,len,data)).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# src/dst можно передать аргументами: build_ramdump_patch.py <src.bin> <dst.bin>
SRC = os.path.join(HERE, "HN27C256G@DIP28.BIN")
DST = os.path.join(HERE, "J30_дамп_озу_тест ИИ.bin")
if len(sys.argv) >= 3:
    SRC, DST = sys.argv[1], sys.argv[2]
ROM_BASE = 0x8000
CODE_ORG = 0xC600
HOOK_CPU = 0x83F8
ORIG_CALL = 0xA99B

# (метка|None, токен, операнд)  операнд: число или метка (для ветвлений)
PROG = [
    (None,     "JSR",   ORIG_CALL),     # C600 (врезка) — родной вызов
    (None,     "OIMd",  (0x02, 0x11)),  # TE=1: включить передатчик SCI (сток его не включает
                                        # в рабочем режиме — гейт $40.7; без этого нога P24 молчит)
    ("DUMP",   "LDAAd", 0x11),          # TRCSR
    (None,     "BITA#", 0x20),          # TDRE?
    (None,     "BNE",   "CONT"),        # готов -> дальше
    (None,     "RTS",   None),          # занят -> ранний выход (неблокирующе)
    ("CONT",   "LDABd", 0xFA),          # B = si
    (None,     "CMPB#", 0),
    (None,     "BNE",   "S1"),
    # --- si==0: начало блока ---
    (None,     "LDAAd", 0xFC),
    (None,     "ORAAd", 0xFD),
    (None,     "BNE",   "PTROK"),
    (None,     "CLRe",  0x00FC),        # ptr := $0040 (начало внутреннего ОЗУ)
    (None,     "LDAA#", 0x40),
    (None,     "STAAd", 0xFD),
    ("PTROK",  "CLRe",  0x00FB),        # chk = 0
    (None,     "LDAA#", 0xAE),
    (None,     "BRA",   "EMIT"),
    ("S1",     "CMPB#", 1),
    (None,     "BNE",   "S2"),
    (None,     "LDAA#", 0x17),
    (None,     "BRA",   "EMIT"),
    ("S2",     "CMPB#", 2),
    (None,     "BNE",   "S3"),
    (None,     "LDAAd", 0xFC),          # ptr_hi
    (None,     "BRA",   "EMITC"),
    ("S3",     "CMPB#", 3),
    (None,     "BNE",   "S4"),
    (None,     "LDAAd", 0xFD),          # ptr_lo
    (None,     "BRA",   "EMITC"),
    ("S4",     "CMPB#", 4),
    (None,     "BNE",   "SD"),
    (None,     "LDAA#", 16),            # len = BLK
    (None,     "BRA",   "EMITC"),
    ("SD",     "CMPB#", 21),            # si==21 -> контрольная сумма
    (None,     "BNE",   "DATA"),
    # --- фаза контрольной суммы: продвинуть ptr, послать chk, si=0 ---
    (None,     "LDAAd", 0xFD),
    (None,     "ADDA#", 16),
    (None,     "STAAd", 0xFD),
    (None,     "BCC",   "NOC"),
    (None,     "INCe",  0x00FC),
    ("NOC",    "LDAAd", 0xFC),
    (None,     "CMPA#", 0x01),          # ptr_hi==$01 -> конец внутр. -> $1400
    (None,     "BNE",   "CHKEXT"),
    (None,     "LDAA#", 0x14),
    (None,     "STAAd", 0xFC),
    (None,     "CLRe",  0x00FD),
    (None,     "BRA",   "SNDCHK"),
    ("CHKEXT", "CMPA#", 0x18),          # ptr_hi==$18 -> конец внешн. -> $0040
    (None,     "BNE",   "SNDCHK"),
    (None,     "CLRe",  0x00FC),        # ptr := $0040
    (None,     "LDAA#", 0x40),
    (None,     "STAAd", 0xFD),
    ("SNDCHK", "LDAAd", 0xFB),          # chk
    (None,     "STAAd", 0x13),          # послать
    (None,     "CLRe",  0x00FA),        # si = 0
    (None,     "BRA",   "DONE"),
    # --- фаза данных: ram[ptr + (si-5)] ---
    ("DATA",   "LDXd",  0xFC),          # X = ptr
    (None,     "LDABd", 0xFA),
    (None,     "SUBB#", 5),
    (None,     "ABX",   None),
    (None,     "LDAAx", 0x00),          # A = ram-байт
    # провалиться в EMITC (chk ^= A, послать, si++)
    ("EMITC",  "PSHA",  None),
    (None,     "EORAd", 0xFB),
    (None,     "STAAd", 0xFB),
    (None,     "PULA",  None),
    (None,     "STAAd", 0x13),          # послать
    (None,     "INCe",  0x00FA),        # si++
    (None,     "BRA",   "DONE"),
    # --- послать байт вне контрольной суммы (SYNC), si++ ---
    ("EMIT",   "STAAd", 0x13),
    (None,     "INCe",  0x00FA),
    ("DONE",   "RTS",   None),
]

LEN = {"JSR":3,"LDAAd":2,"LDAA#":2,"LDAAx":2,"BITA#":2,"BEQ":2,"BNE":2,"BCC":2,
       "BCS":2,"BRA":2,"LDABd":2,"CMPB#":2,"CMPA#":2,"ORAAd":2,"EORAd":2,
       "STAAd":2,"LDXd":2,"CLRe":3,"INCe":3,"ADDA#":2,"SUBB#":2,"ABX":1,
       "PSHA":1,"PULA":1,"RTS":1,"OIMd":3}
OP1 = {"ABX":0x3A,"PSHA":0x36,"PULA":0x32,"RTS":0x39}
BR  = {"BEQ":0x27,"BNE":0x26,"BCC":0x24,"BCS":0x25,"BRA":0x20}


def assemble(org):
    # проход 1: адреса меток
    labels = {}
    pc = org
    for lab, op, arg in PROG:
        if lab:
            labels[lab] = pc
        pc += LEN[op]
    # проход 2: байты
    out = bytearray()
    pc = org
    for lab, op, arg in PROG:
        nxt = pc + LEN[op]
        if op == "JSR":     out += bytes([0xBD, arg >> 8, arg & 0xFF])
        elif op == "LDAA#": out += bytes([0x86, arg & 0xFF])
        elif op == "LDAAd": out += bytes([0x96, arg & 0xFF])
        elif op == "LDAAx": out += bytes([0xA6, arg & 0xFF])
        elif op == "BITA#": out += bytes([0x85, arg & 0xFF])
        elif op == "LDABd": out += bytes([0xD6, arg & 0xFF])
        elif op == "CMPB#": out += bytes([0xC1, arg & 0xFF])
        elif op == "CMPA#": out += bytes([0x81, arg & 0xFF])
        elif op == "ORAAd": out += bytes([0x9A, arg & 0xFF])
        elif op == "EORAd": out += bytes([0x98, arg & 0xFF])
        elif op == "STAAd": out += bytes([0x97, arg & 0xFF])
        elif op == "LDXd":  out += bytes([0xDE, arg & 0xFF])
        elif op == "ADDA#": out += bytes([0x8B, arg & 0xFF])
        elif op == "SUBB#": out += bytes([0xC0, arg & 0xFF])
        elif op == "CLRe":  out += bytes([0x7F, arg >> 8, arg & 0xFF])
        elif op == "INCe":  out += bytes([0x7C, arg >> 8, arg & 0xFF])
        elif op == "OIMd":  out += bytes([0x72, arg[0], arg[1]])  # OIM #imm, dd (прямая)
        elif op in OP1:     out += bytes([OP1[op]])
        elif op in BR:
            rel = labels[arg] - nxt
            assert -128 <= rel <= 127, "ветвление %s вне диапазона: %d" % (arg, rel)
            out += bytes([BR[op], rel & 0xFF])
        else:
            raise ValueError("неизвестный op %s" % op)
        pc = nxt
    return out, labels


def main():
    rom = bytearray(open(SRC, "rb").read())
    assert len(rom) == 32768
    code, labels = assemble(CODE_ORG)
    off = CODE_ORG - ROM_BASE
    assert len(code) <= 0x100, "рутина не влезает в страницу C600..C6FF"
    hoff = HOOK_CPU - ROM_BASE
    tgt = rom[hoff + 1] << 8 | rom[hoff + 2]
    # допускаем и свежий бин (JSR A99B), и уже пропатченный (JSR C600) — перепатч
    assert rom[hoff] == 0xBD and tgt in (ORIG_CALL, CODE_ORG), "по 83F8 не JSR A99B/C600"
    rom[off:off + len(code)] = code
    rom[hoff + 1], rom[hoff + 2] = CODE_ORG >> 8, CODE_ORG & 0xFF

    # пересчитать контрольную сумму: 0x7F7A=SUM, 0x7F7B=XOR всех байт кроме них
    s = x = 0
    for i in range(len(rom)):
        if i in (0x7F7A, 0x7F7B):
            continue
        s = (s + rom[i]) & 0xFF
        x ^= rom[i]
    rom[0x7F7A], rom[0x7F7B] = s, x

    open(DST, "wb").write(rom)
    print("Готово:", os.path.basename(DST))
    print("  подпрограмма %d байт @ %04X..%04X" % (len(code), CODE_ORG, CODE_ORG + len(code) - 1))
    print("  врезка 83F8: JSR %04X -> JSR %04X" % (ORIG_CALL, CODE_ORG))
    print("  контрольная сумма пересчитана: 0x%02X/0x%02X (0x7F7A/0x7F7B)" % (s, x))


if __name__ == "__main__":
    main()
