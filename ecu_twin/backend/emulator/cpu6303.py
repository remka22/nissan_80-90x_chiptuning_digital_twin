# -*- coding: utf-8 -*-
"""
Ядро процессора Hitachi HD6303 (расширение 6801/6301) — исполнитель инструкций.
Big-endian, 16-битное адресное пространство. Реализован документированный набор
команд + 6303-расширения (AIM/OIM/EIM/TIM, XGDX, MUL, ADDD/SUBD, LDD/STD и т.д.).

Цель — SIL-двойник прошивки ЭБУ: гоняем реальный код, смотрим ветки и результат.
Память подаётся снаружи (класс Bus) — так регистры железа (ADC, порты) можно
перехватывать. CPU сам ничего про железо не знает.
"""


class CPU6303:
    # Биты CCR: 1 1 H I N Z V C  (bit5..bit0)
    def __init__(self, bus):
        self.bus = bus            # объект с read8(addr)/write8(addr,val)
        self.A = 0
        self.B = 0
        self.X = 0
        self.SP = 0x01FF
        self.PC = 0
        self.H = 0
        self.I = 0
        self.N = 0
        self.Z = 0
        self.V = 0
        self.C = 0
        self.cycles = 0
        self.instr = 0
        self.halted = False       # SLP/WAI
        self.trace = None         # если задать список — туда пишем (pc, opcode)

    # ---- D = A:B ----
    @property
    def D(self):
        return ((self.A << 8) | self.B) & 0xFFFF

    @D.setter
    def D(self, v):
        v &= 0xFFFF
        self.A = (v >> 8) & 0xFF
        self.B = v & 0xFF

    # ---- CCR упаковка ----
    def get_ccr(self):
        return (0xC0 | (self.H << 5) | (self.I << 4) | (self.N << 3)
                | (self.Z << 2) | (self.V << 1) | self.C)

    def set_ccr(self, v):
        self.H = (v >> 5) & 1
        self.I = (v >> 4) & 1
        self.N = (v >> 3) & 1
        self.Z = (v >> 2) & 1
        self.V = (v >> 1) & 1
        self.C = v & 1

    # ---- доступ к памяти ----
    def rd8(self, a):
        return self.bus.read8(a & 0xFFFF) & 0xFF

    def wr8(self, a, v):
        self.bus.write8(a & 0xFFFF, v & 0xFF)

    def rd16(self, a):
        return ((self.rd8(a) << 8) | self.rd8(a + 1)) & 0xFFFF

    def wr16(self, a, v):
        self.wr8(a, (v >> 8) & 0xFF)
        self.wr8(a + 1, v & 0xFF)

    def fetch8(self):
        v = self.rd8(self.PC)
        self.PC = (self.PC + 1) & 0xFFFF
        return v

    def fetch16(self):
        v = self.rd16(self.PC)
        self.PC = (self.PC + 2) & 0xFFFF
        return v

    # ---- стек (растёт вниз) ----
    def push8(self, v):
        self.wr8(self.SP, v)
        self.SP = (self.SP - 1) & 0xFFFF

    def pull8(self):
        self.SP = (self.SP + 1) & 0xFFFF
        return self.rd8(self.SP)

    def push16(self, v):
        # сначала low, потом high (так RTS читает high первым)
        self.push8(v & 0xFF)
        self.push8((v >> 8) & 0xFF)

    def pull16(self):
        hi = self.pull8()
        lo = self.pull8()
        return ((hi << 8) | lo) & 0xFFFF

    # ---- флаги ----
    def setNZ8(self, r):
        self.N = 1 if (r & 0x80) else 0
        self.Z = 1 if (r & 0xFF) == 0 else 0

    def setNZ16(self, r):
        self.N = 1 if (r & 0x8000) else 0
        self.Z = 1 if (r & 0xFFFF) == 0 else 0

    # ---- арифметика 8 бит ----
    def add8(self, a, b, carry=0):
        r = a + b + carry
        self.H = 1 if ((a & 0xF) + (b & 0xF) + carry) > 0xF else 0
        self.C = 1 if r > 0xFF else 0
        rr = r & 0xFF
        self.V = 1 if ((a ^ b) & 0x80) == 0 and ((a ^ rr) & 0x80) else 0
        self.setNZ8(rr)
        return rr

    def sub8(self, a, b, borrow=0):
        r = a - b - borrow
        self.C = 1 if r < 0 else 0          # C = borrow
        rr = r & 0xFF
        self.V = 1 if ((a ^ b) & 0x80) and ((a ^ rr) & 0x80) else 0
        self.setNZ8(rr)
        return rr

    def cmp8(self, a, b):
        self.sub8(a, b, 0)                  # как sub, но без сохранения

    # ---- арифметика 16 бит (ADDD/SUBD) ----
    def add16(self, a, b):
        r = a + b
        self.C = 1 if r > 0xFFFF else 0
        rr = r & 0xFFFF
        self.V = 1 if ((a ^ b) & 0x8000) == 0 and ((a ^ rr) & 0x8000) else 0
        self.setNZ16(rr)
        return rr

    def sub16(self, a, b):
        r = a - b
        self.C = 1 if r < 0 else 0
        rr = r & 0xFFFF
        self.V = 1 if ((a ^ b) & 0x8000) and ((a ^ rr) & 0x8000) else 0
        self.setNZ16(rr)
        return rr

    # ---- логика ----
    def _logicNZ(self, r):
        self.V = 0
        self.setNZ8(r)
        return r & 0xFF

    # ---- RMW операции (возвращают результат, флаги ставят) ----
    def op_neg(self, m):
        r = self.sub8(0, m, 0)
        return r

    def op_com(self, m):
        r = (~m) & 0xFF
        self.V = 0
        self.C = 1
        self.setNZ8(r)
        return r

    def op_lsr(self, m):
        self.C = m & 1
        r = (m >> 1) & 0xFF
        self.N = 0
        self.Z = 1 if r == 0 else 0
        self.V = self.N ^ self.C
        return r

    def op_ror(self, m):
        c = self.C
        self.C = m & 1
        r = ((m >> 1) | (c << 7)) & 0xFF
        self.setNZ8(r)
        self.V = self.N ^ self.C
        return r

    def op_asr(self, m):
        self.C = m & 1
        r = ((m >> 1) | (m & 0x80)) & 0xFF
        self.setNZ8(r)
        self.V = self.N ^ self.C
        return r

    def op_asl(self, m):
        self.C = 1 if (m & 0x80) else 0
        r = (m << 1) & 0xFF
        self.setNZ8(r)
        self.V = self.N ^ self.C
        return r

    def op_rol(self, m):
        c = self.C
        self.C = 1 if (m & 0x80) else 0
        r = ((m << 1) | c) & 0xFF
        self.setNZ8(r)
        self.V = self.N ^ self.C
        return r

    def op_dec(self, m):
        r = (m - 1) & 0xFF
        self.V = 1 if m == 0x80 else 0
        self.setNZ8(r)
        return r

    def op_inc(self, m):
        r = (m + 1) & 0xFF
        self.V = 1 if m == 0x7F else 0
        self.setNZ8(r)
        return r

    def op_tst(self, m):
        self.V = 0
        self.C = 0
        self.setNZ8(m)
        return m

    def op_clr(self, m):
        self.N = 0
        self.Z = 1
        self.V = 0
        self.C = 0
        return 0

    # ---- адресации ----
    def ea_direct(self):
        return self.fetch8()

    def ea_extended(self):
        return self.fetch16()

    def ea_indexed(self):
        return (self.X + self.fetch8()) & 0xFFFF

    # =====================================================================
    #  Главный шаг
    # =====================================================================
    def step(self):
        if self.halted:
            return
        pc0 = self.PC
        op = self.fetch8()
        if self.trace is not None:
            self.trace.append((pc0, op))
        self.instr += 1

        # ---- 0x20-0x2F: ветвления ----
        if 0x20 <= op <= 0x2F:
            self._branch(op)
            return

        # ---- 0x80-0xFF: аккумулятор + память (регулярная сетка) ----
        if op >= 0x80:
            self._acc_mem(op)
            return

        # ---- 0x00-0x1F: inherent группа 1 ----
        if op < 0x20:
            self._inherent1(op)
            return

        # ---- 0x30-0x3F: inherent группа 2 (стек/индекс) ----
        if 0x30 <= op <= 0x3F:
            self._inherent2(op)
            return

        # ---- 0x40-0x5F: RMW над аккумулятором ----
        if 0x40 <= op <= 0x5F:
            self._acc_rmw(op)
            return

        # ---- 0x60-0x7F: RMW над памятью + bit-ops + JMP ----
        if 0x60 <= op <= 0x7F:
            self._mem_rmw(op)
            return

        raise RuntimeError("неизвестный опкод 0x%02X @ 0x%04X" % (op, pc0))

    # ---------------------------------------------------------------
    def _branch(self, op):
        rel = self.fetch8()
        if rel > 127:
            rel -= 256
        target = (self.PC + rel) & 0xFFFF
        take = {
            0x20: True,                                   # BRA
            0x21: False,                                  # BRN
            0x22: (self.C == 0 and self.Z == 0),          # BHI
            0x23: (self.C == 1 or self.Z == 1),           # BLS
            0x24: (self.C == 0),                          # BCC
            0x25: (self.C == 1),                          # BCS
            0x26: (self.Z == 0),                          # BNE
            0x27: (self.Z == 1),                          # BEQ
            0x28: (self.V == 0),                          # BVC
            0x29: (self.V == 1),                          # BVS
            0x2A: (self.N == 0),                          # BPL
            0x2B: (self.N == 1),                          # BMI
            0x2C: ((self.N ^ self.V) == 0),               # BGE
            0x2D: ((self.N ^ self.V) == 1),               # BLT
            0x2E: (self.Z == 0 and (self.N ^ self.V) == 0),  # BGT
            0x2F: (self.Z == 1 or (self.N ^ self.V) == 1),   # BLE
        }[op]
        if take:
            self.PC = target

    # ---------------------------------------------------------------
    def _inherent1(self, op):
        if op == 0x01:                                   # NOP
            pass
        elif op == 0x04:                                 # LSRD
            d = self.D
            self.C = d & 1
            d = (d >> 1) & 0xFFFF
            self.D = d
            self.N = 0
            self.Z = 1 if d == 0 else 0
            self.V = self.N ^ self.C
        elif op == 0x05:                                 # ASLD/LSLD
            d = self.D
            self.C = 1 if (d & 0x8000) else 0
            d = (d << 1) & 0xFFFF
            self.D = d
            self.setNZ16(d)
            self.V = self.N ^ self.C
        elif op == 0x06:                                 # TAP
            self.set_ccr(self.A)
        elif op == 0x07:                                 # TPA
            self.A = self.get_ccr()
        elif op == 0x08:                                 # INX
            self.X = (self.X + 1) & 0xFFFF
            self.Z = 1 if self.X == 0 else 0
        elif op == 0x09:                                 # DEX
            self.X = (self.X - 1) & 0xFFFF
            self.Z = 1 if self.X == 0 else 0
        elif op == 0x0A:                                 # CLV
            self.V = 0
        elif op == 0x0B:                                 # SEV
            self.V = 1
        elif op == 0x0C:                                 # CLC
            self.C = 0
        elif op == 0x0D:                                 # SEC
            self.C = 1
        elif op == 0x0E:                                 # CLI
            self.I = 0
        elif op == 0x0F:                                 # SEI
            self.I = 1
        elif op == 0x10:                                 # SBA
            self.A = self.sub8(self.A, self.B, 0)
        elif op == 0x11:                                 # CBA
            self.cmp8(self.A, self.B)
        elif op == 0x16:                                 # TAB
            self.B = self.A
            self._logicNZ(self.B)
        elif op == 0x17:                                 # TBA
            self.A = self.B
            self._logicNZ(self.A)
        elif op == 0x18:                                 # XGDX
            d = self.D
            self.D = self.X
            self.X = d
        elif op == 0x19:                                 # DAA
            self._daa()
        elif op == 0x1A:                                 # SLP
            self.halted = True
        elif op == 0x1B:                                 # ABA
            self.A = self.add8(self.A, self.B, 0)
        else:
            raise RuntimeError("inherent1 0x%02X не реализован" % op)

    def _daa(self):
        a = self.A
        corr = 0
        if self.H or (a & 0x0F) > 9:
            corr |= 0x06
        if self.C or (a >> 4) > 9 or ((a >> 4) >= 9 and (a & 0x0F) > 9):
            corr |= 0x60
            self.C = 1
        a = (a + corr) & 0xFF
        self.A = a
        self.setNZ8(a)

    # ---------------------------------------------------------------
    def _inherent2(self, op):
        if op == 0x30:                                   # TSX
            self.X = (self.SP + 1) & 0xFFFF
        elif op == 0x31:                                 # INS
            self.SP = (self.SP + 1) & 0xFFFF
        elif op == 0x32:                                 # PULA
            self.A = self.pull8()
        elif op == 0x33:                                 # PULB
            self.B = self.pull8()
        elif op == 0x34:                                 # DES
            self.SP = (self.SP - 1) & 0xFFFF
        elif op == 0x35:                                 # TXS
            self.SP = (self.X - 1) & 0xFFFF
        elif op == 0x36:                                 # PSHA
            self.push8(self.A)
        elif op == 0x37:                                 # PSHB
            self.push8(self.B)
        elif op == 0x38:                                 # PULX
            self.X = self.pull16()
        elif op == 0x39:                                 # RTS
            self.PC = self.pull16()
        elif op == 0x3A:                                 # ABX
            self.X = (self.X + self.B) & 0xFFFF
        elif op == 0x3B:                                 # RTI
            self.set_ccr(self.pull8())
            self.B = self.pull8()
            self.A = self.pull8()
            self.X = self.pull16()
            self.PC = self.pull16()
        elif op == 0x3C:                                 # PSHX
            self.push16(self.X)
        elif op == 0x3D:                                 # MUL
            r = self.A * self.B
            self.D = r
            self.C = 1 if (r & 0x80) else 0              # C = bit7 результата
        elif op == 0x3E:                                 # WAI
            self.halted = True
        elif op == 0x3F:                                 # SWI
            self._swi()
        else:
            raise RuntimeError("inherent2 0x%02X не реализован" % op)

    def _swi(self):
        self.push16(self.PC)
        self.push16(self.X)
        self.push8(self.A)
        self.push8(self.B)
        self.push8(self.get_ccr())
        self.I = 1
        self.PC = self.rd16(0xFFFA)

    def irq(self, vec_addr):
        """Аппаратное прерывание: сохраняем состояние, маскируем, прыгаем по вектору.
        Порядок push совпадает с RTI (CCR,B,A,X,PC при выходе)."""
        self.halted = False
        self.push16(self.PC)
        self.push16(self.X)
        self.push8(self.A)
        self.push8(self.B)
        self.push8(self.get_ccr())
        self.I = 1
        self.PC = self.rd16(vec_addr)

    # ---------------------------------------------------------------
    def _acc_rmw(self, op):
        # 0x40-0x4F -> A, 0x50-0x5F -> B
        reg = 'A' if op < 0x50 else 'B'
        lo = op & 0x0F
        val = self.A if reg == 'A' else self.B
        fn = {
            0x0: self.op_neg, 0x3: self.op_com, 0x4: self.op_lsr,
            0x6: self.op_ror, 0x7: self.op_asr, 0x8: self.op_asl,
            0x9: self.op_rol, 0xA: self.op_dec, 0xC: self.op_inc,
            0xD: self.op_tst, 0xF: self.op_clr,
        }.get(lo)
        if fn is None:
            raise RuntimeError("acc_rmw 0x%02X не реализован" % op)
        r = fn(val)
        if lo != 0xD:                                    # TST не пишет
            if reg == 'A':
                self.A = r
            else:
                self.B = r

    # ---------------------------------------------------------------
    def _mem_rmw(self, op):
        lo = op & 0x0F
        indexed = (op < 0x70)

        # 6303 bit-операции над памятью
        if lo in (0x1, 0x2, 0x5, 0xB):
            imm = self.fetch8()
            ea = self.ea_indexed() if indexed else self.ea_direct()
            m = self.rd8(ea)
            if lo == 0x1:                                # AIM (AND)
                r = m & imm
                self._logicNZ(r)
                self.wr8(ea, r)
            elif lo == 0x2:                              # OIM (OR)
                r = m | imm
                self._logicNZ(r)
                self.wr8(ea, r)
            elif lo == 0x5:                              # EIM (EOR)
                r = m ^ imm
                self._logicNZ(r)
                self.wr8(ea, r)
            elif lo == 0xB:                              # TIM (тест, без записи)
                r = m & imm
                self._logicNZ(r)
            return

        # JMP
        if lo == 0xE:
            ea = self.ea_indexed() if indexed else self.ea_extended()
            self.PC = ea
            return

        # обычные RMW
        ea = self.ea_indexed() if indexed else self.ea_extended()
        m = self.rd8(ea)
        fn = {
            0x0: self.op_neg, 0x3: self.op_com, 0x4: self.op_lsr,
            0x6: self.op_ror, 0x7: self.op_asr, 0x8: self.op_asl,
            0x9: self.op_rol, 0xA: self.op_dec, 0xC: self.op_inc,
            0xD: self.op_tst, 0xF: self.op_clr,
        }.get(lo)
        if fn is None:
            raise RuntimeError("mem_rmw 0x%02X не реализован" % op)
        r = fn(m)
        if lo != 0xD:
            self.wr8(ea, r)

    # ---------------------------------------------------------------
    def _operand8(self, mode):
        """Вернуть 8-битный операнд по режиму. mode: 0=imm,1=dir,2=idx,3=ext."""
        if mode == 0:
            return self.fetch8()
        if mode == 1:
            return self.rd8(self.ea_direct())
        if mode == 2:
            return self.rd8(self.ea_indexed())
        return self.rd8(self.ea_extended())

    def _ea8(self, mode):
        """Адрес для store (mode 1/2/3)."""
        if mode == 1:
            return self.ea_direct()
        if mode == 2:
            return self.ea_indexed()
        return self.ea_extended()

    def _operand16(self, mode):
        if mode == 0:
            return self.fetch16()
        if mode == 1:
            return self.rd16(self.ea_direct())
        if mode == 2:
            return self.rd16(self.ea_indexed())
        return self.rd16(self.ea_extended())

    def _ea16(self, mode):
        if mode == 1:
            return self.ea_direct()
        if mode == 2:
            return self.ea_indexed()
        return self.ea_extended()

    # ---------------------------------------------------------------
    def _acc_mem(self, op):
        hi = op >> 4
        lo = op & 0x0F
        # группа A: 0x8-0xB, группа B: 0xC-0xF
        accB = hi >= 0xC
        mode = (hi - 8) % 4          # 0=imm,1=dir,2=idx,3=ext

        # --- спец-низкие-нибблы: 3,C,D,E,F (16-битные / переходы) ---
        if lo == 0x3:                # SUBD(A) / ADDD(B)
            v = self._operand16(mode)
            if not accB:             # SUBD
                self.D = self.sub16(self.D, v)
            else:                    # ADDD
                self.D = self.add16(self.D, v)
            return
        if lo == 0xC:                # CPX(A) / LDD(B)
            if not accB:             # CPX
                v = self._operand16(mode)
                self.sub16(self.X, v)   # ставит флаги, X не меняет
            else:                    # LDD
                v = self._operand16(mode)
                self.D = v
                self.setNZ16(v)
                self.V = 0
            return
        if lo == 0xD:                # BSR/JSR(A) / STD(B)
            if not accB:
                if mode == 0:        # 0x8D BSR (relative)
                    rel = self.fetch8()
                    if rel > 127:
                        rel -= 256
                    target = (self.PC + rel) & 0xFFFF
                    self.push16(self.PC)
                    self.PC = target
                else:                # JSR dir/idx/ext
                    ea = self._ea16(mode)
                    self.push16(self.PC)
                    self.PC = ea
            else:                    # STD
                ea = self._ea16(mode)
                self.wr16(ea, self.D)
                self.setNZ16(self.D)
                self.V = 0
            return
        if lo == 0xE:                # LDS(A) / LDX(B)
            v = self._operand16(mode)
            if not accB:             # LDS
                self.SP = v
            else:                    # LDX
                self.X = v
            self.setNZ16(v)
            self.V = 0
            return
        if lo == 0xF:                # STS(A) / STX(B)
            ea = self._ea16(mode)
            v = self.SP if not accB else self.X
            self.wr16(ea, v)
            self.setNZ16(v)
            self.V = 0
            return

        # --- обычные 8-битные операции ---
        if lo == 0x7:                # STAA/STAB (нет immediate)
            ea = self._ea8(mode)
            v = self.A if not accB else self.B
            self._logicNZ(v)
            self.wr8(ea, v)
            return

        v = self._operand8(mode)
        a = self.A if not accB else self.B
        if lo == 0x0:                # SUB
            r = self.sub8(a, v)
        elif lo == 0x1:              # CMP
            self.cmp8(a, v)
            return
        elif lo == 0x2:              # SBC
            r = self.sub8(a, v, self.C)
        elif lo == 0x4:              # AND
            r = self._logicNZ(a & v)
        elif lo == 0x5:              # BIT
            self._logicNZ(a & v)
            return
        elif lo == 0x6:              # LDA
            r = v
            self._logicNZ(r)
        elif lo == 0x8:              # EOR
            r = self._logicNZ(a ^ v)
        elif lo == 0x9:              # ADC
            r = self.add8(a, v, self.C)
        elif lo == 0xA:              # ORA
            r = self._logicNZ(a | v)
        elif lo == 0xB:              # ADD
            r = self.add8(a, v)
        else:
            raise RuntimeError("acc_mem 0x%02X не реализован" % op)

        if not accB:
            self.A = r & 0xFF
        else:
            self.B = r & 0xFF

    # =====================================================================
    def run(self, max_steps=2_000_000):
        n = 0
        while not self.halted and n < max_steps:
            self.step()
            n += 1
        return n
