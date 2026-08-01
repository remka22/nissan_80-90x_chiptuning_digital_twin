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
LABELS = [
    (0x140A, "Обороты",           16, "об/мин",          12.807),   # word × 12.807 (анкер рев-лимит 488=6250)
    (0x1431, "ALPHA (коррекция)",  8, "× (100=1.0)",      0.01),     # 100=нейтраль, окно 95-105 = ±5%
    (0x144E, "Впрыск факт",       16, "мс",               0.005),    # регистр HD63140 × 5мкс
    (0x1411, "Впрыск расчёт",     16, "тики 5мкс",        None),     # Tp×K+deadtime, сырьё
    (0x1482, "Нагрузка Tp (сгл.)", 8, "у.е.",             None),     # внутр. нагрузка, /8=TP только по XDF
    (0x1413, "Tp мгновенная",      8, "у.е.",             None),
    (0x1400, "O2 узкий",           8, "отсчёты АЦП",      None),     # НЕ вольты (пороги 75/21 отсчёта)
    (0x1408, "MAF (ch0)",         16, "сырьё АЦП 10б",    None),
    (0x008F, "Напряжение (ch1)",   8, "≈В (прикидка)",    0.08),     # анкер 175≈14В; точный масштаб код НЕ даёт
    (0x00B1, "Темп: индекс",       8, "индекс (>=холоднее)", None),  # НЕ °C
    (0x140C, "Темп: линеариз.",    8, "индекс",           None),     # уже через таблицу fb30, НЕ сырьё
    (0x004C, "Темп: сырьё АЦП",    8, "сырьё АЦП (ch2)",  None),     # ВОТ чистое сырьё температуры
    (0x1437, "ALPHA счётчик",      8, "у.е.",             None),
    (0x1402, "АЦП ch4",            8, "сырьё АЦП",        None),
    (0x1401, "АЦП ch5",            8, "сырьё АЦП",        None),
    (0x1583, "АЦП ch7",            8, "сырьё АЦП",        None),
    (0x1574, "АЦП ch8",            8, "сырьё АЦП",        None),
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
import glob


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
    f = None
    parser = Parser()
    while not stop_ev.is_set():
        try:
            chunk = ser.read(2048)
        except Exception as e:
            with LOCK: STATE["error"] = f"чтение: {e}"
            break
        if chunk:
            if f is None:
                os.makedirs(os.path.dirname(fname), exist_ok=True)
                f = open(fname, "ab")
            f.write(chunk); f.flush()
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
                        for k, b in enumerate(data):
                            STATE["ram"][addr + k] = b
                    else:
                        STATE["bad"] += 1
    try: ser.close()
    except Exception: pass
    if f: f.close()
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
</style></head><body>
<header><h1>&#128225; Панель логгера ЭБУ — что рассказывает блок</h1></header>
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
 <button class=stop id=btnStop onclick=stop()>&#9632; Стоп</button>
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
<div class=foot><a class=dl href="/api/download">&#11015; Скачать сырьё</a></div>
<script>
async function loadPorts(){
 try{const r=await fetch('/api/ports');const d=await r.json();
  const s=document.getElementById('port');s.innerHTML='';
  d.ports.forEach(p=>{const o=document.createElement('option');o.value=p.device;
    o.textContent=p.device+(p.ftdi?' (FTDI)':'');s.appendChild(o);});
  if(d.suggested)s.value=d.suggested;}catch(e){}
}
async function start(){const port=document.getElementById('port').value;const baud=document.getElementById('baud').value;
 if(!port){alert('Порт не выбран');return;}
 const r=await fetch('/api/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({port,baud})});
 const d=await r.json();if(!d.ok)alert('Не удалось: '+d.error);}
async function stop(){await fetch('/api/stop',{method:'POST'});}
function tick(){fetch('/api/status').then(r=>r.json()).then(d=>{
 const b=document.getElementById('banner');
 if(d.error){b.className='err';b.textContent='ОШИБКА: '+d.error;}
 else if(d.running&&d.rate>0){b.className='live';b.textContent='● ПОТОК ИДЁТ ('+d.port+' @ '+d.baud+')';}
 else if(d.running){b.className='quiet';b.textContent='порт открыт, байт нет';}
 else{b.className='off';b.textContent='остановлено';}
 document.getElementById('total').textContent=d.total;document.getElementById('rate').textContent=d.rate;
 document.getElementById('frames').textContent=d.frames;document.getElementById('bad').textContent=d.bad;
 document.getElementById('ramc').textContent=d.ram_count;document.getElementById('file').textContent=d.file_short||'—';
 let h='';for(const v of d.vars){h+='<tr><td>'+v.name+'</td><td class=a>'+v.addr+'</td>'+
   (v.val===null?'<td class=na>—</td>':'<td class=v>'+v.val+'</td>')+
   '<td class=u>'+v.unit+'</td>'+
   (v.real===null?'<td class=na>—</td>':'<td class=r>'+v.real+'</td>')+'</tr>';}
 document.getElementById('vars').innerHTML=h;
 document.getElementById('ram').textContent=(d.ram_lines&&d.ram_lines.length)?d.ram_lines.join('\n'):'— (ждём кадры)';
 document.getElementById('btnStart').disabled=d.running;document.getElementById('btnStop').disabled=!d.running;
}).catch(e=>{}).finally(()=>setTimeout(tick,400));}
loadPorts();tick();
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
            ports, sug = list_ports(); self._json({"ports": ports, "suggested": sug}); return
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
