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
"""尽心下 图 155–164（v0.33.0 第三批十图，二次返工稿）
跨批 helper 不复用：本文件内重定义 tail_（卷名尽心下）/reed/grip/rail/tiger/yan/curve。
"""


def tail_(h, q, label, name, key):
    return [
        L(120, h - 104, 640, h - 104, LINE, 1),
        T(380, h - 80, q, 8.6, INK, ls=2),
        f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 尽心下</text>',
        f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>',
    ]


def foot(x, y, w=4.6):
    """足迹：一枚小椭圆。"""
    return E(x, y, w, w * 0.55, WARM, 0.7, WARM)


def reed(x, y, n=3, ln=30, down=True, col=ZONG, sw=0.9, sp=9.0, tilt=0.0):
    """茅草一簇：自根部散开的细线，长短不一。"""
    sgn = 1 if down else -1
    o = []
    k = (n - 1) / 2.0
    for i in range(n):
        L_ = ln * (0.82 + 0.18 * ((i * 3) % 4) / 3.0)
        dx = (i - k) * sp
        o += [P(f"M {x},{y} C {x+dx*0.3+tilt*0.3},{y+sgn*L_*0.42} "
                f"{x+dx*0.85+tilt*0.75},{y+sgn*L_*0.76} {x+dx+tilt},{y+sgn*L_}", col, sw)]
    return o


def grip(x, y, ln=26, sgn=1, col=ZHE, sw=1.3):
    """一只手：前臂＋掌＋三指（sgn=1 向下）。"""
    o = [L(x, y - sgn * ln, x, y, col, sw * 1.4),
         P(f"M {x-12},{y} L {x+8},{y} L {x+8},{y+sgn*9} L {x-12},{y+sgn*9} Z", col, sw, SOFT)]
    for i in range(3):
        o += [L(x - 7 + i * 7, y + sgn * 9, x - 6 + i * 7, y + sgn * 20, col, sw * 1.1)]
    o += [L(x - 12, y + sgn * 4, x - 20, y + sgn * 12, col, sw * 1.1)]
    return o


def rail(x0, x1, ybot, ytop, n=7, col=ZONG, sw=1.1):
    """栅栏：n 根竖桩＋两道横杆＋桩顶尖齿。"""
    o = []
    w = (x1 - x0) / (n - 1)
    for i in range(n):
        x = x0 + i * w
        o += [L(x, ybot, x, ytop + 4, col, sw * 1.3)]
        o += [P(f"M {x-4},{ytop+11} L {x},{ytop} L {x+4},{ytop+11}", col, sw)]
    o += [L(x0, ytop + (ybot - ytop) * 0.3, x1, ytop + (ybot - ytop) * 0.3, col, sw * 0.9),
          L(x0, ytop + (ybot - ytop) * 0.66, x1, ytop + (ybot - ytop) * 0.66, col, sw * 0.9)]
    return o


def tiger(cx, fy, s=24, col=INK, sw=1.2):
    """伏虎：椭身、四短腿、长尾上卷、双耳。"""
    o = [E(cx, fy - s * 0.55, s, s * 0.48, col, sw, SOFT)]
    o += [C(cx + s * 0.98, fy - s * 0.84, s * 0.33, col, sw, SOFT)]
    o += [P(f"M {cx+s*1.10},{fy-s*1.04} L {cx+s*1.16},{fy-s*1.26} L {cx+s*0.96},{fy-s*1.14}", col, sw * 0.8),
          P(f"M {cx+s*0.84},{fy-s*1.06} L {cx+s*0.86},{fy-s*1.28} L {cx+s*0.70},{fy-s*1.14}", col, sw * 0.8)]
    for i in range(4):
        dx = -s * 0.74 + i * s * 0.48
        o += [L(cx + dx, fy - s * 0.2, cx + dx, fy, col, sw)]
    o += [P(f"M {cx-s*0.94},{fy-s*0.62} C {cx-s*1.42},{fy-s*1.06} {cx-s*1.24},{fy-s*1.52} {cx-s*1.62},{fy-s*1.42}",
            col, sw * 1.1)]
    return o


def yan(x, y, ln=38, col=INK, sw=1.2):
    """薄刃：两条收敛的线收成尖，内有刃面，后接短柄。"""
    return [P(f"M {x},{y-7} L {x+ln},{y-ln*0.16} L {x},{y+7} Z", col, sw, PALE),
            L(x - 9, y + 1.0, x, y + 2.0, col, sw * 1.4)]


h = 540

# ---------------------------------------------------------- 155 茅塞子心
o = head_("茅 塞 子 心", "《孟子》尽心下　第二百四十四章　MZ244", h)
o += [T(380, 112, "山径之蹊间，介然用之而成路；为间不用，则茅塞之矣", 6.0, ZONG, ls=1.2)]
# 路带
o += [R(140, 306, 480, 60, ZONG, 0.4, SOFT)]
o += [L(140, 306, 620, 306, ZONG, 1.8), L(140, 366, 620, 366, ZONG, 1.8)]
o += [P("M 140,336 L 620,336", WARM, 0.7, "none", "8,5")]
# 缺口：截断右段路面
o += [R(540, 300, 34, 72, PAPER, 0, PAPER)]
o += [L(140, 306, 540, 306, ZONG, 1.8), L(574, 306, 620, 306, ZONG, 1.8)]
o += [L(140, 366, 540, 366, ZONG, 1.8), L(574, 366, 620, 366, ZONG, 1.8)]
o += [L(540, 306, 540, 366, ZONG, 1.2), L(574, 306, 574, 366, ZONG, 1.2)]
o += [P("M 540,336 L 530,336", LINE, 0.8), P("M 574,336 L 584,336", LINE, 0.8)]
# 左段足迹
o += [foot(206, 344), foot(232, 350), foot(258, 344), foot(284, 350)]
# 右侧两侧茅草丛生
for x in (474, 508, 600):
    o += reed(x, 306, 3, 32, True, tilt=3)
    o += reed(x, 366, 3, 32, False, tilt=-3)
for x in (440, 578, 616):
    o += reed(x, 306, 2, 24, True, sp=12)
    o += reed(x, 366, 2, 24, False, sp=12)
o += [T(260, 296, "介然用之而成路", 4.8, WARM, ls=0.5)]
o += [T(614, 296, "为间不用", 4.8, WARM, ls=0.5)]
o += [T(557, 400, "茅 塞", 5.6, ZHE, ls=2)]
o += [T(180, 394, "蹊（痕）", 4.6, WARM, ls=0)]
o += [T(380, 424, "一刻走成，一刻不走即塞", 6.2, INK, ls=2)]
o += tail_(h, "路是每天走出来的，也是隔几天就荒的。", "图一百五十五", "茅塞子心", "ch244a")
save("ch244a-mao-sai-zixin.svg", o)

# ---------------------------------------------------------- 156 追蠡
o = head_("追 蠡", "《孟子》尽心下　第二百四十五章　MZ245", h)
o += [T(380, 112, "禹之声，尚文王之声——以追蠡", 6.0, ZONG, ls=1.4)]
# 悬梁与绳
o += [L(270, 136, 390, 136, ZONG, 1.6)]
o += [L(330, 136, 330, 178, ZONG, 1.0)]
o += [P("M 324,140 L 330,132 L 336,140", ZONG, 1.0)]
# 钟纽（工形）＋三处啮口
o += [R(316, 178, 28, 26, ZONG, 1.2, SOFT)]
o += [L(298, 184, 362, 184, ZONG, 2.0), L(298, 196, 362, 196, ZONG, 1.6)]
o += [P("M 306,184 L 310,192 L 314,184", ZHE, 1.6),
      P("M 324,184 L 328,192 L 332,184", ZHE, 1.6),
      P("M 342,184 L 346,192 L 350,184", ZHE, 1.6)]
# 钟身
o += [P("M 290,204 L 370,204 L 410,336 L 250,336 Z", ZONG, 1.4, SOFT)]
o += [L(250, 336, 410, 336, ZONG, 2.4), L(244, 344, 416, 344, ZONG, 1.6)]
o += [L(266, 288, 394, 288, GREY, 0.7), L(274, 262, 386, 262, GREY, 0.7)]
o += [T(250, 174, "纽", 5.2, ZONG, ls=1)]
o += [T(380, 180, "三道啮痕", 4.6, ZHE, ls=0)]
o += [T(330, 380, "追蠡：钟纽之啮", 5.4, ZONG, ls=1.4)]
# 城门
# 城墙：左右两段矮墙＋门洞
o += [R(430, 300, 200, 104, ZONG, 0.8, SOFT)]
o += [L(430, 300, 430, 404, ZONG, 1.4), L(630, 300, 630, 404, ZONG, 1.4)]
o += [L(430, 300, 630, 300, ZONG, 1.8)]
o += [P("M 434,322 L 466,322", GREY, 0.6), P("M 554,322 L 626,322", GREY, 0.6),
      P("M 434,352 L 466,352", GREY, 0.6), P("M 554,352 L 626,352", GREY, 0.6),
      P("M 434,380 L 466,380", GREY, 0.6), P("M 554,380 L 626,380", GREY, 0.6)]
o += [P("M 470,404 L 470,336 C 470,318 550,318 550,336 L 550,404", ZONG, 1.6, PALE)]
o += [P("M 470,336 C 470,318 550,318 550,336", ZONG, 1.6)]
o += [L(466, 404, 554, 404, ZONG, 2.0)]
# 辙：门洞内两道土痕
o += [P("M 484,396 L 540,396", WARM, 1.6), P("M 484,404 L 540,404", WARM, 1.6)]
o += [T(556, 292, "城门之轨", 4.8, ZONG, ls=1)]
o += [T(470, 210, "两马之力与？", 4.6, WARM, ls=1)]
o += tail_(h, "痕迹是事实，归因是推断。", "图一百五十六", "追蠡", "ch245a")
save("ch245a-zhui-li.svg", o)

# ---------------------------------------------------------- 157 冯妇搏虎
o = head_("冯 妇 搏 虎", "《孟子》尽心下　第二百四十六章　MZ246", h)
o += [T(380, 112, "虎负嵎，莫之敢撄。望见冯妇，趋而迎之", 6.0, ZONG, ls=1.2)]
o += [P("M 118,362 L 156,262 L 196,300 L 240,230 L 278,362", ZONG, 1.4, SOFT)]
o += [P("M 358,362 L 396,262 L 436,300 L 480,230 L 518,362", ZONG, 1.4, SOFT)]
o += [L(118, 362, 278, 362, ZONG, 1.6), L(358, 362, 518, 362, ZONG, 1.6)]
o += [L(118, 404, 522, 404, ZONG, 1.6)]
o += tiger(318, 362, 27)
o += [T(318, 330, "虎负嵎", 4.8, WARM, ls=0.5)]
o += [T(318, 388, "嵎", 4.8, ZONG, ls=1)]
# 攘臂之人（山前平地）
o += [stand(222, 404, 120, INK, 1.2)]
o += [L(222, 316, 198, 274, INK, 1.1), L(222, 316, 246, 274, INK, 1.1)]
o += [T(222, 258, "攘臂下车", 4.8, ZHE, ls=0.5)]
# 远处三众
for xx in (572, 598, 624):
    o += [C(xx, 350, 5.2, INK, 0.9), L(xx, 355, xx, 396, INK, 1.0),
          L(xx, 396, xx - 5, 404, INK, 0.9), L(xx, 396, xx + 5, 404, INK, 0.9),
          L(xx, 362, xx - 13, 350, INK, 0.85), L(xx, 362, xx + 9, 352, INK, 0.8)]
o += [T(598, 338, "众皆悦之", 4.6, WARM, ls=1)]
o += [T(380, 424, "众望其能，士笑其不知止", 6.2, INK, ls=1.8)]
o += tail_(h, "能为是把事做成，知止是把事放下。", "图一百五十七", "冯妇搏虎", "ch246a")
save("ch246a-fengfu-bo-hu.svg", o)

# ---------------------------------------------------------- 158 性也有命焉
o = head_("性 也 有 命 焉", "《孟子》尽心下　第二百四十七章　MZ247", h)
o += [T(380, 108, "性也，有命焉，君子不谓性也", 5.4, ZONG, ls=1.0)]
o += [T(380, 124, "命也，有性焉，君子不谓命也", 5.4, ZONG, ls=1.0)]
o += [P("M 380,146 L 380,412", LINE, 1.0, "none", "6,4")]
for i, ch in enumerate(("味", "色", "声", "臭", "佚")):
    y = 176 + i * 46
    o += [R(250, y, 76, 32, ZONG, 1.1, SOFT), T(288, y + 21, ch, 9.0, INK, ls=2)]
    o += arrow(246, y + 16, 180, y + 16, GREY, 0.8, 3.6)
o += [T(146, 300, "命", 15.0, ZHE, ls=2)]
o += [T(146, 324, "有分限", 4.6, WARM, ls=0.5)]
for i, ch in enumerate(("仁", "义", "礼", "智", "圣")):
    y = 176 + i * 46
    o += [R(434, y, 76, 32, ZONG, 1.1, SOFT), T(472, y + 21, ch, 9.0, INK, ls=2)]
    o += arrow(514, y + 16, 580, y + 16, GREY, 0.8, 3.6)
o += [T(614, 300, "性", 15.0, ZHE, ls=2)]
o += [T(614, 324, "所禀有厚薄", 4.4, WARM, ls=0)]
o += [T(380, 424, "两头的箭都往回走", 6.2, INK, ls=2)]
o += tail_(h, "对欲说有命，不许放纵；对德说有性，不许推诿。", "图一百五十八", "性也有命焉", "ch247a")
save("ch247a-xing-ye-you-ming.svg", o)

# ---------------------------------------------------------- 159 善信美大圣神
o = head_("善 信 美 大 圣 神", "《孟子》尽心下　第二百四十八章　MZ248", h)
o += [T(380, 112, "可欲之谓善，有诸己之谓信，充实之谓美，充实而有光辉之谓大", 5.4, ZONG, ls=0.8)]
stair = ("M 230,404 L 230,366 L 250,366 L 250,328 L 270,328 L 270,290 L 290,290 "
         "L 290,252 L 310,252 L 310,214 L 330,214 L 330,176 L 430,176 L 430,214 "
         "L 450,214 L 450,252 L 470,252 L 470,290 L 490,290 L 490,328 L 510,328 "
         "L 510,366 L 530,366 L 530,404 L 230,404")
o += [P(stair, ZONG, 1.3, SOFT)]
for y, ch, x0, x1 in [(366, "善", 230, 530), (328, "信", 250, 510), (290, "美", 270, 490),
                      (252, "大", 290, 470), (214, "圣", 310, 450), (176, "神", 330, 430)]:
    o += [L(x0, y, x1, y, ZONG, 1.8), T(380, y + 26, ch, 10.0, INK, ls=4)]
o += [L(548, 252, 548, 366, ZHE, 1.0), L(544, 252, 552, 252, ZHE, 1.0),
      L(544, 366, 552, 366, ZHE, 1.0)]
o += [T(568, 386, "乐正子", 5.0, ZHE, "start", ls=1)]
o += [T(568, 400, "二之中·四之下", 4.4, WARM, "start", ls=0)]
o += arrow(196, 396, 196, 200, ZHE, 1.2, 5)
o += [T(182, 300, "上", 5.4, ZHE, "end", ls=1)]
o += [T(380, 424, "一级比一级窄——越高越难占", 6.2, INK, ls=1.8)]
o += tail_(h, "善是别人愿意要，信是自己真有；满了才是美。", "图一百五十九", "善信美大圣神", "ch248a")
save("ch248a-shan-xin-mei-da-sheng-shen.svg", o)

# ---------------------------------------------------------- 160 归斯受之
o = head_("归 斯 受 之", "《孟子》尽心下　第二百四十九章　MZ249", h)
o += [T(380, 112, "逃墨必归于杨，逃杨必归于儒。归，斯受之而已矣", 6.0, ZONG, ls=1.2)]
o += rail(452, 620, 404, 268, 7)
o += [L(452, 404, 620, 404, ZONG, 1.6), L(620, 272, 620, 404, ZONG, 1.6)]
o += tiger(534, 398, 22)
o += [T(536, 246, "既入其苙", 5.2, ZONG, ls=1.2)]
o += [stand(300, 404, 124)]
o += [P("M 360,324 C 420,338 500,362 542,382", ZONG, 1.0)]
o += [C(549, 384, 8, ZHE, 1.2)]
o += [T(424, 300, "招＝羁其足", 4.6, ZHE, ls=0)]
o += [T(300, 252, "栏外之人", 4.6, WARM, ls=1)]
o += [T(380, 424, "豚已进栏，绳还在手", 6.2, INK, ls=2)]
o += tail_(h, "距之严，待之恕；归了就收，收完就完。", "图一百六十", "归斯受之", "ch249a")
save("ch249a-gui-si-shou-zhi.svg", o)

# ---------------------------------------------------------- 161 用其一缓其二
o = head_("用 其 一 缓 其 二", "《孟子》尽心下　第二百五十章　MZ250", h)
o += [T(380, 112, "有布缕之征，粟米之征，力役之征。君子用其一，缓其二", 5.6, ZONG, ls=0.8)]
# 左：布匹（筒卷＋束带＋垂头）
o += [E(240, 304, 32, 9, ZONG, 1.1, SOFT)]
o += [P("M 208,304 L 208,384", ZONG, 1.1), P("M 272,304 L 272,384", ZONG, 1.1)]
o += [E(240, 384, 32, 9, ZONG, 1.1, SOFT)]
o += [L(206, 320, 274, 320, ZONG, 1.2), L(206, 348, 274, 348, ZONG, 1.2)]
o += [P("M 272,352 C 292,360 286,376 300,382 L 300,392 L 268,392 L 268,372", ZONG, 1.0, SOFT)]
o += [T(240, 370, "布", 5.4, ZONG, ls=1)]
# 中：粟袋（束口）
o += [P("M 342,296 L 378,296 L 400,384 L 320,384 Z", ZONG, 1.2, SOFT)]
o += [L(338, 296, 382, 296, ZONG, 1.8), L(341, 306, 379, 306, ZONG, 1.0)]
o += [P("M 334,310 L 348,300", ZONG, 1.0), P("M 386,310 L 372,300", ZONG, 1.0)]
o += [P("M 330,332 C 342,340 378,340 390,332", GREY, 0.6), P("M 326,356 C 340,364 380,364 394,356", GREY, 0.6)]
o += [T(360, 338, "粟", 5.6, ZONG, ls=1)]
# 右：挑夫与担
o += [C(530, 296, 8.2, INK, 1.0)]
o += [L(530, 304, 530, 350, INK, 1.2)]
o += [L(530, 350, 520, 386, INK, 1.1), L(530, 350, 540, 386, INK, 1.1)]
o += [L(474, 312, 586, 312, ZONG, 1.8)]
o += [L(530, 304, 530, 312, INK, 0.8)]
o += [L(530, 312, 516, 330, INK, 0.9), L(530, 312, 544, 330, INK, 0.9)]
o += [P("M 480,320 L 476,352", GREY, 0.7), P("M 578,320 L 582,352", GREY, 0.7)]
for cx in (476, 584):
    o += [P(f"M {cx-14},352 L {cx+14},{352} L {cx+10},{386} L {cx-10},{386} Z",
            ZONG, 1.1, SOFT)]
o += [L(462, 368, 490, 368, GREY, 0.7), L(570, 368, 598, 368, GREY, 0.7)]
o += [T(530, 400, "役", 4.8, ZONG, ls=1)]
# 取走之手（左侧布上）
o += grip(240, 296, 24, 1, ZHE, 1.2)
o += [T(292, 288, "取其一", 4.8, ZHE, ls=0.5)]
# 缓：压线
o += [L(316, 288, 412, 288, ZONG, 2.0), L(452, 288, 616, 288, ZONG, 2.0)]
o += [T(360, 278, "缓", 5.4, WARM, ls=2), T(536, 278, "缓", 5.4, WARM, ls=2)]
o += [T(240, 416, "一 · 活", 5.8, INK, ls=1), T(360, 416, "二 · 殍", 5.8, INK, ls=1),
      T(530, 416, "三 · 离", 5.8, INK, ls=1)]
o += tail_(h, "一活，二饿，三散；取到无度，国就危。", "图一百六十一", "用其一缓其二", "ch250a")
save("ch250a-yong-yi-huan-er.svg", o)

# ---------------------------------------------------------- 162 诸侯之宝
o = head_("诸 侯 之 宝", "《孟子》尽心下　第二百五十一章　MZ251", h)
o += [T(380, 112, "诸侯之宝三：土地，人民，政事。宝珠玉者，殃必及身", 5.6, ZONG, ls=1.0)]
for i, ch in enumerate(("土", "民", "政")):
    x = 150 + i * 160
    o += [R(x, 152, 140, 78, ZONG, 1.4, SOFT), T(x + 70, 200, ch, 16.0, INK, ls=3)]
o += [T(380, 250, "三 宝：所守·所养·所理", 5.0, ZONG, ls=2)]
o += [T(380, 292, "宝珠玉者，殃必及身", 5.4, ZHE, ls=1.4)]
# 珠玉一堆
o += [C(322, 320, 16, ZONG, 1.1, SOFT), C(356, 328, 13, ZONG, 1.1, SOFT),
      C(386, 318, 10, ZONG, 1.1, SOFT)]
o += [E(326, 358, 26, 12, ZONG, 1.0, SOFT), E(326, 358, 9, 5, GREY, 0.8),
      E(386, 356, 26, 12, ZONG, 1.0, SOFT), E(386, 356, 9, 5, GREY, 0.8)]
# 一个大赭叉压住整堆
for cx, cy, r in ((322, 320, 17), (384, 340, 15)):
    o += [L(cx - r, cy - r, cx + r, cy + r, ZHE, 1.6), L(cx + r, cy - r, cx - r, cy + r, ZHE, 1.6)]
o += [T(400, 390, "珠 玉", 4.8, WARM, ls=1)]
o += [T(380, 424, "能锁进库房的不是宝", 6.2, INK, ls=1.8)]
o += tail_(h, "宝得其宝者安，宝失其宝者危。", "图一百六十二", "诸侯之宝", "ch251a")
save("ch251a-zhuhou-zhi-bao.svg", o)

# ---------------------------------------------------------- 163 盆成括
o = head_("盆 成 括", "《孟子》尽心下　第二百五十二章　MZ252", h)
o += [T(380, 112, "其为人也小有才，未闻君子之大道也", 6.0, ZONG, ls=1.4)]
o += [stand(230, 404, 126, INK, 1.2)]
o += yan(256, 336, 46)
o += [T(238, 262, "小 有 才", 4.8, WARM, ls=1)]
# 大道（带路面）
o += [L(308, 404, 600, 250, ZONG, 1.6), L(436, 404, 656, 250, ZONG, 1.6)]
o += [L(308, 404, 436, 404, ZONG, 1.4)]
for i in range(5):
    t = 0.18 + i * 0.185
    o += [P(f"M {308 + t*292:.0f},{404 - t*154:.0f} L {436 + t*220:.0f},{404 - t*154:.0f}", GREY, 0.55)]
o += [P("M 372,404 L 628,250", GREY, 0.45, "none", "7,6")]
o += [C(644, 258, 4.2, ZHE, 1.0, ZHE)]
o += [T(560, 316, "君子之大道", 5.0, ZONG, ls=1.2)]
o += [T(668, 248, "赭", 4.4, ZHE, "start", ls=0)]
o += [T(380, 424, "才使他敢动，无道使他不知何时停", 6.2, INK, ls=1.6)]
o += tail_(h, "恃才妄作，所以取祸。", "图一百六十三", "盆成括", "ch252a")
save("ch252a-pen-cheng-kuo.svg", o)

# ---------------------------------------------------------- 164 馆于上宫
o = head_("馆 于 上 宫", "《孟子》尽心下　第二百五十三章　MZ253", h)
o += [T(380, 112, "有业屦于牖上，馆人求之弗得", 6.0, ZONG, ls=1.4)]
o += house(380, 404, 190, 112)
o += [R(300, 272, 62, 44, ZONG, 1.0, PALE)]
o += [L(300, 294, 362, 294, GREY, 0.7), L(331, 272, 331, 316, GREY, 0.7)]
o += [L(294, 320, 362, 320, ZONG, 1.8)]
o += shoe(302, 318, 30)
o += shoe(332, 318, 30)
o += [T(331, 266, "牖", 5.0, ZONG, ls=1)]
o += [T(331, 344, "业屦一双", 4.6, ZHE, ls=1)]
# 俯身寻者
o += [C(196, 320, 8.2, INK, 1.0)]
o += [P("M 197,328 L 212,362", INK, 1.2)]
o += [P("M 208,344 L 238,368", INK, 1.0)]
o += [P("M 212,362 L 202,404", INK, 1.1), P("M 212,362 L 228,404", INK, 1.1)]
o += [T(196, 424, "俯身寻", 4.6, WARM, ls=1)]
o += [stand(560, 404, 108, INK, 1.2)]
o += [T(560, 424, "负手立", 4.6, WARM, ls=1)]
o += [T(380, 424, "往者不追，来者不距", 5.6, INK, ls=2)]
o += tail_(h, "走的不追，来的不拒；以是心至，则受之。", "图一百六十四", "馆于上宫", "ch253a")
save("ch253a-guan-yu-shanggong.svg", o)
