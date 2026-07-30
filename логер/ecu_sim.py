# -*- coding: utf-8 -*-
"""
Фейковый ЭБУ — генерит тот же байт-поток, что реальный блок по SCI.
Нужен, чтобы тестировать демон и страницу БЕЗ железа («в вакууме»).

Значения шевелятся по синусоиде (без random — воспроизводимо), чтобы на
странице было видно движение. Обороты гуляют 800..3500, нагрузка/O2 следом.
"""
import math
import frame


def gen_raw(t):
    """t — секунды (float). Вернуть dict сырых значений, как в ОЗУ ЭБУ."""
    # обороты 800..3500, период ~8 c
    rpm_phys = 2150 + 1350 * math.sin(t * 2 * math.pi / 8.0)
    rpm_raw = int(rpm_phys / 12.807) & 0xFFFF
    # нагрузка следует за оборотами 20..200
    load = int(110 + 90 * math.sin(t * 2 * math.pi / 8.0)) & 0xFF
    # O2 колеблется вокруг точки переключения (узкополосник дёргается быстро)
    o2 = int(48 + 40 * math.sin(t * 2 * math.pi / 0.7)) & 0xFF
    # Tp пропорционален нагрузке/оборотам
    tp = int(load * 6) & 0xFFFF
    # ALPHA бродит вокруг 128 (100% коррекции)
    alpha = int(128 + 20 * math.sin(t * 2 * math.pi / 5.0)) & 0xFF
    # напряжение ~14В: raw ~ 14/0.0195 ≈ 718, но байт 8-бит -> берём оценку ~180
    volt = int(180 + 4 * math.sin(t * 2 * math.pi / 11.0)) & 0xFF
    return {"rpm": rpm_raw, "load": load, "o2": o2,
            "tp": tp, "alpha": alpha, "volt": volt}


def gen_afr(t):
    """Фейковый AFR (для проверки мержа второго источника без ШДК)."""
    return round(14.7 + 1.5 * math.sin(t * 2 * math.pi / 6.0), 2)


def frame_bytes(t):
    """Готовый кадр (bytes) для момента t."""
    return frame.encode(gen_raw(t))


if __name__ == "__main__":
    # печать нескольких кадров в hex — глазами убедиться, что поток осмысленный
    for i in range(4):
        b = frame_bytes(i * 0.05)
        print("t=%.2f  " % (i * 0.05), " ".join("%02X" % x for x in b))
