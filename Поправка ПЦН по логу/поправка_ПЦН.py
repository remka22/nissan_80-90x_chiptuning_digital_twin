#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Поправка ПЦН из лога Январь (y30). За один запуск:
  ВХОД : лог .csv (открытый цикл, ШДК валиден) + исходный .cte ПЦН [454C2B1D]
  ВЫХОД: 1) текстовый отчёт  — коэффициенты поправок + количество точек по ячейкам
         2) .cte с применённой поправкой (32x16, столбцы >6000 из исходника без изменений)

Поправка = median(AFR_WBL / AFR) по устоявшимся точкам ячейки.
  AFR — эффективная цель блока (с обогащением fPOW); AFR_WBL — факт по ШДК (открытый цикл COEFF=1).
  <1 = ехали БОГАЧЕ цели -> режем наполнение;  >1 = БЕДНЕЕ -> добавляем.
Два метода (переключаются --kgbc / --cte, по умолчанию kgbc):
  kgbc : новая = median(KGBC_из_лога * поправка) — от реального коэф. в момент лога,
         значения входного cte на результат НЕ влияют (вход cte — только холст).
  cte  : новая = значение_входного_cte * поправка — классика, опирается на вход cte.

РЕЗУЛЬТАТ: рядом со скриптом создаётся папка "результат <дата_время> (метод)",
  в неё копируются исходники (лог + cte) и кладутся: отчёт .txt и .cte с поправкой.

Запуск:
  Windows : двойной клик по "Поправка (Windows).bat"  (спросит файлы, если их нет в папке)
  macOS   : двойной клик по "Поправка (Mac).command", или в консоли:
            python3 поправка_ПЦН.py [<лог.csv> <исходник.cte>] [--kgbc|--cte]
  Если лог и cte лежат в папке скрипта — берёт их сам; иначе откроет окно выбора.
"""
import sys, os, csv, re, statistics, shutil
from datetime import datetime

# ---- оси ПЦН (константы прошивки Январь y30) ----
RPM = [600,720,800,920,1000,1120,1200,1400,1600,1800,2000,2280,2520,2760,3000,
       3280,3520,3760,4000,4280,4520,4760,5000,5280,5520,5760,6000]   # 27 -> X1..X27
THR = [0,2,4,6,8,10,14,18,23,29,37,46,56,66,80,100]                   # 16 -> Z1..Z16

# ---- метод расчёта новой ПЦН ----
#   'kgbc' : новая = median(KGBC_из_лога * AFR_WBL/AFR). Берём реальный коэффициент,
#            что крутился в момент лога -> результат НЕ зависит от значений во входном cte
#            (вход cte только холст: неохваченные ячейки и столбцы >6000 берём из него).
#   'cte'  : новая = значение_входного_cte * median(AFR_WBL/AFR). Классика, опирается на вход cte.
# Переключить на запуске:  --kgbc  или  --cte   (перебивает значение ниже)
METHOD = 'kgbc'

# ---- параметры (правь при нужде) ----
MATCH_TOL  = 0.02     # допуск сверки "тот ли входной cte, что в логе" (по KGBC). Это НЕ стоп, просто факт.
MIN_POINTS = 4        # минимум устоявшихся точек в ячейке, иначе не трогаем
DRPM_MAX   = 100      # |ΔRPM| между соседними строками — фильтр устоявшегося режима
DTHR_MAX   = 2        # |ΔTHR| —//—
CLAMP_LO   = 0.60     # ограничение фактора снизу (защита от мусорных ячеек)
CLAMP_HI   = 1.60     # —//— сверху
COEFF_TOL  = 0.05     # COEFF должен быть ~1 (открытый цикл), иначе точку отбрасываем
DGTC_MAX   = 0.1      # если активно ускор. обогащение/обеднение (DGTC_RICH/LEAN) — точку выкидываем
                      # ВАЖНО: цель AFR это обогащение НЕ включает, иначе получим ложное "богато->режь"

def fl(x):
    try: return float(str(x).replace(',','.'))
    except: return None

def nearest(axis, v):
    """индекс ближайшего узла оси"""
    best, bi = 1e18, 0
    for i,a in enumerate(axis):
        if abs(a-v) < best: best, bi = abs(a-v), i
    return bi

def parse_cte(path):
    """читаем .cte -> (строки-заголовка, dict[(x,z)]=float, maxX, maxZ)"""
    hdr, vals, mx, mz = [], {}, 0, 0
    for l in open(path, encoding='cp1251'):
        l = l.rstrip('\r\n')
        m = re.match(r'X(\d+)Z(\d+)=(.+)', l)
        if m:
            x,z = int(m.group(1)), int(m.group(2))
            vals[(x,z)] = float(m.group(3).replace(',','.'))
            mx, mz = max(mx,x), max(mz,z)
        elif l.startswith('[') or l.startswith('Name='):
            hdr.append(l)
    return hdr, vals, mx, mz

def fmt_cte(x):
    """значение в формат .cte: округление к шагу ЭБУ 1/128, запятая-десятичная"""
    v = round(x*128)/128
    return ('%.8f' % v).rstrip('0').rstrip('.').replace('.', ',')

def interp_base(vals, rpm, thr):
    """билинейная интерполяция исходной ПЦН в точке (для сверки с KGBC лога)"""
    def pos(ax,v):
        if v<=ax[0]: return 0,0.0
        if v>=ax[-1]: return len(ax)-2,1.0
        for i in range(len(ax)-1):
            if ax[i]<=v<=ax[i+1]: return i,(v-ax[i])/(ax[i+1]-ax[i])
        return len(ax)-2,1.0
    ci,cf = pos(RPM,rpm); ri,rf = pos(THR,thr)
    def g(xi,zi): return vals[(xi+1,zi+1)]
    a = g(ci,ri)+(g(ci+1,ri)-g(ci,ri))*cf
    b = g(ci,ri+1)+(g(ci+1,ri+1)-g(ci,ri+1))*cf
    return a+(b-a)*rf

def autodetect(here):
    """ровно один .csv и один .cte в папке скрипта -> вернуть пути, иначе (None, None)"""
    csvs = sorted(f for f in os.listdir(here) if f.lower().endswith('.csv'))
    ctes = sorted(f for f in os.listdir(here)
                  if f.lower().endswith('.cte') and 'ПЦН применено' not in f)
    if len(csvs) == 1 and len(ctes) == 1:
        return os.path.join(here, csvs[0]), os.path.join(here, ctes[0])
    return None, None

def pick_files():
    """окно выбора лога и .cte (Windows/GUI); без tkinter — подсказка и выход"""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        print('В папке нет ровно одного .csv и .cte, а окно выбора недоступно.')
        print('Вариант 1: положи в папку ОДИН лог .csv и ОДИН исходный .cte.')
        print('Вариант 2: запусти с путями:  python поправка_ПЦН.py <лог.csv> <исходник.cte>')
        sys.exit(1)
    root = tk.Tk(); root.withdraw()
    log = filedialog.askopenfilename(title='Выбери ЛОГ поездки (.csv)',
                                     filetypes=[('Лог CSV', '*.csv'), ('Все файлы', '*.*')])
    if not log: print('Лог не выбран — отмена.'); sys.exit(1)
    cte = filedialog.askopenfilename(title='Выбери исходный .cte (ПЦН по дросселю)',
                                     filetypes=[('Таблица CTE', '*.cte'), ('Все файлы', '*.*')])
    if not cte: print('Исходный .cte не выбран — отмена.'); sys.exit(1)
    return log, cte

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    args = sys.argv[1:]
    method = METHOD
    if '--kgbc' in args: method = 'kgbc'; args.remove('--kgbc')
    if '--cte'  in args: method = 'cte';  args.remove('--cte')
    if method not in ('kgbc', 'cte'): method = 'kgbc'

    if len(args) >= 2:                       # явные пути (консоль)
        log_path, cte_path = args[0], args[1]
        base_out = args[2] if len(args) > 2 else here
    else:                                    # авто-поиск, иначе окно выбора
        log_path, cte_path = autodetect(here)
        if not (log_path and cte_path):
            log_path, cte_path = pick_files()
        base_out = here

    # отдельная папка результата с меткой времени: туда копируем исходники и кладём результаты
    stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    out_dir = os.path.join(base_out, 'результат ' + stamp + ' (' + method + ')')
    os.makedirs(out_dir, exist_ok=True)
    try:
        shutil.copy2(log_path, os.path.join(out_dir, os.path.basename(log_path)))
        shutil.copy2(cte_path, os.path.join(out_dir, os.path.basename(cte_path)))
    except Exception as e:
        print('не смог скопировать исходники в папку результата:', e)
    base_name = os.path.splitext(os.path.basename(log_path))[0]

    hdr, base, mx, mz = parse_cte(cte_path)
    if (mx, mz) != (32, 16):
        print('ВНИМАНИЕ: .cte %dx%d, ожидалось 32x16 — проверь файл.' % (mx, mz))

    # --- собираем устоявшиеся точки по ячейкам ---
    rows = list(csv.DictReader(open(log_path), delimiter=','))
    pts = {}           # (xi,zi) -> [(поправка, KGBC|None, интерп_базы|None), ...]
    prev = None
    used = skipped = no_kgbc = 0
    for r in rows:
        thr, rpm = fl(r.get('THR')), fl(r.get('RPM'))
        afr, wbl = fl(r.get('AFR')), fl(r.get('AFR_WBL'))
        coeff = fl(r.get('COEFF'))
        if None in (thr, rpm, afr, wbl):
            prev = (rpm, thr); continue
        # фильтр устоявшегося режима
        steady = prev and prev[0] is not None and prev[1] is not None \
                 and abs(rpm-prev[0]) <= DRPM_MAX and abs(thr-prev[1]) <= DTHR_MAX
        prev = (rpm, thr)
        if not steady: skipped += 1; continue
        if coeff is not None and abs(coeff-1.0) > COEFF_TOL: skipped += 1; continue
        # выкидываем точки с активным ускор. обогащением/обеднением (переходной впрыск)
        dgr, dgl = fl(r.get('DGTC_RICH')), fl(r.get('DGTC_LEAN'))
        if (dgr and dgr > DGTC_MAX) or (dgl and dgl > DGTC_MAX): skipped += 1; continue
        if afr <= 0 or wbl <= 0 or rpm < RPM[0] or rpm > RPM[-1]: skipped += 1; continue
        xi, zi = nearest(RPM, rpm), nearest(THR, thr)
        k = fl(r.get('KGBC'))                                  # реальный коэф ПЦН в момент лога
        bi = interp_base(base, rpm, thr) if k is not None else None
        if k is None: no_kgbc += 1
        pts.setdefault((xi,zi), []).append((wbl/afr, k, bi))
        used += 1

    # для метода kgbc нужен KGBC в логе; если его нет вовсе — честно падаем на cte
    if method == 'kgbc' and used and no_kgbc == used:
        print('ВНИМАНИЕ: в логе нет KGBC — метод kgbc невозможен, считаю по cte.')
        method = 'cte'
    clampf = lambda x: max(CLAMP_LO, min(CLAMP_HI, x))

    # --- считаем и применяем по выбранному методу ---
    applied = dict(base)
    cells = []
    changed = 0
    for zi in range(16):
        for xi in range(27):
            P = pts.get((xi,zi))
            if not P: continue
            n = len(P)
            factor = clampf(statistics.median([p[0] for p in P]))       # median(AFR_WBL/AFR)
            ks    = [p[1] for p in P if p[1] is not None]               # KGBC по точкам
            diffs = [abs(p[2]-p[1]) for p in P if p[1] is not None and p[2] is not None]
            mk    = statistics.median(ks) if ks else None               # средний реальный коэф
            match = (statistics.median(diffs) <= MATCH_TOL) if diffs else None
            base_v = base[(xi+1, zi+1)]
            newv, flag = base_v, False
            if method == 'kgbc':
                prod = [p[1]*clampf(p[0]) for p in P if p[1] is not None]   # KGBC_i * поправка_i
                if len(prod) >= MIN_POINTS:
                    newv, flag = statistics.median(prod), True
            else:  # 'cte'
                if n >= MIN_POINTS:
                    newv, flag = base_v*factor, True
            if flag:
                applied[(xi+1, zi+1)] = newv; changed += 1
            cells.append(dict(zi=zi, xi=xi, n=n, factor=factor,
                              base=base_v, new=newv, applied=flag, match=match, mk=mk))

    # --- пишем .cte ---
    out_cte = os.path.join(out_dir, base_name + ' — ПЦН применено ИИ.cte')
    lines = list(hdr) if hdr else ['[454C2B1D]', 'Name=Поправка ЦН 32х16 по дросселю']
    for z in range(1,17):
        for x in range(1,33):
            lines.append('X%dZ%d=%s' % (x, z, fmt_cte(applied[(x,z)])))
    open(out_cte, 'wb').write(('\r\n'.join(lines)+'\r\n').encode('cp1251'))

    # --- сверка входного cte с логом (констатация факта, не стоп) ---
    mall    = [c for c in cells if c['match'] is not None]
    matched = sum(1 for c in mall if c['match'])
    mism    = [c for c in mall if not c['match']]
    alld    = [abs(p[2]-p[1]) for P in pts.values() for p in P
               if p[1] is not None and p[2] is not None]

    # --- пишем отчёт ---
    out_txt = os.path.join(out_dir, base_name + ' — ПЦН коэффициенты ИИ.txt')
    MNAME = {'kgbc': 'KGBC*поправка (от реального коэф. из лога; значения входного cte НЕ влияют)',
             'cte' : 'вход_cte*поправка (опирается на значения входного cte)'}
    R = []
    R.append('ПОПРАВКА ПЦН ИЗ ЛОГА')
    R.append('лог     : ' + os.path.basename(log_path))
    R.append('исходник: ' + os.path.basename(cte_path))
    R.append('МЕТОД   : ' + method + '  — ' + MNAME[method])
    R.append('поправка = median(AFR_WBL/AFR). <1 богато->режем наполнение, >1 бедно->добавляем.')
    R.append('фильтр: |dRPM|<=%d, |dTHR|<=%d, COEFF~1, БЕЗ ускор.обогащения (DGTC_RICH/LEAN<=%.1f), '
             'минимум %d точек/ячейку, поправка зажата [%.2f..%.2f].'
             % (DRPM_MAX, DTHR_MAX, DGTC_MAX, MIN_POINTS, CLAMP_LO, CLAMP_HI))
    R.append('точек использовано: %d, отброшено (переход/замкн.цикл/обогащение): %d' % (used, skipped))
    R.append('изменено ячеек: %d' % changed)
    R.append('')
    R.append('--- СВЕРКА: тот ли входной cte, что крутился в логе (по KGBC, допуск %.2f) ---' % MATCH_TOL)
    if alld:
        R.append('в целом медиана |вход_cte - лог| = %.3f' % statistics.median(alld))
        R.append('ячеек совпало %d из %d, разошлось %d.' % (matched, len(mall), len(mism)))
        if method == 'kgbc':
            R.append('(метод kgbc: расхождение НЕ портит результат — берём коэф прямо из лога.)')
        else:
            R.append('(метод cte: много расхождений = результат на неверной базе -> лучше метод kgbc.)')
        for c in sorted(mism, key=lambda c: -abs(c['base']-(c['mk'] or c['base'])))[:8]:
            R.append('  расх: об %d, дрос %d%%: вход_cte=%.3f, лог(KGBC)=%.3f'
                     % (RPM[c['xi']], THR[c['zi']], c['base'], c['mk']))
    else:
        R.append('KGBC в логе нет — сверять нечем.')
    R.append('')

    # таблицы (обороты по горизонтали, дроссель по вертикали)
    def grid(title, pick):
        R.append('=== %s ===' % title)
        R.append('THR\\об |' + ''.join('%6d' % r for r in RPM))
        R.append('-'*(8+6*27))
        for zi in range(16):
            s = '%5d%% |' % THR[zi]
            for xi in range(27):
                s += '%6s' % pick(xi,zi)
            R.append(s)
        R.append('')
    cmap = {(c['xi'],c['zi']): c for c in cells}
    def pick_fac(xi,zi):
        c = cmap.get((xi,zi))
        if not c: return '.'
        return ('%.2f' % c['factor']) + ('' if c['applied'] else '~')
    def pick_new(xi,zi):
        c = cmap.get((xi,zi))
        if not c or not c['applied']: return '.'
        return '%.2f' % c['new']
    def pick_cnt(xi,zi):
        c = cmap.get((xi,zi)); return str(c['n']) if c else '.'
    grid('ФАКТОР ПОПРАВКИ AFR_WBL/AFR (~ = точек < %d, НЕ применено)' % MIN_POINTS, pick_fac)
    grid('НОВЫЙ КОЭФ (записан в .cte)', pick_new)
    grid('КОЛИЧЕСТВО ТОЧЕК', pick_cnt)
    open(out_txt, 'w', encoding='utf-8').write('\n'.join(R)+'\n')

    print('готово (метод %s):' % method)
    print('  отчёт :', out_txt)
    print('  .cte  :', out_cte)
    print('  использовано точек %d, изменено ячеек %d' % (used, changed))
    if alld:
        print('  сверка вход_cte<->лог: медиана |Δ|=%.3f, разошлось %d/%d ячеек'
              % (statistics.median(alld), len(mism), len(mall)))

if __name__ == '__main__':
    main()
