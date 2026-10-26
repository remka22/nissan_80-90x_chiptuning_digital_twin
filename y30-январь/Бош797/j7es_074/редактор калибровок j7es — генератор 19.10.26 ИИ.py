#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собирает «редактор калибровок j7es ИИ.html» — просмотр и правка калибровок прошивки j7es (Январь 7.2).

Откуда берётся описание таблиц:
  - названия, разделы и размеры — из выгрузок .cte платной прошивки (Логи 28.09.26);
  - адрес, ширина и масштаб — таблица находится в платной (270926_…bin) поиском значений с точностью
    до масштаба, переносится в j7es со сдвигом −0x70000 и берётся, только если код j7es читает этот адрес
    (MOV DPTR,#) или байты стока j7es совпадают со стоком платной;
  - оси — из «Калибровки Января — дерево разделов 28.09.26 ИИ.txt» (посчитаны по квантованию платной).

Запуск (из папки j7es_074):
    python3 "редактор калибровок j7es — генератор 19.10.26 ИИ.py"
"""
import base64
import glob
import importlib.util
import json
import os
import re

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv

HERE = os.path.dirname(os.path.abspath(__file__))
Y30 = os.path.dirname(os.path.dirname(HERE))
LOGS = os.path.join(Y30, 'Логи 28.09.26')
TREE = os.path.join(LOGS, 'Калибровки Января — дерево разделов 28.09.26 ИИ.txt')
PAID27 = os.path.join(LOGS, '270926_Popravka_vozobravlenia_toplivopodachi.bin')
PAIDST = os.path.join(Y30, 'Бош797', 'Исходные калибровки', '01_j796sx_i_v2_21_01_0B_C2_7E_0E_00_00_2D.bin')
TUNED = os.path.join(Y30, 'Бош797', 'Исходные калибровки', '18_10_26_Otsechka_3.bin')
J7STOCK = os.path.join(HERE, 'j7es_v0.7.5.bin')
OUT = os.path.join(HERE, 'редактор калибровок j7es ИИ.html')
SHIFT = 0x70000
CAL_END = 0xA5B6                      # с A5B6 в j7es уже код
CONST = (0x5F62, 0x60FA)              # константы и флаги платной (не разобраны)
SIX = '6 цилиндров (наш патч)'
# адреса, где у j7es другая таблица, чем у платной (проверено кодом j7es 20.10.26); None — не показывать
J7_OTHER = {
    0x7AA7: dict(name='Предел оборотов по счётчику 4Ah', k=40.0, nx=32,
                 desc='Итоговый предел оборотов = меньшее из этой таблицы и предела 605C (код 4A08–4A31); '
                      'точка — счётчик 4Ah / 8.'),
    0xA358: None,      # линеаризация расхода (младшие байты, A358 + A458), а не «Добавка оборотов…»
    0x8FBF: None,      # читается только на остановке (2FCC → F890), смысл не разобран
}
RAW = 'Константы и флаги (не разобраны)'

SECTIONS = {
    'Rabochie_rezhimy': 'Рабочие режимы', 'Kholostoy_khod': 'Холостой ход', 'Pusk': 'Пуск',
    'Perekhod_Pusk': 'Переход от пуска', 'Perekhod_ot_KhKh_k_rabochim_rezhimam': 'Переход от ХХ к рабочим режимам',
    'Progrev': 'Прогрев', 'Otklyuchenie_toplivopodachi': 'Отключение топливоподачи',
    'Avariynye_rezhimy': 'Аварийные режимы', 'Datchiki_mekhanizmy_funktsii': 'Датчики, механизмы, функции',
    'Kontrol_detonatsii': 'Контроль детонации', 'Lyambda-regulirovanie': 'Лямбда-регулирование',
    'Registrator': 'Регистратор', 'BK': 'Бортовой компьютер',
}
AXIS_BY_LABEL = {
    'обороты, об/мин': 'RPM', 'дроссель, %': 'TPS', 'давление, кПа': 'PR', 'наполнение GBC': 'GBC',
    'ТОЖ, °C': 'TW', 'ТВ, °C': 'TA',
}
AXIS_NAME = {v: k for k, v in AXIS_BY_LABEL.items()}


def load_lab():
    spec = importlib.util.spec_from_file_location('lab', os.path.join(HERE, 'метки j7es для Ghidra 01.10.26 ИИ.py'))
    lab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lab)
    return lab


def cte_tables():
    """(код, имя, раздел, nx, nz, варианты порядка значений)."""
    out = []
    for f in sorted(glob.glob(os.path.join(LOGS, '*.cte'))):
        t = open(f, encoding='cp1251').read().replace('\r', '')
        for m in re.finditer(r'\[([0-9A-Fa-f]{8})\]\nName=(.*)\n((?:[^\[\n].*\n?)*)', t):
            kv = re.findall(r'^(\w+)=(.*)$', m.group(3), re.M)
            keys = [k for k, _ in kv]
            if not kv or 'Const' in keys or re.match(r'F\d+$', keys[0]):
                continue
            num = lambda s: float(s.replace(',', '.'))
            if any('Z' in k for k in keys):
                dct = {}
                for k, v in kv:
                    x, z = map(int, re.match(r'X(\d+)Z(\d+)', k).groups())
                    dct[(x, z)] = num(v)
                nx = max(x for x, _ in dct); nz = max(z for _, z in dct)
                var = [[dct[(x, z)] for z in range(1, nz + 1) for x in range(1, nx + 1)],
                       [dct[(x, z)] for x in range(1, nx + 1) for z in range(1, nz + 1)]]
            else:
                nx, nz = len(kv), 1
                var = [[num(v) for _, v in kv]]
            out.append((m.group(1).upper(), m.group(2).strip(), os.path.basename(f)[:-4], nx, nz, var))
    return out


def cte_values():
    """Имя → значение (строкой) для констант и флагов из выгрузок .cte (настройка пользователя в платной)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(LOGS, '*.cte'))):
        t = open(f, encoding='cp1251').read().replace('\r', '')
        for m in re.finditer(r'\[([0-9A-Fa-f]{8})\]\nName=(.*)\n((?:[^\[\n].*\n?)*)', t):
            kv = re.findall(r'^(\w+)=(.*)$', m.group(3), re.M)
            if kv and kv[0][0] == 'Const':
                out[m.group(2).strip()] = kv[0][1].strip()
            elif kv and re.match(r'F\d+$', kv[0][0]):
                out[m.group(2).strip()] = ' '.join('%X' % int(v, 16) for _, v in kv[:6])
    return out


def find(buf, base, v):
    """(адрес, ширина, знак, a, b): значение = байт·a + b."""
    v = np.array(v, dtype=float); n = len(v)
    i0, i1 = int(v.argmin()), int(v.argmax()); span = v[i1] - v[i0]
    if span == 0:
        return []
    tol = max(abs(v).max(), span) * 2e-4 + 1e-6
    b = np.frombuffer(buf, dtype=np.uint8); hits = []
    views = [(b.astype(float), 1, 0, 'u'), (b.view(np.int8).astype(float), 1, 0, 's')]
    for off in (0, 1):
        bb = b[off:off + (len(b) - off) // 2 * 2]
        views += [(bb.view('<u2').astype(float), 2, off, 'u'), (bb.view('<i2').astype(float), 2, off, 's')]
    for arr, w, off, sg in views:
        if len(arr) < n:
            continue
        W = swv(arr, n); d = W[:, i1] - W[:, i0]; ok = d != 0
        a = np.where(ok, span / np.where(ok, d, 1), 0)
        err = np.abs(a[:, None] * (W - W[:, i0][:, None]) + v[i0] - v).max(axis=1)
        for k in np.nonzero(ok & (err < tol))[0]:
            aa = float(a[k])
            hits.append((base + off + int(k) * w, w, sg, aa, float(v[i0] - aa * W[k, i0])))
    return hits


def tree_axes():
    """Оси из дерева разделов: значения осей и привязка осей к таблицам по имени."""
    t = open(TREE, encoding='utf-8').read()
    axes = {}
    for m in re.finditer(r'^ (RPM16|RPM32|TPS16|PR16|PR32|GBC16|TW39|TA39) .*\n((?:\s+[-\d. >]+\n)+)', t, re.M):
        vals = m.group(2).split()
        axes[m.group(1)] = vals
    bind = {}
    for m in re.finditer(r'^• (.+?)\s+\[(карта|таблица) ([^\]]*)\]\n(.*)', t, re.M):
        name, kind, info, nxt = m.group(1).strip(), m.group(2), m.group(3), m.group(4)
        if kind == 'таблица':
            mm = re.search(r'ось: ([^;]+);', info)
            bind[name] = {'x': AXIS_BY_LABEL.get(mm.group(1).strip()) if mm else None, 'z': None}
        else:
            mx = re.search(r'по горизонтали: ([^;]+);', nxt)
            mz = re.search(r'по вертикали: (.+)$', nxt)
            bind[name] = {'x': AXIS_BY_LABEL.get(mx.group(1).strip()) if mx else None,
                          'z': AXIS_BY_LABEL.get(mz.group(1).strip()) if mz else None}
    return axes, bind


def axis_values(key, n, axes):
    if key is None:
        return None
    k = key + str(n)
    return axes.get(k)


def raw_defs(cov, pst, ptu):
    """Байты, которые пользователь менял в платной, но которые не опознаны как таблицы, + блок констант."""
    def one(a, b, name, desc, ro=False):
        n = b - a
        return dict(name=name, sect=RAW, code='', addr=a - SHIFT, w=1, sg='u', k=1.0, b=0.0, nx=n, nz=1, order=0,
                    ax=None, az=None, axn=None, azn=None, note='', kind='raw', n=n, ro=ro, desc=desc,
                    ps=list(pst[a:b]), pt=list(ptu[a:b]))
    out = [one(CONST[0] + SHIFT, CONST[1] + SHIFT, 'Константы и флаги %04X–%04X' % (CONST[0], CONST[1] - 1),
               'Одиночные байты платной: флаги режимов и константы, таблицами не опознаны. Подсвечены те, что '
               'ты менял в своей настройке. Флаги j7es и платной могут значить разное — перед переносом '
               'каждый байт нужно опознать.')]
    diff = [i for i in range(0x75000, 0x7C000)
            if pst[i] != ptu[i] and not cov[i] and not CONST[0] + SHIFT <= i < CONST[1] + SHIFT]
    runs = []
    for i in diff:
        if runs and i - runs[-1][1] <= 8:
            runs[-1][1] = i + 1
        else:
            runs.append([i, i + 1])
    for a, b in runs:
        ja, jb = a - SHIFT, b - SHIFT
        if 0x6000 <= ja and jb <= CAL_END:
            out.append(one(a, b, 'Участок %04X–%04X' % (ja, jb - 1),
                           'Ты менял эти байты в платной, но таблицей они не опознаны.'))
        else:
            where = 'программа' if ja >= CAL_END else 'нет калибровок'
            out.append(one(a, b, 'Участок %04X–%04X (аналога в j7es нет)' % (ja, jb - 1),
                           'Ты менял эти байты в платной, но в j7es по этому адресу %s — перенести нельзя.' % where,
                           ro=True))
    return out


def main():
    lab = load_lab()
    dz = lab.load_disasm()
    jes = open(J7STOCK, 'rb').read()
    p27 = open(PAID27, 'rb').read()
    pst = open(PAIDST, 'rb').read()
    ptu = open(TUNED, 'rb').read()
    dis = dz.Disasm(jes).run()
    dpt = set()
    for pc, ins in dis.insn.items():
        m = re.match(r'MOV   DPTR,#([0-9A-F]{4})h', ins.text)
        if m:
            dpt.add(int(m.group(1), 16))
    axes, bind = tree_axes()
    z0, z1 = 0x75000, 0x7C000
    defs = []
    seen = set()
    cov = bytearray(0x90000)                    # байты платной, опознанные как таблицы
    for code, name, sect, nx, nz, var in cte_tables():
        hits = []
        for oi, v in enumerate(var):
            hits += [h + (oi,) for h in find(p27[z0:z1], z0, v)]
        for h in hits:
            cov[h[0]:h[0] + nx * nz * h[1]] = b'\1' * (nx * nz * h[1])
        if len({h[0] for h in hits}) != 1:
            continue
        a, w, sg, k, b, order = hits[0]
        n = nx * nz
        ja = a - SHIFT
        note = ''
        if 0x7AADE == a and n == 1024:
            # ПЦН по давлению: j7es читает 9294 (E38E–E3B1) как 16×16 (B00A) или 32×32 (AE05) по флагу 5F02 бит4;
            # строка — давление (F89A), столбец — обороты (57h)
            defs.append(dict(name=name, sect=SECTIONS.get(sect, sect), code=code, addr=0x9294, w=w, sg=sg, k=k, b=b,
                             nx=16, nz=16, order=0, ax=axis_values('RPM', 16, axes), az=axis_values('PR', 16, axes),
                             axn=AXIS_NAME['RPM'], azn=AXIS_NAME['PR'], note='',
                             alt=dict(fa=0x5F02, fb=4, nx=32, nz=32,
                                      ax=axis_values('RPM', 32, axes), az=axis_values('PR', 32, axes))))
            continue
        same = sum(1 for i in range(n * w) if jes[ja + i] == pst[a + i])
        if not (ja in dpt or same >= 0.9 * n * w):
            continue
        if ja in J7_OTHER:                      # тот же адрес, но в j7es другой смысл
            o = J7_OTHER[ja]
            if o is None:
                continue
            defs.append(dict(dict(sect=SECTIONS.get(sect, sect), code='', addr=ja, w=1, sg='u', b=0.0, nz=1, order=0,
                                  ax=None, az=None, axn=None, azn=None, nopaid=True,
                                  note='в платной по этому адресу «%s» — не переносить' % name), **o))
            continue
        key = (ja, n)
        if key in seen:
            continue
        seen.add(key)
        bd = bind.get(name, {'x': None, 'z': None})
        defs.append(dict(name=name, sect=SECTIONS.get(sect, sect), code=code, addr=ja, w=w, sg=sg, k=k, b=b,
                         nx=nx, nz=nz, order=order,
                         ax=axis_values(bd['x'], nx, axes), az=axis_values(bd['z'], nz, axes) if nz > 1 else None,
                         axn=AXIS_NAME.get(bd['x']), azn=AXIS_NAME.get(bd['z']) if nz > 1 else None, note=note))
    defs.sort(key=lambda d: (d['sect'], d['name']))
    # наша калибровка 6 цилиндров (режим E7F0 не показываем: редактор при сохранении пишет 07)
    hl = [[1, 'высокий'], [0, 'низкий']]
    cv = cte_values()
    def an(*names):                      # аналог в платной: «имя» = значение в настройке 28.09
        return '; '.join('«%s» = %s' % (n, cv.get(n, '?')) for n in names)
    six = [
        dict(name='Зуб опроса ДФ', addr=0xE7EF, nx=1, analog=an('Зуб опроса ДФ'),
             desc='Зуб коленвала, на котором снимается уровень датчика фаз (1..59; 0 — на первом зубе после '
                  'пропуска). Работает с прошивки v6. Номер считается от первого зуба после пропуска (он 0-й).'),
        dict(name='Уровень фазы на зубе 0', addr=0xE7F1, nx=1, kind='choice', opts=hl, mask=1,
             analog=an('Зуб опроса ДФ'),
             desc='Уровень сигнала датчика фаз на зубе опроса, при котором после ближайшего пропуска идёт такт '
                  '1-го цилиндра. Неверный — искра на ВМТ выпуска; выставляется на машине по 1-му цилиндру. '
                  'При смене зуба опроса с 0 на другой уровень обычно меняется на противоположный: замер '
                  'берётся из предыдущего оборота.'),
        dict(name='Уровень сигнала зарядки К5/К6', addr=0xE7F2, nx=1, kind='choice', opts=hl, mask=1, nopaid=True,
             desc='Каким уровнем ноги процессора 38 (К5) и 37 (К6) заряжают катушки. Должен совпадать '
                  'с уровнем зарядки К1–К4 на разъёме блока.'),
        dict(name='Форсунки: цилиндр → выход', addr=0xE7F3, nx=6, kind='grid', multi=True,
             cols=['Ф%d' % i for i in range(1, 7)],
             analog=an('Форсунки - фазированный режим', 'Форсунки - ПП режим'),
             desc='Строка — цилиндр по порядку работы, столбец — выход форсунки. В строке можно несколько отметок. '
                  'Попарный режим блок строит сам: цилиндры 1 и 4, 2 и 5, 3 и 6 вместе.'),
        dict(name='Катушки: цилиндр → выход', addr=0xE7F9, nx=6, kind='grid', multi=False,
             cols=['К%d' % i for i in range(1, 7)],
             analog=an('Катушки - фазированный режим', 'Катушки - ПП режим'),
             desc='Строка — цилиндр по порядку работы, столбец — выход катушки. В строке одна отметка.'),
        dict(name='Зуб ВМТ 1-го цилиндра по порядку работы (0..59)', addr=0xE7FF, nx=1,
             analog=an('Зуб ВМТ 1 цилиндра относительно пропуска'),
             desc='Номер зуба от первого после пропуска (он 0-й), на котором ВМТ 1-го цилиндра. '
                  'Совпадает ли счёт с платной — проверить стробоскопом (1 зуб = 6°).'),
    ]
    for s in six:
        defs.append(dict(dict(sect=SIX, code='', w=1, sg='u', k=1.0, b=0.0, nz=1, order=0, ax=None, az=None,
                              axn=None, azn=None, note='', six=True), **s))
    raw = raw_defs(cov, pst, ptu)
    defs += raw
    def ver(p):                          # j7es_v6.1_… → (6, 1)
        m = re.match(r'j7es_v(\d+)\.(\d+)_', os.path.basename(p))
        return (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    v5 = sorted((p for p in glob.glob(os.path.join(HERE, 'j7es_v*_*ИИ.bin')) if ver(p) >= (5, 0)), key=ver)
    bins = {'Сток j7es 0.7.5': J7STOCK}
    if v5:
        bins[os.path.basename(v5[-1])[:-4]] = v5[-1]
    emb = {k: base64.b64encode(open(p, 'rb').read()).decode() for k, p in bins.items()}
    html = TEMPLATE.replace('/*DEFS*/', json.dumps(defs, ensure_ascii=False)).replace('/*BINS*/', json.dumps(emb))
    open(OUT, 'w', encoding='utf-8').write(html)
    print('таблиц: %d, настроек 6 цил: %d, неразобранных участков: %d, бин: %s -> %s' % (
        len(defs) - len(six) - len(raw), len(six), len(raw), list(bins)[-1], OUT))


TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Калибровки j7es</title>
<style>
:root{--bg:#fafafa;--fg:#1d1d1f;--mut:#6b6b70;--line:#dcdce0;--pane:#fff;--sel:#e6efff;--acc:#2f6fe4;--chg:#d9480f;--red:#d0342c;--mine:rgba(230,150,30,.18)}
@media (prefers-color-scheme:dark){:root{--bg:#16171a;--fg:#e8e8ea;--mut:#9a9aa3;--line:#2c2e33;--pane:#1d1f23;--sel:#24324d;--acc:#6ea0ff;--chg:#ff8a50;--red:#ff6b6b;--mine:rgba(255,170,60,.16)}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:13px/1.35 -apple-system,Segoe UI,Roboto,sans-serif;height:100vh;display:flex;flex-direction:column}
header{display:flex;gap:8px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
header b{font-size:15px;margin-right:8px}select,button,input{font:inherit;color:inherit;background:var(--pane);border:1px solid var(--line);border-radius:6px;padding:4px 8px}
button{cursor:pointer}button.on{background:var(--acc);color:#fff;border-color:var(--acc)}
main{flex:1;display:flex;min-height:0}#tree{width:330px;min-width:220px;border-right:1px solid var(--line);overflow:auto;padding:6px}
#tree input{width:100%;margin-bottom:6px}.sec{font-weight:600;margin:8px 0 2px;cursor:pointer;user-select:none}.sec .cnt{color:var(--mut);font-weight:400}
.it{padding:3px 6px 3px 14px;border-radius:5px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.it:hover{background:var(--sel)}.it.act{background:var(--sel);color:var(--acc)}
.it .dot{display:inline-block;width:6px;height:6px;border-radius:3px;background:var(--chg);margin-right:5px;vertical-align:middle}
#view{flex:1;overflow:auto;padding:12px 16px}#meta{color:var(--mut);margin:2px 0 10px}h2{margin:0;font-size:16px}
table.g{border-collapse:collapse;font-variant-numeric:tabular-nums}table.g td,table.g th{border:1px solid var(--line);padding:2px 5px;text-align:right;min-width:42px}
table.g th{background:var(--pane);color:var(--mut);font-weight:500;position:sticky;top:0}table.g td.ch{outline:2px solid var(--chg);outline-offset:-2px}
table.g td input{width:56px;border:none;padding:0;background:transparent;text-align:right}
#chart svg{background:var(--pane);border:1px solid var(--line);border-radius:6px}.tools{display:flex;gap:6px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
.hint{color:var(--mut);font-size:12px}#zsel{display:flex;gap:4px;flex-wrap:wrap;margin:6px 0}#zsel label{font-size:12px;color:var(--mut)}
.it.np,.red{color:var(--red)}.desc{margin:0 0 10px;max-width:760px}table.g tr.mine td{background:var(--mine)}table.g.six td{text-align:center}
</style></head><body>
<header><b>Калибровки j7es</b>
<select id="binsel"></select><button id="open">Открыть бин…</button><input id="file" type="file" accept=".bin" hidden>
<button id="save">Сохранить бин</button><label class="hint"><input type="checkbox" id="cmp"> Сравнить со стоком j7es</label>
<span class="hint" id="stat"></span></header>
<main><div id="tree"><input id="q" placeholder="Поиск по названию"><div id="list"></div></div>
<div id="view"><div class="hint">Выберите калибровку слева.</div></div></main>
<script>
const DEFS=/*DEFS*/;const BINS=/*BINS*/;
const b64=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const STOCK=b64(BINS['Сток j7es 0.7.5']);let cur=null,curName='',sel=null,mode='table',cmpOn=false,mineOnly=true;
const hex4=a=>a.toString(16).toUpperCase().padStart(4,'0');
// патч 6 цилиндров есть, если занято место под его код (E800…)
function hasPatch(d){for(let i=0xE800;i<0xE810;i++)if(d[i])return true;return false}
// ПЦН: размер таблицы по флагу (5F02 бит4 = 1 — код читает 32×32)
function geo(t){if(t.alt&&(cur[t.alt.fa]>>t.alt.fb&1))return Object.assign({},t,t.alt,{big:true});return t}
document.getElementById('cmp').onchange=e=>{cmpOn=e.target.checked;refresh()};
const binsel=document.getElementById('binsel');
for(const k of Object.keys(BINS)){const o=document.createElement('option');o.value=k;o.textContent=k;binsel.appendChild(o)}
binsel.value=Object.keys(BINS).slice(-1)[0];
function loadEmb(){cur=b64(BINS[binsel.value]).slice();curName=binsel.value+'.bin';refresh()}
binsel.onchange=loadEmb;
document.getElementById('open').onclick=()=>document.getElementById('file').click();
document.getElementById('file').onchange=e=>{const f=e.target.files[0];if(!f)return;f.arrayBuffer().then(b=>{const u=new Uint8Array(b);
 if(u.length!==65536){alert('Это не бин j7es: нужен файл 64 КБ.');return}cur=u;curName=f.name;refresh()})};
function rd(d,a,w,sg){if(w===1){let v=d[a];return sg==='s'&&v>127?v-256:v}let v=d[a]|d[a+1]<<8;return sg==='s'&&v>32767?v-65536:v}
function wr(d,a,w,sg,v){const lo=sg==='s'?(w===1?-128:-32768):0,hi=sg==='s'?(w===1?127:32767):(w===1?255:65535);v=Math.max(lo,Math.min(hi,v));if(v<0)v+=w===1?256:65536;d[a]=v&255;if(w===2)d[a+1]=v>>8}
function idx(t,x,z){return t.order===0?z*t.nx+x:x*t.nz+z}
function val(d,t,x,z){return rd(d,t.addr+idx(t,x,z)*t.w,t.w,t.sg)*t.k+t.b}
function changed(t0){if(!cmpOn)return false;const t=geo(t0),n=t.nx*t.nz*t.w;for(let i=0;i<n;i++)if(cur[t.addr+i]!==STOCK[t.addr+i])return true;return false}
function fmt(v,t){const a=Math.abs(t.k);const dg=a>=1?0:a>=0.1?1:a>=0.01?2:a>=0.001?3:4;return v.toFixed(dg)}
function buildTree(){const q=document.getElementById('q').value.toLowerCase();const L=document.getElementById('list');L.innerHTML='';
 const by={};DEFS.forEach((t,i)=>{if(q&&!t.name.toLowerCase().includes(q))return;(by[t.sect]=by[t.sect]||[]).push(i)});
 for(const s of Object.keys(by)){const h=document.createElement('div');h.className='sec';h.innerHTML=s+' <span class="cnt">'+by[s].length+'</span>';L.appendChild(h);
  const box=document.createElement('div');L.appendChild(box);h.onclick=()=>box.hidden=!box.hidden;
  for(const i of by[s]){const t=DEFS[i],e=document.createElement('div');e.className='it'+(i===sel?' act':'')+(t.nopaid?' np':'');e.title=t.name+(t.nopaid?' — нет в платной прошивке':'');
   e.innerHTML=(changed(t)?'<span class="dot"></span>':'')+t.name;e.onclick=()=>{sel=i;buildTree();show()};box.appendChild(e)}}}
document.getElementById('q').oninput=buildTree;
function refresh(){buildTree();if(sel!==null)show();let n=0;DEFS.forEach(t=>{if(changed(t))n++});document.getElementById('stat').textContent=curName+(cmpOn?' · отличается от стока j7es: '+n+' калибровок':'')}
function head(t){return '<h2>'+t.name+'</h2><div id="meta">'+t.sect+' · адрес '+hex4(t.addr)+(t.nopaid?' · <span class="red">нет в платной прошивке</span>':'')+
 (t.analog?'<br>В платной (твоя настройка 28.09): '+t.analog:'')+'</div>'+(t.desc?'<p class="desc">'+t.desc+'</p>':'')}
function show(){const t=geo(DEFS[sel]),V=document.getElementById('view');
 if(t.six&&!hasPatch(cur)){V.innerHTML=head(t)+'<p class="desc red">В этом бине нет патча 6 цилиндров.</p>';return}
 if(t.kind==='raw')return rawView(V,t);
 if(t.kind==='choice'||t.kind==='grid')return sixView(V,t);
 const ax=t.ax||Array.from({length:t.nx},(_,i)=>i+1),az=t.az||Array.from({length:t.nz},(_,i)=>i+1);
 V.innerHTML='<h2>'+t.name+'</h2><div id="meta">'+t.sect+' · адрес '+hex4(t.addr)+' · '+(t.nz>1?t.nx+'×'+t.nz:t.nx+' точек')+' · '+(t.w*8)+' бит'+(t.sg==='s'?' со знаком':'')+
 ' · значение = байт × '+(+t.k.toPrecision(6))+(t.b?' + '+(+t.b.toPrecision(6)):'')+(t.axn?' · X: '+t.axn:'')+(t.azn?' · Z: '+t.azn:'')+
 (t.nopaid?' · <span class="red">нет в платной прошивке</span>':'')+(t.analog?'<br>В платной (твоя настройка 28.09): '+t.analog:'')+(t.note?'<br>⚠ '+t.note:'')+
 (t.alt?'<br>Блок читает эту таблицу как '+(t.big?'32×32':'16×16')+' (флаг 5F02 бит4 = '+(t.big?1:0)+').':'')+'</div>'+(t.desc?'<p class="desc">'+t.desc+'</p>':'')+
 '<div class="tools"><button id="mt" class="'+(mode==='table'?'on':'')+'">Таблица</button><button id="mc" class="'+(mode==='chart'?'on':'')+'">График</button>'+
 '<span class="hint">Двойной клик по клетке — правка.'+(cmpOn?' Рамкой — отличие от стока j7es.':'')+'</span></div><div id="body"></div>';
 document.getElementById('mt').onclick=()=>{mode='table';show()};document.getElementById('mc').onclick=()=>{mode='chart';show()};
 const B=document.getElementById('body');if(mode==='table'||t.nx*t.nz===1)tableView(B,t,ax,az);else chartView(B,t,ax,az)}
function color(v,lo,hi){if(hi===lo)return '';const p=(v-lo)/(hi-lo);const h=240-240*p;return 'background:hsla('+h+',70%,55%,.28)'}
function tableView(B,t,ax,az){let lo=Infinity,hi=-Infinity;for(let z=0;z<t.nz;z++)for(let x=0;x<t.nx;x++){const v=val(cur,t,x,z);lo=Math.min(lo,v);hi=Math.max(hi,v)}
 let h='<table class="g"><tr><th>'+(t.nz>1?(t.azn||'Z')+' \\ '+(t.axn||'X'):(t.axn||'№'))+'</th>';
 if(t.nz>1){for(let x=0;x<t.nx;x++)h+='<th>'+ax[x]+'</th>';h+='</tr>';
  for(let z=t.nz-1;z>=0;z--){h+='<tr><th>'+az[z]+'</th>';for(let x=0;x<t.nx;x++)h+=cell(t,x,z,lo,hi);h+='</tr>'}}
 else{h+='<th>значение</th></tr>';for(let x=0;x<t.nx;x++)h+='<tr><th>'+ax[x]+'</th>'+cell(t,x,0,lo,hi)+'</tr>'}
 B.innerHTML=h+'</table>';B.querySelectorAll('td').forEach(td=>td.ondblclick=()=>edit(td,t))}
function cell(t,x,z,lo,hi){const a=t.addr+idx(t,x,z)*t.w;let ch=false;if(cmpOn)for(let i=0;i<t.w;i++)if(cur[a+i]!==STOCK[a+i])ch=true;
 const v=val(cur,t,x,z),s=val(STOCK,t,x,z);return '<td data-x="'+x+'" data-z="'+z+'" class="'+(ch?'ch':'')+'" style="'+color(v,lo,hi)+'"'+(cmpOn?' title="сток j7es: '+fmt(s,t)+'"':'')+'>'+fmt(v,t)+'</td>'}
function sixView(V,t){let h=head(t);
 if(t.kind==='choice'){const v=cur[t.addr]&t.mask;h+='<select id="ch">'+t.opts.map(o=>'<option value="'+o[0]+'"'+(o[0]===v?' selected':'')+'>'+o[1]+'</option>').join('')+'</select>'}
 else{h+='<table class="g six"><tr><th>цилиндр</th>'+t.cols.map(c=>'<th>'+c+'</th>').join('')+'</tr>';
  for(let r=0;r<6;r++){const v=cur[t.addr+r];let row='',any=false;
   for(let c=0;c<6;c++){const on=t.multi?(v>>c&1)===1:v===c;any=any||on;
    row+='<td><input type="'+(t.multi?'checkbox':'radio')+'" name="r'+r+'" data-r="'+r+'" data-c="'+c+'"'+(on?' checked':'')+'></td>'}
   h+='<tr><th'+(any?'':' class="red" title="у цилиндра нет выхода"')+'>'+(r+1)+'</th>'+row+'</tr>'}
  h+='</table>'}
 V.innerHTML=h;
 if(t.kind==='choice')document.getElementById('ch').onchange=e=>{cur[t.addr]=(cur[t.addr]&~t.mask)|+e.target.value;refresh()};
 else V.querySelectorAll('input[data-r]').forEach(i=>i.onchange=()=>{const a=t.addr+ +i.dataset.r,c=+i.dataset.c;
  if(t.multi)cur[a]=i.checked?cur[a]|1<<c:cur[a]&~(1<<c);else cur[a]=c;refresh()})}
function rawView(V,t){let h=head(t)+'<div class="tools"><label class="hint"><input type="checkbox" id="mo"'+(mineOnly?' checked':'')+'> Только изменённые тобой</label>'+
 (t.ro?'':'<span class="hint">Двойной клик по значению — правка (0…255).</span>')+'</div>';
 h+='<table class="g"><tr><th>адрес j7es</th><th>значение</th><th>сток j7es</th><th>сток платной</th><th>твоя настройка</th><th>перенесено</th></tr>';
 for(let i=0;i<t.n;i++){const a=t.addr+i,mine=t.ps[i]!==t.pt[i];if(mineOnly&&!mine)continue;
  h+='<tr class="'+(mine?'mine':'')+'"><th>'+hex4(a)+'</th><td data-i="'+i+'">'+(t.ro?'—':cur[a])+'</td><td>'+(t.ro?'—':STOCK[a])+'</td><td>'+t.ps[i]+'</td><td>'+t.pt[i]+'</td><td>'+
   (mine&&!t.ro?(cur[a]===t.pt[i]?'да':'<span class="red">нет</span>'):'')+'</td></tr>'}
 V.innerHTML=h+'</table>';document.getElementById('mo').onchange=e=>{mineOnly=e.target.checked;show()};
 if(!t.ro)V.querySelectorAll('td[data-i]').forEach(td=>td.ondblclick=()=>{const a=t.addr+ +td.dataset.i;const inp=document.createElement('input');inp.value=cur[a];
  td.textContent='';td.appendChild(inp);inp.focus();inp.select();
  const done=ok=>{if(ok){const v=parseInt(inp.value.trim(),10);if(isNaN(v)||v<0||v>255){alert('Нужно целое число от 0 до 255');show();return}cur[a]=v}refresh()};
  inp.onkeydown=e=>{if(e.key==='Enter')done(true);if(e.key==='Escape')done(false)};inp.onblur=()=>done(true)})}
function edit(td,t){const x=+td.dataset.x,z=+td.dataset.z,old=val(cur,t,x,z);const inp=document.createElement('input');inp.value=fmt(old,t);td.textContent='';td.appendChild(inp);inp.focus();inp.select();
 const done=ok=>{if(ok){let s=inp.value.trim().replace(',','.');let v=parseFloat(s);
  if(isNaN(v)){alert('Не число');show();return}wr(cur,t.addr+idx(t,x,z)*t.w,t.w,t.sg,Math.round((v-t.b)/t.k))}refresh()};
 inp.onkeydown=e=>{if(e.key==='Enter')done(true);if(e.key==='Escape')done(false)};inp.onblur=()=>done(true)}
function chartView(B,t,ax,az){const W=Math.min(1100,B.clientWidth-10)||900,H=420,P=46;let lo=Infinity,hi=-Infinity;
 for(let z=0;z<t.nz;z++)for(let x=0;x<t.nx;x++){const v=val(cur,t,x,z);lo=Math.min(lo,v);hi=Math.max(hi,v)}if(hi===lo){hi+=1;lo-=1}
 const X=i=>P+i*(W-P-12)/Math.max(1,t.nx-1),Y=v=>H-28-(v-lo)/(hi-lo)*(H-50);
 let s='<svg width="'+W+'" height="'+H+'">';for(let g=0;g<=5;g++){const v=lo+(hi-lo)*g/5;s+='<line x1="'+P+'" x2="'+(W-10)+'" y1="'+Y(v)+'" y2="'+Y(v)+'" stroke="currentColor" opacity=".12"/><text x="4" y="'+(Y(v)+4)+'" font-size="11" fill="currentColor" opacity=".6">'+fmt(v,t)+'</text>'}
 for(let x=0;x<t.nx;x+=Math.ceil(t.nx/16))s+='<text x="'+X(x)+'" y="'+(H-8)+'" font-size="11" text-anchor="middle" fill="currentColor" opacity=".6">'+ax[x]+'</text>';
 const zs=[];for(let z=0;z<t.nz;z++)zs.push(z);
 zs.forEach(z=>{let d='';for(let x=0;x<t.nx;x++)d+=(x?'L':'M')+X(x).toFixed(1)+' '+Y(val(cur,t,x,z)).toFixed(1);
  const col='hsl('+(t.nz>1?240-240*z/(t.nz-1):220)+',70%,50%)';s+='<path d="'+d+'" fill="none" stroke="'+col+'" stroke-width="1.6"><title>'+(t.azn||'Z')+' = '+az[z]+'</title></path>'});
 s+='</svg>';B.innerHTML='<div id="chart">'+s+'</div><div class="hint">'+(t.nz>1?'Линия на каждое значение '+(t.azn||'оси Z')+': синяя — нижнее, красная — верхнее. Наведите на линию — подпись.':'')+' По X: '+(t.axn||'номер точки')+'.</div>'}
function fixsum(d){d[0xFFF8]=d[0xFFF9]=0;let s0=0;for(let i=0;i<0xFFFE;i++)s0+=d[i];s0&=0xFFFF;let c=-1;
 for(let hi=0;hi<256;hi++){const cc=(255*hi-s0)&0xFFFF;if(cc<=510){c=cc;break}}if(c<0){alert('Не удалось подобрать контрольную сумму');return false}
 d[0xFFF8]=Math.min(c,255);d[0xFFF9]=c-Math.min(c,255);let s1=0;for(let i=0;i<0xFFFE;i++)s1+=d[i];
 for(let v=0;v<65536;v++)if(((s1+(v&255)+(v>>8))&0xFFFF)===v){d[0xFFFE]=v&255;d[0xFFFF]=v>>8;return true}alert('Не удалось подобрать контрольную сумму');return false}
document.getElementById('save').onclick=()=>{const d=cur.slice();if(hasPatch(d))d[0xE7F0]=7;if(!fixsum(d))return;const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([d],{type:'application/octet-stream'}));a.download=curName.replace(/\.bin$/,'')+' правка.bin';a.click()};
loadEmb();
</script></body></html>
'''

if __name__ == '__main__':
    main()
