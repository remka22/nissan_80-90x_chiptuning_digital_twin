# -*- coding: utf-8 -*-
"""
Сырой монитор входа ЭБУ.

Что делает:
  - читает СЫРЬЁ с последовательного порта (что бы там ни приходило);
  - ПИШЕТ всё в файл на диск (raw_вход_ДАТА.bin) — офлайн, ничего не теряется;
  - поднимает локальную страницу http://localhost:8009 — видно live: есть поток или тишина,
    сколько байт, байт/сек, последние байты в hex+ascii, и сколько кадров AE17 нашлось.
  - интернет НЕ нужен (всё на localhost, без CDN).

Запуск (в машине, после прошивки логгер-бина):
    python3 "raw_монитор входа 31.07.26 ИИ.py"
    # порт и скорость по умолчанию: /dev/cu.usbserial-A5069RR4 @ 125000
    # свои:
    python3 "raw_монитор входа 31.07.26 ИИ.py" --port /dev/cu.usbserial-XXXX --baud 125000

Проверить, что САМА страница работает (без машины) — демо-поток:
    python3 "raw_монитор входа 31.07.26 ИИ.py" --demo

Открыть в браузере: http://localhost:8009
Выход: Ctrl+C. Сырьё уже сохранено в файл — его и пришлёшь.
"""
import argparse, threading, time, json, sys, os
from collections import deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))

# --- общее состояние ---
LOCK = threading.Lock()
STATE = {
    "total": 0,          # всего принято байт
    "recent": deque(maxlen=1024),   # последние байты для показа
    "events": deque(maxlen=4000),   # (t, n) для расчёта байт/сек
    "frames": 0,         # кадров AE17 с верной чек-суммой
    "bad": 0,            # битых кадров
    "connected": False,
    "error": "",
    "file": "",
    "started": time.time(),
}

def find_frames(buf):
    """Ищем кадры AE 17 addr_hi addr_lo len data... chk(XOR). Возвращаем (ok, bad)."""
    ok = bad = 0; i = 0; n = len(buf)
    while i < n - 5:
        if buf[i] == 0xAE and buf[i+1] == 0x17:
            ln = buf[i+4]; end = i + 5 + ln
            if end < n:
                c = 0
                for b in buf[i:i+5+ln]: c ^= b
                if c == buf[end]:
                    ok += 1; i = end + 1; continue
                else:
                    bad += 1
        i += 1
    return ok, bad

def reader_serial(port, baud):
    import serial
    try:
        ser = serial.Serial(port, baud, timeout=0.2)
    except Exception as e:
        with LOCK:
            STATE["error"] = f"Не открыл порт {port}: {e}"
        return
    time.sleep(0.2); ser.reset_input_buffer()
    with LOCK: STATE["connected"] = True
    fname = os.path.join(HERE, "raw_вход_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bin")
    with LOCK: STATE["file"] = fname
    f = open(fname, "ab")
    winbuf = bytearray()   # окно для поиска кадров
    while True:
        chunk = ser.read(512)
        if chunk:
            f.write(chunk); f.flush()
            now = time.time()
            winbuf += chunk
            if len(winbuf) > 4096: winbuf = winbuf[-4096:]
            ok, bad = find_frames(winbuf)
            with LOCK:
                STATE["total"] += len(chunk)
                for b in chunk: STATE["recent"].append(b)
                STATE["events"].append((now, len(chunk)))
                STATE["frames"] = ok
                STATE["bad"] = bad

def reader_demo():
    """Демо: имитируем поток, чтобы проверить саму страницу без машины."""
    with LOCK:
        STATE["connected"] = True
        STATE["file"] = "(демо — на диск не пишу)"
    seed = 12345
    def rnd():
        nonlocal seed
        seed = (1103515245 * seed + 12345) & 0x7fffffff
        return seed
    while True:
        # кадр AE17 с полем нагрузки + мусор
        data = bytes([(rnd() >> 7) & 0xFF for _ in range(8)])
        frame = bytearray([0xAE, 0x17, 0x14, 0x82, len(data)]) + data
        c = 0
        for b in frame: c ^= b
        frame.append(c)
        chunk = bytes(frame)
        now = time.time()
        with LOCK:
            STATE["total"] += len(chunk)
            for b in chunk: STATE["recent"].append(b)
            STATE["events"].append((now, len(chunk)))
            STATE["frames"] += 1
        time.sleep(0.1)

PAGE = """<!doctype html><html lang=ru><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Сырой монитор входа ЭБУ</title>
<style>
 body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#111;color:#ddd}
 header{padding:14px 18px;border-bottom:1px solid #333}
 h1{font-size:16px;margin:0 0 4px}
 .sub{font-size:12px;color:#888}
 #banner{padding:18px;text-align:center;font-size:24px;font-weight:700;letter-spacing:1px}
 .live{background:#0a4d20;color:#6f6}
 .quiet{background:#3a1010;color:#f88}
 .err{background:#5a1a1a;color:#fbb}
 .stats{display:flex;gap:18px;flex-wrap:wrap;padding:12px 18px}
 .stat{background:#1b1b1b;border:1px solid #333;border-radius:8px;padding:10px 14px;min-width:110px}
 .stat b{display:block;font-size:22px}
 .stat span{font-size:11px;color:#888}
 #hexwrap{padding:0 18px 18px}
 pre{background:#0a0a0a;border:1px solid #333;border-radius:8px;padding:12px;overflow:auto;
     max-height:52vh;font-size:12px;line-height:1.5;white-space:pre-wrap;word-break:break-all}
 .file{padding:0 18px 18px;font-size:12px;color:#888}
 .file code{color:#9cf}
</style></head><body>
<header>
 <h1>Сырой монитор входа ЭБУ</h1>
 <div class=sub>Показывает что приходит на провод. Сырьё пишется в файл на диск (офлайн).</div>
 <div class=sub style="margin-top:6px"><a href="http://localhost:8080/" style="color:#9cf;font-weight:600">→ http://localhost:8080/</a></div>
</header>
<div id=banner class=quiet>…</div>
<div class=stats>
 <div class=stat><b id=total>0</b><span>всего байт</span></div>
 <div class=stat><b id=rate>0</b><span>байт / сек</span></div>
 <div class=stat><b id=frames>0</b><span>кадров AE17</span></div>
 <div class=stat><b id=bad>0</b><span>битых кадров</span></div>
</div>
<div id=hexwrap>
 <div class=sub style="margin:0 0 6px">последние байты (hex · ascii):</div>
 <pre id=hex>—</pre>
</div>
<div class=file>файл сырья: <code id=file>—</code></div>
<script>
async function tick(){
 try{
  const r = await fetch('/data'); const d = await r.json();
  const b = document.getElementById('banner');
  if(d.error){ b.className='err'; b.textContent='ОШИБКА: '+d.error; }
  else if(d.rate>0){ b.className='live'; b.textContent='● ПОТОК ИДЁТ'; }
  else if(d.connected){ b.className='quiet'; b.textContent='ТИШИНА (порт открыт, байт нет)'; }
  else { b.className='quiet'; b.textContent='жду подключения…'; }
  document.getElementById('total').textContent=d.total;
  document.getElementById('rate').textContent=d.rate;
  document.getElementById('frames').textContent=d.frames;
  document.getElementById('bad').textContent=d.bad;
  document.getElementById('file').textContent=d.file||'—';
  document.getElementById('hex').textContent=d.hex||'—';
 }catch(e){}
 setTimeout(tick,400);
}
tick();
</script></body></html>"""

_last = {"t": time.time(), "total": 0}

def snapshot():
    now = time.time()
    with LOCK:
        total = STATE["total"]
        recent = list(STATE["recent"])
        events = list(STATE["events"])
        frames = STATE["frames"]; bad = STATE["bad"]
        connected = STATE["connected"]; error = STATE["error"]; file = STATE["file"]
    # байт/сек за последнюю секунду
    rate = sum(n for (t, n) in events if now - t <= 1.0)
    # hex+ascii последних байт (по 16 в строке)
    lines = []
    for i in range(0, len(recent), 16):
        row = recent[i:i+16]
        hx = " ".join(f"{b:02x}" for b in row)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in row)
        lines.append(f"{hx:<47}  {asc}")
    return {
        "total": total, "rate": rate, "frames": frames, "bad": bad,
        "connected": connected, "error": error, "file": file,
        "hex": "\n".join(lines[-40:]),
    }

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.startswith("/data"):
            body = json.dumps(snapshot()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
        else:
            body = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="/dev/cu.usbserial-A5069RR4")
    ap.add_argument("--baud", type=int, default=125000)
    ap.add_argument("--http", type=int, default=8009)
    ap.add_argument("--demo", action="store_true", help="имитировать поток без машины")
    args = ap.parse_args()

    if args.demo:
        threading.Thread(target=reader_demo, daemon=True).start()
        print("ДЕМО-режим: генерирую поток (на диск не пишу).")
    else:
        threading.Thread(target=reader_serial, args=(args.port, args.baud), daemon=True).start()
        print(f"Читаю {args.port} @ {args.baud}. Сырьё пишу в файл рядом со скриптом.")

    srv = ThreadingHTTPServer(("127.0.0.1", args.http), H)
    print(f"Открой в браузере:  http://localhost:{args.http}")
    print("Выход: Ctrl+C (файл сырья уже сохранён).")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановлено. Файл сырья — рядом со скриптом (raw_вход_*.bin).")

if __name__ == "__main__":
    main()
