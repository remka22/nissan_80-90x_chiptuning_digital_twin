#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сравнение кода j7es v0.7.5 и заводской I205DM53 (Январь 7.2, C509) по функциям.

Побайтово сравнивать нельзя: j7es пересобрана, код сдвинут. Поэтому:
  1) оба образа дизассемблируются (тот же дизассемблер);
  2) каждая команда нормализуется: адреса переходов → L, адреса таблиц в ПЗУ → T,
     регистры / ячейки ОЗУ / переменные XRAM (F000+) / константы остаются;
  3) код режется на базовые блоки, блоки сопоставляются по отпечаткам
     (уникальные совпадения + распространение по соседям и переходам);
  4) функция = вход подпрограммы или вектора и весь код до следующего входа;
     для каждой функции j7es ищется пара в заводской и доля совпавшего кода.

Запуск: python3 "сравнение j7es и I205DM53 04.10.26 ИИ.py"  → отчёт рядом.
"""
import collections
import difflib
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
J7 = os.path.join(HERE, 'j7es_074', 'j7es_v0.7.5.bin')
FA = os.path.join(HERE, 'i205dm53', 'I205DM53-D909.bin')
OUT = os.path.join(HERE, 'сравнение j7es и I205DM53 — функции 04.10.26 ИИ.txt')

spec = importlib.util.spec_from_file_location('dis', os.path.join(HERE, 'j7es_074', 'дизассемблер 8051 C509 01.10.26 ИИ.py'))
dis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dis)


class Image:
    def __init__(self, path, name):
        self.name = name
        self.d = open(path, 'rb').read()
        self.D = dis.Disasm(self.d).run()
        self.ins = self.D.insn
        self.addrs = sorted(self.ins)
        self.idx = {a: i for i, a in enumerate(self.addrs)}
        self.norm = {a: self.normalize(self.ins[a]) for a in self.addrs}
        self.blocks = self.make_blocks()
        self.funcs = self.make_funcs()

    def normalize(self, ins):
        t = ins.text
        t = re.sub(r'\{L:[0-9A-F]{4}\}', 'L', t)
        def dptr(m):
            v = int(m.group(1), 16)
            return m.group(0) if v >= 0xF000 else '#T'
        t = re.sub(r'#([0-9A-F]{4})h', dptr, t)
        return re.sub(r'\s+', ' ', t)

    def make_blocks(self):
        starts = set(self.D.xref) | set(self.D.entries)
        blocks = []
        cur = []
        prev_end = None
        for a in self.addrs:
            ins = self.ins[a]
            if cur and (a in starts or a != prev_end):
                blocks.append(cur)
                cur = []
            cur.append(a)
            prev_end = a + ins.size
            if ins.kind in ('jump', 'ret', 'ijmp', 'cond'):
                blocks.append(cur)
                cur = []
                prev_end = None
        if cur:
            blocks.append(cur)
        return blocks

    def make_funcs(self):
        entries = set(self.D.calls) | {self.ins[v].targets[0] for v in self.D.entries if self.ins[v].targets}
        entries = sorted(e for e in entries if e in self.ins)
        funcs = {}
        for i, e in enumerate(entries):
            end = entries[i + 1] if i + 1 < len(entries) else 0x10000
            body = [a for a in self.addrs[self.idx[e]:] if a < end]
            # только непрерывный разобранный код
            funcs[e] = body
        return funcs

    def label(self, a):
        for v, name in dis.VECTORS.items():
            if v in self.D.entries and self.ins[v].targets and self.ins[v].targets[0] == a:
                return 'вектор %04X %s' % (v, name)
        return 'sub_%04X' % a


def match(J, F):
    """Сопоставление базовых блоков: отпечаток = кортеж нормализованных команд."""
    def fp(img, b):
        return tuple(img.norm[a] for a in b)
    jb = {tuple(b): fp(J, b) for b in J.blocks}
    fb = {tuple(b): fp(F, b) for b in F.blocks}
    jcount = collections.Counter(v for v in jb.values() if len(v) >= 2)
    fcount = collections.Counter(v for v in fb.values() if len(v) >= 2)
    finv = collections.defaultdict(list)
    for b, v in fb.items():
        finv[v].append(b)
    amap = {}          # адрес команды j7es -> адрес в заводской
    for b, v in jb.items():
        if len(v) >= 2 and jcount[v] == 1 and fcount[v] == 1:
            fbk = finv[v][0]
            for x, y in zip(b, fbk):
                amap[x] = y
    # распространение: если команда совпала, пробуем соседние команды по порядку
    used = set(amap.values())
    changed = True
    while changed:
        changed = False
        for x in list(amap):
            y = amap[x]
            for dx in (1, -1):
                i, k = J.idx.get(x), F.idx.get(y)
                if i is None or k is None:
                    continue
                i2, k2 = i + dx, k + dx
                if 0 <= i2 < len(J.addrs) and 0 <= k2 < len(F.addrs):
                    x2, y2 = J.addrs[i2], F.addrs[k2]
                    if x2 not in amap and y2 not in used and J.norm[x2] == F.norm[y2] \
                            and (x2 - x) == (y2 - y):
                        amap[x2] = y2
                        used.add(y2)
                        changed = True
    return amap


def summarize(img, body):
    """Что трогает кусок кода: XRAM, таблицы ПЗУ, SFR, вызовы."""
    xr, tb, sfr, calls = set(), set(), set(), set()
    for a in body:
        ins = img.ins[a]
        t = ins.text
        for m in re.finditer(r'#([0-9A-F]{4})h', t):
            v = int(m.group(1), 16)
            (xr if v >= 0xF000 else tb).add(v)
        for name in re.findall(r'\b([A-Z][A-Z0-9]+[?]?)\b', t):
            if name in dis.SFR.values() and name not in ('ACC', 'B', 'PSW', 'DPL', 'DPH', 'SP', 'DPSEL'):
                sfr.add(name)
        if ins.kind == 'call':
            calls.update(ins.targets)
    return xr, tb, sfr, calls


def main():
    J = Image(J7, 'j7es')
    F = Image(FA, 'I205DM53')
    amap = match(J, F)
    rev = {}
    for x, y in amap.items():
        rev[y] = x

    # функции заводской по адресу команды
    fown = {}
    for e, body in F.funcs.items():
        for a in body:
            fown[a] = e

    rows = []
    for e, body in sorted(J.funcs.items()):
        n = len(body)
        if not n:
            continue
        hits = [amap[a] for a in body if a in amap]
        frac = len(hits) / n
        owners = collections.Counter(fown.get(y) for y in hits if fown.get(y) is not None)
        pair = owners.most_common(1)[0][0] if owners else None
        pf = F.funcs.get(pair, []) if pair is not None else []
        if pair is not None:
            sim = difflib.SequenceMatcher(None, [J.norm[a] for a in body], [F.norm[a] for a in pf], autojunk=False).ratio()
        else:
            sim = 0.0
        if pair is not None and sim >= 0.98 and len(pf) == n:
            kind = 'ТОТ ЖЕ'
        elif pair is not None and sim >= 0.5:
            kind = 'ИЗМЕНЁН'
        else:
            kind = 'НОВЫЙ'
        size = sum(J.ins[a].size for a in body)
        rows.append((kind, e, pair, n, size, frac, sim))

    used_f = {r[2] for r in rows if r[2] is not None and r[0] != 'НОВЫЙ'}
    fa_rows = []
    for e, body in sorted(F.funcs.items()):
        hits = sum(1 for a in body if a in rev)
        frac = hits / len(body) if body else 0
        if e not in used_f and frac < 0.5:
            fa_rows.append((e, len(body), sum(F.ins[a].size for a in body), frac))

    with open(OUT, 'w', encoding='utf-8') as w:
        P = lambda s='': w.write(s + '\n')
        P('# Сравнение j7es v0.7.5 и заводской I205DM53 по функциям (скрипт «сравнение j7es и I205DM53 04.10.26 ИИ.py»)')
        P('# Функция = вход подпрограммы/вектора до следующего входа. Доля = часть команд j7es, найденных в заводской')
        P('# (по совпавшим блокам). Сходство = похожесть последовательности команд с парой (адреса заменены на L/T).')
        P('# ТОТ ЖЕ: сходство ≥ 0.98 и та же длина. ИЗМЕНЁН: сходство ≥ 0.5. НОВЫЙ: пары нет или сходство < 0.5.')
        P('')
        P('Код j7es: %d команд, функций %d.  Заводская: %d команд, функций %d.' % (len(J.addrs), len(J.funcs), len(F.addrs), len(F.funcs)))
        P('Команд j7es, сопоставленных с заводской: %d (%.0f %%).' % (len(amap), 100.0 * len(amap) / len(J.addrs)))
        c = collections.Counter(r[0] for r in rows)
        P('Функций j7es: ТОТ ЖЕ %d, ИЗМЕНЁН %d, НОВЫЙ %d. Заводских без пары: %d.' % (c['ТОТ ЖЕ'], c['ИЗМЕНЁН'], c['НОВЫЙ'], len(fa_rows)))
        for kind in ('НОВЫЙ', 'ИЗМЕНЁН', 'ТОТ ЖЕ'):
            P('')
            P('=' * 100)
            P(' %s' % kind)
            P('=' * 100)
            for k, e, pair, n, size, frac, sim in rows:
                if k != kind:
                    continue
                xr, tb, sfr, calls = summarize(J, J.funcs[e])
                P('%s  (%d команд, %d байт)  пара в заводской: %s  доля %.0f%%  сходство %.2f'
                  % (J.label(e), n, size, ('%04X' % pair) if pair is not None else '—', 100 * frac, sim))
                if kind != 'ТОТ ЖЕ':
                    if xr:
                        P('    XRAM: ' + ' '.join('%04X' % v for v in sorted(xr)))
                    if tb:
                        P('    таблицы ПЗУ: ' + ' '.join('%04X' % v for v in sorted(tb)))
                    if sfr:
                        P('    регистры: ' + ' '.join(sorted(sfr)))
                    if calls:
                        P('    вызывает: ' + ' '.join('%04X' % v for v in sorted(calls)))
        P('')
        P('=' * 100)
        P(' ЗАВОДСКИЕ ФУНКЦИИ БЕЗ ПАРЫ В j7es (убраны или переписаны до неузнаваемости)')
        P('=' * 100)
        for e, n, size, frac in fa_rows:
            xr, tb, sfr, calls = summarize(F, F.funcs[e])
            P('%s  (%d команд, %d байт)  найдено в j7es %.0f%%' % (F.label(e), n, size, 100 * frac))
            if xr:
                P('    XRAM: ' + ' '.join('%04X' % v for v in sorted(xr)))
            if sfr:
                P('    регистры: ' + ' '.join(sorted(sfr)))
        # участки без пары (мельче функций): добавленный / убранный код
        def runs(img, mapped, minb):
            out, cur = [], []
            for a in img.addrs:
                if a not in mapped:
                    if cur and a != cur[-1] + img.ins[cur[-1]].size:
                        out.append(cur)
                        cur = []
                    cur.append(a)
                elif cur:
                    out.append(cur)
                    cur = []
            if cur:
                out.append(cur)
            res = []
            for r in out:
                size = sum(img.ins[a].size for a in r)
                if size >= minb:
                    res.append((r[0], r[-1] + img.ins[r[-1]].size - 1, size, r))
            return res
        for title, img, mapped in (('УЧАСТКИ j7es БЕЗ ПАРЫ (добавлено / переписано), от 16 байт', J, amap),
                                   ('УЧАСТКИ ЗАВОДСКОЙ БЕЗ ПАРЫ (убрано / переписано), от 16 байт', F, rev)):
            rr = runs(img, mapped, 16)
            P('')
            P('=' * 100)
            P(' %s: %d участков, %d байт' % (title, len(rr), sum(x[2] for x in rr)))
            P('=' * 100)
            for a0, a1, size, r in rr:
                xr, tb, sfr, calls = summarize(img, r)
                parts = []
                if xr:
                    parts.append('XRAM ' + ' '.join('%04X' % v for v in sorted(xr)[:12]) + (' …' if len(xr) > 12 else ''))
                if tb:
                    parts.append('ПЗУ ' + ' '.join('%04X' % v for v in sorted(tb)[:8]) + (' …' if len(tb) > 8 else ''))
                if sfr:
                    parts.append('рег ' + ' '.join(sorted(sfr)))
                P('%04X–%04X %5d б  %s' % (a0, a1, size, ' | '.join(parts)))
    print('Записан:', OUT)
    print('Сопоставлено команд j7es: %d из %d' % (len(amap), len(J.addrs)))
    print(collections.Counter(r[0] for r in rows), 'заводских без пары:', len(fa_rows))


if __name__ == '__main__':
    main()
