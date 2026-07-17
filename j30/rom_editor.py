#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Редактор ДАННЫХ прошивки J30 — веб-тул.
  - Правит  j30/J30_редактирование.bin  (создаётся копией оригинала при первом старте).
  - Сравнивает с j30/HN27C256G@DIP28.BIN (оригинал), значения оригинала — красным.
  - Выводит ВСЕ данные: где смысл знаем — интерпретированно и подписано;
    где не знаем — сырьём (байты), помечено «ХЗ, у.е., править можно».
  - Кнопка СОХРАНИТЬ сверху (пишет .bin + пересчитывает контрольную сумму 0x7F7A/0x7F7B).

ЗАПУСК:   python3 "j30/rom_editor.py"
          открыть http://localhost:8011
"""
import os, json, http.server, socketserver, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, "HN27C256G@DIP28.BIN")
EDIT = os.path.join(HERE, "J30_редактирование.bin")
PORT = 8011

# ---- байты ----
def load():
    orig = bytearray(open(ORIG, "rb").read())
    if not os.path.exists(EDIT):
        open(EDIT, "wb").write(bytes(orig))
    edit = bytearray(open(EDIT, "rb").read())
    return orig, edit

def recalc_checksum(b):
    s = x = 0
    for i in range(len(b)):
        if i in (0x7F7A, 0x7F7B):
            continue
        s = (s + b[i]) & 0xFF; x ^= b[i]
    b[0x7F7A] = s; b[0x7F7B] = x

# ---- интерпретации (to = байт->физика, frm = физика->байт) ----
def afr_to(x):  return round(1881.6 / ((x - 64) if x >= 128 else (x + 128)), 1)
def afr_frm(v):
    v = float(v)
    if v >= 14.55: return None  # стехиометрия: не трогаем флаг, оставить как есть
    Xo = round(1881.6 / v - 128)
    if 0 <= Xo <= 127: return Xo
    return max(128, min(255, round(64 + 1881.6 / v)))

CONV = {
    # name: (подпись_ед, to(byte)->phys, frm(phys)->byte или None если только сырьё)
    "raw":     ("у.е.",   lambda x: x,               lambda v: int(v)),
    "deg":     ("град",   lambda x: x if x < 90 else ("флаг %d" % x),
                          lambda v: int(v) if str(v).lstrip('-').isdigit() else None),
    "afr":     ("AFR",    afr_to,                    afr_frm),
    "rpm50":   ("об/мин", lambda x: x * 50,          lambda v: round(int(v) / 50)),
    "cutrpm":  ("об/мин", lambda x: round(x * 25.6148), lambda v: max(0, min(255, round(float(v) / 25.6148)))),
    "idlref":  ("об/мин", lambda x: round(x * 12.807),  lambda v: max(0, min(255, round(float(v) / 12.807)))),
    "tp125":   ("TP%",    lambda x: round(x * 0.125, 2), lambda v: round(float(v) / 0.125)),
    "temp":    ("°C",     lambda x: x - 50,          lambda v: int(v) + 50),
    "idlerpm": ("об/мин", lambda x: round((64 + x) * 7.2), lambda v: max(0, min(255, round(int(v) / 7.2 - 64)))),
    "vq16":    ("у.е.16", None, None),   # 16-бит пары, показываем/правим числом
}

# ---- ОПРЕДЕЛЕНИЯ ДАННЫХ (что знаем по реверсу). kind: scalar|row|map16|vq16|raw ----
# unknown=True → «ХЗ что это, но править можно». cols только для map16 (16).
DEFS = [
 # --- КОД: байт ХХ ---
 {"a":0x34B4,"len":1,"kind":"scalar","conv":"idlerpm","name":"Тёплая база ХХ (байт в коде)","note":"(64+X)×7.2; сток 0x40=922, 0x2F=799"},
 # --- Структурный блок ---
 {"a":0x7300,"len":0x180,"kind":"raw","conv":"raw","name":"Структурный блок / Consult","unknown":True,"note":"у M30 тут Gear Fuel Map; у J30 — блок-указатели, править ОСТОРОЖНО"},
 # --- ГЛАВНЫЕ КАРТЫ ---
 {"a":0x7C00,"len":256,"kind":"map16","conv":"deg","name":"КАРТА УОЗ (Primary Timing)","rax":0x7B20,"cax":0x7B10,"note":"градусы; ≥128=флаг"},
 {"a":0x7D00,"len":256,"kind":"map16","conv":"afr","name":"КАРТА ТОПЛИВА (Primary Fuel)","rax":0x7B00,"cax":0x7AF0,"note":"AFR; 0xC0=14.7"},
 # --- ДМРВ / датчики ---
 {"a":0x7A70,"len":128,"kind":"vq16","conv":"vq16","name":"VQ / ДМРВ (MAF Translation)","note":"64т 16-бит; = M30"},
 {"a":0x7B30,"len":32,"kind":"row","conv":"temp","name":"Тарировка ТОЖ (термистор)","note":"°C=X-50; = M30"},
 # --- ОСИ ---
 {"a":0x7AF0,"len":16,"kind":"row","conv":"tp125","name":"Ось TP — топливо"},
 {"a":0x7B00,"len":16,"kind":"row","conv":"rpm50","name":"Ось RPM — топливо"},
 {"a":0x7B10,"len":16,"kind":"row","conv":"tp125","name":"Ось TP — зажигание"},
 {"a":0x7B20,"len":16,"kind":"row","conv":"rpm50","name":"Ось RPM — зажигание"},
 {"a":0x7BA0,"len":8,"kind":"row","conv":"raw","name":"Closed Loop — ось нагрузки (8т)","note":"замкнутый цикл: 5 6 7 8 32 64 250 251"},
 {"a":0x7BA8,"len":8,"kind":"row","conv":"rpm50","name":"Closed Loop — ось RPM (8т)","note":"×50: 450..4000"},
 # --- DWELL ---
 {"a":0x7B50,"len":16,"kind":"row","conv":"raw","name":"Ign Dwell по напряжению (батарея)","note":"X*100/256 %"},
 {"a":0x7B60,"len":16,"kind":"row","conv":"raw","name":"Ign Dwell по RPM","note":"0.33*X %"},
 # --- ТОПЛИВНЫЕ доп ---
 {"a":0x7600,"len":16,"kind":"row","conv":"raw","name":"AlphaN Increase Fuel (vs RPM)","note":"у J30 = 255 (выключено)"},
 {"a":0x7E90,"len":16,"kind":"row","conv":"raw","name":"Max Load / TTP Max (vs RPM)","note":"потолок нагрузки; 106..135"},
 {"a":0x7E80,"len":16,"kind":"row","conv":"raw","name":"TTP Min? (0x7E80)","unknown":True},
 # --- ОБОГАЩЕНИЕ (по темп) ---
 {"a":0x7E00,"len":16,"kind":"row","conv":"raw","name":"After start enrich / прогревочная надбавка ХХ (vs темп)","note":"надбавка к базе ХХ; холод(лево)=высоко(59), тает по after-start таймеру"},
 {"a":0x7E20,"len":16,"kind":"row","conv":"raw","name":"Crank Enrich (пусковое обогащение vs темп)","note":"мс; холод=96 → тепло=6"},
 {"a":0x7EB0,"len":16,"kind":"row","conv":"raw","name":"Temperature Enrich Warm (vs темп)","note":"%; холод=43→0"},
 {"a":0x7F30,"len":16,"kind":"row","conv":"raw","name":"Temperature Enrich (vs темп)","note":"%; прогревочное обогащение"},
 # --- ОТСЕЧКА ТОПЛИВА (накат) ---
 {"a":0x7E30,"len":16,"kind":"row","conv":"cutrpm","name":"Накат: порог ОТСЕЧКИ, В ДВИЖЕНИИ","note":"выше этих об на сбросе газа топливо режется. байт×25.6. код 0x8c95"},
 {"a":0x7E40,"len":16,"kind":"row","conv":"cutrpm","name":"Накат: порог ВОЗВРАТА, В ДВИЖЕНИИ","note":"ниже этих об топливо возвращается. байт×25.6. код 0x8c22"},
 # --- ЗАЖИГАНИЕ доп (градусы) ---
 {"a":0x76F0,"len":16,"kind":"row","conv":"deg","name":"Idle/Decel Timing (УОЗ ХХ/наката vs RPM)","note":"град BDTC"},
 {"a":0x7EA0,"len":16,"kind":"row","conv":"deg","name":"Idle/Decel Neutral Timing (vs RPM)","note":"град BDTC, нейтраль"},
 {"a":0x7F60,"len":16,"kind":"row","conv":"deg","name":"Warmup timing (прогревочный УОЗ vs RPM)","note":"град BDTC"},
 {"a":0x7E50,"len":16,"kind":"row","conv":"deg","name":"Crank Advance (пусковой УОЗ vs темп)","note":"град BDTC; 22→16"},
 {"a":0x7EC0,"len":16,"kind":"row","conv":"deg","name":"After start Timing Adv (vs темп)","note":"град BDTC; 30→0"},
 {"a":0x75B0,"len":16,"kind":"row","conv":"raw","name":"0x75B0 (у M30 — After start Timing Retard)","unknown":True,"note":"в коде J30 НЕ читается (0 ссылок) + все 255 → функция НЕ подтверждена для J30"},
 # --- ХОЛОСТОЙ ---
 {"a":0x7E60,"len":16,"kind":"row","conv":"idlref","name":"Опорные об/мин ХХ — стабилизация ИСКРОЙ (не главный рычаг)","note":"байт×12.8. сравнивается с фактич. оборотами → поправка УОЗ ($1519). держит ХХ углом, ход слабый. главный рычаг ХХ = база 0x34B4. код 0xa5bf→$154E→$143F→b61b"},
 # --- ЛИМИТ-ТАБЛИЦЫ ---
 {"a":0x7F40,"len":16,"kind":"row","conv":"cutrpm","name":"Накат: порог ОТСЕЧКИ, СТОЯ/НЕЙТРАЛЬ","note":"НЕ рев-лимит! выше этих об топливо режется. байт×25.6. у тебя ВСЕГДА активна (нет датчика скор.). код 0x8c18"},
 {"a":0x7F50,"len":16,"kind":"row","conv":"cutrpm","name":"Накат: порог ВОЗВРАТА, СТОЯ/НЕЙТРАЛЬ","note":"НЕ рев-лимит! ниже этих об топливо возвращается. байт×25.6. у тебя ВСЕГДА активна. код 0x8c3c"},
 {"a":0x7960,"len":16,"kind":"row","conv":"raw","name":"Air Flow Limiter","note":"обычно 255=выкл"},
 # --- ДЕТОНАЦИЯ (у J30 датчика НЕТ) ---
 {"a":0x79E3,"len":9,"kind":"row","conv":"raw","name":"Knock Retard Limit Primary (3x3)","note":"детонация; у J30 датчика нет (=0)"},
 {"a":0x7FE0,"len":9,"kind":"row","conv":"raw","name":"Knock Retard Limit Knock (3x3)","note":"детонация; у J30 датчика нет"},
 # --- СКАЛЯРЫ ---
 {"a":0x7FB4,"len":1,"kind":"scalar","conv":"rpm50","name":"ОТСЕЧКА (Rev Limiter)","note":"byte×50; 125=6250"},
 {"a":0x7F2B,"len":2,"kind":"scalar16","conv":"vq16","name":"Injector K (константа форсунок, 16-бит)","note":"сток=345 (у Z31 607 — другие форсунки); больше=больше топлива"},
 {"a":0x7F88,"len":1,"kind":"scalar","conv":"raw","name":"Injector Latency (задержка форсунки)","note":"сток=75 ≈ 0.75 мс (×0.01)"},
 {"a":0x7F91,"len":1,"kind":"scalar","conv":"temp","name":"O2 закрытый цикл — порог темп ОЖ","note":"°C=raw−50; сток 10°C. выше = закрытый цикл вкл (код 966b). в 205°C = петля отключена"},
 {"a":0x7F92,"len":1,"kind":"scalar","conv":"raw","name":"O2 Rich Voltage (богатая граница)","note":"X*0.01 В"},
 {"a":0x7F93,"len":1,"kind":"scalar","conv":"raw","name":"O2 Lean Voltage (бедная граница)","note":"X*0.01 В"},
 {"a":0x7FA5,"len":1,"kind":"scalar","conv":"raw","name":"Top Speed Limit (по скорости)","note":"код 0x8b6c: работает только если $1407(скорость)≠0 → у тебя МЁРТВ (нет датчика)"},
 {"a":0x7FB8,"len":2,"kind":"scalar16","conv":"vq16","name":"Timing retard factor (16-бит)","note":"сток=0x0133=307; физ≈raw/256=1.199"},
 {"a":0x7FC8,"len":1,"kind":"scalar","conv":"raw","name":"Коэф. скорость→обороты (флаг движения/крейсер)","note":"код 0x9ad6: (скорость $1407 × K)/8 сравнивается с оборотами → ставит флаг $53 (едешь/стоишь), который переключает таблицы наката и УОЗ"},
 {"a":0x7FD4,"len":1,"kind":"scalar","conv":"temp","name":"Warmup timing temp min","note":"°C=X-50"},
 {"a":0x7FD5,"len":1,"kind":"scalar","conv":"temp","name":"Warmup timing temp max","note":"°C=X-50"},
 {"a":0x7FD6,"len":1,"kind":"scalar","conv":"raw","name":"Warmup timing Load max"},
 {"a":0x7FD7,"len":1,"kind":"scalar","conv":"rpm50","name":"Warmup timing RPM max","note":"×50"},
 {"a":0x7FDA,"len":1,"kind":"scalar","conv":"raw","name":"Knock Load Index 1"},
 {"a":0x7FDB,"len":1,"kind":"scalar","conv":"raw","name":"Knock Load Index 2"},
 {"a":0x7FDC,"len":1,"kind":"scalar","conv":"rpm50","name":"Knock RPM Index 1","note":"×50"},
 {"a":0x7FDD,"len":1,"kind":"scalar","conv":"rpm50","name":"Knock RPM Index 2","note":"×50"},
 {"a":0x7F15,"len":5,"kind":"row","conv":"raw","name":"DTC Filters 1-5 (маски кодов ошибок)","note":"битовые маски: галка=код вкл; F0/C0/B0/20/00"},
 # --- КОНТРОЛЬНАЯ СУММА ---
 {"a":0x7F7A,"len":2,"kind":"raw","conv":"raw","name":"КОНТРОЛЬНАЯ СУММА (SUM/XOR)","note":"НЕ править — пересчитывается при сохранении","locked":True},
]

def build_layout(orig, edit):
    """Собрать список секций: известные DEFS + сырьё на непокрытые куски 0x6A00-0x7FFF."""
    covered = [False] * 0x10000
    items = []
    for d in sorted(DEFS, key=lambda z: z["a"]):
        for i in range(d["a"], d["a"] + d["len"]):
            covered[i] = True
        items.append(dict(d))
    # непокрытые байты в зоне данных 0x6A00-0x7FFF -> сырьё строками по 16
    lo, hi = 0x6A00, 0x8000
    i = lo
    while i < hi:
        if covered[i]:
            i += 1; continue
        j = i
        while j < hi and not covered[j]:
            j += 1
        # разбить на строки по 16
        a = i
        while a < j:
            ln = min(16, j - a)
            items.append({"a": a, "len": ln, "kind": "raw", "conv": "raw",
                          "name": "ХЗ что это (данные 0x%04X)" % a, "unknown": True,
                          "note": "у.е., править можно"})
            a += ln
        i = j
    items.sort(key=lambda z: z["a"])
    return items

def item_values(it, buf):
    """Значения секции: список {raw, phys} для каждого байта/точки."""
    a, ln, conv = it["a"], it["len"], it["conv"]
    out = []
    if conv == "vq16":
        for k in range(0, ln, 2):
            v = (buf[a + k] << 8) | buf[a + k + 1]
            out.append({"raw": v, "phys": v, "editable16": True})
        return out
    c = CONV.get(conv, CONV["raw"])
    for k in range(ln):
        raw = buf[a + k]
        phys = c[1](raw) if c[1] else raw
        out.append({"raw": raw, "phys": phys})
    return out

def api_data():
    orig, edit = load()
    layout = build_layout(orig, edit)
    res = []
    for it in layout:
        unit = CONV.get(it["conv"], CONV["raw"])[0]
        res.append({
            "addr": "0x%04X" % it["a"], "a": it["a"], "len": it["len"],
            "name": it["name"], "kind": it["kind"], "conv": it["conv"], "unit": unit,
            "unknown": it.get("unknown", False), "locked": it.get("locked", False),
            "note": it.get("note", ""), "cols": 16 if it["kind"] == "map16" else it["len"],
            "edit": item_values(it, edit), "orig": item_values(it, orig),
        })
    return {"items": res, "edit_file": os.path.basename(EDIT), "orig_file": os.path.basename(ORIG)}

def api_save(edits):
    """edits: [{a, k, raw}] — записать сырые байты, пересчитать чек-сумму."""
    orig, edit = load()
    for e in edits:
        a = int(e["a"]); k = int(e["k"]); raw = int(e["raw"]) & 0xFF
        edit[a + k] = raw
    recalc_checksum(edit)
    open(EDIT, "wb").write(bytes(edit))
    return {"ok": True, "chk": "0x%02X/0x%02X" % (edit[0x7F7A], edit[0x7F7B])}

# ---- HTTP ----
class H(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self._send(200, HTML, "text/html")
        elif self.path == "/api/data":
            self._send(200, json.dumps(api_data(), ensure_ascii=False))
        else:
            self._send(404, "{}")
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        if self.path == "/api/save":
            self._send(200, json.dumps(api_save(data.get("edits", [])), ensure_ascii=False))
        else:
            self._send(404, "{}")
    def log_message(self, *a): pass

HTML = r"""<!doctype html><html lang=ru><head><meta charset=utf-8>
<title>Редактор данных прошивки J30</title>
<style>
 body{font:13px/1.4 monospace;margin:0;background:#111;color:#ddd}
 header{position:sticky;top:0;background:#1b1b1b;border-bottom:1px solid #333;padding:8px 12px;display:flex;gap:16px;align-items:center;z-index:10}
 h1{font-size:15px;margin:0}
 button{font:13px monospace;padding:6px 14px;background:#2a6;color:#fff;border:0;border-radius:4px;cursor:pointer}
 button:hover{background:#3b7}
 label{cursor:pointer;user-select:none}
 #status{color:#8c8;margin-left:auto}
 .sec{border-top:1px solid #262626;padding:6px 12px}
 .sec h3{font-size:13px;margin:4px 0;color:#9cf}
 .sec.unk h3{color:#c96}
 .note{color:#777;font-size:11px}
 .grid{display:flex;flex-wrap:wrap;gap:2px;margin-top:3px}
 .cell{width:52px;text-align:center}
 .cell input{width:48px;background:#1e1e1e;color:#dfe;border:1px solid #333;text-align:center;font:12px monospace;padding:2px 0}
 .cell input:focus{border-color:#2a6;outline:0}
 .cell input.chg{background:#243;border-color:#2a6}
 .cell .o{color:#e55;font-size:10px;height:12px;display:none}
 body.cmp .cell .o{display:block}
 .map{border-collapse:collapse;margin-top:3px}
 .map td{border:1px solid #262626;padding:0}
 .map .ax{background:#181818;color:#8ac;font-size:10px;text-align:center;padding:2px 3px}
 .locked input{opacity:.5;pointer-events:none}
</style></head><body>
<header>
 <button id=save>💾 СОХРАНИТЬ</button>
 <h1>Редактор данных J30</h1>
 <label><input type=checkbox id=cmp> Сравнить с оригиналом (<span style=color:#e55>красным</span>)</label>
 <span id=status></span>
</header>
<div id=app>загрузка…</div>
<script>
let DATA=null, CH={};  // CH: "a:k" -> raw
const q=(s,e=document)=>e.querySelector(s);
function unitLabel(it){ return it.unknown ? (it.conv=='raw'?'у.е. (ХЗ)':it.unit) : it.unit; }
function cellHtml(it,k,ev,ov){
  const key=it.a+':'+k, lk=it.locked?' locked':'';
  const val = it.conv=='vq16'||it.conv=='raw'||typeof ev.phys!=='number' ? ev.phys : ev.phys;
  return `<div class="cell${lk}"><input data-a=${it.a} data-k=${k} data-conv="${it.conv}" value="${val}">`+
         `<div class=o>${ov.phys}</div></div>`;
}
function render(){
  const app=q('#app'); app.innerHTML='';
  for(const it of DATA.items){
    const sec=document.createElement('div'); sec.className='sec'+(it.unknown?' unk':'')+(it.locked?' locked':'');
    let h=`<h3>${it.addr} · ${it.name} <span class=note>[${it.kind}, ${unitLabel(it)}]${it.note?' — '+it.note:''}</span></h3>`;
    if(it.kind=='map16'){
      h+='<table class=map><tr><td class=ax>об\\TP</td>';
      // столбцы-ось
      for(let c=0;c<16;c++){ const cav=it.cax; h+=`<td class=ax id=cax_${it.a}_${c}></td>`; }
      h+='</tr>';
      for(let r=0;r<16;r++){
        h+=`<tr><td class=ax id=rax_${it.a}_${r}></td>`;
        for(let c=0;c<16;c++){ const k=r*16+c; h+='<td>'+cellHtml(it,k,it.edit[k],it.orig[k])+'</td>'; }
        h+='</tr>';
      }
      h+='</table>';
    } else {
      h+='<div class=grid>';
      for(let k=0;k<it.edit.length;k++) h+=cellHtml(it,k,it.edit[k],it.orig[k]);
      h+='</div>';
    }
    sec.innerHTML=h; app.appendChild(sec);
  }
  // заполнить оси карт (значения из соответствующих row-секций, если есть в DATA)
  for(const it of DATA.items){ if(it.kind!='map16')continue;
    const rax=DATA.items.find(z=>z.a==it.rax), cax=DATA.items.find(z=>z.a==it.cax);
    for(let c=0;c<16;c++){const el=q('#cax_'+it.a+'_'+c); if(el)el.textContent=cax?cax.edit[c].phys:c;}
    for(let r=0;r<16;r++){const el=q('#rax_'+it.a+'_'+r); if(el)el.textContent=rax?rax.edit[r].phys:r;}
  }
  bind();
}
function bind(){
  document.querySelectorAll('#app input').forEach(inp=>{
    inp.addEventListener('input',()=>{
      const a=+inp.dataset.a,k=+inp.dataset.k,conv=inp.dataset.conv;
      const raw=physToRaw(conv,inp.value);
      if(raw===null){inp.classList.remove('chg');delete CH[a+':'+k];return;}
      CH[a+':'+k]=raw; inp.classList.add('chg');
      q('#status').textContent=Object.keys(CH).length+' правок (не сохранено)';
    });
  });
}
// physТо->raw byte (инверсия). null = не менять (напр. стехиометрия/невалидно)
function physToRaw(conv,v){
  v=(''+v).trim(); if(v==='')return null;
  const f={
    raw:x=>Math.max(0,Math.min(255,parseInt(x)||0)),
    deg:x=>/^-?\d+$/.test(x)?Math.max(0,Math.min(255,+x)):null,
    rpm50:x=>Math.max(0,Math.min(255,Math.round((+x)/50))),
    tp125:x=>Math.max(0,Math.min(255,Math.round((+x)/0.125))),
    temp:x=>Math.max(0,Math.min(255,(+x)+50)),
    idlerpm:x=>Math.max(0,Math.min(255,Math.round((+x)/7.2-64))),
    afr:x=>{const val=+x; if(val>=14.55)return null; let Xo=Math.round(1881.6/val-128); if(Xo>=0&&Xo<=127)return Xo; return Math.max(128,Math.min(255,Math.round(64+1881.6/val)));},
    vq16:x=>null, // 16-бит правим отдельно (пока сырьём числом — сохраняем как есть)
  }[conv]||(x=>Math.max(0,Math.min(255,parseInt(x)||0)));
  const r=f(v); return (r===null||isNaN(r))?null:r;
}
q('#cmp').addEventListener('change',e=>document.body.classList.toggle('cmp',e.target.checked));
q('#save').addEventListener('click',async()=>{
  const edits=[]; for(const key in CH){const[a,k]=key.split(':');edits.push({a:+a,k:+k,raw:CH[key]});}
  if(!edits.length){q('#status').textContent='нет правок';return;}
  q('#status').textContent='сохраняю…';
  const r=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({edits})});
  const j=await r.json(); CH={};
  await loadData(); q('#status').textContent='СОХРАНЕНО ✓ (чек-сумма '+j.chk+')';
});
async function loadData(){DATA=await(await fetch('/api/data')).json();render();}
loadData();
</script></body></html>"""

if __name__ == "__main__":
    orig, edit = load()
    print("Оригинал: %s" % ORIG)
    print("Правка:   %s (создан=%s)" % (EDIT, not os.path.exists(EDIT)))
    print("Открой:   http://localhost:%d" % PORT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), H) as httpd:
        httpd.serve_forever()
