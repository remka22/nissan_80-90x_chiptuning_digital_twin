# v44_2 — дочерняя к v44: тарировка нового ДАД ПРЯМО ПО ДВУМ ТОЧКАМ МАНОМЕТРА.
# Код не тронут. Заменяет v44_1.
#
# v44_1 (наклон по 40↔170, ноль по атмосфере 355 = 100) по логу 25.10.26 15:03
# беднит: ХХ AFR 16–22 при цели 14.7, обороты качаются 450↔1900. Сдвиг
# «манометр врёт на −8 кПа» не подтвердился, к тому же заглушенный мотор
# в логе даёт АЦП 338–339, а не 355.
# Здесь — прямая через 40 кПа = АЦП 58 и 170 кПа = АЦП 624 без сдвига.
#
# Формула блока ($C708, v41): кПа = ((АЦП × $CA11) >> 8) + $CA10, насыщение 255.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "логер", "j30_v44_ТЗ-КТЗ-в-кадре-и-ДТВ-20-при-отказе_02.10.26_2146 ИИ.bin")

OFS, SLOPE = 0x4A10, 0x4A11          # $CA10 смещение (кПа), $CA11 наклон (кПа на 256 отсчётов)
OLD = (7, 34)                        # старый датчик, v44

PTS = [(58, 40), (624, 170)]         # АЦП -> кПа, манометр


def kpa(adc, ofs, slope):
    return min(255, ((adc * slope) >> 8) + ofs)


def calib():
    (x1, y1), (x2, y2) = PTS
    slope = round((y2 - y1) * 256 / (x2 - x1))
    # смещение — чтобы обе точки легли с наименьшей ошибкой при целом наклоне
    ofs = min(range(0, 60), key=lambda o: sum(abs(kpa(x, o, slope) - y) for x, y in PTS))
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
    b[OFS], b[SLOPE] = ofs, slope
    checksum(b)
    open(out_path, "wb").write(b)
    return ofs, slope


if __name__ == "__main__":
    import sys
    out = sys.argv[1]
    ofs, slope = build(out)
    print("смещение $CA10 = %d кПа, наклон $CA11 = %d (v44: %d / %d, v44_1: 19 / 59)" % (ofs, slope, *OLD))
    for adc, p in PTS + [(339, None), (355, None)]:
        print("  АЦП %4d: %s -> блок покажет %3d" % (adc, ("точка %3d кПа" % p) if p else "атмосфера   ", kpa(adc, ofs, slope)))
    print("  АЦП 1023 (5 В) -> %d кПа" % kpa(1023, ofs, slope))
    print("  ловушка $8910: АЦП 32 = %d кПа — ниже блок видит обрыв" % kpa(32, ofs, slope))
    print("записан:", out)
