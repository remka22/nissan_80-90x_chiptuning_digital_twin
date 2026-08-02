# -*- coding: utf-8 -*-
"""
Патч ТАРИРОВКИ TPS (дроссель) для J30. Архитектура: АЦП → тарировка(0-255=0-100%) → потребители.
Единая точка входа 8dd5 (подтверждено трассой: канал 6 читается 1 раз, обходов нет).

ЧТО ДЕЛАЕТ:
1. Рутина CALIB @ C700: вход D=raw10 (из B209). Проверка ОБРЫВА по СЫРОМУ raw ([FLO,FHI]);
   если вне — флаг $00B9.0x20 + дефолт. Иначе норм: $1492 = ((raw10>>2 − CLOSED)×SLOPE)>>6 → 0..510
   (9-бит), значит $1494=$1492>>1 → 0..255 = 0-100%. Всё дальше ($14A2/дельты/пороги) — от него.
2. Врезка 8DDA: заменяет родной >>1/клип на JSR C700 (родное STD $1492 @ 8DE6 остаётся).
3. bc47 (проверка диапазона $1494<3/>240) ОТКЛЮЧЕНА — обрыв теперь ловится в CALIB по сырому.
4. Рескейл ~14 порогов-констант под шкалу 0-255 (открытие ×1.5, дельты ×1.48).

Параметры тарировки (ROM, редактируемые): CLOSED8/SLOPE/FLO/FHI/FDEF @ C740.
Дефолты — под замеренный датчик (закр. $1494≈18, полный≈190). ⚠ ПРОВЕРЯТЬ НА СТЕНДЕ.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(HERE, "..", "логер", "J30_v8plus2_k412_l095_02.08.26 ИИ.bin")
DST = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(HERE, "..", "логер", "J30_tps-калибровка_02.08.26 ИИ.bin")
ROM_BASE = 0x8000
ROUT = 0xC700           # рутина CALIB
PARM = 0xC740           # параметры тарировки
HOOK = 0x8DDA           # врезка (родной >>1/клип)
HOOK_END = 0x8DE6       # тут родное STD $1492

# --- параметры тарировки (дефолты под замер: закрытый $1494=18, полный=190) ---
CLOSED8 = 18            # закрытый в единицах raw1494 (raw10>>2)
SLOPE   = 190           # ((raw1494-CLOSED)*SLOPE)>>6 → полный (190-18=172)*190>>6 = 510
FLO     = 40            # обрыв: raw10 ниже → неисправность (замыкание на массу)
FHI     = 950           # обрыв: raw10 выше → неисправность (обрыв/КЗ на питание)
FDEF    = 132           # дефолт $1492 при обрыве (=66 открытия ×2, лимп)

# рутина: метка|None, токен, операнд
PROG = [
    # --- обрыв по СЫРОМУ raw10 ---
    (None,   "STDd",  0xF2),          # $F2:$F3 = raw10
    (None,   "SUBDe", "FLO"),         # raw - FLO
    (None,   "BCS",   "FAULT"),       # raw<FLO → обрыв
    (None,   "LDDd",  0xF2),
    (None,   "SUBDe", "FHI"),         # raw - FHI
    (None,   "BCC",   "FAULT"),       # raw>=FHI → обрыв
    # --- норм: raw1494 = raw10>>2 ---
    (None,   "LDDd",  0xF2),
    (None,   "LSRD",  None),
    (None,   "LSRD",  None),          # B = raw10>>2 (0-255), A=0
    (None,   "SUBBe", "CLOSED8"),     # B -= закрытый
    (None,   "BCC",   "P1"),
    (None,   "CLRB",  None),          # < закрытого → 0
    ("P1",   "LDAAe", "SLOPE"),
    (None,   "MUL",   None),          # D = (raw1494-closed)*slope
    (None,   "LSRD",  None), (None, "LSRD", None), (None, "LSRD", None),
    (None,   "LSRD",  None), (None, "LSRD", None), (None, "LSRD", None),  # >>6 → 0..510
    (None,   "RTS",   None),
    ("FAULT","OIMd",  (0x20, 0xB9)),  # флаг неисправности TPS $00B9.0x20
    (None,   "LDDe",  "FDEF"),
    (None,   "RTS",   None),
]

LEN = {"STDd":2,"SUBDe":3,"BCS":2,"BCC":2,"LDDd":2,"LSRD":1,"SUBBe":3,"CLRB":1,
       "LDAAe":3,"MUL":1,"RTS":1,"OIMd":3,"LDDe":3}


def asm(org, labels_data):
    labels = {}; pc = org
    for lab, op, a in PROG:
        if lab: labels[lab] = pc
        pc += LEN[op]
    out = bytearray(); pc = org
    for lab, op, a in PROG:
        nx = pc + LEN[op]
        if   op == "STDd":  out += bytes([0xDD, a & 0xFF])
        elif op == "LDDd":  out += bytes([0xDC, a & 0xFF])
        elif op == "SUBDe":
            ad = labels_data[a]; out += bytes([0xB3, ad >> 8, ad & 0xFF])
        elif op == "SUBBe":
            ad = labels_data[a]; out += bytes([0xF0, ad >> 8, ad & 0xFF])
        elif op == "LDAAe":
            ad = labels_data[a]; out += bytes([0xB6, ad >> 8, ad & 0xFF])
        elif op == "LDDe":
            ad = labels_data[a]; out += bytes([0xFC, ad >> 8, ad & 0xFF])
        elif op == "LSRD":  out += bytes([0x04])
        elif op == "CLRB":  out += bytes([0x5F])
        elif op == "MUL":   out += bytes([0x3D])
        elif op == "RTS":   out += bytes([0x39])
        elif op == "OIMd":  out += bytes([0x72, a[0], a[1]])
        elif op in ("BCS", "BCC"):
            rel = labels[a] - nx; assert -128 <= rel <= 127, "%s %d" % (a, rel)
            out += bytes([0x25 if op == "BCS" else 0x24, rel & 0xFF])
        else: raise ValueError(op)
        pc = nx
    return out


# рескейл порогов: файл-адрес → новое значение (открытие ×1.5, дельты ×1.48)
RESCALE = {
    0x76CD: 5,   0x768F: 35,  0x7690: 47,  0x7691: 66,  0x76CC: 75,   # открытие $14A2
    0x792B: 15,  0x793A: 7,   0x793B: 22,  0x793C: 74,               # ускор. $14A3
    0x7920: 3,   0x7921: 6,   0x76D1: 2,   0x77B7: 6,                # dashpot/база
}


def main():
    rom = bytearray(open(SRC, "rb").read()); assert len(rom) == 32768
    off = lambda cpu: cpu - ROM_BASE

    # параметры тарировки @ C740
    p = off(PARM)
    labels_data = {"CLOSED8": PARM, "SLOPE": PARM + 1, "FLO": PARM + 2,
                   "FHI": PARM + 4, "FDEF": PARM + 6}
    rom[p] = CLOSED8; rom[p + 1] = SLOPE
    rom[p + 2], rom[p + 3] = FLO >> 8, FLO & 0xFF
    rom[p + 4], rom[p + 5] = FHI >> 8, FHI & 0xFF
    rom[p + 6], rom[p + 7] = FDEF >> 8, FDEF & 0xFF

    # рутина @ C700
    code = asm(ROUT, labels_data)
    assert all(x == 0x3F for x in rom[off(ROUT):off(ROUT) + len(code)]), "C700 не пусто"
    assert off(ROUT) + len(code) <= off(PARM), "рутина заезжает на параметры"
    rom[off(ROUT):off(ROUT) + len(code)] = code

    # врезка 8DDA: JSR C700 + NOP-заполнение до 8DE6
    h = off(HOOK); hend = off(HOOK_END)
    assert rom[hend:hend + 3] == bytes([0xFD, 0x14, 0x92]), "по 8DE6 не STD $1492"
    rom[h] = 0xBD; rom[h + 1] = ROUT >> 8; rom[h + 2] = ROUT & 0xFF
    for i in range(h + 3, hend): rom[i] = 0x01   # NOP

    # bc47: отключить проверку диапазона $1494 (обрыв теперь в CALIB)
    #   bc4a: 81 03 (CMPA #3) → 81 00 ; bc50: 25 xx (BCS ok) → 20 xx (BRA, всегда «ок»)
    bc = off(0xBC4A)
    assert rom[bc] == 0x81, "bc4a не CMPA #imm"
    rom[bc + 1] = 0x00                  # CMPA #0 → нижний обрыв не срабатывает
    assert rom[off(0xBC50)] == 0x25, "bc50 не BCS"
    rom[off(0xBC50)] = 0x20             # BCS→BRA: верхний обрыв не срабатывает, всегда «ок»

    # рескейл порогов
    for a, nv in RESCALE.items():
        rom[a] = nv

    # чек-сумма
    s = x = 0
    for i in range(len(rom)):
        if i in (0x7F7A, 0x7F7B): continue
        s = (s + rom[i]) & 0xFF; x ^= rom[i]
    rom[0x7F7A], rom[0x7F7B] = s, x
    open(DST, "wb").write(rom)
    print("Готово:", os.path.basename(DST))
    print("  CALIB %d байт @ C700, параметры @ C740" % len(code))
    print("  CLOSED8=%d SLOPE=%d FLO=%d FHI=%d FDEF=%d" % (CLOSED8, SLOPE, FLO, FHI, FDEF))
    print("  врезка 8DDA: JSR C700 | bc47 отключена | порогов рескейл: %d" % len(RESCALE))
    print("  чек-сумма: %02X/%02X" % (s, x))


if __name__ == "__main__":
    main()
