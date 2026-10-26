#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Патч j7es v0.7.5 (Январь 7.2, C509) под 6 цилиндров: VG30, порядок 1-2-3-4-5-6,
попарная искра (1-4, 2-5, 3-6), попарный впрыск, без датчика фаз.
Схема и все адреса — в «j7es — разбор под 6 цилиндров 03.10.26 ИИ.txt», п.4–5.

Раскладка такта: 20 зубьев (120°), ВМТ на зубе 4 такта, загрузка искры на зубе 8,
чтение детонации на зубе 6. Счётчик тактов 40h = 0..5 (720°).
Индекс пары 77h = (40h + 2) mod 3 — для записей искры, детонации и отката.
Номер пары для слотов накопления: 95h (слот A), 96h (слот B), через @R1.

Подключение (по умолчанию):
  форсунки  CM0 (P4.0) — пара 1-4, CM1 (P4.1) — 2-5, CM2 (P4.2) — 3-6;
  катушки   CM4 (P4.4) — пара 1-4, CM5 (P4.5) — 2-5, CM6 (P4.6) — 3-6.

Калибровка Z — байт по адресу E7FF: номер зуба под датчиком в ВМТ 1-го цилиндра,
считая от первого зуба после пропуска (он 0), 0..59. Прошивка читает его сама.

Запуск:
  собрать из стока:      python3 "патч j7es 6 цилиндров 03.10.26 ИИ.py" j7es_v0.7.5.bin --z 9
  сменить Z в готовом:   python3 "патч j7es 6 цилиндров 03.10.26 ИИ.py" готовый.bin --set-z 18
(при смене Z пересчитывается контрольная сумма в конце образа)
"""
import argparse
import datetime
import os
import sys

ORG = 0xE800            # новый код — в свободном флеше E7AE–F3FF (выше F3FF нельзя: нет копии в ОЗУ)
LIMIT = 0xF400
ZCAL = 0xE7FF           # калибровка Z — зуб ВМТ 1-го цилиндра

IDX = 0x77              # индекс пары (нижнее ОЗУ, прямой доступ)
SLOT_A, SLOT_B = 0x95, 0x96   # пара слота A / B (верхнее ОЗУ, только @R1)

# адреса регистров
B, ACC, CMEN = 0xF0, 0xE0, 0xF6
CM_PAIR = [  # пара -> (младший CM, старший CM, маска CMEN, бит P4)
    (0xE4, 0xE5, 0x10, 0xEC),   # CM4, P4.4
    (0xE6, 0xE7, 0x20, 0xED),   # CM5, P4.5
    (0xF2, 0xF3, 0x40, 0xEE),   # CM6, P4.6
]
BIT_26_6 = (0x26 - 0x20) * 8 + 6
BIT_ACC0 = 0xE0


class Asm:
    """Мини-ассемблер 8051: только нужные команды, метки и переходы."""

    def __init__(self, org):
        self.org = org
        self.b = bytearray()
        self.lab = {}
        self.fix = []           # (позиция, метка, вид)

    @property
    def pc(self):
        return self.org + len(self.b)

    def label(self, name):
        assert name not in self.lab, name
        self.lab[name] = self.pc

    def e(self, *xs):
        self.b += bytes(x & 0xFF for x in xs)

    def rel(self, op_bytes, name):
        self.e(*op_bytes)
        self.fix.append((len(self.b), name, 'rel'))
        self.e(0)

    def abs16(self, op, target):
        self.e(op)
        if isinstance(target, str):
            self.fix.append((len(self.b), target, 'abs'))
            self.e(0, 0)
        else:
            self.e(target >> 8, target)

    # команды
    def mov_a_dir(self, d): self.e(0xE5, d)
    def mov_dir_a(self, d): self.e(0xF5, d)
    def mov_dir_imm(self, d, i): self.e(0x75, d, i)
    def mov_dir_dir(self, dst, src): self.e(0x85, src, dst)
    def mov_dir_rn(self, d, n): self.e(0x88 + n, d)
    def mov_rn_imm(self, n, i): self.e(0x78 + n, i)
    def mov_a_imm(self, i): self.e(0x74, i)
    def mov_a_ri(self, i): self.e(0xE6 + i)
    def mov_ri_imm(self, i, v): self.e(0x76 + i, v)
    def mov_ri_dir(self, i, d): self.e(0xA6 + i, d)
    def mov_a_rn(self, n): self.e(0xE8 + n)
    def mov_rn_a(self, n): self.e(0xF8 + n)
    def mov_rn_dir(self, n, d): self.e(0xA8 + n, d)
    def mov_dptr(self, v): self.e(0x90, v >> 8, v)
    def movc_dptr(self): self.e(0x93)
    def rr_a(self): self.e(0x03)
    def mul_ab(self): self.e(0xA4)
    def add_a_rn(self, n): self.e(0x28 + n)
    def subb_a_imm(self, i): self.e(0x94, i)
    def xrl_a_rn(self, n): self.e(0x68 + n)
    def inc_a(self): self.e(0x04)
    def inc_rn(self, n): self.e(0x08 + n)
    def clr_a(self): self.e(0xE4)
    def clr_c(self): self.e(0xC3)
    def add_a_imm(self, i): self.e(0x24, i)
    def subb_a_dir(self, d): self.e(0x95, d)
    def div_ab(self): self.e(0x84)
    def anl_dir_imm(self, d, i): self.e(0x53, d, i)
    def orl_dir_imm(self, d, i): self.e(0x43, d, i)
    def setb(self, bit): self.e(0xD2, bit)
    def clr(self, bit): self.e(0xC2, bit)
    def push(self, d): self.e(0xC0, d)
    def pop(self, d): self.e(0xD0, d)
    def ret(self): self.e(0x22)
    def ljmp(self, t): self.abs16(0x02, t)
    def lcall(self, t): self.abs16(0x12, t)
    def sjmp(self, n): self.rel((0x80,), n)
    def jz(self, n): self.rel((0x60,), n)
    def jnz(self, n): self.rel((0x70,), n)
    def jnc(self, n): self.rel((0x50,), n)
    def jc(self, n): self.rel((0x40,), n)
    def jnb(self, bit, n): self.rel((0x30, bit), n)
    def cjne_a_imm(self, i, n): self.rel((0xB4, i), n)
    def cjne_rn_imm(self, r, i, n): self.rel((0xB8 + r, i), n)

    def link(self):
        for pos, name, kind in self.fix:
            t = self.lab[name]
            if kind == 'rel':
                off = t - (self.org + pos + 1)
                assert -128 <= off <= 127, (name, off)
                self.b[pos] = off & 0xFF
            else:
                self.b[pos] = t >> 8
                self.b[pos + 1] = t & 0xFF
        return bytes(self.b)


def build(code, z):
    d = bytearray(code)

    def put(addr, old, new):
        """Правка на месте с проверкой исходных байтов."""
        old = bytes(old)
        new = bytes(new)
        cur = bytes(d[addr:addr + len(old)])
        if cur != old:
            sys.exit('по адресу %04X ожидалось %s, а там %s' % (addr, old.hex(), cur.hex()))
        d[addr:addr + len(new)] = new

    a = Asm(ORG)

    # --- таблица масок форсунок по 41h = 0..5: CM0 / CM1 / CM2 ---
    a.label('inj_tbl')
    a.e(0x01, 0x02, 0x04, 0x01, 0x02, 0x04)

    # --- BASE (основной цикл, @3E70): R3 = база записи j = (Z − 1 + 20j) mod 60,
    #     на выходе A = R0 − 80h, как в стоке. j = (R0 − 80h) / 4; 4-я запись — вхолостую ---
    a.label('base')
    a.mov_dptr(ZCAL)
    a.clr_a()
    a.movc_dptr()
    a.mov_rn_a(3)                               # R3 = Z
    a.mov_a_rn(0)
    a.clr_c()
    a.subb_a_imm(0x80)
    a.rr_a()
    a.rr_a()                                    # A = j
    a.mov_dir_imm(B, 20)
    a.mul_ab()                                  # A = 20j
    a.add_a_rn(3)
    a.add_a_imm(59)                             # + Z − 1 (−1 = +59 по модулю 60)
    a.label('base_mod')
    a.cjne_a_imm(60, 'base_cmp')
    a.label('base_cmp')
    a.jc('base_ok')
    a.subb_a_imm(60)                            # C = 0 после JC
    a.sjmp('base_mod')
    a.label('base_ok')
    a.mov_rn_a(3)
    a.mov_a_rn(0)
    a.clr_c()
    a.subb_a_imm(0x80)
    a.ret()

    # --- ADV: следующий зуб — R7 + 1, на 20 новый такт, 40h + 1 mod 6 ---
    a.label('adv')
    a.inc_rn(7)
    a.cjne_rn_imm(7, 20, 'adv_done')
    a.mov_rn_imm(7, 0)
    a.mov_a_dir(0x40)
    a.inc_a()
    a.cjne_a_imm(6, 'adv_set')
    a.clr_a()
    a.setb(BIT_26_6)                            # флаг цикла 720°
    a.label('adv_set')
    a.mov_dir_a(0x40)
    a.label('adv_done')
    a.ljmp(0x02B9)

    # --- SYNC0: зуб 0 (R6 уже 0). Из Z: (4 − Z) mod 60 = 20·j0 + r7_0,
    #     R7 = r7_0, такт зуба 0 — пара j0. DPTR обработчика сохраняется ---
    a.label('sync0')
    a.push(0x82)
    a.push(0x83)
    a.mov_dptr(ZCAL)
    a.clr_a()
    a.movc_dptr()                               # A = Z
    a.pop(0x83)
    a.pop(0x82)
    a.mov_dir_a(B)
    a.mov_a_imm(64)
    a.clr_c()
    a.subb_a_dir(B)                             # 64 − Z = 5..64
    a.cjne_a_imm(60, 's0_c')
    a.label('s0_c')
    a.jc('s0_m')
    a.subb_a_imm(60)                            # C = 0 после JC → (4 − Z) mod 60
    a.label('s0_m')
    a.mov_dir_imm(B, 20)
    a.div_ab()                                  # A = j0, B = r7_0
    a.mov_rn_a(1)                               # R1 = j0 (R0:R1 здесь временные)
    a.mov_a_dir(B)
    a.mov_rn_a(7)                               # R7 = r7_0
    a.jnz('s0_chk')
    a.mov_a_dir(0x40)                           # граница такта на зубе 0 — новый такт
    a.inc_a()
    a.cjne_a_imm(6, 's0_inc')
    a.clr_a()
    a.setb(BIT_26_6)
    a.label('s0_inc')
    a.mov_dir_a(0x40)
    a.label('s0_chk')
    a.mov_a_dir(0x40)
    a.cjne_a_imm(6, 's0_lt')
    a.label('s0_lt')
    a.jnc('s0_fix')                             # 40h ≥ 6 — привести
    a.mov_dir_imm(B, 3)
    a.div_ab()
    a.mov_a_dir(B)                              # 40h mod 3
    a.xrl_a_rn(1)
    a.jz('s0_done')
    a.label('s0_fix')
    a.mov_dir_rn(0x40, 1)                       # 40h = j0
    a.label('s0_done')
    a.ljmp(0x02B9)

    # --- INJ41: 41h = (40h − 3Dh) mod 6 ---
    a.label('inj41')
    a.mov_a_dir(0x40)
    a.clr_c()
    a.subb_a_dir(0x3D)
    a.jnc('i41_ok')
    a.add_a_imm(6)
    a.label('i41_ok')
    a.mov_dir_a(0x41)
    a.ret()

    # --- IDX (зуб 8): 43h = 40h; 77h = (40h + 2) mod 3; пара — в байт слота ---
    a.label('idx')
    a.mov_dir_dir(0x43, 0x40)
    a.mov_a_dir(0x40)
    a.add_a_imm(2)
    a.mov_dir_imm(B, 3)
    a.div_ab()
    a.mov_dir_dir(IDX, B)
    a.mov_rn_imm(1, SLOT_B)                     # чётный такт — слот B (14h–17h)
    a.mov_a_dir(0x43)
    a.jnb(BIT_ACC0, 'idx_st')
    a.mov_rn_imm(1, SLOT_A)                     # нечётный — слот A (10h–13h)
    a.label('idx_st')
    a.mov_ri_dir(1, IDX)
    a.ret()

    # --- выходы зажигания: A = старший, R0 = младший байт времени совпадения ---
    def out(name, slot, dwell, back):
        a.label(name)
        a.mov_dir_a(B)                          # старший байт — в B
        a.mov_rn_imm(1, slot)
        a.mov_a_ri(1)                           # пара 0..2
        for p, (cml, cmh, msk, pbit) in enumerate(CM_PAIR):
            nxt = '%s_n%d' % (name, p)
            if p < 2:
                a.cjne_a_imm(p, nxt)
            a.anl_dir_imm(CMEN, (~msk) & 0xFF)
            a.mov_dir_dir(cmh, B)
            a.mov_dir_rn(cml, 0)                # запись младшего — перенос в защёлку
            a.orl_dir_imm(CMEN, msk)
            if dwell:
                a.mov_a_dir(0x68)               # 68h = 0 — такт без искры (отсечка)
                a.jz(name + '_end')
                a.clr(pbit)                     # на совпадении — 0: начало накопления
            else:
                a.setb(pbit)                    # на совпадении — 1: искра
            a.sjmp(name + '_end')
            if p < 2:
                a.label(nxt)
        a.label(name + '_end')
        a.ljmp(back)

    out('dwa', SLOT_A, True, 0x04F7)
    out('spa', SLOT_A, False, 0x0546)
    out('dwb', SLOT_B, True, 0x05C5)
    out('spb', SLOT_B, False, 0x0614)

    # --- STOPFIX: при остановке слоту A — запись 1 (пара 1), слоту B — запись 0 (пара 0) ---
    a.label('stopfix')
    a.mov_a_rn(0)
    a.push(ACC)
    a.mov_rn_imm(0, SLOT_A)
    a.mov_ri_imm(0, 1)
    a.mov_rn_imm(0, SLOT_B)
    a.mov_ri_imm(0, 0)
    a.pop(ACC)
    a.mov_rn_a(0)
    a.ljmp(0x3BE4)

    blob = a.link()
    if ORG + len(blob) > LIMIT:
        sys.exit('новый код не влез в E7AE–F3FF')
    if any(d[ORG:ORG + len(blob)]):
        sys.exit('место под новый код занято')
    d[ORG:ORG + len(blob)] = blob
    L = a.lab

    def jmp(t):
        return [0x02, L[t] >> 8, L[t] & 0xFF]

    def call(t):
        return [0x12, L[t] >> 8, L[t] & 0xFF]

    # 1. Счёт зубьев и тактов
    put(0x0278, [0xBE, 0x1E, 0x09], jmp('adv'))                       # обычный зуб (после INC R6)
    put(0x026C, [0x7F, 0x1B, 0x02, 0x02, 0xB9], jmp('adv') + [0, 0])  # зуб 57
    put(0x00F2, [0x7F, 0x1C, 0x02, 0x02, 0xB9], jmp('adv') + [0, 0])  # досчитанный 58
    put(0x0100, [0x7F, 0x1D, 0x02, 0x02, 0xB9], jmp('adv') + [0, 0])  # досчитанный 59
    put(0x0291, [0x7F, 0x00, 0x30], jmp('sync0'))                     # зуб 0
    # 2. Ловушка перезапуска и фаза впрыска
    put(0x3D47, [0x04], [0x06])
    put(0x3D4E, [0x1E], [0x14])
    put(0x3D74, [0x3C], [0x78])
    put(0x3D7E, [0x0B], [0x0F])
    put(0x3D8D, [0xB2, 0xE1], [0x00, 0x00])
    put(0x3D91, [0x1E], [0x14])
    put(0x3DCA, [0x1E], [0x14])
    put(0x3DCC, [0xB2, 0xE1], [0x00, 0x00])
    # 3. Окно детонации
    for addr in (0x21C5, 0x21D9):
        put(addr, [0x1E], [0x14])
    for addr in (0x21CA, 0x21DE):
        put(addr, [0x1D], [0x13])
    for addr in (0x21CE, 0x21E2):
        put(addr, [0x0B], [0x0F])
    for addr in (0x21D2, 0x21E6):
        put(addr, [0x1E], [0x14])
    # 4. Канал форсунок по такту
    put(0x0365, [0xE5, 0x40, 0xC3, 0x95, 0x3D, 0x54, 0x03, 0xF5, 0x41],
        call('inj41') + [0] * 6)
    put(0x1626, [0xE5, 0x41, 0xA2, 0x50, 0x92, 0xE2, 0x90, 0xA5, 0x58],
        [0xE5, 0x41, 0x90, L['inj_tbl'] >> 8, L['inj_tbl'] & 0xFF, 0, 0, 0, 0])
    # 5. Индекс пары: зуб 8, записи искры, детонация
    put(0x03BF, [0x85, 0x40, 0x43], call('idx'))
    put(0x03D1, [0xE5, 0x43, 0xB2, 0xE1], [0xE5, IDX, 0x00, 0x00])
    for addr in (0x0947, 0x0966, 0x0998, 0x09C5, 0x0A67):
        put(addr, [0xE5, 0x43], [0xE5, IDX])
    put(0x0AB2, [0xA9, 0x43], [0xA9, IDX])
    # 6. Базы искры — из калибровки Z
    put(0x3E70, [0x7B, 0x2F, 0xE8, 0xC3, 0x94, 0x80, 0x30, 0xE2, 0x02, 0x7B, 0x11],
        call('base') + [0] * 8)
    # 7. Выходы зажигания по паре слота
    put(0x04A6, [0x20, 0x0D, 0x2C], jmp('dwa'))
    put(0x052E, [0x53, 0xF6, 0xEF], jmp('spa'))
    put(0x0574, [0x20, 0x0D, 0x2C], jmp('dwb'))
    put(0x05FC, [0x53, 0xF6, 0xBF], jmp('spb'))
    put(0x2FD6, [0x02, 0x3B, 0xE4], jmp('stopfix'))
    # 8. Обороты, передача, отсечка, датчик фаз
    put(0x2313, [0x40], [0x2B])
    put(0x2316, [0x42], [0x2C])
    put(0x2319, [0x0F], [0x0A])
    put(0x02C4, [0xEF], [0xEE])
    put(0x03AE, [0x03], [0x02])                 # SUBB A,#03h @03AD — байт числа в 03AE
    put(0x6051, [0x34], [0x14])
    # 9. Калибровка Z
    put(ZCAL, [0x00], [z])
    if any(d[0xFFF8:0xFFFA]):
        sys.exit('FFF8–FFF9 не пустые')
    cs = fix_sum(d)
    info = dict(size=len(blob), labels=L, cs=cs)
    return bytes(d), info


def fix_sum(d):
    """Контрольная сумма: слово в FFFE–FFFF = сумма всех байт образа.
    Слово v = 256·hi + lo, поэтому сумма остальных байт должна быть 255·hi (mod 65536).
    Добираем её двумя байтами-компенсаторами в FFF8–FFF9 (прошивкой не читаются)."""
    d[0xFFF8] = d[0xFFF9] = 0
    s0 = sum(d[:0xFFFE]) & 0xFFFF
    for hi in range(256):
        c = (255 * hi - s0) & 0xFFFF
        if c <= 510:
            break
    else:
        sys.exit('не подобрать компенсатор контрольной суммы')
    d[0xFFF8], d[0xFFF9] = min(c, 255), c - min(c, 255)
    s1 = sum(d[:0xFFFE])
    cs = next(v for v in range(65536) if (s1 + (v & 0xFF) + (v >> 8)) & 0xFFFF == v)
    d[0xFFFE], d[0xFFFF] = cs & 0xFF, cs >> 8
    assert sum(d) & 0xFFFF == cs
    return cs


def describe(z):
    b = (z - 4) % 20
    return ('Z = %d: ВМТ на зубьях %s, границы тактов %s, на зубе 0 зуб такта %d, пара %d'
            % (z, ', '.join(str((z + 20 * j) % 60) for j in range(3)),
               ', '.join(str((b + 20 * j) % 60) for j in range(3)), (4 - z) % 20, ((4 - z) % 60) // 20))


def main():
    ap = argparse.ArgumentParser(description='Патч j7es под 6 цилиндров')
    ap.add_argument('bin')
    ap.add_argument('--z', type=int, help='собрать из стока с этим Z (0..59)')
    ap.add_argument('--set-z', type=int, help='сменить Z в уже собранном .bin (0..59)')
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    code = open(a.bin, 'rb').read()
    if len(code) != 65536:
        sys.exit('ожидается образ 65536 байт')
    z = a.z if a.z is not None else a.set_z
    if z is None or (a.z is not None and a.set_z is not None):
        sys.exit('нужен один из ключей: --z (сборка из стока) или --set-z (смена Z)')
    if not 0 <= z < 60:
        sys.exit('Z от 0 до 59')
    if a.set_z is not None:
        d = bytearray(code)
        if d[0x0278] != 0x02 or d[0x0279] != 0xE8:
            sys.exit('это не патч v1 (в 0278 нет перехода на E8xx)')
        old = d[ZCAL]
        d[ZCAL] = z
        cs = fix_sum(d)
        out = bytes(d)
        print('Z: %d → %d, контрольная сумма %04X' % (old, z, cs))
    else:
        out, info = build(code, z)
        cs = info['cs']
        print('Новый код %d байт с %04X, Z по адресу %04X, контрольная сумма %04X'
              % (info['size'], ORG, ZCAL, cs))
        for k, v in sorted(info['labels'].items(), key=lambda x: x[1]):
            print('  %04X %s' % (v, k))
    name = a.out or 'j7es_v1_6цил-попарно-ВМТ%d_%s ИИ.bin' % (
        z, datetime.datetime.now().strftime('%d.%m.%y_%H%M'))
    path = os.path.join(os.path.dirname(os.path.abspath(a.bin)), name)
    if os.path.abspath(path) == os.path.abspath(a.bin):
        sys.exit('имя результата совпадает с исходным файлом')
    open(path, 'wb').write(out)
    print('Записан:', path)
    print(describe(z))


if __name__ == '__main__':
    main()
