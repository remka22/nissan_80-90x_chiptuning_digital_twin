# -*- coding: utf-8 -*-
"""
Анализатор расшифровки: по набору СНИМКОВ ОЗУ + известным опорным сигналам
находит, какой адрес за каким сигналом следует (корреляция Пирсона).

Это способ 1 («по поведению»): даёт КАНДИДАТОВ, которых потом подтверждают
дизасмом. Работает и на реальных логах, и на снимках с двойника.

Байтовый режим находит младший байт 16-битных величин; словный режим
(addr, addr+1 как 16-бит big-endian) находит саму 16-битную переменную.
"""


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / ((sxx * syy) ** 0.5)


def rank_bytes(snapshots, ref, base_addr):
    """Корреляция каждого БАЙТА с опорой ref. -> [(addr, |r|, r), ...] по убыв."""
    N = len(snapshots[0])
    out = []
    for i in range(N):
        col = [snap[i] for snap in snapshots]
        r = pearson(col, ref)
        out.append((base_addr + i, abs(r), r))
    out.sort(key=lambda t: -t[1])
    return out


def rank_words(snapshots, ref, base_addr):
    """Корреляция каждой пары (addr,addr+1) как 16-бит big-endian с ref."""
    N = len(snapshots[0])
    out = []
    for i in range(N - 1):
        col = [(snap[i] << 8) | snap[i + 1] for snap in snapshots]
        r = pearson(col, ref)
        out.append((base_addr + i, abs(r), r))
    out.sort(key=lambda t: -t[1])
    return out


def classify(snapshots, base_addr):
    """Грубая классификация: константа / меняется. -> множества адресов."""
    N = len(snapshots[0])
    const, vary = [], []
    for i in range(N):
        col = [snap[i] for snap in snapshots]
        (const if len(set(col)) == 1 else vary).append(base_addr + i)
    return const, vary
