#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Эмулятор блока Январь 7.2 (процессор Infineon C509-L) для проверки прошивки j7es.

Выполняет образ .bin команда за командой, подаёт сигнал ДПКВ 60−2 на заданных
оборотах и записывает переключения выходов P4 (форсунки CM0–CM3, катушки
CM4–CM7) с точным временем и углом коленвала.

Периферия — по C509-L User's Manual 11.97:
  таймер 2 (fOSC/6 с делителем T2PS/T2P1/T2P0/T2PS1), захват/сравнение CC0–CC3,
  выходы CM0–CM7 в режиме сравнения 1 (теневой регистр порта 4),
  блок умножения/деления MD0–MD5/ARCON, 8 указателей DPTR (DPSEL),
  таймеры 0/1 с делителем PRSC, АЦП (запуск записью в ADDATL),
  последовательный порт 0 (передача), прерывания: 6 групп, 4 уровня (IP1/IP0),
  RMAP (SYSCON.4) и PDIR (IP1.7, сам сбрасывается после одной команды).
Мотор не моделируется: обороты задаются, датчики — постоянные коды АЦП.

Запуск:
  python3 "эмулятор j7es C509 03.10.26 ИИ.py" j7es_v0.7.5.bin --rpm 800 --sec 3
Ключи — см. --help.
"""
import argparse
import sys

FOSC = 16_000_000                 # кварц: 1 мс таймера 1 и 10400 бод K-линии сходятся на 16 МГц
MC_S = 6.0 / FOSC                 # машинный цикл, с (6 тактов кварца)

# --- Регистры (адреса по даташиту) ---
P0, SP, DPL, DPH, PCON, TCON, TMOD, TL0, TL1, TH0, TH1 = 0x80, 0x81, 0x82, 0x83, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D
P1, DPSEL, S0CON, S0BUF, IEN2, S1CON, S1BUF = 0x90, 0x92, 0x98, 0x99, 0x9A, 0x9B, 0x9C
P2, COMSETL, COMSETH, IEN0, IP0, S0RELL = 0xA0, 0xA1, 0xA2, 0xA8, 0xA9, 0xAA
P3, SYSCON, PRSC, IEN1, IP1, S0RELH, IEN3 = 0xB0, 0xB1, 0xB4, 0xB8, 0xB9, 0xBA, 0xBE
IRCON0, CCEN, CCL1, CCH1, CCL2, CCH2, CCL3, CCH3, T2CON, CC4EN = 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9
CRCL, CRCH, TL2, TH2, CCL4, CCH4 = 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCF
COMCLRL, COMCLRH, SETMSK, CLRMSK = 0xA3, 0xA4, 0xA5, 0xA6
PSW, IRCON1, ADCON0, ADDATH, ADDATL, ADCON1 = 0xD0, 0xD1, 0xD8, 0xD9, 0xDA, 0xDC
ACC, CTCON, P4, MD0, MD1, MD2, MD3, MD4, MD5, ARCON = 0xE0, 0xE1, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF
B, CMEN, CMSEL, P5, P9, P6 = 0xF0, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA
# CMx: (младший, старший) регистр
CM_REGS = [(0xD2, 0xD3), (0xD4, 0xD5), (0xD6, 0xD7), (0xE2, 0xE3), (0xE4, 0xE5), (0xE6, 0xE7), (0xF2, 0xF3), (0xF4, 0xF5)]
CM_LOW = {lo: i for i, (lo, hi) in enumerate(CM_REGS)}
CM_HIGH = {hi: i for i, (lo, hi) in enumerate(CM_REGS)}
# Регистры, подменяемые при RMAP = 1 и при PDIR = 1
RMAP_ADDRS = set(range(0xD2, 0xD8)) | {0xDE, 0xDF} | set(range(0xE2, 0xE8)) | set(range(0xF2, 0xF8))
PDIR_ADDRS = {0x80, 0x90, 0xA0, 0xB0, 0xBF, 0xE8, 0xF8, 0xF9}
PORTS = {P0, P1, P2, P3, P4, P5, P6, P9, 0xDB, 0xDD}   # P7 = DBh, P8 = DDh — только вход

# Векторы: (вектор, группа 0..5, порядок в группе)
VEC_IE0, VEC_TF0, VEC_IE1, VEC_TF1, VEC_SER0, VEC_TF2 = 0x03, 0x0B, 0x13, 0x1B, 0x23, 0x2B
VEC_ADC, VEC_IEX2, VEC_IEX3, VEC_IEX4, VEC_IEX5, VEC_IEX6 = 0x43, 0x4B, 0x53, 0x5B, 0x63, 0x6B
VEC_SER1, VEC_CMP, VEC_CTF, VEC_ICS, VEC_ICR = 0x83, 0x93, 0x9B, 0xA3, 0xAB
VEC_NAMES = {VEC_IE0: 'INT0', VEC_TF1: 'таймер 1', VEC_SER0: 'порт 0', VEC_IEX6: 'зуб CC3',
             VEC_CMP: 'совпадение CM', VEC_ICS: 'COMSET', VEC_TF0: 'таймер 0', VEC_TF2: 'таймер 2'}


class Stop(Exception):
    pass


class Engine:
    """Сигнал ДПКВ 60−2 и датчика фаз. Угол 0 — фронт первого зуба после пропуска (R6 = 0)."""

    def __init__(self, profile, cam=True, drop=(), cam_off=0.0):
        self.profile = profile      # [(время начала, об/мин), ...]; 0 об/мин — мотор стоит
        self.cam = cam
        self.cam_off = cam_off      # датчик фаз: 1 при (угол − cam_off) mod 720 < 360
        self.drop = sorted(drop)    # моменты, после которых один зуб теряется (помеха)
        self.angle = 0.0            # абсолютный угол, градусы (растёт)
        self.t = 0.0
        self.edges = []             # (время, абсолютный угол) — для пересчёта времени в угол

    def rpm_at(self, t):
        r = self.profile[0][1]
        for t0, v in self.profile:
            if t >= t0:
                r = v
        return r

    def next_edge(self):
        """Время следующего фронта зуба и номер зуба (0..57)."""
        while True:
            rpm = self.rpm_at(self.t)
            if rpm <= 0:                         # стоит: ждём, пока профиль снова даст обороты
                later = [t0 for t0, v in self.profile if t0 > self.t and v > 0]
                if not later:
                    return None
                self.t = later[0]
                continue
            tooth_dt = 1.0 / rpm                 # 6° за 1/rpm секунды
            self.angle += 6.0
            self.t += tooth_dt
            k = int(round(self.angle / 6.0)) % 60
            if k < 58:
                if self.drop and self.t >= self.drop[0]:
                    self.drop.pop(0)             # этот зуб потерян
                    continue
                self.edges.append((self.t, self.angle))
                return self.t, k

    def cam_level(self, t):
        if not self.cam:
            return 1
        a = (self.angle_at(t) - self.cam_off) % 720.0
        return 1 if a < 360.0 else 0

    def angle_at(self, t):
        e = self.edges
        if not e:
            return 0.0
        # поиск с конца — обычно спрашивают недавнее время
        i = len(e) - 1
        while i > 0 and e[i][0] > t:
            i -= 1
        t0, a0 = e[i]
        if i + 1 < len(e):
            t1, a1 = e[i + 1]
            return a0 + (a1 - a0) * (t - t0) / (t1 - t0)
        return a0 + (t - t0) * self.rpm_at(t0) * 6.0


class C509:
    def __init__(self, code, engine, adc, inputs):
        self.code = bytearray(code)
        self.x = bytearray(65536)           # XRAM: 0000–F3FF внешнее ОЗУ, F400–FFFF внутреннее
        self.r = bytearray(256)             # внутреннее ОЗУ
        self.s = bytearray(256)             # SFR (индекс = адрес)
        self.s_rmap = bytearray(256)        # подменяемые при RMAP
        self.s_dir = bytearray(b'\xff' * 256)  # регистры направления (PDIR)
        self.dptr = [0] * 8
        self.pc = 0
        self.mc = 0                         # машинные циклы с начала
        self.eng = engine
        self.adc_val = adc                  # канал -> код 0..1023
        self.inputs = inputs                # порт -> маска входов
        # периферия
        self.t2 = 0
        self.t2_acc = 0
        self.t0 = 0
        self.t1 = 0
        self.t01_acc = [0, 0]
        self.cm_val = [0] * 8
        self.p4_pin = 0xFF
        self.p4_sh = 0xFF
        self.cc_val = [0, 0, 0, 0]          # CC0..CC3 (для сравнения)
        self.mdu_seq = []
        self.adc_done = None
        self.tx_done = None
        self.pdir = 0                       # 1 → доступ к регистрам направления в этой команде
        self.pdir_set = False
        self.adc_ch = 0
        self.ilevel = []                    # стек уровней активных прерываний
        self.ivec = []                      # стек векторов (для замера времени)
        self.skip_irq = False
        self.edge = engine.next_edge()
        self.edge_mc = int(self.edge[0] / MC_S) if self.edge else None
        # P1.0 (CRC) и P1.4 (CC4) — режим сравнения 1: теневой регистр и нога
        self.p1_sh = 0x11
        self.p1_pin = 0x11
        self.crc_val = 0
        self.cc4_val = 0
        # журналы
        self.p4_log = []                    # (мц, выход, уровень): 0–7 = P4.0–P4.7, 8 = P1.0, 9 = P1.4, 10 = P5.1, 11 = P5.7, 12 = P5.6
        self.isr_time = {}                  # вектор -> [число, сумма мц, максимум мц]
        self.isr_start = []
        self.tx = bytearray()
        self.trace_hook = None
        for a, v in ((SP, 7), (P0, 0xFF), (P1, 0xFF), (P2, 0xFF), (P3, 0xFF), (P4, 0xFF), (P5, 0xFF),
                     (P6, 0xFF), (P9, 0xFF), (PRSC, 0xD5), (ADCON1, 0x40), (CTCON, 0x40)):
            self.s[a] = v

    # ------------------------------------------------------------ память
    def bank(self):
        return self.s[PSW] & 0x18

    def get_dir(self, a, rmw=False):
        if a < 0x80:
            return self.r[a]
        return self.sfr_read(a, rmw)

    def set_dir(self, a, v):
        v &= 0xFF
        if a < 0x80:
            self.r[a] = v
        else:
            self.sfr_write(a, v)

    def sfr_read(self, a, rmw=False):
        s = self.s
        if self.pdir and a in PDIR_ADDRS:
            return self.s_dir[a]
        if s[SYSCON] & 0x10 and a in RMAP_ADDRS:
            return self.s_rmap[a]
        if a == DPL:
            return self.dptr[s[DPSEL] & 7] & 0xFF
        if a == DPH:
            return self.dptr[s[DPSEL] & 7] >> 8
        if a == PSW:
            acc = s[ACC]
            p = bin(acc).count('1') & 1
            return (s[PSW] & 0xFE) | p
        if a == TL2:
            return self.t2 & 0xFF
        if a == TH2:
            return self.t2 >> 8
        if a == TL0:
            return self.t0 & 0xFF
        if a == TH0:
            return self.t0 >> 8
        if a == TL1:
            return self.t1 & 0xFF
        if a == TH1:
            return self.t1 >> 8
        if a == P4:
            return self.p4_sh if rmw else self.p4_pin
        if a == P1:
            latch = s[P1]
            cmp = self.p1_cmp_mask()
            if rmw:
                return (latch & ~cmp) | (self.p1_sh & cmp)
            v = latch & self.inputs.get(P1, 0xFF)
            cam = self.eng.cam_level(self.mc * MC_S)
            v = (v & ~0x04) | ((latch & 0x04) & (cam << 2))
            v = (v & ~0x11) | (self.p1_pin & 0x11)
            return v
        if a in PORTS:
            if rmw:
                return s[a]
            return s[a] & self.inputs.get(a, 0xFF)
        if a == ARCON:
            v = s[ARCON]
            s[ARCON] &= 0x7F                  # MDEF сбрасывается чтением
            return v
        return s[a]

    def sfr_write(self, a, v):
        s = self.s
        if self.pdir and a in PDIR_ADDRS:
            self.s_dir[a] = v
            return
        if s[SYSCON] & 0x10 and a in RMAP_ADDRS:
            self.s_rmap[a] = v
            return
        if a == DPL:
            i = s[DPSEL] & 7
            self.dptr[i] = (self.dptr[i] & 0xFF00) | v
            return
        if a == DPH:
            i = s[DPSEL] & 7
            self.dptr[i] = (self.dptr[i] & 0x00FF) | (v << 8)
            return
        if a == TL2:
            self.t2 = (self.t2 & 0xFF00) | v
            return
        if a == TH2:
            self.t2 = (self.t2 & 0x00FF) | (v << 8)
            return
        if a == TL0:
            self.t0 = (self.t0 & 0xFF00) | v
            return
        if a == TH0:
            self.t0 = (self.t0 & 0x00FF) | (v << 8)
            return
        if a == TL1:
            self.t1 = (self.t1 & 0xFF00) | v
            return
        if a == TH1:
            self.t1 = (self.t1 & 0x00FF) | (v << 8)
            return
        if a == P4:
            self.p4_write(0xFF, v)
            return
        if a == P1:
            self.p1_write(0xFF, v)
            return
        if a == P5:
            old = s[P5]
            s[P5] = v
            self.p5_log(old, v)
            return
        if a in (CRCL, CRCH):
            s[a] = v
            self.crc_val = (s[CRCH] << 8) | s[CRCL]
            return
        if a in (CCL4, CCH4):
            s[a] = v
            self.cc4_val = (s[CCH4] << 8) | s[CCL4]
            return
        if a == IP1:
            if v & 0x80:
                self.pdir_set = True
            s[IP1] = v & 0x7F
            return
        if a in CM_LOW:
            i = CM_LOW[a]
            s[a] = v
            self.cm_val[i] = (s[CM_REGS[i][1]] << 8) | v      # перенос в защёлку — по записи младшего
            return
        if a in (CCL1, CCL2, CCL3):
            k = {CCL1: 1, CCL2: 2, CCL3: 3}[a]
            mode = (s[CCEN] >> (2 * k)) & 3
            if mode == 3:                                       # захват по записи
                s[a] = self.t2 & 0xFF
                s[a + 1] = self.t2 >> 8
            else:
                s[a] = v
            self.cc_val[k] = (s[a + 1] << 8) | s[a]
            return
        if a in (CCH1, CCH2, CCH3):
            s[a] = v
            k = {CCH1: 1, CCH2: 2, CCH3: 3}[a]
            self.cc_val[k] = (v << 8) | s[a - 1]
            return
        if a == ADDATL:
            ch = s[ADCON1] & 0x0F
            self.adc_ch = ch
            s[ADCON0] |= 0x10                  # BSY
            self.adc_done = self.mc + 30
            return
        if a == S0BUF:
            self.tx.append(v)
            s[S0BUF] = v
            smod = 2 if s[PCON] & 0x80 else 1
            rel = ((s[S0RELH] & 3) << 8) | s[S0RELL]
            baud = smod * FOSC / (64.0 * max(1, 1024 - rel))
            self.tx_done = self.mc + int(10.0 / baud / MC_S)
            return
        if a in (MD0, MD1, MD2, MD3, MD4, MD5):
            k = a - MD0
            s[a] = v
            if k == 0:
                self.mdu_seq = [0]
            else:
                self.mdu_seq.append(k)
            if k == 5:
                self.mdu_run()
            return
        if a == ARCON:
            s[ARCON] = v & 0x3F
            self.mdu_shift(v)
            return
        if a == PSW:
            s[PSW] = v
            return
        s[a] = v

    def p4_write(self, mask, v):
        """Запись в P4: разрешённые в CMEN биты — в теневой регистр, остальные — сразу на ногу."""
        en = self.s[CMEN]
        for i in range(8):
            m = 1 << i
            if not mask & m:
                continue
            bit = v & m
            self.p4_sh = (self.p4_sh & ~m) | bit
            if not en & m:
                self.set_pin(i, 1 if bit else 0)

    def set_pin(self, i, lvl):
        m = 1 << i
        old = 1 if self.p4_pin & m else 0
        if old != lvl:
            self.p4_pin = (self.p4_pin & ~m) | (m if lvl else 0)
            self.p4_log.append((self.mc, i, lvl))

    def p1_cmp_mask(self):
        """Биты P1 в режиме сравнения 1: P1.0 — CRC (CCEN.1:0 = 10), P1.4 — CC4 (CC4EN COCAH4:COCAL4 = 10)."""
        m = 0
        if self.s[CCEN] & 0x03 == 0x02:
            m |= 0x01
        if self.s[CC4EN] & 0x06 == 0x04:
            m |= 0x10
        return m

    def p1_write(self, mask, v):
        s = self.s
        cmp = self.p1_cmp_mask()
        s[P1] = (s[P1] & ~mask) | (v & mask)
        for bit, lid in ((0x01, 8), (0x10, 9)):
            if not mask & bit:
                continue
            self.p1_sh = (self.p1_sh & ~bit) | (v & bit)
            if not cmp & bit:
                self.p1_set(bit, lid, 1 if v & bit else 0)

    def p1_set(self, bit, lid, lvl):
        old = 1 if self.p1_pin & bit else 0
        if old != lvl:
            self.p1_pin = (self.p1_pin & ~bit) | (bit if lvl else 0)
            self.p4_log.append((self.mc, lid, lvl))

    def p5_log(self, old, new):
        for bit, lid in ((0x02, 10), (0x80, 11), (0x40, 12)):
            if (old ^ new) & bit:
                self.p4_log.append((self.mc, lid, 1 if new & bit else 0))

    # ------------------------------------------------------------ блок умножения/деления
    def mdu_run(self):
        s = self.s
        seq = self.mdu_seq
        md = [s[MD0 + i] for i in range(6)]
        ov = 0
        if seq == [0, 1, 2, 3, 4, 5]:
            dd = md[0] | (md[1] << 8) | (md[2] << 16) | (md[3] << 24)
            dv = md[4] | (md[5] << 8)
            if dv == 0:
                ov, q, r = 1, 0xFFFFFFFF, 0
            else:
                q, r = dd // dv, dd % dv
            for i in range(4):
                s[MD0 + i] = (q >> (8 * i)) & 0xFF
            s[MD4], s[MD5] = r & 0xFF, r >> 8
        elif seq == [0, 1, 4, 5]:
            dd = md[0] | (md[1] << 8)
            dv = md[4] | (md[5] << 8)
            if dv == 0:
                ov, q, r = 1, 0xFFFF, 0
            else:
                q, r = dd // dv, dd % dv
            s[MD0], s[MD1] = q & 0xFF, q >> 8
            s[MD4], s[MD5] = r & 0xFF, r >> 8
        elif seq == [0, 4, 1, 5]:
            p = (md[0] | (md[1] << 8)) * (md[4] | (md[5] << 8))
            ov = 1 if p > 0xFFFF else 0
            for i in range(4):
                s[MD0 + i] = (p >> (8 * i)) & 0xFF
        else:
            # последовательность сбита прерыванием, которое само считало на MDU:
            # на кристалле — флаг ошибки MDEF; прошивка пересчитывает по флагу 28h.4
            s[ARCON] |= 0x80
            self.mdu_seq = []
            self.mdu_err = getattr(self, 'mdu_err', 0) + 1
            return
        s[ARCON] = (s[ARCON] & ~0x40) | (0x40 if ov else 0)
        self.mdu_seq = []

    def mdu_shift(self, v):
        s = self.s
        x = s[MD0] | (s[MD1] << 8) | (s[MD2] << 16) | (s[MD3] << 24)
        sc = v & 0x1F
        if sc == 0:                         # нормализация
            n = 0
            if x:
                while not x & 0x80000000:
                    x = (x << 1) & 0xFFFFFFFF
                    n += 1
            s[ARCON] = (s[ARCON] & 0xE0) | n
        elif v & 0x20:
            x >>= sc
        else:
            x = (x << sc) & 0xFFFFFFFF
        for i in range(4):
            s[MD0 + i] = (x >> (8 * i)) & 0xFF

    # ------------------------------------------------------------ биты
    def bit_addr(self, b):
        if b < 0x80:
            return 0x20 + (b >> 3), b & 7
        return b & 0xF8, b & 7

    def get_bit(self, b, rmw=False):
        a, n = self.bit_addr(b)
        if a < 0x80:
            return (self.r[a] >> n) & 1
        return (self.sfr_read(a, rmw) >> n) & 1

    def set_bit(self, b, val):
        a, n = self.bit_addr(b)
        if a < 0x80:
            if val:
                self.r[a] |= 1 << n
            else:
                self.r[a] &= ~(1 << n) & 0xFF
            return
        if a == P4 and not self.pdir:
            self.p4_write(1 << n, (1 << n) if val else 0)
            return
        if a == P1 and not self.pdir:
            self.p1_write(1 << n, (1 << n) if val else 0)
            return
        cur = self.sfr_read(a, rmw=True)
        cur = (cur | (1 << n)) if val else (cur & ~(1 << n))
        self.sfr_write(a, cur & 0xFF)

    # ------------------------------------------------------------ флаги PSW
    def cy(self):
        return self.s[PSW] >> 7

    def set_cy(self, c):
        if c:
            self.s[PSW] |= 0x80
        else:
            self.s[PSW] &= 0x7F

    def add(self, a, b, c=0):
        r = a + b + c
        cy = r > 0xFF
        ac = ((a & 0xF) + (b & 0xF) + c) > 0xF
        ov = ((a ^ r) & (b ^ r) & 0x80) != 0
        p = self.s[PSW] & 0x3B
        self.s[PSW] = p | (0x80 if cy else 0) | (0x40 if ac else 0) | (0x04 if ov else 0)
        return r & 0xFF

    def subb(self, a, b):
        c = self.cy()
        r = a - b - c
        cy = r < 0
        ac = ((a & 0xF) - (b & 0xF) - c) < 0
        ov = ((a ^ b) & (a ^ r) & 0x80) != 0
        p = self.s[PSW] & 0x3B
        self.s[PSW] = p | (0x80 if cy else 0) | (0x40 if ac else 0) | (0x04 if ov else 0)
        return r & 0xFF

    # ------------------------------------------------------------ стек
    def push(self, v):
        sp = (self.s[SP] + 1) & 0xFF
        self.s[SP] = sp
        self.r[sp] = v & 0xFF

    def pop(self):
        sp = self.s[SP]
        v = self.r[sp]
        self.s[SP] = (sp - 1) & 0xFF
        return v

    # ------------------------------------------------------------ периферия во времени
    def tick(self, n):
        s = self.s
        old_mc = self.mc
        self.mc += n
        # таймер 2
        if s[T2CON] & 0x03 == 0x01:
            p = ((s[PRSC] >> 4) & 3)            # T2P1:T2P0
            ps1 = 1 if s[CTCON] & 0x80 else 0
            base = [1, 4, 2, 8, 4, 16, 8, 32][(p << 1) | ps1]   # делитель от fOSC/6
            div = base * (2 if s[T2CON] & 0x80 else 1)
            self.t2_acc += n
            while self.t2_acc >= div:
                self.t2_acc -= div
                self.t2 = (self.t2 + 1) & 0xFFFF
                self.t2_event()
        # таймеры 0/1 (режим 1 — 16 бит, режим 2 — перезагрузка)
        for k in (0, 1):
            tr = (s[TCON] >> (4 + 2 * k)) & 1
            mode = (s[TMOD] >> (4 * k)) & 0x0F
            if not tr or mode & 0x04:           # остановлен или счётчик внешних импульсов
                continue
            pdiv = 1 << ((s[PRSC] >> (2 * k)) & 3)
            self.t01_acc[k] += n
            cnt = self.t01_acc[k] // pdiv
            self.t01_acc[k] -= cnt * pdiv
            if not cnt:
                continue
            m = mode & 3
            t = self.t0 if k == 0 else self.t1
            if m == 1:
                t += cnt
                if t > 0xFFFF:
                    t &= 0xFFFF
                    s[TCON] |= 0x20 if k == 0 else 0x80
            elif m == 2:
                lo = (t & 0xFF) + cnt
                hi = t >> 8
                while lo > 0xFF:
                    lo = hi + (lo - 0x100)
                    s[TCON] |= 0x20 if k == 0 else 0x80
                t = (hi << 8) | lo
            else:
                t = (t + cnt) & 0xFFFF
            if k == 0:
                self.t0 = t
            else:
                self.t1 = t
        # АЦП
        if self.adc_done is not None and self.mc >= self.adc_done:
            v = self.adc_val.get(self.adc_ch, 512) & 0x3FF
            s[ADDATH] = v >> 2
            s[ADDATL] = (v & 3) << 6
            s[ADCON0] &= ~0x10 & 0xFF
            s[IRCON0] |= 0x01
            self.adc_done = None
        # передача байта
        if self.tx_done is not None and self.mc >= self.tx_done:
            s[S0CON] |= 0x02
            self.tx_done = None
        # фронт зуба
        while self.edge_mc is not None and self.mc >= self.edge_mc:
            self.crank_edge()
            self.edge = self.eng.next_edge()
            self.edge_mc = int(self.edge[0] / MC_S) if self.edge else None

    def crank_edge(self):
        s = self.s
        s[IRCON0] |= 0x20                       # IEX6 — внешнее 6 по фронту на P1.3
        mode = (s[CCEN] >> 6) & 3
        if mode == 1:                           # захват по фронту
            s[CCL3] = self.t2 & 0xFF
            s[CCH3] = self.t2 >> 8

    def t2_event(self):
        """Таймер 2 сменил значение: сравнения CC, CM, COMSET и переполнение."""
        s = self.s
        t = self.t2
        if t == 0:
            s[IRCON0] |= 0x40                   # TF2
        ccen = s[CCEN]
        for k in (1, 2, 3):
            if (ccen >> (2 * k)) & 3 == 2 and self.cc_val[k] == t:
                s[IRCON0] |= (0x08, 0x10, 0x20)[k - 1] if k > 0 else 0   # IEX4/5/6 для CC1/2/3
        if not s[CMSEL]:
            en = s[CMEN]
            if en:
                for i in range(8):
                    if en & (1 << i) and self.cm_val[i] == t:
                        self.set_pin(i, 1 if self.p4_sh & (1 << i) else 0)
                        s[IRCON1] |= 1 << i
        # CRC (P1.0) и CC4 (P1.4) в режиме сравнения 1: теневой бит — на ногу
        if ccen & 0x03 == 0x02 and self.crc_val == t:
            self.p1_set(0x01, 8, 1 if self.p1_sh & 0x01 else 0)
        c4 = s[CC4EN]
        if c4 & 0x06 == 0x04 and self.cc4_val == t:
            self.p1_set(0x10, 9, 1 if self.p1_sh & 0x10 else 0)
            s[IRCON0] |= 0x02                   # IEX2
        # режим 2 на P5: COMSET → 1 по SETMSK, COMCLR → 0 по CLRMSK
        if c4 & 0x80:
            pins = (2 << ((c4 >> 4) & 7)) - 1   # COCON2–0: ноги P5.0 … P5.n
            hs = ((s[COMSETH] << 8) | s[COMSETL]) == t
            hc = ((s[COMCLRH] << 8) | s[COMCLRL]) == t
            if hc:
                s[CTCON] |= 0x20                # ICR
                if c4 & 0x08:
                    old = s[P5]
                    s[P5] = old & ~(s[CLRMSK] & pins) & 0xFF
                    self.p5_log(old, s[P5])
            if hs:                              # установка важнее сброса (даташит 6.3.3.3)
                s[CTCON] |= 0x10                # ICS
                if c4 & 0x08:
                    old = s[P5]
                    s[P5] = old | (s[SETMSK] & pins)
                    self.p5_log(old, s[P5])

    # ------------------------------------------------------------ прерывания
    def irq_sources(self):
        s = self.s
        tcon, ir0, ir1 = s[TCON], s[IRCON0], s[IRCON1]
        ie0, ie1, ie2 = s[IEN0], s[IEN1], s[IEN2]
        # (группа, порядок, вектор, запрос, разрешение)
        return (
            (0, 0, VEC_IE0, tcon & 0x02, ie0 & 0x01),
            (0, 2, VEC_ADC, ir0 & 0x01, ie1 & 0x01),
            (1, 0, VEC_TF0, tcon & 0x20, ie0 & 0x02),
            (1, 2, VEC_IEX2, ir0 & 0x02, ie1 & 0x02),
            (2, 0, VEC_IE1, tcon & 0x08, ie0 & 0x04),
            (2, 1, VEC_CMP, ir1, ie2 & 0x04),
            (2, 2, VEC_IEX3, ir0 & 0x04, ie1 & 0x04),
            (3, 0, VEC_TF1, tcon & 0x80, ie0 & 0x08),
            (3, 2, VEC_IEX4, ir0 & 0x08, ie1 & 0x08),
            (4, 0, VEC_SER0, s[S0CON] & 0x03, ie0 & 0x10),
            (4, 1, VEC_ICS, s[CTCON] & 0x10, ie2 & 0x10),
            (4, 2, VEC_IEX5, ir0 & 0x10, ie1 & 0x10),
            (5, 0, VEC_TF2, ir0 & 0xC0, ie0 & 0x20),
            (5, 2, VEC_IEX6, ir0 & 0x20, ie1 & 0x20),
        )

    def irq_clear(self, vec):
        s = self.s
        if vec == VEC_IE0:
            s[TCON] &= ~0x02 & 0xFF
        elif vec == VEC_IE1:
            s[TCON] &= ~0x08 & 0xFF
        elif vec == VEC_TF0:
            s[TCON] &= ~0x20 & 0xFF
        elif vec == VEC_TF1:
            s[TCON] &= ~0x80 & 0xFF
        elif vec == VEC_IEX2:
            s[IRCON0] &= ~0x02 & 0xFF
        elif vec == VEC_IEX3:
            s[IRCON0] &= ~0x04 & 0xFF
        elif vec == VEC_IEX4:
            s[IRCON0] &= ~0x08 & 0xFF
        elif vec == VEC_IEX5:
            s[IRCON0] &= ~0x10 & 0xFF
        elif vec == VEC_IEX6:
            s[IRCON0] &= ~0x20 & 0xFF
        elif vec == VEC_ICS:
            s[CTCON] &= ~0x10 & 0xFF

    def check_irq(self):
        s = self.s
        if not s[IEN0] & 0x80:
            return
        cur = self.ilevel[-1] if self.ilevel else -1
        best = None
        ip0, ip1 = s[IP0], s[IP1]
        for grp, order, vec, req, en in self.irq_sources():
            if not (req and en):
                continue
            lvl = (((ip1 >> grp) & 1) << 1) | ((ip0 >> grp) & 1)
            if lvl <= cur:
                continue
            key = (-lvl, grp, order)
            if best is None or key < best[0]:
                best = (key, vec, lvl)
        if best is None:
            return
        _, vec, lvl = best
        self.irq_clear(vec)
        self.push(self.pc & 0xFF)
        self.push(self.pc >> 8)
        self.pc = vec
        self.ilevel.append(lvl)
        self.isr_start.append((vec, self.mc))
        self.tick(2)

    # ------------------------------------------------------------ выполнение
    def rel(self, off):
        return (self.pc + (off - 256 if off >= 128 else off)) & 0xFFFF

    def step(self):
        c = self.code
        pc = self.pc
        op = c[pc]
        b1 = c[(pc + 1) & 0xFFFF]
        b2 = c[(pc + 2) & 0xFFFF]
        s = self.s
        r = self.r
        bk = s[PSW] & 0x18
        lo = op & 0x0F
        hi = op >> 4
        cyc = 1
        if self.trace_hook:
            self.trace_hook(self, pc)

        def rn():
            return bk + (op & 7)

        def ri():
            return r[bk + (op & 1)]

        if op & 0x1F == 0x01:                               # AJMP
            self.pc = ((pc + 2) & 0xF800) | ((op >> 5) << 8) | b1
            cyc = 2
        elif op & 0x1F == 0x11:                             # ACALL
            ret = pc + 2
            self.push(ret & 0xFF)
            self.push(ret >> 8)
            self.pc = (ret & 0xF800) | ((op >> 5) << 8) | b1
            cyc = 2
        elif op == 0x00:
            self.pc = pc + 1
        elif op == 0x02:
            self.pc = (b1 << 8) | b2
            cyc = 2
        elif op == 0x12:
            ret = pc + 3
            self.push(ret & 0xFF)
            self.push(ret >> 8)
            self.pc = (b1 << 8) | b2
            cyc = 2
        elif op == 0x22 or op == 0x32:
            h = self.pop()
            l = self.pop()
            self.pc = (h << 8) | l
            cyc = 2
            if op == 0x32:
                if self.ilevel:
                    self.ilevel.pop()
                if self.isr_start:
                    vec, t0 = self.isr_start.pop()
                    st = self.isr_time.setdefault(vec, [0, 0, 0])
                    d = self.mc + 2 - t0
                    st[0] += 1
                    st[1] += d
                    st[2] = max(st[2], d)
                self.skip_irq = True
        elif op == 0x03:                                    # RR A
            a = s[ACC]
            s[ACC] = ((a >> 1) | (a << 7)) & 0xFF
            self.pc = pc + 1
        elif op == 0x13:                                    # RRC A
            a = s[ACC]
            c0 = a & 1
            s[ACC] = (a >> 1) | (self.cy() << 7)
            self.set_cy(c0)
            self.pc = pc + 1
        elif op == 0x23:                                    # RL A
            a = s[ACC]
            s[ACC] = ((a << 1) | (a >> 7)) & 0xFF
            self.pc = pc + 1
        elif op == 0x33:                                    # RLC A
            a = s[ACC]
            c7 = a >> 7
            s[ACC] = ((a << 1) | self.cy()) & 0xFF
            self.set_cy(c7)
            self.pc = pc + 1
        elif op == 0x04:
            s[ACC] = (s[ACC] + 1) & 0xFF
            self.pc = pc + 1
        elif op == 0x14:
            s[ACC] = (s[ACC] - 1) & 0xFF
            self.pc = pc + 1
        elif op in (0x05, 0x15):                            # INC/DEC direct
            d = 1 if op == 0x05 else -1
            self.set_dir(b1, self.get_dir(b1, rmw=True) + d)
            self.pc = pc + 2
        elif op in (0x06, 0x07, 0x16, 0x17):
            d = 1 if op < 0x10 else -1
            a = ri()
            r[a] = (r[a] + d) & 0xFF
            self.pc = pc + 1
        elif 0x08 <= op <= 0x0F or 0x18 <= op <= 0x1F:
            d = 1 if op < 0x10 else -1
            a = rn()
            r[a] = (r[a] + d) & 0xFF
            self.pc = pc + 1
        elif op in (0x10, 0x20, 0x30):                      # JBC / JB / JNB
            self.pc = pc + 3
            bit = self.get_bit(b1, rmw=(op == 0x10))
            if op == 0x10:
                if bit:
                    self.set_bit(b1, 0)
                    self.pc = self.rel(b2)
            elif op == 0x20:
                if bit:
                    self.pc = self.rel(b2)
            else:
                if not bit:
                    self.pc = self.rel(b2)
            cyc = 2
        elif op in (0x40, 0x50, 0x60, 0x70):
            self.pc = pc + 2
            cond = {0x40: self.cy() == 1, 0x50: self.cy() == 0, 0x60: s[ACC] == 0, 0x70: s[ACC] != 0}[op]
            if cond:
                self.pc = self.rel(b1)
            cyc = 2
        elif op == 0x80:
            self.pc = pc + 2
            self.pc = self.rel(b1)
            cyc = 2
        elif op == 0x73:
            self.pc = (s[ACC] + self.dptr[s[DPSEL] & 7]) & 0xFFFF
            cyc = 2
        elif hi in (2, 3, 4, 5, 6, 9) and lo >= 4:          # арифметика/логика с A
            if lo == 4:
                v = b1
                ln = 2
            elif lo == 5:
                v = self.get_dir(b1)
                ln = 2
            elif lo in (6, 7):
                v = r[ri()]
                ln = 1
            else:
                v = r[rn()]
                ln = 1
            a = s[ACC]
            if hi == 2:
                s[ACC] = self.add(a, v)
            elif hi == 3:
                s[ACC] = self.add(a, v, self.cy())
            elif hi == 4:
                s[ACC] = a | v
            elif hi == 5:
                s[ACC] = a & v
            elif hi == 6:
                s[ACC] = a ^ v
            else:
                s[ACC] = self.subb(a, v)
            self.pc = pc + ln
        elif hi in (4, 5, 6) and lo in (2, 3):              # ORL/ANL/XRL direct
            cur = self.get_dir(b1, rmw=True)
            v = s[ACC] if lo == 2 else b2
            nv = cur | v if hi == 4 else (cur & v if hi == 5 else cur ^ v)
            self.set_dir(b1, nv)
            self.pc = pc + (2 if lo == 2 else 3)
            cyc = 1 if lo == 2 else 2
        elif op == 0x72:                                    # ORL C,bit
            self.set_cy(self.cy() | self.get_bit(b1))
            self.pc = pc + 2
            cyc = 2
        elif op == 0x82:                                    # ANL C,bit
            self.set_cy(self.cy() & self.get_bit(b1))
            self.pc = pc + 2
            cyc = 2
        elif op == 0xA0:                                    # ORL C,/bit
            self.set_cy(self.cy() | (1 - self.get_bit(b1)))
            self.pc = pc + 2
            cyc = 2
        elif op == 0xB0:                                    # ANL C,/bit
            self.set_cy(self.cy() & (1 - self.get_bit(b1)))
            self.pc = pc + 2
            cyc = 2
        elif op == 0x74:
            s[ACC] = b1
            self.pc = pc + 2
        elif op == 0x75:
            self.set_dir(b1, b2)
            self.pc = pc + 3
            cyc = 2
        elif op in (0x76, 0x77):
            r[ri()] = b1
            self.pc = pc + 2
        elif 0x78 <= op <= 0x7F:
            r[rn()] = b1
            self.pc = pc + 2
        elif op == 0x83:                                    # MOVC A,@A+PC
            s[ACC] = c[(pc + 1 + s[ACC]) & 0xFFFF]
            self.pc = pc + 1
            cyc = 2
        elif op == 0x84:                                    # DIV AB
            a, bb = s[ACC], s[B]
            s[PSW] &= 0x7B
            if bb == 0:
                s[PSW] |= 0x04
            else:
                s[ACC], s[B] = a // bb, a % bb
            self.pc = pc + 1
            cyc = 4
        elif op == 0x85:                                    # MOV dir,dir (источник b1, приёмник b2)
            self.set_dir(b2, self.get_dir(b1))
            self.pc = pc + 3
            cyc = 2
        elif op in (0x86, 0x87):
            self.set_dir(b1, r[ri()])
            self.pc = pc + 2
            cyc = 2
        elif 0x88 <= op <= 0x8F:
            self.set_dir(b1, r[rn()])
            self.pc = pc + 2
            cyc = 2
        elif op == 0x90:
            self.dptr[s[DPSEL] & 7] = (b1 << 8) | b2
            self.pc = pc + 3
            cyc = 2
        elif op == 0x92:                                    # MOV bit,C
            self.set_bit(b1, self.cy())
            self.pc = pc + 2
            cyc = 2
        elif op == 0x93:                                    # MOVC A,@A+DPTR
            s[ACC] = c[(s[ACC] + self.dptr[s[DPSEL] & 7]) & 0xFFFF]
            self.pc = pc + 1
            cyc = 2
        elif op == 0xA2:                                    # MOV C,bit
            self.set_cy(self.get_bit(b1))
            self.pc = pc + 2
        elif op == 0xA3:
            i = s[DPSEL] & 7
            self.dptr[i] = (self.dptr[i] + 1) & 0xFFFF
            self.pc = pc + 1
            cyc = 2
        elif op == 0xA4:                                    # MUL AB
            p = s[ACC] * s[B]
            s[ACC], s[B] = p & 0xFF, p >> 8
            s[PSW] = (s[PSW] & 0x7B) | (0x04 if p > 0xFF else 0)
            self.pc = pc + 1
            cyc = 4
        elif op in (0xA6, 0xA7):
            r[ri()] = self.get_dir(b1)
            self.pc = pc + 2
            cyc = 2
        elif 0xA8 <= op <= 0xAF:
            r[rn()] = self.get_dir(b1)
            self.pc = pc + 2
            cyc = 2
        elif op == 0xB2:                                    # CPL bit
            self.set_bit(b1, 1 - self.get_bit(b1, rmw=True))
            self.pc = pc + 2
        elif op == 0xB3:
            self.set_cy(1 - self.cy())
            self.pc = pc + 1
        elif 0xB4 <= op <= 0xBF:                            # CJNE
            if op == 0xB4:
                x, y = s[ACC], b1
            elif op == 0xB5:
                x, y = s[ACC], self.get_dir(b1)
            elif op in (0xB6, 0xB7):
                x, y = r[ri()], b1
            else:
                x, y = r[rn()], b1
            self.set_cy(1 if x < y else 0)
            self.pc = pc + 3
            if x != y:
                self.pc = self.rel(b2)
            cyc = 2
        elif op == 0xC0:
            self.push(self.get_dir(b1))
            self.pc = pc + 2
            cyc = 2
        elif op == 0xC2:
            self.set_bit(b1, 0)
            self.pc = pc + 2
        elif op == 0xC3:
            self.set_cy(0)
            self.pc = pc + 1
        elif op == 0xC4:
            a = s[ACC]
            s[ACC] = ((a << 4) | (a >> 4)) & 0xFF
            self.pc = pc + 1
        elif op == 0xC5:
            v = self.get_dir(b1)
            self.set_dir(b1, s[ACC])
            s[ACC] = v
            self.pc = pc + 2
        elif op in (0xC6, 0xC7):
            a = ri()
            r[a], s[ACC] = s[ACC], r[a]
            self.pc = pc + 1
        elif 0xC8 <= op <= 0xCF:
            a = rn()
            r[a], s[ACC] = s[ACC], r[a]
            self.pc = pc + 1
        elif op == 0xD0:
            self.set_dir(b1, self.pop())
            self.pc = pc + 2
            cyc = 2
        elif op == 0xD2:
            self.set_bit(b1, 1)
            self.pc = pc + 2
        elif op == 0xD3:
            self.set_cy(1)
            self.pc = pc + 1
        elif op == 0xD4:                                    # DA A
            a = s[ACC]
            cyv = self.cy()
            if (a & 0x0F) > 9 or s[PSW] & 0x40:
                a += 6
            if (a >> 4) > 9 or cyv or a > 0xFF:
                a += 0x60
            if a > 0xFF:
                cyv = 1
            s[ACC] = a & 0xFF
            self.set_cy(cyv)
            self.pc = pc + 1
        elif op == 0xD5:                                    # DJNZ direct
            v = (self.get_dir(b1, rmw=True) - 1) & 0xFF
            self.set_dir(b1, v)
            self.pc = pc + 3
            if v:
                self.pc = self.rel(b2)
            cyc = 2
        elif op in (0xD6, 0xD7):                            # XCHD
            a = ri()
            v = r[a]
            acc = s[ACC]
            r[a] = (v & 0xF0) | (acc & 0x0F)
            s[ACC] = (acc & 0xF0) | (v & 0x0F)
            self.pc = pc + 1
        elif 0xD8 <= op <= 0xDF:                            # DJNZ Rn
            a = rn()
            r[a] = (r[a] - 1) & 0xFF
            self.pc = pc + 2
            if r[a]:
                self.pc = self.rel(b1)
            cyc = 2
        elif op == 0xE0:
            s[ACC] = self.x[self.dptr[s[DPSEL] & 7]]
            self.pc = pc + 1
            cyc = 2
        elif op in (0xE2, 0xE3):                            # MOVX A,@Ri (страница P2)
            s[ACC] = self.x[(s[P2] << 8) | ri()]
            self.pc = pc + 1
            cyc = 2
        elif op == 0xE4:
            s[ACC] = 0
            self.pc = pc + 1
        elif op == 0xE5:
            s[ACC] = self.get_dir(b1)
            self.pc = pc + 2
        elif op in (0xE6, 0xE7):
            s[ACC] = r[ri()]
            self.pc = pc + 1
        elif 0xE8 <= op <= 0xEF:
            s[ACC] = r[rn()]
            self.pc = pc + 1
        elif op == 0xF0:
            self.x[self.dptr[s[DPSEL] & 7]] = s[ACC]
            self.pc = pc + 1
            cyc = 2
        elif op in (0xF2, 0xF3):
            self.x[(s[P2] << 8) | ri()] = s[ACC]
            self.pc = pc + 1
            cyc = 2
        elif op == 0xF4:
            s[ACC] = (~s[ACC]) & 0xFF
            self.pc = pc + 1
        elif op == 0xF5:
            self.set_dir(b1, s[ACC])
            self.pc = pc + 2
        elif op in (0xF6, 0xF7):
            r[ri()] = s[ACC]
            self.pc = pc + 1
        elif 0xF8 <= op <= 0xFF:
            r[rn()] = s[ACC]
            self.pc = pc + 1
        elif op == 0xE4:
            s[ACC] = 0
            self.pc = pc + 1
        else:
            raise Stop('неизвестная команда %02X @%04X' % (op, pc))

        # PDIR действует только на одну следующую команду после установки
        self.pdir = 1 if self.pdir_set else 0
        self.pdir_set = False
        self.tick(cyc)
        if self.skip_irq:
            self.skip_irq = False
        else:
            self.check_irq()

    def run(self, seconds, stop_pc=None):
        end = int(seconds / MC_S)
        while self.mc < end:
            self.step()
            if stop_pc is not None and self.pc == stop_pc:
                return


# ------------------------------------------------------------------ отчёт
OUT_NAMES = {0: 'P4.0/CM0', 1: 'P4.1/CM1', 2: 'P4.2/CM2', 3: 'P4.3/CM3', 4: 'P4.4/CM4', 5: 'P4.5/CM5',
             6: 'P4.6/CM6', 7: 'P4.7/CM7', 8: 'P1.0/CRC', 9: 'P1.4/CC4', 10: 'P5.1', 11: 'P5.7', 12: 'P5.6'}


def parse_outs(spec, default_act):
    """«4,5,10:1» → [(4, акт.уровень), ...]; уровень по умолчанию — из default_act(выход)."""
    res = []
    for item in filter(None, spec.split(',')):
        if ':' in item:
            o, lv = item.split(':')
            res.append((int(o), int(lv)))
        else:
            res.append((int(item), default_act(int(item))))
    return res


def report(cpu, eng, tdc_teeth, last_rev, ign_bits, inj_bits):
    log = cpu.p4_log
    t_end = cpu.mc * MC_S
    rpm = eng.rpm_at(t_end)
    rev_t = 60.0 / rpm
    t_from = t_end - last_rev * rev_t
    tdcs = [z * 6.0 for z in tdc_teeth]

    def btdc(a):
        """Угол до ближайшей следующей ВМТ из списка (в обороте 360°)."""
        a360 = a % 360.0
        best = None
        for t in tdcs:
            d = (t - a360) % 360.0
            if d > 180.0:
                d -= 360.0
            if best is None or abs(d) < abs(best[0]):
                best = (d, t)
        return best

    print('\n=== Обороты %d об/мин, время %.3f с, разбор последних %d оборотов ===' % (rpm, t_end, last_rev))
    print('ВМТ (зуб от пропуска): %s' % ', '.join(str(z) for z in tdc_teeth))
    print('\nЗажигание (активный уровень — зарядка, обратный фронт — искра):')
    for b, act in ign_bits:
        ev = [(mc * MC_S, lvl) for mc, bit, lvl in log if bit == b and mc * MC_S >= t_from]
        lines = []
        start = None
        for t, lvl in ev:
            if lvl == act:
                start = t
            elif start is not None:
                a = eng.angle_at(t)
                d, tz = btdc(a)
                lines.append('искра %6.1f° до ВМТ%3d (угол %6.1f), накопление %.2f мс'
                             % (d, int(tz / 6), a % 720.0, (t - start) * 1000))
                start = None
        print('  %s: %s' % (OUT_NAMES.get(b, b), ('\n        '.join(lines)) if lines else 'нет событий'))
    print('\nВпрыск (активный уровень — открыта):')
    for b, act in inj_bits:
        ev = [(mc * MC_S, lvl) for mc, bit, lvl in log if bit == b and mc * MC_S >= t_from]
        lines = []
        start = None
        for t, lvl in ev:
            if lvl == act:
                start = t
            elif start is not None:
                a = eng.angle_at(start)
                lines.append('открытие на угле %6.1f (в цикле 720°), %.3f мс' % (a % 720.0, (t - start) * 1000))
                start = None
        print('  %s: %s' % (OUT_NAMES.get(b, b), ('\n        '.join(lines)) if lines else 'нет событий'))
    print('\nПрерывания (число, среднее / максимум, мкс):')
    for vec, (n, tot, mx) in sorted(cpu.isr_time.items()):
        print('  %04X %-14s %7d  %6.1f / %6.1f' % (vec, VEC_NAMES.get(vec, ''), n, tot / n * MC_S * 1e6, mx * MC_S * 1e6))
    tooth_us = 1e6 / rpm
    print('  период зуба на этих оборотах: %.1f мкс' % tooth_us)
    r, x = cpu.r, cpu.x
    print('\nСостояние: R6=%d R7=%d такт 40h=%d 43h=%d 41h=%d  05h=%d  21h=%02X 2Ah=%02X 2Bh=%02X  69h=%d 68h=%d'
          % (r[0x1E], r[0x1F], r[0x40], r[0x43], r[0x41], r[0x05], r[0x21], r[0x2A], r[0x2B], r[0x69], r[0x68]))
    print('  F94A (обороты/5) = %d, 55h = %d, УОЗ 62h = %d, накопление F84D = %d, F800 = %d зуб.'
          % (x[0xF94A] | (x[0xF94B] << 8), r[0x55], r[0x62], x[0xF84D], x[0xF800]))
    print('  записи искры 80h–8Fh: %s' % ' '.join('%02X' % r[0x80 + i] for i in range(16)))
    print('  слоты 10h–17h: %s' % ' '.join('%02X' % r[0x10 + i] for i in range(8)))


def main():
    ap = argparse.ArgumentParser(description='Эмулятор Января 7.2 (C509) для прошивки j7es')
    ap.add_argument('bin')
    ap.add_argument('--rpm', type=float, default=800, help='обороты после пуска')
    ap.add_argument('--crank', type=float, default=250, help='обороты прокрутки')
    ap.add_argument('--crank-sec', type=float, default=1.0, help='сколько секунд прокрутка')
    ap.add_argument('--sec', type=float, default=3.0, help='общее время, с')
    ap.add_argument('--no-cam', action='store_true', help='без датчика фаз')
    ap.add_argument('--adc', default='', help='коды АЦП: канал=код,... (0..1023)')
    ap.add_argument('--patch', default='', help='правки образа: адрес=байт,... (hex)')
    ap.add_argument('--tdc', default='18,48', help='зубья ВМТ от пропуска для отчёта')
    ap.add_argument('--rev', type=int, default=2, help='сколько последних оборотов разбирать')
    ap.add_argument('--ign', default='4,5,6,7', help='выходы катушек (0–7 P4, 10 P5.1, 11 P5.7, 12 P5.6), можно «вых:уровень зарядки»')
    ap.add_argument('--inj', default='0,1,2,3', help='выходы форсунок (0–3 P4, 8 P1.0, 9 P1.4), можно «вых:уровень открытия»')
    ap.add_argument('--cam-off', type=float, default=0.0, help='сдвиг сигнала фазы, градусы')
    a = ap.parse_args()

    code = bytearray(open(a.bin, 'rb').read())
    if len(code) != 65536:
        sys.exit('ожидается образ 65536 байт')
    for item in filter(None, a.patch.split(',')):
        addr, val = item.split('=')
        code[int(addr, 16)] = int(val, 16)
    adc = {k: 512 for k in range(16)}
    adc[1] = 60             # канал 1 — дроссель (закрыт; при 512 на пуске продувка, впрыска нет)
    adc[7] = 0              # канал 7 — детонация
    for item in filter(None, a.adc.split(',')):
        k, v = item.split('=')
        adc[int(k)] = int(v)
    profile = [(0.0, a.crank), (a.crank_sec, a.rpm)]
    eng = Engine(profile, cam=not a.no_cam, cam_off=a.cam_off)
    cpu = C509(code, eng, adc, {})
    try:
        cpu.run(a.sec)
    except Stop as e:
        print('ОСТАНОВ:', e)
    except IndexError as e:
        print('ОСТАНОВ: выход за память @%04X: %s' % (cpu.pc, e))
    report(cpu, eng, [int(z) for z in a.tdc.split(',')], a.rev,
           parse_outs(a.ign, lambda o: 1 if o >= 10 else 0),
           parse_outs(a.inj, lambda o: 1 if o in (8, 9) else 0))
    if cpu.tx:
        print('\nПередано в порт 0: %d байт' % len(cpu.tx))


if __name__ == '__main__':
    main()
