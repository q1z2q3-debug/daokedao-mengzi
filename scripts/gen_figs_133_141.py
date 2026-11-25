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
"""万章下 图 133–141（v0.21.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail6(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 万章下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def bell(cx, top, H=96, col=INK, sw=1.3):
    """编钟：上窄下宽，口作弧，腹上一道横带。"""
    w1, w2 = 20, 44
    base = top + H
    return [L(cx, top - 14, cx, top, col, sw),
            P(f"M {cx-w1},{top} L {cx+w1},{top} L {cx+w2},{base-16} "
              f"Q {cx},{base-4} {cx-w2},{base-16} Z", col, sw, fill=SOFT),
            L(cx - w2 + 4, base - 16, cx + w2 - 4, base - 16, col, sw * 0.8),
            C(cx, top + 10, 3.4, col, 0.8)]


def chime(cx, top, col=INK, sw=1.2):
    """磬：折角石片，悬孔在上。"""
    return [L(cx, top - 14, cx, top + 6, col, sw),
            C(cx, top + 9, 3.2, col, 0.8),
            P(f"M {cx-40},{top+30} L {cx-6},{top+18} L {cx+40},{top+40} L {cx+32},{top+56} "
              f"L {cx-34},{top+52} Z", col, sw, fill=PALE)]


def seat(cx, y, w=110, col=WARM, sw=1.0):
    """席：扁椭圆。"""
    return [E(cx, y, w / 2, 9, col, sw, fill=SOFT)]


def bale(cx, y, w=86, hh=44, col=WARM, sw=1.2):
    """币帛一束：长方捆，中三道绳，上出两卷。"""
    o = [R(cx - w / 2, y - hh, w, hh, col, sw, fill=SOFT)]
    for i in range(3):
        o += [L(cx - w / 2 + 8 + i * 28, y - hh, cx - w / 2 + 8 + i * 28, y, ZONG, 0.7)]
    o += [E(cx - 16, y - hh - 4, 16, 6, col, sw * 0.9, fill=PALE),
          E(cx + 16, y - hh - 4, 16, 6, col, sw * 0.9, fill=PALE)]
    return o


def gate(cx, base, w=120, hh=112, open_=False, col=WARM, sw=1.2):
    """门：双柱、楣、槛，门扇一块。"""
    left = cx - w / 2
    o = [L(left, base, left, base - hh, col, sw), L(left + w, base, left + w, base - hh, col, sw),
         L(left - 8, base - hh, left + w + 8, base - hh, col, sw * 1.2),
         L(left, base, left + w, base, col, sw)]
    if open_:
        o += [R(left + 4, base - hh + 8, 26, hh - 8, col, sw * 0.9, fill=PALE)]
    else:
        o += [R(left + 12, base - hh + 8, w - 24, hh - 8, col, sw * 0.9, fill=SOFT)]
        o += [L(left + w / 2, base - hh + 8, left + w / 2, base, col, sw * 0.7)]
    return o


def clapper(cx, base, H=64, col=ZONG, sw=1.1):
    """柝：木梆与槌。"""
    return [R(cx - 10, base - H, 20, H - 18, col, sw, fill=SOFT),
            L(cx - 14, base - 20, cx + 14, base - 20, col, sw),
            L(cx + 18, base - 40, cx + 34, base - 56, col, sw * 0.9),
            C(cx + 36, base - 58, 4.2, col, sw * 0.8, fill=SOFT)]


def seal(cx, cy, s=54, col=ZHE, sw=1.4):
    """印：方玺，上钮，面作田字。"""
    o = [R(cx - s / 2, cy, s, s, col, sw, fill=PALE),
         R(cx - 9, cy - 12, 18, 12, col, sw * 0.9, fill=SOFT),
         L(cx, cy, cx, cy + s, col, sw * 0.7),
         L(cx - s / 2, cy + s / 2, cx + s / 2, cy + s / 2, col, sw * 0.7)]
    return o


def shrine(cx, base, w=110, hh=88, col=WARM, sw=1.2):
    """宗庙：屋、门洞、内一牌位。"""
    left = cx - w / 2
    return [P(f"M {left},{base} L {left},{base-hh} L {cx},{base-hh-30} L {left+w},{base-hh} L {left+w},{base}",
              col, sw, fill=SOFT),
            R(cx - 26, base - 52, 52, 52, col, sw * 0.9, fill=PALE),
            R(cx - 8, base - 44, 16, 26, ZONG, 0.9, fill=PALE)]


def arcring(cx, cy, r, col=LINE, sw=1.0):
    return P(f"M {cx-r},{cy} A {r},{r} 0 0 1 {cx+r},{cy}", col, sw)


h = 540

# ---------------------------------------------------------- 133 金声玉振
o = head_("金 声 玉 振", "《孟子》万章下　第一百三十三章　MZ133", h)
o += [T(380, 112, "伯夷之清　伊尹之任　柳下惠之和　孔子之时", 6.6, GREY, ls=1)]
o += [L(150, 232, 610, 232, WARM, 1.4), L(150, 232, 150, 404, WARM, 1.2), L(610, 232, 610, 404, WARM, 1.2)]
o += [L(150, 240, 610, 240, LINE, 0.8)]
o += bell(230, 268, 92)
o += [T(230, 384, "金 声", 7.4, ZONG, ls=2), T(230, 398, "始条理", 5.6, GREY)]
o += chime(530, 262)
o += [T(530, 384, "玉 振", 7.4, ZONG, ls=2), T(530, 398, "终条理", 5.6, GREY)]
o += [P("M 300,330 C 360,300 420,300 470,332", ZONG, 0.9, "none", "2,3")]
o += [T(380, 296, "八音之中，金石为重", 5.6, GREY, ls=1)]
o += [T(380, 428, "独奏一音，为一小成；八音毕奏，为一大成", 5.4, GREY)]
o += [L(128, 404, 632, 404, WARM, 1.3)]
o += tail6(h, "始条理者，智之事也；终条理者，圣之事也。", "图四十四", "金声玉振", "ch133a")
save("ch133a-jinsheng-yuzhen.svg", o)

# ---------------------------------------------------------- 134 周室班爵
o = head_("周 室 班 爵", "《孟子》万章下　第一百三十四章　MZ134", h)
o += [T(380, 112, "五等通于天下　六等施于国中", 6.6, GREY, ls=1)]
steps = [("下士", 0), ("中士", 1), ("上士", 2), ("大夫", 3), ("卿", 4), ("君", 5)]
x0, wid, riser = 150, 84, 34
pts = [f"M {x0},404"]
for i in range(6):
    x = x0 + i * wid
    pts.append(f"L {x},{404 - riser * i}")
    pts.append(f"L {x},{404 - riser * (i + 1)}")
pts.append(f"L {x0 + 6 * wid},{404 - riser * 6}")
pts.append(f"L {x0 + 6 * wid},404")
pts.append(f"L {x0},404")
o += [P(" ".join(pts), ZONG, 1.3, fill=SOFT)]
for i, (nm, _) in enumerate(steps):
    x = x0 + i * wid
    o += [T(x + wid / 2, 404 - riser * i - 8, nm, 6.4, ZONG)]
    o += [L(x, 404 - riser * i, x + wid, 404 - riser * i, LINE, 0.5)]
o += [T(380, 404 - riser * 6 - 16, "一级一阶，位高者田多", 5.6, GREY)]
o += [T(210, 226, "五等：天子·公·侯·伯·子男", 5.6, ZHE, anchor="start"),
      T(210, 240, "受地：千里／百里／七十／五十", 5.4, GREY, anchor="start")]
o += [T(380, 428, "诸侯恶其害己，而皆去其籍", 5.4, GREY)]
o += tail6(h, "其详不可得闻也，尝闻其略也。", "图四十五", "周室班爵", "ch134a")
save("ch134a-zhoushi-banue.svg", o)

# ---------------------------------------------------------- 135 友其德
o = head_("友 其 德", "《孟子》万章下　第一百三十五章　MZ135", h)
o += [T(380, 112, "不挟长　不挟贵　不挟兄弟", 6.6, GREY, ls=1)]
o += seat(250, 404, 132) + seat(510, 404, 132)
o += [C(250, 330, 6, INK, 1.2), L(250, 336, 250, 372, INK, 1.3),
      L(250, 372, 236, 404, INK, 1.1), L(250, 372, 264, 404, INK, 1.1),
      L(250, 344, 232, 356, INK, 1.0), L(250, 344, 268, 356, INK, 1.0)]
o += [C(510, 330, 6, INK, 1.2), L(510, 336, 510, 372, INK, 1.3),
      L(510, 372, 496, 404, INK, 1.1), L(510, 372, 524, 404, INK, 1.1),
      L(510, 344, 492, 356, INK, 1.0), L(510, 344, 528, 356, INK, 1.0)]
o += [P("M 300,344 L 460,344", ZONG, 1.0, "none", "3,3")]
o += [T(380, 332, "德", 8.4, ZHE, ls=3)]
o += [L(120, 404, 660, 404, WARM, 1.3)]
o += [T(200, 250, "长", 7.0, GREY), L(190, 240, 210, 258, ZHE, 1.1)]
o += [T(380, 250, "贵", 7.0, GREY), L(370, 240, 390, 258, ZHE, 1.1)]
o += [T(560, 250, "兄弟", 7.0, GREY), L(544, 240, 576, 258, ZHE, 1.1)]
o += [T(380, 428, "献子忘其势，五人者忘人之势", 5.4, GREY)]
o += tail6(h, "友也者，友其德也，不可以有挟也。", "图四十六", "友其德", "ch135a")
save("ch135a-you-qide.svg", o)

# ---------------------------------------------------------- 136 交际以恭
o = head_("交 际 以 恭", "《孟子》万章下　第一百三十六章　MZ136", h)
o += [T(380, 112, "其交也以道，其接也以礼", 6.6, GREY, ls=1)]
o += bale(220, 404, 96, 50)
o += [T(220, 424, "币帛", 5.6, ZONG)]
o += [C(560, 326, 6.2, INK, 1.2), L(560, 332, 560, 372, INK, 1.3),
      L(560, 372, 544, 404, INK, 1.1), L(560, 372, 576, 404, INK, 1.1),
      L(560, 344, 528, 336, INK, 1.0), L(560, 344, 528, 350, INK, 1.0)]
o += [T(560, 424, "受", 5.6, ZONG)]
o += [P("M 282,352 L 514,344", ZHE, 0.9, "none", "4,3")]
o += [T(400, 326, "却之？", 6.0, ZHE)]
o += [T(380, 250, "恭", 12, INK, ls=6)]
o += [T(380, 276, "尊者赐之，弗却也", 5.4, GREY)]
o += [L(120, 404, 660, 404, WARM, 1.3)]
o += [T(380, 428, "君子可欺以其方：受与不受，先看其道", 5.4, GREY)]
o += tail6(h, "交际何心也？曰：恭也。", "图四十七", "交际以恭", "ch136a")
save("ch136a-jiaoji-yigong.svg", o)

# ---------------------------------------------------------- 137 仕非为贫
o = head_("仕 非 为 贫", "《孟子》万章下　第一百三十七章　MZ137", h)
o += [T(380, 112, "为贫者，辞尊居卑，辞富居贫", 6.6, GREY, ls=1)]
o += gate(230, 404, 130, 120, open_=False)
o += [T(230, 424, "抱关", 5.8, ZONG)]
o += [C(400, 328, 6, INK, 1.2), L(400, 334, 400, 374, INK, 1.3),
      L(400, 374, 384, 404, INK, 1.1), L(400, 374, 416, 404, INK, 1.1),
      L(400, 346, 418, 352, INK, 1.0)]
o += clapper(440, 404, 60)
o += [T(456, 424, "击柝", 5.8, ZONG)]
o += [R(540, 366, 110, 38, ZONG, 1.0, fill=SOFT), T(595, 390, "尊位", 6.0, ZONG)]
o += [R(540, 384, 110, 20, ZONG, 1.0, fill=PALE), T(595, 398, "卑位", 6.0, ZONG)]
o += [P("M 590,358 C 620,330 610,318 556,326", ZHE, 0.9, "none", "4,3")]
o += [T(640, 320, "居卑", 5.6, ZHE)]
o += [L(120, 404, 660, 404, WARM, 1.3)]
o += [T(380, 428, "委吏会计当，乘田牛羊茁壮——大圣不以为辱", 5.4, GREY)]
o += tail6(h, "位卑而言高，罪也；立乎人之本朝而道不行，耻也。", "图四十八", "仕非为贫", "ch137a")
save("ch137a-shifei-weipin.svg", o)

# ---------------------------------------------------------- 138 不托诸侯
o = head_("不 托 诸 侯", "《孟子》万章下　第一百三十八章　MZ138", h)
o += [T(380, 112, "君馈之粟则受，赐之禄则不受", 6.6, GREY, ls=1)]
o += [R(150, 380, 84, 16, WARM, 1.2, fill=SOFT), L(160, 380, 160, 396, ZONG, 0.8), L(220, 380, 220, 396, ZONG, 0.8)]
o += [E(192, 372, 26, 8, ZONG, 1.1, fill=PALE), P("M 168,372 Q 192,354 216,372", ZONG, 1.0, fill=PALE)]
o += [T(192, 424, "鼎肉", 5.8, ZONG)]
o += [C(330, 334, 5.6, INK, 1.1), L(330, 340, 330, 374, INK, 1.1),
      L(330, 374, 316, 404, INK, 1.0), L(330, 374, 344, 404, INK, 1.0),
      L(330, 348, 312, 358, INK, 0.9), L(330, 348, 312, 364, INK, 0.9)]
o += [C(300, 352, 5.0, ZONG, 0.9, fill=SOFT)]
o += [T(330, 424, "使者", 5.6, ZONG)]
o += gate(560, 404, 130, 124, open_=True)
o += [T(560, 424, "大门之外", 5.8, ZONG)]
o += [P("M 356,352 C 430,330 470,330 490,352", ZHE, 1.0, "none", "3,2")]
o += [arrow(490, 352, 508, 360, ZHE, 0.9, 4)]
o += [T(430, 320, "摽使者出诸大门之外", 5.6, ZHE)]
o += [L(120, 404, 660, 404, WARM, 1.3)]
o += [T(380, 428, "悦贤不能举，又不能养，可谓悦贤乎", 5.4, GREY)]
o += tail6(h, "不以君命将之，不使贤者有亟拜之劳", "图四十九", "不托诸侯", "ch138a")
save("ch138a-bu-tuo-zhuhou.svg", o)

# ---------------------------------------------------------- 139 义路礼门
o = head_("义 路 礼 门", "《孟子》万章下　第一百三十九章　MZ139", h)
o += [T(380, 112, "夫义，路也；礼，门也", 6.6, GREY, ls=1)]
o += [L(120, 380, 470, 380, WARM, 1.2), L(120, 404, 470, 404, WARM, 1.2)]
o += [T(220, 396, "义　路", 6.4, ZONG, ls=2)]
for i in range(4):
    o += [L(160 + i * 86, 384, 152 + i * 86, 400, GREY, 0.6)]
o += gate(560, 404, 150, 140, open_=True)
o += [T(560, 268, "礼　门", 6.4, ZONG, ls=2)]
o += [C(300, 316, 6, INK, 1.2), L(300, 322, 300, 356, INK, 1.3),
      L(300, 356, 286, 380, INK, 1.1), L(300, 356, 314, 380, INK, 1.1),
      L(300, 330, 322, 340, INK, 1.0)]
o += [P("M 340,338 C 420,320 470,320 500,340", ZONG, 0.9, "none", "4,3")]
o += [arrow(500, 340, 524, 352, ZONG, 0.9, 4)]
o += [T(400, 430, "欲其入而闭之门，不可", 5.4, GREY)]
o += tail6(h, "惟君子能由是路，出入是门也。", "图五十", "义路礼门", "ch139a")
save("ch139a-yilu-limeng.svg", o)

# ---------------------------------------------------------- 140 尚友古人
o = head_("尚 友 古 人", "《孟子》万章下　第一百四十章　MZ140", h)
o += [T(380, 112, "一乡 → 一国 → 天下 → 古人", 6.6, GREY, ls=1)]
cx, cy = 300, 404
for r, nm, yy in ((62, "一乡", 350), (108, "一国", 316), (154, "天下", 282)):
    o += [arcring(cx, cy, r, LINE if r < 150 else GREY, 1.0)]
    o += [T(cx + r - 6, yy, nm, 6.0, ZONG, anchor="end")]
o += [L(120, 404, 470, 404, WARM, 1.3)]
o += [C(cx, cy - 16, 6, INK, 1.2), L(cx, cy - 10, cx, cy, INK, 1.2)]
o += [T(cx, cy - 28, "善士", 6.0, ZONG)]
o += slip(500, 328, 150, 34)
o += [T(575, 320, "颂其诗　读其书", 5.6, ZONG)]
o += [C(575, 300, 7.6, ZONG, 1.0), L(575, 308, 575, 348, ZONG, 1.1),
      L(575, 348, 562, 372, ZONG, 0.9), L(575, 348, 588, 372, ZONG, 0.9)]
o += [T(620, 300, "古人", 5.6, GREY, anchor="start")]
o += [P("M 460,360 C 480,344 496,340 508,336", ZHE, 0.9, "none", "4,3")]
o += [T(380, 430, "不知其人，可乎？是以论其世也", 5.4, GREY)]
o += tail6(h, "以友天下之善士为未足，又尚论古之人。", "图五十一", "尚友古人", "ch140a")
save("ch140a-shangyou-guren.svg", o)

# ---------------------------------------------------------- 141 易位与去
o = head_("易 位 与 去", "《孟子》万章下　第一百四十一章　MZ141", h)
o += [T(380, 112, "贵戚之卿　异姓之卿", 6.6, GREY, ls=1)]
o += shrine(190, 404, 120, 90)
o += [T(190, 424, "贵戚之卿", 5.8, ZONG)]
o += seal(570, 330, 56)
o += [T(570, 424, "异姓之卿", 5.8, ZONG)]
o += [P("M 260,300 L 340,300", LINE, 0.9, "none", "3,3")]
o += [T(300, 292, "君位", 5.6, GREY)]
o += [R(352, 288, 24, 16, ZONG, 0.9, fill=SOFT)]
o += [arrow(300, 330, 300, 292, ZHE, 1.0, 5), T(300, 344, "易位", 6.2, ZHE)]
o += [arrow(300, 372, 300, 400, GREY, 1.0, 5), T(300, 386, "去", 6.2, ZONG)]
o += [T(470, 246, "反复之而不听", 5.4, GREY)]
o += [L(120, 404, 660, 404, WARM, 1.3)]
o += [T(380, 430, "大过不听则易位，小过不听则去", 5.4, GREY)]
o += tail6(h, "亲疏不同，守经行权，各有其分。", "图五十二", "易位与去", "ch141a")
save("ch141a-yiwei-yuqu.svg", o)
