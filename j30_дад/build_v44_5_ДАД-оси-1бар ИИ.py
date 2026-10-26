# v44_5 — дочерняя к v44 (код не тронут): тарировка v44_4 + оси под 1 бар наддува.
#
# Решения пользователя 25.10.26:
#   - тарировка как v44_4: смещение 24, наклон 59 — новый датчик читает в шкале
#     старого (атмо завышено на ~5: сегодня настоящая 97 -> 102). Карта VE в этой
#     шкале остаётся в силе, пересчёта топлива НЕТ;
#   - оси под 1 бар (~200 кПа по этой шкале). Старые точки осей до атмосферы
#     СОХРАНЕНЫ, значения в них не меняются вообще; перекроен только верх.
#
# Что меняется:
#   $CA10/$CA11  тарировка 24 / 59
#   $CA00        ось давления VE: 37…100 как было, наддув 120 140 160 180 200
#   $C900        VE: столбцы 0–10 без изменений; 120/140 — интерполяция старой
#                карты; 160…200 — значение последнего старого столбца (142)
#   $C600        таблица давление -> столбец VE (формула «Канал давления ДАД», р. 9)
#   $D200        КВТЗ — формулой Января, как в v44, по новой оси (КТЗ пока 1.0 —
#                на топливо не влияет)
#   $FAF0/$FB10  оси нагрузки смеси и УОЗ: 16…96 как было, наддув 135 170 210
#   $FD00/$FC00  смесь и УОЗ: столбцы 0–12 без изменений; 135 — интерполяция
#                старой карты (128…144); 170/210 — за краем старой оси:
#                смесь не беднее AFR 11.5, угол −1.5° на 10 кПа от столбца 144
#   $FE90        потолок нагрузки 230 на всех оборотах
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "логер", "j30_v44_ТЗ-КТЗ-в-кадре-и-ДТВ-20-при-отказе_02.10.26_2146 ИИ.bin")
BASE = 0x8000

OFS, SLOPE = 0xCA10, 0xCA11
OLD_CAL, NEW_CAL = (7, 34), (24, 59)

VE, PAX, RAX, C600, KVTZ = 0xC900, 0xCA00, 0xCA20, 0xC600, 0xD200
FUEL, FAX, TIM, TAX, CEIL = 0xFD00, 0xFAF0, 0xFC00, 0xFB10, 0xFE90

OLD_PAX = [37, 45, 49, 52, 55, 59, 64, 71, 80, 90, 100, 108, 116, 124, 133, 142]
NEW_PAX = [37, 45, 49, 52, 55, 59, 64, 71, 80, 90, 100, 120, 140, 160, 180, 200]
OLD_LAX = [16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 96, 112, 128, 144]
NEW_LAX = [16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 96, 135, 170, 210]
CEIL_NEW = 230

BOOST_AFR = 11.5                     # за краем старой оси смесь не беднее этого
UOZ_DROP_PER_10KPA = 1.5


def rd(b, a, n):
    return list(b[a - BASE:a - BASE + n])


def wr(b, a, vals):
    b[a - BASE:a - BASE + len(vals)] = bytes(vals)


# ---------------------------------------------------------------- давление
def c600_table(ax):
    """Байт = (столбец << 4) | дробь, округление вверх от половины (как редактор)."""
    t = []
    for k in range(256):
        if k <= ax[0]:
            t.append(0x00); continue
        if k >= ax[15]:
            t.append(0xF0); continue
        i = max(j for j in range(15) if ax[j] <= k)
        fr = int((k - ax[i]) * 16 / (ax[i + 1] - ax[i]) + 0.5)
        t.append((i << 4) | max(0, min(15, fr)))
    return t


def ve_at(ve, tab, r, p):
    """VE строки r при давлении p — так же, как берёт блок: столбец и дробь из $C600."""
    k = max(0, min(255, int(p)))
    c, fr = tab[k] >> 4, tab[k] & 0x0F
    a = ve[r * 16 + c]
    bb = ve[r * 16 + min(c + 1, 15)]
    return (a + (bb - a) * fr / 16.0) / 128.0


def new_ve(old_ve, old_tab):
    return [max(1, min(255, int(ve_at(old_ve, old_tab, r, p) * 128 + 0.5)))
            for r in range(16) for p in NEW_PAX]


def fill_kvtz(start_rpm8, pax, ve):
    """КВТЗ по формуле Января (как в build_v44): min(1, Q/800)·(0.8984375−0.25)+0.25."""
    tab = []
    for r in range(16):
        rpm = (start_rpm8 + 16 * r) * 2 * 12.807
        for c in range(16):
            rho = pax[c] * 1000.0 / (287.05 * 293.15)
            q = rpm / 120.0 * 2.96e-3 * rho * (ve[r * 16 + c] / 128.0) * 3600.0
            kv = min(1.0, q / 800.0) * (0.8984375 - 0.25) + 0.25
            tab.append(max(0, min(128, int(round(kv * 128)))))
    return tab


# ---------------------------------------------------------------- смесь / УОЗ
def afr_dec(x):
    return 1881.6 / ((x - 64) if x >= 128 else (x + 128))


def afr_enc(v, hi):
    """Две кодировки: hi (байт >= 128) — около стехиометрии, флаг замкнутого цикла
    (189…194 = AFR 15.0…14.4); иначе (< 128) — обогащение, 0 = 14.7."""
    if hi:
        return max(128, min(255, int(64 + 1881.6 / v + 0.5)))
    return max(0, min(127, int(1881.6 / v - 128 + 0.5)))


def interp_pos(ax, x):
    """Индекс и доля x на оси ax; за краями — зажим."""
    if x <= ax[0]:
        return 0, 0.0
    if x >= ax[15]:
        return 15, 0.0
    i = max(j for j in range(15) if ax[j] <= x)
    return i, (x - ax[i]) / float(ax[i + 1] - ax[i])


def kpa_of_load(load):
    # по логам v39/v42 выше атмосферы: нагрузка ≈ 1.25·кПа − 45
    return (load + 45) / 1.25


def remap_fuel(old, oax):
    out = []
    for r in range(16):
        row = old[r * 16:(r + 1) * 16]
        for L in NEW_LAX:
            i, f = interp_pos(oax, L)
            if L > oax[15]:
                out.append(afr_enc(min(afr_dec(row[15]), BOOST_AFR), False))
            elif f == 0:
                out.append(row[i])                                  # точка оси совпала
            else:
                a, bb = afr_dec(row[i]), afr_dec(row[i + 1])
                hi = (row[i] if f < 0.5 else row[i + 1]) >= 128     # кодировка ближайшего
                out.append(afr_enc(a + (bb - a) * f, hi))
    return out


def remap_timing(old, oax):
    """Байт < 128 — градусы; >= 128 — флаг + градусы (128 + °). Флаг берём у
    ближайшего старого столбца, градусы интерполируем."""
    out = []
    for r in range(16):
        row = old[r * 16:(r + 1) * 16]
        deg = [x & 0x7F if x >= 128 else x for x in row]
        flg = [x >= 128 for x in row]
        for L in NEW_LAX:
            i, f = interp_pos(oax, L)
            if L > oax[15]:
                d = deg[15] - UOZ_DROP_PER_10KPA * (kpa_of_load(L) - kpa_of_load(oax[15])) / 10.0
                fl = flg[15]
            elif f == 0:
                out.append(row[i]); continue
            else:
                d = deg[i] + (deg[i + 1] - deg[i]) * f
                fl = flg[i] if f < 0.5 else flg[i + 1]
            d = max(0, min(89, int(d + 0.5)))
            out.append((128 + d) if fl else d)
    return out


# ---------------------------------------------------------------- запас в наддуве
# На верхнем участке точек стало меньше (VE: 108/116/124/133 -> 120/140; нагрузка:
# 112/128/144 -> 135), и прямая между новыми точками местами шла беднее/раньше
# старой карты. Здесь наддувные точки двигаются ТОЛЬКО в безопасную сторону,
# пока на всём старом участке (по каждому целому кПа / каждой единице нагрузки)
# новое не станет не беднее, не раньше и VE не ниже старого.
def lin(ax, vals, x):
    i, f = interp_pos(ax, x)
    return vals[i] + (vals[min(i + 1, 15)] - vals[i]) * f


def safe_ve(ve, old_ve, old_tab):
    ve = list(ve)
    for r in range(16):
        old = {p: ve_at(old_ve, old_tab, r, p) * 128 for p in range(100, 143)}
        for _ in range(200):
            row = ve[r * 16:r * 16 + 16]
            bad = [p for p in old if lin(NEW_PAX, row, p) < old[p] - 0.01]
            if not bad:
                break
            p = bad[0]
            c = 11 if p <= 120 else 12                  # точка 120 или 140
            ve[r * 16 + c] = min(255, ve[r * 16 + c] + 1)
    return ve


def safe_fuel(nf, old):
    nf = list(nf)
    for r in range(16):
        oa = [afr_dec(x) for x in old[r * 16:r * 16 + 16]]
        target = {L: lin(OLD_LAX, oa, L) for L in range(96, 145)}
        for _ in range(127):
            na = [afr_dec(x) for x in nf[r * 16:r * 16 + 16]]
            if all(lin(NEW_LAX, na, L) <= target[L] + 0.005 for L in target):
                break
            c = r * 16 + 13                              # точка 135 — богаче на шаг
            x = nf[c]
            nf[c] = min(127, x + 1) if x < 128 else max(0, int(1881.6 / afr_dec(x) - 128 + 0.5) + 1)
        # с ростом наддува смесь не беднеет: 170 и 210 не беднее предыдущей точки
        for c in (14, 15):
            prev = afr_dec(nf[r * 16 + c - 1])
            if afr_dec(nf[r * 16 + c]) > prev:
                nf[r * 16 + c] = afr_enc(prev, False)
    return nf


def safe_timing(nt, old):
    nt = list(nt)
    for r in range(16):
        od = [x & 0x7F for x in old[r * 16:r * 16 + 16]]
        target = {L: lin(OLD_LAX, od, L) for L in range(96, 145)}
        for _ in range(90):
            nd = [x & 0x7F for x in nt[r * 16:r * 16 + 16]]
            if all(lin(NEW_LAX, nd, L) <= target[L] + 0.01 for L in target):
                break
            c = r * 16 + 13                              # точка 135 — позже на градус
            x = nt[c]
            if (x & 0x7F) == 0:
                break
            nt[c] = x - 1
        # с ростом наддува угол не растёт: 170 и 210 не раньше предыдущей точки
        for c in (14, 15):
            x, prev = nt[r * 16 + c], nt[r * 16 + c - 1] & 0x7F
            if (x & 0x7F) > prev:
                nt[r * 16 + c] = (x & 0x80) | prev
    return nt


def checksum(b):
    s = x = 0
    for i, v in enumerate(b):
        if i in (0x7F7A, 0x7F7B):
            continue
        s = (s + v) & 0xFF
        x ^= v
    b[0x7F7A], b[0x7F7B] = s, x


def build(out_path):
    b = bytearray(open(SRC, "rb").read())
    assert len(b) == 32768
    assert (b[OFS - BASE], b[SLOPE - BASE]) == OLD_CAL
    old_pax, old_ve, old_tab = rd(b, PAX, 16), rd(b, VE, 256), rd(b, C600, 256)
    assert old_pax == OLD_PAX
    assert c600_table(old_pax) == old_tab, "формула $C600 не совпала со старой таблицей"
    old_fuel, old_tim = rd(b, FUEL, 256), rd(b, TIM, 256)
    assert rd(b, FAX, 16) == OLD_LAX and rd(b, TAX, 16) == OLD_LAX
    assert all(x < 128 or 185 <= x <= 200 for x in old_fuel), "в карте смеси неожиданные байты"
    assert all(x < 90 or x >= 128 for x in old_tim), "в карте УОЗ байты 90…127"

    b[OFS - BASE], b[SLOPE - BASE] = NEW_CAL
    ve = safe_ve(new_ve(old_ve, old_tab), old_ve, old_tab)
    wr(b, PAX, NEW_PAX); wr(b, VE, ve); wr(b, C600, c600_table(NEW_PAX))
    wr(b, KVTZ, fill_kvtz(b[RAX - BASE] * 2, NEW_PAX, ve))
    wr(b, FAX, NEW_LAX); wr(b, TAX, NEW_LAX)
    wr(b, FUEL, safe_fuel(remap_fuel(old_fuel, OLD_LAX), old_fuel))
    wr(b, TIM, safe_timing(remap_timing(old_tim, OLD_LAX), old_tim))
    wr(b, CEIL, [CEIL_NEW] * 16)
    checksum(b)
    open(out_path, "wb").write(b)
    return b, dict(old_ve=old_ve, old_tab=old_tab, old_fuel=old_fuel, old_tim=old_tim, ve=ve)


def report(b, o):
    new_tab = rd(b, C600, 256)
    print("тарировка $CA10/$CA11 = %d / %d" % (b[OFS - BASE], b[SLOPE - BASE]))
    # VE: новое против старого при одном давлении (в шкале старого датчика)
    dmax = {}
    for r in range(16):
        for p in range(37, 143):
            n, s = ve_at(o["ve"], new_tab, r, p), ve_at(o["old_ve"], o["old_tab"], r, p)
            z = "до 100" if p <= 100 else "100…142"
            dmax[z] = max(dmax.get(z, 0), abs(n / s - 1) * 100)
    print("VE новое против старого, макс. расхождение: " +
          ", ".join("%s кПа %.1f%%" % kv for kv in dmax.items()))
    # знак расхождений в верхней зоне: должно быть только в безопасную сторону
    lo = min(ve_at(o["ve"], new_tab, r, p) / ve_at(o["old_ve"], o["old_tab"], r, p) - 1
             for r in range(16) for p in range(100, 143))
    nf0, nt0 = rd(b, FUEL, 256), rd(b, TIM, 256)
    fmax = max(lin(NEW_LAX, [afr_dec(x) for x in nf0[r * 16:r * 16 + 16]], L) -
               lin(OLD_LAX, [afr_dec(x) for x in o["old_fuel"][r * 16:r * 16 + 16]], L)
               for r in range(16) for L in range(96, 145))
    tmax = max(lin(NEW_LAX, [x & 0x7F for x in nt0[r * 16:r * 16 + 16]], L) -
               lin(OLD_LAX, [x & 0x7F for x in o["old_tim"][r * 16:r * 16 + 16]], L)
               for r in range(16) for L in range(96, 145))
    print("ЗАПАС: VE ниже старого не более %.1f%%, смесь беднее не более %+.2f AFR, угол раньше не более %+.1f°"
          % (-lo * 100, fmax, tmax))
    nf, nt = rd(b, FUEL, 256), rd(b, TIM, 256)
    df = {}; dt = {}
    for r in range(16):
        for L in range(16, 145):
            z = "до 96" if L <= 96 else "96…144"
            i, f = interp_pos(OLD_LAX, L); j, g = interp_pos(NEW_LAX, L)
            ro, rn = o["old_fuel"][r * 16:r * 16 + 16], nf[r * 16:r * 16 + 16]
            a = afr_dec(ro[i]) + (afr_dec(ro[min(i + 1, 15)]) - afr_dec(ro[i])) * f
            c = afr_dec(rn[j]) + (afr_dec(rn[min(j + 1, 15)]) - afr_dec(rn[j])) * g
            df[z] = max(df.get(z, 0), abs(a - c))
            to = [x & 0x7F for x in o["old_tim"][r * 16:r * 16 + 16]]
            tn = [x & 0x7F for x in nt[r * 16:r * 16 + 16]]
            a = to[i] + (to[min(i + 1, 15)] - to[i]) * f
            c = tn[j] + (tn[min(j + 1, 15)] - tn[j]) * g
            dt[z] = max(dt.get(z, 0), abs(a - c))
    print("смесь, макс. расхождение AFR: " + ", ".join("%s %.2f" % kv for kv in df.items()))
    print("УОЗ,   макс. расхождение °:   " + ", ".join("%s %.1f" % kv for kv in dt.items()))
    frpm, trpm = [x * 50 for x in rd(b, 0xFB00, 16)], [x * 50 for x in rd(b, 0xFB20, 16)]
    print("\nНАДДУВНЫЕ СТОЛБЦЫ нагрузки 96 / 135 / 170 / 210:")
    for r in (6, 8, 10, 12, 15):
        print("  смесь %4d об: AFR %s     УОЗ %4d об: %s" % (
            frpm[r], " / ".join("%.1f" % afr_dec(nf[r * 16 + c]) for c in (12, 13, 14, 15)),
            trpm[r], " / ".join(str(nt[r * 16 + c]) for c in (12, 13, 14, 15))))
    print("\nVE, строки 2400 / 4000 / 6000 об, столбцы 100 / 120 / 140 / 160…200:")
    for r in (5, 9, 14):
        print("  " + " / ".join("%.2f" % (o["ve"][r * 16 + c] / 128) for c in (10, 11, 12, 13, 14, 15)))
    print("VE байт мин/макс:", min(o["ve"]), max(o["ve"]))


if __name__ == "__main__":
    import sys
    b, o = build(sys.argv[1])
    report(b, o)
    print("\nзаписан:", sys.argv[1])
