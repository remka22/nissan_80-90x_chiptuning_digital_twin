#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка v15.2 из v15.1: три согласованные правки калибровок."""
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_NAME = 'j7es_v15.1_весовая-ТОЖ-на-холодную-по-логу-13.38_30.10.26_1440 ИИ.bin'
STOCK_NAME = 'j7es_v0.7.5.bin'
BASE_SHA256 = '20eda976b68be8ebd66be2e5c9f30fa20c43679c05f0fbffac50ffa8ee59d940'
STOCK_SHA256 = 'd64f5e6208e1d5f999c643f8c4a32e207744931ed8c3bdfce70a3ed9f2e584c4'
OUT_NAME = 'j7es_v15.2_давление-исходное-x4-УОЗ10-ПЦН045_31.10.26_1037 ИИ.bin'
DOUBLE_NAME = 'j7es_v15.2.2_128К-две-одинаковые-половины-v15.2_31.10.26_1037 ИИ.bin'


def read_source(name, digest):
    data = (HERE / name).read_bytes()
    if len(data) != 65536 or sha256(data).hexdigest() != digest:
        raise ValueError('Исходный файл не соответствует проверенному образу: ' + name)
    return data


def fix_sum(data):
    # Алгоритм действующего сборщика: компенсатор FFF8–FFF9, сумма FFFE–FFFF.
    data[0xFFF8:0xFFFA] = bytes(2)
    total = sum(data[:0xFFFE]) & 0xFFFF
    compensation = next(((255 * high - total) & 0xFFFF for high in range(256)
                         if ((255 * high - total) & 0xFFFF) <= 510), None)
    if compensation is None:
        raise ValueError('Не удалось подобрать компенсатор контрольной суммы')
    data[0xFFF8] = min(compensation, 255)
    data[0xFFF9] = compensation - data[0xFFF8]
    subtotal = sum(data[:0xFFFE])
    checksum = next(value for value in range(65536)
                    if (subtotal + (value & 255) + (value >> 8)) & 0xFFFF == value)
    data[0xFFFE:0x10000] = checksum.to_bytes(2, 'little')


def main():
    base = read_source(BASE_NAME, BASE_SHA256)
    stock = read_source(STOCK_NAME, STOCK_SHA256)
    data = bytearray(base)
    # 9E7C: 39 температурных точек, коэффициент = байт / 256.
    pressure = [value * 4 for value in stock[0x9E7C:0x9EA3]]
    if max(pressure) > 255:
        raise ValueError('Кривая давления ×4 не помещается в байт')
    data[0x9E7C:0x9EA3] = bytes(pressure)
    # 5FF4: шаг 0.5°, 10° кодируются байтом 20.
    data[0x5FF4] = 20
    if not data[0x5F02] & 0x10:
        raise ValueError('В исходной прошивке не включена ПЦН 32×32')
    minimum = int.from_bytes(data[0x5EF2:0x5EF4], 'little') / 60
    pressure_step = 2048 / (data[0x5EF4] * 60)
    rows = [row for row in range(32) if 20 <= minimum + row * 8 * pressure_step <= 42.8]
    if rows != [0, 1, 2, 3]:
        raise ValueError('Ось давления отличается от проверенной')
    # 0.45 не представимо: 58/128 = 0.453125 — ближайшее значение не ниже 0.45.
    floor_raw = 58
    changed_cells = []
    for row in rows:
        for column in range(32):
            address = 0x9294 + row * 32 + column
            if data[address] / 128 < 0.45:
                data[address] = floor_raw
                changed_cells.append(address)
    fix_sum(data)
    checksum = int.from_bytes(data[0xFFFE:0x10000], 'little')
    assert sum(data) & 0xFFFF == checksum
    allowed = (set(range(0x9E7C, 0x9EA3)) | {0x5FF4} | set(changed_cells)
               | {0xFFF8, 0xFFF9, 0xFFFE, 0xFFFF})
    changed = {address for address in range(65536) if data[address] != base[address]}
    assert changed <= allowed
    assert data[0x9E7C:0x9EA3] == bytes(pressure)
    assert data[0x5FF4] / 2 == 10
    for row in range(32):
        for column in range(32):
            address = 0x9294 + row * 32 + column
            expected = max(base[address], floor_raw) if row in rows else base[address]
            assert data[address] == expected
    single = bytes(data)
    outputs = [(HERE / OUT_NAME, single), (HERE / DOUBLE_NAME, single * 2)]
    # Проверяем оба имени до записи: существующий другой результат не перезаписываем.
    for path, content in outputs:
        if path.exists() and path.read_bytes() != content:
            raise ValueError('Уже существует другой файл: ' + str(path))
    for path, content in outputs:
        if not path.exists():
            path.write_bytes(content)
        assert path.read_bytes() == content
        print(path.name, len(content), 'байт; SHA256', sha256(content).hexdigest())
    assert outputs[1][0].read_bytes()[:65536] == outputs[1][0].read_bytes()[65536:] == single
    print('Строки ПЦН, кПа:', ', '.join('%.4f' % (minimum + row * 8 * pressure_step) for row in rows))
    print('Поднято ячеек ПЦН:', len(changed_cells), '; новое минимальное значение:', floor_raw / 128)
    print('Изменено байт:', len(changed), '; контрольная сумма: %04X' % checksum)


if __name__ == '__main__':
    main()
