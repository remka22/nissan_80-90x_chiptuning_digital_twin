# v44_1 — дочерняя к v44: ТОЛЬКО новая тарировка ДАД (новый датчик), код не тронут.
#
# Точки пользователя (АЦП 10 бит -> кПа), 25.10.26:
#   40 кПа -> 58,  170 кПа -> 624   — один манометр (насос)
#   100 кПа -> 355                  — мотор заглушен, коллектор на атмосфере
# Три точки на одну прямую не ложатся. Объяснение: манометр врёт на постоянную
# величину (как прошлый, см. «Канал давления ДАД ... 31.08.26», раздел 4).
# Тогда разность 170−40 верна -> НАКЛОН по ней, НОЛЬ — по атмосфере (=100 по
# нашему приведению, истина 96). При сдвиге манометра на −8 кПа все три точки
# ложатся на прямую точно.
#
# Формула блока ($C708, v41): кПа = ((АЦП × $CA11) >> 8) + $CA10, насыщение 255.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "логер", "j30_v44_ТЗ-КТЗ-в-кадре-и-ДТВ-20-при-отказе_02.10.26_2146 ИИ.bin")

OFS, SLOPE = 0x4A10, 0x4A11          # $CA10 смещение (кПа), $CA11 наклон (кПа на 256 отсчётов)
OLD = (7, 34)                        # старый датчик, v44

PTS = [(58, 40), (355, 100), (624, 170)]
ATMO_ADC, ATMO_KPA = 355, 100


def kpa(adc, ofs, slope):
    return min(255, ((adc * slope) >> 8) + ofs)


def calib():
    (x1, y1), (x2, y2) = PTS[0], PTS[2]
    slope = round((y2 - y1) * 256 / (x2 - x1))           # по разности манометра
    ofs = ATMO_KPA - ((ATMO_ADC * slope) >> 8)            # ноль по атмосфере
    return ofs, slope


def checksum(b):
    s = x = 0
    for i, v in enumerate(b):
        if i in (0x7F7A, 0x7F7B):
            continue
        s = (s + v) & 0xFF
        x ^= v
    b[0x7F7A], b[0x7F7B] = s, x


def build(out_path):
    b = bytearray(open(SRC, "rb").read())
    assert len(b) == 32768
    assert (b[OFS], b[SLOPE]) == OLD, "в исходнике не та тарировка: %d/%d" % (b[OFS], b[SLOPE])
    ofs, slope = calib()
    assert 0 <= ofs <= 255 and 0 < slope <= 255
    b[OFS], b[SLOPE] = ofs, slope
    checksum(b)
    open(out_path, "wb").write(b)
    return ofs, slope


if __name__ == "__main__":
    import sys
    out = sys.argv[1]
    ofs, slope = build(out)
    print("смещение $CA10 = %d кПа, наклон $CA11 = %d (было %d / %d)" % (ofs, slope, *OLD))
    for adc, p in PTS:
        print("  АЦП %4d: точка %3d кПа -> блок покажет %3d" % (adc, p, kpa(adc, ofs, slope)))
    print("  АЦП 1023 (5 В) -> %d кПа" % kpa(1023, ofs, slope))
    # ловушка $8910: АЦП < 32 подменяется на 16
    print("  ловушка $8910: АЦП 32 = %d кПа — ниже блок видит обрыв" % kpa(32, ofs, slope))
    print("записан:", out)
