# -*- coding: utf-8 -*-
"""
Сборка v43: КТЗ / КВТЗ / датчик температуры воздуха на канале 9.
План — «План — КТЗ, КВТЗ и ДТВ на канале 9 (v43) 02.10.26 ИИ.txt» (эта папка).

База:   логер/j30_v42_3_шов-УОЗ-и-прогрев-яч7_01.09.26_1230 ИИ.bin
Выход:  логер/j30_v43_КТЗ-КВТЗ-и-ДТВ-канал9_<дата_время> ИИ.bin

ЧТО ДЕЛАЕТ ПАТЧ
  1. $D070 (опрос канала 9, зовётся из главного цикла через $CD59) -> JMP KTZ_CALC.
     KTZ_CALC делает то же, что было (сырьё в $17E0 для кадра), и дальше:
       ТВ  = $FB30(сырьё)             заводская тарировка ТОЖ, датчик такой же
       КВТЗ= таблица $D200 16×16      строки — обороты, столбцы — давление (как VE)
       ТЗ  = ТОЖ + (ТВ − ТОЖ)·КВТЗ/128
       КТЗ = кривая $D300 по ТЗ       ось как у прогревных таблиц (−40…+110, шаг 10)
     Сырьё вне 3…241 (обрыв/КЗ) -> КТЗ = 128 (1.0).
  2. $C7D5 в ДАД-прослойке: «LDAB $CA12» (3 байта) -> «JSR KTZ_MUL» (3 байта).
     KTZ_MUL: A = A·КТЗ/128 (с насыщением), затем LDAB $CA12, RTS.
     При КТЗ = 128 это ТОЖДЕСТВО: A·128·2 = A<<8, старший байт = A без потерь.
     КТЗ = 0 (ОЗУ ещё не посчитано после включения) трактуется как 128.

ПЕРЕМЕННЫЕ (zero-page; проверено: ни одна не встречается в ПЗУ как адрес)
  $E1 сырьё кан.9   $E2 ТВ   $E3 ТЗ   $E4 КТЗ   $E5 КВТЗ
  $E6 столбец   $E9 доля строки   $EA смещение строки   $EB доля столбца
  $EE доля для blend   $EF временное
  Свои переменные, а не временные ДАД-прослойки ($F4-$FF): прослойка может
  выполняться в прерывании, общие временные испортили бы друг другу расчёт.

Запуск: python3 "build_v43_ktz ИИ.py"   (проверка на двойнике — в конце)
"""
import os
import sys
import time
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "логер", "j30_v42_3_шов-УОЗ-и-прогрев-яч7_01.09.26_1230 ИИ.bin")
OUT = os.path.join(ROOT, "логер", "j30_v43_КТЗ-КВТЗ-и-ДТВ-канал9_%s ИИ.bin"
                   % time.strftime("%d.%m.%y_%H%M"))

BASE = 0x8000
KVTZ_TAB = 0xD200          # 256 байт
KTZ_TAB = 0xD300           # 16 байт
CODE = 0xD310              # код

ZP = dict(RAW9=0xE1, TV=0xE2, TZ=0xE3, KTZ=0xE4, KV=0xE5, COL=0xE6,
          RFR=0xE9, ROFF=0xEA, CFR=0xEB, BFR=0xEE, TMP=0xEF)

# ---------------------------------------------------------------- мини-ассемблер
OPS = {
    # (мнемоника, режим): опкод.  режимы: inh imm8 imm16 dir ext idx rel
    ("LDAA", "imm8"): 0x86, ("LDAA", "dir"): 0x96, ("LDAA", "ext"): 0xB6, ("LDAA", "idx"): 0xA6,
    ("LDAB", "imm8"): 0xC6, ("LDAB", "dir"): 0xD6, ("LDAB", "ext"): 0xF6, ("LDAB", "idx"): 0xE6,
    ("STAA", "dir"): 0x97, ("STAA", "ext"): 0xB7,
    ("STAB", "dir"): 0xD7, ("STAB", "ext"): 0xF7,
    ("CMPA", "imm8"): 0x81, ("CMPB", "imm8"): 0xC1,
    ("SUBA", "imm8"): 0x80, ("SUBA", "dir"): 0x90,
    ("ADDA", "ext"): 0xBB, ("ADDB", "imm8"): 0xCB, ("ADDB", "dir"): 0xDB,
    ("ANDB", "imm8"): 0xC4,
    ("LDD", "ext"): 0xFC, ("ADDD", "imm16"): 0xC3,
    ("LDX", "imm16"): 0xCE,
    ("JSR", "ext"): 0xBD, ("JMP", "ext"): 0x7E,
    ("BRA", "rel"): 0x20, ("BCC", "rel"): 0x24, ("BCS", "rel"): 0x25,
    ("BNE", "rel"): 0x26, ("BEQ", "rel"): 0x27, ("BSR", "rel"): 0x8D,
    ("RTS", "inh"): 0x39, ("TAB", "inh"): 0x16, ("TBA", "inh"): 0x17,
    ("SBA", "inh"): 0x10, ("ABX", "inh"): 0x3A, ("MUL", "inh"): 0x3D,
    ("LSRD", "inh"): 0x04, ("ASLD", "inh"): 0x05, ("TSTA", "inh"): 0x4D,
    ("CLRA", "inh"): 0x4F, ("CLRB", "inh"): 0x5F, ("NEGA", "inh"): 0x40,
    ("LSRA", "inh"): 0x44, ("ASLA", "inh"): 0x48, ("ASLB", "inh"): 0x58,
}
SIZE = {"inh": 1, "imm8": 2, "dir": 2, "idx": 2, "rel": 2, "imm16": 3, "ext": 3}


def assemble(org, prog):
    """prog: список кортежей. ('метка',) — метка; (мн, режим, операнд) — команда.
    Операнд — число или имя метки. Два прохода."""
    labels, pc = {}, org
    for st in prog:
        if len(st) == 1:
            labels[st[0]] = pc
        else:
            pc += SIZE[st[1]]
    out, pc = bytearray(), org
    for st in prog:
        if len(st) == 1:
            continue
        mn, mode = st[0], st[1]
        opr = st[2] if len(st) > 2 else None
        if isinstance(opr, str):
            opr = labels[opr]
        op = OPS[(mn, mode)]
        if mode == "inh":
            out += bytes([op])
        elif mode in ("imm8", "dir", "idx"):
            assert 0 <= opr <= 0xFF, (mn, mode, opr)
            out += bytes([op, opr])
        elif mode == "rel":
            d = opr - (pc + 2)
            assert -128 <= d <= 127, ("далеко", mn, d)
            out += bytes([op, d & 0xFF])
        else:
            out += bytes([op, (opr >> 8) & 0xFF, opr & 0xFF])
        pc += SIZE[mode]
    return bytes(out), labels


Z = ZP
P = []
P += [("KTZ_CALC",),
      # --- то, что было в $D070: опрос канала 9, сырьё в $17E0 для кадра ---
      ("LDAB", "imm8", 0x09), ("JSR", "ext", 0xB209), ("STAB", "ext", 0x17E0),
      ("STAB", "dir", Z["RAW9"]),
      # --- окно годности 3…241, как у ТОЖ ($B264) ---
      # (ветка «неисправен» стоит здесь же: до конца рутины короткий переход не достаёт)
      ("CMPB", "imm8", 0x03), ("BCS", "rel", "BAD"),
      ("CMPB", "imm8", 0xF2), ("BCS", "rel", "GOOD"),
      ("BAD",), ("LDAA", "imm8", 0x80), ("STAA", "dir", Z["KTZ"]), ("RTS", "inh"),
      ("GOOD",),
      # --- ТВ = $FB30(сырьё) через заводскую $80A9 ---
      ("TBA", "inh"), ("LDX", "imm16", 0xFB30), ("JSR", "ext", 0x80A9),
      ("STAA", "dir", Z["TV"]),
      # --- строка КВТЗ по оборотам: ровно как ДАД-прослойка $C72A-$C756 ---
      ("LDD", "ext", 0x140A), ("LSRD", "inh"), ("TSTA", "inh"), ("BEQ", "rel", "R1"),
      ("LDAB", "imm8", 0xFF),
      ("R1",), ("TBA", "inh"), ("LDAB", "ext", 0xCA20), ("ASLB", "inh"), ("SBA", "inh"),
      ("BCC", "rel", "R2"), ("CLRA", "inh"),
      ("R2",), ("TAB", "inh"), ("ANDB", "imm8", 0x0F),
      ("LSRA", "inh"), ("LSRA", "inh"), ("LSRA", "inh"), ("LSRA", "inh"),
      ("CMPA", "imm8", 0x0F), ("BCS", "rel", "R3"), ("LDAA", "imm8", 0x0F), ("CLRB", "inh"),
      ("R3",), ("STAB", "dir", Z["RFR"]),
      ("ASLA", "inh"), ("ASLA", "inh"), ("ASLA", "inh"), ("ASLA", "inh"),
      ("STAA", "dir", Z["ROFF"]),
      # --- столбец по давлению: та же таблица-ось $C600, что у VE ---
      ("LDAB", "dir", 0xF7), ("LDX", "imm16", 0xC600), ("ABX", "inh"), ("LDAA", "idx", 0),
      ("TAB", "inh"), ("ANDB", "imm8", 0x0F), ("STAB", "dir", Z["CFR"]),
      ("LSRA", "inh"), ("LSRA", "inh"), ("LSRA", "inh"), ("LSRA", "inh"),
      ("STAA", "dir", Z["COL"]),
      # --- билинейная: строка row, затем row+1, смешать по доле строки ---
      ("LDAB", "dir", Z["ROFF"]), ("BSR", "rel", "ROWVAL"), ("STAA", "dir", Z["KV"]),
      ("LDAB", "dir", Z["RFR"]), ("BEQ", "rel", "NOROW"),
      ("LDAB", "dir", Z["ROFF"]), ("ADDB", "imm8", 0x10), ("BSR", "rel", "ROWVAL"),
      ("TAB", "inh"), ("LDAA", "dir", Z["RFR"]), ("STAA", "dir", Z["BFR"]),
      ("LDAA", "dir", Z["KV"]), ("BSR", "rel", "BLEND"), ("STAA", "dir", Z["KV"]),
      ("NOROW",),
      # --- ТЗ = ТОЖ + (ТВ − ТОЖ)·КВТЗ/128, со знаком ---
      ("LDAA", "dir", Z["TV"]), ("LDAB", "ext", 0x140C), ("SBA", "inh"),
      ("BCC", "rel", "TZPOS"),
      ("NEGA", "inh"), ("LDAB", "dir", Z["KV"]), ("MUL", "inh"), ("ASLD", "inh"),
      ("TAB", "inh"), ("LDAA", "ext", 0x140C), ("SBA", "inh"), ("BRA", "rel", "TZOK"),
      ("TZPOS",), ("LDAB", "dir", Z["KV"]), ("MUL", "inh"), ("ASLD", "inh"),
      ("ADDA", "ext", 0x140C),
      ("TZOK",), ("STAA", "dir", Z["TZ"]),
      # --- индекс как у прогревных таблиц ($B295-$B2A9): (ТЗ−10)·1.6 ---
      ("SUBA", "imm8", 0x0A), ("BCS", "rel", "Z0"),
      ("CMPA", "imm8", 0xA0), ("BCS", "rel", "Z1"), ("LDAA", "imm8", 0x9F), ("BRA", "rel", "Z1"),
      ("Z0",), ("CLRA", "inh"),
      ("Z1",), ("LDAB", "imm8", 0xCD), ("MUL", "inh"), ("ASLD", "inh"), ("ADDD", "imm16", 0x0080),
      # --- КТЗ = кривая по индексу, заводская 1D-подпрограмма $809F ---
      ("LDX", "imm16", KTZ_TAB), ("JSR", "ext", 0x809F),
      ("STAA", "dir", Z["KTZ"]), ("RTS", "inh"),

      # ROWVAL: B = смещение строки (row·16). A = T[row][col], смешанное с
      # T[row][col+1] по доле столбца.
      ("ROWVAL",), ("LDX", "imm16", KVTZ_TAB), ("ABX", "inh"),
      ("LDAB", "dir", Z["COL"]), ("ABX", "inh"), ("LDAA", "idx", 0),
      ("LDAB", "dir", Z["CFR"]), ("BEQ", "rel", "RV1"),
      ("STAB", "dir", Z["BFR"]), ("LDAB", "idx", 1), ("BSR", "rel", "BLEND"),
      ("RV1",), ("RTS", "inh"),

      # BLEND: A = a, B = b, доля в $EE (0…15) -> A = a + (b−a)·доля/16
      ("BLEND",), ("STAA", "dir", Z["TMP"]), ("TBA", "inh"), ("SUBA", "dir", Z["TMP"]),
      ("BCS", "rel", "BNEG"),
      ("LDAB", "dir", Z["BFR"]), ("MUL", "inh"),
      ("LSRD", "inh"), ("LSRD", "inh"), ("LSRD", "inh"), ("LSRD", "inh"),
      ("ADDB", "dir", Z["TMP"]), ("TBA", "inh"), ("RTS", "inh"),
      ("BNEG",), ("NEGA", "inh"), ("LDAB", "dir", Z["BFR"]), ("MUL", "inh"),
      ("LSRD", "inh"), ("LSRD", "inh"), ("LSRD", "inh"), ("LSRD", "inh"),
      ("LDAA", "dir", Z["TMP"]), ("SBA", "inh"), ("RTS", "inh"),

      # KTZ_MUL: вызывается вместо «LDAB $CA12» в ДАД-прослойке ($C7D5).
      # A = A·КТЗ/128 с насыщением; КТЗ = 0 (ещё не посчитано) -> как 128.
      ("KTZ_MUL",), ("LDAB", "dir", Z["KTZ"]), ("BNE", "rel", "KM1"), ("LDAB", "imm8", 0x80),
      ("KM1",), ("MUL", "inh"), ("ASLD", "inh"), ("BCC", "rel", "KM2"), ("LDAA", "imm8", 0xFF),
      ("KM2",), ("LDAB", "ext", 0xCA12), ("RTS", "inh"),
      ]


# ---------------------------------------------------------------- таблицы
def fill_kvtz(b):
    """КВТЗ по формуле Января через расход каждой ячейки VE.
    КВТЗ = min(1, Q/800)·(0.8984375 − 0.25) + 0.25,  Q в кг/ч."""
    start = b[0xCA20 - BASE] * 2                  # начало оси оборотов в единицах rpm8
    pax = [b[0xCA00 - BASE + c] for c in range(16)]
    tab = []
    for r in range(16):
        rpm8 = start + 16 * r
        rpm = rpm8 * 2 * 12.807                    # rpm8 = $140A:$140B >> 1
        for c in range(16):
            ve = b[0xC900 - BASE + r * 16 + c] / 128.0
            rho = pax[c] * 1000.0 / (287.05 * 293.15)
            q = rpm / 120.0 * 2.96e-3 * rho * ve * 3600.0
            kv = min(1.0, q / 800.0) * (0.8984375 - 0.25) + 0.25
            tab.append(max(0, min(128, int(round(kv * 128)))))
    return tab, start, pax


def checksum(b):
    s = x = 0
    for i, v in enumerate(b):
        if i in (0x7F7A, 0x7F7B):
            continue
        s = (s + v) & 0xFF
        x ^= v
    b[0x7F7A], b[0x7F7B] = s, x


def build():
    b = bytearray(open(SRC, "rb").read())
    assert len(b) == 32768
    # проверить, что патчим ровно то, что ожидали
    assert b[0xD070 - BASE:0xD079 - BASE] == bytes.fromhex("C609BDB209F717E039"), "D070 не тот"
    assert b[0xC7D5 - BASE:0xC7D8 - BASE] == bytes.fromhex("F6CA12"), "C7D5 не тот"
    code, lab = assemble(CODE, P)
    for a, n in ((KVTZ_TAB, 256), (KTZ_TAB, 16), (CODE, len(code))):
        assert set(b[a - BASE:a - BASE + n]) == {0x3F}, "место $%04X занято" % a
    kv, _, _ = fill_kvtz(b)
    b[KVTZ_TAB - BASE:KVTZ_TAB - BASE + 256] = bytes(kv)
    b[KTZ_TAB - BASE:KTZ_TAB - BASE + 16] = bytes([128] * 16)      # v43: КТЗ = 1.0 везде
    b[CODE - BASE:CODE - BASE + len(code)] = code
    k = lab["KTZ_CALC"]
    b[0xD070 - BASE:0xD073 - BASE] = bytes([0x7E, k >> 8, k & 0xFF])  # JMP KTZ_CALC
    m = lab["KTZ_MUL"]
    b[0xC7D5 - BASE:0xC7D8 - BASE] = bytes([0xBD, m >> 8, m & 0xFF])  # JSR KTZ_MUL
    checksum(b)
    return b, lab, len(code), kv


if __name__ == "__main__":
    b, lab, n, kv = build()
    print("код %d байт: $%04X–$%04X" % (n, CODE, CODE + n - 1))
    for k in ("KTZ_CALC", "ROWVAL", "BLEND", "KTZ_MUL"):
        print("  %-9s $%04X" % (k, lab[k]))
    print("КВТЗ, строки — обороты, столбцы — давление (÷128):")
    for r in range(16):
        print("  " + " ".join("%4.2f" % (kv[r * 16 + c] / 128) for c in range(16)))
    if "--write" in sys.argv:
        open(OUT, "wb").write(b)
        print("записано:", OUT)
