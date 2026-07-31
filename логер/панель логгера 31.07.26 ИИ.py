# -*- coding: utf-8 -*-
"""
ПАНЕЛЬ ЛОГГЕРА ЭБУ — веб-админка.

Запускаешь ОДИН раз:
    python3 "логер/панель логгера 31.07.26 ИИ.py"
Открываешь:  http://localhost:8009
Дальше ВСЁ из браузера:
    - выбор порта (список живых портов, кнопка «обновить», авто-подсказка FTDI);
    - скорость (по умолчанию 125000);
    - Старт / Стоп;
    - live: есть поток / тишина, всего байт, байт/сек, кадры AE17, hex+ascii;
    - запись сырья в файл на диск (офлайн);
    - кнопка «Скачать лог».

Ничего в терминале больше вводить не надо. Интернет не нужен.
"""
import argparse, threading, time, json, os, glob
from collections import deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = threading.Lock()

# состояние приёма
STATE = {
    "running": False, "port": "", "baud": 0,
    "total": 0, "recent": deque(maxlen=1024), "events": deque(maxlen=4000),
    "frames": 0, "bad": 0, "error": "", "file": "",
}
# управление потоком-читателем
CTRL = {"thread": None, "stop": None, "ser": None}
CTRL_LOCK = threading.Lock()


def list_ports():
    """Живые последовательные порты. Возвращает (список, рекомендованный).
    Источник 1 — перечисление pyserial (даёт vid/описание).
    Источник 2 — прямой глоб /dev/cu.* (страховка на маке, если №1 что-то не увидел)."""
    found = {}  # device -> {device, desc, ftdi}
    # 1) pyserial
    try:
        from serial.tools import list_ports as lp
        for p in lp.comports():
            dev = p.device or ""
            if not dev or "Bluetooth" in dev or "debug" in dev:
                continue
            if dev.startswith("/dev/tty."):   # на маке предпочитаем cu.*
                continue
            found[dev] = {"device": dev, "desc": (p.description or ""),
                          "ftdi": getattr(p, "vid", None) == 0x0403}
    except Exception:
        pass
    # 2) глоб /dev/cu.* — страховка
    for dev in sorted(glob.glob("/dev/cu.*")):
        if "Bluetooth" in dev or "debug" in dev:
            continue
        if dev not in found:
            found[dev] = {"device": dev, "desc": "", "ftdi": False}
    ports = list(found.values())
    # рекомендация: сначала настоящий FTDI, потом любой usbserial, потом первый
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


def find_frames(buf):
    ok = bad = 0; i = 0; n = len(buf)
    while i < n - 5:
        if buf[i] == 0xAE and buf[i + 1] == 0x17:
            ln = buf[i + 4]; end = i + 5 + ln
            if end < n:
                c = 0
                for b in buf[i:i + 5 + ln]:
                    c ^= b
                if c == buf[end]:
                    ok += 1; i = end + 1; continue
                else:
                    bad += 1
        i += 1
    return ok, bad


def reader_loop(ser, stop_ev, fname):
    f = open(fname, "ab")
    winbuf = bytearray()
    try:
        while not stop_ev.is_set():
            chunk = ser.read(512)
            if chunk:
                f.write(chunk); f.flush()
                now = time.time()
                winbuf += chunk
                if len(winbuf) > 4096:
                    winbuf = winbuf[-4096:]
                ok, bad = find_frames(winbuf)
                with LOCK:
                    STATE["total"] += len(chunk)
                    for b in chunk:
                        STATE["recent"].append(b)
                    STATE["events"].append((now, len(chunk)))
                    STATE["frames"] = ok
                    STATE["bad"] = bad
    finally:
        try: ser.close()
        except Exception: pass
        f.close()
        with LOCK:
            STATE["running"] = False


def do_start(port, baud):
    import serial
    with CTRL_LOCK:
        # остановить прошлый приём
        if CTRL["stop"]:
            CTRL["stop"].set()
        if CTRL["thread"]:
            CTRL["thread"].join(timeout=1.0)
        # открыть порт
        try:
            ser = serial.Serial(port, int(baud), timeout=0.2)
        except Exception as e:
            with LOCK:
                STATE["error"] = f"Не открыл {port} @ {baud}: {e}"
                STATE["running"] = False
            return False, STATE["error"]
        time.sleep(0.2)
        try: ser.reset_input_buffer()
        except Exception: pass
        fname = os.path.join(HERE, "raw_вход_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bin")
        # сброс статистики
        with LOCK:
            STATE.update({"running": True, "port": port, "baud": int(baud),
                          "total": 0, "frames": 0, "bad": 0, "error": "", "file": fname})
            STATE["recent"].clear(); STATE["events"].clear()
        stop_ev = threading.Event()
        th = threading.Thread(target=reader_loop, args=(ser, stop_ev, fname), daemon=True)
        CTRL["thread"] = th; CTRL["stop"] = stop_ev; CTRL["ser"] = ser
        th.start()
        return True, ""


def do_stop():
    with CTRL_LOCK:
        if CTRL["stop"]:
            CTRL["stop"].set()
        if CTRL["thread"]:
            CTRL["thread"].join(timeout=1.0)
        CTRL["thread"] = None; CTRL["stop"] = None; CTRL["ser"] = None
    with LOCK:
        STATE["running"] = False
    return True


def snapshot():
    now = time.time()
    with LOCK:
        recent = list(STATE["recent"]); events = list(STATE["events"])
        d = {k: STATE[k] for k in ("running", "port", "baud", "total", "frames", "bad", "error", "file")}
    d["rate"] = sum(n for (t, n) in events if now - t <= 1.0)
    lines = []
    for i in range(0, len(recent), 16):
        row = recent[i:i + 16]
        hx = " ".join(f"{b:02x}" for b in row)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in row)
        lines.append(f"{hx:<47}  {asc}")
    d["hex"] = "\n".join(lines[-40:])
    d["file_short"] = os.path.basename(d["file"]) if d["file"] else ""
    return d


PAGE = """<!doctype html><html lang=ru><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Панель логгера ЭБУ</title>
<style>
 body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#12151a;color:#e6e6e6}
 header{padding:14px 18px;background:#1e2a38;border-bottom:1px solid #2a3a4a}
 h1{font-size:17px;margin:0}
 .sub{font-size:12px;color:#9ab;margin-top:3px}
 .panel{padding:16px 18px;display:flex;flex-wrap:wrap;gap:12px;align-items:end;
        background:#161b22;border-bottom:1px solid #263040}
 .fld{display:flex;flex-direction:column;gap:4px}
 .fld label{font-size:11px;color:#8aa}
 select,input{background:#0d1117;color:#e6e6e6;border:1px solid #30404f;border-radius:6px;
        padding:8px 10px;font-size:14px;min-width:220px}
 input.baud{min-width:120px}
 button{border:0;border-radius:6px;padding:9px 16px;font-size:14px;font-weight:600;cursor:pointer}
 .start{background:#1a7f37;color:#fff}
 .stop{background:#b02a2a;color:#fff}
 .ghost{background:#26313d;color:#cde}
 #banner{padding:16px 18px;text-align:center;font-size:22px;font-weight:700;letter-spacing:.5px}
 .live{background:#0a4d20;color:#7f7}
 .quiet{background:#3a3410;color:#fd6}
 .off{background:#22282f;color:#8aa}
 .err{background:#5a1a1a;color:#fbb}
 .stats{display:flex;gap:14px;flex-wrap:wrap;padding:12px 18px}
 .stat{background:#161b22;border:1px solid #263040;border-radius:8px;padding:10px 14px;min-width:110px}
 .stat b{display:block;font-size:22px}
 .stat span{font-size:11px;color:#8aa}
 #hexwrap{padding:0 18px 14px}
 pre{background:#0a0d11;border:1px solid #263040;border-radius:8px;padding:12px;overflow:auto;
     max-height:46vh;font-size:12px;line-height:1.5;white-space:pre;font-family:ui-monospace,Menlo,monospace}
 .foot{padding:0 18px 18px;font-size:12px;color:#8aa;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 .foot code{color:#9cf}
 a.dl{color:#9cf;text-decoration:none;border:1px solid #30404f;border-radius:6px;padding:7px 12px}
</style></head><body>
<header>
 <h1>&#128225; Панель логгера ЭБУ</h1>
 <div class=sub>Выбери порт и скорость, жми Старт. Сырьё пишется в файл (офлайн). Интернет не нужен.</div>
</header>

<div class=panel>
 <div class=fld>
   <label>Порт (авто-подсказка — FTDI)</label>
   <select id=port></select>
 </div>
 <button class=ghost onclick=loadPorts()>&#8635; обновить порты</button>
 <div class=fld>
   <label>Скорость — быстрый выбор</label>
   <select id=baudsel onchange="document.getElementById('baud').value=this.value">
     <option value=9600>9600</option>
     <option value=19200>19200</option>
     <option value=38400>38400</option>
     <option value=57600>57600</option>
     <option value=115200>115200</option>
     <option value=125000 selected>125000 (наш ЭБУ)</option>
     <option value=230400>230400</option>
     <option value=250000>250000</option>
     <option value=500000>500000</option>
   </select>
 </div>
 <div class=fld>
   <label>или своё (бод)</label>
   <input class=baud id=baud value=125000>
 </div>
 <button class=start id=btnStart onclick=start()>&#9654; Старт</button>
 <button class=stop id=btnStop onclick=stop()>&#9632; Стоп</button>
</div>

<div id=banner class=off>остановлено</div>

<div class=stats>
 <div class=stat><b id=total>0</b><span>всего байт</span></div>
 <div class=stat><b id=rate>0</b><span>байт / сек</span></div>
 <div class=stat><b id=frames>0</b><span>кадров AE17</span></div>
 <div class=stat><b id=bad>0</b><span>битых кадров</span></div>
</div>

<div id=hexwrap>
 <div class=sub style="margin:0 0 6px">последние байты (hex &middot; ascii):</div>
 <pre id=hex>—</pre>
</div>

<div class=foot>
 <span>файл: <code id=file>—</code></span>
 <a class=dl id=dl href="/api/download">&#11015; Скачать лог</a>
</div>

<script>
async function loadPorts(){
 try{
  const r=await fetch('/api/ports'); const d=await r.json();
  const sel=document.getElementById('port'); sel.innerHTML='';
  if(!d.ports.length){ const o=document.createElement('option'); o.textContent='портов не найдено'; o.value=''; sel.appendChild(o); return; }
  d.ports.forEach(p=>{ const o=document.createElement('option'); o.value=p.device;
     o.textContent=p.device+(p.ftdi?'  (FTDI)':'')+(p.desc?'  — '+p.desc:''); sel.appendChild(o); });
  if(d.suggested) sel.value=d.suggested;
 }catch(e){}
}
async function start(){
 const port=document.getElementById('port').value;
 const baud=document.getElementById('baud').value;
 if(!port){ alert('Порт не выбран. Нажми «обновить порты».'); return; }
 const r=await fetch('/api/start',{method:'POST',headers:{'Content-Type':'application/json'},
     body:JSON.stringify({port,baud})});
 const d=await r.json(); if(!d.ok) alert('Не удалось: '+d.error);
}
async function stop(){ await fetch('/api/stop',{method:'POST'}); }
async function tick(){
 try{
  const r=await fetch('/api/status'); const d=await r.json();
  const b=document.getElementById('banner');
  if(d.error){ b.className='err'; b.textContent='ОШИБКА: '+d.error; }
  else if(d.running && d.rate>0){ b.className='live'; b.textContent='&#9679; ПОТОК ИДЁТ  ('+d.port+' @ '+d.baud+')'; }
  else if(d.running){ b.className='quiet'; b.textContent='ТИШИНА — порт открыт, байт нет  ('+d.port+')'; }
  else { b.className='off'; b.textContent='остановлено'; }
  document.getElementById('total').textContent=d.total;
  document.getElementById('rate').textContent=d.rate;
  document.getElementById('frames').textContent=d.frames;
  document.getElementById('bad').textContent=d.bad;
  document.getElementById('file').textContent=d.file_short||'—';
  document.getElementById('hex').textContent=d.hex||'—';
  document.getElementById('btnStart').disabled=d.running;
  document.getElementById('btnStop').disabled=!d.running;
 }catch(e){}
 setTimeout(tick,400);
}
loadPorts(); tick();
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/status"):
            self._json(snapshot()); return
        if self.path.startswith("/api/ports"):
            ports, suggested = list_ports()
            self._json({"ports": ports, "suggested": suggested}); return
        if self.path.startswith("/api/download"):
            with LOCK:
                fn = STATE["file"]
            if fn and os.path.exists(fn):
                data = open(fn, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition",
                                 f'attachment; filename="{os.path.basename(fn)}"')
                self.send_header("Content-Length", str(len(data)))
                self.end_headers(); self.wfile.write(data)
            else:
                self.send_response(404); self.end_headers()
            return
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(ln) if ln else b"{}"
        try:
            data = json.loads(raw or b"{}")
        except Exception:
            data = {}
        if self.path.startswith("/api/start"):
            ok, err = do_start(data.get("port", ""), data.get("baud", 125000))
            self._json({"ok": ok, "error": err}); return
        if self.path.startswith("/api/stop"):
            do_stop(); self._json({"ok": True}); return
        self._json({"ok": False, "error": "unknown"}, 404)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--http", type=int, default=8009)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", args.http), H)
    print(f"Панель логгера:  http://localhost:{args.http}")
    print("Открой в браузере, выбери порт, жми Старт. Ctrl+C — выход.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        do_stop()
        print("\nОстановлено.")


if __name__ == "__main__":
    main()
