#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Дизассемблер 8051 для прошивок Января 7.2 (процессор Infineon SAF-C509-L).

Идёт от векторов прерываний по всем переходам и вызовам (рекурсивный обход),
разбирает таблицы переходов после JMP @A+DPTR, подписывает регистры C509.
То, до чего обход не дошёл, выводится как данные.

Запуск:
    python3 "дизассемблер 8051 C509 01.10.26 ИИ.py" прошивка.bin листинг.txt
"""
import sys
from collections import defaultdict

# --- Регистры специальных функций. Имена со знаком «?» — по памяти, не сверены с документацией ---
SFR = {
    0x80: 'P0', 0x81: 'SP', 0x82: 'DPL', 0x83: 'DPH', 0x84: 'WDTL?', 0x85: 'WDTH?', 0x86: 'WDTREL',
    0x87: 'PCON', 0x88: 'TCON', 0x89: 'TMOD', 0x8A: 'TL0', 0x8B: 'TL1', 0x8C: 'TH0', 0x8D: 'TH1',
    0x90: 'P1', 0x91: 'XPAGE', 0x92: 'DPSEL', 0x98: 'S0CON', 0x99: 'S0BUF', 0x9A: 'IEN2',
    0x9B: 'S1CON', 0x9C: 'S1BUF', 0x9D: 'S1RELL',
    0xA0: 'P2', 0xA1: 'COMSETL', 0xA2: 'COMSETH', 0xA3: 'COMCLRL', 0xA4: 'COMCLRH',
    0xA5: 'SETMSK', 0xA6: 'CLRMSK', 0xA8: 'IEN0', 0xA9: 'IP0', 0xAA: 'S0RELL',
    0xB0: 'P3', 0xB1: 'SYSCON', 0xB2: 'SYSCON1?', 0xB4: 'PRSC?', 0xB8: 'IEN1', 0xB9: 'IP1',
    0xBA: 'S0RELH', 0xBB: 'S1RELH', 0xBC: 'CT1CON?', 0xBE: 'IEN3?', 0xBF: 'IRCON2?',
    0xC0: 'IRCON0', 0xC1: 'CCEN', 0xC2: 'CCL1', 0xC3: 'CCH1', 0xC4: 'CCL2', 0xC5: 'CCH2',
    0xC6: 'CCL3', 0xC7: 'CCH3', 0xC8: 'T2CON', 0xC9: 'CC4EN', 0xCA: 'CRCL', 0xCB: 'CRCH',
    0xCC: 'TL2', 0xCD: 'TH2', 0xCE: 'CCL4', 0xCF: 'CCH4',
    0xD0: 'PSW', 0xD1: 'IRCON1', 0xD2: 'CML0', 0xD3: 'CMH0', 0xD4: 'CML1', 0xD5: 'CMH1',
    0xD6: 'CML2', 0xD7: 'CMH2', 0xD8: 'ADCON0', 0xD9: 'ADDATH', 0xDA: 'ADDATL', 0xDB: 'P7',
    0xDC: 'ADCON1', 0xDD: 'P8', 0xDE: 'CTRELL', 0xDF: 'CTRELH',
    0xE0: 'ACC', 0xE1: 'CTCON', 0xE2: 'CML3', 0xE3: 'CMH3', 0xE4: 'CML4', 0xE5: 'CMH4',
    0xE6: 'CML5', 0xE7: 'CMH5', 0xE8: 'P4', 0xE9: 'MD0', 0xEA: 'MD1', 0xEB: 'MD2', 0xEC: 'MD3',
    0xED: 'MD4', 0xEE: 'MD5', 0xEF: 'ARCON',
    0xF0: 'B', 0xF2: 'CML6', 0xF3: 'CMH6', 0xF4: 'CML7', 0xF5: 'CMH7', 0xF6: 'CMEN', 0xF7: 'CMSEL',
    0xF8: 'P5', 0xF9: 'P9?', 0xFA: 'P6',
}

# --- Векторы прерываний C517A/C509 ---
VECTORS = {
    0x0000: 'сброс', 0x0003: 'внешнее INT0', 0x000B: 'таймер 0', 0x0013: 'внешнее INT1',
    0x001B: 'таймер 1', 0x0023: 'последовательный порт 0', 0x002B: 'таймер 2',
    0x0043: 'АЦП', 0x004B: 'внешнее INT2', 0x0053: 'внешнее INT3 / захват CC0',
    0x005B: 'внешнее INT4 / CC1', 0x0063: 'внешнее INT5 / CC2', 0x006B: 'внешнее INT6 / CC3',
    0x0083: 'последовательный порт 1', 0x0093: 'совпадение CM0-CM7',
    0x009B: 'переполнение таймера сравнения', 0x00A3: 'совпадение COMSET', 0x00AB: 'совпадение COMCLR',
}


def direct_name(a):
    """Имя прямого адреса: регистр или ячейка внутренней памяти."""
    if a >= 0x80:
        return SFR.get(a, 'SFR_%02X' % a)
    return '%02Xh' % a


def bit_name(b):
    """Имя битового адреса."""
    if b >= 0x80:
        base = b & 0xF8
        return '%s.%d' % (SFR.get(base, 'SFR_%02X' % base), b & 7)
    return '%02Xh.%d' % (0x20 + (b >> 3), b & 7)


class Insn:
    __slots__ = ('addr', 'size', 'text', 'targets', 'kind', 'raw')

    def __init__(self, addr, size, text, targets, kind, raw):
        self.addr = addr      # адрес команды
        self.size = size      # длина в байтах
        self.text = text      # текст (метки подставляются при печати через {L:xxxx})
        self.targets = targets  # адреса переходов/вызовов
        self.kind = kind      # 'seq' | 'jump' | 'cond' | 'call' | 'ret' | 'ijmp'
        self.raw = raw


def decode(d, pc):
    """Разобрать одну команду по адресу pc."""
    op = d[pc]
    b1 = d[pc + 1] if pc + 1 < len(d) else 0
    b2 = d[pc + 2] if pc + 2 < len(d) else 0

    def rel(off, size):
        return (pc + size + (off - 256 if off >= 128 else off)) & 0xFFFF

    def L(a):
        return '{L:%04X}' % a

    lo = op & 0x0F
    hi = op >> 4
    rn = 'R%d' % (op & 7)
    ri = '@R%d' % (op & 1)

    # AJMP / ACALL
    if op & 0x1F == 0x01:
        t = ((pc + 2) & 0xF800) | ((op >> 5) << 8) | b1
        return Insn(pc, 2, 'AJMP  ' + L(t), [t], 'jump', d[pc:pc + 2])
    if op & 0x1F == 0x11:
        t = ((pc + 2) & 0xF800) | ((op >> 5) << 8) | b1
        return Insn(pc, 2, 'ACALL ' + L(t), [t], 'call', d[pc:pc + 2])

    def I(size, text, targets=(), kind='seq'):
        return Insn(pc, size, text, list(targets), kind, d[pc:pc + size])

    a16 = (b1 << 8) | b2
    simple = {
        0x00: 'NOP', 0x03: 'RR    A', 0x04: 'INC   A', 0x13: 'RRC   A', 0x14: 'DEC   A',
        0x23: 'RL    A', 0x33: 'RLC   A', 0x84: 'DIV   AB', 0x93: 'MOVC  A,@A+DPTR',
        0x83: 'MOVC  A,@A+PC', 0xA3: 'INC   DPTR', 0xA4: 'MUL   AB', 0xB3: 'CPL   C',
        0xC3: 'CLR   C', 0xC4: 'SWAP  A', 0xD3: 'SETB  C', 0xD4: 'DA    A', 0xE0: 'MOVX  A,@DPTR',
        0xE4: 'CLR   A', 0xF0: 'MOVX  @DPTR,A', 0xF4: 'CPL   A', 0xA5: 'DB    0A5h',
    }
    if op in simple:
        return I(1, simple[op])
    if op == 0x02:
        return I(3, 'LJMP  ' + L(a16), [a16], 'jump')
    if op == 0x12:
        return I(3, 'LCALL ' + L(a16), [a16], 'call')
    if op == 0x22:
        return I(1, 'RET', kind='ret')
    if op == 0x32:
        return I(1, 'RETI', kind='ret')
    if op == 0x73:
        return I(1, 'JMP   @A+DPTR', kind='ijmp')
    if op == 0x80:
        t = rel(b1, 2)
        return I(2, 'SJMP  ' + L(t), [t], 'jump')
    # условные переходы по биту
    if op in (0x10, 0x20, 0x30):
        t = rel(b2, 3)
        return I(3, '%-5s %s,%s' % ({0x10: 'JBC', 0x20: 'JB', 0x30: 'JNB'}[op], bit_name(b1), L(t)), [t], 'cond')
    if op in (0x40, 0x50, 0x60, 0x70):
        t = rel(b1, 2)
        return I(2, '%-5s %s' % ({0x40: 'JC', 0x50: 'JNC', 0x60: 'JZ', 0x70: 'JNZ'}[op], L(t)), [t], 'cond')
    # арифметика и логика с аккумулятором
    alu = {2: 'ADD', 3: 'ADDC', 4: 'ORL', 5: 'ANL', 6: 'XRL', 9: 'SUBB'}
    if hi in alu and lo >= 4:
        m = alu[hi]
        if lo == 4:
            return I(2, '%-5s A,#%02Xh' % (m, b1))
        if lo == 5:
            return I(2, '%-5s A,%s' % (m, direct_name(b1)))
        if lo in (6, 7):
            return I(1, '%-5s A,%s' % (m, ri))
        return I(1, '%-5s A,%s' % (m, rn))
    if hi in (4, 5, 6) and lo in (2, 3):
        m = {4: 'ORL', 5: 'ANL', 6: 'XRL'}[hi]
        if lo == 2:
            return I(2, '%-5s %s,A' % (m, direct_name(b1)))
        return I(3, '%-5s %s,#%02Xh' % (m, direct_name(b1), b2))
    # INC / DEC
    if hi in (0, 1) and lo >= 5:
        m = 'INC' if hi == 0 else 'DEC'
        if lo == 5:
            return I(2, '%-5s %s' % (m, direct_name(b1)))
        if lo in (6, 7):
            return I(1, '%-5s %s' % (m, ri))
        return I(1, '%-5s %s' % (m, rn))
    # пересылки
    if hi == 7:
        if lo == 2:
            return I(2, 'ORL   C,%s' % bit_name(b1))
        if lo == 4:
            return I(2, 'MOV   A,#%02Xh' % b1)
        if lo == 5:
            return I(3, 'MOV   %s,#%02Xh' % (direct_name(b1), b2))
        if lo in (6, 7):
            return I(2, 'MOV   %s,#%02Xh' % (ri, b1))
        if lo >= 8:
            return I(2, 'MOV   %s,#%02Xh' % (rn, b1))
    if hi == 8:
        if lo == 2:
            return I(2, 'ANL   C,%s' % bit_name(b1))
        if lo == 5:  # в коде сначала источник, потом приёмник
            return I(3, 'MOV   %s,%s' % (direct_name(b2), direct_name(b1)))
        if lo in (6, 7):
            return I(2, 'MOV   %s,%s' % (direct_name(b1), ri))
        if lo >= 8:
            return I(2, 'MOV   %s,%s' % (direct_name(b1), rn))
    if hi == 9:
        if lo == 0:
            return I(3, 'MOV   DPTR,#%04Xh' % a16)
        if lo == 2:
            return I(2, 'MOV   %s,C' % bit_name(b1))
    if hi == 0xA:
        if lo == 0:
            return I(2, 'ORL   C,/%s' % bit_name(b1))
        if lo == 2:
            return I(2, 'MOV   C,%s' % bit_name(b1))
        if lo in (6, 7):
            return I(2, 'MOV   %s,%s' % (ri, direct_name(b1)))
        if lo >= 8:
            return I(2, 'MOV   %s,%s' % (rn, direct_name(b1)))
    if hi == 0xB:
        if lo == 0:
            return I(2, 'ANL   C,/%s' % bit_name(b1))
        if lo == 2:
            return I(2, 'CPL   %s' % bit_name(b1))
        t = rel(b2, 3)
        if lo == 4:
            return I(3, 'CJNE  A,#%02Xh,%s' % (b1, L(t)), [t], 'cond')
        if lo == 5:
            return I(3, 'CJNE  A,%s,%s' % (direct_name(b1), L(t)), [t], 'cond')
        if lo in (6, 7):
            return I(3, 'CJNE  %s,#%02Xh,%s' % (ri, b1, L(t)), [t], 'cond')
        return I(3, 'CJNE  %s,#%02Xh,%s' % (rn, b1, L(t)), [t], 'cond')
    if hi == 0xC:
        if lo == 0:
            return I(2, 'PUSH  %s' % direct_name(b1))
        if lo == 2:
            return I(2, 'CLR   %s' % bit_name(b1))
        if lo == 5:
            return I(2, 'XCH   A,%s' % direct_name(b1))
        if lo in (6, 7):
            return I(1, 'XCH   A,%s' % ri)
        if lo >= 8:
            return I(1, 'XCH   A,%s' % rn)
    if hi == 0xD:
        if lo == 0:
            return I(2, 'POP   %s' % direct_name(b1))
        if lo == 2:
            return I(2, 'SETB  %s' % bit_name(b1))
        if lo == 5:
            t = rel(b2, 3)
            return I(3, 'DJNZ  %s,%s' % (direct_name(b1), L(t)), [t], 'cond')
        if lo in (6, 7):
            return I(1, 'XCHD  A,%s' % ri)
        if lo >= 8:
            t = rel(b1, 2)
            return I(2, 'DJNZ  %s,%s' % (rn, L(t)), [t], 'cond')
    if hi == 0xE:
        if lo in (2, 3):
            return I(1, 'MOVX  A,%s' % ri)
        if lo == 5:
            return I(2, 'MOV   A,%s' % direct_name(b1))
        if lo in (6, 7):
            return I(1, 'MOV   A,%s' % ri)
        if lo >= 8:
            return I(1, 'MOV   A,%s' % rn)
    if hi == 0xF:
        if lo in (2, 3):
            return I(1, 'MOVX  %s,A' % ri)
        if lo == 5:
            return I(2, 'MOV   %s,A' % direct_name(b1))
        if lo in (6, 7):
            return I(1, 'MOV   %s,A' % ri)
        if lo >= 8:
            return I(1, 'MOV   %s,A' % rn)
    if op == 0x92:
        return I(2, 'MOV   %s,C' % bit_name(b1))
    return I(1, 'DB    %02Xh' % op)


class Disasm:
    def __init__(self, data):
        self.d = data
        self.insn = {}                   # адрес -> Insn
        self.owner = {}                  # адрес байта -> адрес команды
        self.xref = defaultdict(list)    # адрес цели -> откуда
        self.calls = set()               # адреса подпрограмм
        self.entries = {}                # адрес входа -> описание
        self.tables = {}                 # адрес таблицы переходов -> число записей

    def trace(self, start):
        """Обход кода от точки входа по всем переходам."""
        stack = [start]
        while stack:
            pc = stack.pop()
            while 0 <= pc < len(self.d):
                if pc in self.insn:
                    break
                if pc in self.owner:      # попали в середину уже разобранной команды
                    break
                ins = decode(self.d, pc)
                if ins.text.startswith('DB'):
                    break
                self.insn[pc] = ins
                for k in range(pc, pc + ins.size):
                    self.owner[k] = pc
                for t in ins.targets:
                    self.xref[t].append(pc)
                    if ins.kind == 'call':
                        self.calls.add(t)
                    stack.append(t)
                if ins.kind == 'ijmp':
                    for t in self.jump_table(pc):
                        stack.append(t)
                if ins.kind in ('jump', 'ret', 'ijmp'):
                    break
                pc += ins.size

    def jump_table(self, pc):
        """Таблица переходов: перед JMP @A+DPTR ищем MOV DPTR,#адрес и читаем подряд идущие переходы."""
        a = pc
        tbl = None
        for _ in range(12):               # смотрим несколько команд назад
            prev = [p for p in (a - 1, a - 2, a - 3) if p in self.insn and p + self.insn[p].size == a]
            if not prev:
                break
            a = prev[0]
            if self.d[a] == 0x90:
                tbl = (self.d[a + 1] << 8) | self.d[a + 2]
                break
        if tbl is None:
            return []
        out = []
        p = tbl
        n = 0
        while p < len(self.d) - 2 and n < 64:
            op = self.d[p]
            if op == 0x02:
                size = 3
            elif op & 0x1F == 0x01 or op == 0x80:
                size = 2
            else:
                break
            if p in self.owner and self.owner[p] != p:
                break
            out.append(p)
            p += size
            n += 1
        if out:
            self.tables[tbl] = n
        return out

    def run(self):
        # точки входа: сброс и занятые векторы
        for v, name in sorted(VECTORS.items()):
            if self.d[v] == 0x02:
                self.entries[v] = 'вектор: ' + name
                self.trace(v)
        return self

    def label(self, a):
        if a in self.entries and a in VECTORS:
            return 'vec_%04X' % a
        if a in self.calls:
            return 'sub_%04X' % a
        return 'loc_%04X' % a

    def render(self, ins):
        t = ins.text
        while '{L:' in t:
            i = t.index('{L:')
            a = int(t[i + 3:i + 7], 16)
            t = t[:i] + self.label(a) + t[i + 8:]
        return t

    def listing(self, out):
        d = self.d
        covered = len(self.owner)
        w = out.write
        w('; Листинг дизассемблера 8051 (C509). Размер образа %d байт.\n' % len(d))
        w('; Разобрано как код: %d байт, команд %d, подпрограмм %d, таблиц переходов %d.\n'
          % (covered, len(self.insn), len(self.calls), len(self.tables)))
        w('; Имена регистров со знаком «?» взяты по памяти и не сверены с документацией.\n;\n')
        w('; Векторы прерываний:\n')
        for v, name in sorted(VECTORS.items()):
            if v in self.entries:
                tgt = self.insn[v].targets[0]
                w(';   %04X  %-32s -> %04X\n' % (v, name, tgt))
        w('\n')
        pc = 0
        while pc < len(d):
            if pc in self.insn:
                ins = self.insn[pc]
                if pc in self.xref or pc in self.entries:
                    if pc in self.calls:
                        w('\n; ---------------- подпрограмма, вызовов: %d ----------------\n'
                          % sum(1 for s in self.xref[pc] if self.insn[s].kind == 'call'))
                    src = ', '.join('%04X' % s for s in sorted(set(self.xref.get(pc, [])))[:8])
                    more = len(set(self.xref.get(pc, []))) - 8
                    note = self.entries.get(pc, '')
                    w('%s:%s%s%s\n' % (self.label(pc),
                                       ('    ; ' + note) if note else '',
                                       ('    ; сюда из: ' + src) if src else '',
                                       (' и ещё %d' % more) if more > 0 else ''))
                w('  %04X  %-9s %s\n' % (pc, ins.raw.hex(), self.render(ins)))
                if ins.kind in ('jump', 'ret', 'ijmp'):
                    w('\n')
                pc += ins.size
            else:
                # данные: собираем до следующей команды, печатаем по 16 байт, повторы сворачиваем
                end = pc
                while end < len(d) and end not in self.insn:
                    end += 1
                chunk = d[pc:end]
                if len(set(chunk)) == 1 and len(chunk) > 16:
                    w('  %04X  ; %d байт %02Xh\n' % (pc, len(chunk), chunk[0]))
                else:
                    for k in range(0, len(chunk), 16):
                        row = chunk[k:k + 16]
                        w('  %04X  DB %s\n' % (pc + k, ' '.join('%02X' % x for x in row)))
                pc = end


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    data = open(sys.argv[1], 'rb').read()
    dis = Disasm(data).run()
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        dis.listing(f)
    print('Разобрано как код: %d байт из %d, команд %d, подпрограмм %d, таблиц переходов %d'
          % (len(dis.owner), len(data), len(dis.insn), len(dis.calls), len(dis.tables)))


if __name__ == '__main__':
    main()
