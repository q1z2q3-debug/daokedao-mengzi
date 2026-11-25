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
"""告子上 图 152–161（v0.23.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail8(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 告子上</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def heart(cx, cy, r=52, col=ZONG, sw=1.3, label="", ls=2):
    """心：一个圆，圆心书字。"""
    o = [C(cx, cy, r, col, sw), C(cx, cy, r - 6, LINE, 0.6)]
    if label:
        o += [T(cx, cy + 5, label, 12, INK, ls=ls)]
    return o


def road(x1, x2, ytop, ybot, col=WARM, sw=1.1):
    """路：两条收窄的边线，中间数道横缝。"""
    o = [L(x1, ybot, x2, ytop - 8, col, sw), L(x1 + 26, ybot, x2 - 6, ytop - 8, col, sw)]
    for i in range(5):
        t = i / 5.0
        yy = ybot - (ybot - ytop) * t
        w = (26 - 32 * t)
        o += [L(x1 + (x2 - x1) * t + 2, yy, x1 + (x2 - x1) * t + 2 + w, yy - 1, col, sw * 0.5)]
    return o


def hen(x, y, s=1.0, col=INK, sw=1.0):
    """鸡：小身、头上有冠、尾羽两笔。"""
    return [E(x, y - 16 * s, 14 * s, 11 * s, col, sw, fill=PALE),
            C(x - 15 * s, y - 30 * s, 6 * s, col, sw),
            L(x - 18 * s, y - 36 * s, x - 15 * s, y - 31 * s, col, sw * 0.8),
            P(f"M {x+12*s},{y-20*s} q {8*s},{-8*s} {12*s},{-2*s}", col, sw * 0.8),
            L(x - 4 * s, y - 6 * s, x - 4 * s, y, col, sw * 0.8),
            L(x + 4 * s, y - 6 * s, x + 4 * s, y, col, sw * 0.8)]


def hand(cx, base, w=96, col=ZONG, sw=1.2):
    """手：掌作方，四指作窄条上出，其一折而不伸；拇指在左。"""
    o = [R(cx - w / 2, base - 56, w, 56, col, sw, fill=PALE)]
    for i in range(4):
        x = cx - 32 + i * 21
        if i == 2:
            o += [R(x - 4, base - 80, 8, 24, col, sw, fill=PALE),
                  R(x + 4, base - 96, 8, 16, col, sw, fill=PALE)]
        else:
            o += [R(x - 4, base - 94, 8, 38, col, sw, fill=PALE)]
    o += [P(f"M {cx-w/2+2},{base-46} L {cx-w/2-16},{base-62} L {cx-w/2-10},{base-72} L {cx-w/2+4},{base-56} Z",
           col, sw, fill=PALE)]
    o += [T(cx, base + 16, "无名之指", 5.8, ZHE)]
    return o


def frutex(cx, base, H=54, col=ZONG, sw=1.1, thorn=False):
    """小树：双线干、左右两枝、各缀三叶。"""
    o = [P(f"M {cx-4},{base} L {cx-2},{base-H} L {cx+2},{base-H} L {cx+4},{base} Z", col, sw, fill=PALE)]
    for sgn, ly, dx in ((-1, 0.5, 26), (1, 0.68, 24), (-1, 0.86, 16)):
        x0 = cx + sgn * 3
        y0 = base - H * ly
        o += [P(f"M {x0},{y0} q {sgn*dx*0.5},-8 {sgn*dx},-6", col, sw)]
        for k in range(3):
            o += [E(x0 + sgn * dx * 0.75 + sgn * k * 5, y0 - 8 - k * 5, 5.5, 3.8, col, sw * 0.7, fill=SOFT)]
    if thorn:
        for i in range(3):
            o += [L(cx - 7 + i * 7, base - 10 - i * 9, cx - 13 + i * 7, base - 8 - i * 9, col, sw * 0.7)]
    return o


def girth(cx, base, H=54, col=WARM, sw=0.9):
    """拱把：两弧围干。"""
    o = [P(f"M {cx-14},{base-H*0.5} q -10,{-H*0.3} 4,{-H*0.55}", col, sw),
         P(f"M {cx+14},{base-H*0.5} q 10,{-H*0.3} -4,{-H*0.55}", col, sw)]
    return o


def hoe(cx, cy, col=ZONG, sw=1.2):
    return [L(cx + 26, cy + 40, cx - 6, cy - 30, col, sw * 1.1),
            P(f"M {cx-6},{cy-30} L {cx+6},{cy-34} L {cx+6},{cy-18} L {cx-8},{cy-16} Z", col, sw, fill=SOFT)]


def crown(cx, base, w=54, col=ZONG, sw=1.2):
    """冕：上为平板，下为帽身，两侧垂缨。"""
    o = [R(cx - w * 0.72, base - 46, w * 1.44, 7, col, sw * 1.1, fill=SOFT),
         P(f"M {cx-w/2},{base-46} q 0,-26 {w/2},-26 q {w/2},0 {w/2},26", col, sw, fill=PALE),
         L(cx - w * 0.3, base - 40, cx - w * 0.34, base - 10, col, sw * 0.7),
         L(cx + w * 0.3, base - 40, cx + w * 0.34, base - 10, col, sw * 0.7),
         L(cx, base - 46, cx, base - 58, col, sw * 0.9)]
    return o


def slip(cx, base, w=64, hh=76, col=ZONG, sw=1.1, n=4, label=""):
    """册：竖竹简加两道编绳。"""
    o = [R(cx - w / 2, base - hh, w, hh, col, sw, fill=PALE)]
    for i in range(1, n):
        o += [L(cx - w / 2 + i * w / n, base - hh, cx - w / 2 + i * w / n, base, col, sw * 0.6)]
    for j in range(2):
        yy = base - hh + 16 + j * (hh - 28)
        o += [L(cx - w / 2 - 3, yy, cx + w / 2 + 3, yy, col, sw * 0.9)]
    if label:
        o += [T(cx, base - hh / 2 + 4, label, 7.0, INK, ls=2)]
    return o


def jade(cx, cy, r=18, col=ZONG, sw=1.1):
    return [R(cx - r, cy - r, 2 * r, 2 * r, col, sw, fill=SOFT),
            C(cx, cy, r * 0.4, col, sw * 0.8)]


def bi(cx, cy, r=46, col=ZONG, sw=1.3, label=""):
    """璧：圆玉，中有穿，面作谷纹。"""
    o = [C(cx, cy, r, col, sw), C(cx, cy, r - 5, LINE, 0.7),
         C(cx, cy, r * 0.32, col, sw * 1.1)]
    for i in range(8):
        a = i * 0.785
        x = cx + r * 0.66 * math.cos(a)
        y = cy + r * 0.66 * math.sin(a)
        o += [C(x, y, 2.6, col, sw * 0.7)]
    if label:
        o += [T(cx, cy + r + 18, label, 6.4, INK, ls=2)]
    return o


def gui(cx, base, w=52, hh=104, col=ZONG, sw=1.2, label=""):
    """圭：上锐下平的玉版，中有穿。"""
    o = [P(f"M {cx-w/2},{base} L {cx-w/2},{base-hh*0.86} L {cx},{base-hh} L {cx+w/2},{base-hh*0.86} "
           f"L {cx+w/2},{base} Z", col, sw, fill=PALE),
         C(cx, base - hh * 0.58, 7, col, sw * 0.9)]
    for i in range(3):
        o += [L(cx - w * 0.34, base - 12 - i * 10, cx + w * 0.34, base - 12 - i * 10, col, sw * 0.5)]
    if label:
        o += [T(cx, base - hh * 0.24, label, 7.0, INK, ls=2)]
    return o


def cupwater(cx, base, w=44, hh=34, col=ZONG, sw=1.1):
    return [P(f"M {cx-w/2},{base-hh} L {cx-w*0.34},{base} L {cx+w*0.34},{base} L {cx+w/2},{base-hh} Z", col, sw, fill=SOFT),
            E(cx, base - hh, w / 2, 6, col, sw, fill=PALE)]


def fire(cx, base, w=56, col=ZHE, sw=1.0):
    return [P(f"M {cx},{base} q {-w*0.5},{-w*0.5} {-w*0.2},{-w*0.9} q {w*0.2},{w*0.5} {w*0.3},{w*0.2} "
              f"q {w*0.3},{-w*0.4} {w*0.1},{-w*0.75} q {w*0.4},{w*0.5} {w*0.3},{w*1.0} "
              f"q {-w*0.4},{w*0.16} {-w*0.5},0 Z", col, sw)]


def sheaf(cx, base, H=96, col=ZONG, sw=1.1, ripe=True):
    """一束禾：三茎上出，穗下垂，中系一道。"""
    o = [L(cx - 22, base, cx - 14, base - H * 0.8, col, sw),
         L(cx + 2, base, cx + 2, base - H, col, sw),
         L(cx + 22, base, cx + 14, base - H * 0.8, col, sw)]
    o += [L(cx - 24, base - H * 0.34, cx + 24, base - H * 0.34, col, sw * 1.1)]
    for dx, top in ((-16, 0.8), (2, 1.0), (18, 0.8)):
        y0 = base - H * top
        o += [P(f"M {cx+dx},{y0-6} q 2,14 8,26", col, sw)]
        o += [P(f"M {cx+dx+8},{y0+20} q 6,4 9,0", col, sw * 0.8)]
        for k in range(3):
            o += [E(cx + dx + 10, y0 + 24 + k * 6, 4.6, 5.6, col, sw * 0.8, fill=SOFT)]
            o += [L(cx + dx + 8, y0 + 22 + k * 6, cx + dx + 3, y0 + 19 + k * 6, col, sw * 0.5)]
    return o


def weed(cx, base, H=70, col=GREY, sw=0.9):
    """荑稗：细叶四散，穗作散芒。"""
    o = []
    for i, sgn in ((0, -1), (1, 1), (2, -1), (3, 1)):
        w = 14 + i * 5
        o += [P(f"M {cx},{base} q {sgn*w*0.5},{-H*0.5} {sgn*w},{ -H*0.85}", col, sw)]
    for sgn in (-1, 1):
        o += [P(f"M {cx},{base} L {cx+sgn*6},{base-H}", col, sw * 0.8)]
        for k in range(3):
            o += [L(cx + sgn * (6 + k * 6), base - H + k * 8, cx + sgn * (6 + k * 6 + 7 * sgn), base - H + k * 8 - 6, col, sw * 0.6)]
    return o


def bow(cx, base, w=44, hh=110, col=ZONG, sw=1.3):
    """弓：满彀。"""
    o = [P(f"M {cx+w/2},{base} q {-w*1.5},{-hh*0.5} 0,{-hh}", col, sw * 1.4),
         L(cx + w / 2, base, cx + w / 2, base - hh, GREY, sw * 0.9),
         L(cx + w / 2 + 4, base - hh * 0.5, cx - w * 0.62, base - hh * 0.5, ZONG, sw * 0.9),
         P(f"M {cx-w*0.62},{base-hh*0.5} L {cx-w*0.62-10},{base-hh*0.5-4} L {cx-w*0.62-10},{base-hh*0.5+4} Z", ZONG, sw * 0.8, fill=SOFT)]
    for i in range(3):
        o += [L(cx + 6 - i * 4, base - hh * 0.5 + 8 + i * 4, cx + w * 0.2, base - 8 + i * 4, ZONG, sw * 0.7)]
    return o


def compass(cx, cy, r=34, col=ZONG, sw=1.2):
    """规：两脚一圆。"""
    return [C(cx, cy, r, col, sw * 0.7),
            L(cx - 8, cy - 26, cx - 12, cy + 30, col, sw * 1.2),
            L(cx + 8, cy - 26, cx + 22, cy + 30, col, sw * 1.2),
            C(cx, cy - 30, 4, col, sw)]


def square_tool(cx, cy, w=54, col=ZONG, sw=1.2):
    """矩：曲尺。"""
    return [P(f"M {cx-8},{cy-26} L {cx+w},{cy-26} L {cx+w},{cy-14} L {cx+4},{cy-14} "
              f"L {cx+4},{cy+34} L {cx-8},{cy+34} Z", col, sw, fill=PALE)]


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

# ---------------------------------------------------------- 152 仁人心也
o = head_("仁 人 心 也", "《孟子》告子上　第一百五十二章　MZ152", h)
o += [T(380, 112, "仁，人心也；义，人路也", 6.6, GREY, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += heart(214, 296, 54, ZONG, 1.3, "仁")
o += [T(214, 386, "人 心", 6.0, ZONG, ls=2)]
o += [P("M 420,404 L 660,352 L 660,342 L 448,404 Z", WARM, 1.0, fill=SOFT)]
o += [L(452,400, 640,352, LINE, 0.6)]
o += [T(560, 424, "人 路", 6.0, ZONG, ls=2)]
o += hen(330, 404, 1.15), dog(392, 404, 0.9)
o += [T(330, 424, "鸡", 5.6, GREY), T(392, 424, "犬", 5.6, GREY)]
o += [P("M 470,300 q -110,26 -160,4", ZHE, 1.1)]
o += [P("M 310,304 L 322,296 L 320,312 Z", ZHE, 1.0, fill=ZHE)]
o += [T(494, 288, "求 其 放 心", 6.0, ZHE, ls=2)]
o += [T(330, 214, "舍其路而弗由，放其心而不知求", 5.6, GREY)]
o += tail8(h, "学问之道无他，求其放心而已矣。", "图六十三", "仁人心也", "ch152a")
save("ch152a-ren-renxin.svg", o)

# ---------------------------------------------------------- 153 无名指
o = head_("无 名 之 指", "《孟子》告子上　第一百五十三章　MZ153", h)
o += [T(380, 112, "指不若人，则知恶之；心不若人，则不知恶", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [R(200, 302, 26, 102, ZONG, 1.2, fill=PALE)]
o += [L(213, 302, 213, 288, ZONG, 0.8)]
o += [P("M 200,302 q 13,-14 26,0", ZONG, 1.2)]
o += [R(226, 276, 52, 26, ZONG, 1.2, fill=PALE)]
o += [P("M 278,276 q 14,13 0,26", ZONG, 1.2)]
o += [E(286, 289, 5, 7, ZONG, 0.8, fill=SOFT)]
o += [L(190, 360, 196, 358, LINE, 0.7)]
o += [T(250, 348, "屈 而 不 信", 5.6, ZHE, ls=1)]
o += [T(228, 424, "无名之指", 5.8, ZONG, ls=1)]
o += [P("M 300,322 L 540,296", LINE, 0.9, "none", "4,4")]
o += [R(548, 276, 96, 56, WARM, 1.1, fill=SOFT)]
o += [L(576, 276, 576, 332, WARM, 0.9), L(616, 276, 616, 332, WARM, 0.9)]
o += [L(548, 276, 644, 276, WARM, 1.4)]
o += [T(596, 268, "秦 楚", 5.8, ZONG, ls=2)]
o += [T(420, 306, "不远千里", 5.4, GREY)]
o += heart(560, 200, 24, GREY, 0.9, "心")
o += [T(560, 240, "则不知恶", 5.4, GREY)]
o += [T(380, 172, "指不若人，则知恶之", 5.6, ZHE)]
o += tail8(h, "心不若人，则不知恶，此之谓不知类也。", "图六十四", "无名之指", "ch153a")
save("ch153a-wuming-zhizhi.svg", o)

# ---------------------------------------------------------- 154 拱把桐梓
o = head_("拱 把 桐 梓", "《孟子》告子上　第一百五十四章　MZ154", h)
o += [T(380, 112, "拱把之桐梓，人苟欲生之，皆知所以养之者", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += frutex(210, 404, 96, ZONG, 1.2), frutex(300, 404, 84, ZONG, 1.2)
o += girth(210, 404, 96), girth(300, 404, 84)
o += [T(255, 424, "拱把之桐梓", 5.8, ZONG, ls=1)]
o += [T(255, 292, "皆知养之", 5.6, GREY)]
o += [stand(520, 404, 108, INK, 1.2)]
o += [C(520, 340, 5, ZHE, 1.0)]
o += [T(520, 424, "至于身", 5.8, ZONG, ls=1)]
o += [T(520, 372, "不知所以养", 5.6, ZHE)]
o += [P("M 360,330 L 470,330", LINE, 0.9, "none", "3,3")]
o += [T(380, 210, "岂爱身不若桐梓哉？", 5.6, GREY)]
o += tail8(h, "弗思甚也。", "图六十五", "拱把桐梓", "ch154a")
save("ch154a-gongba-tongzi.svg", o)

# ---------------------------------------------------------- 155 人之于身
o = head_("养 其 大 者", "《孟子》告子上　第一百五十五章　MZ155", h)
o += [T(380, 112, "体有贵贱，有小大；无以小害大，无以贱害贵", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += stand(200, 404, 128, INK, 1.2)
o += [C(200, 328, 15, ZHE, 1.0), T(200, 331, "心", 6.4, ZHE)]
o += [T(200, 302, "贵 · 大", 5.4, ZONG)]
o += [C(200, 372, 11, GREY, 0.9), T(200, 374, "口", 5.0, GREY)]
o += [T(200, 396, "贱 · 小", 5.4, GREY)]
o += [L(120, 396, 160, 396, LINE, 0.8)]
o += hoe(360, 330)
o += frutex(300, 404, 84, ZONG, 1.1, False), frutex(420, 404, 64, GREY, 0.9, True)
o += [T(300, 424, "梧 槚", 5.6, ZONG, ls=1), T(420, 424, "樲 棘", 5.6, GREY, ls=1)]
o += [T(360, 268, "场 师", 5.6, ZONG)]
o += [T(530, 300, "舍其梧槚，养其樲棘", 5.4, GREY)]
o += [T(530, 330, "则为贱场师焉", 5.4, GREY)]
o += [T(380, 200, "养其小者为小人，养其大者为大人", 5.8, ZHE)]
o += tail8(h, "饮食之人，则人贱之矣，为其养小以失大也。", "图六十六", "养其大者", "ch155a")
save("ch155a-yangqi-dazhe.svg", o)

# ---------------------------------------------------------- 156 先立乎大
o = head_("先 立 乎 大", "《孟子》告子上　第一百五十六章　MZ156", h)
o += [T(380, 112, "钧是人也，或为大人，或为小人，何也？", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += stand(240, 404, 118, INK, 1.2)
o += [C(240, 326, 14, ZHE, 1.1)]
o += [T(292, 326, "大 体", 5.4, ZHE)]
o += [T(240, 424, "从其大体", 5.6, ZONG)]
o += [L(430, 210, 430, 404, LINE, 0.8)]
o += stand(530, 404, 118, INK, 1.2)
o += [C(530, 352, 4.4, GREY, 0.9), C(546, 352, 4.4, GREY, 0.9),
      E(518, 358, 6, 3.4, GREY, 0.8), E(558, 358, 6, 3.4, GREY, 0.8)]
o += [T(586, 344, "小 体", 5.4, GREY)]
o += [T(530, 424, "从其小体", 5.6, ZONG)]
o += [T(240, 214, "心之官则思", 5.6, ZHE)]
o += [T(530, 214, "耳目之官不思", 5.6, GREY)]
o += [T(380, 268, "钧 是 人 也", 6.4, INK, ls=3)]
o += tail8(h, "先立乎其大者，则其小者不能夺也。", "图六十七", "先立乎大", "ch156a")
save("ch156a-xianli-huda.svg", o)

# ---------------------------------------------------------- 157 天爵人爵
o = head_("天 爵 人 爵", "《孟子》告子上　第一百五十七章　MZ157", h)
o += [T(380, 112, "仁义忠信，乐善不倦，此天爵也", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += bi(220, 336, 46, ZONG, 1.3, "仁义")
o += [T(220, 424, "天 爵", 6.0, ZONG, ls=2)]
o += crown(510, 404, 60)
o += [T(510, 424, "人 爵", 6.0, ZONG, ls=2)]
o += [T(510, 344, "公卿大夫", 5.4, GREY)]
o += [arrow(300, 322, 466, 322, ZHE, 1.0, 4)]
o += [T(384, 300, "修天爵而人爵从之", 5.4, ZHE)]
o += [P("M 470,352 L 316,352", GREY, 0.9, "none", "4,3")]
o += [T(384, 372, "今人修天爵以要人爵", 5.4, GREY)]
o += [T(380, 214, "既得人爵，而弃其天爵，则惑之甚者也", 5.4, GREY)]
o += tail8(h, "终亦必亡而已矣。", "图六十八", "天爵人爵", "ch157a")
save("ch157a-tianjue-renjue.svg", o)

# ---------------------------------------------------------- 158 良贵
o = head_("良 贵", "《孟子》告子上　第一百五十八章　MZ158", h)
o += [T(380, 112, "欲贵者，人之同心也；人人有贵于己者，弗思耳", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += stand(220, 404, 118, INK, 1.2)
o += [jade(220, 322, 14)]
o += [T(220, 296, "良 贵", 6.0, ZHE, ls=2)]
o += [T(220, 424, "在我者", 5.4, GREY)]
o += stand(560, 404, 118, INK, 1.2)
o += crown(620, 330, 46)
o += [L(568, 330, 600, 330, ZONG, 1.0)]
o += [T(620, 300, "赵孟之所贵", 5.4, GREY)]
o += [T(560, 424, "在人者", 5.4, GREY)]
o += [arrow(330, 322, 486, 322, ZHE, 1.0, 4)]
o += [T(408, 306, "赵孟能贱之", 5.4, ZHE)]
o += [T(380, 210, "既醉以酒，既饱以德", 6.0, INK, ls=2)]
o += tail8(h, "言饱乎仁义也，所以不愿人之膏粱之味也。", "图六十九", "良贵", "ch158a")
save("ch158a-lianggui.svg", o)

# ---------------------------------------------------------- 159 杯水车薪
o = head_("杯 水 车 薪", "《孟子》告子上　第一百五十九章　MZ159", h)
o += [T(380, 112, "仁之胜不仁也，犹水胜火", 6.6, GREY, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += cupwater(180, 404, 46, 36)
o += [T(180, 336, "一 杯 水", 5.8, ZONG, ls=1)]
o += [E(470, 384, 20, 20, WARM, 1.2), E(470, 384, 6, 6, WARM, 0.9),
      E(610, 384, 20, 20, WARM, 1.2), E(610, 384, 6, 6, WARM, 0.9)]
o += [R(420, 356, 250, 14, ZONG, 1.2, fill=SOFT),
      L(420, 370, 420, 384, ZONG, 1.0), L(670, 370, 670, 384, ZONG, 1.0)]
o += [L(420, 360, 372, 366, ZONG, 1.0), L(420, 368, 374, 374, ZONG, 1.0)]
o += [fire(545, 356, 84)]
o += [T(600, 324, "一 车 薪 之 火", 5.8, ZHE, ls=1)]
o += [P("M 214,346 q 40,-30 90,10", ZHE, 1.0)]
o += [T(300, 320, "不 熄", 5.4, ZHE)]
o += [T(380, 210, "犹以一杯水救一车薪之火也", 5.6, GREY)]
o += tail8(h, "此又与于不仁之甚者也，亦终必亡而已矣。", "图七十", "杯水车薪", "ch159a")
save("ch159a-beishui-chexin.svg", o)

# ---------------------------------------------------------- 160 五谷不熟
o = head_("五 谷 不 熟", "《孟子》告子上　第一百六十章　MZ160", h)
o += [T(380, 112, "五谷者，种之美者也；苟为不熟，不如荑稗", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += sheaf(220, 404, 108, ZONG, 1.1, True)
o += [T(220, 424, "五 谷 · 熟", 5.8, ZONG, ls=1)]
o += weed(520, 404, 84)
o += [T(520, 424, "荑 稗", 5.8, GREY, ls=1)]
o += [T(380, 300, "熟", 14, ZHE, ls=6)]
o += [T(380, 340, "夫仁亦在乎熟之而已矣", 5.6, GREY)]
o += [T(380, 210, "苟为不熟，不如荑稗", 5.6, GREY)]
o += tail8(h, "夫仁亦在乎熟之而已矣。", "图七十一", "五谷不熟", "ch160a")
save("ch160a-wugu-bushu.svg", o)

# ---------------------------------------------------------- 161 志于彀
o = head_("志 于 彀", "《孟子》告子上　第一百六十一章　MZ161", h)
o += [T(380, 112, "羿之教人射，必志于彀；大匠诲人，必以规矩", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += bow(250, 404, 46, 120)
o += [T(250, 424, "必 志 于 彀", 5.8, ZONG, ls=1)]
o += [T(250, 258, "弓 满", 5.4, GREY)]
o += [L(430, 210, 430, 404, LINE, 0.8)]
o += square_tool(490, 340)
o += compass(586, 348, 30)
o += [T(540, 424, "规 矩", 5.8, ZONG, ls=2)]
o += [T(540, 258, "大 匠", 5.4, GREY)]
o += [T(380, 190, "学者亦必志于彀　学者亦必以规矩", 5.4, GREY)]
o += tail8(h, "事必有法，然后可成。", "图七十二", "志于彀", "ch161a")
save("ch161a-zhiyugou.svg", o)
