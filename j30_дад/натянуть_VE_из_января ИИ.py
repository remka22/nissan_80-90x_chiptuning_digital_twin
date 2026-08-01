# -*- coding: utf-8 -*-
"""
Предварительная VE для J30-ДАД: берём наполнение из ЯНВАРСКОГО тюна (VG30ET,
«ПЦН ДАД итог», массив z в ecu_twin/frontend/dad_data.json — 31×31 по [давление][обороты]),
билинейно НАТЯГИВАЕМ на оси нашей J30-VE (обороты 0x7B20 ×50, давление 0x4A00 кПа),
ОБРЕЗАЯ по диапазону январской таблицы (точки вне — прижимаются к краю).

Значение январского z = доля наполнения (1.0=100%). Наша VE: байт, 0x80=1.0.
Пишем VE_байт = clamp(round(z×128), 1, 255) в 0x4900 бина v8+ДАД. Чек-сумма пересчитывается.

⚠ Это ФОРМА (контур наполнения rpm×давление) с турбо-VG30ET → на атмо-VG30E.
Абсолютный уровень потом трим КМ + по ШДК. Буст (>110 кПа) не переносится (обрезан осью).
"""
import os, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DAD = os.path.join(ROOT, "ecu_twin", "frontend", "dad_data.json")
SRC = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(ROOT, "логер", "J30_дад_v8-узкий_01.08.26 ИИ.bin")
DST = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(ROOT, "логер", "J30_дад_v8_пцн-предв_01.08.26 ИИ.bin")
VEMAP = 0x4900   # файл-смещение VE (CPU C900)
RAXIS = 0x7B20   # обороты (raw ×50)
PAXIS = 0x4A00   # давление, кПа


def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def bilinear(x, y, XA, YA, Z):
    # Z[iy][ix]; XA возр., YA возр. Точки вне диапазона прижимаем к краю (обрезка).
    x = clamp(x, XA[0], XA[-1]); y = clamp(y, YA[0], YA[-1])
    def span(v, A):
        for i in range(len(A) - 1):
            if v <= A[i + 1]:
                t = 0.0 if A[i + 1] == A[i] else (v - A[i]) / (A[i + 1] - A[i])
                return i, i + 1, t
        return len(A) - 2, len(A) - 1, 1.0
    ix0, ix1, tx = span(x, XA)
    iy0, iy1, ty = span(y, YA)
    z00 = Z[iy0][ix0]; z01 = Z[iy0][ix1]; z10 = Z[iy1][ix0]; z11 = Z[iy1][ix1]
    a = z00 + (z01 - z00) * tx
    b = z10 + (z11 - z10) * tx
    return a + (b - a) * ty


def main():
    d = json.load(open(DAD, encoding="utf-8"))
    jrpm, jpress, Z = d["rpm"], d["press"], d["z"]     # jrpm[31], jpress[31], Z[31][31]
    rom = bytearray(open(SRC, "rb").read()); assert len(rom) == 32768
    rd = lambda a, n: list(rom[a:a + n])
    j_rax_raw = rd(RAXIS, 16)                            # наши обороты raw
    our_rpm = [b * 50 for b in j_rax_raw]               # об/мин
    our_press = rd(PAXIS, 16)                           # кПа

    grid = []
    for pj in our_press:                                # строки = давление
        row = []
        for rj in our_rpm:                              # столбцы = обороты
            ve = bilinear(rj, pj, jrpm, jpress, Z)      # доля наполнения
            row.append(ve)
        grid.append(row)

    # запись VE (память: rpm=ряды, press=колонки → offset rpm_idx*16 + press_idx)
    for ri in range(16):
        for pi in range(16):
            ve = grid[pi][ri]
            byte = int(round(ve * 128))
            byte = clamp(byte, 1, 255)
            rom[VEMAP + ri * 16 + pi] = byte

    # чек-сумма
    s = x = 0
    for i in range(len(rom)):
        if i in (0x7F7A, 0x7F7B): continue
        s = (s + rom[i]) & 0xFF; x ^= rom[i]
    rom[0x7F7A], rom[0x7F7B] = s, x
    open(DST, "wb").write(rom)

    print("Готово:", os.path.basename(DST))
    print("  наши обороты:", our_rpm[0], "…", our_rpm[-1], "| давление:", our_press[0], "…", our_press[-1], "кПа")
    print("  диапазон января: об %d-%d, давл %g-%g кПа" % (jrpm[0], jrpm[-1], jpress[0], jpress[-1]))
    print("  чек-сумма: %02X/%02X" % (s, x))
    print("  --- натянутая VE (доля наполнения), ряд=давление кПа, стб=обороты ---")
    hdr = "  давл\\об " + " ".join("%5d" % r for r in our_rpm)
    print(hdr)
    for pi in range(16):
        print("  %5d   " % our_press[pi] + " ".join("%5.2f" % grid[pi][ri] for ri in range(16)))


if __name__ == "__main__":
    main()
