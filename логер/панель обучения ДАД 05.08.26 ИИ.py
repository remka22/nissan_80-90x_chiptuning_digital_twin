# -*- coding: utf-8 -*-
"""
ПАНЕЛЬ ЛОГГЕРА ЭБУ — веб-админка + РАСШИФРОВКА дампа ОЗУ.

Запуск:  python3 "логер/панель логгера 31.07.26 ИИ.py"   → http://localhost:8009
Из браузера: выбор порта, скорость, Старт/Стоп, живые ЗНАЧЕНИЯ (обороты, нагрузка,
O2, напряжение, темпа, впрыск...), полный образ ОЗУ, запись сырья в файл.

Скорости под версии дампа:  v5(E/16)=125000  v6(E/128)=16000  v7(E/1024)=2000
"""
import argparse, threading, time, json, os, collections
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
    (0x004D, "Впрыск РЕАЛ (форс)",   16, "мс",                 0.010),  # $004D→UPP-каналы, ТИК 10 мкс (испр. 04.08.26)
    # --- СОСТОЯНИЕ ТЕНИ (v18): одна тень на все карты, поэтому в кадре не указатели, а состояние ---
    (0x17F8, "Карта в тени",          8, "0 нет / 1 смесь / 2 угол", None),
    (0x17F9, "Вердикт указателя",     8, "0 ПЗУ / 1 тень / 255 АВАРИЯ", None),
    (0x17FA, "XOR тени",              8, "сверка содержимого",  None),
    (0x17FB, "Сумма тени",            8, "сверка содержимого",  None),
    # --- ДРОССЕЛЬ (TPS) ---
    (0x141A, "Карта топлива вернула",8, "сырьё",              None),
    (0x1492, "TPS дроссель",         16, "сырьё 10б",          None),   # аналог. дроссель, ch6
    (0x14A2, "TPS открытие",          8, "сырьё (от нуля)",    None),  # % считается отдельно из $1492: (ацп−мин)/344
    (0x14DE, "Обогащ. ускорения",     8, "добавка в форсунку", None),   # >0 = было обогащение
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
    (0x1408, "АЦП ch0 (МАФ/ДАД)",     8, "сырьё, старший байт", None),
    (0x00F7, "Давление",              8, "кПа (считает рутина ДАД)", None),
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
    0x140A, 0x140B, 0x1482, 0x1413, 0x1431,
    0x17FA, 0x17FB,   # v18: XOR и сумма тени (заняли слоты убранного $1411/$1412)
    0x1408,           # сырьё канала 0 (МАФ, на ДАД-бине — датчик давления), старший байт
    0x00F7,           # v19: ДАВЛЕНИЕ в кПа (заняло слот убранного $1409 — два бита, что ЭБУ и так выбрасывает)
    0x008F, 0x004C, 0x1400,
    0x1492, 0x1493,
    0x140F, 0x143B, 0x0053,
    0x0015, 0x0054, 0x142C,
    0x14A2, 0x14DE, 0x00B9, 0x00AE,   # обогащение — только старший байт (место в кадре)
    0x00F8, 0x00F9,   # VE/Ktps — под ДАД, НЕ занимать
    0x004D, 0x004E,   # РЕАЛЬНЫЙ впрыск в UPP-отсчётах (×0.010=мс, ТИК 10 мкс, испр. 04.08.26)
    0x17F7,   # результат peek (PEEK_OUT)
    0x17F8, 0x17F9,   # v18: какая карта в тени / вердикт по её указателю
    0x141A,   # ЧТО ВЕРНУЛА карта топлива (диагностика)
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
    with WLOCK:
        WBL["running"] = False
        # отключили — значений БОЛЬШЕ НЕТ, а не «последние». Чистим и сырьё: значок ШДК
        # смотрит в т.ч. на raw, и с непочищенным raw оставался бы зелёным после обрыва.
        WBL["afr"] = None; WBL["last_t"] = 0; WBL["raw"] = ""; WBL["hex"] = ""
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


# ---- ОНЛАЙН-тюнинг: одна тень в ОЗУ, карта в ней ВЫБИРАЕТСЯ (v18) ----
# ⚠ ОЗУ в блоке 1280 б, $1800+ НЕ СУЩЕСТВУЕТ (измерено 04.08.26). Тень ОДНА на 256 байт,
# поэтому живой может быть ровно одна карта за раз. Какая именно — говорит команда CB,
# а ЭБУ подтверждает это в кадре ($17F8 номер + $17F9 вердикт по указателю).
SHADOW = {"fuel": 0x1600, "ign": 0x1600, "ve": 0x1600, "ktps": 0x1600}   # тень одна на всех
ROMMAP = {"fuel": 0xFD00, "ign": 0xFC00, "ve": 0xC900, "ktps": 0xCB00}   # базы в ПЗУ
BINOFF = {"fuel": 0x7D00, "ign": 0x7C00, "ve": 0x4900, "ktps": 0x4B00}   # смещения в бине
CBNUM  = {"fuel": 1, "ign": 2, "ve": 3, "ktps": 4}                        # номер в команде CB (0 = отцепить)
SEL_ADDR, VERD_ADDR = 0x17F8, 0x17F9       # что лежит в тени / вердикт по указателю живой карты
CSX_ADDR, CSS_ADDR  = 0x17FA, 0x17FB       # XOR и сумма содержимого тени, считает ЭБУ


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
               "Загрузка_форс_%", "Газ_%", "K_форс", "КМ", "Впрыск расчёт"])


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
            g(tp.get("inj_duty")), g(tp.get("tps_pct")), g(k), g(km),
            g(tp.get("inj_calc"))]
    return row


def _log_sampler(stop_ev):
    # ПИШЕМ ПО ПРИХОДУ КАДРА, а не по таймеру. Раньше таймер 200мс при кадре 410мс
    # дублировал каждую строку дважды: файл выглядел как 5 Гц, данных в нём 2.4 Гц.
    last = -1
    while not stop_ev.is_set():
        fr = STATE.get("frames", 0)
        if fr != last and fr > 0:
            last = fr
            try:
                row = _log_row()
                LOGST["f"].write(";".join(str(x) for x in row) + "\n"); LOGST["f"].flush()
                LOGST["n"] += 1
            except Exception:
                pass
        stop_ev.wait(0.02)


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


# --- перехват C9-дамп-стрима: пока active, reader_loop кладёт сырые байты сюда, парсер кадров молчит ---
DUMPST = {"active": False, "want": 0, "need": 0, "buf": bytearray(), "tail": b"", "until": 0.0}
DUMP_LOCK = threading.Lock()


def reader_loop(ser, stop_ev, fname):
    parser = Parser()   # сырьё НЕ пишем (не нужно, не захламляем папку) — только разбор для панели+CSV
    while not stop_ev.is_set():
        try:
            chunk = ser.read(2048)
        except Exception as e:
            with LOCK: STATE["error"] = f"чтение: {e}"
            break
        if chunk:
            with DUMP_LOCK:
                dumping = DUMPST["active"]
                if dumping:
                    # режим дампа: копим сырьё, кадры не разбираем (ЭБУ кадры не шлёт, пока идёт стрим).
                    # Завершаем СРАЗУ как пришли «преамбула + n», а не по сырому счётчику байт:
                    # иначе ждём хвост возобновившегося кадра — лишние ~68мс на каждый дамп.
                    DUMPST["buf"] += chunk
                    j = DUMPST["buf"].find(b"\x5A\xA5")
                    need = DUMPST["need"]
                    if (j >= 0 and len(DUMPST["buf"]) >= j + 2 + need) or len(DUMPST["buf"]) >= DUMPST["want"]:
                        DUMPST["active"] = False
            if dumping: continue
            with DUMP_LOCK:                       # хвост от дампа — это начало нового кадра
                t = DUMPST["tail"]; DUMPST["tail"] = b""
            if t: chunk = t + chunk
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


# ============================ ОБУЧЕНИЕ ТАБЛИЦ (ДАД) ============================
# Считаем поправку по факту ШДК и раздаём её в карту ТЕМИ ЖЕ билинейными весами,
# которыми заводская выборка $80CF смешивает четыре угла. Если класть всё в ближайшую
# ячейку, интерполяция потом даст перелёт — карта станет «пьяной».
LEARN = {
    "on": False,            # идёт ли обучение
    "which": "",            # какую карту учим (берём живую из ЭБУ)
    "acc": {},              # idx -> [сумма k*вес, сумма весов, число замеров]
    "hits": {},             # idx -> сколько раз ячейка применялась
    "applied": 0,           # всего записей в блок
    "rejects": {},          # причина -> счётчик (видно, почему не учится)
    "base": None,           # снимок карты ДО обучения — для отката
    "last_write": 0.0,
    "last": None,           # куда легла последняя поправка: ячейки, веса, k
    "note": "",
}
LPAR = {
    "min_hits": 3,          # замеров на ячейку до применения
    "damp": 0.7,            # доля поправки за раз (1.0 = сразу всю)
    "max_step": 0.20,       # ограничитель шага на ячейку, доля
    "tps_min": 0.0,         # НЕ учить ниже этого открытия дросселя, %
    "t_cold": 65,           # ТОЖ СЫРЬЁ: БОЛЬШЕ этого = холодный мотор, не учить.
                            # Датчик термисторный, прогрев ЗАНИЖАЕТ сырьё. Две точки замерены
                            # пользователем: сырьё 61 = 53 °C, сырьё 51 = 76 °C → в СРЕДИНЕ
                            # диапазона T ≈ 193.3 − 2.3 × сырьё. На краях характеристика
                            # нелинейная, полную тарировку сделаем отдельно — эту формулу
                            # далеко за пределы 48…61 не тянуть.
    "d_rpm": 150,           # стационар: макс. изменение оборотов за окно
    "d_tps": 3.0,           # стационар: макс. изменение газа, %
    "delay_ms": 350,        # транспортная задержка выхлопа + реакция ШДК
    "afr_lo": 8.0,          # правдоподобие ШДК
    "afr_hi": 20.0,
    "cut_holdoff": 1.0,     # пауза после возврата топлива с ПХХ, с
}
LHIST = collections.deque(maxlen=400)   # (t, rpm, tps, ячейки+веса, цель) — для задержки
LCUT = {"t": 0.0}                        # когда последний раз был ПХХ


def _bilin(val, axis):
    """Доли между точками разбиения оси — так же, как их считает $80CF.
    → [(индекс, вес), ...] : 1 точка если попали в край или ровно в узел, иначе 2."""
    n = len(axis)
    if val <= axis[0]: return [(0, 1.0)]
    if val >= axis[n - 1]: return [(n - 1, 1.0)]
    for i in range(n - 1):
        a, b = axis[i], axis[i + 1]
        if a <= val <= b:
            if b == a: return [(i, 1.0)]
            f = (val - a) / float(b - a)
            if f <= 0.0: return [(i, 1.0)]
            if f >= 1.0: return [(i + 1, 1.0)]
            return [(i, 1.0 - f), (i + 1, f)]
    return [(n - 1, 1.0)]


def _cells_for(rpm_ax, col_ax, rpm, col):
    """Четыре (или две, или одна) ячейки с весами — как их смешивает ЭБУ."""
    out = []
    for r, wr in _bilin(rpm, rpm_ax):
        for c, wc in _bilin(col, col_ax):
            w = wr * wc
            if w > 0.001: out.append((r * 16 + c, w))
    return out


def _learn_reject(reason):
    LEARN["rejects"][reason] = LEARN["rejects"].get(reason, 0) + 1


def _gate(rpm, tps, cool, accel, inj_zero, afr, since_cut):
    """Годен ли замер. ОДНА функция на живое обучение и на обучение по логу —
    иначе они со временем разъедутся и результаты перестанут совпадать.
    → причина отказа или None."""
    if rpm is None or tps is None:              return "нет оборотов/газа"
    if inj_zero:                                return "ПХХ (впрыска нет)"
    if since_cut < LPAR["cut_holdoff"]:         return "пауза после ПХХ"
    if tps < LPAR["tps_min"]:                   return "газ ниже порога"
    if rpm < 500:                               return "мотор не работает"
    if cool is None or cool > LPAR["t_cold"]: return "мотор не прогрет"
    if (accel or 0) > 0:                        return "обогащение ускорения"
    if afr is None:                             return "нет ШДК"
    if not (LPAR["afr_lo"] <= afr <= LPAR["afr_hi"]): return "ШДК вне диапазона"
    return None


def _corr(a):
    """Накопитель ячейки [сумма k*вес, сумма весов, замеров] → множитель с демпфером
    и ограничителем шага."""
    k = a[0] / a[1]
    k = 1.0 + (k - 1.0) * LPAR["damp"]
    lim = LPAR["max_step"]
    return max(1.0 - lim, min(1.0 + lim, k))


def learn_feed(now, ram, top, t, afr_fact):
    """Один кадр → либо замер в накопитель, либо отказ с причиной.
    Вызывается из snapshot(), когда все величины кадра уже разобраны."""
    if not LEARN["on"] or not LEARN["which"]: return
    which = LEARN["which"]
    rpm = top.get("rpm"); tps = top.get("tps_pct")
    # ПХХ ловим по факту длительности впрыска, а не по флагу
    inj_zero = (ram.get(0x004D) == 0 and ram.get(0x004E, 0) == 0)
    if inj_zero: LCUT["t"] = now
    bad = _gate(rpm, tps, ram.get(0x004C), ram.get(0x14DE), inj_zero,
                afr_fact, now - LCUT["t"])
    if bad: return _learn_reject(bad)
    # --- вторая ось карты: у VE давление, у Ktps открытие дросселя ---
    if which == "ve":
        col = top.get("press")
        rax, cax = t.get("ve_rax"), t.get("ve_pax")
    elif which == "ktps":
        col = ram.get(0x14A2)
        rax, cax = t.get("ktps_rax"), t.get("ktps_tax")
    else:
        return _learn_reject("эта карта не учится")
    if col is None or not rax or not cax: return _learn_reject("нет второй оси")
    rpm_ax = [b * 50 for b in rax]
    cells = _cells_for(rpm_ax, list(cax), rpm, col)
    LHIST.append((now, rpm, tps, cells, top.get("afr_target")))
    # --- транспортная задержка: берём ТУ точку, которой соответствует нынешний выхлоп ---
    want = now - LPAR["delay_ms"] / 1000.0
    src = None
    for rec in reversed(LHIST):
        if rec[0] <= want: src = rec; break
    if src is None: return _learn_reject("копится задержка")
    t0, rpm0, tps0, cells0, tgt0 = src
    if tgt0 is None: return _learn_reject("нет цели AFR")
    # --- стационар: с того момента и до сейчас режим не должен был уехать ---
    win = [r for r in LHIST if r[0] >= t0]
    if len(win) >= 2:
        if max(r[1] for r in win) - min(r[1] for r in win) > LPAR["d_rpm"]:
            return _learn_reject("обороты плывут")
        if max(r[2] for r in win) - min(r[2] for r in win) > LPAR["d_tps"]:
            return _learn_reject("газ плывёт")
    # --- сам замер ---
    k = afr_fact / float(tgt0)          # факт беднее цели → k>1 → лить больше
    # что сейчас катается — видно в панели: ячейки и их доли
    LEARN["last"] = {"cells": [[i, round(w, 3)] for i, w in cells0],
                     "k": round(k, 3), "afr": afr_fact, "tgt": tgt0, "t": now}
    for idx, w in cells0:
        a = LEARN["acc"].setdefault(idx, [0.0, 0.0, 0])
        a[0] += k * w; a[1] += w; a[2] += 1
    LEARN["note"] = ""


def learn_apply(ser):
    """Ячейки, набравшие минимум замеров, пересчитать и записать в тень.
    Вызывается из потока управления (держит SER_LOCK снаружи)."""
    which = LEARN["which"]
    if not LEARN["on"] or not which: return 0
    arr = ONLINE_SRV.get(which)
    if not arr or len(arr) != 256: return 0
    ready = [(i, a) for i, a in LEARN["acc"].items() if a[2] >= LPAR["min_hits"] and a[1] > 0]
    if not ready: return 0
    done = 0
    for idx, a in ready:
        nb = int(round(max(1, min(255, arr[idx] * _corr(a)))))
        if nb != arr[idx]:
            ok, _e = _send_block(ser, SHADOW[which] + idx, [nb])
            if not ok: continue
            arr[idx] = nb
            done += 1
        LEARN["acc"].pop(idx, None)                       # ОБНУЛИТЬ: поправка применена
        LEARN["hits"][idx] = LEARN["hits"].get(idx, 0) + 1
    LEARN["applied"] += done
    return done


ONLINE_SRV = {}      # серверная копия живых карт — панель шлёт её при старте обучения


def learn_from_log(path, which, base, t):
    """Тот же движок, но данные не из порта, а из CSV. В блок НИЧЕГО не пишет —
    возвращает предложенную карту, покрытие и причины отказов. Пользователь смотрит
    и заливает сам.
    → (карта 256 байт, {ячейка: замеров}, {причина: сколько}, сколько ячеек изменилось)"""
    import csv as _csv
    if which == "ve":
        rax, cax = t.get("ve_rax"), t.get("ve_pax")
        col_key = "давление_кПа"
    else:
        rax, cax = t.get("ktps_rax"), t.get("ktps_tax")
        col_key = "TPS открытие"
    if not rax or not cax: return None, {}, {"нет осей карты в бине": 1}, 0
    rpm_ax = [b * 50 for b in rax]; col_ax = list(cax)

    def num(row, key):
        v = (row.get(key) or "").replace(",", ".").strip()
        try: return float(v)
        except Exception: return None

    acc = {}; rej = {}; hist = []; cut_t = -1e9
    with open(path, encoding="utf-8-sig") as f:
        for row in _csv.DictReader(f, delimiter=";"):
            tm = num(row, "время_с")
            if tm is None: continue
            rpm = num(row, "Обороты"); tps = num(row, "Газ_%")
            afr = num(row, "AFR_факт"); tgt = num(row, "AFR_цель")
            col = num(row, col_key)
            inj = num(row, "Впрыск РЕАЛ (форс)")
            inj_zero = (inj is not None and inj <= 0.0)
            if inj_zero: cut_t = tm
            bad = _gate(rpm, tps, num(row, "АЦП ch2 темп ОЖ"),
                        num(row, "Обогащ. ускорения"), inj_zero, afr, tm - cut_t)
            if bad: rej[bad] = rej.get(bad, 0) + 1; continue
            if col is None: rej["нет второй оси в логе"] = rej.get("нет второй оси в логе", 0) + 1; continue
            if tgt is None: rej["нет цели AFR"] = rej.get("нет цели AFR", 0) + 1; continue
            hist.append((tm, rpm, tps, _cells_for(rpm_ax, col_ax, rpm, col), tgt, afr))
            # транспортная задержка — по времени ЛОГА, а не по часам компьютера
            want = tm - LPAR["delay_ms"] / 1000.0
            src = None
            for rec in reversed(hist):
                if rec[0] <= want: src = rec; break
            if src is None: rej["копится задержка"] = rej.get("копится задержка", 0) + 1; continue
            t0, _r0, _p0, cells0, tgt0, _a0 = src
            win = [r for r in hist if r[0] >= t0]
            if len(win) >= 2:
                if max(r[1] for r in win) - min(r[1] for r in win) > LPAR["d_rpm"]:
                    rej["обороты плывут"] = rej.get("обороты плывут", 0) + 1; continue
                if max(r[2] for r in win) - min(r[2] for r in win) > LPAR["d_tps"]:
                    rej["газ плывёт"] = rej.get("газ плывёт", 0) + 1; continue
            k = afr / float(tgt0)          # AFR берём СЕЙЧАС, ячейки — из прошлого
            for idx, w in cells0:
                a = acc.setdefault(idx, [0.0, 0.0, 0])
                a[0] += k * w; a[1] += w; a[2] += 1
            if len(hist) > 400: del hist[:200]
    out = list(base); changed = 0
    for idx, a in acc.items():
        if a[2] < LPAR["min_hits"] or a[1] <= 0: continue
        nb = int(round(max(1, min(255, base[idx] * _corr(a)))))
        if nb != base[idx]: changed += 1
        out[idx] = nb
    return out, {i: a[2] for i, a in acc.items()}, rej, changed


def _send_cmd(s, bs, gap=0.0):
    # v7: приёмное прерывание SCI (MYRXISR) кладёт каждый байт в кольцо $1B00 сразу →
    # шлём ВПЛОТНУЮ, без гэпа. Буфер сам сглаживает. (Прежний gap=30мс — для v3 без прерывания.)
    if gap <= 0:
        s.write(bytes(b & 0xFF for b in bs))
        try: s.flush()
        except Exception: pass
        return
    for b in bs:
        s.write(bytes([b & 0xFF]))
        try: s.flush()
        except Exception: pass
        time.sleep(gap)


def _dump_read(s, base, count, timeout=6.0):
    # C9-дамп: ЭБУ стримит [5A A5]+n байт из [base] (по 1 байту за проход задачи, ~10мс).
    # 128 байт ≈ 1.3с → таймаут 6с (запас ×4). reader_loop копит сырьё в DUMPST (кадры молчат).
    # Синхро-преамбула 5A A5 отсекает мусорный префикс от оборванного кадра → блок выровнен.
    out = bytearray(); off = 0
    while off < count:
        n = min(128, count - off); a = base + off
        with DUMP_LOCK:
            DUMPST["buf"] = bytearray(); DUMPST["need"] = n; DUMPST["want"] = n + 48; DUMPST["active"] = True
        _send_cmd(s, [0xC9, a >> 8, a & 0xFF, n])
        t0 = time.time()
        while time.time() - t0 < timeout:
            with DUMP_LOCK:
                if not DUMPST["active"]: break
            time.sleep(0.01)
        with DUMP_LOCK:
            timed_out = DUMPST["active"]
            DUMPST["active"] = False
            DUMPST["until"] = time.time() + 0.3   # короткая пауза: правка ячейки теперь ~0.2с,
            # секундная «занятость» замораживала бы индикатор указателей при правке подряд
            raw = bytes(DUMPST["buf"])
        if timed_out:
            # ЭБУ ещё досылает остаток ($F9 не досчитан) — гасим стрим (len=0), иначе
            # хвост утечёт в парсер кадров и в префикс следующего дампа
            _send_cmd(s, [0xC9, a >> 8, a & 0xFF, 0])
            time.sleep(0.3)
        # перебираем ВСЕ вхождения преамбулы: первое может оказаться в мусорном префиксе
        # от оборванного кадра телеметрии — берём то, после которого реально лежит n байт
        blk = None; j = raw.find(b"\x5A\xA5")
        while j >= 0:
            if len(raw) >= j + 2 + n: blk = raw[j + 2: j + 2 + n]; break
            j = raw.find(b"\x5A\xA5", j + 1)
        # хвост после блока — это уже возобновившийся кадр телеметрии; вернём его парсеру,
        # иначе кадр рвётся и счётчик ошибок растёт на каждой операции
        if blk is not None and j >= 0:
            tail = raw[j + 2 + n:]
            if tail: DUMPST["tail"] = bytes(tail)
        if blk is None:
            return None                        # синхро не найдено / недобор → ошибка чтения
        out += blk; off += n
    return list(out)


BLK_MAX = 32          # размер блока (равен буферу в прошивке STAGE)
BLKC = {"ok": None, "bad": None}   # кэш счётчиков блоков ЭБУ (сбрасывается при переподключении)
RESTART_SEEN = {"flag": False}     # ЭБУ перезапустился посреди обмена (счётчики блоков обнулились)
# ВЕСЬ обмен с ЭБУ — под одним замком. Сервер многопоточный (ThreadingHTTPServer): без него
# правка ячейки во время «привести к бин» шла бы вторым потоком — байты команд в порт
# вперемешку, и оба потока делили бы один DUMPST, читая ответы друг друга.
# /api/status замок НЕ берёт: HUD продолжает обновляться во время долгих операций.
SER_LOCK = threading.RLock()
ST_OK, ST_BAD = 0x17F5, 0x17F6   # счётчики принятых/отвергнутых блоков в ЭБУ


def _blk_status(s):
    # прочитать счётчики блоков (2 байта) — быстрый дамп, ~50мс
    r = _dump_read(s, ST_OK, 2, timeout=3.0)
    return (r[0], r[1]) if r else (None, None)


def _send_block(s, addr, data):
    # [CA][hi][lo][len][данные][chk=XOR данных]. ЭБУ применит блок ТОЛЬКО если сумма сошлась:
    # потерялся байт → блок отброшен целиком, в живые карты не попадает НИЧЕГО.
    chk = 0
    for b in data: chk ^= (b & 0xFF)
    # базовый счётчик берём из кэша — читать его перед КАЖДЫМ блоком это лишние ~100мс,
    # а значение мы и так узнаём из подтверждения предыдущего блока
    ok0, bad0 = BLKC.get("ok"), BLKC.get("bad")
    if ok0 is None:
        ok0, bad0 = _blk_status(s)
        if ok0 is None: return False, "нет связи с ЭБУ"
    _send_cmd(s, [0xCA, addr >> 8, addr & 0xFF, len(data)] + [b & 0xFF for b in data] + [chk])
    want_ok = (ok0 + 1) & 0xFF               # принятый блок увеличивает счётчик РОВНО на 1
    for _ in range(3):                       # ждём, пока ЭБУ дожуёт блок и обновит счётчик
        ok1, bad1 = _blk_status(s)
        if ok1 is None: BLKC["ok"] = None; return False, "нет связи"
        BLKC["ok"], BLKC["bad"] = ok1, bad1
        if ok1 == want_ok:  return True, ""                    # принят
        if bad1 != bad0 and ok1 == ok0: return False, "сумма не сошлась"
        if ok1 != ok0:                                          # ни то ни другое: ЭБУ сбросился
            BLKC["ok"] = None                                   # (мои счётчики обнуляются при старте)
            RESTART_SEEN["flag"] = True
            return False, "счётчики разъехались — ЭБУ перезапустился"
    BLKC["ok"] = None
    return False, "ЭБУ не ответил на блок"


def _fill_shadow_blocks(s, base, arr):
    # залить 256 байт блоками по 64 с контролем суммы. Возвращает (ok, сколько блоков не прошло)
    arr = [b & 0xFF for b in arr]; bad = 0
    for off in range(0, len(arr), BLK_MAX):
        chunk = arr[off:off + BLK_MAX]
        for attempt in range(3):             # блок отвергнут — просто шлём заново
            ok, err = _send_block(s, base + off, chunk)
            if ok: break
        else:
            bad += 1
    return bad == 0, bad


def _bake_bin(maps, suffix="_лог_"):
    """Запечь показанные таблицы в копию выбранного бина. maps = {имя: массив 256 байт}.
    → (имя_файла, ошибка)."""
    if not SEL.get("bin"): return "", "бин не выбран"
    try:
        rom = bytearray(open(SEL["bin"], "rb").read())
        if len(rom) != 32768: return "", "бин не 32КБ"
        for which in BINOFF:
            arr = (maps or {}).get(which)
            if arr and len(arr) == 256:
                off = BINOFF[which]; rom[off:off + 256] = bytes(b & 0xFF for b in arr)
        recalc_checksum(rom)
        d = os.path.join(HERE, "логи"); os.makedirs(d, exist_ok=True)
        bn = os.path.splitext(os.path.basename(SEL["bin"]))[0]
        fn = os.path.join(d, bn + suffix + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bin")
        open(fn, "wb").write(rom)
        return os.path.basename(fn), ""
    except Exception as e:
        return "", str(e)


def live_map():
    """Какая карта сейчас живёт в тени по данным ЭБУ из кадра. → имя или '' ."""
    n = STATE["ram"].get(SEL_ADDR)
    for w, num in CBNUM.items():
        if n == num: return w
    return ""


def _is_online(which=None):
    # для ПОКАЗА в панели: ЭБУ сам сообщает в кадре, что лежит в тени и куда смотрит указатель.
    # Онлайн = нужная карта выбрана И её указатель подтверждён как «смотрит в тень».
    if STATE["ram"].get(VERD_ADDR) != 1: return False
    lm = live_map()
    return bool(lm) and (which is None or lm == which)


def _read_sel(s):
    # АВТОРИТЕТНОЕ состояние — спрашиваем сам ЭБУ (дамп 2 байт, ~50мс), а не гадаем по
    # образу ОЗУ, который может быть пустым или устаревшим. → (номер карты, вердикт) или (None, None)
    r = _dump_read(s, SEL_ADDR, 2, timeout=3.0)
    return (r[0], r[1]) if r and len(r) >= 2 else (None, None)


def _select_map(s, which):
    """Отдать тень карте `which` (или None — отцепить всё) и УБЕДИТЬСЯ, что ЭБУ подчинился.
    Байт команды мог потеряться, а мы бы отрапортовали успех."""
    want = CBNUM.get(which, 0) if which else 0
    for _ in range(3):
        _send_cmd(s, [0xCB, want])
        time.sleep(0.15)
        sel, verd = _read_sel(s)
        if sel == want and verd != 0xFF:
            return True
    return False


def _fill_shadow(s, which, arr):
    # МАССОВАЯ заливка карты в тень. Три защиты:
    #  1) блоки с контрольной суммой — битый блок отвергается ЭБУ целиком (мусор в карты не попадает)
    #  2) на время заливки тень ОТЦЕПЛЯЕТСЯ (CB 0): пока летят восемь блоков, в тени лежит
    #     смесь старой карты и новой, и смотреть туда мотору нельзя. Отцепили — мотор эти
    #     секунды едет стоково и промежуточных состояний не видит вообще.
    #  3) состояние спрашивается у ЭБУ, а не помнится панелью.
    base = SHADOW.get(which)
    if base is None:
        return False, 256, "неизвестная карта: %s" % which
    RESTART_SEEN["flag"] = False          # признак «ЭБУ перезапустился» — только про ЭТУ заливку
    sel, _verd = _read_sel(s)
    if sel is None:
        return False, 256, "не читается состояние тени — заливка отменена"
    if not _select_map(s, None):
        return False, 256, "не удалось отцепить тень — заливка отменена"
    # ok/nbad объявлены ДО try: на них смотрит finally, а внутри try может выстрелить исключение
    # (обрыв порта) — тогда finally упал бы на NameError и спрятал настоящую причину.
    ok, nbad, restarted = False, 256, False
    try:
        ok, nbad = _fill_shadow_blocks(s, base, arr)
        restarted = RESTART_SEEN.get("flag", False)
    finally:
        if ok and not restarted:
            _select_map(s, which)         # залилось целиком → отдаём тень этой карте
        # кадр идёт 433мс: тот, что был снят при отцепленной тени, доедет уже после подключения.
        # Держим «занято» дольше кадра, иначе панель примет его за сброс блока.
        DUMPST["until"] = time.time() + 0.9
    if restarted:
        # ЭБУ перезапустился посреди заливки: my_init увёл обе карты на ПЗУ — это безопасно.
        # НЕ подключаем полузалитую тень молча, решение за пользователем.
        return False, 256, "ЭБУ перезапустился во время заливки — карты оставлены на ПЗУ (сток)"
    if not ok:
        # тень осталась ОТЦЕПЛЕННОЙ — это и есть правильный исход неудачи: мотор на стоке.
        return False, nbad, "часть блоков не подтвердилась — тень отцеплена, мотор на ПЗУ"
    return True, 0, ""


def do_start(port, baud):
    import serial
    # SER_LOCK: смена порта посреди обмена подменила бы CTRL["ser"] под работающей
    # транзакцией. Порядок захвата тот же, что в do_stop (SER→CTRL) — цикла нет.
    with SER_LOCK, CTRL_LOCK:
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
        BLKC["ok"] = BLKC["bad"] = None       # новое подключение → счётчики блоков перечитать
        # Образ ОЗУ и обученный ноль дросселя — от ПРЕДЫДУЩЕГО блока/прошивки. Раньше не
        # чистились: после переподключения HUD показывал старые значения как живые, а ноль
        # газа оставался тем, что поймали в прошлой сессии (в т.ч. при нажатой педали).
        with LOCK:
            STATE["ram"].clear(); STATE["tps_min"] = None; STATE["last_frame_t"] = 0
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
        _learn_writer_start()     # поток, который применяет набранные поправки в блок
        return True, ""


def _learn_writer_start():
    """Отдельный поток записи. В приёмном потоке писать нельзя: блочная запись ждёт
    подтверждения счётчиками, а это чтение кадров — сам себя и заблокирует."""
    if LWRITE.get("thread") and LWRITE["thread"].is_alive(): return
    ev = threading.Event()

    def loop():
        while not ev.is_set():
            time.sleep(0.25)
            if not LEARN["on"]: continue
            s = CTRL.get("ser")
            if not s: continue
            # не лезем в порт, пока идёт дамп/заливка, и не чаще ~4 раз в секунду
            if DUMPST["active"] or time.time() < DUMPST.get("until", 0): continue
            try:
                with SER_LOCK:
                    # писать только если ЭБУ подтверждает, что нужная карта живая
                    if STATE["ram"].get(VERD_ADDR) != 1: continue
                    if STATE["ram"].get(SEL_ADDR) != CBNUM.get(LEARN["which"]): continue
                    learn_apply(s)
            except Exception as e:
                LEARN["note"] = "запись: %s" % e
    th = threading.Thread(target=loop, daemon=True)
    LWRITE["thread"] = th; LWRITE["stop"] = ev
    th.start()


LWRITE = {"thread": None, "stop": None}


def do_stop():
    # SER_LOCK: не закрываем порт, пока идёт обмен с ЭБУ (заливка/дамп) — иначе поток
    # транзакции падает на закрытом порту. Отключение подождёт окончания операции.
    with SER_LOCK, CTRL_LOCK:
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
        wfresh = (now - WBL["last_t"]) < 2.0 if WBL["last_t"] else False
        wbl = {"running": WBL["running"], "port": WBL["port"], "total": WBL["total"],
               "raw": WBL["raw"], "hex": WBL["hex"], "error": WBL["error"], "fresh": wfresh,
               # ПРОТУХШИЙ AFR НЕ ОТДАЁМ. Раньше WBL["afr"] держал последнее значение вечно
               # (при отключении не сбрасывался), и оно шло в лог и в поправку VE как текущее —
               # карта правилась по цифре, которой уже нет.
               "afr": WBL["afr"] if wfresh else None,
               "afr_last": WBL["afr"], "stale": (WBL["afr"] is not None and not wfresh)}
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
    # ТОЧНАЯ загрузка форсунок: РЕАЛЬНЫЙ впрыск $004D (в UPP) × 0.010мс × об / 1200.
    # ЦЕНА ТИКА = 10 мкс (исправлено 04.08.26, было 5). Делитель 1200 — потому что
    # впрыск ПОСЛЕДОВАТЕЛЬНЫЙ: каждая форсунка открывается раз за цикл (720°).
    # Обоснование — j30/база знаний/Впрыск J30 — последовательный, цена тика 10 мкс 04.08.26 ИИ.txt
    inj_raw = w(0x004D)
    inj_ms = inj_raw * 0.010 if inj_raw is not None else None
    # «Впрыск расчёт» ($1411) убран из кадра — слоты ушли под сверку тени. Величина избыточна:
    # $004D = (2×$1411 − $142C) × 1.25, значит $1411 = ($004D/1.25 + $142C)/2. Оба входа в кадре.
    dead = ram.get(0x142C)
    top["inj_calc"] = (round((inj_raw / 1.25 + dead) / 2.0 * 0.010, 2)
                       if (inj_raw is not None and dead is not None) else None)
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
        # raw = СЫРЫЕ байты бина. cells — уже физика (AFR/градусы), её нельзя писать в ОЗУ:
        # «свести к бину» отправляло бы в блок число 14.7 как байт 14.
        fuel_out = {"cells": fuel_cells, "raw": [b & 0xFF for b in t["fuel"]],
                    "rows": [b * 50 for b in t["fuel_rax"]],           # обороты
                    "cols": [round(b * 0.125, 2) for b in t["fuel_cax"]],  # нагрузка TP
                    "hr": -1, "hc": -1}
        ign_cells = [deg_of(v) for v in t["ign"]]
        ign_out = {"cells": ign_cells, "raw": [b & 0xFF for b in t["ign"]],
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
            ve_out = {"cells": ve_cells, "raw": [b & 0xFF for b in t["ve"]],
                      "rows": [bb * 50 for bb in t["ve_rax"]],   # обороты
                      "cols": list(t["ve_pax"]),                 # давление, кПа
                      "hr": -1, "hc": -1}
            # ДАВЛЕНИЕ: с v19 его считает и кладёт в $00F7 сама рутина ДАД — берём готовое.
            # Пересчёт из сырья оставлен запасным путём для старых бинов, где $00F7 в кадре нет.
            press = ram.get(0x00F7)
            maf_raw = ram.get(0x1408)
            if press is None and maf_raw is not None:
                praw = (maf_raw >> 2) - t["dad_ofs"]
                if praw < 0: praw = 0
                press = (praw * t["dad_slope"]) >> 8             # давление, кПа
            if press is not None:
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
            ktps_out = {"cells": k_cells, "raw": [b & 0xFF for b in t["ktps"]],
                        "rows": [bb * 50 for bb in t["ktps_rax"]],              # обороты
                        "cols": [round(a * 100 / 172) for a in t["ktps_tax"]],   # % газа (из $14A2)
                        "hr": -1, "hc": -1}
            a2 = ram.get(0x14A2)
            if rpm_raw is not None and a2 is not None:
                ktps_out["hr"] = nearest_idx(rpm_raw / 4.0, t["ktps_rax"])
                ktps_out["hc"] = nearest_idx(a2, t["ktps_tax"])
    # --- ОБРАТНАЯ СВЯЗЬ: что лежит в тени и куда смотрит указатель (говорит сам ЭБУ) ---
    sel_n = ram.get(SEL_ADDR); verd = ram.get(VERD_ADDR)
    lm = live_map()
    # во время дампа/заливки кадры не идут — это НОРМА, а не потеря связи. Гасим ложную тревогу.
    d["busy"] = bool(DUMPST["active"] or time.time() < DUMPST.get("until", 0))
    # Тень ОДНА на 256 байт: живой может быть ровно одна карта, остальные читают ПЗУ.
    d["ptr"] = {
        "live": lm,                                   # какая карта сейчас живая ('' = никакая)
        "verdict": verd,                              # 0 ПЗУ, 1 тень, 255 авария
        "alarm": (verd == 0xFF),                      # указатель ни туда ни сюда — снимать онлайн
        "raw": [sel_n, verd],
        "online": bool(lm) and verd == 1,
        "known": (sel_n is not None and verd is not None),
        "csum": [ram.get(CSX_ADDR), ram.get(CSS_ADDR)],   # XOR и сумма содержимого тени
    }
    for w in CBNUM:                                   # совместимость с фронтом: состояние по карте
        d["ptr"][w] = ("shadow" if (lm == w and verd == 1) else "rom") if sel_n is not None else None
    # --- ОБУЧЕНИЕ: кормим движок этим кадром (все величины уже разобраны) ---
    try:
        learn_feed(time.time(), ram, top, t or {}, top.get("afr_fact"))
    except Exception as e:
        LEARN["note"] = "сбой обучения: %s" % e
    d["learn"] = {
        "on": LEARN["on"], "which": LEARN["which"], "applied": LEARN["applied"],
        "par": dict(LPAR), "note": LEARN["note"],
        "cov": {str(i): a[2] for i, a in LEARN["acc"].items()},
        "hits": {str(i): v for i, v in LEARN["hits"].items()},
        "rejects": dict(LEARN["rejects"]),
        "last": LEARN["last"] if (LEARN["last"] and time.time() - LEARN["last"]["t"] < 2.0) else None,
        "can_rollback": LEARN["base"] is not None,
    }
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
 /* --- светлая тема для добавленного: панель массовой правки, выделение, СТОП, плашки --- */
 body.light #bulk{background:#dde8f2;border-top:2px solid #8ab;color:#112}
 body.light #bulk input{background:#fff;color:#012;border:1px solid #7f8a99}
 body.light #bulk button{background:#ccd4dd;color:#123;border:1px solid #8895a5}
 body.light #bulk .clr{background:#e0cfae;color:#3a2a08;border:1px solid #b89a63}
 body.light #bulk #bulkstat{color:#456}
 body.light td.ec.sel input{background:#bcd8f5;outline:1px solid #2a6fb0;color:#012}
 body.light .estop{background:#b32020;color:#fff;border:1px solid #8a1414}
 body.light .estop:hover{background:#8a1414}
 body.light .stalebar{color:#7a5200;border:1px solid #b8860b;background:#fdf3d6}
 body.light .divbar{color:#8a1414;border:1px solid #c0392b;background:#fbe0dd}
 body.light .srcmark{color:#8a6100}
 body.light .learninfo{color:#455}
 body.light .learninfo b{color:#0a4a6b}
 body.light #learnpar label{color:#556}
 body.light td.lrn{outline-color:#b8860b}
 body.light .ptr.none{color:#556;border-color:#9aa6b3}
 body.light .ptr.on{color:#0a6b2a;border-color:#0a6b2a;background:#e2f6e8}
 body.light .ptr.off{color:#8a6100;border-color:#b8860b;background:#fdf3d6}
 body.light .ptr.warn{color:#8a1414;border-color:#c0392b;background:#fbe0dd}
 body.light table.map th{background:#d6dee7;color:#123}
 body.light table.map th.corner{color:#567}
 body.light table.map td.hl{outline:2px solid #0a7a2a;background:#c6f0ce;color:#031;font-weight:700}
 body.light table.map td.flag{color:#8a5a10}
 .estop{background:#8b1a1a;color:#fff;border:1px solid #c0392b;border-radius:6px;padding:6px 12px;
        font-weight:700;font-size:13px;cursor:pointer;letter-spacing:.5px}
 .estop:hover{background:#c0392b}
 .estop:active{transform:translateY(1px)}
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
 td.ec.sel input{background:#2b4a6b;outline:1px solid #6cf}
 body.nosel{user-select:none}
 #bulk{display:none;position:fixed;bottom:0;left:0;right:0;background:#17222e;border-top:2px solid #38506a;
       padding:9px 16px;gap:10px;align-items:center;z-index:40;font-size:13px;flex-wrap:wrap}
 #bulk input{background:#0e1620;color:#dfe;border:1px solid #38506a;padding:6px 9px;width:120px;font:13px monospace}
 #bulk button{padding:6px 12px;cursor:pointer}
 #bulk .clr{background:#653;color:#fff;border:1px solid #865}
 .ptr{font-size:12px;padding:4px 10px;border-radius:12px;border:1px solid;white-space:nowrap}
 /* данные устарели: значения остаются видны, но спутать с живыми невозможно */
 #vars.stale .val{opacity:.35;text-decoration:line-through}
 .stalebar{display:none;padding:6px 12px;margin-bottom:8px;border-radius:6px;font-size:13px;
           color:#e0b000;border:1px solid #b8860b;background:rgba(184,134,11,.12)}
 .divbar{display:none;padding:6px 12px;margin-bottom:8px;border-radius:6px;font-size:13px;
         color:#e74c3c;border:1px solid #e74c3c;background:rgba(231,76,60,.12)}
 .ptr.none{color:#7b8794;border-color:#3a4350}
 .ptr.on{color:#2ecc71;border-color:#2ecc71;background:rgba(46,204,113,.10)}
 .ptr.off{color:#c9a227;border-color:#c9a227;background:rgba(201,162,39,.10)}
 .ptr.warn{color:#e74c3c;border-color:#e74c3c;background:rgba(231,76,60,.12)}
 .tobin{font-size:12px;margin-left:8px}
 .srcmark{font-size:11px;font-weight:400;color:#c9a227}
 .lp{width:64px;margin-left:4px}
 #learnpar label{font-size:12px;color:#8aa;margin-right:10px;white-space:nowrap}
 .learninfo{font-size:12px;color:#8aa;padding:4px 12px;line-height:1.6}
 .learninfo b{color:#7fd}
 td.lrn{outline:2px solid #e0b000;outline-offset:-2px}
 td.lrnfull{background:rgba(46,204,113,.18)}
 body.light td.lrnfull{background:#dff5e6}
 .rightcol .mapbox{margin-bottom:26px}
 .rightcol .mapbox h2{margin:0 0 10px}
 .ec{padding:0}
 .ec input{width:100%;box-sizing:border-box;border:none;background:transparent;text-align:center;font:inherit;color:inherit;padding:3px 0}
 .ec.ok{background:#123d1a}.ec.err{background:#4d1414}.ec.pend{background:#4d4413}
 body.light .ec.ok{background:#c8f0d0}body.light .ec.err{background:#f5c6c6}body.light .ec.pend{background:#f5ecc0}
 body.light #ctrlbar{background:#fff}body.light .logtab th{background:#eef2f6}body.light .logtab tr.sticky{background:#eaf3ff}
</style></head><body class=light>
<div id=ctrlbar>
 <div class=cgrp><span class=clbl>Файл</span><select id=binsel onchange=selbin()></select><span class="stat none" id=binicon>&#9679;</span>
   <button id=btnEstop class=estop onclick=eStop() title="Сохранить лог и бин, отключить ЭБУ и ШДК, заблокировать страницу">&#9632; СТОП</button></div>
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
  <div id=stalewarn class=stalebar>&#9888; НЕТ СВЕЖИХ ДАННЫХ — показано последнее, что пришло. Живыми не считать.</div>
  <div id=divwarn class=divbar>&#9888; ПОКАЗ ПАНЕЛИ МОЖЕТ НЕ СОВПАДАТЬ С БЛОКОМ — сохранение бина заблокировано.</div>
  <div id=csumwarn class=divbar><span id=csumstat></span></div>
  <div class=onlinebar>
   <select id=mapsel title="какую карту сделать живой — тень одна, живёт ровно одна карта">
    <option value=fuel>карта: смесь</option>
    <option value=ign>карта: угол</option>
    <option value=ve>карта: VE (ДАД)</option>
    <option value=ktps>карта: Ktps (ДАД)</option>
   </select>
   <button class=start id=btnOnline onclick=goOnline()>&#128246; ОНЛАЙН</button>
   <span id=ptrstat class="ptr none">ЭБУ: связи нет</span>
   <button class=ghost id=btnOffline onclick=goOffline() style="display:none">&#9209; ВЫКЛЮЧИТЬ ОНЛАЙН</button>
   <button class=ghost id=btnLoadRom onclick=readFromRom() style="display:none">&#128229; СЧИТАТЬ ИЗ ПЗУ</button>
   <button class=ghost id=btnSaveBin onclick=saveBin() style="display:none">&#128190; СОХРАНИТЬ БИН</button>
   <span id=onstat class=st style="font-size:13px;color:#8aa"></span>
  </div>
  <div class=onlinebar id=learnbar>
   <button class=start id=btnLearn onclick=learnToggle()>&#127919; ОБУЧЕНИЕ</button>
   <span id=learnstat class="ptr none">обучение выключено</span>
   <button class=ghost onclick="learnPreset('fast')">быстро</button>
   <button class=ghost onclick="learnPreset('fine')">точно</button>
   <button class=estop id=btnLearnBack onclick=learnRollback() style="display:none">&#8630; ВЕРНУТЬ КАК БЫЛО</button>
  </div>
  <div class=onlinebar id=learnpar>
   <label>замеров на ячейку <input id=p_min_hits class=lp value=3></label>
   <label>доля поправки <input id=p_damp class=lp value=0.7></label>
   <label>шаг макс, доля <input id=p_max_step class=lp value=0.2></label>
   <label>не учить ниже газа, % <input id=p_tps_min class=lp value=0></label>
   <label>задержка выхлопа, мс <input id=p_delay_ms class=lp value=350></label>
   <label>холодно выше (сырьё ТОЖ) <input id=p_t_cold class=lp value=65></label>
   <label>стац. обороты <input id=p_d_rpm class=lp value=150></label>
   <label>стац. газ % <input id=p_d_tps class=lp value=3></label>
   <button class=ghost onclick=learnSendPar()>применить пороги</button>
  </div>
  <div class=onlinebar id=learnlogbar>
   <span style="font-size:12px;color:#8aa">по логу:</span>
   <select id=loglist style="max-width:340px"></select>
   <select id=logwhich><option value=ve>VE</option><option value=ktps>Ktps</option></select>
   <button class=ghost onclick=learnFromLog()>прогнать</button>
   <button class=start id=btnLogPush onclick=learnPushLog() style="display:none">&#8681; залить результат в блок</button>
  </div>
  <div id=learninfo class=learninfo></div>
  <div class=mapbox><h2>&#9819; Смесь (AFR) <button class=tobin id=tobin_fuel onclick="applyBin('fuel')" style="display:none">привести к бин</button> <span id=src_fuel class=srcmark></span></h2><div id=fuelmap>—</div></div>
  <div class=mapbox><h2>&#9889; Угол (УОЗ, град) <button class=tobin id=tobin_ign onclick="applyBin('ign')" style="display:none">привести к бин</button> <span id=src_ign class=srcmark></span></h2><div id=ignmap>—</div></div>
  <div class=mapbox id=box_ve style="display:none"><h2>&#128168; VE — наполнение (ДАД) <button class=tobin id=tobin_ve onclick="applyBin('ve')" style="display:none">привести к бин</button> <span id=src_ve class=srcmark></span></h2><div id=vemap>—</div></div>
  <div class=mapbox id=box_ktps style="display:none"><h2>&#127968; Ktps — поправка по дросселю (ДАД) <button class=tobin id=tobin_ktps onclick="applyBin('ktps')" style="display:none">привести к бин</button> <span id=src_ktps class=srcmark></span></h2><div id=ktpsmap>—</div></div>
 </div>
</div>
</div>
<div id=bulk>
 <span>Выделено <b id=bulkn>0</b> яч.:</span>
 <input id=bulkv placeholder="значение AFR">
 <button id=bulkset>Применить ко всем</button>
 <button id=bulkmul>× умножить</button>
 <button id=bulkadd>+ прибавить</button>
 <button id=bulkbin class=clr>Свести к бину</button>
 <button id=bulkclr class=clr>Снять выделение</button>
 <span id=bulkstat style="color:#8aa"></span>
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
let mapBin=null,hlIds={fuel:null,ign:null,ve:null,ktps:null};
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
let online=false,editRendered=false;const ONLINE={fuel:null,ign:null,ve:null,ktps:null},AX={};
// защита от потери прогресса: состояние онлайна в память браузера
function saveProg(){try{localStorage.setItem('j30online',JSON.stringify({on:online,live:liveMap,maps:ONLINE}));}catch(_){}}
function loadProg(){try{const s=JSON.parse(localStorage.getItem('j30online')||'null');
 // Какая карта живая — решает ЭБУ (syncPtr перепишет liveMap из кадра). Из памяти браузера
 // берём только сами таблицы, чтобы не потерять несохранённые правки.
 const M=s&&(s.maps||{fuel:s.fuel,ign:s.ign});
 if(s&&s.on&&M&&Object.keys(M).some(k=>M[k])){online=true;for(const k in ONLINE)ONLINE[k]=M[k]||null;liveMap=s.live||'';editRendered=false;
  const b=document.getElementById('btnOnline');if(b)b.classList.add('on');
  const sel=document.getElementById('mapsel');if(sel&&liveMap)sel.value=liveMap;
  document.getElementById('btnSaveBin').style.display='';document.getElementById('btnLoadRom').style.display='';
  document.getElementById('btnOffline').style.display='';
  const tb=document.getElementById('tobin_'+(liveMap||'fuel'));if(tb)tb.style.display='';
  document.getElementById('onstat').textContent='ОНЛАЙН восстановлен из памяти браузера — прогресс не потерян';}}catch(_){}}
// Показ НЕЖИВОЙ карты. Если в панели есть её правки — рисуем их, а не бин: иначе на экране
// были бы одни числа, а в бин при сохранении ушли бы другие (ONLINE, а не то, что видно).
// Помечаем такую карту явно, чтобы не путать с тем, что реально читает мотор.
function physCells(w,arr){
 if(w==='fuel')return arr.map(afrOf);
 if(w==='ign') return arr.map(b=>(b<90?b:null));
 return arr.map(b=>Math.round(b/128*1000)/1000);   // VE и Ktps: 128 = 1.0
}
function mapView(w,dw){
 const mk=document.getElementById('src_'+w);
 const mine=ONLINE[w]&&ONLINE[w].length===256&&!(online&&liveMap===w);
 if(mk)mk.textContent=mine?'правки панели, в блок НЕ залиты':'';
 if(!mine||!dw)return dw;
 const o={}; for(const k in dw)o[k]=dw[k];
 o.cells=physCells(w,ONLINE[w]);
 return o;
}
// байт↔физика (как в редакторе). Смесь: 2 кластера AFR; угол: байт=градусы
function afrOf(x){return (x>=128)?Math.round(188160/(x-64))/100:Math.round(188160/(x+128))/100;}
function afrToByte(afr,cur){  // остаёмся в кластере текущего байта, чтоб не прыгать кодировку
 let b=(cur>=128)?Math.round(1881.6/afr+64):Math.round(1881.6/afr-128);
 return Math.max(0,Math.min(255,b));}
// байт → физика по карте: смесь = AFR, угол = градусы, VE и Ktps = коэффициент (128 = 1.0)
const MAPBOX={fuel:'fuelmap',ign:'ignmap',ve:'vemap',ktps:'ktpsmap'};
function physOf(which,b){
 if(which==='fuel')return afrOf(b);
 if(which==='ign') return b;
 return Math.round(b/128*1000)/1000;}
// физика → байт (обратно)
function byteOf(which,v,cur){
 if(which==='fuel')return afrToByte(v,cur);
 if(which==='ign') return Math.max(0,Math.min(255,Math.round(v)));
 return Math.max(0,Math.min(255,Math.round(v*128)));}
function renderEdit(which){
 const arr=ONLINE[which],ax=AX[which];if(!arr||!ax)return;
 let h='<table class=map><tr><th class=corner>об\\нагр</th>';
 for(const c of ax.cols)h+='<th>'+c+'</th>';h+='</tr>';
 for(let r=0;r<16;r++){h+='<tr><th>'+ax.rows[r]+'</th>';
  for(let c=0;c<16;c++){const idx=r*16+c,b=arr[idx];
   h+='<td id='+which+'_'+r+'_'+c+' class=ec title="байт '+b+'"><input value="'+physOf(which,b)+'" onchange="cellEdit(\''+which+'\','+idx+',this)"></td>';}
  h+='</tr>';}
 document.getElementById(MAPBOX[which]).innerHTML=h+'</table>';}
async function cellEdit(which,idx,el){
 let val=parseFloat(el.value);
 // тень одна: писать можно только в ЖИВУЮ карту, иначе байты ушли бы в чужую таблицу
 if(which!==liveMap){el.value=physOf(which,ONLINE[which][idx]);
  document.getElementById('onstat').textContent='живая сейчас карта «'+(MAPNAME[liveMap]||'—')+'». Переключи карту в селекторе и нажми ОНЛАЙН.';return;}
 if(isNaN(val)){el.value=physOf(which,ONLINE[which][idx]);return;}
 let byte=byteOf(which,val,ONLINE[which][idx]);
 const td=el.parentNode;td.classList.remove('ok','err');td.classList.add('pend');
 const r=await fetch('/api/pokecell',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:which,idx:idx,val:byte})});
 const d=await r.json();td.classList.remove('pend');
 if(d.ok&&d.applied){ONLINE[which][idx]=byte;saveProg();td.classList.add('ok');td.title='байт '+byte;el.value=physOf(which,byte);}
 else{td.classList.add('err');td.title='НЕ применилось: '+(d.error||'ЭБУ не подтвердил блок');}}
const MAPNAME={fuel:'смесь',ign:'угол',ve:'VE',ktps:'Ktps'};
// ================= ОБУЧЕНИЕ =================
const LP=['min_hits','damp','max_step','tps_min','delay_ms','t_cold','d_rpm','d_tps'];
let learnOn=false,lrnCells=[];
function learnSendPar(){
 const o={};LP.forEach(k=>{const e=document.getElementById('p_'+k);if(e)o[k]=e.value.replace(',','.');});
 return fetch('/api/learn/par',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)});}
function learnPreset(kind){
 // «быстро» — прикинуть смесь за одну поездку. «точно» — доводка, шум не пролезает.
 const v=kind==='fast'?{min_hits:1,damp:1.0,max_step:0.25,d_rpm:250,d_tps:6,delay_ms:350}
                      :{min_hits:5,damp:0.5,max_step:0.15,d_rpm:100,d_tps:2,delay_ms:350};
 for(const k in v){const e=document.getElementById('p_'+k);if(e)e.value=v[k];}
 learnSendPar();}
async function learnToggle(){
 const st=document.getElementById('learnstat');
 if(learnOn){await fetch('/api/learn/stop',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
  learnOn=false;document.getElementById('btnLearn').classList.remove('on');return;}
 if(!liveMap||!ONLINE[liveMap]){st.textContent='сначала включи ОНЛАЙН на карте VE или Ktps';return;}
 await learnSendPar();
 const r=await fetch('/api/learn/start',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({cells:ONLINE[liveMap]})});
 const d=await r.json();
 if(!d.ok){st.textContent='не запустилось: '+(d.error||'');return;}
 learnOn=true;document.getElementById('btnLearn').classList.add('on');
 document.getElementById('btnLearnBack').style.display='';}
async function learnRollback(){
 if(!confirm('Вернуть карту к состоянию до начала обучения?'))return;
 const r=await fetch('/api/learn/rollback',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
 const d=await r.json();
 learnOn=false;document.getElementById('btnLearn').classList.remove('on');
 if(d.ok&&d.cells){ONLINE[liveMap]=d.cells;renderEdit(liveMap);saveProg();
   document.getElementById('learnstat').textContent='карта возвращена как была';}
 else document.getElementById('learnstat').textContent='откат не прошёл: '+(d.error||'');}
// ---- обучение ПО ЛОГУ: тот же движок, данные из CSV. В блок ничего не пишет сам ----
let LOGRES=null;
async function learnLogs(){
 const r=await fetch('/api/learn/logs',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
 const d=await r.json();const s=document.getElementById('loglist');if(!s||!d.ok)return;
 s.innerHTML=d.files.map(f=>'<option>'+f+'</option>').join('');}
async function learnFromLog(){
 const inf=document.getElementById('learninfo');
 const f=document.getElementById('loglist').value,w=document.getElementById('logwhich').value;
 if(!f){inf.textContent='лог не выбран';return;}
 inf.textContent='считаю по логу...';
 await learnSendPar();
 const r=await fetch('/api/learn/fromlog',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({file:f,which:w})});
 const d=await r.json();
 if(!d.ok){inf.textContent='не посчиталось: '+(d.error||'');return;}
 LOGRES=d;
 // показываем предложенную карту сразу в таблице — это ещё НЕ в блоке
 ONLINE[w]=d.cells;liveMapShow(w);
 const cov=Object.keys(d.cov||{}).length;
 const rj=d.rejects||{};const top=Object.keys(rj).sort((a,b)=>rj[b]-rj[a]).slice(0,4);
 inf.innerHTML='<b>по логу:</b> набрано ячеек '+cov+', изменилось '+d.changed+
   '. <b>отказы:</b> '+(top.map(k=>k+' ('+rj[k]+')').join(', ')||'нет')+
   '. <b style="color:#c9a227">Показана предложенная карта — в блок она ещё НЕ залита.</b>';
 document.getElementById('btnLogPush').style.display='';}
function liveMapShow(w){const mk=document.getElementById('src_'+w);
 if(mk)mk.textContent='расчёт по логу, в блок НЕ залито';
 if(AX[w])renderEdit(w);}
async function learnPushLog(){
 if(!LOGRES)return;
 const inf=document.getElementById('learninfo');
 if(!confirm('Залить рассчитанную карту «'+LOGRES.which+'» в блок?'))return;
 inf.textContent='заливаю...';
 const r=await fetch('/api/learn/push',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({which:LOGRES.which,cells:LOGRES.cells})});
 const d=await r.json();
 inf.innerHTML=d.ok?'<b>залито в блок.</b>':'не залилось: '+(d.error||'');
 if(d.ok){const mk=document.getElementById('src_'+LOGRES.which);if(mk)mk.textContent='';}}
// показ: что катается прямо сейчас + покрытие
function learnShow(L){
 if(!L)return;
 const st=document.getElementById('learnstat'),inf=document.getElementById('learninfo');
 learnOn=!!L.on;
 const b=document.getElementById('btnLearn');if(b)b.classList.toggle('on',learnOn);
 if(!learnOn){st.className='ptr none';st.textContent='обучение выключено';}
 else{st.className='ptr on';st.textContent='УЧУ «'+(MAPNAME[L.which]||L.which)+'», записано ячеек: '+L.applied;}
 // подсветка ячеек, куда ложится поправка ПРЯМО СЕЙЧАС
 lrnCells.forEach(id=>{const e=document.getElementById(id);if(e)e.classList.remove('lrn');});
 lrnCells=[];
 if(L.on&&L.last&&L.which===liveMap){
  for(const [idx,w] of L.last.cells){
   const id=L.which+'_'+Math.floor(idx/16)+'_'+(idx%16);
   const e=document.getElementById(id);
   if(e){e.classList.add('lrn');e.title='доля поправки '+w;lrnCells.push(id);}
  }
 }
 // ячейки, которые уже применялись — зелёным фоном
 if(L.hits){for(const k in L.hits){const i=+k;
   const e=document.getElementById((L.which||'')+'_'+Math.floor(i/16)+'_'+(i%16));
   if(e)e.classList.add('lrnfull');}}
 // строка состояния: что мешает учиться
 let txt='';
 if(L.on){
  const last=L.last;
  txt+= last? ('<b>сейчас:</b> AFR факт '+last.afr+' / цель '+last.tgt+' → поправка ×'+last.k+' в '+last.cells.length+' яч. ')
             : '<b>сейчас:</b> замеры не идут. ';
  const covN=Object.keys(L.cov||{}).length, hitN=Object.keys(L.hits||{}).length;
  txt+='<b>копится в</b> '+covN+' яч, <b>применено в</b> '+hitN+' яч. ';
  const rj=L.rejects||{};const top=Object.keys(rj).sort((a,b)=>rj[b]-rj[a]).slice(0,3);
  if(top.length)txt+='<b>отказы:</b> '+top.map(k=>k+' ('+rj[k]+')').join(', ');
  if(L.note)txt+=' <b style="color:#e74c3c">'+L.note+'</b>';
 }
 inf.innerHTML=txt;}
function pickedMap(){const s=document.getElementById('mapsel');return (s&&s.value)||'fuel';}
async function goOnline(){
 const o=document.getElementById('onstat');
 const w=pickedMap();
 online=true;document.getElementById('btnOnline').classList.add('on');editRendered=true;
 // Тень ОДНА: сервер сам отцепляет её (CB 0), заливает выбранную карту и отдаёт тень ей (CB N).
 // Пока летят блоки, на тень никто не смотрит — мотор эти секунды едет стоково.
 o.textContent='подключаю карту «'+MAPNAME[w]+'»: заливаю из бина в тень...';
 const r=await fetch('/api/applybin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:w})});
 const d=await r.json();
 if(!d.ok){o.textContent='не подключилось ('+MAPNAME[w]+'): '+(d.error||'')+' Мотор на ПЗУ (сток), правки не действуют.';
      online=false;editRendered=false;
      document.getElementById('btnOnline').classList.remove('on');
      await resyncFromEcu(w);   // в блоке могла осесть часть блоков — привести показ к факту
      return;}
 // Предыдущая карта перестала быть живой — в ЭБУ она вернулась к ПЗУ. Но её правки в панели
 // НЕ стираем: пока не запечёшь бин, они существуют только здесь. Стереть = потерять работу.
 const prev=liveMap;
 ONLINE[w]=d.cells;liveMap=w;renderEdit(w);
 if(prev&&prev!==w&&ONLINE[prev]){
  o.textContent='карта «'+MAPNAME[prev]+'» больше не живая (в ЭБУ вернулась к ПЗУ). Её правки остались только в панели — сохрани бин, иначе потеряешь.';
 }
 document.getElementById('btnSaveBin').style.display='';document.getElementById('btnLoadRom').style.display='';
 document.getElementById('btnOffline').style.display='';
 for(const k in ONLINE){const e=document.getElementById('tobin_'+k);if(e)e.style.display=(k===w?'':'none');}
 setDiverged(false);   // карта залита блоками с подтверждением → показ совпадает с блоком
 saveProg();
 if(!(prev&&prev!==w&&ONLINE[prev]))
  o.textContent='ОНЛАЙН: живая карта «'+MAPNAME[w]+'». Правь ячейку → уходит сразу. Остальные карты читаются из ПЗУ.';}
async function readFromRom(){
 const o=document.getElementById('onstat');
 for(const w of [liveMap||pickedMap()]){
  o.textContent='читаю '+MAPNAME[w]+' из ПЗУ (дамп)...';
  const r=await fetch('/api/loadrom',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:w})});
  const d=await r.json();
  if(d.ok){ONLINE[w]=d.cells;renderEdit(w);saveProg();}
  else{o.textContent='ошибка чтения ПЗУ ('+w+'): '+(d.error||'')+(d.mismatch?(' — не сошлось '+d.mismatch):'');return;}
 }
 setDiverged(false);   // ПЗУ вычитано и залито в тень с подтверждением → показ совпадает
 o.textContent='считано из ПЗУ (сток) → залито в тень. Показано на компе, живое совпадает.';}
// ---- ВЫКЛЮЧЕНИЕ ОНЛАЙНА: карты обратно на ПЗУ, с подтверждением ----
async function goOffline(){
 const o=document.getElementById('onstat');
 o.textContent='отцепляю тень, возвращаю карты на ПЗУ...';
 const r=await fetch('/api/flip',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:null})});
 const d=await r.json();
 if(!d.ok){o.textContent='НЕ отцепилось: '+(d.error||'')+'. Мотор всё ещё читает тень.';return;}
 online=false;editRendered=false;mapBin=null;liveMap='';csumBad=0;clearSel();
 document.getElementById('btnOnline').classList.remove('on');
 for(const id of ['btnOffline','btnLoadRom','tobin_fuel','tobin_ign','tobin_ve','tobin_ktps']){const e=document.getElementById(id);if(e)e.style.display='none';}
 saveProg();
 o.textContent='ОФФЛАЙН: все карты читаются из ПЗУ (сток). Тень в ОЗУ цела — ОНЛАЙН вернёт её.';}

// ---- ВЫДЕЛЕНИЕ ПРОТЯЖКОЙ + МАССОВАЯ ПРАВКА (как на странице редактора) ----
let selCells=new Set(), dragAnchor=null, dragging=false;
function clearSel(){selCells.forEach(td=>td.classList.remove('sel'));selCells.clear();
 const b=document.getElementById('bulk'); if(b)b.style.display='none';}
function addSel(td){if(td&&!selCells.has(td)){td.classList.add('sel');selCells.add(td);}}
function showBulk(){const b=document.getElementById('bulk');
 if(selCells.size>1){document.getElementById('bulkn').textContent=selCells.size;b.style.display='flex';}
 else clearSel();}
document.addEventListener('mousedown',e=>{const td=e.target.closest('td.ec');if(!td)return;
 dragAnchor=td;dragging=false;clearSel();});
document.addEventListener('mouseover',e=>{const td=e.target.closest('td.ec');if(!td)return;
 if(e.buttons===1&&dragAnchor){if(!dragging){dragging=true;document.body.classList.add('nosel');
  const inp=dragAnchor.querySelector('input');if(inp)inp.blur();addSel(dragAnchor);}addSel(td);}});
document.addEventListener('mouseup',()=>{if(dragging)showBulk();
 dragging=false;dragAnchor=null;document.body.classList.remove('nosel');});

// применить операцию к выделенному и отправить ОДНИМ пакетом
async function bulkApply(fn){
 const st=document.getElementById('bulkstat'); st.textContent='считаю...';
 const w=liveMap;                       // правим только ЖИВУЮ карту — остальные читают ПЗУ
 if(!w||!ONLINE[w]){st.textContent='живой карты нет — включи ОНЛАЙН';return;}
 const cells=[]; const re=new RegExp('^'+w+'_(\\d+)_(\\d+)$');
 selCells.forEach(td=>{
  const m=td.id.match(re); if(!m)return;
  const idx=(+m[1])*16+(+m[2]);
  const cur=ONLINE[w][idx];
  const nb=fn(cur,idx);
  if(nb!==null&&nb!==cur)cells.push({idx:idx,val:nb});
 });
 if(!cells.length){st.textContent='нечего менять';return;}
 st.textContent='пишу '+cells.length+' яч...';
 const r=await fetch('/api/pokecells',{method:'POST',headers:{'Content-Type':'application/json'},
                                       body:JSON.stringify({which:w,cells:cells})});
 const d=await r.json();
 if(d.ok){cells.forEach(c=>ONLINE[w][c.idx]=c.val);saveProg();renderEdit(w);
          st.textContent='записано '+d.written+' яч ✓';}
 else{st.textContent='ОШИБКА: '+(d.error||'');await resyncFromEcu(w);}
 clearSel();
}
function bulkNum(){const v=parseFloat(document.getElementById('bulkv').value.replace(',','.'));return isNaN(v)?null:v;}
// Массовые операции считают в ФИЗИКЕ живой карты: смесь — через AFR, угол — прямо в градусах.
// Раньше всё шло через afrToByte безусловно; на карте угла это записало бы мусор.
function bulkToByte(v,cur){return byteOf(liveMap,v,cur);}
function bulkOfByte(b){return physOf(liveMap,b);}
function wireBulk(){
 const B=(id,fn)=>{const e=document.getElementById(id);if(e)e.onclick=fn;};
 B('bulkclr',clearSel);
 B('bulkset',()=>{const v=bulkNum();if(v===null)return;
   bulkApply(cur=>bulkToByte(v,cur));});
 B('bulkmul',()=>{const f=bulkNum();if(f===null)return;
   bulkApply(cur=>bulkToByte(bulkOfByte(cur)*f,cur));});
 B('bulkadd',()=>{const a=bulkNum();if(a===null)return;
   bulkApply(cur=>bulkToByte(bulkOfByte(cur)+a,cur));});
 B('bulkbin',()=>{const t=BINCELLS[liveMap]; if(!t){document.getElementById('bulkstat').textContent='бин не загружен';return;}
   bulkApply((cur,idx)=>t[idx]);});
}
let BINCELLS={fuel:null,ign:null,ve:null,ktps:null};   // карты из бина — для «свести к бину»
async function saveBin(){
 const r=await fetch('/api/savebin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ONLINE)});
 const d=await r.json();
 document.getElementById('onstat').textContent=d.ok?('сохранено: '+d.name):('ошибка: '+(d.error||''));}
async function applyBin(which){
 const o=document.getElementById('onstat');o.textContent='привожу '+which+' к бину...';
 const r=await fetch('/api/applybin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:which})});
 const d=await r.json();
 if(d.ok){ONLINE[which]=d.cells;setDiverged(false);saveProg();renderEdit(which);o.textContent=which+' приведён к бину ✓';}
 else{o.textContent='ошибка: '+d.error;await resyncFromEcu(which);}}
// ---- РАСХОЖДЕНИЕ ПАНЕЛИ И БЛОКА ----
// Заливка могла лечь наполовину: часть блоков в ЭБУ применилась, часть нет. Если оставить
// показ как был, «СОХРАНИТЬ БИН» запечёт вид ПАНЕЛИ — файл, которого в машине не было.
// Поэтому: перечитываем карту из блока. Не вышло — помечаем данные недостоверными
// и запрещаем сохранение до успешного перечитывания.
let diverged=false;
function setDiverged(v){
 diverged=v;
 const b=document.getElementById('btnSaveBin');
 if(b){b.disabled=v;b.title=v?'данные панели разошлись с блоком — сначала перечитай из блока':'';}
 const w=document.getElementById('divwarn');
 if(w)w.style.display=v?'':'none';
}
async function resyncFromEcu(which){
 const o=document.getElementById('onstat');
 o.textContent='заливка не прошла — перечитываю '+which+' из блока, чтобы показ совпал с фактом...';
 try{
  const r=await fetch('/api/readtable',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:which,src:'shadow'})});
  const d=await r.json();
  if(d.ok){ONLINE[which]=d.cells;renderEdit(which);saveProg();setDiverged(false);
           o.textContent='показ приведён к тому, что РЕАЛЬНО в блоке (заливка не прошла целиком)';return;}
 }catch(_){}
 setDiverged(true);
 o.textContent='НЕ удалось перечитать блок. Данные панели могут не совпадать с ЭБУ — сохранение бина заблокировано.';
}
// ---- ОБРАТНАЯ СВЯЗЬ: панель показывает то, что говорит ЭБУ ($F0/$F2 в кадре) ----
// Никакого автовозврата: если блок сбросился на ПЗУ — пишем правду и ждём твоего решения.
let ptrWas=null,liveMap='',csumBad=0;
// Сверка СОДЕРЖИМОГО тени: ЭБУ считает XOR и сумму по своим 256 байтам, панель — по тем,
// что показывает. Ловит случай «переключил карту, а долилось не всё»: номер карты при этом
// говорит правду, а в тени каша. Одиночное расхождение законно — правка ячейки успевает
// попасть в середину обхода, поэтому ругаемся только на трёх кадрах подряд.
function csumCheck(p){
 const el=document.getElementById('csumstat'),box=document.getElementById('csumwarn');
 if(!el||!box)return;
 const hide=()=>{el.textContent='';box.style.display='none';};
 const c=p.csum||[]; const arr=liveMap?ONLINE[liveMap]:null;
 if(!p.online||!arr||arr.length!==256||c[0]==null||c[1]==null){hide();csumBad=0;return;}
 let x=0,s=0; for(let i=0;i<256;i++){x^=arr[i]&255;s=(s+(arr[i]&255))&255;}
 if(x===c[0]&&s===c[1]){hide();csumBad=0;return;}
 if(++csumBad<3){return;}
 el.textContent='⚠ В БЛОКЕ НЕ ТО, ЧТО НА ЭКРАНЕ: содержимое тени не совпало. Правки уходят в никуда — нажми «привести к бин» для этой карты.';
 box.style.display='';
}
function syncPtr(p,conn){
 const lab=document.getElementById('ptrstat'); if(!lab)return;
 if(!conn||!p.known){lab.className='ptr none';lab.textContent='ЭБУ: связи нет';ptrWas=null;return;}
 const on=!!p.online; const NM={fuel:'СМЕСЬ',ign:'УГОЛ'};
 // тень ОДНА на 256 байт: живой может быть ровно одна карта, остальные читают ПЗУ
 if(p.alarm){lab.className='ptr warn';lab.textContent='ЭБУ: УКАЗАТЕЛЬ БИТЫЙ — снимаю онлайн';}
 else if(on){lab.className='ptr on';lab.textContent='ЭБУ: живая карта — '+(NM[p.live]||p.live)+' (правки действуют)';}
 else{lab.className='ptr off';lab.textContent='ЭБУ: все карты ИЗ ПЗУ (сток, правки НЕ действуют)';}
 liveMap=p.live||'';
 if(p.alarm&&online){   // вердикт FF: указатель ни туда ни сюда. Не рассуждаем — снимаем онлайн.
  online=false;editRendered=false;saveProg();
  document.getElementById('btnOnline').classList.remove('on');
  document.getElementById('onstat').textContent='АВАРИЯ: ЭБУ сообщил, что указатель карты испорчен. Онлайн снят. Не правь ячейки, пока не переподключишь карту.';
 }
 csumCheck(p);
 // блок сам ушёл с тени на ПЗУ (сброс питания/зажигания) — сказать явно, не молчать
 if(ptrWas===true&&on===false){
  online=false;editRendered=false;saveProg();
  document.getElementById('btnOnline').classList.remove('on');
  document.getElementById('onstat').textContent='ЭБУ СБРОСИЛСЯ: указатели вернулись на ПЗУ, мотор на стоке. Тень в ОЗУ цела — нажми ОНЛАЙН, чтобы вернуть.';
 }
 ptrWas=on;
 if(on&&!online){   // блок в тени, а панель об этом не знала (перезагрузил страницу)
  online=true;document.getElementById('btnOnline').classList.add('on');
  document.getElementById('btnSaveBin').style.display='';document.getElementById('btnLoadRom').style.display='';
  document.getElementById('btnOffline').style.display='';
  const tb=document.getElementById('tobin_'+liveMap); if(tb)tb.style.display='';
  const sw=document.getElementById('mapsel'); if(sw)sw.value=liveMap;
  pullShadow();   // ВАЖНО: без этого показали бы бин вместо того, что реально в блоке
 }
}
// вычитать живую тень из блока в панель (когда включились по факту, а данных на компе нет)
let pulling=false,pullTries=0;
async function pullShadow(){
 if(pulling||!liveMap||ONLINE[liveMap])return;
 // ОГРАНИЧИТЕЛЬ: без него отказ вычита крутился бы вечно — каждая попытка это дамп 2.6с,
 // канал был бы забит наглухо. 3 попытки, дальше ждём ручного нажатия.
 if(pullTries>=3){
  document.getElementById('onstat').textContent='тень не читается (3 попытки). Нажми ОНЛАЙН, чтобы попробовать снова.';
  return;
 }
 pullTries++; pulling=true;
 const o=document.getElementById('onstat');
 try{
  for(const w of [liveMap]){
   o.textContent='вычитываю живую карту ('+(w==='ign'?'угол':'смесь')+') из тени блока...';
   const r=await fetch('/api/readtable',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({which:w,src:'shadow'})});
   const d=await r.json();
   if(!d.ok){
    // НЕ оставляем панель в тупике: откатываем признак онлайна, чтобы попытка повторилась,
    // иначе online=true без данных = карты не рисуются и выхода нет кроме перезагрузки
    ONLINE.fuel=null;ONLINE.ign=null;online=false;editRendered=false;
    document.getElementById('btnOnline').classList.remove('on');
    o.textContent='не вычитал тень ('+w+'): '+(d.error||'')+' — повторю автоматически';
    return;
   }
   ONLINE[w]=d.cells;
  }
  editRendered=false;pullTries=0;setDiverged(false);saveProg();   // прочитано ИЗ блока → совпадает
  o.textContent='ОНЛАЙН восстановлен: показано то, что РЕАЛЬНО в блоке (вычитано из тени).';
 }finally{pulling=false;}
}
// ---- АВАРИЙНЫЙ СТОП ----
// Сохранить лог и бин, оборвать ЭБУ и ШДК, снять выбор прошивки → страница блокируется.
// Карты в блоке НЕ трогаем: что в ЭБУ было (тень или ПЗУ) — то и остаётся.
async function eStop(){
 const b=document.getElementById('btnEstop');
 b.disabled=true; b.textContent='СТОП...';
 const o=document.getElementById('onstat'); if(o)o.textContent='аварийный стоп: сохраняю и отключаюсь...';
 let d={};
 try{
  const r=await fetch('/api/estop',{method:'POST',headers:{'Content-Type':'application/json'},
                                    body:JSON.stringify(ONLINE)});
  d=await r.json();
 }catch(e){ d={errors:['связь с панелью: '+e]}; }
 // локальное состояние — в исходное
 online=false;editRendered=false;ONLINE.fuel=null;ONLINE.ign=null;mapBin=null;pullTries=0;
 try{localStorage.removeItem('j30online');}catch(_){}
 const bo=document.getElementById('btnOnline'); if(bo)bo.classList.remove('on');
 for(const id of ['btnSaveBin','btnLoadRom','btnOffline','tobin_fuel']){
  const e=document.getElementById(id); if(e)e.style.display='none';
 }
 document.getElementById('binsel').value='';
 document.getElementById('port').value='';
 document.getElementById('wport').value='';
 binLock();                       // нет прошивки → #page.locked → все действия выключены
 setDiverged(false);
 let msg='ОСТАНОВЛЕНО. ';
 msg += d.bin ? ('бин сохранён: '+d.bin+'. ') : 'бин не сохранён (нет данных карт). ';
 msg += d.log ? ('лог сохранён: '+d.log+'. ') : 'лог не писался. ';
 msg += 'ЭБУ и ШДК отключены. Карты в блоке не тронуты.';
 if(d.errors&&d.errors.length) msg += ' ОШИБКИ: '+d.errors.join('; ');
 if(o)o.textContent=msg;
 const sw=document.getElementById('stalewarn'); if(sw)sw.style.display='none';
 b.disabled=false; b.innerHTML='&#9632; СТОП';
}
// ---- тик ----
function tick(){fetch('/api/status').then(r=>r.json()).then(d=>{
 const portSel=document.getElementById('port').value, wportSel=document.getElementById('wport').value;
 // d.busy = идёт дамп/заливка: кадры молчат ШТАТНО, не мигаем «нет связи»
 setStat('ecuicon', d.error?'err':(!portSel?'none':((d.running&&(d.rate>0||d.busy))?'ok':'warn')));
 const wb=d.wbl||{};
 // зелёный ТОЛЬКО пока данные свежие: раньше хватало непочищенного raw, и значок
 // оставался зелёным после выдернутого провода
 setStat('wblicon', wb.error?'err':(!wportSel?'none':(wb.running&&wb.fresh?'ok':'warn')));
 // ОНЛАЙН доступен только когда ЭБУ реально стримит
 const conn=d.running&&(d.rate>0||d.busy);
 const bo=document.getElementById('btnOnline'); if(bo)bo.disabled=!conn&&!online;
 // --- ОБРАТНАЯ СВЯЗЬ: состояние берём ИЗ БЛОКА, а не из памяти браузера ---
 // во время дампа кадры не идут → состояние указателей неизвестно, НЕ трогаем показания
 if(!d.busy) syncPtr(d.ptr||{}, conn);
 learnShow(d.learn);
 // B2: признак свежести считался и никем не использовался — образ ОЗУ не чистится,
 // и после обрыва связи HUD продолжал показывать последние значения как живые.
 // frames>0: до первого кадра «протухло» показывать не за что — иначе плашка мигает
 // на каждом свежем подключении
 const stale=d.running&&d.frames>0&&!d.fresh&&!d.busy;
 const vt=document.getElementById('vars'); if(vt)vt.classList.toggle('stale',!!stale);
 const sw=document.getElementById('stalewarn'); if(sw)sw.style.display=stale?'':'none';
 renderVars(d.vars||[], d.top||{});
 // карты из бина для «свести к бину» — СЫРЫЕ байты, своя для каждой таблицы.
 // Именно raw, а не cells: в cells лежит физика (AFR/градусы/коэффициент), её запись в ОЗУ = мусор.
 for(const w of ['fuel','ign','ve','ktps']){if(d[w]&&d[w].raw)BINCELLS[w]=d[w].raw;}
 // карты ДАД показываем только на ДАД-бине — на MAF-бине их там просто нет
 for(const w of ['ve','ktps']){const bx=document.getElementById('box_'+w);
  if(bx)bx.style.display=d[w]?'':'none';}
 if(d.fuel&&d.ign){
  // оси для КАЖДОЙ карты: без них renderEdit не рисует редактируемую таблицу
  for(const w of ['fuel','ign','ve','ktps']){if(d[w])AX[w]={rows:d[w].rows,cols:d[w].cols};}
  if(mapBin!==d.bin||!online){
   // живую карту рисует renderEdit (редактируемая), остальные — через mapView:
   // если в панели лежат несохранённые правки этой карты, показываем ИХ, а не бин.
   for(const w of ['fuel','ign','ve','ktps']){
    if(online&&liveMap===w)continue;
    if(!d[w])continue;
    document.getElementById(MAPBOX[w]).innerHTML=renderMap(mapView(w,d[w]),w);
   }
   mapBin=d.bin;hlIds={fuel:null,ign:null,ve:null,ktps:null};}
  // восстановление онлайна из памяти браузера: отрисовать редактируемые таблицы когда оси готовы
  if(online&&liveMap&&ONLINE[liveMap]&&AX[liveMap]&&!editRendered){renderEdit(liveMap);editRendered=true;}
  setHL('fuel',d.fuel.hr,d.fuel.hc);setHL('ign',d.ign.hr,d.ign.hc);
 }
}).catch(e=>{}).finally(()=>setTimeout(tick,150));}   // 400→150мс: срезает до 250мс экранной задержки
function toggletheme(){const dark=document.getElementById('darkbox').checked;
 document.body.classList.toggle('light',!dark);
 try{localStorage.setItem('j30theme',dark?'dark':'light');}catch(_){}}
try{if(localStorage.getItem('j30theme')=='dark'){document.body.classList.remove('light');document.getElementById('darkbox').checked=true;}}catch(_){}
loadProg();wireBulk();loadPorts();loadBins();learnLogs();tick();
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
        # УБРАН /api/poke (отладочный, произвольный адрес). ВАЖНО: он стоял ВЫШЕ /api/pokecell,
        # а "/api/pokecell".startswith("/api/poke") == True — значит ВСЕ правки ячеек попадали
        # сюда, где addr по умолчанию 0 → запись уходила в $0000 вместо карты. Правка ячейки
        # не работала вообще. Теперь /api/pokecell обрабатывается сам.
        # УБРАН /api/cmd (слал ПРОИЗВОЛЬНЫЙ байт — та же дыра, что /api/tx и /api/poke:
        # прилетит C5 или CA и автомат приёма в ЭБУ уедет). Заменён на /api/flip.
        if self.path.startswith("/api/flip"):
            # ПОДКЛЮЧИТЬ карту к тени или ОТЦЕПИТЬ всё — с подтверждением от ЭБУ.
            # which: 'fuel' | 'ign' | пусто/none = отцепить (обе карты на ПЗУ).
            # Раньше флип уходил вслепую: байт терялся — панель писала «на тени», а мотор
            # оставался на ПЗУ. Теперь номер читается обратно из ЭБУ.
            s = CTRL.get("ser")
            if not s: self._json({"ok": False, "error": "порт не открыт"}); return
            which = data.get("which")
            if not which and data.get("shadow"): which = "fuel"      # старый вызов без имени карты
            if which and which not in CBNUM:
                self._json({"ok": False, "error": "неизвестная карта: %s" % which}); return
            with SER_LOCK:
                ok = _select_map(s, which)
            self._json({"ok": ok, "which": which or "", "shadow": bool(which),
                        "error": "" if ok else "ЭБУ не подтвердил выбор карты"}); return
        if self.path.startswith("/api/readtable"):
            # ВЫЧИТ таблицы через C9-дамп (~1-2с). src: shadow (живая тень) | rom (ПЗУ, «считать из ПЗУ»)
            which = data.get("which", "fuel"); src = data.get("src", "shadow"); s = CTRL.get("ser")
            base = (ROMMAP if src == "rom" else SHADOW).get(which)
            if not s or base is None: self._json({"ok": False, "error": "нет ЭБУ/таблицы"}); return
            with SER_LOCK:
                cells = _dump_read(s, base, 256)
            if cells is None: self._json({"ok": False, "error": "дамп не синхронизировался — повтори"}); return
            self._json({"ok": True, "which": which, "src": src, "cells": cells}); return
        if self.path.startswith("/api/pokecells"):
            # МАССОВАЯ правка: список {idx,val}. Группируем в непрерывные отрезки и шлём
            # блоками с контрольной суммой — один блок вместо десятков одиночных команд.
            which = data.get("which", "fuel"); s_ = CTRL.get("ser"); base = SHADOW.get(which)
            cells = data.get("cells") or []
            if not s_ or base is None: self._json({"ok": False, "error": "нет ЭБУ"}); return
            if not cells: self._json({"ok": False, "error": "нечего писать"}); return
            byidx = {}
            for c in cells:
                try: byidx[int(c["idx"]) & 0xFF] = int(c["val"]) & 0xFF
                except Exception: pass
            idxs = sorted(byidx)
            runs = []                                  # непрерывные отрезки, не длиннее блока
            for i in idxs:
                if runs and i == runs[-1][-1] + 1 and len(runs[-1]) < BLK_MAX: runs[-1].append(i)
                else: runs.append([i])
            bad = 0; err = ""
            with SER_LOCK:
                for run in runs:
                    ok = False
                    for _ in range(3):
                        ok, e = _send_block(s_, base + run[0], [byidx[i] for i in run])
                        if ok: break
                        err = e
                    if not ok: bad += len(run)
            self._json({"ok": bad == 0, "written": len(idxs) - bad, "failed": bad,
                        "error": "" if bad == 0 else ("не применилось ячеек: %d (%s)" % (bad, err))}); return
        if self.path.startswith("/api/pokecell"):
            # ОДНА ячейка — блоком из 1 байта с контрольной суммой: ЭБУ подтверждает счётчиком.
            # Раньше: poke + peek + ожидание 2 кадров ≈ 0.87с. Теперь ≈ 0.06с и с гарантией.
            which = data.get("which", "fuel"); idx = int(data.get("idx", 0)) & 0xFF; val = int(data.get("val", 0)) & 0xFF
            s = CTRL.get("ser"); base = SHADOW.get(which)
            if not s or base is None: self._json({"ok": False, "error": "нет ЭБУ"}); return
            with SER_LOCK:
                ok, err = _send_block(s, base + idx, [val])
            self._json({"ok": ok, "applied": ok, "readback": val if ok else None, "error": err}); return
        if self.path.startswith("/api/applybin"):
            # ВЫБРАТЬ карту: отцепить тень → залить в неё таблицу из бина → отдать тень этой карте
            which = data.get("which", "fuel"); s = CTRL.get("ser"); base = SHADOW.get(which)
            t = load_tables(SEL["bin"])
            if not s or base is None or not t: self._json({"ok": False, "error": "нет ЭБУ/бина"}); return
            arr = [b & 0xFF for b in t[which]]
            with SER_LOCK:
                ok, nbad, err = _fill_shadow(s, which, arr)
            self._json({"ok": ok, "which": which, "cells": arr, "mismatch": nbad, "error": err}); return
        if self.path.startswith("/api/loadrom"):
            # «считать из ПЗУ»: C9-дамп стоковой карты из ПЗУ → залить в тень (чтобы живое = показанному) → вернуть
            which = data.get("which", "fuel"); s = CTRL.get("ser")
            sbase = SHADOW.get(which); rbase = ROMMAP.get(which)
            if not s or sbase is None or rbase is None: self._json({"ok": False, "error": "нет ЭБУ/таблицы"}); return
            with SER_LOCK:
                cells = _dump_read(s, rbase, 256)
                if cells is None: self._json({"ok": False, "error": "дамп ПЗУ не синхронизировался — повтори"}); return
                ok, nbad, err = _fill_shadow(s, which, cells)
            self._json({"ok": ok, "which": which, "cells": cells, "mismatch": nbad, "error": err}); return
        if self.path.startswith("/api/savebin"):
            # запечь текущие таблицы (с фронта) в копию бина → логи/<бин>_лог_дата.bin
            name, err = _bake_bin(data)
            self._json({"ok": not err, "name": name, "error": err}); return
        if self.path.startswith("/api/learn/par"):
            # пороги обучения. Пресеты «быстро/точно» фронт шлёт как готовый набор чисел.
            for k, v in (data or {}).items():
                if k in LPAR:
                    try: LPAR[k] = float(v)
                    except Exception: pass
            LPAR["min_hits"] = max(1, int(LPAR["min_hits"]))
            self._json({"ok": True, "par": dict(LPAR)}); return
        if self.path.startswith("/api/learn/start"):
            # Учим ТУ карту, что сейчас живая по данным ЭБУ. Панель присылает её текущее
            # содержимое — оно же становится снимком для отката.
            s = CTRL.get("ser")
            if not s: self._json({"ok": False, "error": "порт не открыт"}); return
            with SER_LOCK:
                sel, verd = _read_sel(s)
            lm = ""
            for w, num in CBNUM.items():
                if sel == num: lm = w
            if not lm or verd != 1:
                self._json({"ok": False, "error": "в блоке нет живой карты — сначала ОНЛАЙН"}); return
            if lm not in ("ve", "ktps"):
                self._json({"ok": False, "error": "обучение сделано для VE и Ktps, живая сейчас «%s»" % lm}); return
            cells = data.get("cells")
            if not cells or len(cells) != 256:
                self._json({"ok": False, "error": "панель не прислала карту"}); return
            # вторая карта ДАД обязана быть 1.0, иначе поправка ляжет дважды
            t = load_tables(SEL["bin"]) or {}
            other = "ktps" if lm == "ve" else "ve"
            oa = t.get(other)
            if oa and any(z != 0x80 for z in oa):
                self._json({"ok": False, "error":
                            "карта «%s» не единичная — учить можно только одну, вторую выставь 1.0" % other}); return
            ONLINE_SRV[lm] = [int(z) & 0xFF for z in cells]
            LEARN.update({"on": True, "which": lm, "acc": {}, "hits": {}, "applied": 0,
                          "rejects": {}, "base": list(ONLINE_SRV[lm]), "note": ""})
            LHIST.clear(); LCUT["t"] = 0.0
            self._json({"ok": True, "which": lm}); return
        if self.path.startswith("/api/learn/stop"):
            LEARN["on"] = False
            self._json({"ok": True, "applied": LEARN["applied"],
                        "cells": ONLINE_SRV.get(LEARN["which"]) or []}); return
        if self.path.startswith("/api/learn/logs"):
            d_ = os.path.join(HERE, "логи")
            try:
                fs = sorted((f for f in os.listdir(d_) if f.lower().endswith(".csv")), reverse=True)
            except Exception: fs = []
            self._json({"ok": True, "files": fs}); return
        if self.path.startswith("/api/learn/fromlog"):
            # ПРОГОН ПО ЛОГУ. В блок не пишем — только считаем и показываем.
            which = data.get("which") or LEARN["which"] or "ve"
            if which not in ("ve", "ktps"):
                self._json({"ok": False, "error": "по логу учатся VE и Ktps"}); return
            fn = data.get("file") or ""
            path = os.path.join(HERE, "логи", os.path.basename(fn))
            if not os.path.exists(path): self._json({"ok": False, "error": "лог не найден"}); return
            t = load_tables(SEL["bin"])
            if not t or not t.get(which):
                self._json({"ok": False, "error": "в выбранном бине нет карты «%s»" % which}); return
            base = [z & 0xFF for z in t[which]]
            try:
                cells, cov, rej, changed = learn_from_log(path, which, base, t)
            except Exception as e:
                self._json({"ok": False, "error": "разбор лога: %s" % e}); return
            if cells is None:
                self._json({"ok": False, "error": list(rej)[0] if rej else "не посчиталось"}); return
            self._json({"ok": True, "which": which, "cells": cells, "base": base,
                        "cov": {str(i): n for i, n in cov.items()},
                        "rejects": rej, "changed": changed}); return
        if self.path.startswith("/api/learn/push"):
            # залить показанную карту в тень (после прогона по логу — с твоего согласия)
            which = data.get("which"); cells = data.get("cells"); s = CTRL.get("ser")
            if which not in SHADOW or not cells or len(cells) != 256 or not s:
                self._json({"ok": False, "error": "нет ЭБУ/карты"}); return
            with SER_LOCK:
                ok, nbad, err = _fill_shadow(s, which, [int(z) & 0xFF for z in cells])
            if ok: ONLINE_SRV[which] = [int(z) & 0xFF for z in cells]
            self._json({"ok": ok, "mismatch": nbad, "error": err}); return
        if self.path.startswith("/api/learn/rollback"):
            # вернуть карту, какой она была до начала обучения
            which = LEARN["which"]; base = LEARN["base"]; s = CTRL.get("ser")
            if not base or not which or not s:
                self._json({"ok": False, "error": "нечего откатывать"}); return
            LEARN["on"] = False
            with SER_LOCK:
                ok, nbad, err = _fill_shadow(s, which, base)
            if ok:
                ONLINE_SRV[which] = list(base); LEARN["acc"] = {}; LEARN["hits"] = {}
            self._json({"ok": ok, "cells": base, "error": err}); return
        if self.path.startswith("/api/estop"):
            # АВАРИЙНЫЙ СТОП. Порядок важен: сначала СОХРАНИТЬ, потом рвать связь.
            # Карты в ЭБУ НЕ трогаем — блок остаётся с тем, что в нём было (тень или ПЗУ).
            res = {"bin": "", "log": "", "errors": []}
            name, err = _bake_bin(data, suffix="_СТОП_")
            res["bin"] = name
            if err and err != "бин не выбран": res["errors"].append("бин: " + err)
            try:
                res["log"] = os.path.basename(LOGST["path"]) if LOGST.get("on") else ""
            except Exception: pass
            for fn_, tag in ((log_stop, "лог"), (do_stop, "ЭБУ"), (wbl_stop, "ШДК")):
                try: fn_()
                except Exception as e: res["errors"].append("%s: %s" % (tag, e))
            SEL["bin"] = ""                      # снять выбор прошивки → страница блокируется
            res["ok"] = True
            self._json(res); return
        # УБРАНЫ отладочные эндпоинты /api/peek, /api/ramprobe, /api/tx, /api/tx/hold.
        # Пока приём был опросным, произвольные байты в основном терялись. С приёмным
        # ПРЕРЫВАНИЕМ ловится каждый — флуд байтом 0xC5 запускал бы бесконечные POKE,
        # а guard разрешает запись ровно в $1800-$1FFF, т.е. В ЖИВЫЕ КАРТЫ на ходу.
        # Карта ОЗУ промерена, отладка больше не нужна.
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
