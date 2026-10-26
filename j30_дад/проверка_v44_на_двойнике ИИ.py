# -*- coding: utf-8 -*-
"""
Проверка v44 на двойнике. Всё, что для v43, плюс:
  6. отказ ДТВ -> ТВ = +20 °C (70), расчёт дальше идёт как обычно;
  7. кадр ($CFC9) кладёт ТВ/ТЗ/КВТЗ/КТЗ на позиции 5, 6, 27, 28.

Исходное описание v43:
Проверка v43 (КТЗ/КВТЗ/ДТВ) на двойнике — настоящий код прошивки в эмуляторе 6303.

  1. КТЗ = 128 (и 0 — «ещё не посчитано»): выход ДАД-прослойки $C700
     ПОБАЙТНО равен v42_3 на сетке обороты × давление × дроссель.
  2. КТЗ = 154 (1.2): расход растёт на 20 % (с точностью 8-битной цепочки).
  3. KTZ_CALC против модели на питоне, повторяющей ассемблер построчно:
     ТВ, КВТЗ, ТЗ, КТЗ — на тестовой кривой КТЗ с разными значениями.
  4. Обрыв/КЗ канала 9 -> КТЗ = 128.
  5. Точки входа $D070 и $CD00 доходят до KTZ_CALC и возвращаются.
"""
import os
import sys
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "ecu_twin", "backend"))
from emulator.machine import Machine  # noqa: E402

spec = importlib.util.spec_from_file_location("bld", os.path.join(HERE, "build_v44_ktz-кадр ИИ.py"))
bld = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bld)

b43, lab, _, _ = bld.build()
T43 = "/tmp/v44_test.bin"
open(T43, "wb").write(b43)
m42 = Machine(bld.SRC)
m43 = Machine(T43)
for m in (m42, m43):
    r = m.boot(80_000)
    assert not r["crashed"], r
print("загрузка: обе прошивки стартуют без падений")
print("указатели VE/Ktps после старта: $D3=%04X $D5=%04X" % (m43.peek16(0xD3), m43.peek16(0xD5)))

FAIL = []


def dad(m, adc, rpm_raw, tps, ktz=None):
    m.poke16(0x1408, adc)
    m.poke16(0x140A, rpm_raw)
    m.poke8(0x14A2, tps)
    if ktz is not None:
        m.poke8(0xE4, ktz)
    info = m.call_routine(0xC700)
    assert info["reached_return"], info
    return m.cpu.D


# ---------------------------------------------------------------- 1. тождество
pts = [(adc, rpm, tps) for adc in range(0, 1024, 31) for rpm in range(20, 560, 23)
       for tps in (0, 40, 120, 172)]
for ktz in (128, 0):
    bad = 0
    for adc, rpm, tps in pts:
        d42 = dad(m42, adc, rpm, tps)
        d43 = dad(m43, adc, rpm, tps, ktz)
        if d42 != d43:
            bad += 1
            if bad <= 5:
                print("  РАСХОЖДЕНИЕ КТЗ=%d adc=%d rpm=%d tps=%d: %d против %d" % (ktz, adc, rpm, tps, d42, d43))
    print("1. КТЗ=%3d: %d точек, расхождений с v42_3: %d" % (ktz, len(pts), bad))
    if bad:
        FAIL.append("тождество КТЗ=%d" % ktz)

# ---------------------------------------------------------------- 2. масштаб
ratios = []
for adc, rpm, tps in pts:
    d42 = dad(m42, adc, rpm, tps)
    d43 = dad(m43, adc, rpm, tps, 154)
    if 2000 < d42 < 50000:
        ratios.append(d43 / d42)
ratios.sort()
med = ratios[len(ratios) // 2]
print("2. КТЗ=154 (1.203): отношение расходов медиана %.4f, разброс %.4f…%.4f (%d точек)"
      % (med, ratios[0], ratios[-1], len(ratios)))
if not (1.18 < med < 1.22):
    FAIL.append("масштаб")


# ---------------------------------------------------------------- 3. KTZ_CALC
def tab_interp(tab, i, b):
    """хвост заводских $80A9/$809F: точка i, доля b (байт), округление вниз"""
    if b == 0 or tab[i + 1] == tab[i]:
        return tab[i]
    if tab[i + 1] > tab[i]:
        return (tab[i] + (((tab[i + 1] - tab[i]) * b) >> 8)) & 0xFF
    return (tab[i + 1] + (((tab[i] - tab[i + 1]) * (256 - b)) >> 8)) & 0xFF


def f80a9(tab, a):
    a = min(a, 0xF8)
    return tab_interp(tab, a >> 3, (a & 7) << 5)


def f809f(tab, a):
    a = min(a, 0xF0)
    return tab_interp(tab, a >> 4, (a & 0xF) << 4)


def blend(a, b, fr):
    if b >= a:
        return (a + (((b - a) * fr) >> 4)) & 0xFF
    return (a - (((a - b) * fr) >> 4)) & 0xFF


def model(rom, raw, rpm_raw, p, toz, ktz_tab):
    fb30 = [rom[0xFB30 - 0x8000 + i] for i in range(32)]
    # v44: отказ ДТВ -> ТВ = +20 °C (70), дальше как обычно
    tv = 70 if (raw < 3 or raw >= 0xF2) else f80a9(fb30, raw)
    rpm8 = min(255, rpm_raw >> 1)
    idx = rpm8 - rom[0xCA20 - 0x8000] * 2
    idx = max(0, idx)
    row, rfr = idx >> 4, idx & 0xF
    if row >= 15:
        row, rfr = 15, 0
    lut = rom[0xC600 - 0x8000 + p]
    col, cfr = lut >> 4, lut & 0xF
    kvt = [rom[0xD200 - 0x8000 + i] for i in range(256)]

    def rowval(r):
        a = kvt[r * 16 + col]
        return blend(a, kvt[r * 16 + col + 1], cfr) if cfr else a
    kv = rowval(row)
    if rfr:
        kv = blend(kv, rowval(row + 1), rfr)
    if tv >= toz:
        tz = (toz + (((tv - toz) * kv) >> 7)) & 0xFF
    else:
        tz = (toz - (((toz - tv) * kv) >> 7)) & 0xFF
    a = tz - 10
    a = 0 if a < 0 else (0x9F if a >= 0xA0 else a)
    ix = ((a * 0xCD * 2) + 0x80) >> 8
    return dict(TV=tv, KV=kv, TZ=tz, KTZ=f809f(ktz_tab, ix))


test_curve = [60 + 9 * i for i in range(16)]          # возрастающая, все разные
for i, v in enumerate(test_curve):
    m43.poke8(bld.KTZ_TAB + i, v)
rom = bytearray(m43.bus.mem[0x8000:0x10000])
bad = n = 0
for raw in (2, 3, 20, 60, 100, 150, 200, 241, 242, 255):
    for rpm in (40, 120, 260, 400, 550):
        for p in (30, 60, 100, 128, 141, 200):
            for toz in (60, 100, 135, 160):
                # регистр результата HD63140 выровнен влево: 8-битный канал
                # читается из СТАРШЕГО байта, поэтому сырьё подаём как raw << 8
                m43.bus.adc[9] = raw << 8
                m43.poke16(0x140A, rpm)
                m43.poke8(0xF7, p)
                m43.poke8(0x140C, toz)
                info = m43.call_routine(lab["KTZ_CALC"])
                assert info["reached_return"], info
                got = dict(TV=m43.peek8(0xE2), KV=m43.peek8(0xE5), TZ=m43.peek8(0xE3), KTZ=m43.peek8(0xE4))
                exp = model(rom, raw, rpm, p, toz, test_curve)
                ok = all(got[k] == v for k, v in exp.items()) and m43.peek8(0x17E0) == raw
                n += 1
                if not ok:
                    bad += 1
                    if bad <= 6:
                        print("  РАСХОЖДЕНИЕ raw=%d rpm=%d P=%d ТОЖ=%d: двойник %s модель %s"
                              % (raw, rpm, p, toz, got, exp))
print("3–4. KTZ_CALC: %d комбинаций, расхождений с моделью: %d" % (n, bad))
if bad:
    FAIL.append("KTZ_CALC")

# ---------------------------------------------------------------- 5. точки входа
# Главный цикл через $83F8 в двойнике не крутится (ни на старте, ни в «живом
# моторе» — двойник гоняет цепочку топлива, а не весь цикл). Поэтому зовём сами
# входы: $D070 (там теперь JMP KTZ_CALC) и всю нашу врезку логгера $CD00, которую
# в машине вызывает главный цикл. Кривую КТЗ возвращаем на 1.0, как в бине.
for i in range(16):
    m43.poke8(bld.KTZ_TAB + i, 128)
for entry in (0xD070, 0xCD00):
    m43.bus.adc[9] = 150 << 8
    m43.poke8(0xE4, 0)
    m43.poke16(0x140A, 300)
    m43.poke8(0xF7, 100)
    m43.poke8(0x140C, 135)
    info = m43.call_routine(entry)
    print("5. вход $%04X: вернулся=%s падение=%s | сырьё $E1=%d $17E0=%d ТВ=%d ТЗ=%d КВТЗ=%d КТЗ=%d"
          % (entry, info["reached_return"], info["crashed"], m43.peek8(0xE1), m43.peek8(0x17E0),
             m43.peek8(0xE2), m43.peek8(0xE3), m43.peek8(0xE5), m43.peek8(0xE4)))
    if not info["reached_return"] or info["crashed"] or m43.peek8(0xE4) != 128 or m43.peek8(0xE1) != 150:
        FAIL.append("вход $%04X" % entry)

# ---------------------------------------------------------------- 6. отказ ДТВ
for raw in (0, 2, 242, 255):
    m43.bus.adc[9] = raw << 8
    m43.call_routine(lab["KTZ_CALC"])
    print("6. отказ ДТВ, сырьё %3d: ТВ=%d (ждём 70 = +20 °C), ТЗ=%d, КТЗ=%d"
          % (raw, m43.peek8(0xE2), m43.peek8(0xE3), m43.peek8(0xE4)))
    if m43.peek8(0xE2) != 70:
        FAIL.append("отказ ДТВ")

# ---------------------------------------------------------------- 7. кадр
for a, v in ((0xE2, 0x11), (0xE3, 0x22), (0xE5, 0x33), (0xE4, 0x44)):
    m43.poke8(a, v)
info = m43.call_routine(0xCFC9)
got = {pos: m43.peek8(0x17A0 + pos) for pos in (5, 6, 27, 28)}
print("7. кадр: позиции 5/6/27/28 =", {k: hex(v) for k, v in got.items()},
      "(ждём ТВ 0x11, ТЗ 0x22, КВТЗ 0x33, КТЗ 0x44)")
if got != {5: 0x11, 6: 0x22, 27: 0x33, 28: 0x44} or not info["reached_return"]:
    FAIL.append("кадр")

print("\nИТОГ:", "ВСЁ СХОДИТСЯ" if not FAIL else "ПРОВАЛ: " + ", ".join(FAIL))
