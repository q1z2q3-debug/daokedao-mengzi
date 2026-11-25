# -*- coding: utf-8 -*-
"""离娄上 图 72–81（v0.14.0 二稿）
用法：python3 scripts/gen_figs_072_081.py
注意：P() 第五位才是 dash；画虚线须写 P(d, col, sw, "none", "x,y")。
"""
import os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "assets", "fig")

PAPER = "#F7F4EE"; INK = "#25211D"; ZHE = "#994433"; ZONG = "#7C6D5C"
LINE = "#DCD5C8"; GREY = "#BFB4A4"; WARM = "#8C7B69"
SOFT = "#F0EBE2"; PALE = "#FCFAF6"


def T(x, y, s, size=6.6, fill=INK, anchor="middle", ls=0, weight="400"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'letter-spacing="{ls}" fill="{fill}" font-weight="{weight}">{s}</text>')


def L(x1, y1, x2, y2, col=INK, sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
            f'stroke-width="{sw}"{d}/>')


def P(d, col=INK, sw=1.2, fill="none", dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'  <path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{da}/>'


def C(cx, cy, r, col=INK, sw=1.2, fill="none"):
    return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>'


def E(cx, cy, rx, ry, col=INK, sw=1.2, fill="none"):
    return (f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" '
            f'stroke="{col}" stroke-width="{sw}"/>')


def R(x, y, w, hh, col=INK, sw=1.2, fill="none"):
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{hh}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>'


def arrow(x1, y1, x2, y2, col=INK, sw=1.2, size=5):
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 + size * math.cos(ang + 2.6), y2 + size * math.sin(ang + 2.6))
    p2 = (x2 + size * math.cos(ang - 2.6), y2 + size * math.sin(ang - 2.6))
    return [L(x1, y1, x2, y2, col, sw),
            P(f"M {p1[0]:.1f},{p1[1]:.1f} L {x2},{y2} L {p2[0]:.1f},{p2[1]:.1f}", col, sw * 0.9)]


def stand(x, fy, H, col=INK, sw=1.2, arms="down"):
    hr = max(5, H * 0.075)
    top = fy - H
    hy = top + hr * 2 + H * 0.12
    o = [C(x, top + hr, hr, col, sw), L(x, top + hr * 2, x, fy - H * 0.24, col, sw * 1.25)]
    if arms == "down":
        o += [L(x, hy, x - H * 0.16, hy + H * 0.22, col, sw),
              L(x, hy, x + H * 0.16, hy + H * 0.22, col, sw)]
    elif arms == "point":
        o += [L(x, hy, x - H * 0.16, hy + H * 0.2, col, sw),
              L(x, hy, x + H * 0.5, hy + H * 0.06, col, sw)]
    o += [L(x, fy - H * 0.24, x - H * 0.09, fy, col, sw), L(x, fy - H * 0.24, x + H * 0.09, fy, col, sw)]
    return o


def head_(t, sub, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {h}" width="760" height="{h}" '
        f'font-family="\'Noto Serif SC\',\'Songti SC\',\'Source Han Serif SC\',serif">',
        f'  <rect x="0" y="0" width="760" height="{h}" fill="{PAPER}"/>',
        f'  <rect x="10" y="10" width="740" height="{h-40}" fill="none" stroke="{LINE}" stroke-width="1"/>',
        f'  <rect x="16" y="16" width="728" height="{h-52}" fill="none" stroke="{LINE}" stroke-width="0.6"/>',
        T(380, 48, t, 21, INK, ls=5, weight="700"),
        T(380, 68, sub, 10.5, ZONG, ls=2),
        L(120, 80, 640, 80, LINE, 1),
    ]


def tail_(h, q, label, name, key):
    return [
        L(120, h - 104, 640, h - 104, LINE, 1),
        T(380, h - 80, q, 8.6, INK, ls=2),
        f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 离娄上</text>',
        f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>',
    ]


def _flat(x):
    out = []
    for it in x:
        if isinstance(it, (list, tuple)):
            out.extend(_flat(it))
        else:
            out.append(it)
    return out


def save(name, lines):
    s = "\n".join(_flat(lines)) + "\n</svg>\n"
    with open(os.path.join(FIG, name), "w", encoding="utf-8") as f:
        f.write(s)
    print(name, len(s))


def house(cx, base, w=104, hh=76, col=INK, sw=1.3):
    left = cx - w / 2
    return [P(f"M {left},{base} L {left},{base-hh} L {cx},{base-hh-34} L {left+w},{base-hh} L {left+w},{base}",
              col, sw, fill=SOFT),
            R(cx - 16, base - 56, 32, 56, col, sw * 0.9, fill=PALE)]


def oldman(cx, base, H=100, col=INK, sw=1.1):
    hr = 7.6
    top = base - H
    shoulder = top + hr * 2 + H * 0.1
    o = [C(cx, top + hr, hr, col, sw), L(cx, top + hr * 2, cx, base - H * 0.2, col, sw * 1.2),
         L(cx, base - H * 0.2, cx - H * 0.07, base, col, sw),
         L(cx, base - H * 0.2, cx + H * 0.07, base, col, sw),
         L(cx, shoulder, cx - H * 0.15, shoulder + H * 0.26, col, sw),
         L(cx, shoulder, cx + H * 0.1, shoulder + H * 0.22, col, sw),
         L(cx + H * 0.24, top + hr + 3, cx + H * 0.28, base, col, sw * 1.1),
         P(f"M {cx+H*0.24},{top+hr+3} C {cx+H*0.19},{top+hr-3} {cx+H*0.28},{top+hr-4} {cx+H*0.30},{top+hr+3}",
           col, sw * 0.9),
         C(cx - H * 0.2, shoulder + H * 0.3, 8.5, col, sw, fill=SOFT),
         L(cx - H * 0.2, shoulder + H * 0.3 - 8, cx - H * 0.12, shoulder + H * 0.06, col, sw * 0.9)]
    return o


def shoe(x, y, w=56, col=INK, sw=1.0):
    """侧形鞋：厚底、后跟直、前掌斜下，鞋口一个小椭圆。"""
    return [P(f"M {x},{y} L {x},{y-12} C {x},{y-16} {x+5},{y-17} {x+11},{y-17} "
              f"L {x+w*0.58:.0f},{y-17} C {x+w*0.86:.0f},{y-16} {x+w},{y-9} {x+w},{y} L {x},{y} Z",
              col, sw, fill=PALE),
            L(x, y, x + w, y, WARM, 2.0),
            f'  <ellipse cx="{x+19:.0f}" cy="{y-15}" rx="7" ry="2.6" fill="none" stroke="{GREY}" stroke-width="0.7"/>']


def dou(x, y, w=84, hh=76):
    """斗：上宽下窄的开口量器。"""
    return [P(f"M {x},{y} L {x+w},{y} L {x+w*0.82},{y+hh} L {x+w*0.18},{y+hh} Z", ZONG, 1.6),
            L(x, y, x + w, y, ZONG, 1.2)]



def bowl(cx, cy, rw=88, rh=26, col=INK, sw=1.4):
    """陶碗：口沿椭圆、腹壁、圈足。"""
    return [E(cx, cy, rw, rh, col, sw, fill=SOFT),
            P(f"M {cx-rw},{cy} C {cx-rw},{cy+rh*1.5} {cx-rw*0.55},{cy+rh*2.1} {cx},{cy+rh*2.1} "
              f"C {cx+rw*0.55},{cy+rh*2.1} {cx+rw},{cy+rh*1.5} {cx+rw},{cy}", col, sw, fill=SOFT),
            P(f"M {cx-rw*0.3},{cy+rh*2.1} L {cx-rw*0.24},{cy+rh*2.6} L {cx+rw*0.24},{cy+rh*2.6} "
              f"L {cx+rw*0.3},{cy+rh*2.1}", col, sw * 0.9)]


def desk(x, y, w=260, hh=12, col=WARM, sw=1.3):
    return [R(x, y, w, hh, col, sw, fill=SOFT),
            L(x + 14, y + hh, x + 14, y + 62, col, 1.1),
            L(x + w - 14, y + hh, x + w - 14, y + 62, col, 1.1)]


def slip(x, y, w=120, hh=26, col=WARM, sw=1.0):
    """简册：横放的一卷，编绳两道。"""
    return [R(x, y, w, hh, col, sw, fill=PALE),
            L(x + 18, y, x + 18, y + hh, GREY, 0.6),
            L(x + 40, y, x + 40, y + hh, GREY, 0.6),
            L(x + 62, y, x + 62, y + hh, GREY, 0.6),
            L(x + 84, y, x + 84, y + hh, GREY, 0.6),
            L(x + 3, y + 7, x + w - 3, y + 7, ZONG, 0.7),
            L(x + 3, y + hh - 7, x + w - 3, y + hh - 7, ZONG, 0.7)]


def doufood(cx, base, H=86, col=ZONG, sw=1.2):
    """豆：高足盘。"""
    return [E(cx, base - H, 34, 10, col, sw, fill=SOFT),
            P(f"M {cx-24},{base-H+8} C {cx-24},{base-H+34} {cx+24},{base-H+34} {cx+24},{base-H+8}",
              col, sw, fill=SOFT),
            L(cx, base - H + 34, cx, base - 12, col, sw * 1.1),
            E(cx, base - 10, 20, 7, col, sw, fill=SOFT)]


def child(cx, base, H=54, col=ZONG, sw=1.0):
    hr = 4.6
    top = base - H
    return [C(cx, top + hr, hr, col, sw), L(cx, top + hr * 2, cx, base - H * 0.3, col, sw),
            L(cx, base - H * 0.3, cx - 7, base, col, sw), L(cx, base - H * 0.3, cx + 7, base, col, sw),
            L(cx, top + hr * 2 + 4, cx - 11, base - H * 0.45, col, sw * 0.9),
            L(cx, top + hr * 2 + 4, cx + 11, base - H * 0.45, col, sw * 0.9)]
# -*- coding: utf-8 -*-
"""告子下 图 162–171（v0.24.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail9(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 告子下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def tower(cx, base, w=96, hh=132, n=3, col=WARM, sw=1.2):
    """岑楼：层层收窄的高楼，各层开窗。"""
    o = []
    for i in range(n):
        wl = w - i * 22
        y0 = base - (hh / n) * i
        y1 = y0 - hh / n
        o += [P(f"M {cx-wl/2-8},{y0} L {cx-wl/2},{y1} L {cx+wl/2},{y1} L {cx+wl/2+8},{y0} Z", col, sw, fill=SOFT)]
        for k in range(2):
            o += [R(cx - 8 + k * 12 - 6, y1 + 10, 9, 14, col, sw * 0.6, fill=PALE)]
    o += [L(cx - w / 2 - 6, base, cx - w / 2 - 6, base - 6, col, sw * 0.8),
          L(cx + w / 2 + 6, base, cx + w / 2 + 6, base - 6, col, sw * 0.8)]
    return o


def block(cx, cy, s=18, col=ZONG, sw=1.1):
    return [R(cx - s / 2, cy - s / 2, s, s, col, sw, fill=PALE)]


def flag(cx, base, hh=110, w=54, col=ZONG, sw=1.2, label="", txt_col=None):
    """旗：杆直，旗面右展。"""
    o = [L(cx, base, cx, base - hh, col, sw * 1.3),
         P(f"M {cx},{base-hh} L {cx+w},{base-hh+8} L {cx+w},{base-hh+42} L {cx},{base-hh+34} Z",
           col, sw, fill=SOFT)]
    if label:
        o += [T(cx + w * 0.52, base - hh + 32, label, 11, txt_col or INK, ls=2)]
    return o


def sector_pie(cx, cy, r=78, n=20, col=ZONG, sw=0.9, hot=0, fill=SOFT):
    """二十取一：圆分二十扇，一格填赭。"""
    o = [C(cx, cy, r + 4, LINE, 0.7)]
    for i in range(n):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        f = ZHE if i == hot else fill
        o += [P(f"M {cx},{cy} L {x0:.1f},{y0:.1f} A {r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z", col, sw, fill=f)]
    o += [C(cx, cy, 6, col, sw)]
    return o


def granary(cx, base, w=64, hh=64, col=WARM, sw=1.2):
    """仓：圆身形、茅顶、一门。"""
    o = [P(f"M {cx-w/2},{base} L {cx-w/2},{base-hh*0.7} A {w/2},{w/2*0.55} 0 0 1 {cx+w/2},{base-hh*0.7} "
           f"L {cx+w/2},{base} Z", col, sw, fill=SOFT),
         P(f"M {cx-w*0.62},{base-hh*0.7} Q {cx},{base-hh*1.3} {cx+w*0.62},{base-hh*0.7}", col, sw * 1.2),
         R(cx - 10, base - 30, 20, 30, col, sw * 0.9, fill=PALE)]
    return o


def ge(cx, base, hh=118, col=ZONG, sw=1.2):
    """戈：直柄、横刃、下镦。"""
    return [L(cx, base, cx, base - hh, col, sw * 1.3),
            P(f"M {cx},{base-hh*0.72} L {cx+34},{base-hh*0.62} L {cx+26},{base-hh*0.5} L {cx},{base-hh*0.6} Z",
              col, sw, fill=SOFT),
            P(f"M {cx-8},{base} L {cx+8},{base} L {cx},{base-10} Z", col, sw * 0.9, fill=SOFT)]


def bundle(cx, base, w=64, hh=26, col=ZONG, sw=1.1):
    """币：一束帛，两端束结。"""
    o = [R(cx - w / 2, base - hh, w, hh, col, sw, fill=PALE)]
    for i in range(3):
        o += [L(cx - w / 2, base - hh + 7 + i * 7, cx + w / 2, base - hh + 7 + i * 7, col, sw * 0.5)]
    o += [E(cx - w / 2 - 5, base - hh / 2, 5, 8, col, sw * 0.9, fill=SOFT),
          E(cx + w / 2 + 5, base - hh / 2, 5, 8, col, sw * 0.9, fill=SOFT)]
    return o


def path3(x0, y0, x1, y1, cx, cy, col, sw=1.1):
    return [P(f"M {x0},{y0} Q {cx},{cy} {x1},{y1}", col, sw)]


def slip(cx, base, w=64, hh=76, col=ZONG, sw=1.1, n=4, label=""):
    """册：竖竹简加两道编绳，册面书题。"""
    o = [R(cx - w / 2, base - hh, w, hh, col, sw, fill=PALE)]
    for i in range(1, n):
        o += [L(cx - w / 2 + i * w / n, base - hh, cx - w / 2 + i * w / n, base, col, sw * 0.6)]
    for j in range(2):
        yy = base - hh + 16 + j * (hh - 28)
        o += [L(cx - w / 2 - 3, yy, cx + w / 2 + 3, yy, col, sw * 0.9)]
    if label:
        o += [T(cx, base - hh / 2 + 4, label, 7.0, INK, ls=2)]
    return o


def strip(cx, base, w=34, hh=88, col=ZONG, sw=1.1, label=""):
    """单片竹简：窄长条、上端微削、面书题。"""
    o = [P(f"M {cx-w/2},{base} L {cx-w/2},{base-hh+6} L {cx},{base-hh} L {cx+w/2},{base-hh+6} L {cx+w/2},{base} Z",
           col, sw, fill=PALE)]
    o += [L(cx - w / 2 + 3, base - hh * 0.22, cx + w / 2 - 3, base - hh * 0.22, col, sw * 0.5)]
    if label:
        for i, ch in enumerate(label):
            o += [T(cx, base - hh * 0.34 - i * 0, ch, 5.6, INK)]
    return o


def field(x, y, w=150, hh=64, col=WARM, sw=1.1):
    o = [R(x, y, w, hh, col, sw, fill=PALE)]
    for i in range(3):
        yy = y + 14 + i * 14
        o += [P(f"M {x+4},{yy} q 18,-5 36,0 q 18,5 36,0 q 18,-5 36,0", col, sw * 0.7)]
    return o


h = 540

# ---------------------------------------------------------- 162 寸木岑楼
o = head_("寸 木 岑 楼", "《孟子》告子下　第一百六十二章　MZ162", h)
o += [T(380, 112, "不揣其本而齐其末，方寸之木可使高于岑楼", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += tower(520, 404, 106, 140, 3)
o += [T(520, 424, "岑 楼", 5.8, ZONG, ls=2)]
o += block(520, 258, 20)
o += [T(560, 240, "方寸之木", 5.4, ZHE)]
o += [L(160, 262, 660, 262, LINE, 0.9)]
o += [T(196, 254, "齐 其 末", 5.2, GREY)]
o += [L(160, 404, 160, 262, LINE, 0.8)]
o += [T(150, 340, "本", 6.0, GREY)]
o += [P("M 250,300 L 250,404", LINE, 0.8, "none", "3,3")]
o += [block(250, 390, 14)]
o += [T(250, 424, "寸木在其本", 5.2, GREY)]
o += [T(300, 200, "金重于羽，岂谓一钩金与一舆羽", 5.4, GREY)]
o += tail9(h, "取食之重者，与礼之轻者而比之，奚翅食重？", "图七十三", "寸木岑楼", "ch162a")
save("ch162a-cunmu-cenlou.svg", o)

# ---------------------------------------------------------- 163 徐行后长
o = head_("徐 行 后 长", "《孟子》告子下　第一百六十三章　MZ163", h)
o += [T(380, 112, "徐行后长者谓之弟，疾行先长者谓之不弟", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(430, 404, 116, INK, 1.2)]
o += [L(430, 296, 392, 404, ZONG, 1.3)]
o += [C(430, 268, 7, INK, 1.1), L(430, 275, 430, 320, INK, 1.2),
      L(430, 320, 414, 360, INK, 1.0), L(430, 320, 446, 360, INK, 1.0),
      L(430, 288, 452, 278, INK, 1.0), L(408, 288, 424, 296, INK, 1.0)]
o += [T(430, 250, "长 者", 5.6, ZONG, ls=2)]
o += [stand(250, 404, 96, INK, 1.1)]
o += [T(250, 424, "少者徐行", 5.6, ZHE)]
o += [P("M 290,372 L 380,372", LINE, 0.9, "none", "3,3")]
o += [arrow(300, 372, 372, 372, ZHE, 0.9, 4)]
o += [T(300, 342, "后 长", 5.4, ZHE)]
o += [stand(590, 404, 108, INK, 1.0)]
o += [T(590, 424, "疾行先长", 5.4, GREY)]
o += [P("M 560,300 L 620,300", GREY, 0.8), P("M 620,300 L 560,318", GREY, 0.8)]
o += [T(380, 220, "亦为之而已矣　弗为耳", 5.6, GREY)]
o += tail9(h, "尧舜之道，孝弟而已矣。", "图七十四", "徐行后长", "ch163a")
save("ch163a-xuxing-houchang.svg", o)

# ---------------------------------------------------------- 164 亲过大小
o = head_("亲 过 大 小", "《孟子》告子下　第一百六十四章　MZ164", h)
o += [T(380, 112, "亲之过大而不怨，是愈疏也；亲之过小而怨，是不可矶也", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += strip(214, 404, 40, 96, ZONG, 1.2)
o += [T(214, 300, "小", 8.6, INK), T(214, 328, "弁", 8.6, INK)]
o += [T(220, 424, "亲之过大", 5.8, ZONG, ls=1)]
o += [C(320, 330, 6, INK, 1.1), L(320, 336, 320, 372, INK, 1.1),
      L(320, 372, 308, 404, INK, 0.9), L(320, 372, 332, 404, INK, 0.9)]
o += [T(320, 314, "怨", 6.4, ZHE, ls=2)]
o += [P("M 312,348 q 5,10 8,16", ZHE, 0.9), P("M 328,348 q 5,10 8,16", ZHE, 0.9)]
o += strip(510, 404, 34, 72, GREY, 1.0)
o += [T(510, 356, "凯", 7.0, GREY), T(510, 378, "风", 7.0, GREY)]
o += [T(520, 424, "亲之过小", 5.8, GREY, ls=1)]
o += [C(600, 356, 5.4, INK, 1.0), L(600, 361, 600, 390, INK, 1.0),
      L(600, 390, 590, 404, INK, 0.9), L(600, 390, 610, 404, INK, 0.9),
      L(600, 366, 616, 372, INK, 0.9), L(600, 366, 584, 372, INK, 0.9)]
o += [T(600, 340, "不怨", 5.6, GREY)]
o += [T(380, 214, "愈疏，不孝也；不可矶，亦不孝也", 5.6, GREY)]
o += [T(380, 250, "舜五十而慕", 5.4, ZHE)]
o += tail9(h, "固哉，高叟之为诗也！", "图七十五", "亲过大小", "ch164a")
save("ch164a-qinguo-daxiao.svg", o)

# ---------------------------------------------------------- 165 义利之号
o = head_("义 利 之 号", "《孟子》告子下　第一百六十五章　MZ165", h)
o += [T(380, 112, "先生之志则大矣，先生之号则不可", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += flag(210, 404, 120, 56, GREY, 1.1, "利", GREY)
o += [T(210, 424, "以利说之", 5.6, GREY)]
o += flag(520, 404, 120, 56, ZHE, 1.2, "义", ZHE)
o += [T(520, 424, "以仁义说之", 5.6, ZHE)]
for i in range(3):
    x = 330 + i * 32
    o += [C(x, 322, 5, INK, 0.9), L(x, 327, x, 360, INK, 1.0),
          L(x, 360, x - 7, 384, INK, 0.8), L(x, 360, x + 7, 384, INK, 0.8),
          L(x, 336, x - 9, 348, INK, 0.8), L(x, 336, x + 9, 348, INK, 0.8)]
o += [T(362, 404, "三 军", 5.4, ZONG, ls=2)]
o += [T(360, 250, "罢 三 军 之 师", 5.4, GREY)]
o += tail9(h, "何必曰利？", "图七十六", "义利之号", "ch165a")
save("ch165a-yili-zhihao.svg", o)

# ---------------------------------------------------------- 166 币交不报
o = head_("币 交 不 报", "《孟子》告子下　第一百六十六章　MZ166", h)
o += [T(380, 112, "受之而不报", 6.6, GREY, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [R(150, 316, 54, 88, WARM, 1.1, fill=SOFT), L(150, 316, 204, 316, WARM, 1.3)]
o += [T(177, 304, "任", 7.0, ZONG, ls=2)]
o += [R(560, 316, 54, 88, WARM, 1.1, fill=SOFT), L(560, 316, 614, 316, WARM, 1.3)]
o += [T(587, 304, "齐", 7.0, ZONG, ls=2)]
o += [R(300, 372, 160, 10, WARM, 1.1, fill=SOFT)]
o += bundle(380, 372, 60, 24)
o += [T(380, 424, "币 交", 5.8, ZONG, ls=2)]
o += [arrow(240, 340, 300, 350, GREY, 0.9, 4)]
o += [arrow(520, 350, 460, 340, GREY, 0.9, 4)]
o += [T(380, 300, "仪不及物，曰不享", 5.6, GREY)]
o += [P("M 380,286 L 380,330", ZHE, 1.0, "none", "4,3")]
o += [T(430, 268, "不 报", 6.0, ZHE, ls=2)]
o += [T(380, 210, "季子不得之邹，储子得之平陆", 5.4, GREY)]
o += tail9(h, "为其不成享也。", "图七十七", "币交不报", "ch166a")
save("ch166a-bijiao-bubao.svg", o)

# ---------------------------------------------------------- 167 三子趋一
o = head_("三 子 趋 一", "《孟子》告子下　第一百六十七章　MZ167", h)
o += [T(380, 112, "三子者不同道，其趋一也；一者何也？曰：仁也", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [C(470, 300, 34, ZONG, 1.3), T(470, 305, "仁", 10, INK, ls=2)]
o += path3(180, 396, 432, 322, 260, 400, ZONG)
o += path3(180, 300, 436, 300, 300, 250, ZONG)
o += path3(180, 240, 432, 286, 300, 300, ZONG)
o += [T(170, 400, "伯夷", 6.0, ZONG, ls=1)]
o += [T(170, 304, "伊尹", 6.0, ZONG, ls=1)]
o += [T(170, 236, "柳下惠", 6.0, ZONG, ls=1)]
o += [T(540, 268, "居下位不以贤事不肖", 5.0, GREY)]
o += [T(540, 292, "五就汤五就桀", 5.0, GREY)]
o += [T(540, 316, "不恶污君不辞小官", 5.0, GREY)]
o += [T(380, 404, "君子亦仁而已矣，何必同？", 5.8, ZHE)]
o += tail9(h, "君子亦仁而已矣，何必同？", "图七十八", "三子趋一", "ch167a")
save("ch167a-sanziquyi.svg", o)

# ---------------------------------------------------------- 168 五霸罪人
o = head_("五 霸 罪 人", "《孟子》告子下　第一百六十八章　MZ168", h)
o += [T(380, 112, "五霸者，三王之罪人也；今之诸侯，五霸之罪人也", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [P("M 190,404 L 250,404 L 250,340 L 330,340 L 330,286 L 410,286 L 410,232 L 490,232 L 490,182 L 560,182",
       ZONG, 1.2)]
o += [R(190, 404 - 30, 60, 30, WARM, 0.9, fill=SOFT),
      R(250, 340 - 30, 80, 30, WARM, 0.9, fill=SOFT),
      R(330, 286 - 30, 80, 30, WARM, 0.9, fill=SOFT),
      R(410, 232 - 30, 80, 30, WARM, 0.9, fill=SOFT)]
o += [T(220, 424, "今之大夫", 5.4, GREY)]
o += [T(290, 328, "今之诸侯", 5.4, GREY)]
o += [T(370, 274, "五 霸", 5.4, ZONG)]
o += [T(450, 220, "三 王", 5.4, ZHE)]
o += [T(560, 176, "天 子", 5.6, INK)]
o += [arrow(600, 220, 600, 380, ZHE, 1.0, 4)]
o += [T(614, 300, "罪", 6.4, ZHE, ls=2)]
o += [T(200, 230, "长君之恶其罪小，逢君之恶其罪大", 5.2, GREY)]
o += tail9(h, "今之大夫，今之诸侯之罪人也。", "图七十九", "五霸罪人", "ch168a")
save("ch168a-wuba-zuiren.svg", o)

# ---------------------------------------------------------- 169 殃民
o = head_("殃 民", "《孟子》告子下　第一百六十九章　MZ169", h)
o += [T(380, 112, "不教民而用之，谓之殃民", 6.6, GREY, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(230, 404, 96, INK, 1.1)]
o += [stand(320, 404, 92, INK, 1.1)]
o += [stand(410, 404, 88, INK, 1.1)]
o += [T(320, 424, "未 教 之 民", 5.6, GREY, ls=1)]
o += ge(560, 404, 128)
o += ge(620, 404, 118)
o += [T(590, 424, "战 阵", 5.6, ZHE, ls=1)]
o += [P("M 440,340 L 520,360", ZHE, 1.0, "none", "4,3")]
o += [P("M 424,340 L 440,332 L 438,348 Z", ZHE, 0.9, fill=ZHE)]
o += [T(470, 320, "驱 之", 5.6, ZHE)]
o += [T(380, 214, "一战胜齐，遂有南阳，然且不可", 5.4, GREY)]
o += [T(380, 250, "徒取诸彼以与此，仁者不为", 5.4, GREY)]
o += tail9(h, "殃民者，不容于尧舜之世。", "图八十", "殃民", "ch169a")
save("ch169a-yangmin.svg", o)

# ---------------------------------------------------------- 170 民贼
o = head_("民 贼", "《孟子》告子下　第一百七十章　MZ170", h)
o += [T(380, 112, "今之所谓良臣，古之所谓民贼也", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += field(150, 340, 190, 64)
for i in range(4):
    o += [P(f"M 170,{340} q 6,-18 4,-26", ZONG, 0.9), P(f"M 216,{340} q 6,-20 4,-28", ZONG, 0.9),
          P(f"M 262,{340} q 6,-18 4,-26", ZONG, 0.9), P(f"M 308,{340} q 6,-20 4,-28", ZONG, 0.9)]
o += [T(245, 424, "辟 土 地", 5.6, ZONG, ls=1)]
o += granary(430, 404, 70, 70)
o += [T(430, 424, "充 府 库", 5.6, ZONG, ls=1)]
o += [stand(560, 404, 112, INK, 1.2)]
o += [T(560, 424, "君", 5.8, ZONG)]
o += [C(600, 300, 24, LINE, 0.9), T(600, 305, "道", 8.0, GREY)]
o += [P("M 574,320 L 588,316", LINE, 0.9, "none", "3,3")]
o += [T(380, 200, "君不乡道，不志于仁，而求富之，是富桀也", 5.4, GREY)]
o += tail9(h, "由今之道，无变今之俗，虽与之天下，不能一朝居也。", "图八十一", "民贼", "ch170a")
save("ch170a-minzei.svg", o)

# ---------------------------------------------------------- 171 貉道
o = head_("貉 道", "《孟子》告子下　第一百七十一章　MZ171", h)
o += [T(380, 112, "欲轻之于尧舜之道者，大貉小貉也", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += sector_pie(380, 290, 84, 20, ZONG, 0.8, 0)
o += [T(380, 300, "二 十", 8.0, INK, ls=2)]
o += [T(380, 424, "二十而取一", 5.8, ZHE, ls=1)]
o += [P("M 480,232 L 520,214", ZHE, 0.9)]
o += [T(536, 208, "取其一", 5.4, ZHE)]
o += [T(200, 250, "万室之国", 5.4, GREY), T(200, 272, "一人陶，则可乎？", 5.4, GREY)]
o += [T(560, 300, "貉：五谷不生", 5.2, GREY), T(560, 320, "无城郭宫室宗庙", 5.2, GREY),
      T(560, 340, "无诸侯币帛饔飧", 5.2, GREY)]
o += tail9(h, "去人伦，无君子，如之何其可也？", "图八十二", "貉道", "ch171a")
save("ch171a-hedao.svg", o)
