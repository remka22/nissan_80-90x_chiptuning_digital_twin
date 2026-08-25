# -*- coding: utf-8 -*-
# Генератор автономной веб-страницы редактора данных J30 (всё в браузере).
import os, sys, base64, json
sys.path.insert(0, "/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS/j30")
import rom_editor as RE

ROOT = "/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS"
orig = bytearray(open(RE.ORIG, "rb").read())   # СТОК вшит; ДАД-карты появятся при «Загрузить дамп» боевого бина
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
  0x7910:"tps16", 0x7700:"tps16", 0x7720:"tps16",
}

items = []
for it in layout:
    unit = RE.CONV.get(it["conv"], RE.CONV["raw"])[0]
    items.append({
        "a": it["a"], "len": it["len"], "kind": it["kind"], "conv": it["conv"],
        "name": it["name"], "unit": unit, "unknown": it.get("unknown", False),
        "locked": it.get("locked", False), "note": it.get("note", ""),
        "rax": it.get("rax"), "cax": it.get("cax"), "own": it.get("own", False),
        "axis": AXIS.get(it["a"], ""), "dead": it.get("dead", False),
    })
rom_b64 = base64.b64encode(bytes(orig)).decode()

INJ_GUIDE = """
<h4>КАК ЗАМЕНИТЬ ФОРСУНКИ НА ДРУГИЕ</h4>
Ввести производительность новых форсунок в калькуляторе ниже и нажать кнопку. Она пересчитает
ТРИ параметра, которые зависят от производительности. Дальше — только мёртвое время руками и проверка по ШДК.

<h4>K НЕ ТРОГАЕМ</h4>
Раньше форсунки меняли через K (0x7F2B), и это тянуло за собой пересчёт осей карт, пола и потолка
нагрузки, порогов и обогащения ускорения — потому что K меняет само НАПОЛНЕНИЕ, а оно же является
осью карт. Теперь есть прямой множитель длительности впрыска <code>0x0A81</code>: он масштабирует
только топливо и не двигает ни одну ось. K остаётся как есть.

<h4>ЧТО МЕНЯЕТ КНОПКА</h4>
<b>1. Множитель впрыска (0x0A81)</b> = 33280 × 220 ÷ поток новых. Основная ручка: масштабирует
длительность впрыска. Мёртвое время прибавляется после него и не масштабируется — так и надо.<br>
<b>2. Пусковое обогащение (0x7E20)</b>, все 16 значений × (220 ÷ поток). Пуск идёт МИМО множителя:
таблица × ($142E+100) кладётся прямо в длительность и берётся по максимуму с основным расчётом
(код 8a92-8ad8). Не отмасштабируешь — зальёт свечи на холодном пуске.<br>
<b>3. Шаг лямбда-коррекции (0x7EEE и 0x7F0C)</b> = 15728 × поток ÷ 220. Шаг интегратора замкнутого
цикла считается как 0.24 от длительности впрыска (код 97f1/9891). Впрыск стал короче — шаг стал
мельче, и контур во столько же раз дольше выходит на цель. Возвращаем прежнюю скорость.<br>
<b>4. Обогащение ускорения (0x7910)</b> × (220 ÷ поток). Его добавка $1450 прибавляется к
длительности впрыска ПОСЛЕ множителя (8a8b) и им не масштабируется — доказано замером: при делении
множителя вдвое разница впрыска остаётся постоянной при любом $1450. С большими форсунками та же
добавка залила бы больше топлива на каждой перегазовке. Три таблицы обогащения перемножаются,
поэтому отношение применяется к одной — по положению дросселя.

<h4>ЧТО ОСТАЁТСЯ РУКАМИ</h4>
<b>Мёртвое время, база (0x7F88)</b> — свойство самой форсунки, отношением не считается. Ставить
паспортное для новых. Нет паспорта — оставить как есть и добить по ШДК.<br>
<b>Наклон по напряжению (0x7F87)</b> — не трогать.

<h4>ПРОВЕРКА НА МОТОРЕ</h4>
Сохранить дамп → залить → снять лог ШДК на прогретом. По логу подправить:<br>
• смесь врёт РАВНОМЕРНО везде → множитель 0x0A81<br>
• врёт только на ХХ и малых нагрузках → мёртвое время 0x7F88<br>
• врёт на пуске / первые секунды → пусковое 0x7E20

<hr>
<h4>Условия и оговорки</h4>
• Поток старых и новых мерить при ОДНОМ давлении топлива. Разные регуляторы → поток ∝ √(давление).<br>
• Проливка точнее паспорта: обе форсунки в одну рампу на один провод, открыть одновременно, лить 30-60 с, взвесить. Пролей весь комплект — увидишь разброс и износ.<br>
• Если СТАРЫЕ изношены (льют меньше паспорта) — в отношение бери ПАСПОРТ старых, не замеренное.<br>
• ⚠ ПУСК ПРОВЕРИТЬ ОТДЕЛЬНО. Базовый пусковой расчёт (8b26-8b51) множителем НЕ масштабируется — он
построен на наполнении. Пока пусковая таблица его перекрывает (замер: 896-1024 против 350-460) —
всё в порядке. Если опустить таблицу слишком низко, упрёшься в этот расчёт как в пол, и пуск
останется богатым. Заливает при пуске и таблица уже низкая — сюда и смотреть.<br>
• Очень большие форсунки → короткий импульс на ХХ, ниже линейного диапазона форсунки → неровный ХХ, прошивкой не лечится (физика).<br>
• Сопротивление форсунок (низко/высокоомные): другой тип = резисторы/драйвер, это железо.<br>
• «мс» у задержки/пускового — оценка из M30, из кода J30 точный масштаб не выведен; на пропорции не влияет.<br>
• ⚠ ЕСЛИ ПРОШИВКУ БУДУТ ПЕРЕСОБИРАТЬ билдером — он берёт сток, и множитель с шагом лямбды вернутся
к заводским. Калибровку накатывать заново или прописать значения в билдер.
"""

ACC_GUIDE = """
<h4>КАК УСТРОЕНО ОБОГАЩЕНИЕ УСКОРЕНИЯ (накачка при газовке)</h4>
Добавка топлива на тип-ине считается как <b>произведение ТРЁХ таблиц</b>, и результат
кладётся в <code>$1450</code>, который прибавляется к длительности впрыска (код 8a8b):
<code>$1450 = (скорость × положение × температура)</code>

<h4>⚠ ЛЮБОЙ НОЛЬ ОТМЕНЯЕТ ВСЁ</h4>
После каждой из трёх выборок стоит выход по нулю (904a, 9058, 9065). Ноль в одной таблице —
обогащения не будет вообще, сколько ни поднимай остальные.

<h4>Плюс два выключателя ДО таблиц</h4>
<b>0x7922</b> — порог оборотов (сток 64): выше него обогащение не считается.<br>
<b>0x792B</b> — порог скорости открытия (сток 10): плавно открыл — не тип-ин, накачки нет.<br>
Не работает при поднятых таблицах — сначала смотреть сюда.

<h4>Почему на ДАД провал в бедную, а на расходомере нет</h4>
Таблица по положению <b>0x7910</b> в стоке нулевая выше ~192 отсчётов открытия, то есть примерно
с половины хода педали обогащение выключено. Для расходомера это правильно: он меряет воздух,
входящий во впуск, и при наполнении коллектора сам даёт перелёт, который закрывает потребность.
Наша прослойка считает от давления, перелёта у неё нет — и на резком широком открытии остаётся
голая база, которая ещё и отстаёт. Отсюда кратковременный уход в бедную с последующей стабилизацией.
<b>Лечится подъёмом правой половины 0x7910</b> — ступенями, с проверкой по ШДК.
Триггер при этом общий и не виноват: обогащение запускается СКОРОСТЬЮ ОТКРЫТИЯ ДРОССЕЛЯ
($14A3 = разница положений, код 8ee0-8eec), ни расход, ни давление в него не входят.

<h4>При смене форсунок</h4>
Добавка $1450 прибавляется ПОСЛЕ множителя длительности и им не масштабируется. Поэтому калькулятор
форсунок правит 0x7910 тем же отношением — иначе с большими форсунками каждая перегазовка зальёт.
"""

# подразделы известных данных (порядок = порядок вывода)
GROUPS = [
  ("🗺 Главные карты", [0x7C00, 0x7D00]),
  ("🔥 Зажигание (УОЗ)", [0x76F0, 0x7EA0, 0x7F60, 0x7E50, 0x7EC0, 0x7FB8, 0x7FD4, 0x7FD5, 0x7FD6, 0x7FD7]),
  ("⛽ Топливо / смесь", [0x7E00, 0x7EB0, 0x7F30, 0x7BA0, 0x7BA8, 0x7F91, 0x7F92, 0x7F93]),
  ("🚫 Отсечка топлива на накате", [0x7E30, 0x7E40, 0x7F40, 0x7F50]),
  ("🌀 Холостой ход", [0x34B4, 0x7E60]),
  ("📊 ДМРВ / датчики / оси", [0x7A70, 0x7B30, 0x7AF0, 0x7B00, 0x7B10, 0x7B20, 0x7B50, 0x7B60]),
  ("🎚 Дроссель (TPS = АЦП ch6): обогащение ускорения + фильтры + пороги", [0x7900, 0x7910, 0x7BC0, 0x7922, 0x792B, 0x7700, 0x7720, 0x7600, 0x79A0, 0x79B0, 0x79C0, 0x79D0, 0x7691, 0x76CD, 0x7920, 0x7921, 0x7679, 0x767A], ACC_GUIDE),
  ("💉 Форсунки / впрыск (менять при замене форсунок)", [0x0A81, 0x7E20, 0x7EEE, 0x7F0C, 0x7F88, 0x7F87, 0x7F2B], INJ_GUIDE),
  ("⛔ Лимиты (обороты / скорость / нагрузка)", [0x7FB4, 0x7FA5, 0x7960, 0x7E90, 0x7E80]),
  ("💥 Детонация", [0x79E3, 0x7FE0, 0x7FDA, 0x7FDB, 0x7FDC, 0x7FDD]),
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
 <label><input type=checkbox id=heat> 🌡 Заливка карт</label>
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
<b>💉 ЗАМЕНА ФОРСУНОК</b> — производительность НОВЫХ форсунок, см³/мин:
<select id=calcnew class=ci style="width:auto">
<option value="220">220 — сток</option>
<option value="240">240</option>
<option value="259">259 (Z32 300ZX)</option>
<option value="270">270</option>
<option value="300">300</option>
<option value="330">330</option>
<option value="370">370</option>
<option value="440">440</option>
<option value="550">550</option>
<option value="650">650</option>
<option value="">— своё число —</option>
</select>
<input id=calcnewman class=ci placeholder="см³/мин" style="display:none">
&nbsp;&nbsp;Поток СТАРЫХ <input id=calcold class=ci value="220"> см³/мин<br>
Мёртвое время новых при ~14В, мс <input id=calclat class=ci placeholder="0.75"> &nbsp;<span style="color:#787;font-size:11px">пусто = не трогать</span><br>
<button id=calcgo>⚙ ПЕРЕСЧИТАТЬ ПОД НОВЫЕ ФОРСУНКИ</button>
<div class=calcnote>Меняет ТРИ параметра: множитель впрыска 0x0A81, пусковое обогащение 0x7E20 (16 значений) и шаг лямбда-коррекции 0x7EEE/0x7F0C. <b>K (0x7F2B) не трогает</b> — оси карт, пол/потолок нагрузки и пороги остаются на месте, пересчитывать их не надо.<br>Считает всегда от СТОКА, поэтому жать можно повторно — не накапливается. Наклон 0x7F87 не трогается. После — проверь значения ниже и сохрани дамп.</div>
</div>`;

const DAD_CALC=`<div class=calc>
<b>📐 Расчёт тарировки ДАД по 2 точкам</b> — введи две пары <b>отсчёт АЦП → давление</b>. Отсчёт бери прямо из панели, строка «АЦП Расходомер/ДАД» (10 бит, 0…1023):<br>
Точка 1: <input id=dv1 class=ci placeholder="170"> АЦП → <input id=dp1 class=ci placeholder="40"> кПа<br>
Точка 2: <input id=dv2 class=ci placeholder="1000"> АЦП → <input id=dp2 class=ci placeholder="150"> кПа<br>
<button id=dadgo>📐 РАССЧИТАТЬ — Наклон + Смещение</button>
<div class=calcnote>Вводятся ОТСЧЁТЫ, а не вольты: блок работает в отсчётах, а перевод в вольты содержит непроверенное допущение про опору АЦП платы. Рутина делит 10 бит на 4 — редактор это учитывает сам. Смещение может быть ОТРИЦАТЕЛЬНЫМ, это норма для широкодиапазонных датчиков.<br>
<b>Перевод в вольты (прикидка):</b> <code>В ≈ АЦП10 × 0.00488</code> &nbsp;·&nbsp; обратно <code>АЦП10 ≈ В × 205</code>. Для 8-битного отсчёта <code>В ≈ АЦП8 × 0.0195</code>. Это допущение «5 В на 256 отсчётов»; реальная опора АЦП платы блока из ПЗУ не выводится, поэтому в вольтах может быть смещение — тарируйся по отсчётам, а вольты только для прикидки.<br>
Пишет прямо в поля Наклон/Смещение выше. После — сохрани дамп.</div>
</div>`;
const ROM_ORIG=Uint8Array.from(atob("__ROM__"),c=>c.charCodeAt(0));
let ROM=ROM_ORIG.slice();      // редактируемая копия
let REF=ROM_ORIG.slice();      // эталон сравнения (по умолчанию = сток, можно загрузить файл)
const CHK=[0x7F7A,0x7F7B];
const EXPANDED=new Set();       // адреса свёрнутых секций, которые раскрыли вручную
let RAWMODE=false;              // показывать/править сырые байты 0..255 вместо интерпретации
// граф-вид: у неизвестных вкл по умолчанию, НО только если есть разброс (константы оставляем свёрнутыми)
let HEATMAP=false;              // тепловая заливка ячеек карт 16x16 по значению (по умолчанию ВЫКЛ)
// поля калькулятора форсунок живут ЗДЕСЬ, а не в DOM: render() пересобирает страницу
const INJST={sel:"220",man:"",old:"220",lat:""};
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
  case 've': return Math.round(x/128*1000)/1000;
  case 'kpa': return x;
  case 'dadofs': {const s=(x>127?x-256:x); return Math.round(s*0.0195*100)/100;}  // ЗНАКОВОЕ
  case 'dadslope': return Math.round(x/5*10)/10;
  case 'km': return Math.round(x/255*1000)/1000;
  case 'tpsadc': return x*2;
  case 'tpspct': return Math.round(x*100/172);
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
   case 've': return clamp(Math.round(+v*128));
   case 'kpa': return clamp(Math.round(+v));
   // ЗНАКОВОЕ: −128…+127 отсчётов (≈ −2.5…+2.5 В). clamp() режет в 0…255 и минус бы съел.
   case 'dadofs': {const n=Math.round(+v/0.0195); return isNaN(n)?null:(Math.max(-128,Math.min(127,n))&0xFF);}
   case 'dadslope': return clamp(Math.round(+v*5));
   case 'km': return clamp(Math.round(+v*255));
   case 'tpsadc': return clamp(Math.round(+v/2));
   case 'tpspct': return clamp(Math.round(+v*172/100));
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
  ld8x2:['0','16','32','48','64','80','96','112','0','16','32','48','64','80','96','112'],
  tps16:['0','16','32','48','64','80','96','112','128','144','160','176','192','208','224','240'],
};
function axCap(a){return {temp:'темп ОЖ °C',rpm6000:'об/мин',rpm3000:'об/мин',clrpm:'об/мин',idx8:'индекс',ld8x2:'открытие дросселя, АЦП $1492 (2 подтабл. по 8)',tps16:'открытие дросселя, АЦП $1492 (0=закрыт)'}[a]||'ось';}
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
  // ⚠ ОСЬ БЕЗ ПЕРЕСЧЁТА КАРТЫ — ТИХАЯ ПОРЧА НАСТРОЙКИ. Числа в ячейках остаются на
  // месте, но начинают означать другую нагрузку/давление: поверхность перекашивается,
  // и заметить это по цифрам невозможно. Поэтому у каждой оси, на которой сидят карты,
  // есть кнопка пересчёта, а появляется она ровно тогда, когда ось УЖЕ изменена.
  const deps=ITEMS.filter(m=>m.rax===it.a||m.cax===it.a);
  let axbtn='';
  if(deps.length){
    const moved=[...Array(cellCount(it)).keys()].some(k=>ROM[it.a+k]!==REF[it.a+k]);
    axbtn=`<button class=axre data-a=${it.a} ${moved?'':'disabled'} title="${moved?'Пересчитать карты, которые сидят на этой оси, чтобы поверхность осталась прежней':'Ось не менялась — пересчитывать нечего'}">⟲ пересчитать карты под ось${moved?'':' (ось не менялась)'}</button>`;
  }
  let h=`<h3>${A} · ${it.name}${deadb} <span class=note>[${it.kind}, ${unitLabel(it)}]${it.note?' — '+it.note:''}</span>${grph}${axbtn}${secrev}</h3>`;
  if(deps.length) h+=`<div class=hint>Ось. На ней сидят: ${deps.map(m=>'0x'+m.a.toString(16).toUpperCase()+' '+m.name.split('(')[0].trim()).join(', ')}. <b>Изменил ось — жми «пересчитать карты под ось»</b>, иначе значения останутся в тех же ячейках, но будут означать другую точку, и настройка тихо перекосится. Пересчёт берёт СТАРУЮ ось из эталона (по умолчанию сток) и переносит текущие карты на новую с сохранением поверхности.</div>`;
  if(it.kind=='map16'){
    const rax=byName(it.rax),cax=byName(it.cax);
    let mn=0,mx=1;
    if(HEATMAP){const vs=[];for(let j=0;j<256;j++)vs.push(cnum(it,j,ROM));mn=Math.min(...vs);mx=Math.max(...vs);}
    h+=`<table class=map><tr><td class=ax>об\\${cax?cax.unit:'нагр'}</td>`;
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
  const own=ITEMS.filter(i=>i.own);
  // Собственные карты показывать ТОЛЬКО если ДАД-патч реально прошит.
  // ⚠ 09.08.26 врезка ПЕРЕЕХАЛА с 89D8 на 8965 (на выход таблицы линеаризации).
  // Детект по старому адресу молча прятал ВСЕ собственные карты, и настройку ДАД
  // было не открыть. Проверяем оба места: 8965 (файл 0x0965) — текущая схема,
  // 89D8 (файл 0x09D8) — прежняя, чтобы старые бины тоже открывались.
  const dadOn=(ROM[0x0965]===0xBD && ROM[0x0966]===0xC7 && ROM[0x0967]===0x00)
            ||(ROM[0x09D8]===0xBD && ROM[0x09D9]===0xC7 && ROM[0x09DA]===0x00);
  const known=ITEMS.filter(i=>!i.unknown && !i.own), unk=ITEMS.filter(i=>i.unknown);
  const byA={}; for(const i of known) byA[i.a]=i;
  let html='';
  if(own.length && dadOn){
    // ⚠ ВРЕЗКИ МАЛО: первая команда рутины — TST $CA13 (файл 0x4A13). Ноль = хвостовой
    // переход в заводскую таблицу расходомера, и всё, что ниже, блок не читает вообще.
    // Карты тут НЕ прячем (это файловый редактор — режим можно как раз и переключить),
    // но состояние обязаны показать: иначе крутишь VE и не понимаешь, почему без толку.
    const dadMode=ROM[0x4A13]!==0;
    html+='<div class=group style="color:#fc6">🔧 СОБСТВЕННЫЕ КАРТЫ ('+own.length+') — НАШ ПАТЧ: speed-density по ДАД'+
          (dadMode?' — <span style="color:#6d6">РЕЖИМ ДАД ВКЛЮЧЁН</span>'
                  :' — <span style="color:#f66">РЕЖИМ ВЫКЛЮЧЕН, БЛОК ЕДЕТ НА РАСХОДОМЕРЕ</span>')+'</div>';
    if(!dadMode) html+='<div class=hint style="border-color:#a33;color:#fbb">⚠ Скаляр «РЕЖИМ РАСЧЁТА» ниже стоит в <b>0</b>. Рутина ДАД уходит в заводскую таблицу линеаризации расходомера первой же командой — до всего, что в этом разделе, дело НЕ доходит. Правки VE, Ktps, осей и тарировки на поведение мотора не повлияют, пока режим не станет 1.</div>';
    html+='<div class=hint>НЕ заводское — наш патч перевода на ДАД (давление вместо MAF). Наполнение = Об·Д·VE, впрыск ∝ наполнению. <b>VE</b> — основная карта тюна (крутишь по ШДК: форма наполнения по оборотам×давлению, 1.0=норма). <b>Ось давления</b> — 16 точек в кПа (атмо 20-110). <b>Смещение</b> (В) и <b>Наклон</b> (кПа/В) — тарировка ДАД (у каждого датчика свои, из паспорта). <b>КМ</b> — общий уровень топлива (0-1, старт ~0.5). Работает ТОЛЬКО с прошитым патчем и ДАД на месте MAF.</div>';
    for(const it of own) html+=secHtml(it);
    html+=DAD_CALC;
  }
  html+='<div class=group>✅ ИЗВЕСТНЫЕ ДАННЫЕ ('+known.length+') — смысл известен, подписано</div>';
  const used=new Set();
  for(const g of GROUPS){
    const title=g[0], addrs=g[1], info=g[2];
    const its=addrs.map(a=>byA[a]).filter(Boolean);
    if(!its.length)continue;
    html+='<div class=sub>'+title+' ('+its.length+')</div>';
    // Заголовок и калькулятор — по группе, а не захардкоженные под форсунки:
    // групп с инструкцией стало две (форсунки и обогащение ускорения).
    if(info){
      const isInj=(addrs.indexOf(0x0A81)>=0);
      html+='<details class=guide><summary>📖 '+(isInj?'Инструкция по замене форсунок':'Как устроено обогащение ускорения')+
            ' — нажми чтобы раскрыть</summary><div class=guidebody>'+info+'</div></details>'+(isInj?INJ_CALC:'');
    }
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
      // правили ТАБЛИЦУ-ОСЬ (её адрес = rax/cax какой-то карты)? -> перерисовать, чтобы оси на картах обновились
      if(ITEMS.some(m=>m.rax===a||m.cax===a)) render();
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
  // ---- ПЕРЕСЧЁТ КАРТ ПОД ИЗМЕНЁННУЮ ОСЬ ----
  // ⚠ СЧИТАЕМ В СЫРЫХ БАЙТАХ, А НЕ В ФИЗИКЕ. Первая версия считала в физике (AFR,
  // градусы) и делала ХУЖЕ: поверхность уезжала на 6.4 AFR вместо 0.9. Причина —
  // обратное преобразование AFR→байт перебрасывает ячейку в другой кластер кодировки
  // (у смеси их два, и в заводской карте они перемешаны: 142 байта в нижнем, 114 в
  // верхнем), а блок интерполирует СОСЕДНИЕ БАЙТЫ. Правило: пересчитывать надо в том
  // же пространстве, в котором интерполирует ЭБУ, иначе «сохранение поверхности»
  // сохраняет не ту поверхность.
  document.querySelectorAll('#app button.axre').forEach(b=>{
    b.addEventListener('click',()=>{
      const ax=+b.dataset.a, axIt=byName(ax);
      const n=cellCount(axIt);
      const oldAx=[...Array(n).keys()].map(k=>cnum(axIt,k,REF));
      const newAx=[...Array(n).keys()].map(k=>cnum(axIt,k,ROM));
      const mono=v=>v.every((x,i)=>i===0||x>v[i-1]);
      if(!mono(oldAx)||!mono(newAx)){alert('Ось должна строго возрастать. Сейчас это не так — пересчёт отменён, поправь ось.');return;}
      const at=(vals,axv,x)=>{                 // линейная выборка vals по оси axv в точке x
        if(x<=axv[0])return vals[0];
        if(x>=axv[axv.length-1])return vals[vals.length-1];
        let i=0; while(i<axv.length-2&&axv[i+1]<x)i++;
        const f=(x-axv[i])/(axv[i+1]-axv[i]);
        return vals[i]+(vals[i+1]-vals[i])*f;
      };
      const deps=ITEMS.filter(m=>m.rax===ax||m.cax===ax);
      const done=[];
      for(const m of deps){
        const cur=[...Array(256).keys()].map(k=>ROM[m.a+k]);      // СЫРЫЕ байты карты
        const out=cur.slice();
        if(m.cax===ax){                        // ось столбцов: пересобираем каждую строку
          for(let r=0;r<16;r++){
            const row=cur.slice(r*16,r*16+16);
            for(let c=0;c<16;c++) out[r*16+c]=at(row,oldAx,newAx[c]);
          }
        }else{                                 // ось строк: пересобираем каждый столбец
          for(let c=0;c<16;c++){
            const col=[...Array(16).keys()].map(r=>cur[r*16+c]);
            for(let r=0;r<16;r++) out[r*16+c]=at(col,oldAx,newAx[r]);
          }
        }
        let ch=0;
        for(let k=0;k<256;k++){
          const raw=Math.max(0,Math.min(255,Math.round(out[k])));
          if(raw!==ROM[m.a+k]){ROM[m.a+k]=raw;ch++;}
        }
        done.push(m.name.split('(')[0].trim()+': '+ch+' яч.');
      }
      mark();
      document.getElementById('status').textContent=
        'Ось 0x'+ax.toString(16).toUpperCase()+' — карты пересчитаны, поверхность сохранена. '+done.join(' · ')+
        '. Старая ось взята из эталона.';
      render();
    });
  });
  // ⚠ render() пересобирает калькулятор целиком, поэтому введённое надо ХРАНИТЬ СНАРУЖИ
  // и восстанавливать. Без этого после нажатия кнопки поля сбрасывались на 220, и
  // повторное нажатие молча возвращало прошивку к стоку.
  const csel=document.getElementById('calcnew'), cman=document.getElementById('calcnewman');
  const cold=document.getElementById('calcold'), clat=document.getElementById('calclat');
  if(csel){
    csel.value=INJST.sel; cman.value=INJST.man; cold.value=INJST.old; clat.value=INJST.lat;
    cman.style.display=(csel.value==='')?'':'none';
    const save=()=>{INJST.sel=csel.value;INJST.man=cman.value;INJST.old=cold.value;INJST.lat=clat.value;};
    csel.addEventListener('change',()=>{
      const own=csel.value==='';
      cman.style.display=own?'':'none';
      if(own)cman.focus();
      save();
    });
    [cman,cold,clat].forEach(e=>e.addEventListener('input',save));
  }
  const cg=document.getElementById('calcgo');
  if(cg)cg.addEventListener('click',()=>{
    INJST.sel=csel.value; INJST.man=cman.value; INJST.old=cold.value; INJST.lat=clat.value;
    const o=parseFloat(cold.value);
    const n=parseFloat(csel.value!==''?csel.value:cman.value);
    const lat=parseFloat(clat.value);
    if(!(o>0)||!(n>0)){alert('Укажи производительность новых форсунок в см³/мин (и поток старых, сток 220).');return;}
    const r=o/n;                       // <1 при форсунках больше: топлива лить МЕНЬШЕ
    const put16=(a,v)=>{v=Math.max(1,Math.min(65535,Math.round(v)));ROM[a]=(v>>8)&255;ROM[a+1]=v&255;return v;};
    const org16=a=>(ROM_ORIG[a]<<8)|ROM_ORIG[a+1];
    // 1) множитель длительности впрыска — ГЛАВНАЯ ручка производительности
    const mult=put16(0x0A81, org16(0x0A81)*r);
    // 2) пусковое обогащение — идёт МИМО множителя, масштабируем отдельно
    for(let i=0;i<16;i++) ROM[0x7E20+i]=Math.max(1,Math.min(255,Math.round(ROM_ORIG[0x7E20+i]*r)));
    // 3) шаг лямбда-коррекции — считается как доля от длительности впрыска, значит
    //    при коротком впрыске мельчает. Поднимаем ОБРАТНЫМ отношением, чтобы скорость
    //    выхода замкнутого цикла на цель осталась прежней.
    const st1=put16(0x7EEE, org16(0x7EEE)/r);
    put16(0x7F0C, org16(0x7F0C)/r);
    // 4) ОБОГАЩЕНИЕ УСКОРЕНИЯ. Его добавка $1450 прибавляется к длительности ПОСЛЕ
    //    множителя (8a8b) и им не масштабируется — доказано замером: при делении
    //    множителя вдвое разница впрыска остаётся 143 при любых $1450. Значит с
    //    большими форсунками та же добавка зальёт больше топлива. Три таблицы
    //    ПЕРЕМНОЖАЮТСЯ, поэтому отношение достаточно применить к ОДНОЙ — берём ту,
    //    что по положению дросселя: она же основная ручка настройки, и у неё правая
    //    половина нулевая (ноль × что угодно = ноль, масштабировать нечего).
    let acc=0;
    for(let i=0;i<16;i++){
      const v=Math.max(0,Math.min(255,Math.round(ROM_ORIG[0x7910+i]*r)));
      if(v!==ROM[0x7910+i]){ROM[0x7910+i]=v;acc++;}
    }
    // мёртвое время — свойство форсунки, отношением НЕ считается. Пусто = не трогаем.
    let latTxt='не трогали';
    if(lat>0){ROM[0x7F88]=Math.max(0,Math.min(255,Math.round(lat*100))); latTxt='байт '+ROM[0x7F88];}
    mark();
    document.getElementById('status').textContent=
      'Форсунки '+o+' → '+n+' см³/мин (отношение '+r.toFixed(3)+'): множитель впрыска '+mult+
      ', пусковое ×'+r.toFixed(3)+', шаг лямбды '+st1+', обогащение ускорения ×'+r.toFixed(3)+
      ' ('+acc+' яч.). K не тронут. Мёртвое время: '+latTxt+'.';
    render();
  });
  const dg=document.getElementById('dadgo');
  if(dg)dg.addEventListener('click',()=>{
    const v1=parseFloat(document.getElementById('dv1').value), p1=parseFloat(document.getElementById('dp1').value);
    const v2=parseFloat(document.getElementById('dv2').value), p2=parseFloat(document.getElementById('dp2').value);
    if(isNaN(v1)||isNaN(p1)||isNaN(v2)||isNaN(p2)||v1===v2){alert('Введи две РАЗНЫЕ точки: отсчёт АЦП → давление');return;}
    // Панель показывает 10 бит, а рутина работает с 8 (делит на 4). Приводим сразу,
    // чтобы пользователь вводил ровно то, что видит, и ничего не пересчитывал в уме.
    const a1=v1/4, a2=v2/4;
    const kpc=(p2-p1)/(a2-a1);              // кПа на ОТСЧЁТ
    const aoff=a1 - p1/kpc;                 // отсчёт при 0 кПа — может быть ОТРИЦАТЕЛЬНЫМ
    // Блок считает (АЦП − Смещ) × Наклон / 256, значит Наклон = кПа_на_отсчёт × 256.
    const smRaw=Math.round(aoff), slRaw=Math.round(kpc*256);
    // Смещение ЗНАКОВОЕ: −128…+127 отсчётов. Минус — не ошибка: широкодиапазонные
    // датчики показывают давление уже при нуле, и прямая пересекает 0 кПа в минусе.
    if(slRaw<0||slRaw>255||smRaw<-128||smRaw>127){alert('Вне диапазона: наклон 0…1.0 кПа/отсчёт (круче не влезает) или смещение вне −128…+127 отсчётов. Запишу с ограничением — проверь точки.');}
    const smByte=Math.max(-128,Math.min(127,smRaw)) & 0xFF;
    const slByte=Math.max(0,Math.min(255,slRaw));
    ROM[0x4A10]=smByte; ROM[0x4A11]=slByte;
    mark();
    document.getElementById('status').textContent='ДАД: наклон '+kpc.toFixed(3)+' кПа/отсчёт (байт '+slByte+'), смещение '+smRaw+' отсчётов ≈ '+(smRaw*0.0195).toFixed(2)+' В (байт '+smByte+'). Проверка: АЦП '+v1+' ≈ '+(v1*0.00488).toFixed(2)+' В → '+(((Math.max(0,Math.min(255,Math.round(a1)-smRaw)))*slByte)>>8)+' кПа';
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

// ---- ТАБЛИЦА ПЕРЕСЧЁТА ДАВЛЕНИЯ ($C600) ----
// С v37 рутина ДАД не вычисляет номер столбца по давлению, а читает готовый ответ из
// таблицы: на каждое давление 0…255 лежит байт (столбец<<4 | дробь). Благодаря этому ось
// 0x4A00 может быть любой формы. Но таблица и ось — ДВЕ СВЯЗАННЫЕ ВЕЩИ в разных местах
// ПЗУ: разъедутся — блок возьмёт не тот столбец, и притом молча. Поэтому таблица
// пересобирается из оси при КАЖДОМ сохранении, а не по отдельной кнопке.
const PLUT=0x4600, PAX=0x4A00, PLUT_AT=0x4758;
const PLUT_SIG=[0xD6,0xF7,0xCE,0xC6,0x00,0x3A,0xA6,0x00];   // LDAB $F7 / LDX #$C600 / ABX / LDAA 0,X
function hasPressLut(){return PLUT_SIG.every((v,i)=>ROM[PLUT_AT+i]==v);}
function rebuildPressLut(){
  if(!hasPressLut())return null;            // старая прошивка (столбец считается сдвигами) — не трогаем
  const ax=[];for(let i=0;i<16;i++)ax.push(ROM[PAX+i]);
  for(let i=0;i<15;i++)if(ax[i]>=ax[i+1])
    return {err:'ячейка '+i+' = '+ax[i]+', следующая '+ax[i+1]+' — ось обязана возрастать'};
  let ch=0;
  for(let p=0;p<256;p++){
    let col,fr;
    if(p<=ax[0]){col=0;fr=0;}                // ниже начала — прижать к первому столбцу
    else if(p>=ax[15]){col=15;fr=0;}         // выше конца — к последнему
    else{
      col=15;
      for(let i=0;i<15;i++)if(ax[i]<=p&&p<ax[i+1]){col=i;break;}
      if(col>=15){fr=0;col=15;}
      else{
        fr=Math.round((p-ax[col])/(ax[col+1]-ax[col])*16);
        if(fr>15){col++;fr=0;}               // дробь 16/16 — это уже следующая ячейка
        if(col>15){col=15;fr=0;}
      }
    }
    const v=(col<<4)|fr;
    if(ROM[PLUT+p]!=v){ROM[PLUT+p]=v;ch++;}
  }
  return {changed:ch,ax:ax};
}
function ts(){const d=new Date();const p=n=>(''+n).padStart(2,'0');return d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+'_'+p(d.getHours())+p(d.getMinutes());}
document.getElementById('save').addEventListener('click',()=>{
  // ось давления могла измениться — таблица пересчёта обязана пойти следом, иначе
  // прошивка будет читать карту не из тех столбцов
  const lut=rebuildPressLut();
  if(lut&&lut.err){
    alert('Ось давления (0x4A00) задана неверно:\n\n'+lut.err+
          '\n\nТочки оси должны идти строго по возрастанию. Файл НЕ сохранён — исправь ось и нажми сохранить ещё раз.');
    return;
  }
  recalcChecksum();
  const name=(document.getElementById('fname').value.trim()||'J30_редактирование')+'_'+ts()+'.bin';
  const blob=new Blob([ROM],{type:'application/octet-stream'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();
  document.getElementById('status').textContent='скачано: '+name+' (чек-сумма 0x'+ROM[0x7F7A].toString(16)+'/0x'+ROM[0x7F7B].toString(16)+')'
    +(lut?(lut.changed?' · таблица давления пересобрана под ось, '+lut.changed+' байт':' · таблица давления сверена, менять нечего'):'');dirty=false;
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
# пишем в ОБА места: локальный html + реальный редактор контейнера ecu_twin (:8080/editor)
outs = [
    os.path.join(ROOT, "j30", "J30_редактор.html"),
    os.path.join(ROOT, "ecu_twin", "frontend", "editor.html"),
]
for out in outs:
    if os.path.isdir(os.path.dirname(out)):
        open(out, "w", encoding="utf-8").write(HTML)
        print("OK:", out, "| размер", len(HTML), "| секций", len(items))
