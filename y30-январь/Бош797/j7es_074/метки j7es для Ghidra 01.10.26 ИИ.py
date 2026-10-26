#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собирает файл меток для проекта Ghidra по прошивке j7es (Январь 7.2, C509).

Три источника:
  1. Ручные метки: то, что разобрано по листингу (обработчик зуба, счётчики, выходы).
  2. Регистры C509, которых нет в стандартном описании 8051 у Ghidra.
  3. Названия калибровок: таблицы находятся в платной прошивке по значениям из выгрузки .cte,
     переносятся в j7es со сдвигом -0x70000 и принимаются, только если код j7es читает этот адрес
     командой MOV DPTR,#адрес.

Запуск (из папки j7es_074):
    python3 "метки j7es для Ghidra 01.10.26 ИИ.py"
Результат: "j7es метки для Ghidra 01.10.26 ИИ.tsv" (пространство, адрес, имя, комментарий).
"""
import glob
import importlib.util
import os
import re
import sys

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'j7es_v0.7.5.bin')
PAID = os.path.join(HERE, '..', '..', 'Логи 28.09.26', '270926_Popravka_vozobravlenia_toplivopodachi.bin')
CTE_DIR = os.path.join(HERE, '..', '..', 'Логи 28.09.26')
OUT = os.path.join(HERE, 'j7es метки для Ghidra 01.10.26 ИИ.tsv')

# --- 1. Ручные метки (проверены по листингу) ---
CODE = [
    (0xDF4E, 'старт_после_сброса', 'Сюда процессор прыгает после включения (вектор 0000).'),
    (0x0105, 'обработчик_зуба_ДПКВ',
     'Прерывание по захвату CC3 (вектор 006B), вход ДПКВ на P1.3. Банк регистров 3. '
     'R2:R3 = время текущего зуба, R4:R5 = период зуба, R6 = зуб за оборот 0..59, R7 = зуб внутри такта 0..29, '
     'ячейка 40h = номер такта 0..3 (такт = 30 зубьев = 180°). Диск 60-2.'),
    (0x00E0, 'дорисовка_пропущенных_зубьев',
     'Зубья 57-59: таймер CC3 в режиме сравнения сам отмеряет время пропущенного зуба.'),
    (0x0231, 'потеря_синхронизации', 'Зуб не там, где ждали: сброс синхронизации, все катушки P4.4-P4.7 в 1 (выкл).'),
    (0x0246, 'нормальный_зуб', 'Период зуба прошёл проверку. Здесь счёт зубьев и граница такта.'),
    (0x0271, 'счёт_зуба', 'R6++, на 30-м зубе (1Eh) R7=0 и номер такта (40h) +1 по модулю 4.'),
    (0x028F, 'начало_оборота', 'Зуб 0 после пропуска. Номер такта 0 или 2 по датчику фаз P1.2 или чередованием.'),
    (0x02B9, 'события_по_зубу', 'Отсюда раздаются события по номеру зуба: замер периода, впрыск, зажигание.'),
    (0x0346, 'событие_расчёта_впрыска', 'Если R7 = зуб события впрыска (3Ch): запуск задачи INT0 (флаг 28h.0, TCON.1).'),
    (0x03BC, 'подготовка_зажигания',
     'На 8-м зубе такта: номер цилиндра для зажигания (43h), выбор записи таблицы 80h-8Fh, запуск расчёта (28h.2).'),
    (0x0478, 'катушки_A_начало_заряда', 'Зуб = 10h: ставим момент начала заряда на CM4 (P4.4) или CM7 (P4.7).'),
    (0x0500, 'катушки_A_искра', 'Зуб = 12h: ставим момент искры на CM4 и CM7.'),
    (0x0547, 'катушки_B_начало_заряда', 'Зуб = 14h: начало заряда на CM6 (P4.6) или CM5 (P4.5).'),
    (0x05CE, 'катушки_B_искра', 'Зуб = 16h: искра на CM6 и CM5.'),
    (0x0614, 'выход_из_обработчика_зуба', None),
    (0x08F1, 'задача_INT0_расчёты',
     'Вектор INT0, но вызывается программно: обработчик зуба ставит флаг TCON.1. '
     'Флаг 28h.2 - расчёт зажигания, 28h.0 - расчёт и запуск впрыска.'),
    (0x061D, 'прерывание_таймера_1', None),
    (0xB9A7, 'прерывание_совпадения_CM', 'Совпадение одного из каналов CM0-CM7.'),
    (0x498E, 'прерывание_COMSET', None),
    (0xCB05, 'прерывание_последовательного_порта', 'Связь с диагностикой.'),
    (0xBA42, 'прерывание_INT1_пустое', 'Только RETI.'),
    (0x1626, 'открытие_форсунок',
     'Маска форсунок из таблицы A558 по такту впрыска (41h): фаз. 02 04 01 08, попарно 03 0C 03 0C. '
     'Каналы CM0-CM3 = P4.0-P4.3.'),
    (0x3D55, 'расчёт_фазы_впрыска',
     'Фаза впрыска в зубьях цикла 0..119 (78h), делится на 30: частное -> такт (3Fh), остаток -> зуб (3Eh).'),
    (0xA558, 'маски_форсунок_по_такту', '8 байт: фазированный 02 04 01 08, попарный 03 0C 03 0C.'),
]
INTMEM = [
    (0x05, 'состояние_синхронизации', '0..4, 4 = синхронизирован.'),
    (0x10, 'катушки_A_зуб_заряда', None), (0x11, 'катушки_A_доля_заряда', 'Доля периода зуба, 1/128.'),
    (0x12, 'катушки_A_зуб_искры', None), (0x13, 'катушки_A_доля_искры', None),
    (0x14, 'катушки_B_зуб_заряда', None), (0x15, 'катушки_B_доля_заряда', None),
    (0x16, 'катушки_B_зуб_искры', None), (0x17, 'катушки_B_доля_искры', None),
    (0x1A, 'время_зуба_L', 'Банк 3, R2: время текущего зуба (младший).'),
    (0x1B, 'время_зуба_H', 'Банк 3, R3.'),
    (0x1C, 'период_зуба_L', 'Банк 3, R4.'), (0x1D, 'период_зуба_H', 'Банк 3, R5.'),
    (0x1E, 'зуб_за_оборот', 'Банк 3, R6: 0..59.'), (0x1F, 'зуб_в_такте', 'Банк 3, R7: 0..29.'),
    (0x36, 'время_начала_такта_L', None), (0x37, 'время_начала_такта_H', None),
    (0x38, 'период_такта_180_L', 'Время последних 180°, отсюда обороты.'), (0x39, 'период_такта_180_H', None),
    (0x3C, 'зуб_события_впрыска', None), (0x3D, 'такт_события_впрыска', None),
    (0x3E, 'зуб_события_впрыска_новый', 'Записывает расчёт фазы, обработчик зуба переносит в 3Ch.'),
    (0x3F, 'такт_события_впрыска_новый', None),
    (0x40, 'номер_такта', '0..3, такт = 180°. +1 на 30-м зубе, на зубе 0 ставится 0 или 2.'),
    (0x41, 'такт_впрыска', '(номер_такта - такт_события_впрыска) & 3, индекс в маски_форсунок_по_такту.'),
    (0x42, 'зуб_записи_цилиндра', None),
    (0x43, 'цилиндр_зажигания', 'Копия номера такта на 8-м зубе.'),
    (0x80, 'таблица_зажигания', '4 записи по 4 байта: зуб заряда, доля, зуб искры, доля.'),
    (0x90, 'цилиндр_для_катушки', '0..3: какой канал CM4-CM7 заряжать.'),
]
BITS = [
    (0x05, 'датчик_фаз_включён', 'Бит 20h.5.'),
    (0x0D, 'зажигание_попарно', 'Бит 21h.5: заряжать обе катушки пары.'),
    (0x40, 'флаг_расчёт_впрыска', 'Бит 28h.0, ставит обработчик зуба.'),
    (0x42, 'флаг_расчёт_зажигания', 'Бит 28h.2, ставит обработчик зуба на 8-м зубе такта.'),
]

# --- 2. Регистры C509 сверх стандартного 8051 (только уверенные имена) ---
SFR = {
    0x86: 'WDTREL', 0x91: 'XPAGE', 0x92: 'DPSEL', 0x98: 'S0CON', 0x99: 'S0BUF', 0x9A: 'IEN2',
    0x9B: 'S1CON', 0x9C: 'S1BUF', 0x9D: 'S1RELL', 0xA1: 'COMSETL', 0xA2: 'COMSETH', 0xA3: 'COMCLRL',
    0xA4: 'COMCLRH', 0xA5: 'SETMSK', 0xA6: 'CLRMSK', 0xA8: 'IEN0', 0xA9: 'IP0', 0xAA: 'S0RELL',
    0xB1: 'SYSCON', 0xB8: 'IEN1', 0xB9: 'IP1', 0xBA: 'S0RELH', 0xBB: 'S1RELH',
    0xC0: 'IRCON0', 0xC1: 'CCEN', 0xC2: 'CCL1', 0xC3: 'CCH1', 0xC4: 'CCL2', 0xC5: 'CCH2',
    0xC6: 'CCL3', 0xC7: 'CCH3', 0xC8: 'T2CON', 0xC9: 'CC4EN', 0xCA: 'CRCL', 0xCB: 'CRCH',
    0xCC: 'TL2', 0xCD: 'TH2', 0xCE: 'CCL4', 0xCF: 'CCH4', 0xD1: 'IRCON1',
    0xD2: 'CML0', 0xD3: 'CMH0', 0xD4: 'CML1', 0xD5: 'CMH1', 0xD6: 'CML2', 0xD7: 'CMH2',
    0xD8: 'ADCON0', 0xD9: 'ADDATH', 0xDA: 'ADDATL', 0xDB: 'P7', 0xDC: 'ADCON1', 0xDD: 'P8',
    0xDE: 'CTRELL', 0xDF: 'CTRELH', 0xE1: 'CTCON', 0xE2: 'CML3', 0xE3: 'CMH3', 0xE4: 'CML4',
    0xE5: 'CMH4', 0xE6: 'CML5', 0xE7: 'CMH5', 0xE8: 'P4', 0xE9: 'MD0', 0xEA: 'MD1', 0xEB: 'MD2',
    0xEC: 'MD3', 0xED: 'MD4', 0xEE: 'MD5', 0xEF: 'ARCON', 0xF2: 'CML6', 0xF3: 'CMH6',
    0xF4: 'CML7', 0xF5: 'CMH7', 0xF6: 'CMEN', 0xF7: 'CMSEL', 0xF8: 'P5', 0xFA: 'P6',
}


def label_name(s):
    """Имя метки: пробелы и знаки препинания -> подчёркивание."""
    s = re.sub(r'[^0-9A-Za-zА-Яа-яЁё_]+', '_', s.strip())
    return re.sub(r'_+', '_', s).strip('_')


def load_disasm():
    path = os.path.join(HERE, 'дизассемблер 8051 C509 01.10.26 ИИ.py')
    spec = importlib.util.spec_from_file_location('dz', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cte_tables():
    """Таблицы и карты из выгрузки .cte: (имя, раздел, варианты порядка значений)."""
    out = []
    for f in sorted(glob.glob(os.path.join(CTE_DIR, '*.cte'))):
        t = open(f, encoding='cp1251').read().replace('\r', '')
        for m in re.finditer(r'\[([0-9A-Fa-f]{8})\]\nName=(.*)\n((?:[^\[\n].*\n?)*)', t):
            kv = re.findall(r'^(\w+)=(.*)$', m.group(3), re.M)
            keys = [k for k, _ in kv]
            if not kv or 'Const' in keys or re.match(r'F\d+$', keys[0]):
                continue
            num = lambda s: float(s.replace(',', '.'))
            if any('Z' in k for k in keys):
                d = {}
                for k, v in kv:
                    x, z = re.match(r'X(\d+)Z(\d+)', k).groups()
                    d[(int(x), int(z))] = num(v)
                nx = max(x for x, _ in d)
                nz = max(z for _, z in d)
                var = [[d[(x, z)] for z in range(1, nz + 1) for x in range(1, nx + 1)],
                       [d[(x, z)] for x in range(1, nx + 1) for z in range(1, nz + 1)]]
            else:
                var = [[num(v) for _, v in kv]]
            out.append((m.group(2).strip(), os.path.basename(f)[:-4], var))
    return out


def find_affine(buf, base, v):
    """Адреса, где байты (8 или 16 бит, со знаком или без) равны значениям с точностью до масштаба."""
    v = np.array(v, dtype=float)
    n = len(v)
    i0, i1 = int(v.argmin()), int(v.argmax())
    span = v[i1] - v[i0]
    if span == 0:
        return []
    tol = max(abs(v).max(), span) * 2e-4 + 1e-6
    hits = []
    b = np.frombuffer(buf, dtype=np.uint8)
    views = [(b.astype(float), 1, 0), (b.view(np.int8).astype(float), 1, 0)]
    for off in (0, 1):
        bb = b[off:off + (len(b) - off) // 2 * 2]
        views += [(bb.view('<u2').astype(float), 2, off), (bb.view('<i2').astype(float), 2, off)]
    for arr, w, off in views:
        if len(arr) < n:
            continue
        W = swv(arr, n)
        d = W[:, i1] - W[:, i0]
        ok = d != 0
        a = np.where(ok, span / np.where(ok, d, 1), 0)
        err = np.abs(a[:, None] * (W - W[:, i0][:, None]) + v[i0] - v).max(axis=1)
        for k in np.nonzero(ok & (err < tol))[0]:
            hits.append(base + off + int(k) * w)
    return sorted(set(hits))


def calibration_labels(dpt_refs):
    paid = open(PAID, 'rb').read()
    z0, z1 = 0x75C00, 0x7B800
    res = []
    for name, sect, var in cte_tables():
        addrs = set()
        for v in var:
            addrs.update(find_affine(paid[z0:z1], z0, v))
        if len(addrs) != 1:
            continue
        a = addrs.pop() - 0x70000
        if a in dpt_refs:
            res.append((a, name, sect))
    return res


def main():
    dz = load_disasm()
    data = open(BIN, 'rb').read()
    dis = dz.Disasm(data).run()
    dpt = {}
    for pc, ins in dis.insn.items():
        m = re.match(r'MOV   DPTR,#([0-9A-F]{4})h', ins.text)
        if m:
            dpt.setdefault(int(m.group(1), 16), []).append(pc)

    rows = []
    for a, n, c in CODE:
        rows.append(('CODE', a, n, c or ''))
    for a, n, c in INTMEM:
        rows.append(('INTMEM', a, n, c or ''))
    for a, n, c in BITS:
        rows.append(('BITS', a, n, c or ''))
    for a, n in SFR.items():
        rows.append(('SFR', a, n, ''))
    cal = calibration_labels(dpt)
    taken = {a for s, a, _, _ in rows if s == 'CODE'}
    for a, name, sect in cal:
        if a in taken:
            continue
        taken.add(a)
        rows.append(('CODE', a, 'кал_' + label_name(name),
                     'Калибровка «%s» (раздел %s). Найдена по платной прошивке, код j7es читает её с %s.'
                     % (name, sect, ', '.join('%04X' % p for p in sorted(dpt[a])[:4]))))

    with open(OUT, 'w', encoding='utf-8') as f:
        for s, a, n, c in rows:
            f.write('%s\t%04X\t%s\t%s\n' % (s, a, n, c.replace('\t', ' ')))
    print('Меток: %d, из них калибровок: %d -> %s' % (len(rows), len(cal), OUT))


if __name__ == '__main__':
    sys.exit(main())
