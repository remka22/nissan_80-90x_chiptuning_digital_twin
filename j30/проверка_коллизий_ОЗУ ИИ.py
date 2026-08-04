# -*- coding: utf-8 -*-
"""Механическая проверка: не легло ли что-то из патча поверх заводского ОЗУ.
Сопоставляет РЕГИОНЫ ПАТЧА со ВСЕМИ адресами, которых касается заводской код.
Ловит три вида заводского использования:
  1) прямые операнды инструкций ($0040-$1FFF)
  2) ЦИКЛЫ: LDX #$addr ... CPX #$end  -> занят весь диапазон
  3) БАЗЫ ТАБЛИЦ: LDX #$addr ; STX $0074/$0076/$0078 -> база двумерной выборки
"""
import re, sys, importlib.util

ASM = "J30_дизасм_листинг ИИ.asm"
sp = importlib.util.spec_from_file_location("b", "build_targeted_patch ИИ.py")
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)

# ---- РЕГИОНЫ ПАТЧА ----
mine = [
    ("тень смеси",      m.SH_SS,  256),
    ("тень угла",       m.SH_UOZ, 256),
    ("кольцо приёма",   m.RING,   m.RING_MASK + 1),
    ("снимок кадра",    m.SNAP,   len(m.ADDR_LIST)),
    ("буфер блока",     m.STAGE,  m.BLK_MAX),
    ("перем. блока",    m.BLK_DST, 9),
    ("перем. дампа",    m.DMP_SRC, 3),
]
try: mine.append(("выход peek", m.PEEK_OUT, 1))
except AttributeError: mine.append(("выход peek", 0x1600, 1))

lines = [l.strip() for l in open(ASM, encoding="utf-8", errors="ignore")]
code = [(int(x.group(1), 16), x.group(2)) for l in lines
        for x in [re.match(r"^([0-9a-f]{4}):\s+(.*)$", l)] if x]

used = {}          # адрес -> причина
def mark(a, why):
    if 0x0040 <= a <= 0x1FFF and a not in used: used[a] = why

# 1) прямые операнды
for pc, ins in code:
    for h in re.findall(r"0x([0-9a-f]{4})", ins):
        mark(int(h, 16), "операнд @%04X: %s" % (pc, ins))

# 2) циклы LDX #$addr ... CPX #$end
for i, (pc, ins) in enumerate(code):
    mx = re.match(r"LDX #0x([0-9a-f]{4})", ins)
    if not mx: continue
    start = int(mx.group(1), 16)
    if not (0x0040 <= start <= 0x1FFF): continue
    for pc2, ins2 in code[i + 1:i + 20]:
        mc = re.match(r"CPX #0x([0-9a-f]{4})", ins2)
        if mc:
            end = int(mc.group(1), 16)
            if start < end <= 0x2000:
                for a in range(start, end): mark(a, "ЦИКЛ %04X..%04X @%04X" % (start, end - 1, pc))
            break

# 3) базы таблиц: LDX #$addr ; STX $0074/76/78
for i, (pc, ins) in enumerate(code):
    mx = re.match(r"LDX #0x([0-9a-f]{4})", ins)
    if not mx: continue
    base = int(mx.group(1), 16)
    if not (0x0040 <= base <= 0x1FFF): continue
    for pc2, ins2 in code[i + 1:i + 3]:
        if re.match(r"STX 0x007[468]", ins2):
            for a in range(base, min(base + 256, 0x2000)):
                mark(a, "БАЗА ТАБЛИЦЫ %04X @%04X (%s)" % (base, pc, ins2))
            break

print("заводской код касается %d адресов в $0040-$1FFF\n" % len(used))
bad = 0
for name, base, size in sorted(mine, key=lambda t: t[1]):
    hits = [(a, used[a]) for a in range(base, base + size) if a in used]
    tag = "✗ КОЛЛИЗИЯ" if hits else "✓ чисто"
    print("%-16s $%04X-$%04X  %s" % (name, base, base + size - 1, tag))
    if hits:
        bad += 1
        print("     пересечений: %d, напр. $%04X — %s" % (len(hits), hits[0][0], hits[0][1]))
        if len(hits) > 1: print("     ... и $%04X — %s" % (hits[-1][0], hits[-1][1]))
sys.exit(1 if bad else 0)
