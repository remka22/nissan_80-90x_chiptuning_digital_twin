# -*- coding: utf-8 -*-
"""
Фейковый ЭБУ для дампа ОЗУ: держит меняющийся образ ОЗУ и отдаёт его
БЛОКАМИ по кругу (бегущий указатель), как это будет делать подпрограмма.
"""
import math
import ramframe

# два диапазона, как в реальном патче: внутр. ОЗУ 6303 + внешн. ОЗУ HD63140
RANGES = [(0x0040, 0x0100), (0x1400, 0x1800)]
BLOCK = 16                          # байт данных в блоке (как в патче)

# старты блоков (16-байт, не пересекают границы диапазонов)
_starts = []
for _lo, _hi in RANGES:
    _a = _lo
    while _a < _hi:
        _starts.append(_a)
        _a += BLOCK
_seg = [0]


def _cell(addr, t):
    """Значение ячейки ОЗУ (0..255) в момент t. «Живые» метки шевелятся,
    остальное = младший байт адреса (узнаваемо для сверки)."""
    v = {
        0x140A: int(1 + 1 * math.sin(t)),            # обороты hi (с $140B)
        0x140B: int(128 + 120 * math.sin(t * 1.7)),  # обороты lo
        0x1482: int(110 + 90 * math.sin(t * 1.3)),   # нагрузка
        0x1437: int(128 + 20 * math.sin(t * 0.9)),   # ALPHA
        0x1400: int(48 + 40 * math.sin(t * 9)),      # O2 (быстрый)
        0x008F: int(180 + 4 * math.sin(t * 0.3)),    # напряжение (ВНУТР. ОЗУ)
        0x00B1: int(90 + 5 * math.sin(t * 0.1)),     # темп ОЖ (ВНУТР. ОЗУ)
    }.get(addr)
    return (v & 0xFF) if v is not None else (addr & 0xFF)


def next_block(t):
    """Следующий блок дампа (bytes) для момента t — по кругу обоих диапазонов."""
    start = _starts[_seg[0] % len(_starts)]
    _seg[0] += 1
    data = bytes(_cell(start + k, t) for k in range(BLOCK))
    return ramframe.encode_block(start, data)
