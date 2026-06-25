#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мини-дизассемблер Hitachi HD6303 (совместим с Motorola 6801/6301, big-endian)
+ инструменты реверса прошивок Nissan ECCS.

КАРТА ПАМЯТИ: CPU-адрес = смещение_в_файле + BASE.
  Z31 (88_Z31turbo32k.bin):  BASE = 0x4000
  M30 (infiniti90m30at.bin): BASE = 0x8000
  Как определить BASE для незнакомой прошивки: см. find_base() ниже.

ИСПОЛЬЗОВАНИЕ (в python3):
  from dis6303 import *
  load("z31/88_Z31turbo32k.bin", base=0x4000)
  dis(0x5600, 20)            # дизассемблировать 20 инструкций с file-адреса 0x5600
  refs(0x7D00)               # где код читает таблицу (file 0x7D00 -> cpu 0xBD00)
  writers(0x13)              # кто пишет RAM-переменную 0x13
  strings()                 # поиск ASCII-строк
  find_base()               # подсказать BASE по гистограмме LDX#
ИЛИ из консоли:
  python3 dis6303.py <bin> <base_hex> dis <start_hex> <count>
  python3 dis6303.py <bin> <base_hex> refs <table_file_addr_hex>
"""
import sys
from collections import Counter

D = b""      # содержимое прошивки
BASE = 0x4000
CODE_LO, CODE_HI = 0x0000, 0x8000  # диапазон, где искать код (уточняется)

def load(path, base=0x4000, code=(0x0000, 0x8000)):
    global D, BASE, CODE_LO, CODE_HI
    D = open(path, "rb").read()
    BASE = base
    CODE_LO, CODE_HI = code
    return len(D)

# --- таблицы опкодов 6801/6303 ---
LO = {0: "SUB", 1: "CMP", 2: "SBC", 4: "AND", 5: "BIT", 6: "LDA", 7: "STA",
      8: "EOR", 9: "ADC", 0xA: "ORA", 0xB: "ADD"}
INH = {0x01: "NOP", 0x04: "LSRD", 0x05: "ASLD", 0x06: "TAP", 0x07: "TPA",
       0x08: "INX", 0x09: "DEX", 0x0A: "CLV", 0x0B: "SEV", 0x0C: "CLC",
       0x0D: "SEC", 0x0E: "CLI", 0x0F: "SEI", 0x10: "SBA", 0x11: "CBA",
       0x16: "TAB", 0x17: "TBA", 0x19: "DAA", 0x1B: "ABA",
       0x30: "TSX", 0x31: "INS", 0x32: "PULA", 0x33: "PULB", 0x34: "DES",
       0x35: "TXS", 0x36: "PSHA", 0x37: "PSHB", 0x38: "PULX", 0x39: "RTS",
       0x3A: "ABX", 0x3B: "RTI", 0x3C: "PSHX", 0x3D: "MUL", 0x3E: "WAI",
       0x3F: "SWI", 0x40: "NEGA", 0x43: "COMA", 0x44: "LSRA", 0x46: "RORA",
       0x47: "ASRA", 0x48: "ASLA", 0x49: "ROLA", 0x4A: "DECA", 0x4C: "INCA",
       0x4D: "TSTA", 0x4F: "CLRA", 0x50: "NEGB", 0x53: "COMB", 0x54: "LSRB",
       0x56: "RORB", 0x57: "ASRB", 0x58: "ASLB", 0x59: "ROLB", 0x5A: "DECB",
       0x5C: "INCB", 0x5D: "TSTB", 0x5F: "CLRB"}
BR = {0x20: "BRA", 0x21: "BRN", 0x22: "BHI", 0x23: "BLS", 0x24: "BCC",
      0x25: "BCS", 0x26: "BNE", 0x27: "BEQ", 0x28: "BVC", 0x29: "BVS",
      0x2A: "BPL", 0x2B: "BMI", 0x2C: "BGE", 0x2D: "BLT", 0x2E: "BGT",
      0x2F: "BLE", 0x8D: "BSR"}
MEM = {0x0: "NEG", 0x3: "COM", 0x4: "LSR", 0x6: "ROR", 0x7: "ASR", 0x8: "ASL",
       0x9: "ROL", 0xA: "DEC", 0xC: "INC", 0xD: "TST", 0xE: "JMP", 0xF: "CLR"}

def _cpu(f): return f + BASE

def dis(start, n):
    """Дизассемблировать n инструкций с file-адреса start."""
    d = D; i = start
    for _ in range(n):
        b = d[i]; h = b >> 4; l = b & 0xF
        s = "0x%04X(cpu%04X): %02X " % (i, _cpu(i), b)
        if b in INH:
            print(s + "        " + INH[b]); i += 1; continue
        if b in BR:
            rel = d[i+1]; tgt = i+2 + (rel-256 if rel > 127 else rel)
            print(s + "%02X     %s 0x%04X" % (d[i+1], BR[b], tgt)); i += 2; continue
        if 0x60 <= b <= 0x6F and l in MEM:
            print(s + "%02X     %s %d,X" % (d[i+1], MEM[l], d[i+1])); i += 2; continue
        if 0x70 <= b <= 0x7F and l in MEM:
            a = (d[i+1] << 8) | d[i+2]
            print(s + "%02X %02X  %s $%04X" % (d[i+1], d[i+2], MEM[l], a)); i += 3; continue
        if h >= 8:
            acc = "A" if h < 0xC else "B"; mode = (h - 8) % 4  # 0=IMM,1=DIR,2=IDX,3=EXT
            if l in (0xC, 0xE, 0xF):  # 16-битные: CPX/LDD, LDS/LDX, STS/STX
                nm = {0xC: ("LDD" if acc == "B" else "CPX"),
                      0xE: ("LDX" if acc == "B" else "LDS"),
                      0xF: ("STX" if acc == "B" else "STS")}[l]
                if l != 0xF and mode == 0:
                    a = (d[i+1] << 8) | d[i+2]
                    print(s + "%02X %02X  %s #$%04X" % (d[i+1], d[i+2], nm, a)); i += 3; continue
                if mode == 1:
                    print(s + "%02X     %s $%02X" % (d[i+1], nm, d[i+1])); i += 2; continue
                if mode == 2:
                    print(s + "%02X     %s %d,X" % (d[i+1], nm, d[i+1])); i += 2; continue
                a = (d[i+1] << 8) | d[i+2]
                print(s + "%02X %02X  %s $%04X" % (d[i+1], d[i+2], nm, a)); i += 3; continue
            if l == 0xD:  # BSR/JSR(A) / STD(B)
                nm = "JSR" if acc == "A" else "STD"
                if mode == 1:
                    print(s + "%02X     %s $%02X" % (d[i+1], nm, d[i+1])); i += 2; continue
                if mode == 2:
                    print(s + "%02X     %s %d,X" % (d[i+1], nm, d[i+1])); i += 2; continue
                a = (d[i+1] << 8) | d[i+2]
                print(s + "%02X %02X  %s $%04X" % (d[i+1], d[i+2], nm, a)); i += 3; continue
            if l in LO:
                nm = LO[l] + acc
                if mode == 0:
                    print(s + "%02X     %s #$%02X" % (d[i+1], nm, d[i+1])); i += 2; continue
                if mode == 1:
                    print(s + "%02X     %s $%02X" % (d[i+1], nm, d[i+1])); i += 2; continue
                if mode == 2:
                    print(s + "%02X     %s %d,X" % (d[i+1], nm, d[i+1])); i += 2; continue
                a = (d[i+1] << 8) | d[i+2]
                print(s + "%02X %02X  %s $%04X" % (d[i+1], d[i+2], nm, a)); i += 3; continue
        print(s + "        ??? (6301-доп/данные?)"); i += 1

OPN = {0xCE: "LDX#", 0xB6: "LDAA", 0xF6: "LDAB", 0xFE: "LDX", 0xBD: "JSR",
       0xDF: "STX", 0xB7: "STAA", 0xF7: "STAB", 0x96: "LDAA.d", 0xD6: "LDAB.d"}

def refs(table_file_addr):
    """Найти, где код ЧИТАЕТ таблицу (по её 16-бит CPU-адресу как операнду)."""
    cpu = _cpu(table_file_addr); hi, lo = cpu >> 8, cpu & 0xFF
    hits = [i for i in range(CODE_LO, CODE_HI - 1)
            if D[i] == hi and D[i+1] == lo]
    print("table file 0x%04X -> cpu 0x%04X : %d ссылок" % (table_file_addr, cpu, len(hits)))
    for h in hits:
        op = OPN.get(D[h-1], "%02X" % D[h-1])
        print("   0x%04X  [пред.опкод %s]" % (h, op))
    return hits

def writers(var):
    """Найти, кто ПИШЕТ zero-page RAM-переменную var (STAA/STAB direct)."""
    hits = [i for i in range(CODE_LO, CODE_HI - 1)
            if D[i] in (0x97, 0xD7) and D[i+1] == var]
    print("RAM 0x%02X : %d записей" % (var, len(hits)))
    for h in hits:
        print("  -- запись на 0x%04X --" % h); dis(max(CODE_LO, h-9), 6)
    return hits

def find_base():
    """Подсказать BASE: гистограмма старших байтов адресов в LDX# (CE)."""
    vals = []
    for i in range(len(D) - 2):
        if D[i] == 0xCE:
            vals.append((D[i+1] << 8) | D[i+2])
    hi = Counter(v >> 8 for v in vals)
    print("Гистограмма старших байтов LDX#-адресов (где густо — там таблицы):")
    for h, c in sorted(hi.items()):
        if c >= 3:
            print("  0x%02Xxx : %d" % (h, c))
    print("Данные в файле обычно в 0x7xxx. Если адреса густо в 0xBxxx -> BASE=0x4000;")
    print("если в 0xFxxx -> BASE=0x8000.")

def strings(minlen=4):
    """ASCII-строки (для поиска версии/номера; в старых ЭБУ часто пусто)."""
    d = D; i = 0
    while i < len(d):
        if 0x20 <= d[i] <= 0x7E:
            j = i
            while j < len(d) and 0x20 <= d[j] <= 0x7E: j += 1
            if j - i >= minlen:
                s = d[i:j].decode("ascii")
                if any(c.isalnum() for c in s):
                    print("  0x%05X: %r" % (i, s))
            i = j
        else:
            i += 1

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(0)
    load(sys.argv[1], base=int(sys.argv[2], 16))
    cmd = sys.argv[3]
    if cmd == "dis":
        dis(int(sys.argv[4], 16), int(sys.argv[5]))
    elif cmd == "refs":
        refs(int(sys.argv[4], 16))
    elif cmd == "writers":
        writers(int(sys.argv[4], 16))
    elif cmd == "base":
        find_base()
    elif cmd == "strings":
        strings()
