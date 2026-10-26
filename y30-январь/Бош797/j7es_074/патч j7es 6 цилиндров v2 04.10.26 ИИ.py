#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Прошивка v2: j7es v0.7.5 (Январь 7.2, C509) под 6 цилиндров VG30 (порядок 1-2-3-4-5-6).
Внутри всё по 6 цилиндрам; режимы и проводка — калибровкой, без переписывания кода.

Угловое ядро — как в v1 (такт 20 зубьев, ВМТ на зубе 4 такта, такт 40h = 0..5, Z в E7FF).
Цилиндр c = 0..5 — цилиндр c+1 (ВМТ на зубе Z + 20c, c и c+3 — пара).

КАЛИБРОВКА (флеш, ниже F400):
  E7F0  с v7 не используется. Датчик фаз включается штатным флагом 6051.5 «Датчик фаз»;
        при исправном сигнале фазы — впрыск фазированно и искра поцилиндрово, иначе блок сам попарно.
        (v2–v6: режим — бит0 фаз. впрыск, бит1 поцилиндровая искра, бит2 датчик фаз.)
  E7F1  ФАЗА: уровень P1.2 на зубе 0, при котором такт зуба 0 — такт цилиндра j0 (иначе j0+3).
  E7F2  К5/К6: бит0 = 1 — катушка заряжается высоким уровнем (покой — низкий), 0 — наоборот.
  E7F3–E7F8  ФОРСУНКИ: для цилиндра c — маска выходов (бит0 Ф1 … бит5 Ф6).
  E7F9–E7FE  КАТУШКИ: для цилиндра c — номер выхода 0..5 (К1 … К6).
  E7FF  Z — зуб ВМТ 1-го цилиндра от первого зуба после пропуска (0..59).
  E7EF  ЗУБ ОПРОСА ДФ (с v6): 0 — датчик фаз читается на зубе 0 (как в стоке); 1..59 — уровень снимается на этом
        зубе (до пропуска, т.е. в предыдущем обороте) и берётся на зубе 0; нет свежего замера — фаза не подтверждена.
По умолчанию: цилиндр N → форсунка ФN и катушка КN (с 19.10.26; раньше было по v1 — пары на Ф1–Ф3 и К1–К3).
Датчик фаз — штатный флаг 6051.5 (с v7; в v2–v6 был бит E7F0.2, а 6051.5 сборщик выключал).

ВЫХОДЫ:
  Ф1–Ф4 = CM0–CM3 (P4.0–P4.3, ноги 64,65,66,68), открыта = 0 (штатные каналы).
  Ф5 = CC4 / P1.4 (нога 1), Ф6 = CRC / P1.0 (нога 9), открыта = 1 (затворы ключей DA11 / DA12).
  К1–К4 = CM4–CM7 (P4.4–P4.7, ноги 69–72), зарядка = 0 (штатные каналы).
  К5 = P5.6 (нога 38), К6 = P5.7 (нога 37) через COMSET / COMCLR, полярность — E7F2.
  (P5.6 / P5.7 на плате — SCL / SDA EEPROM 24C04, на разъём не выведены; j7es EEPROM не использует.
   P5.2 не взят: на нём j7es выдаёт свой ШИМ из таймера 1, @08B2–08CA.)
  P5.1 — сигнал расхода топлива, как в стоке (порции по [60FE/60FF]); гасится не COMCLR (он у катушек),
  а таймером 1: счётчик в B6h, ширина импульса 1–2 мс вместо 0.89 мс.
  SPI микросхемы детонации (P1.0 / P1.1 / P1.7) выключен — P1.0 занят Ф6.
  Расчёт детонации в INT0 (0909–0AE5: уровень, шум, флаги, откат, SPI) пропущен — откат и так 0 (63D3),
  а INT0 не успевал на высоких оборотах; замер АЦП ДД в обработчике зуба (0453) остался.
  На старте (DF53, до копирования в ОЗУ ~0.3 с) сразу: Ф5 / Ф6 закрыты (P1.4 / P1.0 = 0), К5 / К6 в покое.

Запуск (имя бина — по правилу версий: j7es_v<код>.<дочерняя>_<что нового>_<дата>_<время> ИИ.bin):
  python3 "патч j7es 6 цилиндров v2 04.10.26 ИИ.py" j7es_v0.7.5.bin --z 9            → j7es_v3.0_…
  … --z 17 --child 1 --what зуб-ВМТ-под-колесо                                         → j7es_v3.1_…
Версия кода — CODE_VER / CODE_WHAT ниже (менять только при правке кода).
"""
import argparse
import datetime
import os
import sys

# версия КОДА: меняется только при правке кода/врезок; калибровочные сборки — дочерние (--child M --what …)
CODE_VER = 7
CODE_WHAT = 'штатные-режимы-стока-на-6-цилиндров-фаза-впрыска'

ORG = 0xE800
LIMIT = 0xF400
CFG = 0xE7F0
MODE, PHPOL, P5POL = CFG, CFG + 1, CFG + 2
INJMAP, COILMAP, ZCAL = CFG + 3, CFG + 9, 0xE7FF
PHT_CAL = 0xE7EF                   # зуб опроса ДФ (0 — на зубе 0, как в стоке)
PHLAT = 0x94                       # замер ДФ на зубе опроса: бит0 уровень, бит7 «свежий» (верхнее ОЗУ, @R)
PHT = 0xB7                         # копия PHT_CAL в ОЗУ (обработчик зуба не трогает DPTR)

IDX = 0x77                         # индекс пары (нижнее ОЗУ)
SLOT_A, SLOT_B = 0x95, 0x96        # цилиндр слота A / B (верхнее ОЗУ, через @R)
PH_LAST, COPF, PH_GOOD = 0x97, 0x98, 0x99
CTAB = 0x9A                        # 9Ah–9Fh: маска катушек для цилиндра c (считает основной цикл)
FUELCNT = 0xB6                     # мс до гашения импульса расхода на P5.1 (таймер 1)

# регистры
B, ACC, DPL, DPH = 0xF0, 0xE0, 0x82, 0x83
CMEN, CCEN, CC4EN = 0xF6, 0xC1, 0xC9
CRCL, CRCH, CCL4, CCH4, CCL1, CCH1 = 0xCA, 0xCB, 0xCE, 0xCF, 0xC2, 0xC3
COMSETL, COMSETH, COMCLRL, COMCLRH, SETMSK, CLRMSK = 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6
P4, P5 = 0xE8, 0xF8
PSW, IEN2, CTCON = 0xD0, 0x9A, 0xE1     # CTCON.4 — флаг совпадения COMSET, IEN2.4 — его прерывание (вектор 00A3)
P5_COILS = 0xC0                    # К5 = P5.6, К6 = P5.7 (P5.1 — сигнал расхода, P5.2 — ШИМ j7es)
# биты
EA, BIT_2AH0, BIT_26_6 = 0xAF, 0x50, 0x36
BIT_PHASE = 0x05                   # 20h.5 = 6051.5 «Датчик фаз» (копирует стоковый @E711)
BIT_PHERR = 0x14                   # 22h.4 — стоковый признак ошибки фазы (→ E711: 21h.5, → 0340)
BIT_PAIRIGN = 0x0D                 # 21h.5 — стоковое «искра попарно» (считает E711 каждый проход цикла)
BIT_2AH2 = 0x52                    # 2Ah.2 — стоковая «искра по времени» (CM4–CM7 через прерывание B9A7)
PHERR_X = 0xFF53                   # FF53.0 — копия ошибки фазы для стокового выбора впрыска (1341, 14F7)
P1_0, P1_2, P1_4 = 0x90, 0x92, 0x94
P5_1, TF1 = 0xF9, 0x8E


def ACCb(n): return 0xE0 + n
def Bb(n): return 0xF0 + n


CM_COIL = [  # К1..К4: (младший CM, старший CM, маска CMEN, бит P4)
    (0xE4, 0xE5, 0x10, 0xEC), (0xE6, 0xE7, 0x20, 0xED),
    (0xF2, 0xF3, 0x40, 0xEE), (0xF4, 0xF5, 0x80, 0xEF),
]


class Asm:
    def __init__(self, org):
        self.org, self.b, self.lab, self.fix = org, bytearray(), {}, []

    @property
    def pc(self): return self.org + len(self.b)

    def label(self, n):
        assert n not in self.lab, n
        self.lab[n] = self.pc

    def e(self, *xs): self.b += bytes(x & 0xFF for x in xs)

    def rel(self, ops, n):
        self.e(*ops)
        self.fix.append((len(self.b), n, 'rel'))
        self.e(0)

    def abs16(self, op, t):
        self.e(op)
        if isinstance(t, str):
            self.fix.append((len(self.b), t, 'abs'))
            self.e(0, 0)
        else:
            self.e(t >> 8, t)

    # пересылки
    def mov_a_dir(self, d): self.e(0xE5, d)
    def mov_dir_a(self, d): self.e(0xF5, d)
    def mov_dir_imm(self, d, i): self.e(0x75, d, i)
    def mov_dir_dir(self, dst, src): self.e(0x85, src, dst)
    def mov_dir_rn(self, d, n): self.e(0x88 + n, d)
    def mov_rn_imm(self, n, i): self.e(0x78 + n, i)
    def mov_rn_a(self, n): self.e(0xF8 + n)
    def mov_a_rn(self, n): self.e(0xE8 + n)
    def mov_a_imm(self, i): self.e(0x74, i)
    def mov_a_ri(self, i): self.e(0xE6 + i)
    def mov_ri_a(self, i): self.e(0xF6 + i)
    def mov_ri_imm(self, i, v): self.e(0x76 + i, v)
    def mov_ri_dir(self, i, d): self.e(0xA6 + i, d)
    def mov_dptr(self, v): self.e(0x90, v >> 8, v)
    def movc(self): self.e(0x93)
    def movx_a(self): self.e(0xE0)          # MOVX A,@DPTR
    def movx_w(self): self.e(0xF0)          # MOVX @DPTR,A
    def xch_a_dir(self, d): self.e(0xC5, d)
    def push(self, d): self.e(0xC0, d)
    def pop(self, d): self.e(0xD0, d)
    # арифметика / логика
    def add_a_imm(self, i): self.e(0x24, i)
    def add_a_dir(self, d): self.e(0x25, d)
    def addc_a_dir(self, d): self.e(0x35, d)
    def reti(self): self.e(0x32)
    def add_a_rn(self, n): self.e(0x28 + n)
    def addc_a_rn(self, n): self.e(0x38 + n)
    def subb_a_imm(self, i): self.e(0x94, i)
    def subb_a_dir(self, d): self.e(0x95, d)
    def anl_a_imm(self, i): self.e(0x54, i)
    def orl_a_dir(self, d): self.e(0x45, d)
    def orl_a_rn(self, n): self.e(0x48 + n)
    def xrl_a_dir(self, d): self.e(0x65, d)
    def xrl_a_rn(self, n): self.e(0x68 + n)
    def anl_dir_imm(self, d, i): self.e(0x53, d, i)
    def orl_dir_imm(self, d, i): self.e(0x43, d, i)
    def anl_dir_a(self, d): self.e(0x52, d)
    def orl_dir_a(self, d): self.e(0x42, d)
    def orl_a_imm(self, i): self.e(0x44, i)
    def inc_a(self): self.e(0x04)
    def inc_rn(self, n): self.e(0x08 + n)
    def dec_rn(self, n): self.e(0x18 + n)
    def inc_ri(self, i): self.e(0x06 + i)
    def clr_a(self): self.e(0xE4)
    def cpl_a(self): self.e(0xF4)
    def clr_c(self): self.e(0xC3)
    def cpl_c(self): self.e(0xB3)
    def rl_a(self): self.e(0x23)
    def rr_a(self): self.e(0x03)
    def rlc_a(self): self.e(0x33)
    def div_ab(self): self.e(0x84)
    # биты
    def setb(self, b): self.e(0xD2, b)
    def clr(self, b): self.e(0xC2, b)
    def mov_c_bit(self, b): self.e(0xA2, b)
    def mov_bit_c(self, b): self.e(0x92, b)
    # переходы
    def ret(self): self.e(0x22)
    def ljmp(self, t): self.abs16(0x02, t)
    def lcall(self, t): self.abs16(0x12, t)
    def sjmp(self, n): self.rel((0x80,), n)
    def jz(self, n): self.rel((0x60,), n)
    def jnz(self, n): self.rel((0x70,), n)
    def jc(self, n): self.rel((0x40,), n)
    def jnc(self, n): self.rel((0x50,), n)
    def jb(self, b, n): self.rel((0x20, b), n)
    def jnb(self, b, n): self.rel((0x30, b), n)
    def cjne_a_imm(self, i, n): self.rel((0xB4, i), n)
    def cjne_rn_imm(self, r, i, n): self.rel((0xB8 + r, i), n)
    def djnz_rn(self, r, n): self.rel((0xD8 + r,), n)

    def link(self):
        for pos, n, kind in self.fix:
            t = self.lab[n]
            if kind == 'rel':
                off = t - (self.org + pos + 1)
                assert -128 <= off <= 127, ('далеко', n, off)
                self.b[pos] = off & 0xFF
            else:
                self.b[pos], self.b[pos + 1] = t >> 8, t & 0xFF
        return bytes(self.b)


def code(a):
    """Весь новый код. Комментарии — что делает каждая подпрограмма."""
    # ---------- ADV: следующий зуб (как v1); R6 уже = номер этого зуба 1..59 ----------
    a.label('adv')
    a.mov_rn_imm(1, PHT)            # зуб опроса ДФ? (R1 здесь свободен: дальше 02B9 его пишет до чтения)
    a.mov_a_ri(1)
    a.xrl_a_rn(6)
    a.jnz('adv_r7')
    a.mov_c_bit(P1_2)               # замер уровня ДФ
    a.clr_a()
    a.rlc_a()
    a.orl_a_imm(0x80)               # бит7 — замер свежий
    a.mov_rn_imm(1, PHLAT)
    a.mov_ri_a(1)
    a.label('adv_r7')
    a.inc_rn(7)
    a.cjne_rn_imm(7, 20, 'adv_done')
    a.mov_rn_imm(7, 0)
    a.mov_a_dir(0x40)
    a.inc_a()
    a.cjne_a_imm(6, 'adv_set')
    a.clr_a()
    a.setb(BIT_26_6)
    a.label('adv_set')
    a.mov_dir_a(0x40)
    a.label('adv_done')
    a.ljmp(0x02B9)

    # ---------- SYNC0: зуб 0. R7 и такт по Z, фаза по P1.2, режимы ----------
    a.label('sync0')
    a.push(DPL)
    a.push(DPH)
    a.mov_dptr(ZCAL)
    a.clr_a()
    a.movc()
    a.mov_dir_a(B)
    a.mov_a_imm(64)
    a.clr_c()
    a.subb_a_dir(B)                 # 64 − Z
    a.cjne_a_imm(60, 's0_c')
    a.label('s0_c')
    a.jc('s0_m')
    a.subb_a_imm(60)                # (4 − Z) mod 60
    a.label('s0_m')
    a.mov_dir_imm(B, 20)
    a.div_ab()                      # A = j0, B = зуб в такте
    a.mov_rn_a(0)                   # R0 = ожидаемый такт зуба 0
    a.mov_a_dir(B)
    a.mov_rn_a(7)
    a.jnz('s0_ph')
    a.mov_a_dir(0x40)               # граница такта на зубе 0 — новый такт
    a.inc_a()
    a.cjne_a_imm(6, 's0_i')
    a.clr_a()
    a.setb(BIT_26_6)
    a.label('s0_i')
    a.mov_dir_a(0x40)
    a.label('s0_ph')
    a.jnb(BIT_PHASE, 's0_nph')      # штатный флаг 6051.5 «Датчик фаз» (копия в 20h.5, @E711)
    a.mov_dptr(PHT_CAL)             # зуб опроса ДФ → копия в ОЗУ для обработчика зуба
    a.clr_a()
    a.movc()
    a.mov_rn_imm(1, PHT)
    a.mov_ri_a(1)
    a.jnz('s0_lat')
    a.mov_c_bit(P1_2)               # зуб опроса 0: уровень датчика фаз сейчас
    a.clr_a()
    a.rlc_a()
    a.sjmp('s0_lv')
    a.label('s0_lat')               # зуб опроса N: замер с зуба N, забрать и сбросить
    a.mov_rn_imm(1, PHLAT)
    a.mov_a_ri(1)
    a.mov_ri_imm(1, 0)
    a.jnb(ACCb(7), 's0_nph')        # замера не было — фаза не подтверждена
    a.anl_a_imm(1)
    a.label('s0_lv')
    a.mov_dir_a(B)
    a.mov_dptr(PHPOL)
    a.clr_a()
    a.movc()
    a.xrl_a_dir(B)
    a.anl_a_imm(1)
    a.jz('s0_e')
    a.mov_a_rn(0)
    a.add_a_imm(3)
    a.mov_rn_a(0)                   # такт цилиндра j0+3
    a.label('s0_e')
    a.mov_rn_imm(1, PH_LAST)        # исправность: уровень обязан меняться каждый оборот
    a.mov_a_ri(1)
    a.xrl_a_dir(B)
    a.mov_ri_dir(1, B)
    a.mov_rn_imm(1, PH_GOOD)
    a.jz('s0_bad')
    a.mov_a_ri(1)
    a.cjne_a_imm(3, 's0_g')
    a.sjmp('s0_okc')
    a.label('s0_g')
    a.inc_ri(1)
    a.sjmp('s0_okc')
    a.label('s0_bad')
    a.mov_ri_imm(1, 0)
    a.label('s0_okc')
    a.mov_a_ri(1)
    a.clr_c()
    a.subb_a_imm(2)
    a.jc('s0_nok')                  # меньше 2 оборотов подряд — фаза не подтверждена
    a.mov_dir_rn(0x40, 0)           # фаза есть: такт точно
    a.mov_a_imm(1)
    a.sjmp('s0_fl')
    a.label('s0_nph')
    a.mov_rn_imm(1, PH_GOOD)
    a.mov_ri_imm(1, 0)
    a.label('s0_nok')               # без фазы: такт только по модулю 3 (как v1)
    a.mov_a_dir(0x40)
    a.cjne_a_imm(6, 's0_lt')
    a.label('s0_lt')
    a.jnc('s0_fix')
    a.mov_dir_imm(B, 3)
    a.div_ab()
    a.mov_a_dir(B)
    a.mov_rn_a(1)
    a.mov_a_rn(0)
    a.mov_dir_imm(B, 3)
    a.div_ab()
    a.mov_a_dir(B)
    a.xrl_a_rn(1)
    a.jz('s0_keep')
    a.label('s0_fix')
    a.mov_dir_rn(0x40, 0)
    a.label('s0_keep')
    a.clr_a()
    a.label('s0_fl')                # A = фаза подтверждена (0/1) → стоковые признаки ошибки фазы,
    a.jnb(BIT_PHASE, 's0_x')        # дальше сток решает сам: искра (E711 → 21h.5), впрыск (14F7 → 2Ah.0)
    a.mov_dptr(PHERR_X)
    a.jz('s0_er')
    a.clr(BIT_PHERR)                # фаза есть
    a.movx_a()
    a.anl_a_imm(0xFE)
    a.sjmp('s0_w')
    a.label('s0_er')
    a.setb(BIT_PHERR)               # фазы нет / не подтверждена
    a.movx_a()
    a.orl_a_imm(0x01)
    a.label('s0_w')
    a.movx_w()
    a.label('s0_x')
    a.pop(DPH)
    a.pop(DPL)
    a.ljmp(0x02B9)

    # ---------- INJ41: 41h = (40h − 3Dh) mod 6 (как v1) ----------
    a.label('inj41')
    a.mov_a_dir(0x40)
    a.clr_c()
    a.subb_a_dir(0x3D)
    a.jnc('i41_ok')
    a.add_a_imm(6)
    a.label('i41_ok')
    a.mov_dir_a(0x41)
    a.ret()

    # ---------- IDX (зуб 8): 43h = 40h; цилиндр c = (40h+2) mod 6 → слот; 77h = c mod 3 ----------
    a.label('idx')
    a.mov_dir_dir(0x43, 0x40)
    a.mov_a_dir(0x40)
    a.add_a_imm(2)
    a.cjne_a_imm(6, 'ix_c')
    a.label('ix_c')
    a.jc('ix_k')
    a.subb_a_imm(6)
    a.label('ix_k')
    a.push(ACC)
    a.mov_dir_imm(B, 3)
    a.div_ab()
    a.mov_dir_dir(IDX, B)
    a.mov_rn_imm(1, SLOT_B)
    a.mov_a_dir(0x43)
    a.jnb(ACCb(0), 'ix_st')
    a.mov_rn_imm(1, SLOT_A)
    a.label('ix_st')
    a.pop(ACC)
    a.mov_ri_a(1)
    a.ret()

    # ---------- BASE (@3E70, основной цикл): R3 = база записи j = (Z − 1 + 20j) mod 60 (как v1).
    #            На первой записи (R0 = 80h) — пересчёт таблицы масок катушек CTAB[c] ----------
    a.label('base')
    a.cjne_rn_imm(0, 0x80, 'base_z')
    for c in range(6):
        a.mov_a_imm(c)
        a.lcall('coilmask')
        a.mov_rn_imm(1, CTAB + c)
        a.mov_ri_a(1)
    a.label('base_z')
    a.mov_dptr(ZCAL)
    a.clr_a()
    a.movc()
    a.mov_rn_a(3)
    a.mov_a_rn(0)
    a.clr_c()
    a.subb_a_imm(0x80)
    a.rr_a()
    a.rr_a()
    a.mov_dir_imm(B, 20)
    a.e(0xA4)                       # MUL AB
    a.add_a_rn(3)
    a.add_a_imm(59)
    a.label('base_mod')
    a.cjne_a_imm(60, 'base_cmp')
    a.label('base_cmp')
    a.jc('base_ok')
    a.subb_a_imm(60)
    a.sjmp('base_mod')
    a.label('base_ok')
    a.mov_rn_a(3)
    a.mov_a_rn(0)
    a.clr_c()
    a.subb_a_imm(0x80)
    a.ret()

    # ---------- BIT2: A = 1 << A (портит R1) ----------
    a.label('bit2')
    a.mov_rn_a(1)
    a.inc_rn(1)
    a.mov_a_imm(1)
    a.sjmp('b2c')
    a.label('b2l')
    a.rl_a()
    a.label('b2c')
    a.djnz_rn(1, 'b2l')
    a.ret()

    # ---------- COILMASK: A = цилиндр → A = маска катушек (бит0 К1 … бит5 К6) ----------
    a.label('coilmask')
    a.mov_dir_a(B)
    a.mov_dptr(COILMAP)
    a.movc()
    a.lcall('bit2')
    a.xch_a_dir(B)                  # A = c, B = маска цилиндра c
    a.push(ACC)
    a.jb(BIT_PAIRIGN, 'cm_w')       # стоковый режим искры (21h.5): попарно — плюс цилиндр пары
    a.pop(ACC)                      # поцилиндрово — только своя
    a.mov_a_dir(B)
    a.ret()
    a.label('cm_w')                 # холостая искра — плюс цилиндр пары (c+3)
    a.pop(ACC)
    a.add_a_imm(3)
    a.cjne_a_imm(6, 'cm_c')
    a.label('cm_c')
    a.jc('cm_k')
    a.subb_a_imm(6)
    a.label('cm_k')
    a.movc()
    a.lcall('bit2')
    a.orl_a_dir(B)
    a.ret()

    # ---------- выходы зажигания: A = старший, R0 = младший байт времени ----------
    def out(name, slot, dwell, back):
        a.label(name)
        a.mov_dir_a(B)              # B = старший байт времени
        a.mov_rn_imm(1, slot)
        a.mov_a_ri(1)               # цилиндр слота
        a.add_a_imm(CTAB)
        a.mov_rn_a(1)
        a.mov_a_ri(1)
        a.mov_rn_a(1)               # R1 = маска катушек (готовая, из основного цикла)
        for k, (cml, cmh, msk, pbit) in enumerate(CM_COIL):
            nk = '%s_k%d' % (name, k)
            a.mov_a_rn(1)
            a.jnb(ACCb(k), nk)
            a.anl_dir_imm(CMEN, (~msk) & 0xFF)
            a.mov_dir_dir(cmh, B)
            a.mov_dir_rn(cml, 0)
            a.orl_dir_imm(CMEN, msk)
            if dwell:
                a.mov_a_dir(0x68)   # 68h = 0 — такт без искры (отсечка)
                a.jz(nk)
                a.clr(pbit)         # на совпадении — 0: зарядка
            else:
                a.setb(pbit)        # на совпадении — 1: искра
            a.label(nk)
        a.mov_a_rn(1)               # К5 / К6 на P5 через COMSET / COMCLR
        a.anl_a_imm(0x30)
        a.jz(name + '_end')
        a.mov_c_bit(ACCb(5))
        a.mov_bit_c(ACCb(7))        # бит5 (К6) → P5.7
        a.mov_c_bit(ACCb(4))
        a.mov_bit_c(ACCb(6))        # бит4 (К5) → P5.6
        a.anl_a_imm(P5_COILS)
        a.mov_rn_a(1)
        if dwell:
            a.mov_a_dir(0x68)
            a.jz(name + '_end')
        a.mov_dptr(P5POL)
        a.clr_a()
        a.movc()
        a.jnb(ACCb(0), name + '_lo')
        if dwell:                   # зарядка высоким: COMSET; бит снять из CLRMSK — иначе
            a.mov_dir_dir(COMSETH, B)   # старый COMCLR через 393 мс (переполнение таймера 2) погасит раньше
            a.mov_dir_rn(COMSETL, 0)
            a.mov_dir_rn(SETMSK, 1)
            a.mov_a_rn(1)
            a.cpl_a()
            a.anl_dir_a(CLRMSK)
            # «искра по времени» (2Ah.2, сток: B9A7 для К1–К4): искра = зарядка + 45h:44h сразу во второй
            # регистр; прерывание COMSET (на зарядке) снимет бит зарядки, чтобы через 393 мс она не повторилась
            a.jnb(BIT_2AH2, name + '_end')
            a.mov_a_rn(0)
            a.add_a_dir(0x44)
            a.mov_dir_a(COMCLRL)
            a.mov_a_dir(B)
            a.addc_a_dir(0x45)
            a.mov_dir_a(COMCLRH)
            a.mov_dir_rn(CLRMSK, 1)
            a.sjmp(name + '_int')
        else:                      # искра — низким: COMCLR, зарядку снять с маски
            a.mov_dir_dir(COMCLRH, B)
            a.mov_dir_rn(COMCLRL, 0)
            a.mov_dir_rn(CLRMSK, 1)
            a.mov_a_rn(1)
            a.cpl_a()
            a.anl_dir_a(SETMSK)
        a.sjmp(name + '_end')
        a.label(name + '_lo')
        if dwell:                   # зарядка низким: COMCLR; бит снять из SETMSK
            a.mov_dir_dir(COMCLRH, B)
            a.mov_dir_rn(COMCLRL, 0)
            a.mov_dir_rn(CLRMSK, 1)
            a.mov_a_rn(1)
            a.cpl_a()
            a.anl_dir_a(SETMSK)
            a.jnb(BIT_2AH2, name + '_end')    # «искра по времени»: искра COMSET = зарядка + 45h:44h,
            a.mov_a_rn(0)                     # прерывание COMSET (на искре) снимет бит зарядки
            a.add_a_dir(0x44)
            a.mov_dir_a(COMSETL)
            a.mov_a_dir(B)
            a.addc_a_dir(0x45)
            a.mov_dir_a(COMSETH)
            a.mov_dir_rn(SETMSK, 1)
            a.label(name + '_int')
            a.anl_dir_imm(CTCON, 0xEF)        # флаг COMSET сбросить, прерывание COMSET разрешить
            a.orl_dir_imm(IEN2, 0x10)
        else:                      # искра — высоким: COMSET
            a.mov_dir_dir(COMSETH, B)
            a.mov_dir_rn(COMSETL, 0)
            a.mov_dir_rn(SETMSK, 1)
            a.mov_a_rn(1)
            a.cpl_a()
            a.anl_dir_a(CLRMSK)
        a.label(name + '_end')
        a.ljmp(back)

    out('dwa', SLOT_A, True, 0x04F7)
    out('spa', SLOT_A, False, 0x0546)
    out('dwb', SLOT_B, True, 0x05C5)
    out('spb', SLOT_B, False, 0x0614)

    # ---------- STOPFIX: при остановке записи 0 / 1 → слоты B / A = цилиндры 0 / 1 ----------
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

    # ---------- INJMASK (@1626): A = маска форсунок для события такта 41h ----------
    a.label('injmask')
    a.mov_a_dir(0x41)
    a.mov_dptr(INJMAP)
    a.jnb(BIT_2AH0, 'im_ph')
    a.mov_dir_imm(B, 3)             # попарно: цилиндры c и c+3
    a.div_ab()
    a.mov_a_dir(B)
    a.push(ACC)
    a.movc()
    a.mov_dir_a(B)
    a.pop(ACC)
    a.add_a_imm(3)
    a.movc()
    a.orl_a_dir(B)
    a.ret()
    a.label('im_ph')                # фазированно: один цилиндр
    a.movc()
    a.ret()

    # ---------- OPEN5 / OPEN6: открыть Ф5 (P1.4) / Ф6 (P1.0) сейчас, закрыть через R0:R1 ----------
    for name, (enr, off, on), (lo, hi), pin in (
            ('open5', (CC4EN, 0xFB, 0x04), (CCL4, CCH4), P1_4),
            ('open6', (CCEN, 0xFC, 0x02), (CRCL, CRCH), P1_0)):
        a.label(name)
        a.anl_dir_imm(enr, off)     # сравнение выкл — запись в порт сразу на ногу
        a.clr(EA)
        a.setb(pin)                 # открыть
        a.mov_dir_a(CCL1)           # снимок таймера 2 (захват по записи)
        a.setb(EA)
        a.mov_a_dir(CCL1)
        a.add_a_rn(0)
        a.push(ACC)
        a.mov_a_dir(CCH1)
        a.addc_a_rn(1)
        a.mov_dir_a(hi)
        a.pop(ACC)
        a.mov_dir_a(lo)
        a.orl_dir_imm(enr, on)      # сравнение вкл (режим 1)
        a.clr(pin)                  # на совпадении — 0: закрыть
        a.ret()

    # ---------- SYNC56 (@16BE): Ф5 / Ф6 в основном впрыске (маска в B, импульс R0:R1) ----------
    a.label('sync56')
    a.mov_a_rn(0)
    a.orl_a_rn(1)
    a.jz('s56_done')                # нулевой импульс (вход с 1623) — ничего
    a.mov_a_dir(B)
    a.anl_a_imm(0x30)
    a.jz('s56_done')
    a.jnb(Bb(4), 's56_6')
    a.lcall('open5')
    a.label('s56_6')
    a.jnb(Bb(5), 's56_done')
    a.lcall('open6')
    a.label('s56_done')
    a.mov_dptr(0x5F00)
    a.ljmp(0x16C1)

    # ---------- USED56: A = выходы Ф5 / Ф6, задействованные в таблице (биты 4, 5) ----------
    a.label('used56')
    a.mov_dptr(INJMAP)
    a.mov_dir_imm(B, 0)
    for i in range(6):
        a.mov_a_imm(i)
        a.movc()
        a.orl_dir_a(B)
    a.mov_a_dir(B)
    a.anl_a_imm(0x30)
    a.ret()

    # ---------- ASY56 (@181C): асинхронный импульс на закрытые Ф5 / Ф6 ----------
    a.label('asy56')
    a.lcall('used56')
    a.jnb(ACCb(4), 'a_6')
    a.jb(P1_4, 'a_6')               # уже открыта
    a.push(ACC)
    a.lcall('open5')
    a.pop(ACC)
    a.label('a_6')
    a.jnb(ACCb(5), 'a_done')
    a.jb(P1_0, 'a_done')
    a.lcall('open6')
    a.label('a_done')
    a.mov_a_dir(0x7C)               # заменённые команды
    a.anl_a_imm(0x01)
    a.ret()

    # ---------- PRIME56 (@30E0): подкачка при включении — Ф5 / Ф6 (A = старший, R2 = младший) ----------
    a.label('prime56')
    a.orl_dir_imm(P4, 0x0F)         # заменённая команда
    a.push(ACC)
    a.mov_a_dir(0x7C)
    a.anl_a_imm(0x0F)
    a.jnz('p_done')
    a.lcall('used56')
    a.mov_dir_a(B)
    a.jnb(Bb(4), 'p_6')
    a.anl_dir_imm(CC4EN, 0xFB)
    a.setb(P1_4)
    a.pop(ACC)
    a.push(ACC)
    a.mov_dir_a(CCH4)
    a.mov_dir_rn(CCL4, 2)
    a.orl_dir_imm(CC4EN, 0x04)
    a.clr(P1_4)
    a.label('p_6')
    a.jnb(Bb(5), 'p_done')
    a.anl_dir_imm(CCEN, 0xFC)
    a.setb(P1_0)
    a.pop(ACC)
    a.push(ACC)
    a.mov_dir_a(CRCH)
    a.mov_dir_rn(CRCL, 2)
    a.orl_dir_imm(CCEN, 0x02)
    a.clr(P1_0)
    a.label('p_done')
    a.pop(ACC)
    a.ret()

    # ---------- INJOFF (@2EB1): закрыть все форсунки ----------
    a.label('injoff')
    a.orl_dir_imm(P4, 0x0F)
    a.anl_dir_imm(CC4EN, 0xFB)
    a.clr(P1_4)
    a.orl_dir_imm(CC4EN, 0x04)
    a.anl_dir_imm(CCEN, 0xFC)
    a.clr(P1_0)
    a.orl_dir_imm(CCEN, 0x02)
    a.ret()

    # ---------- COILOFF (@0240, @2284): катушки в покой, маски P5 снять ----------
    # ---------- P5ISR (вектор 00A3, совпадение COMSET): «искра по времени» К5/К6 — снять бит зарядки ----------
    # Разрешается только из dwa/dwb в режиме 2Ah.2. Полярность 1: прерывание на зарядке → бит зарядки (SETMSK)
    # снять, искра COMCLR уже загружена. Полярность 0: прерывание на искре → снять оба (зарядка COMCLR прошла).
    a.label('p5isr')
    a.push(ACC)
    a.push(PSW)
    a.push(DPL)
    a.push(DPH)
    a.mov_dptr(P5POL)
    a.clr_a()
    a.movc()
    a.jnb(ACCb(0), 'pi_lo')
    a.anl_dir_imm(SETMSK, (~P5_COILS) & 0xFF)
    a.sjmp('pi_x')
    a.label('pi_lo')
    a.anl_dir_imm(CLRMSK, (~P5_COILS) & 0xFF)
    a.anl_dir_imm(SETMSK, (~P5_COILS) & 0xFF)
    a.label('pi_x')
    a.anl_dir_imm(CTCON, 0xEF)      # флаг сбросить (как стоковый 498E), прерывание выключить
    a.anl_dir_imm(IEN2, 0xEF)
    a.pop(DPH)
    a.pop(DPL)
    a.pop(PSW)
    a.pop(ACC)
    a.reti()

    a.label('relayoff')             # @B500 (выключение главного реле): P4 = FF и К5/К6 в покой
    a.orl_dir_imm(P4, 0xFF)         # заменённая команда
    a.sjmp('p5rest')
    a.label('ccoff')                # @2DEF (выключение по напряжению): CCEN = 0 и К5/К6 в покой
    a.mov_dir_imm(CCEN, 0x00)       # заменённая команда
    a.sjmp('p5rest')
    a.label('coiloff')
    a.orl_dir_imm(CMEN, 0xF0)       # заменённая команда
    a.label('p5rest')               # К5/К6 в покой, маски COMSET/COMCLR снять
    a.push(ACC)
    a.push(DPL)
    a.push(DPH)
    a.anl_dir_imm(SETMSK, (~P5_COILS) & 0xFF)
    a.anl_dir_imm(CLRMSK, (~P5_COILS) & 0xFF)
    a.mov_dptr(P5POL)
    a.clr_a()
    a.movc()
    a.jnb(ACCb(0), 'co_hi')
    a.anl_dir_imm(P5, (~P5_COILS) & 0xFF)   # зарядка высоким — покой низкий
    a.sjmp('co_x')
    a.label('co_hi')
    a.orl_dir_imm(P5, P5_COILS)
    a.label('co_x')
    a.pop(DPH)
    a.pop(DPL)
    a.pop(ACC)
    a.ret()

    # ---------- INITP5 (@1932): начальный P5 с покоем К5 / К6 ----------
    a.label('initp5')
    a.mov_dir_imm(P5, 0xBF)         # заменённая команда
    a.mov_dptr(P5POL)
    a.clr_a()
    a.movc()
    a.jnb(ACCb(0), 'ip_hi')
    a.anl_dir_imm(P5, (~P5_COILS) & 0xFF)   # зарядка высоким — покой низкий
    a.ret()
    a.label('ip_hi')
    a.orl_dir_imm(P5, P5_COILS)             # зарядка низким — покой высокий
    a.ret()

    # ---------- EARLY (@DF53, первые команды после сброса): Ф5 / Ф6 закрыть, К5 / К6 в покой ----------
    a.label('early')
    a.mov_dir_imm(0xB1, 0x00)       # заменённая команда: MOV SYSCON,#00h
    a.anl_dir_imm(0x90, 0xEE)       # P1.0 (Ф6), P1.4 (Ф5) = 0 — ключи закрыты
    a.mov_rn_imm(0, 0x99)           # 94h–99h (замер ДФ, слоты, фаза) и B6h–B7h = 0: после включения в ОЗУ мусор
    a.label('ea_clr')               # (SP уже C3h, R0 до этого никто не задавал)
    a.mov_ri_imm(0, 0)
    a.dec_rn(0)
    a.cjne_rn_imm(0, 0x93, 'ea_clr')
    a.mov_rn_imm(0, FUELCNT)
    a.mov_ri_imm(0, 0)
    a.mov_rn_imm(0, PHT)
    a.mov_ri_imm(0, 0)
    a.mov_dptr(P5POL)
    a.clr_a()
    a.movc()
    a.jnb(ACCb(0), 'ea_hi')
    a.anl_dir_imm(P5, (~P5_COILS) & 0xFF)   # зарядка высоким — покой низкий
    a.ret()
    a.label('ea_hi')
    a.orl_dir_imm(P5, P5_COILS)             # зарядка низким — покой высокий
    a.ret()

    # ---------- FUELON (@171D): импульс расхода на P5.1, гашение — таймер 1 через FUELCNT мс ----------
    a.label('fuelon')
    a.setb(P5_1)
    a.mov_a_rn(0)
    a.mov_rn_imm(0, FUELCNT)
    a.mov_ri_imm(0, 2)              # 2 тика таймера 1 → импульс 1–2 мс
    a.mov_rn_a(0)
    a.ljmp(0x1738)

    # ---------- T1FUEL (@062C, таймер 1 раз в 1 мс): отсчёт и гашение импульса расхода ----------
    a.label('t1fuel')
    a.clr(EA)                       # заменённые команды
    a.clr(TF1)
    a.push(0x00)                    # здесь PSW = 0 (банк 0, @0627), R0 = адрес 00h
    a.mov_rn_imm(0, FUELCNT)
    a.mov_a_ri(0)
    a.jz('tf_x')
    a.e(0x16)                       # DEC @R0
    a.mov_a_ri(0)
    a.jnz('tf_x')
    a.clr(P5_1)
    a.label('tf_x')
    a.pop(0x00)
    a.ret()


PAID_SHIFT = 0x70000                # адрес в платной j796 = адрес в j7es + 0x70000
CAL_END = 0xA5B6                    # с A5B6 в j7es уже код (дизасм), таблицы только ниже


def load_cal_list(path):
    """Список переноса. Строки:
      «адрес_j7es<TAB>длина<TAB>название[<TAB>адрес_в_платной]» — таблица (адрес в платной по умолчанию +0x70000);
      «адрес_j7es<TAB>битN<TAB>название» — включить бит N в байте j7es (флаг режима);
      «адрес_j7es<TAB>hex:байты<TAB>название» — готовые байты (значения уже в масштабе j7es).
    Возвращает (таблицы, биты); у таблицы с байтами вместо адреса в платной — bytes."""
    tables, bits = [], []
    for line in open(path, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        f = line.rstrip('\n').split('\t')
        a = int(f[0], 16)
        if f[1].startswith('бит'):                         # «битN» — включить, «битN=0» — выключить
            nb, _, v = f[1][3:].partition('=')
            bits.append((a, int(nb), f[2], v != '0'))
        elif f[1].startswith('hex:'):
            b = bytes.fromhex(f[1][4:])
            tables.append((a, len(b), f[2], b))
        else:
            src = int(f[3], 16) if len(f) > 3 and f[3].strip() else a + PAID_SHIFT
            tables.append((a, int(f[1]), f[2], src))
    return tables, bits


def apply_cal(d, paid, cal):
    """Таблицы из платной прошивки — побайтно в j7es (до патчей, чтобы put() поймал пересечения)."""
    tables, bits = cal
    busy = {}
    for a, n, name, src in tables:
        if not (0x5E00 <= a and a + n <= CAL_END):                 # с 5EF0 — константы j7es
            sys.exit('таблица «%s» вне калибровок j7es: %04X+%d' % (name, a, n))
        if a < CFG + 16 and a + n > CFG:
            sys.exit('таблица «%s» налезает на калибровку 6 цилиндров' % name)
        for x in range(a, a + n):                                  # две строки списка на одни байты
            if x in busy:
                sys.exit('«%s» и «%s» пишут в один байт %04X' % (busy[x], name, x))
            busy[x] = name
        d[a:a + n] = src if isinstance(src, bytes) else paid[src:src + n]
    for a, b, name, on in bits:
        if not (0x5E00 <= a < CAL_END and 0 <= b <= 7):
            sys.exit('флаг «%s» вне калибровок j7es: %04X бит%d' % (name, a, b))
        d[a] = d[a] | 1 << b if on else d[a] & ~(1 << b) & 0xFF


def build(stock, z, cfg, paid=None, cal=(), pht=0):
    d = bytearray(stock)
    if cal:
        apply_cal(d, paid, cal)

    def put(addr, old, new):
        old, new = bytes(old), bytes(new)
        cur = bytes(d[addr:addr + len(old)])
        if cur != old:
            sys.exit('по адресу %04X ожидалось %s, а там %s' % (addr, old.hex(), cur.hex()))
        d[addr:addr + len(new)] = new

    a = Asm(ORG)
    code(a)
    blob = a.link()
    if ORG + len(blob) > LIMIT:
        sys.exit('новый код не влез ниже F400')
    if any(d[ORG:ORG + len(blob)]) or any(d[CFG:CFG + 16]):
        sys.exit('место под код / калибровку занято')
    d[ORG:ORG + len(blob)] = blob
    L = a.lab

    def jmp(t): return [0x02, L[t] >> 8, L[t] & 0xFF]
    def call(t): return [0x12, L[t] >> 8, L[t] & 0xFF]

    # --- угловое ядро (как v1) ---
    put(0x0278, [0xBE, 0x1E, 0x09], jmp('adv'))
    put(0x026C, [0x7F, 0x1B, 0x02, 0x02, 0xB9], jmp('adv') + [0, 0])
    put(0x00F2, [0x7F, 0x1C, 0x02, 0x02, 0xB9], jmp('adv') + [0, 0])
    put(0x0100, [0x7F, 0x1D, 0x02, 0x02, 0xB9], jmp('adv') + [0, 0])
    put(0x0291, [0x7F, 0x00, 0x30], jmp('sync0'))
    put(0x3D47, [0x04], [0x06])
    put(0x3D4E, [0x1E], [0x14])
    # фаза впрыска (v7): цель = (FF47 − длительность − 37h) mod 120 зубьев от начала такта цилиндра; ВМТ на R7 = 4
    # → начало впрыска = FF47 − длительность − 57 зубьев после ВМТ своего цилиндра, как у стока (эмулятор 20.10.26).
    # В v1–v6 было 3D74 = 78h: цель вылетала за 119, кламп давал 119 — фаза не зависела от таблицы.
    put(0x3D74, [0x3C], [0x00])
    put(0x3D7E, [0x0B], [0x37])
    put(0x3D8D, [0xB2, 0xE1], [0x00, 0x00])
    put(0x3D91, [0x1E], [0x14])
    put(0x3DCA, [0x1E], [0x14])
    put(0x3DCC, [0xB2, 0xE1], [0x00, 0x00])
    for x in (0x21C5, 0x21D9):
        put(x, [0x1E], [0x14])
    for x in (0x21CA, 0x21DE):
        put(x, [0x1D], [0x13])
    for x in (0x21CE, 0x21E2):
        put(x, [0x0B], [0x0F])
    for x in (0x21D2, 0x21E6):
        put(x, [0x1E], [0x14])
    put(0x0365, [0xE5, 0x40, 0xC3, 0x95, 0x3D, 0x54, 0x03, 0xF5, 0x41], call('inj41') + [0] * 6)
    put(0x03BF, [0x85, 0x40, 0x43], call('idx'))
    put(0x03D1, [0xE5, 0x43, 0xB2, 0xE1], [0xE5, IDX, 0x00, 0x00])
    for x in (0x0947, 0x0966, 0x0998, 0x09C5, 0x0A67):
        put(x, [0xE5, 0x43], [0xE5, IDX])
    put(0x0AB2, [0xA9, 0x43], [0xA9, IDX])
    put(0x3E70, [0x7B, 0x2F, 0xE8, 0xC3, 0x94, 0x80, 0x30, 0xE2, 0x02, 0x7B, 0x11], call('base') + [0] * 8)
    put(0x04A6, [0x20, 0x0D, 0x2C], jmp('dwa'))
    put(0x052E, [0x53, 0xF6, 0xEF], jmp('spa'))
    put(0x0574, [0x20, 0x0D, 0x2C], jmp('dwb'))
    put(0x05FC, [0x53, 0xF6, 0xBF], jmp('spb'))
    put(0x2FD6, [0x02, 0x3B, 0xE4], jmp('stopfix'))
    put(0x2313, [0x40], [0x2B])
    put(0x2316, [0x42], [0x2C])
    put(0x2319, [0x0F], [0x0A])
    put(0x02C4, [0xEF], [0xEE])
    put(0x03AE, [0x03], [0x02])
    # 6051.5 «Датчик фаз» — штатный флаг, с v7 включает и наш механизм фазы (SYNC0); стоковое чтение на 0293
    # обходится переходом на 0291, стоковый выбор 2Ah.0 убран (134E/14F3/14FD); E742 (21h.5, P9.6) — штатно
    # --- впрыск на 6 выходов ---
    put(0x1626, [0xE5, 0x41, 0xA2, 0x50, 0x92, 0xE2, 0x90, 0xA5, 0x58, 0x93], call('injmask') + [0] * 7)
    put(0x16BE, [0x90, 0x5F, 0x00], jmp('sync56'))
    put(0x171D, [0x53, 0xA6, 0xFD], jmp('fuelon'))         # импульс расхода: гашение таймером 1, не COMCLR
    put(0x062C, [0xC2, 0xAF, 0xC2, 0x8E], call('t1fuel') + [0])   # таймер 1: отсчёт импульса расхода
    put(0x181C, [0xE5, 0x7C, 0x54, 0x01], call('asy56') + [0])
    put(0x30E0, [0x43, 0xE8, 0x0F], call('prime56'))
    put(0x2EB1, [0x43, 0xE8, 0x0F], call('injoff'))
    # 134E / 14F3 / 14FD (стоковый выбор попарно/фазированно по FF53.0) — с v7 штатно, SYNC0 пишет FF53.0 и 22h.4
    # --- зажигание: штатный поцилиндровый режим на 6 катушек ---
    # «искра по времени» (2Ah.2): стоковый пропуск искры по зубу (0503/05D1) как есть, К1–К4 — B9A7,
    # К5/К6 — dwa/dwb грузят искру во второй регистр пары + p5isr на COMSET (вектор моментного РХХ — он вырезан)
    put(0x00A3, [0x02, 0x49, 0x8E], jmp('p5isr'))
    put(0x03BD, [0x08], [0x0C])     # загрузка слота на R7 = 12: до ВМТ 32 зуба, запас после ВМТ 7 зубьев (Launch)
    put(0x3E52, [0xAE], [0x8C])     # предел накопления 140° (окно до ВМТ 192° − УОЗ 45° − зуб)
    # --- прочее под 6 цилиндров ---
    put(0x38C6, [0x04], [0x06])     # «добавка на первых тактах» после пуска/отсечки — на все 6 цилиндров
    put(0xB500, [0x43, 0xE8, 0xFF], call('relayoff'))      # выключение реле: К5/К6 в покой
    put(0x2DEF, [0x75, 0xC1, 0x00], call('ccoff'))         # выключение по напряжению: К5/К6 в покой
    put(0x20F7, [0x30, 0xE0, 0x24], [0x80, 0x25, 0x00])    # моментный РХХ (5F00.0) не трогает COMSET/COMCLR
    # --- катушки на P5, покой ---
    put(0x0240, [0x43, 0xF6, 0xF0], call('coiloff'))
    put(0x2284, [0x43, 0xF6, 0xF0], call('coiloff'))
    put(0x1932, [0x75, 0xF8, 0xBF], call('initp5'))
    # --- порты и блоки сравнения ---
    put(0x1929, [0x75, 0x90, 0xFF], [0x75, 0x90, 0xEE])    # P1.0, P1.4 = 0 (Ф5 / Ф6 закрыты)
    put(0x19C6, [0x75, 0x90, 0x1C], [0x75, 0x90, 0x0C])    # направление: P1.4 — выход
    put(0x1A72, [0x75, 0xC1, 0x4C], [0x75, 0xC1, 0x4E])    # CRC — сравнение
    put(0x211E, [0x75, 0xC9, 0x98], [0x75, 0xC9, 0xFD])    # CC4 сравнение 1 + режим 2 на P5.0–P5.7 (COCON=111)
    put(0x46F0, [0xC2, 0x97], [0x22, 0x00])                # SPI детонации выкл (P1.0 — Ф6)
    put(0x0909, [0xC2, 0x42, 0x30, 0x47, 0x15], [0xC2, 0x42, 0x02, 0x0A, 0xE8])   # INT0: расчёт ДД пропустить
    put(0xDF53, [0x75, 0xB1, 0x00], call('early'))         # старт: ноги Ф5/Ф6/К5/К6 сразу
    # --- калибровка ---
    put(CFG, [0] * 16, cfg + [z])
    put(PHT_CAL, [0], [pht])
    fix_sum(d)
    return bytes(d), len(blob), L


def fix_sum(d):
    """Слово FFFE–FFFF = сумма всех байт; компенсатор FFF8–FFF9 (см. разбор п.3.12)."""
    d[0xFFF8] = d[0xFFF9] = 0
    s0 = sum(d[:0xFFFE]) & 0xFFFF
    for hi in range(256):
        c = (255 * hi - s0) & 0xFFFF
        if c <= 510:
            break
    else:
        sys.exit('не подобрать компенсатор')
    d[0xFFF8], d[0xFFF9] = min(c, 255), c - min(c, 255)
    s1 = sum(d[:0xFFFE])
    cs = next(v for v in range(65536) if (s1 + (v & 0xFF) + (v >> 8)) & 0xFFFF == v)
    d[0xFFFE], d[0xFFFF] = cs & 0xFF, cs >> 8
    assert sum(d) & 0xFFFF == cs
    return cs


DEFAULT = dict(mode=0x00, phpol=0x00, p5pol=0x01,          # mode (E7F0) с v7 не используется
               inj=[0x01, 0x02, 0x04, 0x08, 0x10, 0x20], coil=[0, 1, 2, 3, 4, 5])


def cfg_bytes(c):
    return [c['mode'], c['phpol'], c['p5pol']] + list(c['inj']) + list(c['coil'])


def main():
    ap = argparse.ArgumentParser(description='Прошивка v2 j7es под 6 цилиндров')
    ap.add_argument('bin')
    ap.add_argument('--z', type=int, required=True)
    ap.add_argument('--phtooth', type=int, default=0,
                    help='зуб опроса ДФ 0..59 (0 — на зубе 0, как в стоке)')
    ap.add_argument('--mode', type=lambda s: int(s, 0), default=DEFAULT['mode'],
                    help='бит0 фаз впрыск, бит1 поцилиндровая искра, бит2 датчик фаз')
    ap.add_argument('--phpol', type=int, default=DEFAULT['phpol'])
    ap.add_argument('--p5pol', type=int, default=DEFAULT['p5pol'])
    ap.add_argument('--inj', default=','.join('%x' % v for v in DEFAULT['inj']),
                    help='маски выходов форсунок для цилиндров 1..6 (hex)')
    ap.add_argument('--coil', default=','.join(str(v) for v in DEFAULT['coil']),
                    help='номер катушки 0..5 (К1..К6) для цилиндров 1..6')
    ap.add_argument('--child', type=int, default=0,
                    help='номер дочерней (смена калибровки): 0 — родитель v%d.0' % CODE_VER)
    ap.add_argument('--what', default='', help='что изменилось относительно v%d.0 (для --child > 0)' % CODE_VER)
    ap.add_argument('--cal-from', default='', help='бин платной j796 (576 К), откуда брать таблицы')
    ap.add_argument('--cal-list', default='', help='список таблиц для переноса (.tsv: адрес_j7es, длина, название)')
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    if bool(a.cal_from) != bool(a.cal_list):
        sys.exit('--cal-from и --cal-list задаются вместе')
    if a.child > 0 and not a.what:
        sys.exit('для дочерней (--child) нужно --what: что изменилось в калибровке')
    stock = open(a.bin, 'rb').read()
    if len(stock) != 65536 or not 0 <= a.z < 60 or not 0 <= a.phtooth < 60:
        sys.exit('нужен сток 64К, Z и зуб опроса ДФ 0..59')
    cfg = dict(mode=a.mode, phpol=a.phpol, p5pol=a.p5pol,
               inj=[int(x, 16) for x in a.inj.split(',')], coil=[int(x) for x in a.coil.split(',')])
    if len(cfg['inj']) != 6 or len(cfg['coil']) != 6 or any(not 0 <= k <= 5 for k in cfg['coil']):
        sys.exit('таблицы: 6 значений, катушки 0..5')
    paid, cal = None, []
    if a.cal_from:
        paid = open(a.cal_from, 'rb').read()
        if len(paid) != 0x90000:
            sys.exit('платная должна быть 576 К (0x90000)')
        cal = load_cal_list(a.cal_list)
    out, size, L = build(stock, a.z, cfg_bytes(cfg), paid, cal, a.phtooth)
    if cal:
        print('Перенесено таблиц из платной: %d (%d байт), флагов: %d' % (
            len(cal[0]), sum(t[1] for t in cal[0]), len(cal[1])))
    name = a.out or 'j7es_v%d.%d_%s_%s ИИ.bin' % (
        CODE_VER, a.child, a.what if a.child else CODE_WHAT, datetime.datetime.now().strftime('%d.%m.%y_%H%M'))
    path = os.path.join(os.path.dirname(os.path.abspath(a.bin)), name)
    open(path, 'wb').write(out)
    print('Записан:', path)
    print('Новый код %d байт с %04X, калибровка E7F0–E7FF: %s' % (size, ORG, ' '.join('%02X' % v for v in cfg_bytes(cfg) + [a.z])))
    for k, v in sorted(L.items(), key=lambda x: x[1]):
        if '_' not in k or k in ('open5', 'open6'):
            print('  %04X %s' % (v, k))


if __name__ == '__main__':
    main()
