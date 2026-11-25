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
"""告子上 图 142–151（v0.22.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail7(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 告子上</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def willow(cx, base, H=150, col=ZONG, sw=1.2):
    """杞柳：双线直干、四枝下垂、枝上短叶。"""
    o = [L(cx - 4, base, cx - 3, base - H, col, sw * 1.4),
         L(cx + 4, base, cx + 3, base - H, col, sw * 1.4),
         L(cx - 4, base, cx + 4, base, col, sw * 1.0)]
    br = [(base - H * 0.42, -1, 46, 74), (base - H * 0.58, 1, 52, 62),
          (base - H * 0.78, -1, 34, 46), (base - H * 0.9, 1, 26, 30)]
    for y0, sgn, dx, dy in br:
        x0 = cx + sgn * 4
        o += [P(f"M {x0},{y0} Q {x0+sgn*dx*0.7},{y0-dy*0.7} {x0+sgn*dx},{y0+dy*0.3}", col, sw)]
        for k in range(3):
            yy = y0 + dy * 0.3 - k * 10
            xx = x0 + sgn * dx * (0.55 + k * 0.14)
            o += [P(f"M {xx},{yy} q {sgn*9},-6 {sgn*13},-2", col, sw * 0.6)]
    return o


def woodcup(cx, base, w=62, hh=54, col=ZONG, sw=1.2):
    """桮桊：屈木为杯，口沿椭圆，圈足。"""
    return [E(cx, base - hh, w / 2, 8, col, sw, fill=PALE),
            P(f"M {cx-w/2},{base-hh} C {cx-w/2},{base-hh*0.5} {cx-w*0.3},{base-8} {cx},{base-8} "
              f"C {cx+w*0.3},{base-8} {cx+w/2},{base-hh*0.5} {cx+w/2},{base-hh}", col, sw, fill=SOFT),
            L(cx - 12, base - 8, cx - 12, base, col, sw * 0.9),
            L(cx + 12, base - 8, cx + 12, base, col, sw * 0.9)]


def waterline(x1, x2, y, col=ZONG, sw=1.2, n=6):
    """水：一道横线加数道短波。"""
    o = [L(x1, y, x2, y, col, sw)]
    step = (x2 - x1) / n
    for i in range(n):
        xx = x1 + i * step
        o += [P(f"M {xx},{y} q {step*0.25},-6 {step*0.5},0 q {step*0.25},6 {step*0.5},0", col, sw * 0.8)]
    return o


def field(x, y, w=150, hh=64, col=WARM, sw=1.1):
    o = [R(x, y, w, hh, col, sw, fill=PALE)]
    for i in range(4):
        yy = y + 14 + i * 14
        o += [P(f"M {x+4},{yy} q 18,-5 36,0 q 18,5 36,0 q 18,-5 36,0", col, sw * 0.7)]
    return o


def ear(cx, base, H=54, col=ZONG, sw=1.0, ripe=True):
    o = [L(cx, base, cx, base - H, col, sw)]
    if ripe:
        o += [E(cx, base - H - 6, 5.2, 11, col, sw * 0.9, fill=SOFT)]
        for i in range(4):
            o += [L(cx - 4, base - H - 14 + i * 5, cx - 10, base - H - 18 + i * 5, col, sw * 0.6)]
    else:
        o += [L(cx, base - H, cx - 7, base - H - 9, GREY, sw * 0.8),
              L(cx, base - H, cx + 6, base - H - 8, GREY, sw * 0.8)]
    return o


def axe(cx, cy, col=ZONG, sw=1.2):
    """斧：柄斜、刃作梯形。"""
    return [L(cx + 18, cy + 34, cx - 12, cy - 30, col, sw * 1.2),
            P(f"M {cx-12},{cy-30} L {cx-2},{cy-46} L {cx-18},{cy-52} L {cx-26},{cy-34} Z",
              col, sw, fill=SOFT)]


def mountain(cx, base, w=300, hh=120, col=WARM, sw=1.2):
    return [P(f"M {cx-w/2},{base} L {cx-w*0.18},{base-hh} L {cx+w*0.06},{base-hh*0.62} "
              f"L {cx+w*0.28},{base-hh*0.86} L {cx+w/2},{base}", col, sw, fill=SOFT)]


def fish(cx, cy, w=96, col=ZONG, sw=1.2):
    return [P(f"M {cx-w/2},{cy} C {cx-w*0.3},{cy-16} {cx+w*0.2},{cy-16} {cx+w*0.34},{cy} "
              f"C {cx+w*0.2},{cy+16} {cx-w*0.3},{cy+16} {cx-w/2},{cy} Z", col, sw, fill=PALE),
            P(f"M {cx+w*0.34},{cy} L {cx+w/2},{cy-12} L {cx+w/2},{cy+12} Z", col, sw, fill=SOFT),
            C(cx - w * 0.28, cy - 4, 2.4, col, 0.8, fill=col)]


def paw(cx, base, w=70, col=ZONG, sw=1.2):
    """熊掌：圆掌垫，四趾在下、各带爪尖。"""
    o = [E(cx, base - 26, w / 2, 24, col, sw, fill=SOFT)]
    for i in range(4):
        x = cx - 27 + i * 18
        o += [E(x, base - 6, 7.5, 10, col, sw * 0.9, fill=PALE),
              L(x, base + 3, x - 3, base + 9, col, sw * 0.8)]
    return o


def dog(x, y, s=0.8, col=INK, sw=1.1):
    """犬：四足、椭圆身、头前伸、尾上翘。"""
    return [E(x, y - 26 * s, 26 * s, 13 * s, col, sw, fill=PALE),
            C(x - 26 * s, y - 34 * s, 7 * s, col, sw),
            P(f"M {x-26*s},{y-40*s} L {x-30*s},{y-48*s}", col, sw * 0.8),
            L(x - 16 * s, y - 14 * s, x - 16 * s, y, col, sw),
            L(x + 14 * s, y - 14 * s, x + 14 * s, y, col, sw),
            P(f"M {x+22*s},{y-34*s} q {8*s},{-8*s} {6*s},{-14*s}", col, sw * 0.8)]


def cow(x, y, s=1.0, col=INK, sw=1.2):
    """牛：身厚、头低、双角、尾细。"""
    return [E(x, y - 36 * s, 34 * s, 18 * s, col, sw, fill=PALE),
            E(x - 34 * s, y - 30 * s, 12 * s, 10 * s, col, sw, fill=SOFT),
            P(f"M {x-36*s},{y-38*s} q {-6*s},{-8*s} {-2*s},{-14*s}", col, sw * 0.9),
            P(f"M {x-28*s},{y-38*s} q {2*s},{-8*s} {8*s},{-10*s}", col, sw * 0.9),
            L(x - 20 * s, y - 20 * s, x - 20 * s, y, col, sw),
            L(x + 16 * s, y - 20 * s, x + 16 * s, y, col, sw),
            P(f"M {x+32*s},{y-40*s} q {8*s},{10*s} {2*s},{20*s}", col, sw * 0.8)]


h = 540

# ---------------------------------------------------------- 142 杞柳桮桊
o = head_("杞 柳 桮 桊", "《孟子》告子上　第一百四十二章　MZ142", h)
o += [T(380, 112, "以人性为仁义，犹以杞柳为桮桊", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += willow(210, 404, 152)
o += [T(210, 424, "杞 柳", 6.0, ZONG, ls=2)]
o += woodcup(520, 404, 76, 62)
o += [T(520, 424, "桮 桊", 6.0, ZONG, ls=2)]
o += axe(432, 300)
o += [T(432, 240, "戕 贼", 7.0, ZHE, ls=3)]
o += [P("M 244,336 L 396,312", ZHE, 0.9, "none", "3,3")]
o += [P("M 448,318 L 496,336", ZHE, 0.9, "none", "3,3")]
o += [T(380, 380, "顺其性，还是贼其性？", 5.6, GREY)]
o += tail7(h, "率天下之人而祸仁义者，必子之言夫！", "图五十三", "杞柳桮桊", "ch142a")
save("ch142a-qiliu-beijuan.svg", o)

# ---------------------------------------------------------- 143 水之就下
o = head_("水 之 就 下", "《孟子》告子上　第一百四十三章　MZ143", h)
o += [T(380, 112, "决诸东方则东流，决诸西方则西流", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [P("M 160,296 L 240,296 L 240,326 L 320,326 L 320,356 L 400,356 L 400,404 L 160,404 Z",
       WARM, 1.2, fill=SOFT)]
o += [L(166, 316, 236, 316, ZONG, 0.7), L(246, 346, 316, 346, ZONG, 0.7), L(326, 376, 396, 376, ZONG, 0.7)]
o += [P("M 196,308 q 8,-5 16,0 q 8,5 16,0", ZONG, 0.7), P("M 286,338 q 8,-5 16,0 q 8,5 16,0", ZONG, 0.7),
      P("M 356,368 q 8,-5 16,0 q 8,5 16,0", ZONG, 0.7)]
o += [C(150, 300, 8, INK, 1.1), L(150, 308, 150, 358, INK, 1.2),
      L(150, 358, 138, 404, INK, 1.0), L(150, 358, 162, 404, INK, 1.0),
      L(150, 320, 132, 330, INK, 1.0), L(150, 320, 168, 330, INK, 1.0)]
o += [T(150, 424, "搏而跃之", 5.6, ZONG)]
o += [arrow(430, 320, 560, 388, ZHE, 1.1, 5)]
o += [T(580, 360, "就 下", 7.0, ZHE, ls=3)]
o += [T(560, 424, "水无有不下", 5.6, GREY)]
o += [T(300, 260, "可使过颡，可使在山——势也，非性也", 5.4, GREY)]
o += tail7(h, "人性之善也，犹水之就下也。", "图五十四", "水之就下", "ch143a")
save("ch143a-shui-zhijiuxia.svg", o)

# ---------------------------------------------------------- 144 生之谓性
o = head_("生 之 谓 性", "《孟子》告子上　第一百四十四章　MZ144", h)
o += [T(380, 112, "白羽之白　白雪之白　白玉之白", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
for i, nm in enumerate(["羽", "雪", "玉"]):
    x = 190 + i * 90
    o += [R(x - 26, 246, 52, 34, ZONG, 1.0, fill=PALE), T(x, 268, nm, 8.0, ZONG, ls=2)]
    if nm == "羽":
        o += [L(x - 10, 292, x + 10, 288, GREY, 0.8), L(x - 10, 292, x, 282, GREY, 0.7)]
    elif nm == "雪":
        o += [L(x - 8, 292, x + 8, 292, GREY, 0.8), L(x, 284, x, 298, GREY, 0.8)]
    else:
        o += [R(x - 10, 284, 20, 10, GREY, 0.8, fill=PALE)]
o += [T(380, 240, "皆 白", 7.0, ZHE, ls=4)]
o += [T(380, 332, "性", 16, INK, ls=8)]
o += [L(120, 350, 250, 350, LINE, 0.8), L(510, 350, 660, 350, LINE, 0.8)]
o += dog(210, 404, 0.9)
o += [T(210, 424, "犬", 6.4, ZONG)]
o += cow(310, 404, 1.0)
o += [T(310, 424, "牛", 6.4, ZONG)]
o += [stand(470, 404, 110, INK, 1.2)]
o += [T(470, 424, "人", 6.4, ZONG)]
o += [T(560, 300, "犬之性犹牛之性乎？", 5.6, GREY)]
o += [T(380, 380, "以气言之则同，以理言之则异", 5.6, GREY)]
o += tail7(h, "生之谓性也，犹白之谓白与？", "图五十五", "生之谓性", "ch144a")
save("ch144a-sheng-zhixing.svg", o)

# ---------------------------------------------------------- 145 仁内义外
o = head_("仁 内 义 外", "《孟子》告子上　第一百四十五章　MZ145", h)
o += [T(380, 112, "仁，内也，非外也；义，外也，非内也", 6.6, GREY, ls=1)]
o += [C(250, 300, 76, LINE, 1.0), C(250, 300, 70, LINE, 0.6)]
o += [T(250, 292, "仁", 13, INK, ls=4), T(250, 314, "内", 6.0, GREY, ls=2)]
o += [R(500, 244, 130, 112, LINE, 1.0), T(565, 288, "义", 13, INK, ls=4), T(565, 310, "外", 6.0, GREY, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [C(380, 330, 6, INK, 1.1), L(380, 336, 380, 372, INK, 1.2),
      L(380, 372, 366, 404, INK, 1.0), L(380, 372, 394, 404, INK, 1.0),
      L(380, 346, 404, 336, INK, 1.0), L(330, 336, 368, 346, INK, 1.0)]
o += [T(380, 260, "彼长而我长之", 6.0, ZHE)]
o += [T(380, 424, "长之者，我也——义不在彼", 5.6, GREY)]
o += tail7(h, "彼长而我长之，非有长于我也。", "图五十六", "仁内义外", "ch145a")
save("ch145a-rennei-yiwai.svg", o)

# ---------------------------------------------------------- 146 斯须之敬
o = head_("斯 须 之 敬", "《孟子》告子上　第一百四十六章　MZ146", h)
o += [T(380, 112, "庸敬在兄，斯须之敬在乡人", 6.6, GREY, ls=1)]
o += [R(200, 356, 196, 48, WARM, 1.2, fill=SOFT),
      R(216, 336, 164, 20, WARM, 1.1, fill=PALE)]
o += [L(196, 356, 196, 320, LINE, 0.8)]
for i in range(3):
    o += [R(398 + i * 22, 364 + i * 14, 22, 12, WARM, 1.0, fill=SOFT)]
o += [C(300, 322, 6, INK, 1.1), L(300, 328, 300, 372, INK, 1.2),
      L(300, 372, 288, 404, INK, 1.0), L(300, 372, 312, 404, INK, 1.0),
      L(300, 340, 280, 350, INK, 0.9), L(300, 340, 320, 350, INK, 0.9)]
o += [T(300, 302, "尸", 7.0, ZHE), T(300, 424, "弟为尸", 5.6, GREY)]
o += [T(240, 332, "堂上", 5.4, WARM)]
o += [stand(500, 404, 86, INK, 1.1)]
o += [T(500, 424, "乡人", 5.6, ZONG)]
o += [T(470, 340, "阶下", 5.4, WARM)]
o += [stand(620, 404, 90, INK, 1.1)]
o += [T(620, 424, "兄", 5.6, ZONG)]
o += [T(380, 240, "敬叔父乎？敬弟乎？——在位故也", 5.6, GREY)]
o += tail7(h, "庸敬在兄，斯须之敬在乡人。", "图五十七", "斯须之敬", "ch146a")
save("ch146a-sixu-zhijing.svg", o)

# ---------------------------------------------------------- 147 乃若其情
o = head_("乃 若 其 情", "《孟子》告子上　第一百四十七章　MZ147", h)
o += [T(380, 112, "恻隐　羞恶　恭敬　是非", 6.6, GREY, ls=2)]
o += [C(380, 300, 86, ZONG, 1.4)]
o += [L(380, 214, 380, 386, ZONG, 0.8), L(294, 300, 466, 300, ZONG, 0.8)]
o += [P("M 330,262 C 360,286 400,286 430,262", LINE, 0.6)]
o += [T(380, 246, "仁", 8.0, INK), T(380, 366, "智", 8.0, INK)]
o += [T(318, 306, "义", 8.0, INK), T(442, 306, "礼", 8.0, INK)]
o += [T(380, 300, "心", 7.0, ZHE, ls=3)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(250, 424, "非由外铄我也", 5.6, GREY), T(520, 424, "我固有之也", 5.6, GREY)]
o += [T(380, 424, "弗思耳矣", 5.8, ZHE)]
o += [T(380, 150, "求则得之，舍则失之", 5.6, GREY)]
o += tail7(h, "乃若其情，则可以为善矣，乃所谓善也。", "图五十八", "乃若其情", "ch147a")
save("ch147a-nairuo-qing.svg", o)

# ---------------------------------------------------------- 148 富岁凶岁
o = head_("富 岁 凶 岁", "《孟子》告子上　第一百四十八章　MZ148", h)
o += [T(380, 112, "非天之降才尔殊也，其所以陷溺其心者然也", 6.4, GREY, ls=1)]
o += field(140, 340, 220, 64)
o += field(400, 340, 220, 64)
for i in range(4):
    o += ear(180 + i * 42, 340, 50, ZONG, 1.0, True)
for i in range(4):
    o += ear(440 + i * 42, 340, 46, GREY, 0.9, False)
o += [T(250, 324, "富 岁", 7.0, ZONG, ls=3)]
o += [T(510, 324, "凶 岁", 7.0, GREY, ls=3)]
o += [T(250, 424, "子弟多赖", 5.6, ZONG), T(510, 424, "子弟多暴", 5.6, GREY)]
o += [T(380, 300, "麰麦同地同时", 5.6, ZHE)]
o += [P("M 372,308 L 372,332", LINE, 0.8, "none", "3,3"), P("M 388,308 L 388,332", LINE, 0.8, "none", "3,3")]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 206, "地有肥硗，雨露有养，人事不齐", 5.6, GREY)]
o += tail7(h, "圣人与我同类者。", "图五十九", "富岁凶岁", "ch148a")
save("ch148a-fusui-xiongsui.svg", o)

# ---------------------------------------------------------- 149 牛山之木
o = head_("牛 山 之 木", "《孟子》告子上　第一百四十九章　MZ149", h)
o += [T(380, 112, "斧斤伐之，牛羊又从而牧之", 6.6, GREY, ls=1)]
o += mountain(300, 404, 320, 130)
o += [L(190, 380, 220, 340, ZONG, 1.2), L(410, 380, 382, 336, ZONG, 1.2)]
o += axe(470, 300)
o += [L(250, 404, 300, 404, WARM, 1.0), L(300, 404, 350, 404, WARM, 1.0)]
o += [P("M 262,404 L 262,388 L 290,388 L 290,404 Z", ZONG, 1.0, fill=SOFT)]
o += [T(276, 424, "牛羊", 5.6, ZONG)]
o += [P("M 358,404 L 358,382", ZONG, 0.9), P("M 358,382 L 350,374", ZONG, 0.8), P("M 358,382 L 366,374", ZONG, 0.8)]
o += [T(358, 368, "萌蘖", 5.4, ZHE)]
o += [T(300, 292, "濯濯", 8.0, GREY, ls=3)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(560, 424, "此岂山之性也哉", 5.6, GREY)]
o += tail7(h, "苟得其养，无物不长；苟失其养，无物不消。", "图六十", "牛山之木", "ch149a")
save("ch149a-niushan-zhimu.svg", o)

# ---------------------------------------------------------- 150 一日暴之
o = head_("一 日 暴 之", "《孟子》告子上　第一百五十章　MZ150", h)
o += [T(380, 112, "一日暴之，十日寒之，未有能生者也", 6.6, GREY, ls=1)]
o += [L(120, 404, 300, 404, WARM, 1.2)]
o += [P("M 210,404 L 210,352", ZONG, 1.4), P("M 210,372 L 194,352", ZONG, 1.0), P("M 210,372 L 226,352", ZONG, 1.0)]
o += [P("M 210,352 L 202,340", ZONG, 0.8), P("M 210,352 L 218,340", ZONG, 0.8)]
o += [T(210, 424, "苗", 5.8, ZONG)]
o += [C(210, 268, 15, ZHE, 1.2), T(210, 273, "日", 8.6, ZHE)]
for i in range(8):
    a = i * 0.785
    o += [L(210 + 19 * math.cos(a), 268 + 19 * math.sin(a), 210 + 26 * math.cos(a), 268 + 26 * math.sin(a), ZHE, 0.8)]
o += [T(210, 236, "一日暴之", 5.6, ZHE)]
for i in range(10):
    x = 400 + (i % 5) * 46
    y = 310 + (i // 5) * 46
    o += [L(x - 7, y - 7, x + 7, y + 7, GREY, 0.9), L(x - 7, y + 7, x + 7, y - 7, GREY, 0.9)]
o += [T(492, 290, "十日寒之", 5.6, GREY)]
o += [L(300, 404, 660, 404, WARM, 1.2)]
o += [T(560, 424, "吾见亦罕矣", 5.6, GREY)]
o += [T(540, 200, "虽有天下易生之物", 5.4, GREY)]
o += tail7(h, "吾如有萌焉何哉？", "图六十一", "一日暴之", "ch150a")
save("ch150a-yiri-baozhi.svg", o)

# ---------------------------------------------------------- 151 舍生取义
o = head_("舍 生 取 义", "《孟子》告子上　第一百五十一章　MZ151", h)
o += [T(380, 112, "二者不可得兼", 6.6, GREY, ls=3)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += fish(230, 300, 110)
o += [T(230, 340, "鱼", 7.0, ZONG, ls=3)]
o += paw(500, 404, 86, 62)
o += [T(500, 360, "熊掌", 7.0, ZONG, ls=3)]
o += [P("M 356,258 L 356,346", ZHE, 1.4, "none", "5,4")]
o += [T(380, 300, "不　可　得　兼", 6.4, ZHE, ls=2)]
o += [T(380, 380, "取舍之间，见其所欲之深浅", 5.6, GREY)]
o += [T(380, 424, "所欲有甚于生者", 5.8, INK)]
o += tail7(h, "二者不可得兼，舍生而取义者也。", "图六十二", "舍生取义", "ch151a")
save("ch151a-shesheng-quyi.svg", o)
