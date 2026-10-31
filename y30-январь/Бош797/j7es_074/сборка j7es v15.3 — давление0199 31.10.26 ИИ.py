#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка v15.3 из v15.2: только 9E7C = 51/256 во всех точках ТОЖ."""
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_NAME = 'j7es_v15.2_давление-исходное-x4-УОЗ10-ПЦН045_31.10.26_1037 ИИ.bin'
BASE_SHA256 = '94d53ebf0773227f8f498240145fbc7cf7d736abe4e5060745ef36d28dc52440'
OUT_NAME = 'j7es_v15.3_давление0199-УОЗ10-ПЦН045_31.10.26_1123 ИИ.bin'
DOUBLE_NAME = 'j7es_v15.3.2_128К-две-одинаковые-половины-v15.3_31.10.26_1123 ИИ.bin'


def main():
    base = (HERE / BASE_NAME).read_bytes()
    if len(base) != 65536 or sha256(base).hexdigest() != BASE_SHA256:
        raise ValueError('Исходная v15.2 не соответствует проверенному образу')
    # Используем проверенный пересчёт контрольной суммы предыдущей сборки.
    spec = spec_from_file_location('build_v152', HERE / 'сборка j7es v15.2 — давление-x4-УОЗ10-ПЦН045 31.10.26 ИИ.py')
    previous = module_from_spec(spec)
    spec.loader.exec_module(previous)
    data = bytearray(base)
    # 0.199 в редакторе = 51/256 = 0.19921875 в бинарнике.
    data[0x9E7C:0x9EA3] = bytes([51]) * 39
    previous.fix_sum(data)
    checksum = int.from_bytes(data[0xFFFE:0x10000], 'little')
    assert sum(data) & 0xFFFF == checksum
    allowed = set(range(0x9E7C, 0x9EA3)) | {0xFFF8, 0xFFF9, 0xFFFE, 0xFFFF}
    changed = {address for address in range(65536) if data[address] != base[address]}
    assert changed <= allowed
    assert data[0x9E7C:0x9EA3] == bytes([51]) * 39
    assert data[0x5FF4] == base[0x5FF4] == 20
    assert data[0x9294:0x9694] == base[0x9294:0x9694]
    single = bytes(data)
    outputs = [(HERE / OUT_NAME, single), (HERE / DOUBLE_NAME, single * 2)]
    # Проверяем оба имени до записи; другой существующий файл не перезаписываем.
    for path, content in outputs:
        if path.exists() and path.read_bytes() != content:
            raise ValueError('Уже существует другой файл: ' + str(path))
    for path, content in outputs:
        if not path.exists():
            path.write_bytes(content)
        assert path.read_bytes() == content
        print(path.name, len(content), 'байт; SHA256', sha256(content).hexdigest())
    doubled = outputs[1][0].read_bytes()
    assert doubled[:65536] == doubled[65536:] == single
    print('9E7C: 0.19921875 во всех 39 точках; ДК УОЗ: 10°; ПЦН сохранена из v15.2')
    print('Изменено байт:', len(changed), '; контрольная сумма: %04X' % checksum)


if __name__ == '__main__':
    main()
