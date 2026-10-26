#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собирает «редактор калибровок j7es ИИ.html» по собственному описанию j7es (j7es_0.7.4.j7, разбор — модуль
«описание j7es (.j7) — разбор 20.10.26 ИИ.py»): дерево, названия, адреса, масштабы, оси и флаги — как в ChipTuningPro.

Сопоставление с платной j796 (выгрузки .cte, Логи 28.09.26):
  - по коду калибровки; коды вида xx00FFyy — порядковые, у двух прошивок значат разное → ещё и сходство названия;
  - иначе по точному названию (уникальному в обеих) и размеру;
  - значения платной: таблица находится в 270926_…bin поиском значений, читается из прошивки 18.10.26 по тому же
    адресу; не найдена — значения выгрузки 28.09; константы и флаги — только из выгрузки 28.09.
Цвета в дереве: синий — есть в j7es, нет в платной; красный — есть в платной, нет в j7es (только просмотр).

Запуск (из папки j7es_074):
    python3 "редактор калибровок j7es — генератор по описанию .j7 20.10.26 ИИ.py"           → редактор
    python3 "…" --list "файл.tsv"                                                            → + список переноса таблиц
"""
import argparse
import base64
import difflib
import glob
import importlib.util
import json
import os
import re
import struct

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv

HERE = os.path.dirname(os.path.abspath(__file__))
Y30 = os.path.dirname(os.path.dirname(HERE))
LOGS = os.path.join(Y30, 'Логи 28.09.26')
PAID27 = os.path.join(LOGS, '270926_Popravka_vozobravlenia_toplivopodachi.bin')
PAIDST = os.path.join(Y30, 'Бош797', 'Исходные калибровки', '01_j796sx_i_v2_21_01_0B_C2_7E_0E_00_00_2D.bin')
TUNED = os.path.join(Y30, 'Бош797', 'Исходные калибровки', '18_10_26_Otsechka_3.bin')
J7STOCK = os.path.join(HERE, 'j7es_v0.7.5.bin')
J7DESC = os.path.join(HERE, 'j7es_0.7.4.j7')
OUT = os.path.join(HERE, 'редактор калибровок j7es ИИ.html')
SIX = '6 цилиндров (наш патч)'
PAIDONLY = 'Только в платной'
SHIFT = 0x70000                     # родственная раскладка: адрес в платной = адрес j7es + 0x70000
NO_FLASH = {(5, 0): 'Ф4–Ф6, К4–К6 не работают', (5, 1): 'Ф4–Ф6, К4–К6 не работают, отсечка',
            (6, 0): 'калибровки стока ВАЗ', (6, 1): 'перенос по адресу с ошибками',
            (6, 2): 'флаги и маска ошибок не как в платной, нет ПЦН 32×16',
            (6, 3): 'датчик фаз включался своим байтом, штатный флаг выключен (исправлено в v7)',
            (7, 0): 'калибровки стока ВАЗ'}
SECTIONS = {
    'Rabochie_rezhimy': 'Рабочие режимы', 'Kholostoy_khod': 'Холостой ход', 'Pusk': 'Пуск',
    'Perekhod_Pusk': 'Переход от пуска', 'Perekhod_ot_KhKh_k_rabochim_rezhimam': 'Переход от ХХ к рабочим режимам',
    'Progrev': 'Прогрев', 'Otklyuchenie_toplivopodachi': 'Отключение топливоподачи',
    'Avariynye_rezhimy': 'Аварийные режимы', 'Datchiki_mekhanizmy_funktsii': 'Датчики, механизмы, функции',
    'Kontrol_detonatsii': 'Контроль детонации', 'Lyambda-regulirovanie': 'Лямбда-регулирование',
    'Registrator': 'Регистратор', 'BK': 'Бортовой компьютер',
}
# несколько таблиц платной на один адрес j7es (j7es выбирает флагом) — какую переносить:
# у пользователя активны ПЦН 32×32 и карты «от наполнения» (память y30-calibration-sets)
PREFER = {0x9294: 'Поправка ЦН 32х32 по давлению', 0x6AC8: 'УОЗ от наполнения',
          0x83BA: 'Состав смеси от оборотов и наполнения'}
BITS_FOR = {0x9294: (0x5F02, 4)}                 # флаг, который нужен перенесённой таблице
# флаги j7es по скриншотам флагов платной (Исходные калибровки/Флаги платной — скриншоты программы 20.10.26/,
# разбор там же): (адрес, бит, 1/0, название, как в программе платной). Байты 1–2 «Флагов конфигурации» платной
# совпадают с 6051/6052 бит в бит; с 5-го байта раскладка у платной своя — по названиям.
FLAGS = [(0x6051, 0, 0, 'Датчик концентрации кислорода', 'в платной 0 (бит 0 байта)'),
         (0x6051, 1, 0, 'Адсорбер', 'в платной 0 (бит 1 байта)'),
         (0x6051, 2, 0, 'Соленоид наддува', 'в платной 0 (бит 2 байта)'),
         (0x6051, 3, 0, 'Датчик детонации', 'в платной ☐'),
         (0x6051, 4, 1, 'Датчик температуры воздуха', 'в платной ☑'),
         (0x6051, 5, 1, 'Датчик фаз', 'в платной ☑ (с v7 включает механизм фазы 6 цилиндров)'),
         (0x6051, 6, 0, 'Признак постоянного включения топлива', 'в платной ☐'),
         (0x6052, 1, 1, 'Адаптация нуля дросселя', 'в платной ☑'),
         (0x6052, 2, 0, 'Асинхронная топливоподача при повторном пуске', 'в платной ☐'),
         (0x6052, 3, 1, 'Постоянное хранение ошибок', 'в платной ☑'),
         (0x6052, 4, 0, 'Датчик скорости автомобиля', 'в платной ☐'),
         (0x6052, 6, 1, 'Асинхронное обогащение при ускорении', 'в платной ☑'),
         (0x6052, 7, 1, 'Пуск в фазированном режиме', 'в платной ☑'),
         (0x5F00, 1, 0, 'Попарно-параллельный режим катушек', 'в платной ☐'),
         (0x5F00, 4, 0, 'ДАД подключен на пин 55', 'в платной расчёт по ДАД, ДАД на пине 37, не на 55'),
         (0x5F01, 0, 1, 'УОЗ, ALF и Фаза по Наполнению', 'в платной ● таблицы СС/УОЗ и фаза по наполнению'),
         (0x5F01, 1, 0, 'УОЗ, ALF и Фаза по давлению', 'в платной ○ по давлению'),
         (0x5F01, 4, 0, 'Не экстраполировать результат лямбда-регулятора', 'в платной ☐ отключить экстраполяцию'),
         (0x5F01, 5, 1, 'Таблица самообучения по давлению', 'в платной ● обучение по ДК — по давлению'),
         (0x5F01, 6, 1, 'Запрет адаптации положения РХХ по GB', 'в платной ☑'),
         (0x5F02, 0, 1, 'Работать без ДМРВ (ДАД или по дросселю)', 'в платной ● расчёт наполнения — ДАД'),
         (0x5F02, 1, 0, 'Рассчитывать наполнение по таблице БЦН (дроссельный режим)', 'в платной ○ дроссель'),
         (0x5F02, 2, 0, 'Барометрическая коррекция дроссельного режима', 'в платной ☐'),
         (0x5F02, 3, 1, 'Таблица поправки ЦН 32х16 по дросселю', 'в платной ☑'),
         (0x5F02, 4, 1, 'Таблица поправки ЦН 32х32 по давлению', 'в платной ☑'),
         (0x5F02, 5, 0, 'Таблица БЦН по давлению', 'в программе платной такого нет; база — «БЦН по дросселю»'),
         (0x5F03, 1, 0, 'Отключить БН', 'в платной ☐'),
         (0x5F03, 2, 0, 'Отключить форсунки', 'в платной ☐'),
         (0x9ED3, 1, 0, 'Функции доп. входов: подключен на 37pin', 'на пине 37 у тебя ДАД')]
NO_PAID_BIT = {(0x5F02, 5), (0x9ED3, 1)}                  # решения без галочки в платной
# статус битов в редакторе: 'pair' — как в платной; 'orange' — пара есть, ставится иначе; 'blue' — галочки нет
FLAG_STATUS = {(a, b): ('blue' if (a, b) in NO_PAID_BIT else 'pair', why, on) for a, b, on, _, why in FLAGS}
FLAG_STATUS[(0x5F00, 0)] = ('blue', 'при 6 цилиндрах выход моментного РХХ отключён: пара COMSET/COMCLR занята '
                                    'катушками К5/К6, ключи DA11/DA12 — форсунками 5/6', None)
FLAG_UNKNOWN = 'в программе платной такой галочки нет — как в j7es'
COPY_SAME = {0x8B00: 0x9194}       # «Время накопления» → «… для попарно-параллельного режима»
# «Маска ошибок» платной: байты 1–8 = j7es бит в бит (сверено со скриншотами по кодам ошибок)
MASK_BYTES = [0x60DA, 0x60DB, 0x60DC, 0x60DD, 0x5FAD, 0x5FB0, 0x5FB1, 0x5FB2]
SIX_ANALOGS = {'Зуб опроса ДФ', 'Зуб ВМТ 1 цилиндра относительно пропуска', 'Форсунки - фазированный режим',
               'Форсунки - ПП режим', 'Катушки - фазированный режим', 'Катушки - ПП режим'}
# название в платной → название в j7es (одна таблица, разные код и название)
ALIAS = {'Состав смеси от наполнения': 'Состав смеси от оборотов и наполнения'}
# пары, найденные разбором синих 20.10.26 (название j7es → название платной): размер, раздел и значения сходятся
PAIRS = {'Индекс по скорости/оборотам': 'Определитель номера передачи',
         'Коррекция порога детонации': 'Коррекция общего порога детонации',
         'Флаги комплектации': 'Флаги конфигурации'}           # флаги — только показ: раскладка битов у платной другая
# коды совпали случайно, смысл разный (проверено по названиям и значениям 20.10.26) — не пара
REJECT = {0x5F97: 'в платной этот код — «Максимальный коэфф. для расчета ТЗ»',
          0x5F98: 'в платной этот код — «Максимальный МРВ для расчета Тз»',
          0x60A9: 'в платной этот код — «Минимальный коэфф. для расчета ТЗ»',
          0x6291: 'в платной этот код — «Коэффициент фильтра»',
          0x5EF8: 'в платной этот код — «Порог ТВ»',
          0x60E0: 'в платной этот код — «Порог высоких оборотов»',
          0x63AC: 'в платной этот код — «Коррекция аварийного ЦН»; в j7es это множитель топлива по ТОЖ'}
# пары по адресу j7es (название в j7es повторяется): адрес → (название платной, вид в платной)
PAIRS_ADDR = {0x5F63: ('Число импульсов на 1 метр пути', 'const')}       # 180 / 30 = 6 имп/м — те же единицы
# пара по смыслу есть, но сама не переносится: адрес j7es → (название платной, почему; None — разное устройство)
STRUCT = {0x9E5C: ('Желаемое положение РХХ', None),
          0x6713: ('Коэффициент весовой коррекции по ТОЖ', None),
          0x9074: ('Коэффициент уменьшения GTC 1 при выходе из ХХ', None),
          0x6913: ('Шаг уменьшения уставки оборотов 1', None),
          0x6933: ('Шаг уменьшения уставки оборотов 2', None),
          0x5F16: ('Отскок УОЗ в режиме Launch', None),
          0x623C: ('Базовый duty (WGDC)', None),
          0x5FA3: ('Минимальное положение РХХ', 'в j7es одно число, в платной таблица'),
          0x6054: ('Зона нечувствительности по дросселю', 'в j7es одно число (обогащение по открытию), в платной '
                   'таблица на 6 точек; константа платной = 2 — это обеднение по закрытию (5F74, перенесена)'),
          0x8A0C: ('Коэффициент фильтра', 'в платной все значения 0 — перенос остановит регулятор')}
STRUCT_PAID = {n for n, _ in STRUCT.values()}
# одноимённые в платной, но у другого узла — не пара (остаются синими с пояснением)
NOT_PAIR = {0x9ECF: 'в платной «Задержка включения вентилятора» — у её собственного вентилятора, не у доп. выхода j7es',
            0x71C6: 'в платной «Задержка включения вентилятора» — у её собственного вентилятора, не у кондиционера j7es',
            0x71C7: 'в платной «Смещение РХХ при включения вентилятора» — у её собственного вентилятора',
            0x6090: 'в платной два «Режима управления» у других узлов'}
# константа j7es ← таблица платной: в j7es одно число, в платной таблица по ТОЖ — берётся максимум
DERIVED = {'Обороты блокировки впрыска': 'Обороты блокировки впрыска по ТОЖ'}
PREFER[0x9BC7] = 'Коррекция порога детонации'
PREFER[0x7CF7] = 'Поправка ЦН 32х16 по дросселю'          # в платной ☑ «Таблица поправки ЦН 32х16 по дросселю»


def mod(name, fname):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def cte_all():
    """Код → описание калибровки платной из выгрузок .cte (значения — настройка 28.09)."""
    out = {}
    num = lambda s: float(s.replace(',', '.'))
    for f in sorted(glob.glob(os.path.join(LOGS, '*.cte'))):
        sect = SECTIONS.get(os.path.basename(f)[:-4], os.path.basename(f)[:-4])
        t = open(f, encoding='cp1251').read().replace('\r', '')
        for m in re.finditer(r'\[([0-9A-Fa-f]{8})\]\nName=(.*)\n((?:[^\[\n].*\n?)*)', t):
            kv = re.findall(r'^(\w+)=(.*)$', m.group(3), re.M)
            if not kv:
                continue
            e = dict(name=m.group(2).strip(), sect=sect)
            if kv[0][0] == 'Const':
                e.update(kind='const', text=kv[0][1].strip())
                try:
                    e['v'] = num(kv[0][1])
                except ValueError:
                    pass
            elif re.match(r'F\d+$', kv[0][0]):
                e.update(kind='flags', text=' '.join(v.strip() for _, v in kv))
            elif any('Z' in k for k, _ in kv):
                dct = {}
                for k, v in kv:
                    x, z = map(int, re.match(r'X(\d+)Z(\d+)', k).groups())
                    dct[(x, z)] = num(v)
                nx = max(x for x, _ in dct)
                nz = max(z for _, z in dct)
                e.update(kind='table', nx=nx, nz=nz,
                         var=[[dct[(x, z)] for z in range(1, nz + 1) for x in range(1, nx + 1)],
                              [dct[(x, z)] for x in range(1, nx + 1) for z in range(1, nz + 1)]])
            else:
                e.update(kind='table', nx=len(kv), nz=1, var=[[num(v) for _, v in kv]])
            out[int(m.group(1), 16)] = e
    return out


def overlay_patches(cte):
    """Поверх выгрузки 28.09 — наши файлы правок, залитые позже (Логи 29.09 / 02.10 / 03.10, «y30_…cte»)."""
    files = sorted(glob.glob(os.path.join(Y30, 'Логи *', 'y30_*.cte')), key=os.path.getmtime)
    byname = {}
    for code, e in cte.items():
        byname.setdefault(e['name'], []).append(code)
    num = lambda s: float(s.replace(',', '.'))
    for f in files:
        t = open(f, encoding='cp1251').read().replace('\r', '')
        for m in re.finditer(r'\[([0-9A-Fa-f]{8})\]\nName=(.*)\n((?:[^\[\n].*\n?)*)', t):
            code = int(m.group(1), 16)
            kv = re.findall(r'^(\w+)=(.*)$', m.group(3), re.M)
            e = cte.get(code)
            if not e or not kv:
                continue
            if e['kind'] == 'const' and kv[0][0] == 'Const':
                e['text'] = kv[0][1].strip()
                e['v'] = num(kv[0][1])
                e['patched'] = os.path.basename(f)
    return files


def find(buf, base, v):
    """(адрес, ширина, знак, a, b): значение = байт·a + b."""
    v = np.array(v, dtype=float)
    n = len(v)
    i0, i1 = int(v.argmin()), int(v.argmax())
    span = v[i1] - v[i0]
    if span == 0:
        return []
    tol = max(abs(v).max(), span) * 2e-4 + 1e-6
    b = np.frombuffer(buf, dtype=np.uint8)
    hits = []
    views = [(b.astype(float), 1, 0, 'u'), (b.view(np.int8).astype(float), 1, 0, 's')]
    for off in (0, 1):
        bb = b[off:off + (len(b) - off) // 2 * 2]
        views += [(bb.view('<u2').astype(float), 2, off, 'u'), (bb.view('<i2').astype(float), 2, off, 's')]
    for arr, w, off, sg in views:
        if len(arr) < n:
            continue
        W = swv(arr, n)
        dd = W[:, i1] - W[:, i0]
        ok = dd != 0
        a = np.where(ok, span / np.where(ok, dd, 1), 0)
        err = np.abs(a[:, None] * (W - W[:, i0][:, None]) + v[i0] - v).max(axis=1)
        for k in np.nonzero(ok & (err < tol))[0]:
            aa = float(a[k])
            hits.append((base + off + int(k) * w, w, sg, aa, float(v[i0] - aa * W[k, i0])))
    return hits


def norm(s):
    return re.sub(r'[^0-9a-zа-яё]', '', s.lower().replace('h', 'н'))


def similar(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def generic(code):
    return ((code >> 16) & 0xFF) == 0x00 and ((code >> 8) & 0xFF) == 0xFF


KIND = {1: 'table', 2: 'table', 3: 'const', 4: 'flags'}


def match(cal, cte):
    """Индекс калибровки j7es → код калибровки платной."""
    res = {}
    for i, c in enumerate(cal):
        e = cte.get(c['code'])
        if not e or e['kind'] != KIND[c['kind']] or c['addr'] in REJECT:
            continue
        if generic(c['code']) and similar(e['name'], c['name']) < 0.55:
            continue
        if e['kind'] == 'table' and e['nx'] * e['nz'] != c['n']:
            continue
        res[i] = c['code']
    used = set(res.values())
    byname = {}
    for code, e in cte.items():
        byname.setdefault(e['name'], []).append(code)
    for i, c in enumerate(cal):
        pa = PAIRS_ADDR.get(c['addr'])
        if i in res or not pa:
            continue
        codes = [k for k in byname.get(pa[0], []) if cte[k]['kind'] == pa[1] and k not in used]
        if len(codes) == 1 and pa[1] == KIND[c['kind']]:
            res[i] = codes[0]
            used.add(codes[0])
    for i, c in enumerate(cal):
        pn = PAIRS.get(c['name'])
        if i in res or not pn or len(byname.get(pn, [])) != 1:
            continue
        code = byname[pn][0]
        e = cte[code]
        if e['kind'] == KIND[c['kind']] and (e['kind'] != 'table' or e['nx'] * e['nz'] == c['n']):
            res[i] = code
            used.add(code)
    pname = {}
    for code, e in cte.items():
        pname.setdefault(norm(ALIAS.get(e['name'], e['name'])), []).append(code)
    jname = {}
    for i, c in enumerate(cal):
        jname.setdefault(norm(c['name']), []).append(i)
    for i, c in enumerate(cal):
        if i in res:
            continue
        ps, js = pname.get(norm(c['name']), []), jname.get(norm(c['name']), [])
        if len(ps) == 1 and len(js) == 1 and ps[0] not in used:
            e = cte[ps[0]]
            if e['kind'] == KIND[c['kind']] and (e['kind'] != 'table' or e['nx'] * e['nz'] == c['n']):
                res[i] = ps[0]
                used.add(ps[0])
    return res


def paid_table(e, p27, ptu, c=None):
    """Значения таблицы платной (z снаружи, x внутри): из прошивки 18.10 по найденному адресу или из выгрузки 28.09.
    c — пара в j7es: если поиск не нашёл (одинаковые значения), проверяется адрес j7es + 0x70000 — там у
    родственных калибровок та же раскладка и тот же масштаб (у 189 из 226 констант так и есть)."""
    hits = []
    for oi, v in enumerate(e['var']):
        hits += [h + (oi,) for h in find(p27[0x75000:0x7C000], 0x75000, v)]
    if len({h[0] for h in hits}) == 1:
        a, w, sg, k, b, order = hits[0]
        n = e['nx'] * e['nz']
        dt = {('u', 1): np.uint8, ('s', 1): np.int8, ('u', 2): '<u2', ('s', 2): '<i2'}[(sg, w)]
        raw = np.frombuffer(ptu[a:a + n * w], dtype=dt).astype(float) * k + b
        if order == 1:                                   # в бине x снаружи → переставить
            raw = raw.reshape(e['nx'], e['nz']).T.reshape(-1)
        return dict(v=[round(float(x), 6) for x in raw], src='18.10', pa=a)
    if c is not None:                                    # не нашлась поиском — адрес родственной раскладки
        enc = encode(c, e['var'][0])
        pa = c['addr'] + SHIFT
        if enc is not None and p27[pa:pa + len(enc)] == enc:
            return dict(v=[round(float(x), 6) for x in j7val(ptu[SHIFT:], c)], src='18.10', pa=pa)
    return dict(v=e['var'][0], src='28.09', pa=None)


def dec(c, raw):
    """Сырое → значение по описанию .j7 (прямая или обратная шкала, два смещения)."""
    raw = np.asarray(raw, float) - c['off']
    if c.get('inv'):
        with np.errstate(divide='ignore'):
            v = np.where(raw != 0, c['inv'] * c['mul'] / (c['div'] * np.where(raw != 0, raw, 1)), np.inf)
    else:
        v = raw * c['mul'] / c['div']
    return v - c.get('off2', 0.0)


def enc_raw(c, vals):
    v = np.asarray(vals, float) + c.get('off2', 0.0)
    if c.get('inv'):
        return c['inv'] * c['mul'] / (c['div'] * v) + c['off']
    return v * c['div'] / c['mul'] + c['off']


def j7val(buf, c):
    f = {0: 'B', 1: 'b', 2: 'H', 3: 'h'}[c['ty']]
    raw = np.array(struct.unpack('<%d%s' % (c['n'], f), buf[c['addr']:c['addr'] + c['n'] * c['w']]), float)
    return dec(c, raw)


def encode(c, vals):
    """Значения → байты j7es; None, если не ложатся в тип/шаг (другие единицы)."""
    lo, hi = {0: (0, 255), 1: (-128, 127), 2: (0, 65535), 3: (-32768, 32767)}[c['ty']]
    vals = np.array(vals, float)
    if c.get('inv') and (vals + c.get('off2', 0.0) == 0).any():
        return None
    raw = np.round(enc_raw(c, vals))
    if raw.min() < lo or raw.max() > hi:
        return None
    back = dec(c, raw)
    st = np.abs(dec(c, raw + 1) - back)                   # шаг в этой точке (у обратной шкалы разный)
    if (np.abs(back - vals) > st * 0.51 + 1e-9).any():
        return None
    f = {0: 'B', 1: 'b', 2: 'H', 3: 'h'}[c['ty']]
    return struct.pack('<%d%s' % (len(raw), f), *[int(x) for x in raw])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', default='', help='записать список переноса таблиц из платной (.tsv)')
    args = ap.parse_args()
    j7 = mod('j7', 'описание j7es (.j7) — разбор 20.10.26 ИИ.py')
    cal = j7.load(J7DESC)
    cte = cte_all()
    for e in cte.values():
        if 'v' in e:
            e['v0'] = e['v']                         # значение выгрузки 28.09 (= состояние бина 27.09)
    overlay_patches(cte)
    jes, p27, pst, ptu = (open(p, 'rb').read() for p in (J7STOCK, PAID27, PAIDST, TUNED))
    m = match(cal, cte)
    cmin = {c['addr']: c['div'] for c in cal if c['kind'] == 3}          # делители минимумов осей
    same_addr = {}
    for c in cal:
        if c['kind'] in (1, 2):
            same_addr.setdefault(c['addr'], []).append(c['name'])
    defs, transfer, report = [], [], []
    for i, c in enumerate(cal):
        dd = dict(name=c['name'], sect=c['path'], kind=c['kind'], addr=c['addr'])
        if c['kind'] in (1, 2, 3):
            dd.update(ty=c['ty'], w=c['w'], div=c['div'], mul=c['mul'], off=c['off'], nx=c['nx'], nz=c['nz'],
                      off2=c['off2'], inv=c['inv'])
        if c['kind'] in (1, 2):
            for k in ('xax', 'zax'):
                ax = c.get(k)
                if ax and ax['kind'] == 'mm':
                    ax = dict(ax, dmin=cmin.get(ax['min'], 1.0))
                dd[k] = ax
            dd.update(xl=c.get('xl', ''), zl=c.get('zl', ''), vl=c.get('vl', ''))
            others = [n for n in same_addr[c['addr']] if n != c['name']]
            if others:
                dd['note'] = 'та же память, что у «%s» — какую читает блок, решают флаги' % '», «'.join(others)
        if c['kind'] == 3:
            dd['unit'] = c.get('unit', '')
        if c['kind'] == 4:
            # бит: [адрес, бит, название, статус, как в платной, нужное значение (None — не задано)]
            mask = c['name'] == 'Маска ошибок'
            pm = []
            if mask:
                e = next((x for x in cte.values() if x['name'] == 'Маска ошибок' and x['kind'] == 'flags'), None)
                pm = [int(x, 16) for x in e['text'].split()] if e else []
            bl = []
            for a, b, nm in c['bits']:
                if mask and a in MASK_BYTES and MASK_BYTES.index(a) < len(pm):
                    on = pm[MASK_BYTES.index(a)] >> b & 1
                    bl.append([a, b, nm, 'pair', 'в платной ' + ('☑' if on else '☐'), on])
                else:
                    st = FLAG_STATUS.get((a, b), ('blue', FLAG_UNKNOWN, None))
                    bl.append([a, b, nm, st[0], st[1], st[2]])
            dd['bits'] = bl
        code = m.get(i)
        src = DERIVED.get(c['name']) if c['kind'] == 3 else None
        srcs = [e for e in cte.values() if e['name'] == src and e['kind'] == 'table'] if src else []
        if code is None and len(srcs) == 1:
            pt = paid_table(srcs[0], p27, ptu)
            v = max(pt['v'])
            enc = encode(c, [v])
            dd['paid'] = dict(name=src, text='таблица по ТОЖ %g…%g, в j7es берётся максимум %g' % (min(pt['v']), v, v),
                              src=pt['src'], why='' if enc else 'значение не ложится в тип j7es')
            if enc and c['addr'] not in {t[0] for t in transfer}:
                transfer.append((c['addr'], enc, c['name'], src + ' (максимум)', pt['src']))
            if enc:
                dd['pb'] = enc.hex()
        elif code is None and c['addr'] in STRUCT and c['kind'] in (1, 2, 3):
            pn, why = STRUCT[c['addr']]
            pe = [e for e in cte.values() if e['name'] == pn and e['kind'] == 'table']
            if why is None:
                why = 'разное устройство: в j7es %d точек, в платной %s — нужен разрез по осям' % (
                    c['n'], '%d×%d' % (pe[0]['nx'], pe[0]['nz']) if pe else '?')
            dd['orange'] = True
            dd['paid'] = dict(name=pn, why=why)
        elif code is None:
            dd['blue'] = True
            if c['addr'] in NOT_PAIR or c['addr'] in REJECT:
                dd['note'] = NOT_PAIR.get(c['addr']) or REJECT[c['addr']] + ' — не пара'
        else:
            e = cte[code]
            p = dict(name=e['name'])
            if e['kind'] == 'table':
                pt = paid_table(e, p27, ptu, c)
                p.update(v=pt['v'], src=pt['src'])
                vals = pt['v']
                enc = encode(c, vals)
                js = j7val(jes, c)
                ps = paid_table(dict(e), p27, pst, c)['v'] if pt['pa'] else None
                why = ''
                if enc is None:
                    why = 'значения не ложатся в тип/шаг j7es — другие единицы'
                elif ps is not None:
                    sj, sp = float(js.max() - js.min()), float(max(ps) - min(ps))
                    if sj > 0 and sp > 0 and not 0.2 < sj / sp < 5:
                        why = 'разброс стока j7es и платной отличается в %.0f раз — проверить единицы' % (sj / sp if sj > sp else sp / sj)
                p['why'] = why
                if why:
                    dd['orange'] = True
                report.append((c['addr'], c['name'], e['name'], pt['src'], why))
                if not why:
                    transfer.append((c['addr'], enc, c['name'], e['name'], pt['src']))
                    dd['pb'] = enc.hex()
            elif e['kind'] == 'const' and 'v' in e:
                # константа: по адресу j7es + 0x70000 в бине 27.09 то же сырое, что даёт выгрузка → читаем 18.10 там же;
                # иначе (платная переложила) — значение выгрузки 28.09 с нашими правками поверх
                pa, w = c['addr'] + SHIFT, c['w']
                e28 = encode(c, [e['v0']])
                if e28 is not None and p27[pa:pa + w] == e28:
                    enc, src = bytes(ptu[pa:pa + w]), '18.10'
                else:
                    enc, src = encode(c, [e['v']]), '28.09' + (' + ' + e['patched'][:18] if e.get('patched') else '')
                why = ''
                if enc is None:
                    why = 'значение %s не ложится в тип j7es — другие единицы' % e.get('text', '')
                else:
                    pv = float(j7val(enc.rjust(c['addr'] + w, b'\0'), c)[0])
                    js = float(j7val(jes, c)[0])
                    if js and pv and not 0.05 < abs(pv / js) < 20:
                        why = 'в %.0f раз отличается от стока j7es — проверить единицы' % max(abs(pv / js), abs(js / pv))
                    p['text'] = ('%.6g' % pv) + (' (было в выгрузке %s)' % e.get('text', '') if src == '18.10' and
                                                 abs(pv - e['v0']) > 1e-6 * max(1, abs(pv)) else '')
                p.update(src=src, why=why)
                if why:
                    dd['orange'] = True
                    p['text'] = e.get('text', '')
                report.append((c['addr'], c['name'], e['name'], src, why))
                if not why and c['addr'] not in {t[0] for t in transfer}:
                    transfer.append((c['addr'], enc, c['name'], e['name'], src))
                    dd['pb'] = enc.hex()
            elif e['kind'] == 'flags':                       # байты флагов платной — разбивкой, без названий битов
                vals = [int(x, 16) for x in e.get('text', '').split()]
                while vals and not vals[-1]:
                    vals.pop()
                p['bytes'] = vals
                if c['name'] == 'Маска ошибок':               # байты 1–8 переносятся как есть
                    for a, v in zip(MASK_BYTES, vals + [0] * 8):
                        transfer.append((a, bytes([v]), 'Маска ошибок, байт %04X' % a, 'Маска ошибок', '28.09'))
            else:
                p['text'] = e.get('text', '')
            dd['paid'] = p
        defs.append(dd)
    # вторая таблица накопления (5F00.1 «Попарно-параллельный режим катушек») = основная из платной: чтобы при
    # включении флага катушки не заряжались по стоку ВАЗ
    for src, dst in COPY_SAME.items():
        cs = next((c for c in cal if c['addr'] == src and c['kind'] in (1, 2)), None)
        cd = next((c for c in cal if c['addr'] == dst and c['kind'] in (1, 2)), None)
        enc = next((t[1] for t in transfer if t[0] == src), None)
        if cs and cd and enc and all(cs[k] == cd[k] for k in ('ty', 'div', 'mul', 'off', 'n')):
            transfer.append((dst, enc, cd['name'], cs['name'] + ' (копия)', 'как ' + '%04X' % src))
            for dd in defs:
                if dd.get('addr') == dst and dd['kind'] in (1, 2):
                    dd.pop('blue', None)
                    dd['pb'] = enc.hex()
                    dd['paid'] = dict(name='= «%s» (своя таблица в платной одна)' % cs['name'])
    # несколько вариантов на одном адресе (выбор флагом): сравнивать с платной только тот, что переносится
    byaddr = {}
    for dd in defs:
        if dd.get('pb'):
            byaddr.setdefault(dd['addr'], []).append(dd)
    for a, ds in byaddr.items():
        if len(ds) > 1:
            for dd in ds:
                if dd['name'] != PREFER.get(a):
                    dd.pop('pb')
                    dd['note'] = (dd.get('note', '') + '; ' if dd.get('note') else '') + \
                        'блок читает на этом адресе «%s» — эта не используется' % PREFER.get(a, '?')
    # только в платной
    usedc = set(m.values())
    for code, e in cte.items():
        if code in usedc or e['name'] in SIX_ANALOGS:           # аналоги есть в нашем патче 6 цилиндров
            continue
        dd = dict(name=e['name'], sect=PAIDONLY + ' › ' + e['sect'], kind='paid', red=True, addr=0)
        if e['name'] in STRUCT_PAID and e['kind'] == 'table':                # пара в j7es есть, сама не переносится
            dd.update(red=False, orange=True, note='пара в j7es есть, но сама не переносится — см. её в дереве j7es')
        if e['kind'] == 'table':
            pt = paid_table(e, p27, ptu)
            dd.update(pk=1, nx=e['nx'], nz=e['nz'], v=pt['v'], src=pt['src'])
        else:
            dd.update(pk=0, text=e.get('text', ''), src='28.09')
        defs.append(dd)
    defs += six_defs(cte)
    # бины
    def ver(p):
        mm = re.match(r'j7es_v(\d+)\.(\d+)_', os.path.basename(p))
        return (int(mm.group(1)), int(mm.group(2))) if mm else (0, 0)
    vb = sorted((p for p in glob.glob(os.path.join(HERE, 'j7es_v*_*ИИ.bin')) if ver(p) >= (5, 0)), key=ver)
    bins = {'Сток j7es 0.7.5': J7STOCK}
    for p in vb:                                          # все сборки; последняя — по умолчанию
        nm = os.path.basename(p)[:-4]
        if p != vb[-1] and NO_FLASH.get(ver(p)):
            nm += ' — НЕ ШИТЬ: ' + NO_FLASH[ver(p)]
        bins[nm] = p
    emb = {k: base64.b64encode(open(p, 'rb').read()).decode() for k, p in bins.items()}
    html = TEMPLATE.replace('/*DEFS*/', json.dumps(defs, ensure_ascii=False)).replace('/*BINS*/', json.dumps(emb))
    open(OUT, 'w', encoding='utf-8').write(html)
    nb = sum(1 for d in defs if d.get('blue'))
    nr = sum(1 for d in defs if d.get('red'))
    print('калибровок j7es: %d (без пары в платной: %d), только в платной: %d, бин: %s' % (len(cal), nb, nr, list(bins)[-1]))
    if args.list:
        write_list(args.list, transfer, report)


def write_list(path, transfer, report):
    """Список переноса: таблицы, сопоставленные по коду / названию, байты уже в масштабе j7es."""
    by = {}
    for a, enc, nm, pn, src in transfer:
        by.setdefault(a, []).append((enc, nm, pn, src))
    lines = ['# Перенос из платной j796 в j7es (таблицы и константы) — сопоставление по коду/названию из описания '
             'j7es (.j7), значения из прошивки 18.10 (где адрес найден) или из выгрузки 28.09 с правками, '
             'пересчитаны в масштаб j7es.',
             '# адрес_j7es<TAB>hex:байты<TAB>название j7es ← название платной (откуда значения)',
             '# адрес_j7es<TAB>битN<TAB>название — включить бит N (флаг j7es)']
    for a in sorted(by):
        rows = by[a]
        if len(rows) > 1:
            pick = [r for r in rows if r[1] == PREFER.get(a)]
            if not pick:
                lines.append('# %04X — несколько таблиц платной на один адрес, не выбрано: %s' % (
                    a, ', '.join('«%s»' % r[2] for r in rows)))
                continue
            for r in rows:
                if r is not pick[0]:
                    lines.append('# %04X «%s» — не переносится: блок читает на этом адресе «%s» (флаг)' % (
                        a, r[1], pick[0][1]))
            rows = pick
        enc, nm, pn, src = rows[0]
        lines.append('%04X\thex:%s\t%s ← «%s» (%s)' % (a, enc.hex(), nm, pn, src))
    lines.append('# --- флаги j7es по настройке пользователя ---')
    for fa, fb, on, nm, why in FLAGS:
        lines.append('%04X\tбит%d%s\t%s — %s' % (fa, fb, '' if on else '=0', nm, why))
    lines.append('# --- не переносятся (единицы) ---')
    for a, nm, pn, src, why in report:
        if why:
            lines.append('# %04X «%s» ← «%s»: %s' % (a, nm, pn, why))
    open(path, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('список переноса: %d строк → %s' % (sum(1 for l in lines if not l.startswith('#')), path))


def six_defs(cte):
    """Калибровка нашего патча 6 цилиндров (E7EF–E7FF); режим E7F0 не показываем — при сохранении пишется 07."""
    cv = {e['name']: e.get('text', '') for e in cte.values()}
    def an(*names):
        return '; '.join('«%s» = %s' % (n, cv.get(n, '?')) for n in names)
    hl = [[1, 'высокий'], [0, 'низкий']]
    base = dict(sect=SIX, kind='six', ty=0, w=1, div=1.0, mul=1.0, off=0.0, nx=1, nz=1)
    six = [
        dict(name='Зуб опроса ДФ', addr=0xE7EF, sk='num', paid=dict(name='Зуб опроса ДФ', text=cv.get('Зуб опроса ДФ', '')),
             desc='Зуб коленвала, на котором снимается уровень датчика фаз (1..59; 0 — на первом зубе после '
                  'пропуска). Работает с прошивки v6. Номер считается от первого зуба после пропуска (он 0-й).'),
        dict(name='Уровень фазы на зубе 0', addr=0xE7F1, sk='choice', opts=hl, mask=1, analog=an('Зуб опроса ДФ'),
             desc='Уровень сигнала датчика фаз на зубе опроса, при котором после ближайшего пропуска идёт такт '
                  '1-го цилиндра. Неверный — искра на ВМТ выпуска; выставляется на машине по 1-му цилиндру. '
                  'При смене зуба опроса с 0 на другой уровень обычно меняется на противоположный: замер '
                  'берётся из предыдущего оборота.'),
        dict(name='Уровень сигнала зарядки К5/К6', addr=0xE7F2, sk='choice', opts=hl, mask=1, blue=True,
             desc='Каким уровнем ноги процессора 38 (К5) и 37 (К6) заряжают катушки. Должен совпадать '
                  'с уровнем зарядки К1–К4 на разъёме блока.'),
        dict(name='Форсунки: цилиндр → выход', addr=0xE7F3, sk='grid', multi=True, nx=6,
             cols=['Ф%d' % i for i in range(1, 7)], analog=an('Форсунки - фазированный режим', 'Форсунки - ПП режим'),
             desc='Строка — цилиндр по порядку работы, столбец — выход форсунки. В строке можно несколько отметок. '
                  'Попарный режим блок строит сам: цилиндры 1 и 4, 2 и 5, 3 и 6 вместе.'),
        dict(name='Катушки: цилиндр → выход', addr=0xE7F9, sk='grid', multi=False, nx=6,
             cols=['К%d' % i for i in range(1, 7)], analog=an('Катушки - фазированный режим', 'Катушки - ПП режим'),
             desc='Строка — цилиндр по порядку работы, столбец — выход катушки. В строке одна отметка.'),
        dict(name='Зуб ВМТ 1-го цилиндра по порядку работы (0..59)', addr=0xE7FF, sk='num',
             analog=an('Зуб ВМТ 1 цилиндра относительно пропуска'),
             desc='Номер зуба от первого после пропуска (он 0-й), на котором ВМТ 1-го цилиндра. '
                  'Совпадает ли счёт с платной — проверить стробоскопом (1 зуб = 6°).'),
    ]
    return [dict(base, **s) for s in six]


TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Калибровки j7es</title>
<style>
:root{--bg:#fafafa;--fg:#1d1d1f;--mut:#6b6b70;--line:#dcdce0;--pane:#fff;--sel:#e6efff;--acc:#2f6fe4;--chg:#d9480f;--red:#d0342c;--blue:#1f6fd1;--orange:#c26a00}
@media (prefers-color-scheme:dark){:root{--bg:#16171a;--fg:#e8e8ea;--mut:#9a9aa3;--line:#2c2e33;--pane:#1d1f23;--sel:#24324d;--acc:#6ea0ff;--chg:#ff8a50;--red:#ff6b6b;--blue:#6aa6ff;--orange:#ffab40}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:13px/1.35 -apple-system,Segoe UI,Roboto,sans-serif;height:100vh;display:flex;flex-direction:column}
header{display:flex;gap:8px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
header b{font-size:15px;margin-right:8px}select,button,input{font:inherit;color:inherit;background:var(--pane);border:1px solid var(--line);border-radius:6px;padding:4px 8px}
button{cursor:pointer}button.on{background:var(--acc);color:#fff;border-color:var(--acc)}
main{flex:1;display:flex;min-height:0}#tree{width:360px;min-width:220px;border-right:1px solid var(--line);overflow:auto;padding:6px}
#tree input[type=text]{width:100%;margin-bottom:6px}.sec{font-weight:600;margin:8px 0 2px;cursor:pointer;user-select:none}.sec .cnt{color:var(--mut);font-weight:400}
.it{padding:3px 6px 3px 14px;border-radius:5px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.it:hover{background:var(--sel)}.it.act{background:var(--sel)}
.it .dot{display:inline-block;width:6px;height:6px;border-radius:3px;background:var(--chg);margin-right:5px;vertical-align:middle}
.blue{color:var(--blue)}.red{color:var(--red)}.orange{color:var(--orange)}.legend{font-size:12px;color:var(--mut);margin:0 0 6px}
#view{flex:1;overflow:auto;padding:12px 16px}#meta{color:var(--mut);margin:2px 0 10px}h2{margin:0;font-size:16px}
table.g{border-collapse:collapse;font-variant-numeric:tabular-nums}table.g td,table.g th{border:1px solid var(--line);padding:2px 5px;text-align:right;min-width:42px}
table.g th{background:var(--pane);color:var(--mut);font-weight:500;position:sticky;top:0}table.g td.ch{outline:2px solid var(--chg);outline-offset:-2px}
table.g td input{width:56px;border:none;padding:0;background:transparent;text-align:right}table.g.six td{text-align:center}
#chart svg{background:var(--pane);border:1px solid var(--line);border-radius:6px}.tools{display:flex;gap:6px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
.hint{color:var(--mut);font-size:12px}.desc{margin:0 0 10px;max-width:760px}.flags label{display:block;padding:2px 0}.flags h3{font-size:13px;margin:10px 0 2px}
</style></head><body>
<header><b>Калибровки j7es</b>
<select id="binsel"></select><button id="open">Открыть бин…</button><input id="file" type="file" accept=".bin" hidden>
<button id="save">Сохранить бин</button><label class="hint"><input type="checkbox" id="cmp"> Сравнить со стоком j7es</label>
<span class="hint" id="stat"></span></header>
<main><div id="tree"><input id="q" type="text" placeholder="Поиск по названию">
<div class="legend"><span class="blue">синим</span> — нет в платной · <span class="red">красным</span> — нет в j7es (только просмотр) · <span class="orange">оранжевым</span> — пара есть, но сама не переносится</div><div id="list"></div></div>
<div id="view"><div class="hint">Выберите калибровку слева.</div></div></main>
<script>
const DEFS=/*DEFS*/;const BINS=/*BINS*/;
const b64=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const STOCK=b64(BINS['Сток j7es 0.7.5']);let cur=null,curName='',sel=null,mode='table',cmpOn=false,paidOn=false;
const hex4=a=>a.toString(16).toUpperCase().padStart(4,'0');
const binsel=document.getElementById('binsel');
for(const k of Object.keys(BINS)){const o=document.createElement('option');o.value=k;o.textContent=k;binsel.appendChild(o)}
binsel.value=Object.keys(BINS).slice(-1)[0];
function loadEmb(){cur=b64(BINS[binsel.value]).slice();curName=binsel.value+'.bin';refresh()}
binsel.onchange=loadEmb;
document.getElementById('cmp').onchange=e=>{cmpOn=e.target.checked;refresh()};
document.getElementById('open').onclick=()=>document.getElementById('file').click();
document.getElementById('file').onchange=e=>{const f=e.target.files[0];if(!f)return;f.arrayBuffer().then(b=>{const u=new Uint8Array(b);
 if(u.length!==65536){alert('Это не бин j7es: нужен файл 64 КБ.');return}cur=u;curName=f.name;refresh()})};
function hasPatch(d){for(let i=0xE800;i<0xE810;i++)if(d[i])return true;return false}
function rraw(d,a,ty){let v=ty>=2?d[a]|d[a+1]<<8:d[a];if(ty===1&&v>127)v-=256;if(ty===3&&v>32767)v-=65536;return v}
function wraw(d,a,ty,v){const w=ty>=2?2:1,s=ty===1||ty===3,lo=s?(w===1?-128:-32768):0,hi=s?(w===1?127:32767):(w===1?255:65535);
 v=Math.max(lo,Math.min(hi,Math.round(v)));if(v<0)v+=w===1?256:65536;d[a]=v&255;if(w===2)d[a+1]=v>>8}
// значение = (сырое − смещение)·множ/дел − смещение2; при обратной шкале — K·множ/(дел·(сырое − смещение)) − смещение2
function dec(t,r){r-=t.off;const v=t.inv?(r?t.inv*t.mul/(t.div*r):Infinity):r*t.mul/t.div;return v-(t.off2||0)}
function val(d,t,i){return dec(t,rraw(d,t.addr+i*t.w,t.ty))}
function put(t,i,v){v+=t.off2||0;if(t.inv&&!v){alert('При такой шкале ноль записать нельзя');return}
 wraw(cur,t.addr+i*t.w,t.ty,t.inv?t.inv*t.mul/(t.div*v)+t.off:v*t.div/t.mul+t.off)}
function stp(t){if(t.inv&&t.addr!==undefined&&cur){const r=rraw(cur,t.addr,t.ty);return Math.abs(dec(t,r+1)-dec(t,r))||0.001}return Math.abs(t.mul/t.div)}
function fmt(v,s){const dg=s>=1?0:s>=0.1?1:s>=0.01?2:s>=0.001?3:4;return (+v).toFixed(dg)}
function nbytes(t){if(t.kind===4){const s=new Set(t.bits.map(b=>b[0]));return [...s]}const a=[];if(t.kind==='paid'||!t.w)return a;
 for(let i=0;i<t.nx*t.nz*t.w;i++)a.push(t.addr+i);return a}
function changed(t){if(!cmpOn)return false;for(const a of nbytes(t))if(cur[a]!==STOCK[a])return true;return false}
// оси: по калибровкам текущего бина
function u16(d,a){return d[a]|d[a+1]<<8}
function axis(ax,n){if(!ax)return Array.from({length:n},(_,i)=>i+1);
 if(ax.kind==='lin')return Array.from({length:n},(_,i)=>+(ax.a+(ax.b-ax.a)*i/Math.max(1,n-1)).toFixed(2));
 const st=256/n;
 if(ax.kind==='mm'){const mn=u16(cur,ax.min)/ax.dmin,B=cur[ax.rng],pc=B?2048/(B*ax.dmin):0;return Array.from({length:n},(_,k)=>+(mn+k*st*pc).toFixed(1))}
 const out=[];for(let k=0;k<n;k++){const tg=k*st;let x=null;
  for(let i=0;i<ax.len;i++){const c=cur[ax.tab+i];if(c>tg||(c===tg&&tg>0)){if(i===0)x=0;else{const c0=cur[ax.tab+i-1];x=i-1+(c>c0?(tg-c0)/(c-c0):0)}break}}
  out.push(x===null?'>'+(ax.len-1)*ax.xstep:Math.round(x*ax.xstep))}return out}
// не совпадает с платной в открытом бине: байты переноса другие или флаг стоит иначе
function bitOn(a,b){return cur[a]>>b&1}
function mism(t){if(t.pb){for(let i=0;i<t.pb.length/2;i++)if(cur[t.addr+i]!==parseInt(t.pb.substr(2*i,2),16))return true;return false}
 if(t.kind===4)return t.bits.some(x=>x[5]!==null&&x[5]!==undefined&&bitOn(x[0],x[1])!==x[5]);return false}
function cls(t){return t.red?' red':(t.orange||mism(t))?' orange':t.blue?' blue':''}
function buildTree(){const q=document.getElementById('q').value.toLowerCase();const L=document.getElementById('list');L.innerHTML='';
 const by={},order=[];DEFS.forEach((t,i)=>{if(q&&!t.name.toLowerCase().includes(q))return;if(!by[t.sect]){by[t.sect]=[];order.push(t.sect)}by[t.sect].push(i)});
 for(const s of order){const h=document.createElement('div');h.className='sec';h.innerHTML=s+' <span class="cnt">'+by[s].length+'</span>';L.appendChild(h);
  const box=document.createElement('div');L.appendChild(box);h.onclick=()=>box.hidden=!box.hidden;
  for(const i of by[s]){const t=DEFS[i],e=document.createElement('div');e.className='it'+(i===sel?' act':'')+cls(t);e.title=t.name;
   e.innerHTML=(changed(t)?'<span class="dot"></span>':'')+t.name;e.onclick=()=>{sel=i;buildTree();show()};box.appendChild(e)}}}
document.getElementById('q').oninput=buildTree;
function refresh(){buildTree();if(sel!==null)show();let n=0;DEFS.forEach(t=>{if(changed(t))n++});document.getElementById('stat').textContent=curName+(cmpOn?' · отличается от стока j7es: '+n+' калибровок':'')}
function head(t,extra){let m=t.sect+(t.addr?' · адрес '+hex4(t.addr):'');
 if(t.kind===1||t.kind===2)m+=' · '+(t.nz>1?t.nx+'×'+t.nz:t.nx+' точек')+' · '+(t.ty>=2?16:8)+' бит'+(t.ty===1||t.ty===3?' со знаком':'');
 if(t.blue)m+=' · <span class="blue">нет в платной</span>';if(t.red)m+=' · <span class="red">нет в j7es</span>';if(t.orange)m+=' · <span class="orange">пара есть, сама не переносится</span>';
 if(!t.orange&&mism(t))m+=' · <span class="orange">в этом бине не как в платной</span>';
 if(t.paid)m+='<br>В платной: «'+t.paid.name+'»'+(t.paid.text!==undefined&&t.paid.text!==''?' = '+t.paid.text:'')+(t.paid.src?' (значение '+t.paid.src+')':(t.paid.text?' (выгрузка 28.09)':''))+(t.paid.why?' · <span class="orange">не переносится: '+t.paid.why+'</span>':'');
 if(t.analog)m+='<br>В платной (настройка 28.09): '+t.analog;if(t.note)m+='<br>'+t.note;
 return '<h2 class="'+cls(t)+'">'+t.name+'</h2><div id="meta">'+m+(extra||'')+'</div>'+(t.desc?'<p class="desc">'+t.desc+'</p>':'')}
function show(){const t=DEFS[sel],V=document.getElementById('view');
 if(t.kind==='six'){if(!hasPatch(cur)){V.innerHTML=head(t)+'<p class="desc red">В этом бине нет патча 6 цилиндров.</p>';return}return sixView(V,t)}
 if(t.kind==='paid')return paidView(V,t);
 if(t.kind===3)return constView(V,t);
 if(t.kind===4)return flagsView(V,t);
 const ax=axis(t.xax,t.nx),az=axis(t.zax,t.nz);
 V.innerHTML=head(t,(t.xl?'<br>X: '+t.xl:'')+(t.nz>1&&t.zl?' · Z: '+t.zl:'')+(t.vl?' · значение: '+t.vl:''))+
 '<div class="tools"><button id="mt" class="'+(mode==='table'?'on':'')+'">Таблица</button><button id="mc" class="'+(mode==='chart'?'on':'')+'">График</button>'+
 (t.paid&&t.paid.v?'<label class="hint"><input type="checkbox" id="pp"'+(paidOn?' checked':'')+'> Показать твою из платной</label>':'')+
 '<span class="hint">Двойной клик по клетке — правка.'+(cmpOn?' Рамкой — отличие от стока j7es.':'')+'</span></div><div id="body"></div>';
 document.getElementById('mt').onclick=()=>{mode='table';show()};document.getElementById('mc').onclick=()=>{mode='chart';show()};
 const pp=document.getElementById('pp');if(pp)pp.onchange=e=>{paidOn=e.target.checked;show()};
 const get=(paidOn&&t.paid&&t.paid.v)?(i=>t.paid.v[i]):(i=>val(cur,t,i));
 const B=document.getElementById('body');if(mode==='table'||t.nx*t.nz===1)tableView(B,t,ax,az,get,!(paidOn&&t.paid&&t.paid.v));else chartView(B,t,ax,az,get)}
function color(v,lo,hi){if(hi===lo)return '';const p=(v-lo)/(hi-lo);return 'background:hsla('+(240-240*p)+',70%,55%,.28)'}
function tableView(B,t,ax,az,get,edt){let lo=Infinity,hi=-Infinity;const n=t.nx*t.nz;for(let i=0;i<n;i++){const v=get(i);lo=Math.min(lo,v);hi=Math.max(hi,v)}
 const s=t.kind==='paid'?0.001:stp(t);
 let h='<table class="g"><tr><th>'+(t.nz>1?'Z \\ X':'X')+'</th>';
 const cell=i=>{let ch=false;if(cmpOn&&edt)for(let k=0;k<t.w;k++)if(cur[t.addr+i*t.w+k]!==STOCK[t.addr+i*t.w+k])ch=true;
  return '<td data-i="'+i+'" class="'+(ch?'ch':'')+'" style="'+color(get(i),lo,hi)+'"'+(cmpOn&&edt?' title="сток j7es: '+fmt(val(STOCK,t,i),s)+'"':'')+'>'+fmt(get(i),s)+'</td>'};
 if(t.nz>1){for(let x=0;x<t.nx;x++)h+='<th>'+ax[x]+'</th>';h+='</tr>';for(let z=t.nz-1;z>=0;z--){h+='<tr><th>'+az[z]+'</th>';for(let x=0;x<t.nx;x++)h+=cell(z*t.nx+x);h+='</tr>'}}
 else{h+='<th>значение</th></tr>';for(let x=0;x<t.nx;x++)h+='<tr><th>'+ax[x]+'</th>'+cell(x)+'</tr>'}
 B.innerHTML=h+'</table>';if(edt)B.querySelectorAll('td[data-i]').forEach(td=>td.ondblclick=()=>edit(td,t))}
function edit(td,t){const i=+td.dataset.i;const inp=document.createElement('input');inp.value=fmt(val(cur,t,i),stp(t));td.textContent='';td.appendChild(inp);inp.focus();inp.select();
 const done=ok=>{if(ok){const v=parseFloat(inp.value.trim().replace(',','.'));if(isNaN(v)){alert('Нужно число');show();return}put(t,i,v)}refresh()};
 inp.onkeydown=e=>{if(e.key==='Enter')done(true);if(e.key==='Escape')done(false)};inp.onblur=()=>done(true)}
function chartView(B,t,ax,az,get){const W=Math.min(1100,B.clientWidth-10)||900,H=420,P=46;let lo=Infinity,hi=-Infinity;const n=t.nx*t.nz;
 for(let i=0;i<n;i++){const v=get(i);lo=Math.min(lo,v);hi=Math.max(hi,v)}if(hi===lo){hi+=1;lo-=1}
 const X=i=>P+i*(W-P-12)/Math.max(1,t.nx-1),Y=v=>H-28-(v-lo)/(hi-lo)*(H-50),s=t.kind==='paid'?0.001:stp(t);
 let g='<svg width="'+W+'" height="'+H+'">';for(let k=0;k<=5;k++){const v=lo+(hi-lo)*k/5;g+='<line x1="'+P+'" x2="'+(W-10)+'" y1="'+Y(v)+'" y2="'+Y(v)+'" stroke="currentColor" opacity=".12"/><text x="4" y="'+(Y(v)+4)+'" font-size="11" fill="currentColor" opacity=".6">'+fmt(v,s)+'</text>'}
 for(let x=0;x<t.nx;x+=Math.ceil(t.nx/16))g+='<text x="'+X(x)+'" y="'+(H-8)+'" font-size="11" text-anchor="middle" fill="currentColor" opacity=".6">'+ax[x]+'</text>';
 for(let z=0;z<t.nz;z++){let d='';for(let x=0;x<t.nx;x++)d+=(x?'L':'M')+X(x).toFixed(1)+' '+Y(get(z*t.nx+x)).toFixed(1);
  g+='<path d="'+d+'" fill="none" stroke="hsl('+(t.nz>1?240-240*z/(t.nz-1):220)+',70%,50%)" stroke-width="1.6"><title>Z = '+az[z]+'</title></path>'}
 B.innerHTML='<div id="chart">'+g+'</svg></div><div class="hint">'+(t.nz>1?'Линия на каждое значение Z'+(t.zl?' ('+t.zl+')':'')+': синяя — нижнее, красная — верхнее.':'')+' По X: '+(t.xl||'номер точки')+'.</div>'}
function constView(V,t){const v=val(cur,t,0);V.innerHTML=head(t)+'<p><input id="cv" value="'+fmt(v,stp(t))+'" style="width:120px"> '+(t.unit||'')+
 (cmpOn?' <span class="hint">сток j7es: '+fmt(val(STOCK,t,0),stp(t))+'</span>':'')+'</p><p class="hint">Enter — записать. Шаг '+fmt(stp(t),stp(t)/10)+'.</p>';
 const inp=document.getElementById('cv');inp.onkeydown=e=>{if(e.key!=='Enter')return;const x=parseFloat(inp.value.replace(',','.'));if(isNaN(x)){alert('Нужно число');return}put(t,0,x);refresh()}}
function flagsView(V,t){const hx=v=>v.toString(16).toUpperCase().padStart(2,'0')+'h';let h=head(t);
 if(t.paid&&t.paid.bytes)h+='<p class="desc">Байты «'+t.paid.name+'» в платной (выгрузка 28.09, названий битов нет): '+
  t.paid.bytes.map((v,i)=>(i+1)+'-й = '+hx(v)).join(', ')+'.</p>';
 h+='<div class="flags">';let last=-1;
 t.bits.forEach(([a,b,nm,st,why,want],k)=>{if(a!==last){h+='<h3>Байт '+hex4(a)+' = '+hx(cur[a])+(cmpOn?' <span class="hint">(сток '+hx(STOCK[a])+')</span>':'')+'</h3>';last=a}
  const on=bitOn(a,b),known=want!==null&&want!==undefined,diff=known&&on!==want;
  const c=st==='blue'?'blue':(st==='orange'||diff)?'orange':'';
  let txt=why||'';if(known&&st!=='orange')txt+=' → нужно '+(want?'вкл':'выкл')+(diff?' · в этом бине '+(on?'вкл':'выкл'):' · совпадает');
  h+='<label class="'+c+'"><input type="checkbox" data-k="'+k+'"'+(on?' checked':'')+'> бит '+b+' — '+nm+
   (txt&&(t.paid||st!=='blue')?' <span class="hint">· '+txt+'</span>':'')+'</label>'});
 V.innerHTML=h+'</div>';V.querySelectorAll('input[data-k]').forEach(i=>i.onchange=()=>{const [a,b]=t.bits[+i.dataset.k];cur[a]=i.checked?cur[a]|1<<b:cur[a]&~(1<<b);refresh()})}
function paidView(V,t){if(!t.pk){V.innerHTML=head(t)+'<p>Значение в платной (настройка 28.09): <b>'+t.text+'</b></p>';return}
 V.innerHTML=head(t,'<br>Значения из платной ('+t.src+'), только просмотр')+'<div id="body"></div>';
 const B=document.getElementById('body'),f=i=>t.v[i];tableView(B,t,Array.from({length:t.nx},(_,i)=>i+1),Array.from({length:t.nz},(_,i)=>i+1),f,false)}
function sixView(V,t){let h=head(t);
 if(t.sk==='choice'){const v=cur[t.addr]&t.mask;h+='<select id="ch">'+t.opts.map(o=>'<option value="'+o[0]+'"'+(o[0]===v?' selected':'')+'>'+o[1]+'</option>').join('')+'</select>'}
 else if(t.sk==='num'){h+='<p><input id="cv" value="'+cur[t.addr]+'" style="width:80px"> <span class="hint">Enter — записать</span></p>'}
 else{h+='<table class="g six"><tr><th>цилиндр</th>'+t.cols.map(c=>'<th>'+c+'</th>').join('')+'</tr>';
  for(let r=0;r<6;r++){const v=cur[t.addr+r];let row='',any=false;
   for(let c=0;c<6;c++){const on=t.multi?(v>>c&1)===1:v===c;any=any||on;row+='<td><input type="'+(t.multi?'checkbox':'radio')+'" name="r'+r+'" data-r="'+r+'" data-c="'+c+'"'+(on?' checked':'')+'></td>'}
   h+='<tr><th'+(any?'':' class="red" title="у цилиндра нет выхода"')+'>'+(r+1)+'</th>'+row+'</tr>'}h+='</table>'}
 V.innerHTML=h;
 if(t.sk==='choice')document.getElementById('ch').onchange=e=>{cur[t.addr]=(cur[t.addr]&~t.mask)|+e.target.value;refresh()};
 else if(t.sk==='num'){const inp=document.getElementById('cv');inp.onkeydown=e=>{if(e.key!=='Enter')return;const x=parseInt(inp.value,10);if(isNaN(x)||x<0||x>59){alert('Нужно число 0…59');return}cur[t.addr]=x;refresh()}}
 else V.querySelectorAll('input[data-r]').forEach(i=>i.onchange=()=>{const a=t.addr+ +i.dataset.r,c=+i.dataset.c;if(t.multi)cur[a]=i.checked?cur[a]|1<<c:cur[a]&~(1<<c);else cur[a]=c;refresh()})}
function fixsum(d){d[0xFFF8]=d[0xFFF9]=0;let s0=0;for(let i=0;i<0xFFFE;i++)s0+=d[i];s0&=0xFFFF;let c=-1;
 for(let hi=0;hi<256;hi++){const cc=(255*hi-s0)&0xFFFF;if(cc<=510){c=cc;break}}if(c<0){alert('Не удалось подобрать контрольную сумму');return false}
 d[0xFFF8]=Math.min(c,255);d[0xFFF9]=c-Math.min(c,255);let s1=0;for(let i=0;i<0xFFFE;i++)s1+=d[i];
 for(let v=0;v<65536;v++)if(((s1+(v&255)+(v>>8))&0xFFFF)===v){d[0xFFFE]=v&255;d[0xFFFF]=v>>8;return true}alert('Не удалось подобрать контрольную сумму');return false}
document.getElementById('save').onclick=()=>{const d=cur.slice();if(!fixsum(d))return;const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([d],{type:'application/octet-stream'}));a.download=curName.replace(/\.bin$/,'')+' правка.bin';a.click()};
loadEmb();
</script></body></html>
'''

if __name__ == '__main__':
    main()
