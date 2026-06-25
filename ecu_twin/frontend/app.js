// Панель двойника ЭБУ: слайдеры -> /api/state -> гейджи/флаги/память.
let META = null;

async function api(path, body) {
  const opt = body ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) } : {};
  const r = await fetch(path, opt);
  if (!r.ok) throw new Error(path + ' -> ' + r.status);
  return r.json();
}
function el(tag, attrs = {}, kids = []) {
  const e = document.createElement(tag);
  for (const k in attrs) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
  for (const c of kids) e.appendChild(c);
  return e;
}

// диапазоны/дефолты слайдеров по имени входа
const RANGE = {
  RPM: [0, 7000, 50], RPM8: [0, 140, 1], MAF: [0, 600, 5], Load: [0, 255, 1],
  Coolant: [0, 255, 1], AirTemp: [0, 255, 1], TempIdx: [0, 15, 1],
};
const DEF = { RPM: 800, RPM8: 16, MAF: 80, Load: 0, Coolant: 130, AirTemp: 130, TempIdx: 8 };
const GMAX = { Airflow_1577: 5000, Load_1413: 600, Tp_1482: 600, MAF_1408: 600 };
const GAUGES = ['Airflow_1577', 'Load_1413', 'Tp_1482'];

const sliders = {};       // name -> input element

function buildSliders() {
  const box = document.getElementById('sliders');
  box.innerHTML = '';
  for (const [name, info] of Object.entries(META.inputs)) {
    const [mn, mx, st] = RANGE[name] || [0, 255, 1];
    const inp = el('input', { type: 'range', min: mn, max: mx, step: st, value: DEF[name] ?? 0 });
    inp.dataset.addr = info.addr; inp.dataset.size = info.size;
    const val = el('span', { class: 'val', text: DEF[name] ?? 0 });
    inp.addEventListener('input', () => { val.textContent = inp.value; scheduleUpdate(); });
    sliders[name] = inp;
    box.appendChild(el('div', { class: 'slider' }, [
      el('div', { class: 'top' }, [el('span', { class: 'name', text: name }), val]),
      inp,
    ]));
  }
}

function buildGauges() {
  const box = document.getElementById('gauges');
  box.innerHTML = '';
  for (const name of GAUGES) {
    const num = el('div', { class: 'num', text: '—' });
    const bar = el('i'); bar.style.width = '0%';
    const g = el('div', { class: 'gauge' }, [
      el('div', { class: 'label', text: name }), num,
      el('div', { class: 'bar' }, [bar]),
    ]);
    g.dataset.name = name; g._num = num; g._bar = bar;
    box.appendChild(g);
  }
}

function buildFlags() {
  const box = document.getElementById('flags');
  box.innerHTML = '';
  for (const name of Object.keys(META.flags)) {
    const led = el('span', { class: 'led' });
    const hex = el('span', { class: 'hex', text: '' });
    const f = el('div', { class: 'flag' }, [led, el('span', { text: name }), hex]);
    f._led = led; f._hex = hex; box.appendChild(f); f.dataset.name = name;
  }
}

function collectInputs() {
  return Object.values(sliders).map(inp => ({ addr: +inp.dataset.addr, size: +inp.dataset.size, value: +inp.value }));
}

let updTimer = null;
function scheduleUpdate() { clearTimeout(updTimer); updTimer = setTimeout(updateState, 120); }

async function updateState() {
  const req = { inputs: collectInputs(), iterations: +document.getElementById('iterations').value };
  try {
    const r = await api('/api/state', req);
    // гейджи
    for (const g of document.querySelectorAll('.gauge')) {
      const v = r.watch[g.dataset.name] ?? 0;
      g._num.textContent = v;
      g._bar.style.width = Math.min(100, 100 * v / (GMAX[g.dataset.name] || 255)) + '%';
    }
    // флаги
    for (const f of document.querySelectorAll('.flag')) {
      const st = r.flags[f.dataset.name];
      f._led.classList.toggle('on', !!(st && st.on));
      f._hex.textContent = st ? '0x' + st.byte.toString(16).toUpperCase() : '';
    }
    // таблица памяти
    const t = document.getElementById('watch-table');
    t.innerHTML = '';
    for (const [k, v] of Object.entries(r.watch)) {
      t.appendChild(el('tr', {}, [el('td', { text: k }), el('td', { text: v + '  (0x' + v.toString(16).toUpperCase() + ')' })]));
    }
    const crashed = Object.keys(r.chain.crashed || {}).length;
    document.getElementById('live-status').textContent =
      crashed ? ('⚠ сбой в рутине: ' + JSON.stringify(r.chain.crashed)) : '✓ цикл прогнан, все рутины вернулись';
  } catch (e) {
    document.getElementById('live-status').textContent = 'ошибка: ' + e.message;
  }
}

// ---------- свип ----------
function buildRoutineSel(sel) {
  sel.innerHTML = '';
  for (const [key, info] of Object.entries(META.routines))
    sel.appendChild(el('option', { value: info.addr, text: key }));
}
function buildVarSel(sel) {
  sel.innerHTML = '';
  for (const [name, info] of Object.entries(META.inputs))
    sel.appendChild(el('option', { value: name, text: name }));
  sel.value = 'MAF';
}
let swPicks;
function buildSwWatch() {
  const box = document.getElementById('sw-watch'); box.innerHTML = '';
  swPicks = {};
  for (const [name, info] of Object.entries(META.watch)) {
    const cb = el('input', { type: 'checkbox' }); cb.dataset.name = name; cb.dataset.addr = info.addr; cb.dataset.size = info.size;
    if (['Airflow_1577', 'Load_1413', 'Tp_1482'].includes(name)) cb.checked = true;
    swPicks[name] = cb;
    box.appendChild(el('label', {}, [cb, el('span', { text: name })]));
  }
}
async function doSweep() {
  const varName = document.getElementById('sw-var').value;
  const vinfo = META.inputs[varName];
  const watch = Object.values(swPicks).filter(c => c.checked).map(c => ({ name: c.dataset.name, addr: +c.dataset.addr, size: +c.dataset.size }));
  if (!watch.length) { alert('Отметь наблюдаемые'); return; }
  const base = collectInputs().filter(i => i.addr !== vinfo.addr);
  const req = {
    routine_addr: +document.getElementById('sw-routine').value,
    sweep_addr: vinfo.addr, sweep_size: vinfo.size,
    start: +document.getElementById('sw-start').value, stop: +document.getElementById('sw-stop').value,
    step: +document.getElementById('sw-step').value, inputs: base, watch, iterations: 10,
  };
  document.getElementById('status').textContent = 'свип…';
  const r = await api('/api/sweep', req);
  const xs = r.rows.map(x => x.sweep);
  const traces = watch.map(w => ({ x: xs, y: r.rows.map(x => x[w.name]), mode: 'lines+markers', name: w.name }));
  Plotly.newPlot('sweep-chart', traces, {
    paper_bgcolor: '#151a21', plot_bgcolor: '#0e1116', font: { color: '#aeb7c3' },
    margin: { t: 16, r: 10, b: 40, l: 50 }, xaxis: { title: varName, gridcolor: '#232a34' },
    yaxis: { gridcolor: '#232a34' }, legend: { orientation: 'h' },
  }, { displayModeBar: false });
  document.getElementById('status').textContent = 'свип готов: ' + r.count + ' точек';
}

// ---------------- ЖИВОЙ МОТОР ----------------
const EGAUGES = [
  // строка 1: Обороты · РХХ · Впрыск · AFR факт · AFR цель
  { key: 'rpm', label: 'Обороты (об/мин)', max: 8000 },
  { key: 'iacv_pct', label: 'РХХ (% открытия)', max: 100 },
  { key: 'fuel_mass', label: 'Топливо (масса)', max: 2600 },
  { key: 'afr', label: 'AFR ФАКТ (мотор)', max: 20 },
  { key: 'afr_target', label: 'AFR ЦЕЛЬ (блок)', max: 20 },
  // строка 2: Воздух · Зажигание · ТОЖ · ТВ
  { key: 'air_mass', label: 'Воздух (масса)', max: 38000 },
  { key: 'timing', label: 'Зажигание (° угол)', max: 50 },
  { key: 'coolant', label: 'Темп. ОЖ (ТОЖ), °C', max: 120 },
  { key: 'airtemp', label: 'Темп. воздуха (ТВ), °C', max: 80 },
];
const EDATA = [
  ['rpm', 'Обороты (RPM)'], ['idle_target', 'Цель ХХ (об/мин)'], ['idle_cmd', 'Уставка контура ($1411)'],
  ['airflow', 'Расход воздуха'], ['load', 'Нагрузка ($1413)'],
  ['fuel', 'Впрыск/топливо ($150C)'], ['tp', 'Tp застрявший ($1482)'],
  ['iacv', 'РХХ duty сырой ($004D)'], ['iacv_pct', 'РХХ % открытия'], ['timing', 'Угол зажигания ($1455), °'],
  ['coolant', 'Темп. ОЖ (°C)'],
  ['airtemp', 'Темп. воздуха ($1489)'], ['maf_raw', 'Сырьё MAF ($1408)'],
  ['solA7', 'Соленоиды A7'], ['solA9', 'Соленоиды A9'], ['solAB', 'Соленоиды AB'],
];
function buildEngine() {
  const box = document.getElementById('eng-gauges'); box.innerHTML = '';
  for (const g of EGAUGES) {
    const num = el('div', { class: 'num', text: '—' });
    const bar = el('i');
    const e = el('div', { class: 'egauge' }, [
      el('div', { class: 'label', text: g.label }), num, el('div', { class: 'bar' }, [bar]),
    ]);
    e._num = num; e._bar = bar; e.dataset.key = g.key; e.dataset.max = g.max;
    box.appendChild(e);
  }
}
let ignitionOn = false, starterHeld = false;   // ключ зажигания и стартер
let engBusy = false;
async function updateEngine() {
  if (engBusy) return;               // не наслаивать кадры
  engBusy = true;
  const gas = +document.getElementById('eng-load').value;
  const coolant = +document.getElementById('eng-cool').value;
  const airtemp = +document.getElementById('eng-air').value;
  const screw = +document.getElementById('eng-screw').value;
  try {
    const r = await api('/api/engine', { gas, coolant, airtemp, screw, ignition: ignitionOn, starter: starterHeld, ticks: 12 });
    const s = r.state;
    const rs = document.getElementById('eng-run-state');
    if (s.starter) rs.textContent = 'стартер крутит…';
    else if (s.running) rs.textContent = '● работает · ' + s.rpm + ' об/мин';
    else if (!s.ignition) rs.textContent = 'мотор заглушен (зажигание выкл)';
    else rs.textContent = 'зажигание вкл — крути стартер';
    rs.classList.toggle('live', !!s.running);
    document.getElementById('thr-idle-led').classList.toggle('on', !!s.idle_sw);  // концевик ХХ
    document.getElementById('thr-wot-led').classList.toggle('on', !!s.wot_sw);    // WOT
    for (const e of document.querySelectorAll('.egauge')) {
      if (!e._num) continue;             // ячейка огоньков цилиндров — без числа/бара
      const v = s[e.dataset.key] ?? 0;
      e._num.textContent = v;
      e._bar.style.width = Math.min(100, Math.max(0, 100 * v / (+e.dataset.max))) + '%';
    }
    // выходы (соленоиды)
    const ob = document.getElementById('eng-outputs'); ob.innerHTML = '';
    for (const [name, on] of Object.entries(r.outputs || {})) {
      const led = el('span', { class: 'led' + (on ? ' on' : '') });
      ob.appendChild(el('div', { class: 'flag' }, [led, el('span', { text: name })]));
    }
    // полная таблица данных
    const t = document.getElementById('eng-data'); t.innerHTML = '';
    for (const [k, label] of EDATA) {
      const v = s[k] ?? 0;
      t.appendChild(el('tr', {}, [el('td', { text: label }), el('td', { text: v + '  (0x' + v.toString(16).toUpperCase() + ')' })]));
    }
    document.getElementById('eng-status').textContent =
      '✓ мотор крутится · RPM ' + s.rpm + ' · газ ' + s.throttle + '% · цил ' + s.cyl;
  } catch (e) {
    document.getElementById('eng-status').textContent = 'ошибка: ' + e.message;
  } finally { engBusy = false; }
}

(async function () {
  try { META = await api('/api/meta'); }
  catch (e) { document.getElementById('status').textContent = 'нет связи с бэкендом: ' + e.message; return; }
  // живой мотор — крутится непрерывно
  buildEngine();
  const elo = document.getElementById('eng-load');
  elo.addEventListener('input', () => { document.getElementById('eng-load-val').textContent = elo.value + '%'; });
  const ec = document.getElementById('eng-cool'), ea = document.getElementById('eng-air');
  ec.addEventListener('input', () => { document.getElementById('eng-cool-val').textContent = ec.value + '°C'; });
  ea.addEventListener('input', () => { document.getElementById('eng-air-val').textContent = ea.value + '°C'; });
  const es = document.getElementById('eng-screw');
  es.addEventListener('input', () => { document.getElementById('eng-screw-val').textContent = es.value; });
  // ключ зажигания (тумблер) + стартер (держать)
  const ignBtn = document.getElementById('eng-ignition');
  ignBtn.addEventListener('click', () => {
    ignitionOn = !ignitionOn;
    ignBtn.textContent = '🔑 Зажигание: ' + (ignitionOn ? 'ВКЛ' : 'ВЫКЛ');
    ignBtn.classList.toggle('on', ignitionOn);
  });
  const startBtn = document.getElementById('eng-starter');
  const crankOn = (e) => { if (e) e.preventDefault(); starterHeld = true; };
  const crankOff = () => { starterHeld = false; };
  startBtn.addEventListener('mousedown', crankOn);
  startBtn.addEventListener('mouseup', crankOff);
  startBtn.addEventListener('mouseleave', crankOff);
  startBtn.addEventListener('touchstart', crankOn);
  startBtn.addEventListener('touchend', crankOff);
  setInterval(updateEngine, 250);   // кадр модели каждые 250 мс (мотор живёт сам)
  updateEngine();
  buildSliders(); buildGauges(); buildFlags();
  buildRoutineSel(document.getElementById('sw-routine'));
  buildVarSel(document.getElementById('sw-var'));
  buildSwWatch();
  document.getElementById('iterations').addEventListener('change', scheduleUpdate);
  document.getElementById('btn-sweep').addEventListener('click', doSweep);
  document.getElementById('status').textContent = 'готов · ROM base 0x' + META.rom_base.toString(16);
  updateState();   // первый прогон
})();
