# -*- coding: utf-8 -*-
"""
Демон-логгер J30: читает поток телеметрии (реальный порт CH340 ИЛИ фейковый ЭБУ),
раскладывает кадры, пишет CSV-лог и отдаёт живьём в браузер через SSE.

Запуск:
  БЕЗ ЖЕЛЕЗА (тест в вакууме):   python3 server.py --sim
  С ЖЕЛЕЗОМ (Mac):              python3 server.py --port /dev/tty.usbserial-XXXX --baud 93750
  С ЖЕЛЕЗОМ (Windows):         python  server.py --port COM5 --baud 93750

Открыть в браузере: http://localhost:8009
"""
import argparse
import json
import os
import queue
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import frame
import ecu_sim
import ramframe
import ram_sim
import labels

HERE = os.path.dirname(os.path.abspath(__file__))

# --- дамп-режим: диапазоны ОЗУ (внутр.+внешн.) и пересчёт в физику ---
DUMP_RANGES = [(0x0040, 0x0100), (0x1400, 0x1800)]
SWEEP_START = 0x0040          # первый адрес прохода (начало внутреннего ОЗУ)
DUMP_CONV = {
    0x140A: ("об/мин", lambda v: round(v * 12.807)),
    0x008F: ("В~", lambda v: round(v * 0.0195, 2)),
    0x140D: ("В~", lambda v: round(v * 0.0195, 2)),
    0x004D: ("мс", lambda v: round(v * 0.005, 3)),
}
_dump_mode = False

# --- общее состояние ---------------------------------------------------------
_subs = set()                 # очереди подписчиков SSE
_subs_lock = threading.Lock()
_latest = {"t": 0, "raw": {}, "phys": {}, "afr": None}
# последний AFR от ШДК (второй источник). None -> данных нет -> в логе "-"
_afr_lock = threading.Lock()
_latest_afr = None


def _broadcast(rec):
    _latest.update(rec)
    with _subs_lock:
        for q in list(_subs):
            try:
                q.put_nowait(rec)
            except queue.Full:
                pass


# --- источники байт ----------------------------------------------------------
def sim_source(stop):
    """Фейковый ЭБУ: генерит кадры ~20 раз/с."""
    t0 = time.time()
    while not stop.is_set():
        t = time.time() - t0
        yield ecu_sim.frame_bytes(t)
        time.sleep(0.05)


def serial_source(stop, port, baud):
    """Реальный порт через pyserial."""
    try:
        import serial
    except ImportError:
        raise SystemExit("Нужен pyserial:  pip install pyserial")
    ser = serial.Serial(port, baud, timeout=0.1)
    try:
        while not stop.is_set():
            data = ser.read(64)
            if data:
                yield data
    finally:
        ser.close()


# --- второй источник: ШДК (широкополосник) по RS232 -------------------------
# AEM X-Series: 9600 8N1, дисплей держать в AFR, поток ASCII (число строкой).
# Точную форму строки фиксируем по сырому образцу (--wbl-raw). Пока — лениво:
# берём первое число из строки, отсекаем по здравому диапазону AFR.
_num_re = re.compile(rb"(\d+(?:\.\d+)?)")


def _parse_afr(line):
    m = _num_re.search(line)
    if not m:
        return None
    try:
        v = float(m.group(1))
    except ValueError:
        return None
    # здравый диапазон AFR (бензин). Отсекает битые строки и баг точки в Lambda.
    # ПОСЛЕ снятия реального образца — заменить на точный разбор формата AEM.
    return v if 8.0 <= v <= 22.0 else None


def wbl_reader_loop(stop, port, baud, raw=False):
    """Читает ШДК со второго порта -> кладёт AFR в _latest_afr."""
    global _latest_afr
    try:
        import serial
    except ImportError:
        print("ШДК: нужен pyserial (pip install pyserial)")
        return
    try:
        ser = serial.Serial(port, baud, timeout=0.2)
    except Exception as e:                       # noqa: BLE001
        print("ШДК: не открыть порт %s: %s" % (port, e))
        return
    buf = bytearray()
    try:
        while not stop.is_set():
            data = ser.read(64)
            if not data:
                continue
            if raw:                              # сырой дамп — снять образец формата
                hexs = " ".join("%02X" % b for b in data)
                txt = "".join(chr(b) if 32 <= b < 127 else "." for b in data)
                print("ШДК RAW | %s | %s" % (hexs, txt))
                continue
            buf.extend(data)
            while True:                          # резать по CR/LF
                i = next((k for k, b in enumerate(buf) if b in (0x0D, 0x0A)), -1)
                if i < 0:
                    break
                line = bytes(buf[:i])
                del buf[:i + 1]
                afr = _parse_afr(line)
                if afr is not None:
                    with _afr_lock:
                        _latest_afr = afr
            if len(buf) > 256:                   # не копить мусор
                del buf[:len(buf) - 256]
    finally:
        ser.close()


def sim_afr_loop(stop):
    """Фейковый AFR для проверки мержа в вакууме (--sim)."""
    global _latest_afr
    t0 = time.time()
    while not stop.is_set():
        with _afr_lock:
            _latest_afr = ecu_sim.gen_afr(time.time() - t0)
        time.sleep(0.1)


# --- поток чтения: байты -> кадры -> лог + broadcast -------------------------
def reader_loop(source_gen, csv_path, stop):
    dec = frame.StreamDecoder()
    csv = open(csv_path, "w", encoding="utf-8")
    header = ["t_ms"] + [k for k, *_ in frame.FIELDS] + ["afr"]
    csv.write(",".join(header) + "\n")
    csv.flush()
    t0 = time.time()
    n = 0
    for chunk in source_gen:
        if stop.is_set():
            break
        for raw in dec.feed(chunk):
            phys = frame.to_phys(raw)
            t_ms = int((time.time() - t0) * 1000)
            with _afr_lock:
                afr = _latest_afr
            afr_s = ("%.2f" % afr) if afr is not None else "-"   # нет ШДК -> "-"
            row = ([str(t_ms)] + [str(phys[k]) for k, *_ in frame.FIELDS]
                   + [afr_s])
            csv.write(",".join(row) + "\n")
            n += 1
            if n % 20 == 0:
                csv.flush()
            _broadcast({"t": t_ms, "raw": raw, "phys": phys, "afr": afr})
    csv.flush()
    csv.close()


# --- дамп-режим: источник + сборка образа ОЗУ -------------------------------
def sim_dump_source(stop):
    """Фейковый дамп ОЗУ блоками (~500 блоков/с)."""
    t0 = time.time()
    while not stop.is_set():
        yield ram_sim.next_block(time.time() - t0)
        time.sleep(0.002)


def extract_labeled(image):
    """Из образа ОЗУ вытащить известные величины по таблице меток."""
    out = {}
    for addr, meta in labels.LABELS.items():
        sz = meta.get("size", 1)
        if addr not in image:
            continue
        if sz == 2:
            if (addr + 1) not in image:
                continue
            raw = (image[addr] << 8) | image[addr + 1]
        else:
            raw = image[addr]
        conv = DUMP_CONV.get(addr)
        out["$%04X" % addr] = {
            "name": meta["name"], "raw": raw,
            "phys": conv[1](raw) if conv else None,
            "unit": conv[0] if conv else "",
            "conf": meta["conf"],
        }
    return out


def dump_reader_loop(source_gen, csv_path, stop):
    """Собирает образ ОЗУ из блоков; на каждый полный проход — запись в лог
    (метки + сырой полный образ) и broadcast на страницу."""
    dec = ramframe.RamDecoder()
    raw_path = csv_path.replace(".csv", "_raw.csv")
    csv = open(csv_path, "w", encoding="utf-8")
    raw_f = open(raw_path, "w", encoding="utf-8")
    cols = sorted(labels.LABELS)
    csv.write("t_ms," + ",".join(labels.LABELS[a]["name"] for a in cols) + "\n")
    csv.flush()
    raw_f.write("t_ms," + "_".join("%04X%04X" % (lo, hi - 1)
                                   for lo, hi in DUMP_RANGES) + "_hex\n")
    raw_f.flush()
    t0 = time.time()
    seen_start = False
    sweep = 0
    for chunk in source_gen:
        if stop.is_set():
            break
        for addr, _payload in dec.feed(chunk):
            if addr != SWEEP_START:
                continue
            if not seen_start:               # первый заход — ждём полного прохода
                seen_start = True
                continue
            t_ms = int((time.time() - t0) * 1000)
            vars_ = extract_labeled(dec.image)
            row = [str(t_ms)]
            for a in cols:
                v = vars_.get("$%04X" % a)
                row.append(str(v["raw"]) if v else "-")
            csv.write(",".join(row) + "\n")
            raw = bytes(dec.image.get(a, 0)
                        for lo, hi in DUMP_RANGES for a in range(lo, hi))
            raw_f.write("%d,%s\n" % (t_ms, raw.hex()))
            sweep += 1
            if sweep % 8 == 0:
                csv.flush()
                raw_f.flush()
            _broadcast({"t": t_ms, "sweep": sweep, "vars": vars_})
    csv.flush()
    csv.close()
    raw_f.flush()
    raw_f.close()


# --- HTTP + SSE --------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass  # тихо

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self._serve_file("dump.html" if _dump_mode else "index.html",
                             "text/html; charset=utf-8")
        elif self.path == "/fields":
            body = json.dumps({
                "fields": [{"key": k, "unit": frame.UNITS.get(k, "")}
                           for k, *_ in frame.FIELDS]
                          + [{"key": "afr", "unit": "AFR"}]
            }).encode("utf-8")
            self._send(200, "application/json", body)
        elif self.path == "/stream":
            self._sse()
        else:
            self._send(404, "text/plain", b"not found")

    def _serve_file(self, name, ctype):
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            self._send(404, "text/plain", b"no file")
            return
        with open(p, "rb") as f:
            self._send(200, ctype, f.read())

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass

    def _sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        q = queue.Queue(maxsize=200)
        with _subs_lock:
            _subs.add(q)
        try:
            # сразу отдать последнее значение
            if _latest.get("phys") or _latest.get("vars"):
                self._event(_latest)
            while True:
                try:
                    rec = q.get(timeout=5)
                    self._event(rec)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")   # heartbeat
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            with _subs_lock:
                _subs.discard(q)

    def _event(self, rec):
        if "vars" in rec:                       # дамп-режим
            payload = json.dumps(rec)
        else:                                    # фиксированный кадр
            phys = dict(rec.get("phys", {}))
            phys["afr"] = rec.get("afr")        # AFR со второго источника (или None)
            payload = json.dumps({"t": rec["t"], "phys": phys,
                                  "raw": rec.get("raw", {})})
        self.wfile.write(("data: " + payload + "\n\n").encode("utf-8"))
        self.wfile.flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", action="store_true", help="фейковый ЭБУ без железа")
    ap.add_argument("--port", help="серийный порт (реальный ЭБУ)")
    ap.add_argument("--baud", type=int, default=93750, help="скорость (кварц/64)")
    ap.add_argument("--http-port", type=int, default=8009)
    ap.add_argument("--log", default=None, help="файл CSV-лога")
    ap.add_argument("--wbl-port", help="порт ШДК (RS232) — второй источник AFR")
    ap.add_argument("--wbl-baud", type=int, default=9600, help="скорость ШДК (AEM=9600)")
    ap.add_argument("--wbl-raw", action="store_true", help="сырой дамп потока ШДК")
    ap.add_argument("--dump", action="store_true",
                    help="режим полного дампа ОЗУ (протокол ramframe)")
    args = ap.parse_args()

    if not args.sim and not args.port:
        raise SystemExit("Укажи --sim (без железа) или --port ... (с железом)")

    log_path = args.log or os.path.join(
        HERE, "log_%s.csv" % time.strftime("%d.%m_%H%M"))

    stop = threading.Event()
    global _dump_mode
    _dump_mode = args.dump
    tag = " [ДАМП ОЗУ]" if args.dump else ""
    if args.sim:
        src = sim_dump_source(stop) if args.dump else sim_source(stop)
        print("Источник: ФЕЙКОВЫЙ ЭБУ (вакуум)%s" % tag)
    else:
        src = serial_source(stop, args.port, args.baud)
        print("Источник: порт %s @ %d бод%s" % (args.port, args.baud, tag))

    loop = dump_reader_loop if args.dump else reader_loop
    th = threading.Thread(target=loop, args=(src, log_path, stop), daemon=True)
    th.start()

    # второй источник — ШДК
    if args.wbl_port:
        thw = threading.Thread(
            target=wbl_reader_loop,
            args=(stop, args.wbl_port, args.wbl_baud, args.wbl_raw),
            daemon=True)
        thw.start()
        print("ШДК: порт %s @ %d%s" % (args.wbl_port, args.wbl_baud,
              " (СЫРОЙ ДАМП)" if args.wbl_raw else ""))
    elif args.sim:
        threading.Thread(target=sim_afr_loop, args=(stop,), daemon=True).start()
        print("ШДК: фейковый AFR (вакуум)")
    else:
        print("ШДК: не подключён -> колонка afr = '-'")

    httpd = ThreadingHTTPServer(("127.0.0.1", args.http_port), Handler)
    print("Лог: %s" % log_path)
    print("Открой в браузере: http://localhost:%d" % args.http_port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        httpd.shutdown()


if __name__ == "__main__":
    main()
