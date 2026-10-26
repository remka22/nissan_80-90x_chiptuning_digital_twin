# -*- coding: utf-8 -*-
"""
Выгрузка платы в формат KiCad 5 — для импорта в EasyEDA Pro.

ЗАЧЕМ: EasyEDA Pro импортирует только KiCad 5.1/5.9 (так в их документации).
Файл KiCad 10 она отвергла: «Unexpected error while converting». А сам KiCad 10
сохранять в старый формат не умеет. Поэтому пишем старый формат сами, обходя
готовую плату j30_fm18w08_gal.kicad_pcb (её строит gen_board.py).

ПРОВЕРКА: KiCad 10 читает файлы KiCad 5. После выгрузки на ней же гоняется DRC —
если там 0 нарушений и 0 разрывов, при переводе ничего не потерялось.

Запуск питоном из KiCad:
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 export_kicad5.py
"""
import math
import os
import pcbnew as p

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "j30_fm18w08_gal.kicad_pcb")
OUTDIR = os.path.join(HERE, "easyeda_kicad5")
OUT = os.path.join(OUTDIR, "j30_fm18w08_gal.kicad_pcb")

b = p.LoadBoard(SRC)
mm = p.ToMM

# имена слоёв KiCad 10 -> KiCad 5 (с 6-й версии часть слоёв переименовали)
LAYER = {"F.Cu": "F.Cu", "B.Cu": "B.Cu",
         "F.Silkscreen": "F.SilkS", "B.Silkscreen": "B.SilkS",
         "F.Courtyard": "F.CrtYd", "B.Courtyard": "B.CrtYd",
         "F.Fab": "F.Fab", "B.Fab": "B.Fab",
         "F.Mask": "F.Mask", "B.Mask": "B.Mask",
         "F.Paste": "F.Paste", "B.Paste": "B.Paste",
         "Edge.Cuts": "Edge.Cuts"}


def lay(item_layer):
    return LAYER.get(b.GetLayerName(item_layer))


def f(v):
    s = ("%.4f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---------------------------------------------------------------- цепи
nets = {}
for code, ni in b.GetNetInfo().NetsByNetcode().items():
    nets[code] = ni.GetNetname()


def netref(item):
    """у площадок в KiCad 5 цепь с именем: (net 2 "VCC")"""
    c = item.GetNetCode()
    return "(net %d %s)" % (c, q(nets[c])) if c > 0 else ""


def netnum(item):
    """у дорожек и переходных — только номер: (net 2)"""
    return "(net %d)" % item.GetNetCode()


# ---------------------------------------------------------------- геометрия
def to_local(fp, x, y):
    """абсолютные мм -> система посадочного места (без поворота)"""
    ox, oy = mm(fp.GetPosition().x), mm(fp.GetPosition().y)
    a = math.radians(fp.GetOrientationDegrees())
    dx, dy = x - ox, y - oy
    # KiCad: ось Y вниз, положительный угол — против часовой на экране
    lx = dx * math.cos(a) - dy * math.sin(a)
    ly = dx * math.sin(a) + dy * math.cos(a)
    return lx, ly


def arc_points(sh, n=12):
    s, m, e = sh.GetStart(), sh.GetArcMid(), sh.GetEnd()
    (x1, y1), (x2, y2), (x3, y3) = [(mm(v.x), mm(v.y)) for v in (s, m, e)]
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
    uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
    r = math.hypot(x1 - ux, y1 - uy)
    a1 = math.atan2(y1 - uy, x1 - ux)
    a2 = math.atan2(y2 - uy, x2 - ux)
    a3 = math.atan2(y3 - uy, x3 - ux)

    def norm(a):
        return (a - a1) % (2 * math.pi)
    sweep = norm(a3)
    if norm(a2) > sweep:              # идём в другую сторону
        sweep = sweep - 2 * math.pi
    return [(ux + r * math.cos(a1 + sweep * i / n), uy + r * math.sin(a1 + sweep * i / n))
            for i in range(n + 1)]


def shape_segments(sh):
    """любая фигура -> список отрезков (x1,y1,x2,y2) в абсолютных мм"""
    t = sh.GetShape()
    if t == p.SHAPE_T_SEGMENT:
        s, e = sh.GetStart(), sh.GetEnd()
        return [(mm(s.x), mm(s.y), mm(e.x), mm(e.y))]
    if t == p.SHAPE_T_RECT:
        s, e = sh.GetStart(), sh.GetEnd()
        x1, y1, x2, y2 = mm(s.x), mm(s.y), mm(e.x), mm(e.y)
        return [(x1, y1, x2, y1), (x2, y1, x2, y2), (x2, y2, x1, y2), (x1, y2, x1, y1)]
    if t == p.SHAPE_T_ARC:
        pts = arc_points(sh)
        return [(a[0], a[1], c[0], c[1]) for a, c in zip(pts, pts[1:])]
    if t == p.SHAPE_T_CIRCLE:
        c = sh.GetCenter()
        cx, cy, r = mm(c.x), mm(c.y), mm(sh.GetRadius())
        pts = [(cx + r * math.cos(2 * math.pi * i / 24), cy + r * math.sin(2 * math.pi * i / 24))
               for i in range(25)]
        return [(a[0], a[1], c2[0], c2[1]) for a, c2 in zip(pts, pts[1:])]
    if t == p.SHAPE_T_POLY:
        out = []
        poly = sh.GetPolyShape()
        for oi in range(poly.OutlineCount()):
            o = poly.Outline(oi)
            n = o.PointCount()
            for i in range(n):
                a, c = o.CPoint(i), o.CPoint((i + 1) % n)
                out.append((mm(a.x), mm(a.y), mm(c.x), mm(c.y)))
        return out
    return []


def text_effects(t, mirror=False):
    h = mm(t.GetTextHeight())
    w = mm(t.GetTextWidth())
    th = mm(t.GetTextThickness())
    j = " (justify mirror)" if mirror else ""
    return "(effects (font (size %s %s) (thickness %s))%s)" % (f(h), f(w), f(th), j)


# ---------------------------------------------------------------- модули
SHAPE = {p.PAD_SHAPE_RECT: "rect", p.PAD_SHAPE_CIRCLE: "circle",
         p.PAD_SHAPE_OVAL: "oval", p.PAD_SHAPE_ROUNDRECT: "roundrect"}


def module(fp):
    L = []
    x, y = mm(fp.GetPosition().x), mm(fp.GetPosition().y)
    rot = fp.GetOrientationDegrees()
    at = "(at %s %s%s)" % (f(x), f(y), (" " + f(rot)) if rot else "")
    fid = fp.GetFPID()
    name = "%s:%s" % (fid.GetLibNickname(), fid.GetLibItemName())
    L.append("  (module %s (layer F.Cu) (tedit 0) %s" % (q(name), at))
    if fp.IsDNP():
        L.append("    (attr virtual)")
    for kind, t in (("reference", fp.Reference()), ("value", fp.Value())):
        lx, ly = to_local(fp, mm(t.GetPosition().x), mm(t.GetPosition().y))
        tr = t.GetTextAngleDegrees()
        hide = "" if t.IsVisible() else " hide"
        L.append("    (fp_text %s %s (at %s %s%s) (layer %s)%s"
                 % (kind, q(t.GetText()), f(lx), f(ly), (" " + f(tr)) if tr else "",
                    lay(t.GetLayer()) or "F.SilkS", hide))
        L.append("      %s)" % text_effects(t))
    for g in fp.GraphicalItems():
        if g.GetClass() not in ("PCB_SHAPE",):
            continue
        ln = lay(g.GetLayer())
        if not ln:
            continue
        w = mm(g.GetWidth()) or 0.05
        for (x1, y1, x2, y2) in shape_segments(g):
            a = to_local(fp, x1, y1)
            c = to_local(fp, x2, y2)
            L.append("    (fp_line (start %s %s) (end %s %s) (layer %s) (width %s))"
                     % (f(a[0]), f(a[1]), f(c[0]), f(c[1]), ln, f(w)))
    for pd in fp.Pads():
        rel = pd.GetFPRelativePosition()
        px, py = mm(rel.x), mm(rel.y)
        ori = pd.GetOrientationDegrees()
        shp = SHAPE[pd.GetShape(p.F_Cu)]
        sz = pd.GetSize(p.F_Cu)
        tht = pd.GetAttribute() == p.PAD_ATTRIB_PTH
        kind = "thru_hole" if tht else "smd"
        layers = "*.Cu *.Mask" if tht else "F.Cu F.Paste F.Mask"
        s = "    (pad %s %s %s (at %s %s%s) (size %s %s)" % (
            q(pd.GetNumber()), kind, shp, f(px), f(py), (" " + f(ori)) if ori else "",
            f(mm(sz.x)), f(mm(sz.y)))
        if tht:
            s += " (drill %s)" % f(mm(pd.GetDrillSize().x))
        s += " (layers %s)" % layers
        if shp == "roundrect":
            s += " (roundrect_rratio %s)" % f(pd.GetRoundRectRadiusRatio(p.F_Cu))
        nr = netref(pd)
        if nr:
            s += " " + nr
        L.append(s + ")")
    L.append("  )")
    return L


# ---------------------------------------------------------------- файл
out = []
out.append('(kicad_pcb (version 20171130) (host pcbnew "(5.1.9)-1")')
out.append("  (general (thickness 1.6) (drawings 0) (tracks 0) (zones 0) (modules %d) (nets %d))"
           % (len(b.GetFootprints()), len(nets)))
out.append("  (page A4)")
out.append("""  (layers
    (0 F.Cu signal)
    (31 B.Cu signal)
    (32 B.Adhes user)
    (33 F.Adhes user)
    (34 B.Paste user)
    (35 F.Paste user)
    (36 B.SilkS user)
    (37 F.SilkS user)
    (38 B.Mask user)
    (39 F.Mask user)
    (40 Dwgs.User user)
    (41 Cmts.User user)
    (42 Eco1.User user)
    (43 Eco2.User user)
    (44 Edge.Cuts user)
    (45 Margin user)
    (46 B.CrtYd user)
    (47 F.CrtYd user)
    (48 B.Fab user)
    (49 F.Fab user)
  )""")
out.append("""  (setup
    (last_trace_width 0.2)
    (trace_clearance 0.2)
    (zone_clearance 0.3)
    (zone_45_only no)
    (trace_min 0.15)
    (via_size 0.6)
    (via_drill 0.3)
    (via_min_size 0.5)
    (via_min_drill 0.3)
    (uvia_size 0.3)
    (uvia_drill 0.1)
    (uvias_allowed no)
    (uvia_min_size 0.2)
    (uvia_min_drill 0.1)
    (edge_width 0.1)
    (segment_width 0.2)
    (pcb_text_width 0.15)
    (pcb_text_size 1 1)
    (mod_edge_width 0.12)
    (mod_text_size 1 1)
    (mod_text_width 0.15)
    (pad_size 1.6 1.6)
    (pad_drill 0.8)
    (pad_to_mask_clearance 0.05)
    (aux_axis_origin 0 0)
    (visible_elements FFFFFF7F)
    (pcbplotparams
      (layerselection 0x010fc_ffffffff)
      (usegerberextensions false)
      (usegerberattributes true)
      (usegerberadvancedattributes true)
      (creategerberjobfile true)
      (excludeedgelayer true)
      (linewidth 0.100000)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotinvisibletext false)
      (padsonsilk false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory ""))
  )""")
for code in sorted(nets):
    out.append("  (net %d %s)" % (code, q(nets[code])))
out.append('  (net_class Default "Default"')
out.append("    (clearance 0.2) (trace_width 0.2) (via_dia 0.6) (via_drill 0.3) (uvia_dia 0.3) (uvia_drill 0.1)")
for code in sorted(nets):
    if code > 0:
        out.append("    (add_net %s)" % q(nets[code]))
out.append("  )")

for fp in b.GetFootprints():
    out += module(fp)

for d in b.GetDrawings():
    if d.GetClass() == "PCB_SHAPE":
        ln = lay(d.GetLayer())
        if not ln:
            continue
        w = mm(d.GetWidth()) or 0.1
        for (x1, y1, x2, y2) in shape_segments(d):
            out.append("  (gr_line (start %s %s) (end %s %s) (layer %s) (width %s))"
                       % (f(x1), f(y1), f(x2), f(y2), ln, f(w)))
    elif d.GetClass() == "PCB_TEXT":
        ln = lay(d.GetLayer())
        pos = d.GetPosition()
        out.append("  (gr_text %s (at %s %s) (layer %s)" % (q(d.GetText()), f(mm(pos.x)), f(mm(pos.y)), ln))
        out.append("    %s)" % text_effects(d, d.IsMirrored()))

for t in b.GetTracks():
    if t.GetClass() == "PCB_VIA":
        pos = t.GetPosition()
        out.append("  (via (at %s %s) (size %s) (drill %s) (layers F.Cu B.Cu) %s)"
                   % (f(mm(pos.x)), f(mm(pos.y)), f(mm(t.GetWidth(p.F_Cu))), f(mm(t.GetDrillValue())),
                      netnum(t)))
    else:
        s, e = t.GetStart(), t.GetEnd()
        out.append("  (segment (start %s %s) (end %s %s) (width %s) (layer %s) %s)"
                   % (f(mm(s.x)), f(mm(s.y)), f(mm(e.x)), f(mm(e.y)), f(mm(t.GetWidth())),
                      lay(t.GetLayer()), netnum(t)))
out.append(")")

os.makedirs(OUTDIR, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
# проект KiCad 5 — простой INI
with open(os.path.join(OUTDIR, "j30_fm18w08_gal.pro"), "w", encoding="utf-8") as fh:
    fh.write("update=02.10.2026\nversion=1\nlast_client=kicad\n[general]\nversion=1\nRootSch=\nBoardNm=\n"
             "[pcbnew]\nversion=1\nLastNetListRead=\n")
print("выгружено:", OUT)
