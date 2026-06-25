# -*- coding: utf-8 -*-
"""
Машина ЭБУ: 64К адресного пространства, ROM сверху, перехват регистров железа,
прогон рутины с подставленными входами, свипы параметров.
"""
from .cpu6303 import CPU6303


class Bus:
    """Память + перехват аппаратных регистров (ADC, таймер HD6303, порты)."""
    def __init__(self):
        self.mem = bytearray(0x10000)
        self.adc = {ch: 0 for ch in range(9)}  # каналы ADC 0-8; 0 = MAF
        self.adc_mux = 0                      # выбранный канал (из MUX-записи в $1006)
        self.adc_result = [0, 0, 0, 0]        # 4 регистра-результата (канал&3 -> слот)
        self.port2000 = 0x00                  # порт положения коленвала
        self.io_writes = []
        # --- таймер HD6303 ---
        self.counter = 0x0000                 # free-running counter ($09/$0A)
        self.icr = 0x0000                     # input capture register ($0D/$0E)
        self.tcsr_enable = 0x16               # как пишет прошивка (EICI+ETOI+IEDG)
        self.icf = 0                          # input capture flag
        self.ocf = 0
        self.tof = 0                          # timer overflow flag

    def read8(self, a):
        a &= 0xFFFF
        # --- таймер ---
        if a == 0x08:                         # TCSR: флаги + enable-биты
            return (self.icf << 7) | (self.ocf << 6) | (self.tof << 5) | self.tcsr_enable
        if a == 0x09:                         # счётчик high (чтение очищает TOF)
            self.tof = 0
            return (self.counter >> 8) & 0xFF
        if a == 0x0A:
            return self.counter & 0xFF
        if a == 0x0D:                         # ICR high (чтение очищает ICF)
            self.icf = 0
            return (self.icr >> 8) & 0xFF
        if a == 0x0E:
            return self.icr & 0xFF
        # --- ADC с MUX ---
        # Прошивка выбирает канал записью в $1006 (0x20+канал), потом читает результат
        # из одного из 4 регистров ($1007/9/B/D hi, $1008/A/C/E lo). Какой регистр —
        # неважно: отдаём значение ВЫБРАННОГО MUX-канала (он только что сконвертирован).
        if a == 0x1006:
            return 0x80                       # бит7=1: преобразование готово
        if a in (0x1007, 0x1009, 0x100B, 0x100D):
            return (self.adc_result[(a - 0x1007) // 2] >> 8) & 0xFF   # старший слота
        if a in (0x1008, 0x100A, 0x100C, 0x100E):
            return self.adc_result[(a - 0x1008) // 2] & 0xFF          # младший слота
        # --- порт положения ---
        if a == 0x2000:
            return self.port2000
        return self.mem[a]

    def write8(self, a, v):
        a &= 0xFFFF
        v &= 0xFF
        if a == 0x08:                         # запись TCSR — запоминаем enable-биты
            self.tcsr_enable = v & 0x1F
            self.mem[a] = v
            return
        if a in (0x00A7, 0x00A9, 0x00AB, 0x1006):
            self.io_writes.append((a, v))
        if a == 0x1006:                       # выбор канала ADC + старт преобразования
            ch = v & 0x0F                     # 0x20+канал -> канал
            self.adc_mux = ch
            # защёлкиваем значение канала в его регистр-результат (канал & 3)
            self.adc_result[ch & 3] = self.adc.get(ch, 0)
        self.mem[a] = v


class Machine:
    def __init__(self, rom_path, rom_base=0x8000):
        self.bus = Bus()
        self.cpu = CPU6303(self.bus)
        self.rom_base = rom_base
        self.rom = bytearray()
        self.load_rom(rom_path)

    def load_rom(self, path):
        with open(path, "rb") as f:
            self.rom = bytearray(f.read())
        for i, b in enumerate(self.rom):
            self.bus.mem[(self.rom_base + i) & 0xFFFF] = b

    # ---- завести прошивку с reset ----
    def boot(self, steps=80_000):
        cpu = self.cpu
        cpu.PC = self.peek16(0xFFFE)
        cpu.SP = 0x01FF
        cpu.I = 0
        crashed = None
        for _ in range(steps):
            try:
                cpu.step()
            except Exception as e:            # noqa: BLE001
                crashed = "%s @ 0x%04X" % (e, cpu.PC); break
            if cpu.halted:
                cpu.halted = False
        return {"PC": cpu.PC, "I": cpu.I, "crashed": crashed}

    # ---- «пульс»: тикаем таймер, шлём импульсы коленвала, дёргаем прерывания ----
    def run_engine(self, period, total_instr, set_adc=None):
        """
        period      — инструкций между импульсами коленвала (меньше = выше обороты).
        total_instr — сколько инструкций прокрутить.
        set_adc     — {канал: значение} для датчиков (0 = MAF).
        Прерывание подтверждаем сбросом флага (иначе зацикливание, если обработчик
        не прочитал регистр захвата).
        """
        cpu = self.cpu
        bus = self.bus
        if set_adc:
            for ch, v in set_adc.items():
                bus.adc[ch] = v & 0xFFFF
        EICI = bool(bus.tcsr_enable & 0x10)
        ETOI = bool(bus.tcsr_enable & 0x04)
        ICF_VEC, TOF_VEC = 0xFFF6, 0xFFF2
        fired = {"icf": 0, "tof": 0}
        since_cap = 0
        crashed = None
        i = 0
        while i < total_instr:
            try:
                cpu.step()
            except Exception as e:            # noqa: BLE001
                crashed = "%s @ 0x%04X" % (e, cpu.PC); break
            if cpu.halted:
                cpu.halted = False
            prev = bus.counter
            bus.counter = (bus.counter + 1) & 0xFFFF
            if bus.counter < prev:
                bus.tof = 1
            since_cap += 1
            if since_cap >= period:
                since_cap = 0
                bus.icr = bus.counter
                bus.icf = 1
            if cpu.I == 0:
                if bus.icf and EICI:
                    bus.icf = 0
                    cpu.irq(ICF_VEC); fired["icf"] += 1
                elif bus.tof and ETOI:
                    bus.tof = 0
                    cpu.irq(TOF_VEC); fired["tof"] += 1
            i += 1
        return {"fired": fired, "crashed": crashed, "instr": i,
                "rpm_raw": self.peek16(0x140A)}

    # ---- доступ ----
    def poke8(self, a, v):
        self.bus.mem[a & 0xFFFF] = v & 0xFF

    def poke16(self, a, v):
        self.bus.mem[a & 0xFFFF] = (v >> 8) & 0xFF
        self.bus.mem[(a + 1) & 0xFFFF] = v & 0xFF

    def peek8(self, a):
        return self.bus.read8(a)

    def peek16(self, a):
        return (self.bus.read8(a) << 8) | self.bus.read8(a + 1)

    def set_var(self, addr, size, value):
        if size == 16:
            self.poke16(addr, value)
        else:
            self.poke8(addr, value)

    def get_var(self, addr, size):
        return self.peek16(addr) if size == 16 else self.peek8(addr)

    # ---- прогон одной рутины до RTS ----
    def call_routine(self, addr, max_steps=200_000, trace=False):
        """
        Запустить рутину как подпрограмму: кладём сторожевой адрес возврата,
        крутим до RTS на него (или до лимита шагов). Возвращает инфо о прогоне.
        """
        cpu = self.cpu
        cpu.halted = False
        cpu.SP = 0x01FF
        SENT = 0xE7E7                 # «магический» адрес возврата
        cpu.push16(SENT)
        cpu.PC = addr & 0xFFFF
        cpu.instr = 0
        if trace:
            cpu.trace = []
        steps = 0
        crashed = None
        while steps < max_steps:
            if cpu.PC == SENT:
                break
            try:
                cpu.step()
            except Exception as e:               # noqa: BLE001
                crashed = "%s @ PC=0x%04X" % (e, cpu.PC)
                break
            if cpu.halted:
                break
            steps += 1
        return {
            "steps": steps,
            "reached_return": cpu.PC == SENT,
            "halted": cpu.halted,
            "crashed": crashed,
            "trace": cpu.trace if trace else None,
        }

    # ---- запустить рутину с входами, прочитать наблюдаемые ----
    def run(self, routine_addr, inputs, watch, max_steps=200_000, trace=False,
            iterations=8):
        """
        inputs: список {addr,size,value}; watch: список {name,addr,size}.
        iterations: сколько раз прогнать рутину перед чтением выходов. Нужно,
          чтобы устаканить ВНУТРЕННИЕ ФИЛЬТРЫ прошивки (напр. сглаживание $1577) —
          как будто держим вход постоянным, пока значение сойдётся. Вход
          перезадаётся перед каждой итерацией (фильтр не уводит его).
        """
        self.bus.io_writes = []
        info = None
        for _ in range(max(1, iterations)):
            for inp in inputs:
                self.set_var(inp["addr"], inp.get("size", 8), inp["value"])
                if inp["addr"] == 0x1408:
                    self.bus.adc[0] = inp["value"] & 0xFFFF
            info = self.call_routine(routine_addr, max_steps=max_steps, trace=trace)
        out = {}
        for w in watch:
            out[w["name"]] = self.get_var(w["addr"], w.get("size", 8))
        info["watch"] = out
        info["io_writes"] = [
            {"addr": a, "val": v} for a, v in self.bus.io_writes
        ]
        info["iterations"] = max(1, iterations)
        return info

    # ==================================================================
    #  ЖИВОЙ МОТОР (полный цикл) — найденная рабочая модель
    #  Цепочка: синхро цилиндра (порт $17.бит3=опорный) + запуск расчёта
    #  (гейт-массив пускает поток через планировщик: redirect $83CE->$83C8)
    #  + RPM из периода $1046 + MAF из ADC канала 0.
    # ==================================================================
    def start_engine(self, boot_steps=80_000):
        """Завести прошивку: boot + redirect через планировщик."""
        self.boot(boot_steps)
        # JMP $83CE -> JMP $83C8: поток идёт ЧЕРЕЗ планировщик $88DE,
        # как это делает гейт-массив на реальном железе.
        self.bus.mem[0x83C7] = 0xC8
        self._engine_started = True

    def _eng_tick(self, n):
        bus = self.bus
        for _ in range(n):
            prev = bus.counter
            bus.counter = (bus.counter + 1) & 0xFFFF
            if bus.counter < prev:
                bus.tof = 1

    def _eng_handler(self, vec, cap=12000):
        cpu = self.cpu
        bus = self.bus
        cpu.irq(vec)
        for _ in range(cap):
            cpu.step()
            if cpu.halted:
                cpu.halted = False
            prev = bus.counter
            bus.counter = (bus.counter + 1) & 0xFFFF
            if bus.counter < prev:
                bus.tof = 1
            if cpu.PC in (0x82A1, 0x82A4):     # вернулись в главный цикл
                break

    def _eng_mark(self, ref, rpm_period, maf_adc):
        """Одна метка 120° (большая дырка диска). ref=True -> широкая (опорная)."""
        bus = self.bus
        cpu = self.cpu
        bus.adc[0] = maf_adc & 0xFFFF
        self._eng_tick(600)
        bus.icr = bus.counter
        self.poke16(0x1046, rpm_period & 0xFFFF)   # период -> RPM
        self.poke8(0x102E, 0x20)                   # бит метки положения
        self.poke8(0x102F, 0x10)
        if ref:
            self.poke8(0x17, self.peek8(0x17) | 0x08)   # опорный на порт $17.бит3
        if cpu.I == 0:
            self._eng_handler(0xFFF6)              # ICF (вход капчер)
        if cpu.I == 0:
            self._eng_handler(0xFFF8)              # IRQ (положение -> расчёт)
        self.poke8(0x17, self.peek8(0x17) & 0xF7)
        self.poke8(0x102E, 0)
        self.poke8(0x102F, 0)

    def _eng_mainloop(self, n):
        """Дать ФОНОВОМУ главному циклу поработать (опрос датчиков, РХХ, idle)."""
        cpu = self.cpu
        bus = self.bus
        for _ in range(n):
            cpu.step()
            if cpu.halted:
                cpu.halted = False
            prev = bus.counter
            bus.counter = (bus.counter + 1) & 0xFFFF
            if bus.counter < prev:
                bus.tof = 1
            if cpu.I == 0 and bus.tof:
                bus.tof = 0
                cpu.irq(0xFFF2)   # TOF — база времени для фоновых задач

    def engine_run(self, rpm_period, maf_adc, cycles=8):
        """Прокрутить мотор cycles оборотов; вернуть ПОЛНОЕ живое состояние."""
        if not getattr(self, "_engine_started", False):
            self.start_engine()
        for _ in range(max(1, cycles)):
            for seg in range(6):
                self._eng_mark(seg == 0, rpm_period, maf_adc)
        # фоновый цикл: датчики (температура), idle-контроль (РХХ), коррекции
        self._eng_mainloop(15000)
        return self._engine_state()

    def _engine_state(self):
        """Снимок ключевых переменных ЭБУ — «что мотор делает» (для панели)."""
        return {
            "rpm": self.peek16(0x140A),
            "airflow": self.peek16(0x1577),
            "load": self.peek16(0x1413),
            "tp": self.peek16(0x1482),
            "iacv": self.peek8(0x1402),       # РХХ (положение регулятора ХХ)
            "coolant": self.peek8(0x1424),    # темп. ОЖ (сырьё)
            "airtemp": self.peek8(0x1489),    # темп. воздуха
            "maf_raw": self.peek16(0x1408),   # сырьё расходомера
            "cyl": self.peek8(0x00D6),        # текущий цилиндр
            "solA7": self.peek8(0x00A7),
            "solA9": self.peek8(0x00A9),
            "solAB": self.peek8(0x00AB),
            "f54": self.peek8(0x0054),
            "f55": self.peek8(0x0055),
            "fB0": self.peek8(0x00B0),
        }

    def _coolant_table(self):
        """Таблица датчика ОЖ из ROM (file 0x7B30 = CPU 0xFB30, 32 точки)."""
        if not hasattr(self, "_ctab"):
            self._ctab = [self.peek8(0xFB30 + i) for i in range(32)]
        return self._ctab

    def celsius_to_coolant_raw(self, celsius):
        """°C -> ADC-сырьё ОЖ через таблицу блока 0x7B30 (обратная интерполяция).
        Холод -> высокое сырьё. Это сырьё подаём на канал, который блок читает."""
        ctab = self._coolant_table()
        tv = celsius + 50                      # таблица: °C = значение − 50
        best, bd = 128, 1e9
        for raw in range(256):
            i = raw >> 3
            f = (raw & 7) / 8.0
            v = ctab[i] + (ctab[min(i + 1, 31)] - ctab[i]) * f
            if abs(v - tv) < bd:
                bd = abs(v - tv); best = raw
        return best

    # ==================================================================
    #  ПЛАНТ-МОДЕЛЬ ДВИГАТЕЛЯ (физика «мотор на нейтрали/дино»)
    #  газ -> воздух -> ЭБУ(прошивка) считает топливо -> момент ->
    #  обороты меняются через инерцию маховика -> назад в ЭБУ.
    #  Обороты — ВЫХОД (как стрелка тахометра), не задаются.
    # ==================================================================
    # ДВОЙНИК = ДВЕ САМОДОСТАТОЧНЫЕ СИСТЕМЫ, связь только сигналами, БЕЗ костылей:
    #   • МОТОР (железо, тут): воздух=винт+РХХ+газ -> обороты (маховик); расход->MAF;
    #     обороты -> импульсы 1°/120°. Сгорание ТОЛЬКО при зажигании (искра).
    #   • ЭБУ (прошивка): сам читает датчики -> льёт топливо, рулит РХХ ($004D),
    #     сам включает контур ХХ по концевику дросселя ($15.4). Свой регулятор НЕ нужен.
    #  ЗАПУСК: стартер крутит до ~300 -> ЭБУ видит импульсы -> льёт -> схватывает ->
    #  сам выходит на ХХ по своей таблице (холоднее = выше). Нет вращения/искры -> нет цикла.
    # МАСШТАБ (по разбору порогов прошивки):
    #  • ХХ-воздух (maf) ДОЛЖЕН быть ≥6400, иначе топливо-отсечка ($1408<100 -> Tp=0).
    #  • $1046 ≈ rpm/5, иначе $140A≥256 -> $1442=255 -> ломается индексация нагрузки.
    #  • Плавная нагрузка = $150C (не $1413, тот на полу 1792 = низ оси карт).
    # МОТОР КРУТИТ ТОПЛИВО: считает воздух -> ЭБУ даёт впрыск -> смесь AFR=воздух/топливо;
    # горит в окне ~10-16 (пик ~13), вне — пропуски/глохнет. Обороты ∝ топливо×КПД(AFR).
    P_BASE_SCREW = 5000.0   # дефолт винта ХХ (обвод); воздух ХХ выше порога отсечки
    P_KAIR = 9.0            # воздух на единицу duty РХХ ($004D)
    P_K_THR = 8.0           # воздух от газа (×обороты)
    P_C_FUEL = 2.3          # обороты на единицу топлива ($150C) при идеальной смеси
    P_AFR_K = 26.0          # масштаб AFR = K×расход($1577)/топливо($150C); стехио ~14.7 ХХ
    P_TP_K = 0.23           # базовый впрыск TP ≈ K×воздух/обороты (индекс столбца карты)
    P_AFR_TARGET = 14.7     # целевая смесь блока на ХХ/круизе (стехио)
    P_AFR_WOT = 12.0        # целевая смесь под полной нагрузкой (обогащение мощности)
    # ОТСЕЧКИ ЗДЕСЬ НЕТ: мотору похуй сколько крутиться. Обороты ограничивает БЛОК,
    # когда сам решает резать впрыск на красной зоне (это его команда, не наша).
    P_RPM_DIV = 5.0         # период $1046 = rpm/5 (чтобы $140A<256, индексация цела)
    P_RELAX = 4.0           # инерция маховика (плавность раскрутки/осадки)
    P_CRANK_RPM = 800.0     # обороты стартера (раскрутить до живого воздуха/$150C)
    P_CATCH_RPM = 450.0     # выше этого мотор «схватил» -> стартер отпускаем
    P_RPM_MAX = 10000.0     # НЕ отсечка — просто чтоб число не улетело в бесконечность
    P_IAC_KI = 0.15         # интегральный коэф. контура ХХ (ошибка в единицах блока)
    P_IDLE_TGT_SCALE = 0.0586  # перевод цели прогрева $142A в шкалу оборотов $140A
                               # (из блока: тёплый ХХ $142A=4096 <-> $140A=240)
    P_IAC_FB_MAX = 350.0    # макс поправка контура ХХ (открытие РХХ сверх базы $4D)

    @staticmethod
    def _combustion_eff(afr):
        """КПД сгорания по смеси: пик у ~13 (макс момент). Богатый пуск (AFR~3-6)
        горит СЛАБО (мотор схватывает), стехио (~14.7) — почти полная отдача,
        вне ~3..22 — пропуски/нет цикла (0). Нет топлива (AFR>22) -> 0."""
        if afr < 2.0 or afr > 22.0:
            return 0.0
        return max(0.15, 1.0 - ((afr - 13.0) / 9.0) ** 2)

    # ТАБЛИЦА ОТДАЧИ vs ОБОРОТЫ (мотор НЕЛИНЕЕН — момент колоколом, как в жизни):
    # полка в середине, спад к красной зоне -> мотор сам упирается в обороты, а не
    # улетает в отсечку. Это «таблица», о которой ты говорил — калибровка по оборотам.
    P_VE_RPM = [0,   800, 1500, 2500, 3500, 4500, 5200, 5800, 6200, 7000]
    P_VE_K   = [1.0, 1.0, 1.05, 1.08, 1.05, 0.95, 0.85, 0.72, 0.60, 0.40]

    def _torque_ve(self, rpm):
        """Множитель отдачи от оборотов (объёмный КПД колоколом) — линейная
        интерполяция по таблице P_VE_RPM/P_VE_K."""
        xs, ys = self.P_VE_RPM, self.P_VE_K
        if rpm <= xs[0]:
            return ys[0]
        if rpm >= xs[-1]:
            return ys[-1]
        for i in range(1, len(xs)):
            if rpm < xs[i]:
                t = (rpm - xs[i - 1]) / (xs[i] - xs[i - 1])
                return ys[i - 1] + t * (ys[i] - ys[i - 1])
        return ys[-1]

    @staticmethod
    def _afr_decode(x):
        """Байт карты топлива -> AFR. Из реверса: X>=128 -> 1881.6/(X-64),
        иначе 1881.6/(X+128). Проверено: 192->14.7, 26->12.2."""
        return 1881.6 / (x - 64) if x >= 128 else 1881.6 / (x + 128)

    def _fuel_target_afr(self, rpm, tp):
        """ЦЕЛЕВАЯ СМЕСЬ из ТОПЛИВНОЙ КАРТЫ блока 0xFD00 (rpm × нагрузка TP) —
        НЕ считаем, читаем карту блока. Оси: rpm $FB00 (×50), TP $FAF0 (/8)."""
        if not hasattr(self, "_fmap"):
            self._fmap = [[self._afr_decode(self.peek8(0xFD00 + r * 16 + c))
                           for c in range(16)] for r in range(16)]
            self._rax = [self.peek8(0xFB00 + i) * 50 for i in range(16)]    # об/мин
            self._tax = [self.peek8(0xFAF0 + i) / 8.0 for i in range(16)]   # TP

        def idx(axis, v):
            if v <= axis[0]:
                return 0, 0.0
            if v >= axis[-1]:
                return len(axis) - 2, 1.0
            for i in range(len(axis) - 1):
                if v < axis[i + 1]:
                    return i, (v - axis[i]) / (axis[i + 1] - axis[i])
            return len(axis) - 2, 1.0

        ri, rf = idx(self._rax, rpm)
        ti, tf = idx(self._tax, tp)
        m = self._fmap
        a = m[ri][ti] * (1 - tf) + m[ri][ti + 1] * tf          # билинейная
        b = m[ri + 1][ti] * (1 - tf) + m[ri + 1][ti + 1] * tf
        return a * (1 - rf) + b * rf

    def engine_plant_step(self, throttle, coolant=20, airtemp=20, base_air=None,
                          ignition=True, starter=False, ticks=12):
        """Кадр живого двойника. Две системы, связь сигналами, без костылей.
        ЗАЖИГАНИЕ (ключ) — НЕ искра (её не моделируем), а отрубание ВПРЫСКА:
          ignition=OFF -> ЭБУ не льёт топливо -> нет топлива -> нет цикла -> глохнет.
        starter — стартер: крутит мотор до ~300, дальше ЭБУ подхватывает САМ.
        coolant/airtemp — °C (ползунки). base_air — винт ХХ (ползунок)."""
        if not getattr(self, "_engine_started", False):
            self.start_engine()
        if not hasattr(self, "plant_rpm"):
            self.plant_rpm = 0.0                  # мотор ЗАГЛУШЕН при первом старте
        if not hasattr(self, "cranking"):
            self.cranking = False
        if not hasattr(self, "_rxx_duty"):
            self._rxx_duty = 0
        if not hasattr(self, "_iac_fb"):
            self._iac_fb = 0.0                    # поправка гейт-массива (замкнутый контур ХХ)
        if not hasattr(self, "_eff_duty"):
            self._eff_duty = 0.0                  # эффективный РХХ = база $4D + поправка
        if base_air is None:
            base_air = self.P_BASE_SCREW
        thr = max(0.0, min(1.0, throttle))

        # --- ДАТЧИКИ -> в ЭБУ (через калибровку датчика ОЖ блока) ---
        # ОЖ на канал, который двигает прогрев/цель ($B1/$142A) — это adc[2] (проверено).
        # ОЖ = канал 2 (он реально ведёт прогревочный ХХ $1489->$142A/$142C, проверено:
        # холод -> выше цель/РХХ). ТВ = канал 8. Раньше всё шло мимо (MUX не моделился).
        self.bus.adc[2] = (self.celsius_to_coolant_raw(coolant) & 0xFF) << 8
        self.bus.adc[8] = (self.celsius_to_coolant_raw(airtemp) & 0xFF) << 8
        self.poke8(0x14A2, int(thr * 200))        # TPS (дроссель)
        self.poke16(0x1400, int(thr * 200))
        # КОНЦЕВИК ХХ -> блок ($15.4): дроссель закрыт = холостой -> блок вкл. контур РХХ
        if thr <= 0.0:
            self.poke8(0x15, self.peek8(0x15) | 0x10)
        else:
            self.poke8(0x15, self.peek8(0x15) & ~0x10)

        # --- СТАРТЕР: крутит ТОЛЬКО пока кнопка держится (отпустил -> не крутит) ---
        self.cranking = bool(starter)

        # --- ВОЗДУХ = винт + ЭФФЕКТИВНЫЙ РХХ (база $4D + поправка контура ХХ) + газ ---
        duty = self._eff_duty
        air = base_air + self.P_KAIR * duty + self.P_K_THR * self.plant_rpm * thr
        maf_adc = int(max(0, min(55000, air)))

        # --- мотор вращается -> импульсы+MAF в ЭБУ; стоит -> только фон (датчики) ---
        if self.plant_rpm > 50:
            period = max(1, round(self.plant_rpm / self.P_RPM_DIV))
            st = self.engine_run(period, maf_adc, cycles=1)
        else:
            self._eng_mainloop(8000)
            st = self._engine_state()

        # --- ВЫХОДЫ ЭБУ: РХХ duty ($004D) и впрыск (Tp $1482) ---
        duty_raw = self.peek16(0x004D)
        duty_raw = 0 if duty_raw > 0x8000 else duty_raw
        # СГЛАЖИВАНИЕ duty РХХ — механика клапана + наполнение коллектора («на пути
        # стоит сглаживатель», как ты говорил). Это ФИЗИКА, гасит колебания контура.
        self._rxx_duty = 0.15 * duty_raw + 0.85 * self._rxx_duty
        duty = self._rxx_duty
        # СГЛАЖИВАНИЕ впрыска (топливная плёнка + наполнение коллектора) — гасит
        # одиночные спайки Tp, которые иначе срывают смесь.
        if not hasattr(self, "_fuel"):
            self._fuel = 0.0
        # ТОПЛИВО = нагрузка $150C (идёт за воздухом). Сглаживаем — топливная плёнка
        # + наполнение коллектора («на пути стоит сглаживатель»). 0.5 = быстрее, без
        # затяжного запаздывания, но переходный заброс смеси остаётся.
        load_now = self.peek16(0x150C)
        self._fuel = 0.5 * load_now + 0.5 * self._fuel
        fuel_ecu = self._fuel

        # ЦЕЛЕВАЯ СМЕСЬ — ИЗ ТОПЛИВНОЙ КАРТЫ блока 0xFD00 (rpm × нагрузка TP). Это
        # ТАБЛИЦА, а не расчёт — блок хочет ровно её (14.7 круиз, богаче под нагрузкой).
        tp_load = self.P_TP_K * maf_adc / max(50.0, self.plant_rpm)   # базовый впрыск ~ воздух/обороты
        afr_target = self._fuel_target_afr(self.plant_rpm, tp_load)
        # ФАКТ AFR — РЕАЛЬНОЕ ОТНОШЕНИЕ МАСС (а не мой K×отношение):
        #   $1577 — это уже МАССА воздуха (блок прогнал ДМРВ через VQ-таблицу 0x7A70);
        #   масса топлива = блок льёт под ЦЕЛЬ из карты от ИЗМЕРЕННОГО (запазд.) воздуха:
        #       m_топл = m_воздух_изм / цель;
        #   факт = m_воздух_сейчас / m_топл = цель × (воздух_сейчас / воздух_когда_лил).
        # Установка: факт = цель (блок попал, без подгонки). Перегаз: воздух обгоняет
        # запаздывающее топливо -> на миг бедно (тип-ин) / богато (сброс).
        airflow_blk = self.peek16(0x1577)
        if not hasattr(self, "_air_lag"):
            self._air_lag = float(airflow_blk)
        self._air_lag = 0.4 * airflow_blk + 0.6 * self._air_lag   # запаздывание топлива
        if ignition and self._air_lag > 0:
            afr = afr_target * airflow_blk / self._air_lag
        else:
            afr = 99.0                            # нет топлива -> бесконечно бедно
        eff = self._combustion_eff(afr)           # КПД сгорания (0 вне окна ~10-16)
        combusting = bool(ignition) and self.plant_rpm > 50 and eff > 0.0
        # ОТДАЧА нелинейна: × таблица КПД по оборотам (мотор упирается у красной зоны)
        rpm_eq = (self.P_C_FUEL * fuel_ecu * eff * self._torque_ve(self.plant_rpm)
                  if combusting else 0.0)

        # --- ДИНАМИКА МАХОВИКА ---
        if self.cranking:
            # стартер тянет к 300; сгорание (если льётся топливо) добавляет сверху
            self.plant_rpm += (max(self.P_CRANK_RPM, rpm_eq) - self.plant_rpm) / 3.0
        else:
            # МЯГКАЯ релаксация (1 шаг/кадр): обороты не «проваливаются» за кадр
            # ниже полки нагрузочного контура блока -> мотор сидит на полке ХХ,
            # а не коллапсит на нижний режим (455). Маховик = инерция.
            self.plant_rpm += (rpm_eq - self.plant_rpm) / self.P_RELAX
        if self.plant_rpm < 0:
            self.plant_rpm = 0.0
        if self.plant_rpm > self.P_RPM_MAX:
            self.plant_rpm = self.P_RPM_MAX

        # --- ГЕЙТ-МАССИВ: замкнутый контур ХХ ---
        # В железе к базе $4D подмешивается поправка по ошибке оборотов (цель блока −
        # факт). Тут моделируем именно её. Работает только на ХХ (дроссель закрыт):
        # обороты ниже цели -> поправка растёт -> РХХ шире -> воздух -> обороты к цели.
        # Винт прикрутил -> обороты упали -> контур сам шире откроет РХХ (компенсация).
        # Ошибка контура — В ЕДИНИЦАХ БЛОКА: уставка $1411 минус факт оборотов $140A.
        # Оба числа считает БЛОК; никакого моего пересчёта в обороты (700 выкинут).
        # Двигатель задаёт $140A (через импульсы), блок задаёт $1411 — я лишь подмешиваю
        # их разницу в РХХ (это и есть работа гейт-массива).
        # Целимся в ЦЕЛЬ ПРОГРЕВА $142A (несёт весь прогрев), переведённую в шкалу
        # оборотов $140A родным блочным соотношением. Раньше целились в $1411 — он
        # нёс лишь ~1/5 прогрева, потому на ОЖ почти не реагировало.
        setpt = self.peek16(0x142A) * self.P_IDLE_TGT_SCALE
        rpm_blk = self.peek16(0x140A)
        if thr <= 0.0 and self.plant_rpm > 50 and not self.cranking:
            self._iac_fb += self.P_IAC_KI * (setpt - rpm_blk)
            self._iac_fb = max(-self._rxx_duty, min(self.P_IAC_FB_MAX, self._iac_fb))
        else:
            self._iac_fb *= 0.9                              # вне ХХ поправка спадает
        self._eff_duty = max(0.0, min(512.0, self._rxx_duty + self._iac_fb))

        # --- СОСТОЯНИЕ ДЛЯ ПАНЕЛИ ---
        st["rpm_ecu"] = st["rpm"]                 # что насчитал сам ЭБУ
        st["rpm"] = round(self.plant_rpm)         # обороты мотора (тахометр)
        st["throttle"] = round(thr * 100)
        st["idle_sw"] = bool(thr <= 0.0)          # концевик ХХ (закрыт)
        st["wot_sw"] = bool(thr >= 0.70)          # полный газ
        st["iacv"] = int(round(self._eff_duty))   # ЭФФЕКТИВНЫЙ РХХ (база $4D + контур ХХ)
        st["iacv_pct"] = max(0, min(100, round(self._eff_duty / 512.0 * 100)))  # РХХ % открытия
        st["iacv_base"] = int(round(duty_raw))    # сырая база блока ($004D) — для справки
        st["timing"] = self.peek8(0x1455)         # угол опережения зажигания блока ($1455), °
        fueling = bool(ignition) and self.plant_rpm > 50
        st["fuel"] = round(fuel_ecu) if fueling else 0  # топливо $150C (зажиг OFF -> 0)
        st["ignition"] = bool(ignition)
        st["starter"] = bool(self.cranking)
        st["running"] = bool(combusting and not self.cranking)  # работает сам (не стартер)
        # Цель ХХ в оборотах = уставка блока $1411, переведённая через СОБСТВЕННОЕ
        # отношение мотора обороты/$140A (а не моё число): на равновесии = обороты мотора.
        rpm_blk_now = self.peek16(0x140A)
        st["idle_target"] = (round(self.peek16(0x142A) * self.P_IDLE_TGT_SCALE
                                   * self.plant_rpm / rpm_blk_now)
                             if (fueling and rpm_blk_now > 0) else 0)
        st["coolant"] = round(coolant)            # показываем ползунок °C
        st["airtemp"] = round(airtemp)
        # ДВЕ СМЕСИ: факт (что в цилиндре) vs цель (что хочет блок)
        st["afr"] = round(afr, 1) if combusting else 0.0   # ФАКТ — мотор
        st["afr_target"] = round(afr_target, 1)            # ОЖИДАНИЕ — подвижная цель
        st["comb_eff"] = round(eff, 2)                      # КПД сгорания (0..1)
        # ВОЗДУХ и ТОПЛИВО в СОГЛАСОВАННОЙ МАССЕ: воздух/топливо = AFR прямо на глаз.
        # воздух = масса из VQ ($1577); топливо = масса, что блок налил под цель.
        st["air_mass"] = round(airflow_blk)
        st["fuel_mass"] = (round(self._air_lag / afr_target, 1)
                           if (fueling and afr_target > 0) else 0.0)
        return st

    # ---- прогон цепочки рутин (мини-цикл для панели) ----
    def run_chain(self, inputs, chain, iterations=6, max_steps=200_000):
        """Прогнать список рутин по очереди iterations раз (устаканить фильтры)."""
        self.bus.io_writes = []
        info = {"reached": {}, "crashed": {}}
        for _ in range(max(1, iterations)):
            for addr in chain:
                for inp in inputs:
                    self.set_var(inp["addr"], inp.get("size", 8), inp["value"])
                    if inp["addr"] == 0x1408:
                        self.bus.adc[0] = inp["value"] & 0xFFFF
                r = self.call_routine(addr, max_steps=max_steps)
                info["reached"]["0x%04X" % addr] = r["reached_return"]
                if r["crashed"]:
                    info["crashed"]["0x%04X" % addr] = r["crashed"]
        return info

    # ---- свип одного входа ----
    def sweep(self, routine_addr, sweep_addr, sweep_size, values,
              base_inputs, watch, max_steps=200_000, iterations=8):
        """
        Гоняем рутину для каждого значения sweep-переменной.
        iterations — устаканивание фильтров на каждой точке (см. run()).
        """
        rows = []
        for val in values:
            inputs = list(base_inputs) + [
                {"addr": sweep_addr, "size": sweep_size, "value": val}
            ]
            info = self.run(routine_addr, inputs, watch,
                            max_steps=max_steps, iterations=iterations)
            row = {"sweep": val, "reached_return": info["reached_return"],
                   "crashed": info["crashed"]}
            row.update(info["watch"])
            rows.append(row)
        return rows
