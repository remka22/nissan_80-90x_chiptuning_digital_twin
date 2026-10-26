# -*- coding: utf-8 -*-
"""
Генератор платы-переходника J30: FM18W08 (SOP-28) + GAL16V8B (DIP-20) на штырях DIP-28.

Запуск — ТОЛЬКО питоном из KiCad (в нём модуль pcbnew):
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 gen_board.py

Плата строится целиком из этого файла: расстановка, дорожки, переходные. Руками
файл платы не правим — правим здесь и перегенерируем, иначе правки потеряются.

ТЕХЗАДАНИЕ (согласовано 02.10.26):
  - габарит не больше 40 x 50 мм, левая сторона — по ряду DIP-28;
  - штыри DIP-28, ряды через 15.24 мм, левый ряд прижат к левому краю,
    ключ (нога 1) в левом верхнем углу;
  - FM18W08 в SOP-28, GAL16V8B впаяна (DIP-20 без панельки);
  - 4 отверстия под провода над ключом GAL, шаг 2.54, слева направо
    A(E) B(A15) C(A14) D(R/W) — как на ЭБУ (сверено с инструкцией Nistune
    Type 1, раздел J30 Maxima);
  - ⚠ входы GAL ПЕРЕСТАВЛЕНЫ под этот ряд: нога 2 = E, 3 = A15, 4 = R/W
    (было 2 = R/W, 3 = E, 4 = A15). Иначе R/W с правого отверстия режет E и A15.
    GAL шьётся НОВЫМ файлом gal_board_rev02.jed из этой папки — и в нём же
    исправлена полярность /WE (в j30/gal_fm18w08.jed ревизии 01 она перевёрнута);
  - три переключателя на нулевых резисторах «или-или»: рабочий режим / прошивка
    в программаторе 62256, плюс /CE на будущее (из GAL вместо штатного).

ГЛАВНОЕ ПРО РАЗВОДКУ FM:
  FM стоит МЕЖДУ рядами штырей, нога N FM напротив штыря N — распиновки EPROM и
  SRAM совпадают во всём, кроме ног 1 и 27 (и /CE мы тоже пускаем через
  переключатель). Шаг FM 1.27, шаг штырей 2.54: веер 2:1 на одном слое не
  пролезает (между штырём и площадкой FM 1.2 мм на три дорожки). Поэтому все
  прямые связи идут ВЕЕРОМ ПО НИЖНЕМУ СЛОЮ и поднимаются переходными ПОД КОРПУСОМ
  FM к внутренним концам площадок. Верхний слой внутри DIP остаётся свободным под
  переключатели, конденсатор и землю.
"""
import os
import pcbnew as p

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "j30_fm18w08_gal.kicad_pcb")
FPL = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

OX, OY = 100.0, 100.0          # левый верхний угол платы в координатах KiCad
BW, BH = 34.6, 39.0            # габарит платы, мм (потолок по ТЗ 50 x 40)

TR = 0.2                       # сигнальная дорожка
TP = 0.5                       # питание
VIA_D, VIA_H = 0.6, 0.3        # переходное: диаметр / сверло

b = p.BOARD()
mm = p.FromMM


def V(x, y):
    return p.VECTOR2I(mm(OX + x), mm(OY + y))


# ---------------------------------------------------------------- цепи
NETS = {}


def net(name):
    if name not in NETS:
        n = p.NETINFO_ITEM(b, name)
        b.Add(n)
        NETS[name] = n
    return NETS[name]


# распиновка EPROM 27C256 в панели ЭБУ == SRAM 62256 / FM18W08, кроме ног 1 и 27
EPROM = {2: "A12", 3: "A7", 4: "A6", 5: "A5", 6: "A4", 7: "A3", 8: "A2", 9: "A1",
         10: "A0", 11: "D0", 12: "D1", 13: "D2", 15: "D3", 16: "D4", 17: "D5",
         18: "D6", 19: "D7", 21: "A10", 22: "/OE", 23: "A11", 24: "A9", 25: "A8",
         26: "A13"}

CONN = {
    "VCC": [("J1", 28), ("U1", 28), ("U2", 20), ("C1", 2), ("C2", 1)],
    "GND": [("J1", 14), ("U1", 14), ("U2", 10), ("U2", 11), ("C1", 1), ("C2", 2)],
    # переключатель A14: R1 рабочий (контакт C), R2 прошивка (штырь 1)
    "FM_A14": [("U1", 1), ("R1", 1), ("R2", 1)],
    "A14": [("R1", 2), ("J2", 3)],
    "PIN1_PRG": [("R2", 2), ("J1", 1)],
    # переключатель /WE: R3 рабочий (GAL 19), R4 прошивка (штырь 27)
    "FM_/WE": [("U1", 27), ("R3", 1), ("R4", 1)],
    "GAL_/WE": [("R3", 2), ("U2", 19)],
    "PIN27_PRG": [("R4", 2), ("J1", 27)],
    # переключатель /CE: R5 штатный (штырь 20), R6 на будущее (GAL 18)
    "FM_/CE": [("U1", 20), ("R5", 1), ("R6", 1)],
    "/CE": [("R5", 2), ("J1", 20)],
    "GAL_/CE": [("R6", 2), ("U2", 18)],
    # отверстия от ЭБУ
    # входы GAL переставлены под ряд отверстий (см. шапку)
    "E": [("J2", 1), ("U2", 2)],
    "A15": [("J2", 2), ("U2", 3)],
    "R/W": [("J2", 4), ("U2", 4)],
}
for pin, name in EPROM.items():
    CONN[name] = [("J1", pin), ("U1", pin)]

# ---------------------------------------------------------------- компоненты
FP = {}
STRIP = []
IO = p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP)


def place(ref, lib, name, x, y, rot=0, value="", dnp=False, keep_graphics=True):
    # Не p.FootprintLoad: в KiCad 10 вторая загрузка через него падает
    # («SwigPyObject has no attribute FootprintLoad»). Через плагин — стабильно.
    f = IO.FootprintLoad(os.path.join(FPL, lib + ".pretty"), name)
    f.SetReference(ref)
    f.SetValue(value or name)
    f.SetPosition(V(x, y))
    f.SetOrientationDegrees(rot)
    f.Value().SetVisible(False)
    f.Reference().SetTextSize(p.VECTOR2I(mm(0.8), mm(0.8)))
    f.Reference().SetTextThickness(mm(0.12))
    if dnp:
        f.SetDNP(True)
    if not keep_graphics:
        STRIP.append(f)          # снимем в самом конце, см. перед b.Save
    b.Add(f)
    FP[ref] = f
    return f


# Штыри DIP-28: левый ряд x=1.3 (кромка площадки в 0.5 мм от края платы),
# нога 1 вверху. Графику посадочного места снимаем: она рисует корпус МЕЖДУ
# рядами, а там у нас стоит FM — получилась бы каша и ложные ошибки проверки.
X_L, Y1 = 1.3, 3.49
X_R = X_L + 15.24
place("J1", "Package_DIP", "DIP-28_W15.24mm", X_L, Y1, value="ШТЫРИ В ПАНЕЛЬ ЭБУ",
      keep_graphics=False)

# FM18W08 ровно посередине между рядами, нога 1 вверху слева
FMX, FMY = (X_L + X_R) / 2, Y1 + 16.51
place("U1", "Package_SO", "SOIC-28W_7.5x17.9mm_P1.27mm", FMX, FMY, value="FM18W08-SG")

# GAL впаяна — обычное DIP-20, без рамки панельки
GX, GY = 23.0, 8.57             # вплотную к R5/R6: отверстия ушли наверх, место между FM и GAL не нужно
place("U2", "Package_DIP", "DIP-20_W7.62mm", GX, GY, value="GAL16V8B")

# Отверстия под провода от ЭБУ — ряд над ключом GAL, A над ногой 1, D над ногой 20.
# Повёрнуты на 90°: ряд идёт вправо. Графику (рамку разъёма) снимаем — это
# просто отверстия, подписи A-D рисуем сами.
JX, JY = GX, 4.0
place("J2", "Connector_PinHeader_2.54mm", "PinHeader_1x04_P2.54mm_Vertical", JX, JY, 90,
      value="ЭБУ A B C D", keep_graphics=False)

R0805 = ("Resistor_SMD", "R_0805_2012Metric")
C0805 = ("Capacitor_SMD", "C_0805_2012Metric")
# 0° — площадка 1 слева; 180° — справа; 270° — сверху
place("R2", *R0805, 5.2, 4.2, 180, "0R", dnp=True)     # A14 прошивка
place("R1", *R0805, 9.2, 4.2, 0, "0R")                 # A14 рабочий
place("R3", *R0805, 13.6, 3.2, 0, "0R")                # /WE рабочий
place("R4", *R0805, 13.6, 6.03, 0, "0R", dnp=True)     # /WE прошивка
place("C1", *C0805, 12.0, 9.3, 0, "100n")
place("R5", *R0805, 18.6, 25.0, 270, "0R")             # /CE штатный
place("R6", *R0805, 20.6, 25.0, 270, "0R", dnp=True)   # /CE из GAL — на будущее
place("C2", *C0805, GX + 10.2, 9.5, 270, "100n")

# назначить цепи площадкам
for name, pins in CONN.items():
    n = net(name)
    for ref, num in pins:
        pads = [pd for pd in FP[ref].Pads() if pd.GetNumber() == str(num)]
        assert pads, (ref, num)
        for pd in pads:
            pd.SetNet(n)


def P(ref, num):
    for pd in FP[ref].Pads():
        if pd.GetNumber() == str(num):
            q = pd.GetPosition()
            return (p.ToMM(q.x) - OX, p.ToMM(q.y) - OY)
    raise KeyError((ref, num))


# ---------------------------------------------------------------- дорожки
def path(name, pts, layer="F", w=TR):
    lay = p.F_Cu if layer == "F" else p.B_Cu
    pts = [P(*q) if isinstance(q[0], str) else q for q in pts]
    for a, c in zip(pts, pts[1:]):
        t = p.PCB_TRACK(b)
        t.SetStart(V(*a))
        t.SetEnd(V(*c))
        t.SetWidth(mm(w))
        t.SetLayer(lay)
        t.SetNet(net(name))
        b.Add(t)


def via(name, x, y):
    v = p.PCB_VIA(b)
    v.SetPosition(V(x, y))
    v.SetDrill(mm(VIA_H))
    v.SetWidth(mm(VIA_D))
    v.SetNet(net(name))
    b.Add(v)


def pin_y(k):                    # штырь DIP / нога FM по номеру 1..28
    return P("J1", k)[1]


# ---- веер: штырь -> нижний слой -> переходное под корпусом -> площадка FM
VIA_L = P("U1", 2)[0] + 1.025 + 0.35      # чуть правее внутреннего конца левых площадок
VIA_R = P("U1", 27)[0] - 1.025 - 0.35
FAN_SKIP = {1, 20, 27}                    # эти идут через переключатели


def fan(k, vx):
    """прямая связь штырь k <-> нога FM k"""
    name = EPROM.get(k) or ("GND" if k == 14 else "VCC")
    jx, jy = P("J1", k)
    fx, fy = P("U1", k)
    vxx = VIA_L if fx < FMX else VIA_R
    path(name, [(jx, jy), (vx, jy), (vx, fy), (vxx, fy)], "B")
    via(name, vxx, fy)
    path(name, [(vxx, fy), (fx, fy)], "F")


# левый ряд: внешние дорожки ближе к переходным, иначе пересекутся
up_l = [k for k in range(2, 8)]                 # 2..7 спускаются
for i, k in enumerate(up_l):
    fan(k, 5.1 - i * 0.5)
lo_l = [k for k in range(14, 7, -1)]            # 14..8 поднимаются
for i, k in enumerate(lo_l):
    fan(k, 5.1 - i * 0.45)
# правый ряд (зеркально)
up_r = [n for n in range(28, 21, -1) if n not in FAN_SKIP]   # 28,26..22
for i, n in enumerate(up_r):
    fan(n, 12.74 + i * 0.5)
lo_r = [n for n in range(15, 22) if n not in FAN_SKIP]       # 15..19,21
for i, n in enumerate(lo_r):
    fan(n, 12.74 + i * 0.5)

# ---- переключатель A14 (R1/R2)
fx, fy = P("U1", 1)
path("FM_A14", [(fx, fy), (fx, 7.0), (7.2, 7.0), (7.2, 4.2)])
path("FM_A14", [("R2", 1), ("R1", 1)])
jx, jy = P("J1", 1)
path("PIN1_PRG", [(jx, jy), (2.6, jy), (3.3, 4.2), ("R2", 2)])
# A14 от отверстия C — полосой вдоль верхнего края, над штырём 28 и над A, B,
# и сверху прямо в C. Ряд отверстий ниже полосы, поэтому пересечений нет.
cx, cy = P("J2", 3)
path("A14", [("R1", 2), (P("R1", 2)[0], 1.4), (cx, 1.4), (cx, cy)])

# ---- переключатель /WE (R3/R4)
fx, fy = P("U1", 27)
path("FM_/WE", [(fx, fy), (15.0, fy), (15.0, 7.6), (11.9, 7.6), (11.9, 3.2), ("R3", 1)])
path("FM_/WE", [(11.9, P("R4", 1)[1]), ("R4", 1)])
path("PIN27_PRG", [("R4", 2), ("J1", 27)])
# /WE от GAL: наверху выходит между штырями 28 и 27, дальше нижним слоем
WEY = (pin_y(28) + pin_y(27)) / 2
r3 = P("R3", 2)
path("GAL_/WE", [r3, (15.0, r3[1] + 0.5), (15.0, WEY), (18.6, WEY)])
via("GAL_/WE", 18.6, WEY)
gx19, gy19 = P("U2", 19)
MIDX = GX + 3.81                       # середина между рядами GAL
# Внизу идёт полосой ПОД рядом отверстий (между ними и ногами GAL), потом
# серединой GAL вниз к ноге 19.
WEB = 6.2
path("GAL_/WE", [(18.6, WEY), (20.0, WEB), (MIDX, WEB), (MIDX, gy19), (gx19, gy19)], "B")

# ---- переключатель /CE (R5/R6)
fx, fy = P("U1", 20)
CEY = (pin_y(21) + pin_y(20)) / 2      # выход между штырями 21 и 20
path("FM_/CE", [(fx, fy), (14.9, fy), (15.4, CEY), (P("R6", 1)[0], CEY), ("R6", 1)])
path("FM_/CE", [(P("R5", 1)[0], CEY), ("R5", 1)])
r5 = P("R5", 2)
path("/CE", [r5, (17.7, r5[1]), ("J1", 20)])
# /CE из GAL (на будущее): между ногами GAL 7 и 8, вверх серединой к ноге 18
GCY = (P("U2", 7)[1] + P("U2", 8)[1]) / 2
r6 = P("R6", 2)
gx18, gy18 = P("U2", 18)
path("GAL_/CE", [r6, (r6[0] + 0.83, GCY), (MIDX, GCY), (MIDX, gy18), (gx18, gy18)])

# ---- отверстия от ЭБУ -> GAL, верхним слоем, без пересечений
# Спускаются в середину GAL и заходят в ноги 2, 3, 4 изнутри. Чем выше нога,
# тем ближе к левому ряду её вертикаль — поэтому порядок входов в GAL и
# переставлен под порядок отверстий (см. шапку).
ax, ay = P("J2", 1)
bx, by = P("J2", 2)
dx, dy = P("J2", 4)
g2x, g2y = P("U2", 2)
g3x, g3y = P("U2", 3)
g4x, g4y = P("U2", 4)
path("E", [(ax, ay), (GX + 1.2, ay + 1.2), (GX + 1.2, g2y), (g2x, g2y)])
path("A15", [(bx, by), (bx, by + 1.0), (GX + 1.7, by + 1.84), (GX + 1.7, g3y), (g3x, g3y)])
path("R/W", [(dx, dy), (GX + 6.4, dy + 1.22), (GX + 3.0, dy + 1.22), (GX + 2.2, dy + 2.02), (GX + 2.2, g4y), (g4x, g4y)])

# ---- питание
# VCC: штырь 28 -> GAL 20 нижним слоем, в обход ряда отверстий: вдоль верхнего
# края и вниз правее GAL
g20x, g20y = P("U2", 20)
VTOP, VRX = 1.0, GX + 9.2
path("VCC", [("J1", 28), (P("J1", 28)[0], VTOP), (VRX, VTOP), (VRX, g20y), (g20x, g20y)], "B", TP)
# C1 у FM: VCC с ноги 28 FM, земля — «хребтом» под корпусом от ноги 14
f28x, f28y = P("U1", 28)
c1v = P("C1", 2)
path("VCC", [(f28x, f28y), (f28x, 10.0), c1v])
gv = (VIA_L, P("U1", 14)[1])
path("GND", [gv, (FMX, gv[1]), (FMX, P("C1", 1)[1]), ("C1", 1)], "F", 0.3)
# C2 у GAL
path("VCC", [(g20x, g20y), ("C2", 1)], "F", TP)
c2g = P("C2", 2)
GVX, GVY = c2g[0], c2g[1] + 1.4              # переходное земли под C2
via("GND", GVX, GVY)
path("GND", [c2g, (GVX, GVY)], "F", TP)
# земля: штырь 14 -> вдоль нижнего края -> GAL 10, 11 и C2
j14 = P("J1", 14)
g10 = P("U2", 10)
g11 = P("U2", 11)
GB = 38.2
path("GND", [j14, (j14[0], GB), (g10[0], GB), g10], "B", TP)
path("GND", [(g10[0], g10[1] + 1.77), (g11[0], g10[1] + 1.77), g11], "B", TP)
path("GND", [(GVX, GVY), (GVX, g10[1] + 1.77), (g11[0], g10[1] + 1.77)], "B", TP)

# ---------------------------------------------------------------- контур и надписи
r = p.PCB_SHAPE(b)
r.SetShape(p.SHAPE_T_RECT)
r.SetStart(V(0, 0))
r.SetEnd(V(BW, BH))
r.SetLayer(p.Edge_Cuts)
r.SetWidth(mm(0.1))
b.Add(r)


def text(s, x, y, h=0.8, layer=p.F_SilkS):
    t = p.PCB_TEXT(b)
    t.SetText(s)
    t.SetPosition(V(x, y))
    t.SetTextSize(p.VECTOR2I(mm(h), mm(h)))
    t.SetTextThickness(mm(h * 0.15))
    t.SetLayer(layer)
    b.Add(t)


def back(s, x, y, h=0.9):
    t = p.PCB_TEXT(b)
    t.SetText(s)
    t.SetPosition(V(x, y))
    t.SetTextSize(p.VECTOR2I(mm(h), mm(h)))
    t.SetTextThickness(mm(h * 0.15))
    t.SetLayer(p.B_SilkS)
    t.SetMirrored(True)
    b.Add(t)


# лицо: только то, что нужно при пайке
text("J30 FM18W08+GAL v1", GX + 3.81, 35.6, 0.8)
for i, s in enumerate("ABCD"):
    text(s, P("J2", i + 1)[0], 2.35, 0.8)    # над отверстиями
text("1", X_L, 1.6, 0.8)                      # ключ штырей
# обратная сторона: памятка по перемычкам (деталей там нет — места полно)
# внутри DIP на обороте нет открытых площадок — только закрытые маской переходные
for i, s in enumerate(["J30 FM18W08+GAL v1",
                       "A=E  B=A15",
                       "C=A14  D=RW",
                       "РАБОТА: R1 R3 R5",
                       "ПРОШИВКА: R2 R4",
                       "CE ИЗ GAL: R6"]):
    back(s, FMX, 24.0 + i * 2.0, 0.8)

# обозначения деталей — вручную, где свободно
REFPOS = {"R2": (5.2, 2.6), "R1": (9.0, 2.6), "R3": (13.6, 1.9), "R4": (13.6, 7.85),
          "C1": (9.8, 9.3), "R5": (18.6, 27.4), "R6": (20.8, 27.4), "C2": (GX + 10.2, 7.0),
          "U1": (FMX, FMY), "U2": (MIDX, 20.0), "J1": (6.0, 38.2), "J2": (GX - 1.6, JY)}
for ref, (x, y) in REFPOS.items():
    FP[ref].Reference().SetPosition(V(x, y))
    FP[ref].Reference().SetTextAngleDegrees(0)

# ---------------------------------------------------------------- правила
ds = b.GetDesignSettings()
ds.m_TrackMinWidth = mm(0.15)
ds.m_MinClearance = mm(0.15)
ds.m_ViasMinSize = mm(0.5)
ds.m_MinThroughDrill = mm(0.3)
ds.m_CopperEdgeClearance = mm(0.3)

# Снятие графики с посадочного места ломает SWIG-обвязку KiCad 10: все
# последующие загрузки возвращают пустой объект. Поэтому — только здесь, когда
# больше ничего создавать не нужно.
for f in STRIP:
    for g in list(f.GraphicalItems()):
        f.Remove(g)
    f.Models().clear()       # иначе в 3D на штырях рисуется корпус микросхемы и закрывает FM

b.Save(OUT)
print("сохранено:", OUT)
