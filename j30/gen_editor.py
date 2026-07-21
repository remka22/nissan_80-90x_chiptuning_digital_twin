# -*- coding: utf-8 -*-
# Генератор автономной веб-страницы редактора данных J30 (всё в браузере).
import os, sys, base64, json
sys.path.insert(0, "/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS/j30")
import rom_editor as RE

ROOT = "/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS"
orig = bytearray(open(RE.ORIG, "rb").read())
layout = RE.build_layout(orig, orig)

# ось (шкала X) по адресу таблицы: чем индексируется значение
AXIS = {
  0x7600:"rpm6000", 0x75B0:"rpm6000", 0x7E90:"rpm6000", 0x7E80:"rpm6000",
  0x76F0:"rpm3000", 0x7EA0:"rpm3000", 0x7F60:"rpm3000",
  0x7E00:"temp", 0x7E20:"temp", 0x7EB0:"temp", 0x7F30:"temp",
  0x7E30:"temp", 0x7E40:"temp", 0x7E50:"temp", 0x7EC0:"temp",
  0x7E60:"temp", 0x7F40:"temp", 0x7F50:"temp",
  0x7BA8:"clrpm", 0x7BA0:"idx8",
  0x79E3:"knock3", 0x7FE0:"knock3",
  0x79A0:"ld8x2", 0x79B0:"ld8x2", 0x79C0:"ld8x2", 0x79D0:"ld8x2",
}

items = []
for it in layout:
    unit = RE.CONV.get(it["conv"], RE.CONV["raw"])[0]
    items.append({
        "a": it["a"], "len": it["len"], "kind": it["kind"], "conv": it["conv"],
        "name": it["name"], "unit": unit, "unknown": it.get("unknown", False),
        "locked": it.get("locked", False), "note": it.get("note", ""),
        "rax": it.get("rax"), "cax": it.get("cax"),
        "axis": AXIS.get(it["a"], ""), "dead": it.get("dead", False),
    })
rom_b64 = base64.b64encode(bytes(orig)).decode()

INJ_GUIDE = """
<h4>КАК ЗАМЕНИТЬ ФОРСУНКИ НА ДРУГИЕ</h4>

<h4>ШАГ 1. Найти ОТНОШЕНИЕ</h4>
<code>ОТНОШЕНИЕ = поток старых ÷ поток новых</code><br>
Взять производительность старых и новых форсунок (cc/min из паспорта, или граммы за одинаковый пролив) и поделить одно на другое. Запомнить это число — оно нужно в шагах 2 и 3.

<h4>ШАГ 2. K (0x7F2B)</h4>
Вписать: <code>K_старое × ОТНОШЕНИЕ</code>. K_старое — что стоит сейчас (сток 345).

<h4>ШАГ 3. Пусковое (0x7E20)</h4>
Выделить всю строку протягиванием мыши → кнопка «× умножить» внизу → ввести ОТНОШЕНИЕ → нажать.

<h4>ШАГ 4. Задержка база (0x7F88)</h4>
Вписать мёртвое время новых форсунок из их паспорта. Сток 75 = 0.75 мс, то есть 0.90 мс = 90.

<h4>ШАГ 5. Наклон (0x7F87)</h4>
Не трогать.

<h4>ШАГ 6. Сохранить и довести по ШДК</h4>
Сохранить дамп → залить → снять лог ШДК на прогретом. По логу подправить:<br>
• смесь врёт РАВНОМЕРНО везде → K (0x7F2B)<br>
• врёт только на ХХ → задержка (0x7F88)<br>
• врёт на пуске / первые секунды → пусковое (0x7E20)

<hr>
<h4>Условия и оговорки</h4>
• Поток старых и новых мерить при ОДНОМ давлении топлива. Разные регуляторы → поток ∝ √(давление).<br>
• Проливка точнее паспорта: обе форсунки в одну рампу на один провод, открыть одновременно, лить 30-60 с, взвесить. Пролей весь комплект — увидишь разброс и износ.<br>
• Если СТАРЫЕ изношены (льют меньше паспорта) — в отношение бери ПАСПОРТ старых, не замеренное.<br>
• ШДК мерить в ОТКРЫТОЙ петле, замкнутый цикл скрывает ошибку (0x7F91=205°C отключает; у тебя уже отключена).<br>
• Нет данных по мёртвому времени новых → оставить 75, добить по ШДК.<br>
• Меньше K сдвигает рабочую точку по картам влево (Tp = ось нагрузки) — иногда после больших форсунок карту слегка подправляют.<br>
• Очень большие форсунки → короткий импульс на ХХ, ниже линейного диапазона форсунки → неровный ХХ, прошивкой не лечится (физика).<br>
• Сопротивление форсунок (низко/высокоомные): другой тип = резисторы/драйвер, это железо.<br>
• «мс» у задержки/пускового — оценка из M30, из кода J30 точный масштаб не выведен; на пропорции не влияет.
"""

# подразделы известных данных (порядок = порядок вывода)
GROUPS = [
  ("🗺 Главные карты", [0x7C00, 0x7D00]),
  ("🔥 Зажигание (УОЗ)", [0x76F0, 0x7EA0, 0x7F60, 0x7E50, 0x7EC0, 0x7FB8, 0x7FD4, 0x7FD5, 0x7FD6, 0x7FD7]),
  ("⛽ Топливо / смесь", [0x7600, 0x7E00, 0x7EB0, 0x7F30, 0x7BA0, 0x7BA8, 0x7F91, 0x7F92, 0x7F93]),
  ("🚫 Отсечка топлива на накате", [0x7E30, 0x7E40, 0x7F40, 0x7F50]),
  ("🌀 Холостой ход", [0x34B4, 0x7E60]),
  ("📊 ДМРВ / датчики / оси", [0x7A70, 0x7B30, 0x7AF0, 0x7B00, 0x7B10, 0x7B20, 0x7B50, 0x7B60]),
  ("🎛 Сглаживание оси нагрузки (k фильтра расхода)", [0x79A0, 0x79B0, 0x79C0, 0x79D0]),
  ("💉 Форсунки / впрыск (менять при замене форсунок)", [0x7F2B, 0x7E20, 0x7F88, 0x7F87], INJ_GUIDE),
  ("⛔ Лимиты (обороты / скорость / нагрузка)", [0x7FB4, 0x7FA5, 0x7960, 0x7E90, 0x7E80]),
  ("💥 Детонация — у J30 датчика НЕТ", [0x79E3, 0x7FE0, 0x7FDA, 0x7FDB, 0x7FDC, 0x7FDD]),
  ("🩺 Диагностика (DTC)", [0x7F15]),
  ("⚙ Прочие скаляры", [0x7FC8]),
  ("🔒 Контрольная сумма", [0x7F7A]),
]

HTML = r"""<!doctype html><html lang=ru><head><meta charset=utf-8>
<title>Редактор данных прошивки J30</title>
<style>
 body{font:13px/1.4 monospace;margin:0;background:#111;color:#ddd}
 header{position:sticky;top:0;background:#1b1b1b;border-bottom:1px solid #333;padding:8px 12px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;z-index:10}
 h1{font-size:15px;margin:0;color:#9cf}
 button{font:13px monospace;padding:6px 14px;background:#2a6;color:#fff;border:0;border-radius:4px;cursor:pointer}
 button:hover{background:#3b7}
 input.fn{background:#1e1e1e;color:#dfe;border:1px solid #333;font:13px monospace;padding:5px 8px;width:230px}
 label{cursor:pointer;user-select:none}
 #status{color:#8c8;margin-left:auto}
 .filebtn{background:#357}
 .group{font-size:17px;font-weight:bold;padding:14px 14px 8px;margin:26px 0 6px;border-bottom:2px solid #3a3a3a;color:#6cf;position:sticky;top:46px;background:#111;z-index:6}
 .group.unk{color:#e93}
 .sub{font-size:15px;font-weight:bold;padding:10px 14px 5px;margin:22px 10px 2px;color:#8e8;border-bottom:1px solid #2a3a2a;background:#141414}
 .sec{border:1px solid #2c2c2c;border-radius:7px;padding:10px 14px 12px;margin:14px 14px;background:#171717;overflow-x:auto}
 .sec h3{font-size:13px;margin:0 0 6px;color:#9cf}
 .sec.dead{opacity:.55}
 .sec.dead:hover{opacity:1}
 .deadbadge{background:#622;color:#fbb;font-size:10px;padding:1px 6px;border-radius:3px;margin-left:6px;vertical-align:middle}
 .sec.unk{border-color:#4a3a1a;background:#1a1712}
 .sec.unk h3{color:#c96}
 .note{color:#777;font-size:11px}
 .grid{display:flex;flex-wrap:wrap;gap:2px;margin-top:3px}
 .cell{width:56px;text-align:center}
 .cell input{width:52px;background:#1e1e1e;color:#dfe;border:1px solid #333;text-align:center;font:12px monospace;padding:2px 0}
 .cell input:focus{border-color:#2a6;outline:0}
 body.cmp .cell input.diff{color:#f66;border-color:#c44;font-weight:bold}
 .cell input.adj{background:#5a4a10;border-color:#db4}
 .cell .o{font-size:10px;height:12px;display:none;color:#ddd}
 body.cmp .cell .o{display:block}
 .t1d{border-collapse:collapse;margin-top:4px}
 .t1d td{border:1px solid #262626;padding:1px}
 .t1d .ax{background:#181818;color:#8ac;font-size:10px;text-align:center;padding:2px 4px;white-space:nowrap}
 .t1d .axl{background:#141414;color:#678;font-size:9px;text-align:right;padding:2px 6px;white-space:nowrap}
 .map{border-collapse:collapse;margin-top:3px}
 .map td{border:1px solid #262626;padding:0}
 .map .ax{background:#181818;color:#8ac;font-size:10px;text-align:center;padding:2px 4px}
 .locked input{opacity:.5;pointer-events:none}
 .hint{color:#666;padding:4px 12px;font-size:11px}
 .coll{color:#9a9;padding:5px 2px;font-size:12px}
 .coll b{color:#dfe;font-size:13px}
 button.exp{background:#444;padding:2px 10px;font-size:11px;margin-top:5px;margin-left:8px}
 button.exp:hover{background:#555}
 details.guide{margin:2px 14px 10px;border:1px solid #2c3a4a;border-radius:6px;background:#131a21}
 details.guide summary{cursor:pointer;padding:8px 12px;color:#7cf;font-weight:bold;user-select:none;font-size:12px}
 details.guide .guidebody{padding:2px 16px 12px;color:#cdd;font-size:12px;line-height:1.55}
 .guidebody h4{color:#9cf;margin:11px 0 3px;font-size:13px}
 .guidebody code{background:#0e1620;color:#8fe;padding:1px 5px;border-radius:3px}
 .guidebody table{border-collapse:collapse;margin:5px 0}
 .guidebody td{border:1px solid #2c3a4a;padding:2px 9px}
 .calc{margin:2px 14px 12px;border:1px solid #3a4a2c;border-radius:6px;background:#171a13;padding:11px 14px;font-size:13px;line-height:2}
 .calc b{color:#bf6;font-size:13px}
 .calc .ci{width:74px;background:#0e1608;color:#efe;border:1px solid #3a4a2c;padding:5px 6px;font:13px monospace;text-align:center;margin:0 3px}
 .calc button{margin-top:9px;background:#5a2;padding:7px 14px}
 .calc button:hover{background:#6b3}
 .calcnote{color:#787;font-size:11px;line-height:1.4;margin-top:7px}
 .cell input.sel{outline:2px solid #6cf;outline-offset:-1px;background:#10202c}
 body.nosel{user-select:none}
 button.secrev{display:none;font-size:10px;padding:2px 9px;background:#357;margin-left:8px;vertical-align:middle}
 body.cmp button.secrev{display:inline-block}
 button.secrev:hover{background:#468}
 button.gtgl{font-size:10px;padding:2px 9px;background:#425;margin-left:8px;vertical-align:middle}
 button.gtgl:hover{background:#547}
 .chart{margin-top:5px}
 .chart svg{display:block;max-width:100%;height:auto}
 .chartlbl{color:#789;font-size:10px;margin-top:3px}
 #refname{color:#89a;font-size:11px;cursor:pointer}
 #bulk{display:none;position:fixed;bottom:0;left:0;right:0;background:#17222e;border-top:2px solid #38506a;padding:9px 16px;gap:12px;align-items:center;z-index:30;font-size:13px}
 #bulk input{background:#0e1620;color:#dfe;border:1px solid #38506a;padding:6px 9px;width:130px;font:13px monospace}
 #bulk button{padding:6px 12px}
 #bulk .clr{background:#653}
 /* ===== СВЕТЛАЯ ТЕМА (для солнца) ===== */
 body.light{background:#f4f4f4;color:#1a1a1a}
 body.light header{background:#e7e7e7;border-bottom:1px solid #bbb}
 body.light h1{color:#046}
 body.light input.fn{background:#fff;color:#012;border:1px solid #aaa}
 body.light #status{color:#161}
 body.light .group{color:#025;background:#f4f4f4;border-bottom:2px solid #99b}
 body.light .group.unk{color:#a40}
 body.light .sub{color:#141;background:#e6efe6;border-bottom:1px solid #9c9}
 body.light .sec{border:1px solid #bbb;background:#fff}
 body.light .sec h3{color:#036}
 body.light .sec.unk{border-color:#c8a35a;background:#fbf4e6}
 body.light .sec.unk h3{color:#864}
 body.light .note{color:#555}
 body.light .cell input{background:#fff;color:#012;border:1px solid #aaa}
 body.light .cell input:focus{border-color:#2a6}
 body.light.cmp .cell input.diff{color:#c00;border-color:#c00}
 body.light .cell input.adj{background:#ffe9a6;border-color:#c90}
 body.light .cell .o{color:#333}
 body.light .cell input.sel{outline:2px solid #06c;background:#dce9ff}
 body.light .t1d td,body.light .map td{border:1px solid #bbb}
 body.light .t1d .ax,body.light .map .ax{background:#eef;color:#036}
 body.light .t1d .axl{background:#e6e6e6;color:#345}
 body.light .hint,body.light .chartlbl{color:#666}
 body.light .coll{color:#363}
 body.light .coll b{color:#012}
 body.light .chart svg{background:#fff !important;border:1px solid #ccc}
 body.light details.guide{background:#eef3f8;border-color:#9bc}
 body.light details.guide summary{color:#046}
 body.light .guidebody{color:#233}
 body.light .guidebody h4{color:#046}
 body.light .guidebody code{background:#dde8f2;color:#036}
 body.light .guidebody td{border-color:#9bc}
 body.light .calc{background:#eef6e6;border-color:#9c7}
 body.light .calc b{color:#150}
 body.light .calc .ci{background:#fff;color:#012;border:1px solid #9c7}
 body.light .calcnote{color:#576}
 body.light #refname{color:#357}
 body.light #bulk{background:#dde8f2;border-top:2px solid #8ab}
 body.light #bulk input{background:#fff;color:#012;border:1px solid #8ab}
</style></head><body>
<header>
 <h1>Редактор данных J30</h1>
 <button id=theme style=background:#557>☀ Светлая</button>
 <input class=fn id=fname value="J30_редактирование">
 <button id=save>💾 Сохранить дамп</button>
 <label class=filebtn style="padding:6px 12px;border-radius:4px">📂 Загрузить дамп<input type=file id=load accept=".bin" style=display:none></label>
 <button id=reset style=background:#845>↩ Сброс к оригиналу</button>
 <label><input type=checkbox id=cmp> Сравнить (<span style=color:#e55>красным</span>) с эталоном</label>
 <label class=filebtn style="padding:6px 12px;border-radius:4px">📎 Эталон<input type=file id=reff accept=".bin" style=display:none></label>
 <span id=refname title="клик — вернуть эталон = сток">эталон: сток</span>
 <label><input type=checkbox id=rawm> Сырые байты (0-255)</label>
 <label><input type=checkbox id=heat checked> 🌡 Заливка карт</label>
 <span id=status></span>
</header>
<div class=hint>Оригинал (сток) вшит в страницу. По умолчанию сравнение со стоком; «📎 Эталон» — сравнить с выбранным .bin (клик по «эталон: …» вернёт сток). У каждой ячейки кнопка ↺ — свести к эталону. Протяни мышью по ячейкам → массовое изменение снизу. «Сохранить дамп» пересчитывает чек-сумму.</div>
<div id=app>загрузка…</div>
<div id=bulk>
 <span>Выделено <b id=bulkn>0</b> яч.:</span>
 <input id=bulkv placeholder="значение / коэф">
 <button id=bulkapply>Применить ко всем</button>
 <button id=bulkmul>× умножить</button>
 <button id=bulkrev class=clr>↺ Свести к эталону</button>
 <button id=bulkclr class=clr>Снять выделение</button>
</div>
<script>
const ITEMS=__ITEMS__;
const GROUPS=__GROUPS__;
const INJ_CALC=`<div class=calc>
<b>🔧 Пересчёт под новые форсунки</b> — введи что знаешь, нажми кнопку:<br>
Поток/вес СТАРЫХ <input id=calcold class=ci placeholder="напр 270"> ÷ НОВЫХ <input id=calcnew class=ci placeholder="напр 370"> &nbsp;(cc/min или граммы пролива — под ОДНИМ давлением, за ОДНО время)<br>
Задержка новых форсунок при ~14В, мс <input id=calclat class=ci value="0.75"><br>
<button id=calcgo>⚙ ЗАМЕНИТЬ ФОРСУНКИ — пересчитать K + пусковое + задержку</button>
<div class=calcnote>Считает от СТОКА × отношение (старые÷новые). Жать можно повторно — не накапливается. Наклон 0x7F87 не трогается. После — проверь значения ниже и сохрани дамп.</div>
</div>`;
const ROM_ORIG=Uint8Array.from(atob("__ROM__"),c=>c.charCodeAt(0));
let ROM=ROM_ORIG.slice();      // редактируемая копия
let REF=ROM_ORIG.slice();      // эталон сравнения (по умолчанию = сток, можно загрузить файл)
const CHK=[0x7F7A,0x7F7B];
const EXPANDED=new Set();       // адреса свёрнутых секций, которые раскрыли вручную
let RAWMODE=false;              // показывать/править сырые байты 0..255 вместо интерпретации
// граф-вид: у неизвестных вкл по умолчанию, НО только если есть разброс (константы оставляем свёрнутыми)
let HEATMAP=true;               // тепловая заливка ячеек карт 16x16 по значению
function heat(v,mn,mx){const t=(mx>mn)?(v-mn)/(mx-mn):0.5;return 'hsl('+Math.round((1-t)*230)+',68%,60%)';}
const GRAPHED=new Set(ITEMS.filter(i=>{
  if(!i.unknown||i.len<3)return false;
  for(let k=1;k<i.len;k++)if(ROM[i.a+k]!=ROM[i.a])return true;
  return false;
}).map(i=>i.a));
// секция однородна (все байты равны)? возвращает значение или null
function allSame(it){
  if(it.kind=='map16'||it.conv=='vq16')return null;
  if(it.len<3)return null;
  const v0=ROM[it.a];
  for(let k=1;k<it.len;k++)if(ROM[it.a+k]!=v0)return null;
  return v0;
}

// ---- интерпретации байт->физика ----
function rawToPhys(conv,x){switch(conv){
  case 'deg': return x<90?x:('флаг '+x);
  case 'afr': return Math.round((1881.6/((x>=128)?(x-64):(x+128)))*10)/10;
  case 'rpm50': return x*50;
  case 'lat01': return Math.round(x*0.01*100)/100;
  case 'msraw': return x;
  case 'volt': return Math.round(x*0.0195*100)/100;
  case 'cutrpm': return Math.round(x*25.6148);
  case 'idlref': return Math.round(x*12.807);
  case 'tp125': return Math.round(x*0.125*100)/100;
  case 'temp': return x-50;
  case 'idlerpm': return Math.round((64+x)*7.2);
  default: return x;
}}
// физика->байт (null = не менять)
function physToRaw(conv,v){v=(''+v).trim();if(v==='')return null;
  switch(conv){
   case 'deg': return /^-?\d+$/.test(v)?clamp(+v):null;
   case 'afr':{const val=+v;if(isNaN(val)||val<=0)return null;let Xo=Math.round(1881.6/val-128);if(Xo>=0&&Xo<=127)return Xo;return Math.max(128,Math.min(255,Math.round(64+1881.6/val)));}
   case 'rpm50': return clamp(Math.round(+v/50));
   case 'lat01': return clamp(Math.round(+v/0.01));
   case 'msraw': return clamp(Math.round(+v));
   case 'volt': return clamp(Math.round(+v/0.0195));
   case 'cutrpm': return clamp(Math.round(+v/25.6148));
   case 'idlref': return clamp(Math.round(+v/12.807));
   case 'tp125': return clamp(Math.round(+v/0.125));
   case 'temp': return clamp((+v)+50);
   case 'idlerpm': return clamp(Math.round(+v/7.2-64));
   default: return clamp(parseInt(v));
  }}
function clamp(x){x=x|0;return isNaN(x)?null:Math.max(0,Math.min(255,x));}
const byName=a=>ITEMS.find(z=>z.a==a);
function unitLabel(it){return it.unknown?(it.conv=='raw'?'у.е. (ХЗ)':it.unit):it.unit;}

function cellVal(it,k,rom){ // отображаемое значение
  if(it.conv=='vq16'){const off=it.a+k*2;return (rom[off]<<8)|rom[off+1];}
  return rawToPhys(it.conv,rom[it.a+k]);
}
function cellCount(it){return it.conv=='vq16'?it.len/2:it.len;}

function curDisplay(a,k,conv){ // что реально лежит в ROM, в физ.виде
  if(conv=='vq16'){const o=a+k*2;return (ROM[o]<<8)|ROM[o+1];}
  return rawToPhys(conv,ROM[a+k]);
}
function diffAK(a,k,conv){ // байт(ы) отличаются от ЭТАЛОНА?
  if(conv=='vq16'){const o=a+k*2;return ROM[o]!=REF[o]||ROM[o+1]!=REF[o+1];}
  return ROM[a+k]!=REF[a+k];
}
function cellHtml(it,k,heatStyle){
  const lk=it.locked?' locked':'';
  const raw = RAWMODE && it.conv!='vq16';        // сырой режим (кроме 16-бит пар)
  const cv = raw ? 'raw' : it.conv;              // конверсия для правки
  const ev = raw ? ROM[it.a+k] : cellVal(it,k,ROM);
  const ov = raw ? REF[it.a+k] : cellVal(it,k,REF);
  const dc = diffAK(it.a,k,it.conv)?' diff':'';
  const ttl = raw ? ` title="= ${cellVal(it,k,ROM)} ${unitLabel(it)}"` : '';
  const hs = heatStyle ? ` style="${heatStyle}"` : '';
  return `<div class="cell${lk}"><input${hs} class="${dc}" data-a=${it.a} data-k=${k} data-conv="${cv}"${ttl} value="${ev}">`+
         `<div class="o">${ov}</div></div>`;
}
const AX={
  temp:['-40','-30','-20','-10','0','10','20','30','40','50','60','70','80','90','100','110'],
  rpm6000:['0','400','800','1200','1600','2000','2400','2800','3200','3600','4000','4400','4800','5200','5600','6000'],
  rpm3000:['0','200','400','600','800','1000','1200','1400','1600','1800','2000','2200','2400','2600','2800','3000'],
  clrpm:['450','500','550','600','700','800','2000','4000'],
  idx8:['0','1','2','3','4','5','6','7'],
  ld8x2:['0','8','16','24','32','40','48','56','0','8','16','24','32','40','48','56'],
};
function axCap(a){return {temp:'темп ОЖ °C',rpm6000:'об/мин',rpm3000:'об/мин',clrpm:'об/мин',idx8:'индекс',ld8x2:'нагрузка $14A2 (2 подтабл. по 8)'}[a]||'ось';}
function bodyHtml(it){
  if(it.axis=='knock3'){ // 3x3: столбцы=нагрузка, строки=обороты
    const L=['0','29','80'],R=['0','1600','3600'];
    let h='<table class=t1d><tr><td class=axl>об\\наг</td>';
    for(const l of L)h+=`<td class=ax>${l}</td>`;h+='</tr>';
    for(let r=0;r<3;r++){h+=`<tr><td class=ax>${R[r]}</td>`;
      for(let c=0;c<3;c++)h+='<td>'+cellHtml(it,r*3+c)+'</td>';h+='</tr>';}
    return h+'</table>';
  }
  const lbls=AX[it.axis];
  if(lbls){
    let h='<table class=t1d><tr><td class=axl>'+axCap(it.axis)+'</td>';
    for(let k=0;k<cellCount(it);k++)h+=`<td class=ax>${lbls[k]!==undefined?lbls[k]:k}</td>`;
    h+='</tr><tr><td class=axl>знач</td>';
    for(let k=0;k<cellCount(it);k++)h+='<td>'+cellHtml(it,k)+'</td>';
    return h+'</tr></table>';
  }
  let h='<div class=grid>';for(let k=0;k<cellCount(it);k++)h+=cellHtml(it,k);return h+'</div>';
}
function cnum(it,k,rom){let v=cellVal(it,k,rom);return (typeof v=='number'&&isFinite(v))?v:rom[it.a+k];}
function chartHtml(it){ // ломаная по значениям (текущие + эталон пунктиром)
  const n=cellCount(it), cur=[],ref=[];
  for(let k=0;k<n;k++){cur.push(cnum(it,k,ROM));ref.push(cnum(it,k,REF));}
  let mn=Math.min(...cur,...ref), mx=Math.max(...cur,...ref); if(mn===mx){mn-=1;mx+=1;}
  const W=Math.max(300,n*20), H=130, pad=8;
  const X=k=> (n<2?W/2:pad+k*(W-2*pad)/(n-1));
  const Y=v=> H-pad-(v-mn)*(H-2*pad)/(mx-mn);
  const pts=arr=>arr.map((v,k)=>X(k).toFixed(1)+','+Y(v).toFixed(1)).join(' ');
  let svg='<svg viewBox="0 0 '+W+' '+H+'" width='+W+' height='+H+' style="background:#141414;border:1px solid #2a2a2a;border-radius:4px">';
  svg+='<polyline fill=none stroke="#a55" stroke-width=1 stroke-dasharray="3,3" points="'+pts(ref)+'"/>';
  svg+='<polyline fill=none stroke="#6cf" stroke-width=1.5 points="'+pts(cur)+'"/>';
  for(let k=0;k<n;k++)svg+='<circle cx='+X(k).toFixed(1)+' cy='+Y(cur[k]).toFixed(1)+' r=2 fill="#6cf"/>';
  svg+='</svg>';
  const lbls=AX[it.axis];
  let foot='макс '+(Math.round(mx*100)/100)+' · мин '+(Math.round(mn*100)/100)+' '+unitLabel(it);
  foot += lbls ? (' · ось: '+lbls[0]+'…'+lbls[Math.min(lbls.length,n)-1]+' '+axCap(it.axis)) : ' · ось: индекс 0…'+(n-1)+' (неизвестна)';
  return '<div class=chart>'+svg+'<div class=chartlbl>'+foot+' — <b style="color:#6cf">синее</b> текущее, <span style="color:#a55">красный пунктир</span> эталон</div></div>';
}
function secHtml(it){
  const A='0x'+it.a.toString(16).toUpperCase().padStart(4,'0');
  const graphable = it.kind!='map16' && cellCount(it)>=3;
  const graphed = graphable && GRAPHED.has(it.a);
  const secrev=it.locked?'':`<button class=secrev data-a=${it.a} data-len=${it.len} title="сбросить всю эту таблицу к эталону">↺ к эталону</button>`;
  const grph=graphable?`<button class=gtgl data-a=${it.a}>${graphed?'🔢 числа':'📈 график'}</button>`:'';
  const deadb=it.dead?`<span class=deadbadge title="на этой машине не влияет">💀 МЁРТВ</span>`:'';
  let h=`<h3>${A} · ${it.name}${deadb} <span class=note>[${it.kind}, ${unitLabel(it)}]${it.note?' — '+it.note:''}</span>${grph}${secrev}</h3>`;
  if(it.kind=='map16'){
    const rax=byName(it.rax),cax=byName(it.cax);
    let mn=0,mx=1;
    if(HEATMAP){const vs=[];for(let j=0;j<256;j++)vs.push(cnum(it,j,ROM));mn=Math.min(...vs);mx=Math.max(...vs);}
    h+='<table class=map><tr><td class=ax>об\\нагр</td>';
    for(let c=0;c<16;c++)h+=`<td class=ax>${cax?cellVal(cax,c,ROM):c}</td>`;
    h+='</tr>';
    for(let r=0;r<16;r++){h+=`<tr><td class=ax>${rax?cellVal(rax,r,ROM):r}</td>`;
      for(let c=0;c<16;c++){const hs=HEATMAP?('background:'+heat(cnum(it,r*16+c,ROM),mn,mx)+';color:#111'):'';h+='<td>'+cellHtml(it,r*16+c,hs)+'</td>';}h+='</tr>';}
    h+='</table>';
  }else if(graphed){
    h+=chartHtml(it);
  }else{
    const same=allSame(it);
    if(same!==null && it.unknown && !EXPANDED.has(it.a)){
      const axn=it.axis?' (ось: '+axCap(it.axis)+')':'';
      h+=`<div class=coll>${cellCount(it)} байт, все = <b>${rawToPhys(it.conv,same)}</b> ${unitLabel(it)}${axn}<button class=exp data-a=${it.a}>развернуть</button></div>`;
    }else{
      h+=bodyHtml(it);
      if(same!==null)h+=`<button class=exp data-a=${it.a}>свернуть</button>`;
    }
  }
  return `<div class="sec${it.unknown?' unk':''}${it.locked?' locked':''}${it.dead?' dead':''}">${h}</div>`;
}
function render(){
  const app=document.getElementById('app');
  const known=ITEMS.filter(i=>!i.unknown), unk=ITEMS.filter(i=>i.unknown);
  const byA={}; for(const i of known) byA[i.a]=i;
  let html='<div class=group>✅ ИЗВЕСТНЫЕ ДАННЫЕ ('+known.length+') — смысл известен, подписано</div>';
  const used=new Set();
  for(const g of GROUPS){
    const title=g[0], addrs=g[1], info=g[2];
    const its=addrs.map(a=>byA[a]).filter(Boolean);
    if(!its.length)continue;
    html+='<div class=sub>'+title+' ('+its.length+')</div>';
    if(info)html+='<details class=guide><summary>📖 Инструкция по замене форсунок — нажми чтобы раскрыть</summary><div class=guidebody>'+info+'</div></details>'+INJ_CALC;
    for(const it of its){html+=secHtml(it);used.add(it.a);}
  }
  const rest=known.filter(i=>!used.has(i.a));
  if(rest.length){html+='<div class=sub>📦 Прочее известное ('+rest.length+')</div>';for(const it of rest)html+=secHtml(it);}
  html+='<div class="group unk">❓ НЕИЗВЕСТНЫЕ ДАННЫЕ ('+unk.length+') — ХЗ что это, у.е., но править можно</div>';
  for(const it of unk) html+=secHtml(it);
  app.innerHTML=html;
  document.querySelectorAll('#app .cell input').forEach(inp=>{
    inp.addEventListener('input',()=>{
      const a=+inp.dataset.a,k=+inp.dataset.k,conv=inp.dataset.conv;
      if(conv=='vq16'){const val=parseInt(inp.value)||0,off=a+k*2;ROM[off]=(val>>8)&0xFF;ROM[off+1]=val&0xFF;inp.classList.toggle('diff',diffAK(a,k,conv));mark();return;}
      const raw=physToRaw(conv,inp.value);
      if(raw===null)return;
      ROM[a+k]=raw;inp.classList.toggle('diff',diffAK(a,k,conv));mark();
    });
    // snap-back: по уходу с поля показать РЕАЛЬНОЕ значение из ROM; мигнуть если зажалось/округлилось
    inp.addEventListener('change',()=>{
      const a=+inp.dataset.a,k=+inp.dataset.k,conv=inp.dataset.conv;
      const typed=inp.value.trim();
      const real=''+curDisplay(a,k,conv);
      inp.value=real;
      const dt=parseFloat(typed), dr=parseFloat(real);
      if(typed!=='' && !isNaN(dt) && !isNaN(dr) && Math.abs(dt-dr)>0.05){
        inp.classList.add('adj'); setTimeout(()=>inp.classList.remove('adj'),1200);
      }
    });
  });
  document.querySelectorAll('#app button.exp').forEach(b=>{
    b.addEventListener('click',()=>{const a=+b.dataset.a;EXPANDED.has(a)?EXPANDED.delete(a):EXPANDED.add(a);render();});
  });
  document.querySelectorAll('#app button.secrev').forEach(b=>{
    b.addEventListener('click',()=>{
      const a=+b.dataset.a,len=+b.dataset.len;
      for(let i=0;i<len;i++)ROM[a+i]=REF[a+i];
      mark();render();
    });
  });
  document.querySelectorAll('#app button.gtgl').forEach(b=>{
    b.addEventListener('click',()=>{const a=+b.dataset.a;GRAPHED.has(a)?GRAPHED.delete(a):GRAPHED.add(a);render();});
  });
  const cg=document.getElementById('calcgo');
  if(cg)cg.addEventListener('click',()=>{
    const o=parseFloat(document.getElementById('calcold').value), n=parseFloat(document.getElementById('calcnew').value), lat=parseFloat(document.getElementById('calclat').value);
    if(!(o>0)||!(n>0)){alert('Введи поток/вес старых И новых форсунок');return;}
    const r=o/n;
    let K=Math.max(0,Math.min(65535,Math.round(((ROM_ORIG[0x7F2B]<<8)|ROM_ORIG[0x7F2C])*r)));
    ROM[0x7F2B]=(K>>8)&255; ROM[0x7F2C]=K&255;
    for(let i=0;i<16;i++) ROM[0x7E20+i]=Math.max(0,Math.min(255,Math.round(ROM_ORIG[0x7E20+i]*r)));
    if(lat>0) ROM[0x7F88]=Math.max(0,Math.min(255,Math.round(lat*100)));
    mark();
    document.getElementById('status').textContent='форсунки пересчитаны: отношение '+r.toFixed(3)+' → K='+K+', задержка байт '+ROM[0x7F88];
    render();
  });
}
let dirty=false;
function mark(){dirty=true;document.getElementById('status').textContent='есть правки (не скачано)';}
document.getElementById('cmp').addEventListener('change',e=>document.body.classList.toggle('cmp',e.target.checked));
document.getElementById('rawm').addEventListener('change',e=>{RAWMODE=e.target.checked;render();});
document.getElementById('heat').addEventListener('change',e=>{HEATMAP=e.target.checked;render();});
// эталон = выбранный файл
document.getElementById('reff').addEventListener('change',e=>{
  const f=e.target.files[0];if(!f)return;const rd=new FileReader();
  rd.onload=()=>{const u=new Uint8Array(rd.result);if(u.length!=ROM_ORIG.length){alert('Размер эталона не 32768!');return;}
    REF=u.slice();document.getElementById('refname').textContent='эталон: '+f.name;render();};
  rd.readAsArrayBuffer(f);
});
document.getElementById('refname').addEventListener('click',()=>{REF=ROM_ORIG.slice();document.getElementById('refname').textContent='эталон: сток';render();});

// ---- множественное выделение протягиванием мышью ----
let selCells=new Set(), dragAnchor=null, dragging=false;
function clearSel(){selCells.forEach(i=>i.classList.remove('sel'));selCells.clear();document.getElementById('bulk').style.display='none';}
function addSel(inp){if(inp&&!selCells.has(inp)){inp.classList.add('sel');selCells.add(inp);}}
function showBulk(){if(selCells.size>1){document.getElementById('bulkn').textContent=selCells.size;document.getElementById('bulk').style.display='flex';}else clearSel();}
const appEl=document.getElementById('app');
appEl.addEventListener('mousedown',e=>{const inp=e.target.closest('.cell input');if(!inp)return;dragAnchor=inp;dragging=false;clearSel();});
appEl.addEventListener('mouseover',e=>{const inp=e.target.closest('.cell input');if(!inp)return;
  if(e.buttons===1&&dragAnchor){if(!dragging){dragging=true;document.body.classList.add('nosel');dragAnchor.blur();addSel(dragAnchor);}addSel(inp);}});
document.addEventListener('mouseup',()=>{if(dragging)showBulk();dragging=false;dragAnchor=null;document.body.classList.remove('nosel');});
document.getElementById('bulkapply').addEventListener('click',()=>{
  const v=document.getElementById('bulkv').value;
  selCells.forEach(inp=>{const a=+inp.dataset.a,k=+inp.dataset.k,conv=inp.dataset.conv;
    if(conv=='vq16'){const val=parseInt(v);if(!isNaN(val)){const o=a+k*2;ROM[o]=(val>>8)&255;ROM[o+1]=val&255;}return;}
    const raw=physToRaw(conv,v);if(raw!==null)ROM[a+k]=raw;});
  mark();clearSel();render();
});
document.getElementById('bulkmul').addEventListener('click',()=>{
  const f=parseFloat(document.getElementById('bulkv').value);
  if(isNaN(f))return;
  selCells.forEach(inp=>{const a=+inp.dataset.a,k=+inp.dataset.k,conv=inp.dataset.conv;
    if(conv=='vq16'){const o=a+k*2;let v=Math.max(0,Math.min(65535,Math.round(((ROM[o]<<8)|ROM[o+1])*f)));ROM[o]=(v>>8)&255;ROM[o+1]=v&255;return;}
    ROM[a+k]=Math.max(0,Math.min(255,Math.round(ROM[a+k]*f)));});
  mark();clearSel();render();
});
document.getElementById('bulkrev').addEventListener('click',()=>{
  selCells.forEach(inp=>{const a=+inp.dataset.a,k=+inp.dataset.k,conv=inp.dataset.conv;
    if(conv=='vq16'){const o=a+k*2;ROM[o]=REF[o];ROM[o+1]=REF[o+1];}else ROM[a+k]=REF[a+k];});
  mark();clearSel();render();
});
document.getElementById('bulkclr').addEventListener('click',clearSel);

function recalcChecksum(){let s=0,x=0;for(let i=0;i<ROM.length;i++){if(i==0x7F7A||i==0x7F7B)continue;s=(s+ROM[i])&0xFF;x^=ROM[i];}ROM[0x7F7A]=s;ROM[0x7F7B]=x;}
function ts(){const d=new Date();const p=n=>(''+n).padStart(2,'0');return d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+'_'+p(d.getHours())+p(d.getMinutes());}
document.getElementById('save').addEventListener('click',()=>{
  recalcChecksum();
  const name=(document.getElementById('fname').value.trim()||'J30_редактирование')+'_'+ts()+'.bin';
  const blob=new Blob([ROM],{type:'application/octet-stream'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();
  document.getElementById('status').textContent='скачано: '+name+' (чек-сумма 0x'+ROM[0x7F7A].toString(16)+'/0x'+ROM[0x7F7B].toString(16)+')';dirty=false;
  render(); // обновить (чек-сумма изменилась)
});
document.getElementById('load').addEventListener('change',e=>{
  const f=e.target.files[0];if(!f)return;const rd=new FileReader();
  rd.onload=()=>{const u=new Uint8Array(rd.result);if(u.length!=ROM_ORIG.length){alert('Размер не 32768!');return;}ROM=u.slice();
    let s=0,x=0;for(let i=0;i<ROM.length;i++){if(i==0x7F7A||i==0x7F7B)continue;s=(s+ROM[i])&0xFF;x^=ROM[i];}
    const ok=(ROM[0x7F7A]==s&&ROM[0x7F7B]==x);render();
    document.getElementById('status').textContent='загружен: '+f.name+' — чек-сумма '+(ok?'✓ СХОДИТСЯ':'✗ НЕ СХОДИТСЯ (файл правленый или битый)');};
  rd.readAsArrayBuffer(f);
});
document.getElementById('reset').addEventListener('click',()=>{if(confirm('Сбросить все правки к оригиналу?')){ROM=ROM_ORIG.slice();render();document.getElementById('status').textContent='сброшено к оригиналу';}});
document.getElementById('theme').addEventListener('click',e=>{
  const light=document.body.classList.toggle('light');
  e.target.textContent=light?'🌙 Тёмная':'☀ Светлая';
  try{localStorage.setItem('j30theme',light?'light':'dark');}catch(_){}
});
try{if(localStorage.getItem('j30theme')=='light'){document.body.classList.add('light');document.getElementById('theme').textContent='🌙 Тёмная';}}catch(_){}
render();
</script></body></html>"""

HTML = HTML.replace("__ITEMS__", json.dumps(items, ensure_ascii=False)).replace("__ROM__", rom_b64).replace("__GROUPS__", json.dumps(GROUPS, ensure_ascii=False))
out = os.path.join(ROOT, "j30", "J30_редактор.html")
open(out, "w", encoding="utf-8").write(HTML)
print("OK:", out, "| размер", len(HTML), "| секций", len(items))
