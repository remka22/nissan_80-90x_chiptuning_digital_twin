#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разбор описания калибровок j7es для ChipTuningPro (j7es_0.7.4.j7, подпись CTM, cp1251).
Раскладка совпадает с j7es_v0.7.5.bin: код 0.7.5 читает все 159 таблиц и 275 из 277 констант (20.10.26).

Формат (найден 20.10.26):
  Каждый элемент дерева: [u16][имя: паскаль-строка в слоте 65 байт][глубина u8][вид u8]…
    вид 0 — папка; 1 — таблица 1D; 2 — карта 2D; 3 — константа; 4 — флаги.
  Калибровка (вид 1–4), h = начало после имени:
    h+2 u16 размер записи, h+4 u32 код (те же коды, что в .cte платной), h+8 u16 адрес XOR FBB8, h+10 = A6 28.
    Подписи: h+20 — ось X (у константы — единица), h+53 — значение, h+86 — ось Z (паскаль-строки).
    Константа: h+53 тип, h+55 делитель, h+79 множитель, h+87 смещение (double).
    1D: h+342 u16 точек, h+346 / h+354 X от / до, h+380 тип, h+384 делитель, h+408 множитель, h+416 смещение.
    2D: h+119 / h+375 ось X / Z текстом («!002-613C-40», «!004-5EF2-5EF4», «!006-7208»),
        h+631 / h+635 u16 размер X / Z, h+687 тип, h+692 делитель, h+716 множитель, h+724 смещение.
    Флаги: адреса байтов — h+8 и далее u32 с h+12 до нуля (FFFFFFFF — пустой байт);
        имена битов — слоты по 65 байт с h+568, слот = 8·номер байта + бит.
  Тип: 0 u8, 1 s8, 2 u16, 3 s16. Значение = (сырое − смещение) · множитель / делитель − смещение2
  (состав смеси: (сырое + 128) · 14.7 / 256; ДТОЖ: сырое − 60; темп. доп. вентилятора: сырое − 40 через смещение2).
  Шкала обратная, если задан K: значение = K · множитель / (делитель · (сырое − смещение)) − смещение2
  (диапазон давления 8248.5 / 102 = 81 кПа; шаг GBC 341.13 / 171 = 2 мг; импульсы ДСА 180 / 30 = 6 на метр).
  Поля от делителя: +8 смещение2, +16 K, +24 множитель, +32 смещение (у константы делитель h+55, 1D h+384, 2D h+692).
"""
import struct

KEY = 0xFBB8


def _pstr(d, p, maxlen=64):
    n = d[p]
    if not 1 <= n <= maxlen:
        return ''
    s = d[p + 1:p + 1 + n]
    if 0 in s:
        return ''
    try:
        return s.decode('cp1251').strip()
    except UnicodeDecodeError:
        return ''


def _dbl(d, a):
    return struct.unpack('<d', d[a:a + 8])[0]


def _axis(spec):
    """«!002-613C-40» → квантование по таблице; «!004-5EF2-5EF4» → минимум/шаг; «!006-7208» → таблица ДПДЗ."""
    if not spec.startswith('!'):
        return None
    parts = spec[1:].split('-')
    if len(parts) == 3 and len(parts[2]) < 4:                  # таблица квантования, шаг входа (десятичный)
        return dict(kind='q', tab=int(parts[1], 16), xstep=int(parts[2]), len=256)
    if len(parts) == 3:                                         # минимум (u16) и шаг (u8)
        return dict(kind='mm', min=int(parts[1], 16), rng=int(parts[2], 16))
    if len(parts) == 2:                                         # ДПДЗ: 101 точка, вход — %
        return dict(kind='q', tab=int(parts[1], 16), xstep=1, len=101)
    return None


def load(path):
    d = open(path, 'rb').read()
    items = []
    for p in range(0x40, len(d) - 80):
        name = _pstr(d, p)
        if not name:
            continue
        depth, kind = d[p + 65], d[p + 66]
        h = p + 65
        if kind in (1, 2, 3, 4) and d[h + 10:h + 12] == b'\xa6\x28':      # хвост слота имени бывает с мусором
            it = dict(p=p, name=name, depth=depth, kind=kind, code=struct.unpack('<I', d[h + 4:h + 8])[0],
                      addr=struct.unpack('<H', d[h + 8:h + 10])[0] ^ KEY)
            if kind == 3:
                it.update(ty=d[h + 53], div=_dbl(d, h + 55), mul=_dbl(d, h + 79), off=_dbl(d, h + 87),
                          unit=_pstr(d, h + 20, 30), n=1, nx=1, nz=1)
            elif kind == 1:
                n = struct.unpack('<H', d[h + 342:h + 344])[0]
                it.update(ty=d[h + 380], div=_dbl(d, h + 384), mul=_dbl(d, h + 408), off=_dbl(d, h + 416),
                          xl=_pstr(d, h + 20, 30), vl=_pstr(d, h + 53, 30), nx=n, nz=1, n=n,
                          xax=dict(kind='lin', a=_dbl(d, h + 346), b=_dbl(d, h + 354)))
            elif kind == 2:
                nx, nz = struct.unpack('<H', d[h + 631:h + 633])[0], struct.unpack('<H', d[h + 635:h + 637])[0]
                it.update(ty=d[h + 687], div=_dbl(d, h + 692), mul=_dbl(d, h + 716), off=_dbl(d, h + 724),
                          xl=_pstr(d, h + 20, 30), vl=_pstr(d, h + 53, 30), zl=_pstr(d, h + 86, 30),
                          nx=nx, nz=nz, n=nx * nz,
                          xax=_axis(_pstr(d, h + 119, 30)), zax=_axis(_pstr(d, h + 375, 30)))
            else:
                lst, i = [it['addr']], h + 12
                while True:
                    v = struct.unpack('<I', d[i:i + 4])[0]
                    if v == 0:
                        break
                    lst.append(v)
                    i += 4
                bits = []
                for k in range(8 * len(lst)):
                    nm = _pstr(d, h + 568 + 65 * k)
                    if nm and lst[k // 8] != 0xFFFFFFFF:
                        bits.append((lst[k // 8], k % 8, nm))
                it.update(bits=bits, n=0)
            if kind in (1, 2, 3):
                if it['ty'] not in (0, 1, 2, 3) or not it['div']:
                    continue
                it['w'] = 2 if it['ty'] >= 2 else 1
                dv = h + {3: 55, 1: 384, 2: 692}[kind]               # смещение2 и K — после делителя
                it.update(off2=_dbl(d, dv + 8), inv=_dbl(d, dv + 16))
            items.append(it)
        elif (kind == 0 and 1 <= depth <= 6 and d[p + 67] == 0 and not any(d[p + 1 + d[p]:p + 65])
              and (name[0].isalnum() or name[0] in '«(')):
            items.append(dict(p=p, name=name, depth=depth, kind=0))
    items.sort(key=lambda x: x['p'])
    # путь в дереве по глубине
    stack = []
    out = []
    for it in items:
        while stack and stack[-1][0] >= it['depth']:
            stack.pop()
        if it['kind'] == 0:
            stack.append((it['depth'], it['name']))
            continue
        it['path'] = ' › '.join(n for _, n in stack) or 'Общее'
        out.append(it)
    return out


if __name__ == '__main__':
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    cal = load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'j7es_0.7.4.j7'))
    from collections import Counter
    print(len(cal), Counter(c['kind'] for c in cal))
    for c in cal[:12]:
        print('%04X %d %s | %s' % (c['addr'], c['kind'], c['name'], c['path']))
