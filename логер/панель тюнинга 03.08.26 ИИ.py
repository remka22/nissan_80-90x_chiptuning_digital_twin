# -*- coding: utf-8 -*-
"""
ПАНЕЛЬ ЛОГГЕРА ЭБУ — веб-админка + РАСШИФРОВКА дампа ОЗУ.

Запуск:  python3 "логер/панель логгера 31.07.26 ИИ.py"   → http://localhost:8009
Из браузера: выбор порта, скорость, Старт/Стоп, живые ЗНАЧЕНИЯ (обороты, нагрузка,
O2, напряжение, темпа, впрыск...), полный образ ОЗУ, запись сырья в файл.

Скорости под версии дампа:  v5(E/16)=125000  v6(E/128)=16000  v7(E/1024)=2000
"""
import argparse, threading, time, json, os
from collections import deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = threading.Lock()

# известные адреса ОЗУ (из разбора). fmt: 8=байт, 16=слово big-endian. Показываем СЫРЬЁ.
# (адрес, имя, формат 8/16, единица, множитель-в-реал или None). Единицы ВЫВЕДЕНЫ ИЗ КОДА.
# Подписи под УЗКИЙ кадр v8+ (27 байт). Все адреса подтверждены дизасмом (трассы 01.08.26).
# fmt: 8=байт, 16=слово. mul: множитель в реал или None (сырьё).
LABELS = [
    # --- основное ---
    (0x140A, "Обороты",              16, "об/мин",             12.807),
    (0x1482, "Нагрузка (сглаж.)",     8, "сырьё (/8=TP)",      None),
    (0x1413, "Расход мгновенный",     8, "сырьё (гэп→транзит)", None),  # $1413−$1482 = газовка
    (0x1431, "ALPHA",                 8, "× (100=1.0)",        0.01),
    (0x1411, "Впрыск расчёт",        16, "мс(до UPP)",         0.005),  # $142A×$1413+deadtime, ДО масштаба
    (0x004D, "Впрыск РЕАЛ (форс)",   16, "мс",                 0.005),  # $004D→UPP-каналы, тик 5мкс (датащит)
    # --- ДРОССЕЛЬ (TPS) ---
    (0x1492, "TPS дроссель",         16, "сырьё 10б",          None),   # аналог. дроссель, ch6
    (0x14A2, "TPS открытие",          8, "сырьё (от нуля)",    None),  # % считается отдельно из $1492: (ацп−мин)/344
    (0x14DE, "Обогащ. ускорения",    16, "добавка в форсунку", None),   # >0 = было обогащение
    (0x00B9, "Флаг TPS",              8, "0x20=ХХ/WOT/обрыв",  None),
    # --- ДАД: выбранные из ОЗУ (на MAF-бине = мусор) ---
    (0x00F8, "VE выбранное",          8, "×нап (128=1.0)",     0.0078125),  # карта 0x4900
    (0x00F9, "Ktps выбранное",        8, "× (128=1.0)",        0.0078125),  # карта 0x4B00
    # --- концевики / флаги режима ---
    (0x0054, "Флаг ХХ/газ",           8, "б0=ХХ",              None),
    (0x0015, "Банк концевиков",       8, "0x80=СТАРТЕР(255=крутит) 0x20нейтр 0x10ХХ", None),
    (0x0053, "Флаги угла",            8, "б0ХХ б1крэнк б2нейтр (какая карта)", None),
    (0x00AE, "Замкнутый цикл",        8, "0x80=вошёл",         None),
    # --- УОЗ (°BTDC = 70 − сырьё; см. колонку УОЗ_°BTDC) ---
    (0x140F, "УОЗ финал сырьё",       8, "°=70−байт",          None),
    (0x143B, "УОЗ карта",             8, "≈градусы (база)",    None),
    # --- контур ХХ ---
    (0x142C, "Цель ХХ",               8, "у.е.",               None),
    # --- АЦП опознанные (рабочие) ---
    (0x1408, "АЦП ch0 MAF",          16, "сырьё 10б",          None),
    (0x008F, "АЦП ch1 напряжение",    8, "сырьё",              None),
    (0x004C, "АЦП ch2 темп ОЖ",       8, "сырьё",              None),
    (0x1400, "АЦП ch3 O2",            8, "сырьё (лямбда титан)", None),
    # --- RX-ТЕСТ приёма по SCI ---
    (0x1600, "peek ($1600)",          8, "*(указатель) — poke/peek/проба", None),
]

# Узкий кадр v8: маркер $FFF0, 13 байт значений в фикс. порядке (декод по позиции).
# Порядок = ADDR_LIST билдера build_targeted_patch: раскладываем на РЕАЛЬНЫЕ адреса.
NARROW_MARKER = 0xFFF0
# Порядок ДОЛЖЕН совпадать с ADDR_LIST в build_targeted_patch ИИ.py (27 адресов).
# Декод позиционный + панель адаптивна по длине — терпит старые бины (короче/длиннее).
NARROW_MAP = [
    0x140A, 0x140B, 0x1482, 0x1413, 0x1431, 0x1411, 0x1412,
    0x1408, 0x1409, 0x008F, 0x004C, 0x1400,
    0x1492, 0x1493,
    0x140F, 0x143B, 0x0053,
    0x0015, 0x0054, 0x142C,
    0x14A2, 0x14DE, 0x14DF, 0x00B9, 0x00AE,
    0x00F8, 0x00F9,
    0x004D, 0x004E,   # РЕАЛЬНЫЙ впрыск в UPP-отсчётах (×0.005=мс, тик 5мкс датащит)
    0x1600,   # RX-тест: последний принятый по SCI байт
]

STATE = {
    "running": False, "port": "", "baud": 0,
    "total": 0, "events": deque(maxlen=4000),
    "frames": 0, "bad": 0, "error": "", "file": "",
    "ram": {},           # addr -> байт (образ ОЗУ из кадров)
    "recent": deque(maxlen=1024),
    "last_frame_t": 0,
}
CTRL = {"thread": None, "stop": None, "ser": None}
CTRL_LOCK = threading.Lock()
import glob, re

# ---------- ШДК (широкополосник) — второй серийный поток, AFR факт ----------
WBL = {"running": False, "port": "", "total": 0, "raw": "", "hex": "", "afr": None, "last_t": 0, "error": ""}
WLOCK = threading.Lock()
WCTRL = {"thread": None, "stop": None, "ser": None}


def parse_afr(buf):
    # формат AEM пока неизвестен (0 байт) — наивный разбор ASCII-числа AFR.
    # когда пойдут реальные байты — уточним по факту формата.
    try:
        s = "".join(chr(x) for x in buf if 32 <= x < 127)
        m = re.findall(r"\d{1,2}\.\d+", s)
        if m:
            v = float(m[-1])
            if 7.0 <= v <= 25.0:
                return round(v, 2)
    except Exception:
        pass
    return None


def wbl_reader(ser, stop_ev):
    buf = bytearray()
    while not stop_ev.is_set():
        try:
            chunk = ser.read(256)
        except Exception as e:
            with WLOCK: WBL["error"] = str(e)
            break
        if chunk:
            buf += chunk
            if len(buf) > 96: buf = buf[-96:]
            asc = "".join(chr(x) if 32 <= x < 127 else "." for x in buf[-48:])
            hx = " ".join("%02X" % x for x in buf[-24:])
            afr = parse_afr(buf)
            with WLOCK:
                WBL["total"] += len(chunk); WBL["raw"] = asc; WBL["hex"] = hx
                WBL["last_t"] = time.time()
                if afr is not None: WBL["afr"] = afr
    try: ser.close()
    except Exception: pass
    with WLOCK: WBL["running"] = False


def wbl_start(port):
    import serial
    with WLOCK:
        if WCTRL["stop"]: WCTRL["stop"].set()
    if WCTRL["thread"]: WCTRL["thread"].join(timeout=1.0)
    try:
        ser = serial.Serial(port, 9600, bytesize=8, parity="N", stopbits=1, timeout=1)
    except Exception as e:
        with WLOCK: WBL["error"] = str(e); WBL["running"] = False
        return False, str(e)
    stop_ev = threading.Event()
    th = threading.Thread(target=wbl_reader, args=(ser, stop_ev), daemon=True)
    with WLOCK:
        WBL["running"] = True; WBL["port"] = port; WBL["error"] = ""; WBL["total"] = 0
    WCTRL["thread"] = th; WCTRL["stop"] = stop_ev; WCTRL["ser"] = ser
    th.start()
    return True, ""


def wbl_stop():
    if WCTRL["stop"]: WCTRL["stop"].set()
    if WCTRL["thread"]: WCTRL["thread"].join(timeout=1.0)
    WCTRL["thread"] = None; WCTRL["stop"] = None; WCTRL["ser"] = None
    with WLOCK: WBL["running"] = False
    return True


# ---------- Таблицы из бина (смесь 0x7D00 / угол 0x7C00) + поиск ячейки ----------
# По умолчанию — v8-дамп. Оси: смесь rax=RPM(7B00)/cax=load(7AF0); угол rax=RPM(7B20)/cax=load(7B10).
DEFAULT_BIN = os.path.join(HERE, "J30_vq-форсы_v8-узкий_01.08.26 ИИ.bin")


def pick_default_bin():
    # автовыбор: ПОСЛЕДНЯЯ по времени НЕ-ДАД прошивка в логер/ (dad/дад в имени → пропуск)
    cands = [f for f in glob.glob(os.path.join(HERE, "*.bin"))
             if os.path.getsize(f) == 32768
             and "дад" not in os.path.basename(f).lower()
             and "dad" not in os.path.basename(f).lower()]
    if cands:
        return max(cands, key=os.path.getmtime)
    return DEFAULT_BIN if os.path.exists(DEFAULT_BIN) else ""


SEL = {"bin": ""}   # по умолчанию НЕ выбрана — пользователь выбирает вручную (иначе молча подставятся чужие карты/AFR)
_tab_cache = {}


def list_bins():
    found = []
    for d in (HERE, os.path.join(HERE, "..", "j30")):
        for f in sorted(glob.glob(os.path.join(d, "*.bin"))):
            if os.path.getsize(f) == 32768:
                found.append(os.path.abspath(f))
    # уникальные, дамп-бины первыми
    seen = set(); out = []
    for f in found:
        if f in seen: continue
        seen.add(f); out.append(f)
    return out


def load_tables(path):
    if not path or not os.path.exists(path):
        return None
    mt = os.path.getmtime(path)
    c = _tab_cache.get(path)
    if c and c[0] == mt:
        return c[1]
    b = open(path, "rb").read()
    if len(b) != 32768:
        return None
    rd = lambda a, n: list(b[a - 0x8000:a - 0x8000 + n])
    t = {
        "fuel": rd(0x7D00, 256), "fuel_rax": rd(0x7B00, 16), "fuel_cax": rd(0x7AF0, 16),
        "ign":  rd(0x7C00, 256), "ign_rax":  rd(0x7B20, 16), "ign_cax":  rd(0x7B10, 16),
    }
    kk = rd(0x7F2B, 2); t["k"] = (kk[0] << 8) | kk[1]   # форсуночная K ($7F2B)
    t["km"] = rd(0x4A12, 1)[0]                          # КМ ($4A12, ДАД масштаб уровня)
    # ДАД speed-density: хук 89D8 = JSR C700 (файл 0x09D8). VE @ C900, ось давл @ CA00.
    dad = (b[0x09D8] == 0xBD and b[0x09D9] == 0xC7 and b[0x09DA] == 0x00)
    t["dad"] = dad
    if dad:
        t["ve"] = rd(0x4900, 256)       # VE 16×16 (значение/128 = наполнение)
        t["ve_rax"] = rd(0x7B20, 16)    # ось оборотов (родная FB20)
        t["ve_pax"] = rd(0x4A00, 16)    # ось давления, кПа
        t["dad_ofs"] = b[0x4A10]        # Смещ (ноль датчика, отсчёты>>2)
        t["dad_slope"] = b[0x4A11]      # наклон кПа/отсчёт ×256
    # Ktps (поправка по дросселю) — есть если карта 0x4B00 не пустая (0x3F)
    if dad and any(z != 0x3F for z in rd(0x4B00, 16)):
        t["ktps"] = rd(0x4B00, 256)     # Ktps 16×16 (/128=1.0)
        t["ktps_rax"] = rd(0x7B20, 16)  # обороты (родная)
        t["ktps_tax"] = rd(0x4C00, 16)  # ось TPS в $14A2
    _tab_cache[path] = (mt, t)
    return t


def afr_of(x):        # значение карты смеси → AFR (формула M30-XDF)
    return round(1881.6 / (x - 64), 2) if x >= 128 else round(1881.6 / (x + 128), 2)


def deg_of(x):        # значение карты угла → градусы (1.0×X, ≥90 = флаг)
    return x if x < 90 else None


# ---- ОНЛАЙН-тюнинг: тень карт в ОЗУ (v4) ----
SHADOW = {"fuel": 0x1800, "ign": 0x1900}   # адрес тени в ОЗУ (см. build_targeted_patch)
BINOFF = {"fuel": 0x7D00, "ign": 0x7C00}   # смещение карты в файле бина


def recalc_checksum(b):
    s = x = 0
    for i in range(len(b)):
        if i in (0x7F7A, 0x7F7B): continue
        s = (s + b[i]) & 0xFF; x ^= b[i]
    b[0x7F7A], b[0x7F7B] = s, x


def nearest_idx(val, axis):   # индекс ближайшей точки оси (сырьё vs сырьё)
    best, bd = 0, 1e18
    for i, a in enumerate(axis):
        d = abs(val - a)
        if d < bd: bd, best = d, i
    return best


# ---------- лог ИНТЕРПРЕТИРОВАННЫХ данных в CSV (Старт/Стоп лог) ----------
LOGST = {"on": False, "path": "", "n": 0, "stop": None, "thread": None, "f": None, "t0": 0}
# колонки = ВСЁ: время + все декодированные сигналы (LABELS) + вычисленные (производные)
LOG_HEADER = (["время_с"] + [nm for (_a, nm, _f, _u, _m) in LABELS] +
              ["УОЗ_°BTDC", "TP_%8", "AFR_цель", "AFR_факт", "поправка_VE", "давление_кПа",
               "Загрузка_форс_%", "Газ_%", "K_форс", "КМ"])


def _log_row():
    d = snapshot()
    g = lambda x: "" if x is None else x
    row = [round(time.time() - LOGST["t0"], 2)]
    # все декодированные: реал если есть, иначе сырьё
    for v in d["vars"]:
        row.append(v["real"] if v["real"] is not None else g(v["val"]))
    # вычисленные производные
    tp = d["top"]
    tb = load_tables(SEL["bin"]) or {}
    # K/КМ: из ОЗУ если известны (онлайн-тюн), иначе из активного бина ($7F2B/$4A12)
    k = STATE.get("k_ram") if STATE.get("k_ram") is not None else tb.get("k", "")
    km = STATE.get("km_ram") if STATE.get("km_ram") is not None else tb.get("km", "")
    row += [g(tp["uoz_deg"]),
            round(tp["load"] / 8.0, 2) if tp["load"] is not None else "",
            g(tp["afr_target"]), g(tp["afr_fact"]), g(tp["ve_corr"]), g(tp["press"]),
            g(tp.get("inj_duty")), g(tp.get("tps_pct")), g(k), g(km)]
    return row


def _log_sampler(stop_ev):
    while not stop_ev.is_set():
        try:
            row = _log_row()
            LOGST["f"].write(";".join(str(x) for x in row) + "\n"); LOGST["f"].flush()
            LOGST["n"] += 1
        except Exception:
            pass
        stop_ev.wait(0.2)


def log_start():
    if LOGST["on"]:
        return True, os.path.basename(LOGST["path"])
    d = os.path.join(HERE, "логи"); os.makedirs(d, exist_ok=True)
    bn = os.path.splitext(os.path.basename(SEL["bin"]))[0] if SEL.get("bin") else "нобин"
    fn = os.path.join(d, "лог_" + bn + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv")
    f = open(fn, "w", encoding="utf-8-sig")
    f.write(";".join(LOG_HEADER) + "\n"); f.flush()
    LOGST.update(on=True, path=fn, n=0, f=f, t0=time.time())
    ev = threading.Event(); th = threading.Thread(target=_log_sampler, args=(ev,), daemon=True)
    LOGST["stop"] = ev; LOGST["thread"] = th; th.start()
    return True, os.path.basename(fn)


def log_stop():
    if LOGST["stop"]: LOGST["stop"].set()
    if LOGST["thread"]: LOGST["thread"].join(timeout=1.0)
    try: LOGST["f"].close()
    except Exception: pass
    LOGST["on"] = False; LOGST["stop"] = None; LOGST["thread"] = None
    return True


def list_ports():
    found = {}
    try:
        from serial.tools import list_ports as lp
        for p in lp.comports():
            dev = p.device or ""
            if not dev or "Bluetooth" in dev or "debug" in dev or dev.startswith("/dev/tty."):
                continue
            found[dev] = {"device": dev, "desc": (p.description or ""),
                          "ftdi": getattr(p, "vid", None) == 0x0403}
    except Exception:
        pass
    for dev in sorted(glob.glob("/dev/cu.*")):
        if "Bluetooth" in dev or "debug" in dev:
            continue
        if dev not in found:
            found[dev] = {"device": dev, "desc": "", "ftdi": False}
    ports = list(found.values())
    suggested = None
    for p in ports:
        if p["ftdi"]:
            suggested = p["device"]; break
    if not suggested:
        for p in ports:
            if "usbserial" in p["device"].lower():
                suggested = p["device"]; break
    if not suggested and ports:
        suggested = ports[0]["device"]
    return ports, suggested


class Parser:
    """Потоковый разбор кадров AE 17 addr_hi addr_lo len data... chk(XOR addr,len,data)."""
    def __init__(self):
        self.buf = bytearray()

    def feed(self, chunk):
        self.buf += chunk
        if len(self.buf) > 16384:
            self.buf = self.buf[-16384:]
        out = []
        i = 0; n = len(self.buf)
        while i < n - 5:
            if self.buf[i] == 0xAE and self.buf[i+1] == 0x17:
                ln = self.buf[i+4]; end = i + 5 + ln
                if end >= n:
                    break   # кадр ещё не дошёл целиком
                c = 0
                for b in self.buf[i+2:i+5+ln]:
                    c ^= b
                if c == self.buf[end]:
                    addr = (self.buf[i+2] << 8) | self.buf[i+3]
                    out.append((addr, bytes(self.buf[i+5:i+5+ln]), True))
                    i = end + 1; continue
                else:
                    out.append((None, None, False))  # битый
            i += 1
        self.buf = self.buf[i:]
        return out


def reader_loop(ser, stop_ev, fname):
    parser = Parser()   # сырьё НЕ пишем (не нужно, не захламляем папку) — только разбор для панели+CSV
    while not stop_ev.is_set():
        try:
            chunk = ser.read(2048)
        except Exception as e:
            with LOCK: STATE["error"] = f"чтение: {e}"
            break
        if chunk:
            now = time.time()
            frames = parser.feed(chunk)
            with LOCK:
                STATE["total"] += len(chunk)
                for b in chunk: STATE["recent"].append(b)
                STATE["events"].append((now, len(chunk)))
                for addr, data, ok in frames:
                    if ok:
                        STATE["frames"] += 1
                        STATE["last_frame_t"] = now
                        if addr == NARROW_MARKER:
                            # узкий кадр v8: позиционно, ЛЮБАЯ длина (терпим к версии бина —
                            # порядок совпадает по префиксу, лишние адреса просто не придут)
                            for k, b in enumerate(data):
                                if k < len(NARROW_MAP):
                                    STATE["ram"][NARROW_MAP[k]] = b
                        else:
                            for k, b in enumerate(data):
                                STATE["ram"][addr + k] = b
                    else:
                        STATE["bad"] += 1
    try: ser.close()
    except Exception: pass
    with LOCK: STATE["running"] = False


def _send_cmd(s, bs, gap=0.03):
    # байты команды С ПАУЗОЙ — ЭБУ опрашивает RDRF раз в проход цикла (~6мс),
    # подряд идущие байты теряет. gap>период цикла → каждый байт пойман.
    for b in bs:
        s.write(bytes([b & 0xFF]))
        try: s.flush()
        except Exception: pass
        time.sleep(gap)


def _probe_wait(addr, nframes=2, timeout=2.0):
    # ждём nframes свежих кадров, возвращаем текущий байт по адресу из образа ОЗУ
    start = STATE.get("frames", 0); t0 = time.time()
    while STATE.get("frames", 0) - start < nframes:
        if time.time() - t0 > timeout: break
        time.sleep(0.02)
    return STATE["ram"].get(addr)


TXFLOOD = {"on": False, "byte": 0, "thread_alive": False}
def tx_flood_loop():
    # непрерывный поток байтов в ЭБУ — чтобы мультиметром увидеть просадку на ноге Rx
    while TXFLOOD["on"]:
        s = CTRL.get("ser")
        if not s: break
        try: s.write(bytes([TXFLOOD["byte"]]) * 128)
        except Exception: break
    TXFLOOD["thread_alive"] = False


def do_start(port, baud):
    import serial
    with CTRL_LOCK:
        if CTRL["stop"]: CTRL["stop"].set()
        if CTRL["thread"]: CTRL["thread"].join(timeout=1.0)
        try:
            ser = serial.Serial(port, int(baud), bytesize=8,
                                parity=serial.PARITY_NONE, stopbits=1, timeout=0.2)
        except Exception as e:
            with LOCK:
                STATE["error"] = f"Не открыл {port} @ {baud}: {e}"; STATE["running"] = False
            return False, STATE["error"]
        time.sleep(0.2)
        try: ser.reset_input_buffer()
        except Exception: pass
        fname = os.path.join(HERE, "сырьё", "raw_вход_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bin")
        with LOCK:
            STATE.update({"running": True, "port": port, "baud": int(baud),
                          "total": 0, "frames": 0, "bad": 0, "error": "", "file": fname})
            STATE["recent"].clear(); STATE["events"].clear()
            # ram НЕ чистим — накапливаем образ
        stop_ev = threading.Event()
        th = threading.Thread(target=reader_loop, args=(ser, stop_ev, fname), daemon=True)
        CTRL["thread"] = th; CTRL["stop"] = stop_ev; CTRL["ser"] = ser
        th.start()
        try: log_start()          # автолог стартует вместе с подключением ЭБУ
        except Exception: pass
        return True, ""


def do_stop():
    with CTRL_LOCK:
        if CTRL["stop"]: CTRL["stop"].set()
        if CTRL["thread"]: CTRL["thread"].join(timeout=1.0)
        CTRL["thread"] = None; CTRL["stop"] = None; CTRL["ser"] = None
    try: log_stop()               # лог закрывается при отключении ЭБУ
    except Exception: pass
    with LOCK: STATE["running"] = False
    return True


def snapshot():
    now = time.time()
    with LOCK:
        events = list(STATE["events"]); ram = dict(STATE["ram"])
        d = {k: STATE[k] for k in ("running", "port", "baud", "total", "frames", "bad", "error", "file")}
        recent = list(STATE["recent"]); lft = STATE["last_frame_t"]
    d["rate"] = sum(n for (t, n) in events if now - t <= 1.0)
    d["fresh"] = (now - lft) < 2.0 if lft else False
    d["file_short"] = os.path.basename(d["file"]) if d["file"] else ""
    # расшифровка известных переменных
    var = []
    for addr, name, fmt, unit, mul in LABELS:
        if fmt == 16:
            v = (ram[addr] << 8) | ram[addr + 1] if (addr in ram and addr + 1 in ram) else None
        else:
            v = ram.get(addr)
        real = None
        if v is not None and mul is not None:
            r = v * mul
            real = int(round(r)) if abs(r) >= 10 else round(r, 2)
        var.append({"name": name, "addr": "$%04X" % addr, "val": v, "unit": unit, "real": real})
    d["vars"] = var
    # образ ОЗУ строками по 16 (только там где есть данные)
    lines = []
    for base in list(range(0x40, 0x100, 16)) + list(range(0x1400, 0x1800, 16)):
        row = [ram.get(base + k) for k in range(16)]
        if all(x is None for x in row): continue
        hx = " ".join("%02X" % x if x is not None else ".." for x in row)
        lines.append("%04X: %s" % (base, hx))
    d["ram_lines"] = lines
    d["ram_count"] = len(ram)

    # ---- живые значения для верхней строки + подсветка ячеек карт ----
    def w(a):  # слово
        return (ram[a] << 8) | ram[a + 1] if (a in ram and a + 1 in ram) else None
    rpm_raw = w(0x140A)
    load_raw = ram.get(0x1482)
    temp_raw = ram.get(0x004C)
    alpha_raw = ram.get(0x1431)
    with WLOCK:
        wbl = {"running": WBL["running"], "port": WBL["port"], "total": WBL["total"],
               "raw": WBL["raw"], "hex": WBL["hex"], "afr": WBL["afr"], "error": WBL["error"],
               "fresh": (now - WBL["last_t"]) < 2.0 if WBL["last_t"] else False}
    d["wbl"] = wbl

    top = {
        "rpm": int(round(rpm_raw * 12.807)) if rpm_raw is not None else None,
        "load": load_raw,                              # сырьё (для CSV)
        "tp": round(load_raw / 8.0, 2) if load_raw is not None else None,  # читаемо, как в таблицах
        "temp": temp_raw,                              # сырьё АЦП
        "alpha": round(alpha_raw * 0.01, 2) if alpha_raw is not None else None,
        "afr_target": None, "uoz": None,
        # °BTDC = 70 − $140F (код: SBA #0x46; проверено: ХХ-нейтраль 55→15° = спец VG30E)
        "uoz_deg": (70 - ram[0x140F]) if 0x140F in ram else None,
        "afr_fact": wbl["afr"], "press": None, "ve_corr": None,
    }
    # ТОЧНАЯ загрузка форсунок: РЕАЛЬНЫЙ впрыск $004D (в UPP) × 0.005мс (тик 5мкс, датащит HD63140) × об / 1200
    inj_raw = w(0x004D)
    inj_ms = inj_raw * 0.005 if inj_raw is not None else None
    top["inj_ms"] = round(inj_ms, 2) if inj_ms is not None else None
    top["inj_duty"] = round(inj_ms * top["rpm"] / 1200, 1) if (inj_ms is not None and top["rpm"]) else None
    # ГАЗ %: (TPS_ацп $1492 − наблюдаемый минимум) / 344 × 100, обрезка 0-100.
    # минимум из ОЗУ (выученный ноль) не логируется → берём минимум самого АЦП
    tps_raw = w(0x1492)
    if tps_raw is not None:
        m = STATE.get("tps_min")
        if m is None or tps_raw < m: STATE["tps_min"] = tps_raw; m = tps_raw
        top["tps_pct"] = max(0.0, min(100.0, round((tps_raw - m) / 344.0 * 100, 1)))
    else:
        top["tps_pct"] = None
    t = load_tables(SEL["bin"])
    fuel_out = ign_out = ve_out = ktps_out = None
    top["is_dad"] = bool(t and t.get("dad"))
    if t:
        # смесь: ряды=обороты(7B00), колонки=нагрузка(7AF0)
        fuel_cells = [afr_of(v) for v in t["fuel"]]
        fuel_out = {"cells": fuel_cells,
                    "rows": [b * 50 for b in t["fuel_rax"]],           # обороты
                    "cols": [round(b * 0.125, 2) for b in t["fuel_cax"]],  # нагрузка TP
                    "hr": -1, "hc": -1}
        ign_cells = [deg_of(v) for v in t["ign"]]
        ign_out = {"cells": ign_cells,
                   "rows": [b * 50 for b in t["ign_rax"]],
                   "cols": [round(b * 0.125, 2) for b in t["ign_cax"]],
                   "hr": -1, "hc": -1}
        if rpm_raw is not None and load_raw is not None:
            fr = nearest_idx(rpm_raw / 4.0, t["fuel_rax"])
            fc = nearest_idx(load_raw, t["fuel_cax"])
            fuel_out["hr"], fuel_out["hc"] = fr, fc
            top["afr_target"] = fuel_cells[fr * 16 + fc]
            ir = nearest_idx(rpm_raw / 4.0, t["ign_rax"])
            ic = nearest_idx(load_raw, t["ign_cax"])
            ign_out["hr"], ign_out["hc"] = ir, ic
            # реальный доставленный угол $140F из лога; карта — запасной вариант
            top["uoz"] = ram.get(0x140F, ign_cells[ir * 16 + ic])
        # --- VE (только ДАД-прошивка): ось давления из $1408 через тарировку ---
        if t.get("dad"):
            ve_cells = [round(v / 128.0, 3) for v in t["ve"]]
            ve_out = {"cells": ve_cells,
                      "rows": [bb * 50 for bb in t["ve_rax"]],   # обороты
                      "cols": list(t["ve_pax"]),                 # давление, кПа
                      "hr": -1, "hc": -1}
            maf_raw = w(0x1408)
            if maf_raw is not None:
                praw = (maf_raw >> 2) - t["dad_ofs"]
                if praw < 0: praw = 0
                press = (praw * t["dad_slope"]) >> 8             # давление, кПа
                top["press"] = press
                if rpm_raw is not None:
                    vr = nearest_idx(rpm_raw / 4.0, t["ve_rax"])
                    vc = nearest_idx(press, t["ve_pax"])
                    ve_out["hr"], ve_out["hc"] = vr, vc
            # поправка VE = AFR факт / AFR цель (>1 = добавить топлива в ячейку)
            if top["afr_fact"] and top["afr_target"]:
                top["ve_corr"] = round(top["afr_fact"] / top["afr_target"], 3)
        # --- Ktps (поправка по дросселю): ось обороты × открытие TPS $14A2 ---
        if t.get("ktps") is not None:
            k_cells = [round(v / 128.0, 3) for v in t["ktps"]]
            ktps_out = {"cells": k_cells,
                        "rows": [bb * 50 for bb in t["ktps_rax"]],              # обороты
                        "cols": [round(a * 100 / 172) for a in t["ktps_tax"]],   # % газа (из $14A2)
                        "hr": -1, "hc": -1}
            a2 = ram.get(0x14A2)
            if rpm_raw is not None and a2 is not None:
                ktps_out["hr"] = nearest_idx(rpm_raw / 4.0, t["ktps_rax"])
                ktps_out["hc"] = nearest_idx(a2, t["ktps_tax"])
    d["top"] = top
    d["fuel"] = fuel_out
    d["ign"] = ign_out
    d["ve"] = ve_out
    d["ktps"] = ktps_out
    d["bin"] = os.path.basename(SEL["bin"]) if SEL["bin"] else ""
    d["log"] = {"on": LOGST["on"], "n": LOGST["n"],
                "file": os.path.basename(LOGST["path"]) if LOGST["path"] else ""}
    return d


PAGE = r"""<!doctype html><html lang=ru><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Панель логгера ЭБУ — расшифровка</title>
<style>
 body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#12151a;color:#e6e6e6}
 header{padding:12px 18px;background:#1e2a38;border-bottom:1px solid #2a3a4a}
 h1{font-size:16px;margin:0}
 .panel{padding:12px 18px;display:flex;flex-wrap:wrap;gap:10px;align-items:end;background:#161b22;border-bottom:1px solid #263040}
 .fld{display:flex;flex-direction:column;gap:4px}
 .fld label{font-size:11px;color:#8aa}
 select,input{background:#0d1117;color:#e6e6e6;border:1px solid #30404f;border-radius:6px;padding:7px 9px;font-size:14px}
 input.baud{width:110px}
 button{border:0;border-radius:6px;padding:8px 15px;font-size:14px;font-weight:600;cursor:pointer}
 button:disabled{opacity:.3;cursor:not-allowed}
 .start{background:#1a7f37;color:#fff}.stop{background:#b02a2a;color:#fff}.ghost{background:#26313d;color:#cde}
 #banner{padding:12px;text-align:center;font-size:19px;font-weight:700}
 .live{background:#0a4d20;color:#7f7}.quiet{background:#3a3410;color:#fd6}.off{background:#22282f;color:#8aa}.err{background:#5a1a1a;color:#fbb}
 .stats{display:flex;gap:12px;flex-wrap:wrap;padding:8px 18px;font-size:12px;color:#8aa}
 .stats b{color:#e6e6e6}
 .wrap{display:flex;flex-wrap:wrap;gap:16px;padding:12px 18px}
 .col{flex:1;min-width:320px}
 h2{font-size:13px;color:#9ab;text-transform:uppercase;letter-spacing:.5px;margin:0 0 8px}
 table{border-collapse:collapse;width:100%;font-size:13px}
 td,th{border:1px solid #263040;padding:5px 8px;text-align:left}
 th{background:#1b222c;color:#9ab;font-weight:600}
 td.v{font-family:ui-monospace,Menlo,monospace;text-align:right;color:#7fd}
 td.a{font-family:ui-monospace,Menlo,monospace;color:#89a;font-size:11px}
 td.u{color:#8aa;font-size:11px}
 td.r{font-family:ui-monospace,Menlo,monospace;text-align:right;color:#8f8;font-weight:600}
 td.na{color:#556}
 pre{background:#0a0d11;border:1px solid #263040;border-radius:8px;padding:10px;overflow:auto;max-height:60vh;font-size:11px;line-height:1.5;font-family:ui-monospace,Menlo,monospace}
 .foot{padding:0 18px 16px;font-size:12px;color:#8aa}
 a.dl{color:#9cf;text-decoration:none;border:1px solid #30404f;border-radius:6px;padding:6px 11px}
 /* липкий верх: лог-бар + строка параметров */
 .topstick{position:sticky;top:0;z-index:20;box-shadow:0 2px 10px #000a}
 .logbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:8px 18px;background:#141c26;border-bottom:1px solid #263040;font-size:13px}
 .logbar .st{color:#8aa}
 .logbar .rec{background:#1a7f37;color:#fff;font-weight:700;padding:5px 16px;border-radius:6px;font-size:16px;box-shadow:0 0 12px #2e7c;animation:pulse 1.2s infinite}
 @keyframes pulse{50%{box-shadow:0 0 3px #2e73}}
 .logbar a.dl{padding:4px 9px}
 .hud{display:flex;flex-wrap:wrap;gap:2px;padding:10px 18px;background:#0e1520;border-bottom:1px solid #2a3a4a}
 .hud .cell{flex:1;min-width:96px;background:#151d2a;border:1px solid #22303f;border-radius:8px;padding:8px 10px;text-align:center}
 .hud .lbl{font-size:10px;color:#8aa;text-transform:uppercase;letter-spacing:.4px}
 .hud .num{font-size:24px;font-weight:700;font-family:ui-monospace,Menlo,monospace;color:#7fd;line-height:1.2}
 .hud .cell.tgt .num{color:#fc8}.hud .cell.fact .num{color:#8f8}.hud .cell.uoz .num{color:#9cf}.hud .cell.vec .num{color:#f9a}
 .hud .num.na{color:#556;font-weight:400}
 /* панель ШДК */
 .wblbar{display:flex;flex-wrap:wrap;gap:10px;align-items:end;padding:10px 18px;background:#131922;border-bottom:1px solid #263040}
 .wblbar .raw{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#9c8;background:#0a0d11;border:1px solid #263040;border-radius:6px;padding:6px 9px;min-width:220px}
 /* карты */
 .maps{display:flex;flex-direction:column;gap:18px;padding:12px 18px;background:#0f141b;border-bottom:1px solid #263040}
 .mapbox{width:100%;overflow:auto}
 table.map{border-collapse:collapse;font-size:11px;width:auto}
 table.map td,table.map th{width:34px;min-width:34px}
 table.map td,table.map th{border:1px solid #223040;padding:2px 5px;text-align:right;font-family:ui-monospace,Menlo,monospace}
 table.map th{background:#161e29;color:#9ab;position:sticky;top:0}
 table.map th.corner{color:#678}
 table.map td.hl{outline:2px solid #2ecc40;outline-offset:-2px;background:#12351a;color:#bfe;font-weight:700}
 table.map td.flag{color:#a86}
 /* ===== СВЕТЛАЯ ТЕМА (контрастная, для солнца) ===== */
 body.light{background:#fff;color:#111}
 body.light header{background:#dbe7f3;border-bottom:2px solid #7fa3c4}
 body.light .panel{background:#eef1f5;border-bottom:2px solid #b3bcc7}
 body.light .fld label,body.light .logbar .st,body.light .stats,body.light .foot,body.light td.u,body.light .hud .lbl{color:#334}
 body.light select,body.light input{background:#fff;color:#111;border:1px solid #7f8a99}
 body.light .ghost{background:#ccd4dd;color:#123}
 body.light .stats b{color:#000}
 body.light .live{background:#0a5d26;color:#dfffe6}body.light .quiet{background:#7a6a10;color:#fff8dc}body.light .off{background:#c3ccd6;color:#334}body.light .err{background:#8a1a1a;color:#ffe0e0}
 body.light td,body.light th{border:1px solid #9aa6b3}
 body.light th{background:#d6dee7;color:#123}
 body.light td.v{color:#046}body.light td.r{color:#063}body.light td.a{color:#456}body.light td.na{color:#99a}
 body.light pre{background:#f6f8fa;border:1px solid #9aa6b3;color:#111}
 body.light a.dl{color:#046;border:1px solid #7f8a99}
 body.light .topstick{box-shadow:0 2px 10px #0004}
 body.light .logbar{background:#e3ecf5;border-bottom:2px solid #b3bcc7}
 body.light .hud{background:#e9eef4;border-bottom:2px solid #b3bcc7}
 body.light .hud .cell{background:#fff;border:1px solid #9aa6b3}
 body.light .hud .num{color:#046}
 body.light .hud .cell.tgt .num{color:#a3520a}body.light .hud .cell.fact .num{color:#0a6b2a}body.light .hud .cell.uoz .num{color:#1650a3}body.light .hud .cell.vec .num{color:#a3186a}
 body.light .hud .num.na{color:#99a}
 body.light .wblbar{background:#e6edf4;border-bottom:2px solid #b3bcc7}
 body.light .wblbar .raw{color:#0a5d26;background:#f6f8fa;border:1px solid #9aa6b3}
 body.light .maps{background:#eef1f5;border-bottom:2px solid #b3bcc7}
 body.light h2{color:#234}
 body.light table.map td,body.light table.map th{border:1px solid #9aa6b3}
 body.light table.map th{background:#d6dee7;color:#123}
 body.light table.map th.corner{color:#567}
 body.light table.map td.hl{outline:2px solid #0a7a2a;background:#c6f0ce;color:#031;font-weight:700}
 body.light table.map td.flag{color:#8a5a10}
 .themebox{display:flex;align-items:center;gap:6px;font-size:13px;cursor:pointer;user-select:none}
 header .themebox{float:right;color:inherit;font-weight:600}
 /* ---- новая практическая страница ---- */
 #ctrlbar{display:flex;gap:18px;align-items:center;flex-wrap:wrap;padding:8px 14px;border-bottom:2px solid #2a3340;position:sticky;top:0;z-index:20;background:inherit}
 .cgrp{display:flex;gap:6px;align-items:center}
 .clbl{font-size:13px;color:#8aa;font-weight:600}
 .stat{font-size:16px;line-height:1}
 .stat.ok{color:#2ecc40}.stat.warn{color:#ffcf33}.stat.err{color:#ff4136}.stat.none{color:#77808a}
 #page.locked{opacity:.35;pointer-events:none;filter:grayscale(.6)}
 .split{display:flex;gap:12px;padding:10px;align-items:flex-start}
 .leftcol{width:30%;min-width:260px;max-height:calc(100vh - 70px);overflow:auto;border:1px solid #2a3340;border-radius:8px}
 .rightcol{width:70%;flex:1;max-height:calc(100vh - 70px);overflow:auto}
 .logtab{width:100%;border-collapse:collapse;font-size:14px}
 .logtab th{position:sticky;top:0;background:#1b2129;text-align:left;padding:6px 8px;border-bottom:1px solid #2a3340}
 .logtab td{padding:5px 8px;border-bottom:1px solid #222a33}
 .logtab tr.sticky{background:#182028}.logtab tr.sticky td:first-child{font-weight:700}
 .logtab .val{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
 .logtab .unit{color:#8aa;font-size:12px;margin-left:4px}
 .onlinebar{display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
 .tobin{font-size:12px;margin-left:8px}
 .rightcol .mapbox{margin-bottom:26px}
 .rightcol .mapbox h2{margin:0 0 10px}
 .ec{padding:0}
 .ec input{width:100%;box-sizing:border-box;border:none;background:transparent;text-align:center;font:inherit;color:inherit;padding:3px 0}
 .ec.ok{background:#123d1a}.ec.err{background:#4d1414}.ec.pend{background:#4d4413}
 body.light .ec.ok{background:#c8f0d0}body.light .ec.err{background:#f5c6c6}body.light .ec.pend{background:#f5ecc0}
 body.light #ctrlbar{background:#fff}body.light .logtab th{background:#eef2f6}body.light .logtab tr.sticky{background:#eaf3ff}
</style></head><body class=light>
<div id=ctrlbar>
 <div class=cgrp><span class=clbl>Файл</span><select id=binsel onchange=selbin()></select><span class="stat none" id=binicon>&#9679;</span></div>
 <div class=cgrp><span class=clbl>ЭБУ</span><select id=port onchange=ecuAuto()></select><span class="stat none" id=ecuicon>&#9679;</span></div>
 <div class=cgrp><span class=clbl>ШДК</span><select id=wport onchange=wblAuto()></select><span class="stat none" id=wblicon>&#9679;</span></div>
 <button class=ghost onclick=loadPorts()>&#8635; порты</button>
 <span class=themebox style="margin-left:auto"><input type=checkbox id=darkbox onchange=toggletheme()> &#127769;</span>
</div>

<div id=page class=locked>
<div class=split>
 <div class=leftcol>
  <table class=logtab><thead><tr><th>Параметр</th><th>Значение</th></tr></thead><tbody id=vars></tbody></table>
 </div>
 <div class=rightcol>
  <div class=onlinebar>
   <button class=start id=btnOnline onclick=goOnline()>&#128246; ОНЛАЙН</button>
   <button class=ghost id=btnSaveBin onclick=saveBin() style="display:none">&#128190; СОХРАНИТЬ БИН</button>
   <span id=onstat class=st style="font-size:13px;color:#8aa"></span>
  </div>
  <div class=mapbox><h2>&#9819; Смесь (AFR) <button class=tobin id=tobin_fuel onclick="applyBin('fuel')" style="display:none">привести к бин</button></h2><div id=fuelmap>—</div></div>
  <div class=mapbox><h2>&#9889; Угол (УОЗ, град) <button class=tobin id=tobin_ign onclick="applyBin('ign')" style="display:none">привести к бин</button></h2><div id=ignmap>—</div></div>
 </div>
</div>
</div>
<script>
// ==== практическая страница тюнинга ====
function setStat(id,st){const e=document.getElementById(id);if(e)e.className='stat '+st;}
async function loadPorts(){
 try{const r=await fetch('/api/ports');const d=await r.json();
  for(const sid of ['port','wport']){
    const busy=(sid==='port')?d.wbl_port:d.ecu_port;
    const s=document.getElementById(sid);const cur=s.value;s.innerHTML='';
    const ph=document.createElement('option');ph.value='';ph.textContent='— порт —';s.appendChild(ph);
    d.ports.forEach(p=>{if(busy&&p.device===busy)return;
      const o=document.createElement('option');o.value=p.device;o.textContent=p.device+(p.ftdi?' (FTDI)':'');s.appendChild(o);});
    if(cur&&cur!==busy)s.value=cur;
    else if(sid==='port'&&d.suggested&&d.suggested!==busy&&!s.value)s.value=d.suggested;
  }}catch(e){}
}
async function loadBins(){
 try{const r=await fetch('/api/bins');const d=await r.json();
  const s=document.getElementById('binsel');s.innerHTML='';
  const ph=document.createElement('option');ph.value='';ph.textContent='— выбери бин —';s.appendChild(ph);
  d.bins.forEach(b=>{const o=document.createElement('option');o.value=b.path;o.textContent=b.name;s.appendChild(o);});
  s.value=d.selected||'';binLock();}catch(e){}
}
function binLock(){const has=!!document.getElementById('binsel').value;
 document.getElementById('page').classList.toggle('locked',!has);
 setStat('binicon',has?'ok':'none');}
async function selbin(){const p=document.getElementById('binsel').value;
 await fetch('/api/selectbin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({bin:p})});
 mapBin=null;binLock();
 if(p&&document.getElementById('port').value)ecuAuto();}
// автоподключение по выбору порта (бод известен = 15625)
async function ecuAuto(){const port=document.getElementById('port').value;
 if(!port){await fetch('/api/stop',{method:'POST'});return;}
 await fetch('/api/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({port:port,baud:15625})});}
async function wblAuto(){const port=document.getElementById('wport').value;
 if(!port){await fetch('/api/wbl/stop',{method:'POST'});return;}
 await fetch('/api/wbl/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({port:port})});}
// ---- карты + бегунок ----
let mapBin=null,hlIds={fuel:null,ign:null};
function renderMap(m,prefix){
 let h='<table class=map><tr><th class=corner>об\\нагр</th>';
 for(const c of m.cols)h+='<th>'+c+'</th>';h+='</tr>';
 for(let r=0;r<16;r++){h+='<tr><th>'+m.rows[r]+'</th>';
  for(let c=0;c<16;c++){const v=m.cells[r*16+c];
   const cls=(v===null)?' class=flag':'';const disp=(v===null)?'фл':v;
   h+='<td id='+prefix+'_'+r+'_'+c+cls+'>'+disp+'</td>';}
  h+='</tr>';}
 return h+'</table>';}
function setHL(prefix,hr,hc){
 if(hlIds[prefix]){const e=document.getElementById(hlIds[prefix]);if(e)e.classList.remove('hl');hlIds[prefix]=null;}
 if(hr>=0&&hc>=0){const id=prefix+'_'+hr+'_'+hc;const e=document.getElementById(id);if(e){e.classList.add('hl');hlIds[prefix]=id;}}}
// ---- левая таблица логируемых (стики в топе, значение+ед./у.е./сырьё) ----
// СТИКИ-ТОП = HUD из d.top (человеческие значения), не сырые АЦП
const TOP=[['Обороты','rpm',''],['Нагрузка','tp',''],['Газ %','tps_pct','%'],['Темп ОЖ','temp',''],['ALPHA','alpha',''],
           ['AFR цель','afr_target',''],['AFR факт','afr_fact',''],['УОЗ','uoz_deg','°'],
           ['Впрыск мс','inj_ms',''],['Загрузка форс','inj_duty','%'],['Поправка VE','ve_corr','×']];
let varsBuilt=0;
function renderVars(vars,top){
 const tb=document.getElementById('vars');
 if(varsBuilt!==vars.length){
  let h='';
  TOP.forEach((t,j)=>{h+='<tr class=sticky><td>'+t[0]+'</td><td class=val id=tv'+j+'></td></tr>';});
  for(let i=0;i<vars.length;i++){h+='<tr><td>'+vars[i].name+'</td><td class=val id=vv'+i+'></td></tr>';}
  tb.innerHTML=h;varsBuilt=vars.length;}
 TOP.forEach((t,j)=>{const c=document.getElementById('tv'+j);
  const v=(top&&top[t[1]]!=null)?(top[t[1]]+t[2]):'—';
  if(c.textContent!==v)c.textContent=v;});
 for(let i=0;i<vars.length;i++){const v=vars[i];const c=document.getElementById('vv'+i);
  let disp;
  if(v.val===null)disp='—';
  else if(v.real!==null)disp=v.real+' <span class=unit>'+(v.unit||'у.е.')+'</span>';
  else disp=v.val+' <span class=unit>('+(v.unit||'у.е.')+', сырьё)</span>';
  if(c.dataset.d!==disp){c.innerHTML=disp;c.dataset.d=disp;}
 }}
// ---- ОНЛАЙН: вычит теней из проца, правка ячеек → poke, сохранение ----
let online=false,editRendered=false;const ONLINE={fuel:null,ign:null},AX={};
// защита от потери прогресса: состояние онлайна в память браузера
function saveProg(){try{localStorage.setItem('j30online',JSON.stringify({on:online,fuel:ONLINE.fuel,ign:ONLINE.ign}));}catch(_){}}
function loadProg(){try{const s=JSON.parse(localStorage.getItem('j30online')||'null');
 if(s&&s.on&&s.fuel){online=true;ONLINE.fuel=s.fuel;ONLINE.ign=s.ign;editRendered=false;
  const b=document.getElementById('btnOnline');if(b)b.classList.add('on');
  document.getElementById('btnSaveBin').style.display='';
  document.getElementById('tobin_fuel').style.display='';document.getElementById('tobin_ign').style.display='';
  document.getElementById('onstat').textContent='ОНЛАЙН восстановлен из памяти браузера — прогресс не потерян';}}catch(_){}}
// байт↔физика (как в редакторе). Смесь: 2 кластера AFR; угол: байт=градусы
function afrOf(x){return (x>=128)?Math.round(188160/(x-64))/100:Math.round(188160/(x+128))/100;}
function afrToByte(afr,cur){  // остаёмся в кластере текущего байта, чтоб не прыгать кодировку
 let b=(cur>=128)?Math.round(1881.6/afr+64):Math.round(1881.6/afr-128);
 return Math.max(0,Math.min(255,b));}
function physOf(which,b){return (which==='fuel')?afrOf(b):b;}   // угол: байт=градусы
function renderEdit(which){
 const arr=ONLINE[which],ax=AX[which];if(!arr||!ax)return;
 let h='<table class=map><tr><th class=corner>об\\нагр</th>';
 for(const c of ax.cols)h+='<th>'+c+'</th>';h+='</tr>';
 for(let r=0;r<16;r++){h+='<tr><th>'+ax.rows[r]+'</th>';
  for(let c=0;c<16;c++){const idx=r*16+c,b=arr[idx];
   h+='<td id='+which+'_'+r+'_'+c+' class=ec title="байт '+b+'"><input value="'+physOf(which,b)+'" onchange="cellEdit(\''+which+'\','+idx+',this)"></td>';}
  h+='</tr>';}
 document.getElementById(which==='fuel'?'fuelmap':'ignmap').innerHTML=h+'</table>';}
async function cellEdit(which,idx,el){
 let val=parseFloat(el.value);
 if(isNaN(val)){el.value=physOf(which,ONLINE[which][idx]);return;}
 // ФИЗИКА → БАЙТ (смесь=AFR, угол=градусы)
 let byte=(which==='fuel')?afrToByte(val,ONLINE[which][idx]):Math.max(0,Math.min(255,Math.round(val)));
 const td=el.parentNode;td.classList.remove('ok','err');td.classList.add('pend');
 const r=await fetch('/api/pokecell',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:which,idx:idx,val:byte})});
 const d=await r.json();td.classList.remove('pend');
 if(d.ok&&d.applied){ONLINE[which][idx]=byte;saveProg();td.classList.add('ok');td.title='байт '+byte;el.value=physOf(which,byte);}
 else{td.classList.add('err');td.title='НЕ применилось: в проце '+d.readback;}}
async function goOnline(){
 const o=document.getElementById('onstat');
 if(!online){o.textContent='выгрузка карт в тень (C7, стоком)...';
  await fetch('/api/cmd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({byte:0xC7})});}
 else o.textContent='перечитываю тени из проца (БЕЗ сброса тюна)...';
 online=true;document.getElementById('btnOnline').classList.add('on');editRendered=true;
 for(const w of ['fuel','ign']){
  o.textContent='вычит '+(w==='fuel'?'смеси':'угла')+' из проца, ~90с...';
  const r=await fetch('/api/readtable',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:w})});
  const d=await r.json();
  if(d.ok){ONLINE[w]=d.cells;renderEdit(w);}else{o.textContent='ошибка вычита: '+d.error;return;}
 }
 document.getElementById('btnSaveBin').style.display='';
 document.getElementById('tobin_fuel').style.display='';document.getElementById('tobin_ign').style.display='';
 saveProg();
 o.textContent='ОНЛАЙН: правь ячейку → уходит в прошивку сразу (зелёная=применилось, красная=нет)';}
async function saveBin(){
 const r=await fetch('/api/savebin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fuel:ONLINE.fuel,ign:ONLINE.ign})});
 const d=await r.json();
 document.getElementById('onstat').textContent=d.ok?('сохранено: '+d.name):('ошибка: '+(d.error||''));}
async function applyBin(which){
 const o=document.getElementById('onstat');o.textContent='привожу '+which+' к бину...';
 const r=await fetch('/api/applybin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:which})});
 const d=await r.json();
 if(d.ok){ONLINE[which]=d.cells;saveProg();renderEdit(which);o.textContent=which+' приведён к бину ✓';}
 else o.textContent='ошибка: '+d.error;}
// ---- тик ----
function tick(){fetch('/api/status').then(r=>r.json()).then(d=>{
 const portSel=document.getElementById('port').value, wportSel=document.getElementById('wport').value;
 setStat('ecuicon', d.error?'err':(!portSel?'none':(d.running&&d.rate>0?'ok':'warn')));
 const wb=d.wbl||{};
 setStat('wblicon', wb.error?'err':(!wportSel?'none':(wb.running&&(wb.afr!=null||(wb.raw&&wb.raw.length>2))?'ok':'warn')));
 // ОНЛАЙН доступен только когда ЭБУ реально стримит
 const conn=d.running&&d.rate>0;
 const bo=document.getElementById('btnOnline'); if(bo)bo.disabled=!conn&&!online;
 renderVars(d.vars||[], d.top||{});
 if(d.fuel&&d.ign){
  AX.fuel={rows:d.fuel.rows,cols:d.fuel.cols};AX.ign={rows:d.ign.rows,cols:d.ign.cols};
  if(!online&&mapBin!==d.bin){  // в онлайне карты редактируемые — не затираем
   document.getElementById('fuelmap').innerHTML=renderMap(d.fuel,'fuel');
   document.getElementById('ignmap').innerHTML=renderMap(d.ign,'ign');
   mapBin=d.bin;hlIds={fuel:null,ign:null};}
  // восстановление онлайна из памяти браузера: отрисовать редактируемые таблицы когда оси готовы
  if(online&&ONLINE.fuel&&AX.fuel&&!editRendered){renderEdit('fuel');renderEdit('ign');editRendered=true;}
  setHL('fuel',d.fuel.hr,d.fuel.hc);setHL('ign',d.ign.hr,d.ign.hc);
 }
}).catch(e=>{}).finally(()=>setTimeout(tick,400));}
function toggletheme(){const dark=document.getElementById('darkbox').checked;
 document.body.classList.toggle('light',!dark);
 try{localStorage.setItem('j30theme',dark?'dark':'light');}catch(_){}}
try{if(localStorage.getItem('j30theme')=='dark'){document.body.classList.remove('light');document.getElementById('darkbox').checked=true;}}catch(_){}
loadProg();loadPorts();loadBins();tick();
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path.startswith("/api/status"): self._json(snapshot()); return
        if self.path.startswith("/api/ports"):
            ports, sug = list_ports()
            with LOCK: ep = STATE["port"] if STATE["running"] else ""
            with WLOCK: wp = WBL["port"] if WBL["running"] else ""
            self._json({"ports": ports, "suggested": sug, "ecu_port": ep, "wbl_port": wp}); return
        if self.path.startswith("/api/bins"):
            bins = [{"path": p, "name": os.path.basename(p)} for p in list_bins()]
            self._json({"bins": bins, "selected": SEL["bin"]}); return
        if self.path.startswith("/api/log/download"):
            fn = LOGST["path"]
            if not (fn and os.path.exists(fn)):   # фолбэк — последний CSV в логи/
                cands = sorted(glob.glob(os.path.join(HERE, "логи", "*.csv")), key=os.path.getmtime)
                fn = cands[-1] if cands else None
            if fn and os.path.exists(fn):
                data = open(fn, "rb").read()
                self.send_response(200); self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="%s"' % os.path.basename(fn))
                self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            else:
                self.send_response(404); self.end_headers()
            return
        if self.path.startswith("/api/download"):
            with LOCK: fn = STATE["file"]
            if not (fn and os.path.exists(fn)):   # запасной вариант — последний файл в сырьё/
                cands = sorted(glob.glob(os.path.join(HERE, "сырьё", "*.bin")), key=os.path.getmtime)
                fn = cands[-1] if cands else None
            if fn and os.path.exists(fn):
                data = open(fn, "rb").read()
                self.send_response(200); self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", 'attachment; filename="%s"' % os.path.basename(fn))
                self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            else:
                self.send_response(404); self.end_headers()
            return
        body = PAGE.encode()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(ln) if ln else b"{}"
        try: data = json.loads(raw or b"{}")
        except Exception: data = {}
        if self.path.startswith("/api/start"):
            ok, err = do_start(data.get("port", ""), data.get("baud", 125000)); self._json({"ok": ok, "error": err}); return
        if self.path.startswith("/api/stop"):
            do_stop(); self._json({"ok": True}); return
        if self.path.startswith("/api/selectbin"):
            p = data.get("bin", "")
            if p == "": SEL["bin"] = ""            # сброс в «не выбрано»
            elif os.path.exists(p): SEL["bin"] = p
            self._json({"ok": True}); return
        if self.path.startswith("/api/poke"):
            try:
                a = int(data.get("addr", 0)) & 0xFFFF; v = int(data.get("val", 0)) & 0xFF
                s = CTRL.get("ser")
                if s: _send_cmd(s, [0xC5, a >> 8, a & 0xFF, v]); self._json({"ok": True})
                else: self._json({"ok": False, "error": "порт не открыт — Старт"})
            except Exception as e: self._json({"ok": False, "error": str(e)})
            return
        if self.path.startswith("/api/cmd"):
            # одиночная команда (C7=выгрузить в тень, C8=назад на ROM)
            try:
                b = int(data.get("byte", 0)) & 0xFF
                s = CTRL.get("ser")
                if s: _send_cmd(s, [b]); self._json({"ok": True})
                else: self._json({"ok": False, "error": "порт не открыт — Старт"})
            except Exception as e: self._json({"ok": False, "error": str(e)})
            return
        if self.path.startswith("/api/readtable"):
            # ВЫЧИТ всей таблицы из проца через peek (256 ячеек, ~90с) — раз на вход в онлайн
            which = data.get("which", "fuel"); s = CTRL.get("ser"); base = SHADOW.get(which)
            if not s or base is None: self._json({"ok": False, "error": "нет ЭБУ/таблицы"}); return
            cells = []
            for i in range(256):
                a = base + i
                _send_cmd(s, [0xC6, a >> 8, a & 0xFF]); v = _probe_wait(0x1600)
                cells.append(v if v is not None else 0)
            self._json({"ok": True, "which": which, "cells": cells}); return
        if self.path.startswith("/api/pokecell"):
            which = data.get("which", "fuel"); idx = int(data.get("idx", 0)) & 0xFF; val = int(data.get("val", 0)) & 0xFF
            s = CTRL.get("ser"); base = SHADOW.get(which)
            if not s or base is None: self._json({"ok": False, "error": "нет ЭБУ"}); return
            a = base + idx
            _send_cmd(s, [0xC5, a >> 8, a & 0xFF, val])
            _send_cmd(s, [0xC6, a >> 8, a & 0xFF]); rb = _probe_wait(0x1600)
            self._json({"ok": True, "applied": rb == val, "readback": rb}); return
        if self.path.startswith("/api/applybin"):
            # привести всю таблицу к значениям бина (poke каждой ячейки)
            which = data.get("which", "fuel"); s = CTRL.get("ser"); base = SHADOW.get(which)
            t = load_tables(SEL["bin"])
            if not s or base is None or not t: self._json({"ok": False, "error": "нет ЭБУ/бина"}); return
            arr = t[which]
            for i in range(256):
                a = base + i
                _send_cmd(s, [0xC5, a >> 8, a & 0xFF, arr[i] & 0xFF])
            self._json({"ok": True, "cells": arr}); return
        if self.path.startswith("/api/savebin"):
            # запечь текущие таблицы (с фронта) в копию бина → логи/<бин>_лог_дата.bin
            if not SEL.get("bin"): self._json({"ok": False, "error": "бин не выбран"}); return
            try:
                rom = bytearray(open(SEL["bin"], "rb").read()); assert len(rom) == 32768
                for which, off in BINOFF.items():
                    arr = data.get(which)
                    if arr and len(arr) == 256:
                        rom[off:off + 256] = bytes(b & 0xFF for b in arr)
                recalc_checksum(rom)
                d = os.path.join(HERE, "логи"); os.makedirs(d, exist_ok=True)
                bn = os.path.splitext(os.path.basename(SEL["bin"]))[0]
                fn = os.path.join(d, bn + "_лог_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bin")
                open(fn, "wb").write(rom)
                self._json({"ok": True, "name": os.path.basename(fn)})
            except Exception as e:
                self._json({"ok": False, "error": str(e)})
            return
        if self.path.startswith("/api/peek"):
            try:
                a = int(data.get("addr", 0)) & 0xFFFF
                s = CTRL.get("ser")
                if s: _send_cmd(s, [0xC6, a >> 8, a & 0xFF]); self._json({"ok": True})
                else: self._json({"ok": False, "error": "порт не открыт — Старт"})
            except Exception as e: self._json({"ok": False, "error": str(e)})
            return
        if self.path.startswith("/api/ramprobe"):
            s = CTRL.get("ser")
            if not s: self._json({"ok": False, "error": "порт не открыт — Старт"}); return
            res = []
            for a in data.get("addrs", []):
                a &= 0xFFFF
                if a < 0x40 or (0x1000 <= a <= 0x106F):   # регистры/UPP — не трогаем
                    res.append({"addr": a, "ram": None, "skip": "регистр/UPP"}); continue
                _send_cmd(s, [0xC6, a >> 8, a & 0xFF]); orig = _probe_wait(0x1600)
                _send_cmd(s, [0xC5, a >> 8, a & 0xFF, 0xAA]); v1 = _probe_wait(0x1600)
                _send_cmd(s, [0xC5, a >> 8, a & 0xFF, 0x55]); v2 = _probe_wait(0x1600)
                _send_cmd(s, [0xC5, a >> 8, a & 0xFF, orig if orig is not None else 0])  # restore
                res.append({"addr": a, "ram": (v1 == 0xAA and v2 == 0x55), "orig": orig})
            self._json({"ok": True, "res": res})
            return
        if self.path.startswith("/api/tx/hold"):
            # непрерывный поток (для замера просадки на ноге). Байт 0 = линия внизу 90% времени
            v = int(data.get("byte", 0)) & 0xFF
            on = bool(data.get("on", False))
            TXFLOOD["byte"] = v; TXFLOOD["on"] = on
            if on and not TXFLOOD["thread_alive"] and CTRL.get("ser"):
                TXFLOOD["thread_alive"] = True
                threading.Thread(target=tx_flood_loop, daemon=True).start()
            self._json({"ok": bool(CTRL.get("ser")), "error": "" if CTRL.get("ser") else "порт не открыт — Старт"})
            return
        if self.path.startswith("/api/tx"):
            # RX-тест: шлём байт в ЭБУ по тому же порту (FTDI TX → Rx блока)
            try:
                v = int(data.get("byte", 0)) & 0xFF
                s = CTRL.get("ser")
                if s: s.write(bytes([v])); self._json({"ok": True, "error": ""})
                else: self._json({"ok": False, "error": "порт не открыт — нажми Старт"})
            except Exception as e:
                self._json({"ok": False, "error": str(e)})
            return
        if self.path.startswith("/api/wbl/start"):
            ok, err = wbl_start(data.get("port", "")); self._json({"ok": ok, "error": err}); return
        if self.path.startswith("/api/wbl/stop"):
            wbl_stop(); self._json({"ok": True}); return
        if self.path.startswith("/api/log/start"):
            ok, fn = log_start(); self._json({"ok": ok, "file": fn}); return
        if self.path.startswith("/api/log/stop"):
            log_stop(); self._json({"ok": True}); return
        self._json({"ok": False, "error": "unknown"}, 404)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--http", type=int, default=8009)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", args.http), H)
    print("Панель:  http://localhost:%d" % args.http)
    try: srv.serve_forever()
    except KeyboardInterrupt: do_stop(); print("\nОстановлено.")


if __name__ == "__main__":
    main()
