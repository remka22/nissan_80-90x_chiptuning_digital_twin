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
    (0x1411, "Впрыск факт",          16, "мс",                 0.005),  # $142A×$1413+deadtime
    # --- ДРОССЕЛЬ (TPS) — всё вместе ---
    (0x1492, "TPS дроссель",         16, "сырьё 10б",          None),   # аналог. дроссель, ch6
    (0x14A2, "TPS открытие",          8, "АЦП $1492 (от ХХ)",  2),      # ×2 = шкала $1492, как в редакторе
    (0x14A3, "TPS скорость откр.",    8, "АЦП $1492/такт",     2),      # газуешь → >0
    (0x14DE, "Обогащ. ускорения",    16, "добавка в форсунку", None),   # накачка при газовке
    (0x00B9, "Флаг TPS",              8, "0x20=ХХ/WOT/обрыв",  None),
    # --- ДАД: выбранные из ОЗУ ---
    (0x00F8, "VE выбранное",          8, "×нап (128=1.0)",     0.0078125),  # карта 0x4900
    (0x00F9, "Ktps выбранное",        8, "× (128=1.0)",        0.0078125),  # карта 0x4B00
    # --- концевики / флаги режима ---
    (0x0054, "Флаг ХХ/газ",           8, "б0=ХХ",              None),
    (0x0015, "Банк концевиков",       8, "0x10ХХ 0x20нейтр 0x40ГУР 0x80AC", None),
    (0x0053, "Флаги угла",            8, "б0ХХ б1крэнк б2нейтр", None),
    (0x00AE, "Замкнутый цикл",        8, "0x80=вошёл",         None),
    # --- УОЗ ---
    (0x140F, "УОЗ финал",             8, "град (доставленный)", None),
    (0x143B, "УОЗ карта",             8, "град (ХХ=0x76F0)",   None),
    # --- контур ХХ ---
    (0x142C, "Цель ХХ",               8, "у.е.",               None),
    (0x004D, "РХХ duty",             16, "у.е.",               None),
    (0x144E, "Ошибка контура ХХ",     8, "у.е. (НЕ впрыск)",   None),
    # --- АЦП опознанные ---
    (0x1408, "АЦП ch0 MAF",          16, "сырьё 10б",          None),
    (0x008F, "АЦП ch1 напряжение",    8, "сырьё",              None),
    (0x004C, "АЦП ch2 темп ОЖ",       8, "сырьё",              None),
    (0x1400, "АЦП ch3 O2",            8, "сырьё",              None),
    # --- АЦП НЕ опознаны (в самый низ, отключай датчик → смотри что в 0/FF) ---
    (0x1402, "АЦП ch4 (?)",           8, "сырьё, не опознан",  None),
    (0x1401, "АЦП ch5 (?)",           8, "сырьё, не опознан",  None),
    (0x1583, "АЦП ch7 Vbatt−",        8, "сырьё (voltage-fb)", None),
    (0x1574, "АЦП ch8 (?)",           8, "сырьё, не опознан",  None),
]

# Узкий кадр v8: маркер $FFF0, 13 байт значений в фикс. порядке (декод по позиции).
# Порядок = ADDR_LIST билдера build_targeted_patch: раскладываем на РЕАЛЬНЫЕ адреса.
NARROW_MARKER = 0xFFF0
# Порядок ДОЛЖЕН совпадать с ADDR_LIST в build_targeted_patch ИИ.py (27 байт).
NARROW_MAP = [
    0x140A, 0x140B, 0x1482, 0x1413, 0x1431, 0x1411, 0x1412,
    0x1408, 0x1409, 0x008F, 0x004C, 0x1400, 0x1402, 0x1401,
    0x1492, 0x1493, 0x1583, 0x1574,
    0x140F, 0x143B, 0x0053,
    0x0015, 0x0054,
    0x142C, 0x004D, 0x004E, 0x144E,
    0x14A2, 0x14A3, 0x14DE, 0x14DF, 0x00B9, 0x00AE,
    0x00F8, 0x00F9,
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
SEL = {"bin": DEFAULT_BIN if os.path.exists(DEFAULT_BIN) else ""}
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
              ["TP_%8", "AFR_цель", "AFR_факт", "поправка_VE", "давление_кПа"])


def _log_row():
    d = snapshot()
    g = lambda x: "" if x is None else x
    row = [round(time.time() - LOGST["t0"], 2)]
    # все декодированные: реал если есть, иначе сырьё
    for v in d["vars"]:
        row.append(v["real"] if v["real"] is not None else g(v["val"]))
    # вычисленные производные
    tp = d["top"]
    row += [round(tp["load"] / 8.0, 2) if tp["load"] is not None else "",
            g(tp["afr_target"]), g(tp["afr_fact"]), g(tp["ve_corr"]), g(tp["press"])]
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
    fn = os.path.join(d, "лог_" + datetime.now().strftime("%Y%m%d_%H%M%S") + " ИИ.csv")
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
                        if addr == NARROW_MARKER and len(data) == len(NARROW_MAP):
                            # узкий кадр v8: разложить 13 байт по реальным адресам
                            for k, b in enumerate(data):
                                STATE["ram"][NARROW_MAP[k]] = b
                        else:
                            for k, b in enumerate(data):
                                STATE["ram"][addr + k] = b
                    else:
                        STATE["bad"] += 1
    try: ser.close()
    except Exception: pass
    with LOCK: STATE["running"] = False


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
        return True, ""


def do_stop():
    with CTRL_LOCK:
        if CTRL["stop"]: CTRL["stop"].set()
        if CTRL["thread"]: CTRL["thread"].join(timeout=1.0)
        CTRL["thread"] = None; CTRL["stop"] = None; CTRL["ser"] = None
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
        "afr_fact": wbl["afr"], "press": None, "ve_corr": None,
    }
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
</style></head><body>
<header><h1>&#128225; Панель логгера ЭБУ — что рассказывает блок</h1></header>

<!-- ЛИПКИЙ ВЕРХ: лог-кнопки + строка живых параметров -->
<div class=topstick>
<div class=logbar>
 <button class=start id=logStart onclick=logstart()>&#9679; Старт лог</button>
 <button class=stop id=logStop onclick=logstop() disabled>&#9632; Стоп лог</button>
 <span class=st id=logst>лог выключен</span>
 <a class=dl href="/api/log/download" download>&#11015; CSV</a>
 <span class=st style="margin-left:auto">CSV = интерпретированные значения (5 Гц)</span>
</div>
<div class=hud id=hud>
 <div class=cell><div class=lbl>Обороты</div><div class="num na" id=t_rpm>—</div></div>
 <div class=cell><div class=lbl>Нагрузка</div><div class="num na" id=t_load>—</div></div>
 <div class=cell><div class=lbl>Темп сырьё</div><div class="num na" id=t_temp>—</div></div>
 <div class=cell><div class=lbl>ALPHA</div><div class="num na" id=t_alpha>—</div></div>
 <div class="cell tgt"><div class=lbl>AFR цель</div><div class="num na" id=t_tgt>—</div></div>
 <div class="cell fact"><div class=lbl>AFR факт</div><div class="num na" id=t_fact>—</div></div>
 <div class="cell uoz"><div class=lbl>УОЗ</div><div class="num na" id=t_uoz>—</div></div>
 <div class="cell vec" id=cell_vec style="display:none"><div class=lbl>Поправка VE</div><div class="num na" id=t_vecorr>—</div></div>
</div>
</div>

<!-- ПАНЕЛЬ ШДК (AFR факт) — свой порт, 9600 8N1 -->
<div class=wblbar>
 <div class=fld><label>Порт ШДК</label><select id=wport></select></div>
 <button class=ghost onclick=loadPorts()>&#8635;</button>
 <button class=start id=wStart onclick=wstart()>&#9654; ШДК</button>
 <button class=stop id=wStop onclick=wstop() disabled>&#9632;</button>
 <div class=fld><label>сырьё ШДК (9600 8N1)</label><div class=raw id=wraw>— (нет данных)</div></div>
</div>

<!-- КАРТЫ смеси и угла из выбираемого бина (по умолч. v8-дамп), подсветка ячейки -->
<div class=maps>
 <div style="width:100%;display:flex;gap:10px;align-items:end;flex-wrap:wrap">
   <div class=fld><label>Бин для карт</label><select id=binsel onchange=selbin()></select></div>
   <span style="font-size:12px;color:#8aa">зелёная рамка = текущая ячейка (обороты×нагрузка)</span>
 </div>
 <div class=mapbox><h2>&#9819; Карта смеси (AFR) &nbsp;<span id=binlbl style="color:#678;font-weight:400"></span></h2><div id=fuelmap>—</div></div>
 <div class=mapbox><h2>&#9889; Карта угла (УОЗ, град)</h2><div id=ignmap>—</div></div>
 <div class=mapbox id=vebox style="display:none"><h2>&#127777; Карта VE (наполнение ×, 1.0=номинал) — ДАД</h2><div id=vemap>—</div></div>
 <div class=mapbox id=ktpsbox style="display:none"><h2>&#127919; Карта Ktps (× дроссель, 1.0=номинал) — ДАД</h2><div id=ktpsmap>—</div></div>
</div>

<div class=panel>
 <div class=fld><label>Порт</label><select id=port></select></div>
 <button class=ghost onclick=loadPorts()>&#8635; порты</button>
 <div class=fld><label>Скорость</label>
   <select id=baudsel onchange="document.getElementById('baud').value=this.value">
     <option value=2000>2000 (v7 E/1024)</option>
     <option value=15625 selected>15625 (v6 E/128)</option>
     <option value=128000>128000 (v5 E/16)</option>
     <option value=9600>9600</option><option value=115200>115200</option><option value=250000>250000</option>
   </select></div>
 <div class=fld><label>или своё</label><input class=baud id=baud value=15625></div>
 <button class=start id=btnStart onclick=start()>&#9654; Старт</button>
 <button class=stop id=btnStop onclick=stop() disabled>&#9632; Стоп</button>
</div>
<div id=banner class=off>остановлено</div>
<div class=stats>
 <span>всего: <b id=total>0</b> б</span><span><b id=rate>0</b> б/с</span>
 <span>кадров: <b id=frames>0</b></span><span>битых: <b id=bad>0</b></span>
 <span>адресов ОЗУ: <b id=ramc>0</b></span><span>файл: <b id=file>—</b></span>
</div>
<div class=wrap>
 <div class=col>
   <h2>&#128202; Расшифровка (сырые значения)</h2>
   <table><thead><tr><th>Переменная</th><th>Адрес</th><th>Сырьё</th><th>Ед.</th><th>Реал</th></tr></thead>
   <tbody id=vars></tbody></table>
 </div>
 <div class=col>
   <h2>&#128190; Образ ОЗУ</h2>
   <pre id=ram>—</pre>
 </div>
</div>
<div class=foot><a class=dl href="/api/log/download" download>&#11015; Скачать CSV-лог</a></div>
<script>
async function loadPorts(){
 try{const r=await fetch('/api/ports');const d=await r.json();
  for(const sid of ['port','wport']){
    const busy = (sid==='port') ? d.wbl_port : d.ecu_port;  // исключить порт ДРУГОГО ридера
    const s=document.getElementById(sid);const cur=s.value;s.innerHTML='';
    d.ports.forEach(p=>{if(busy&&p.device===busy)return;   // занят другим — не показываем
      const o=document.createElement('option');o.value=p.device;
      o.textContent=p.device+(p.ftdi?' (FTDI)':'');s.appendChild(o);});
    if(cur&&cur!==busy)s.value=cur; else if(sid==='port'&&d.suggested&&d.suggested!==busy)s.value=d.suggested;
  }}catch(e){}
}
async function loadBins(){
 try{const r=await fetch('/api/bins');const d=await r.json();
  const s=document.getElementById('binsel');s.innerHTML='';
  d.bins.forEach(b=>{const o=document.createElement('option');o.value=b.path;o.textContent=b.name;s.appendChild(o);});
  if(d.selected)s.value=d.selected;}catch(e){}
}
async function selbin(){const p=document.getElementById('binsel').value;
 await fetch('/api/selectbin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({bin:p})});mapBin=null;}
async function wstart(){const port=document.getElementById('wport').value;
 if(!port){alert('Порт ШДК не выбран');return;}
 const r=await fetch('/api/wbl/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({port})});
 const d=await r.json();if(!d.ok)alert('ШДК не удалось: '+d.error);loadPorts();}
async function wstop(){await fetch('/api/wbl/stop',{method:'POST'});loadPorts();}
async function logstart(){await fetch('/api/log/start',{method:'POST'});}
async function logstop(){await fetch('/api/log/stop',{method:'POST'});}
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
function setNum(id,val,suf){const e=document.getElementById(id);
 const t=(val===null||val===undefined)?'—':(val+(suf||''));
 if(e.textContent!==t)e.textContent=t;
 e.classList.toggle('na',val===null||val===undefined);}
let varsBuilt=0;
function renderVars(vars){
 const tb=document.getElementById('vars');
 if(varsBuilt!==vars.length){  // строим скелет ОДИН раз (имя/адрес/ед. статичны — копируй свободно)
  let h='';
  for(let i=0;i<vars.length;i++){const v=vars[i];
   h+='<tr><td>'+v.name+'</td><td class=a>'+v.addr+'</td><td id=vv'+i+'></td><td class=u>'+v.unit+'</td><td id=vr'+i+'></td></tr>';}
  tb.innerHTML=h;varsBuilt=vars.length;
 }
 for(let i=0;i<vars.length;i++){const v=vars[i];  // обновляем ТОЛЬКО значения, и только если изменились
  const cv=document.getElementById('vv'+i),cr=document.getElementById('vr'+i);
  const sv=(v.val===null)?'—':(''+v.val), sr=(v.real===null)?'—':(''+v.real);
  if(cv.textContent!==sv){cv.textContent=sv;cv.className=(v.val===null)?'na':'v';}
  if(cr.textContent!==sr){cr.textContent=sr;cr.className=(v.real===null)?'na':'r';}
 }}
async function start(){const port=document.getElementById('port').value;const baud=document.getElementById('baud').value;
 if(!port){alert('Порт не выбран');return;}
 const r=await fetch('/api/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({port,baud})});
 const d=await r.json();if(!d.ok)alert('Не удалось: '+d.error);loadPorts();}
async function stop(){await fetch('/api/stop',{method:'POST'});loadPorts();}
function tick(){fetch('/api/status').then(r=>r.json()).then(d=>{
 // блокировка ПАР кнопок ПЕРВЫМ делом (до отрисовки, чтоб не сорвалось при ошибке ниже)
 const _wb=d.wbl||{}, _lg=d.log||{};
 document.getElementById('btnStart').disabled=!!d.running; document.getElementById('btnStop').disabled=!d.running;
 document.getElementById('wStart').disabled=!!_wb.running;  document.getElementById('wStop').disabled=!_wb.running;
 document.getElementById('logStart').disabled=!!_lg.on;     document.getElementById('logStop').disabled=!_lg.on;
 const b=document.getElementById('banner');
 if(d.error){b.className='err';b.textContent='ОШИБКА: '+d.error;}
 else if(d.running&&d.rate>0){b.className='live';b.textContent='● ПОТОК ИДЁТ ('+d.port+' @ '+d.baud+')';}
 else if(d.running){b.className='quiet';b.textContent='порт открыт, байт нет';}
 else{b.className='off';b.textContent='остановлено';}
 document.getElementById('total').textContent=d.total;document.getElementById('rate').textContent=d.rate;
 document.getElementById('frames').textContent=d.frames;document.getElementById('bad').textContent=d.bad;
 document.getElementById('ramc').textContent=d.ram_count;document.getElementById('file').textContent=d.file_short||'—';
 renderVars(d.vars);
 const rt=(d.ram_lines&&d.ram_lines.length)?d.ram_lines.join('\n'):'— (ждём кадры)';
 const re=document.getElementById('ram'); if(re.textContent!==rt)re.textContent=rt;
 document.getElementById('btnStart').disabled=d.running;document.getElementById('btnStop').disabled=!d.running;
 // верхняя строка
 const tp=d.top||{};
 setNum('t_rpm',tp.rpm);setNum('t_load',tp.tp);setNum('t_temp',tp.temp);setNum('t_alpha',tp.alpha);
 setNum('t_tgt',tp.afr_target);setNum('t_fact',tp.afr_fact);setNum('t_uoz',tp.uoz);
 // сырьё ШДК
 const wb=d.wbl||{};
 document.getElementById('wraw').textContent=(wb.raw&&wb.raw.length)?(wb.raw+'   ['+(wb.hex||'')+']'):(wb.error?('ошибка: '+wb.error):(wb.running?'порт открыт, байт нет':'— (нет данных)'));
 document.getElementById('wStart').disabled=wb.running;document.getElementById('wStop').disabled=!wb.running;
 // карты (перестраиваем при смене бина, подсветку двигаем каждый тик)
 if(d.fuel&&d.ign){
  if(mapBin!==d.bin){
   document.getElementById('fuelmap').innerHTML=renderMap(d.fuel,'fuel');
   document.getElementById('ignmap').innerHTML=renderMap(d.ign,'ign');
   document.getElementById('binlbl').textContent=d.bin||'';
   const vb=document.getElementById('vebox');
   if(d.ve){document.getElementById('vemap').innerHTML=renderMap(d.ve,'ve');vb.style.display='';}
   else vb.style.display='none';
   const kb=document.getElementById('ktpsbox');
   if(d.ktps){document.getElementById('ktpsmap').innerHTML=renderMap(d.ktps,'ktps');kb.style.display='';}
   else kb.style.display='none';
   mapBin=d.bin;hlIds={fuel:null,ign:null,ve:null,ktps:null};
  }
  setHL('fuel',d.fuel.hr,d.fuel.hc);setHL('ign',d.ign.hr,d.ign.hc);
  if(d.ve)setHL('ve',d.ve.hr,d.ve.hc);
  if(d.ktps)setHL('ktps',d.ktps.hr,d.ktps.hc);
 }
 // ДАД: ячейка «Поправка VE»
 const cv=document.getElementById('cell_vec');
 if(tp.is_dad){cv.style.display='';setNum('t_vecorr',tp.ve_corr,'×');}else cv.style.display='none';
 // статус лога
 const lg=d.log||{};
 const ls=document.getElementById('logst');
 if(lg.on){ls.className='rec';ls.textContent='● ЗАПИСЬ ИДЁТ — '+(lg.file||'')+' ('+lg.n+' строк)';}
 else{ls.className='st';ls.textContent=lg.file?('остановлен: '+lg.file+' ('+lg.n+')'):'лог выключен';}
 document.getElementById('logStart').disabled=lg.on;document.getElementById('logStop').disabled=!lg.on;
}).catch(e=>{}).finally(()=>setTimeout(tick,400));}
loadPorts();loadBins();tick();
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
            if p and os.path.exists(p): SEL["bin"] = p
            self._json({"ok": True}); return
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
