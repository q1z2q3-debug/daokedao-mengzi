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


# ============================================================ 离娄下 90–99

def tail2(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 离娄下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


# ---------------------------------------------------------- 90 符节相合
h = 540
o = head_("符 节 相 合", "《孟子》离娄下　第九十章　MZ090", h)
o.append(T(380, 112, "舜生于诸冯　文王生于岐周", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 150,296 L 362,296 L 370,312 L 356,328 L 370,344 L 362,362 L 150,362 Z", ZONG, 1.3, fill=SOFT)]
o += [P("M 398,296 L 610,296 L 610,362 L 398,362 L 390,344 L 404,328 L 390,312 Z", ZONG, 1.3, fill=SOFT)]
for i in range(4):
    o += [L(180 + i * 44, 314, 180 + i * 44, 330, ZONG, 0.8)]
    o += [L(580 - i * 44, 314, 580 - i * 44, 330, ZONG, 0.8)]
o += [L(376, 306, 387, 306, GREY, 0.7, "4,3"), L(376, 352, 387, 352, GREY, 0.7, "4,3")]
o += arrow(352, 270, 378, 270, ZHE, 1.0, 4.0) + arrow(408, 270, 382, 270, ZHE, 1.0, 4.0)
o += [T(256, 286, "东夷之地", 6.4, ZONG, ls=2), T(504, 286, "西夷之地", 6.4, ZONG, ls=2)]
o += [T(380, 258, "若 合 符 节", 6.4, ZHE, ls=3)]
o += [L(150, 384, 610, 384, GREY, 0.7), L(150, 379, 150, 389, GREY, 0.7), L(610, 379, 610, 389, GREY, 0.7)]
o += [T(380, 398, "地之相去　千有余里", 5.8, GREY)]
o += [T(380, 424, "世相后而道相同：度之，则一", 6.2, GREY)]
o += tail2(h, "先圣后圣，其揆一也。", "图一", "符节相合", "ch90a")
save("ch90a-fu-jie.svg", o)

# ---------------------------------------------------------- 91 一车与两桥
h = 540
o = head_("一 车 与 两 桥", "《孟子》离娄下　第九十一章　MZ091", h)
o.append(T(380, 112, "子产以其乘舆济人于溱洧", 6.6, GREY, ls=1))
# 河
o += [P("M 96,336 C 150,326 190,346 240,336 C 290,326 330,346 380,336 C 430,326 470,346 520,336 C 570,326 610,346 664,336",
        WARM, 1.3), L(96, 384, 664, 384, WARM, 1.3), L(96, 330, 664, 330, WARM, 1.0)]
for i in range(3):
    y = 352 + i * 10
    o += [P(f"M 110,{y} C 160,{y-6} 200,{y+6} 250,{y} C 300,{y-6} 340,{y+6} 390,{y} C 440,{y-6} 480,{y+6} 530,{y} C 580,{y-6} 620,{y+6} 660,{y}",
            LINE, 0.8)]
# 车（在水中）
o += [C(176, 348, 19, INK, 1.3), C(176, 348, 3.4, INK, 1.0, fill=INK),
      C(222, 348, 19, INK, 1.3), C(222, 348, 3.4, INK, 1.0, fill=INK),
      R(160, 300, 78, 30, ZONG, 1.3, fill=SOFT),
      L(160, 312, 238, 312, ZONG, 0.8),
      L(238, 314, 268, 306, ZONG, 1.8)]
o += [C(186, 288, 7, INK, 1.1), L(186, 295, 186, 312, INK, 1.1),
      C(212, 288, 7, INK, 1.1), L(212, 295, 212, 312, INK, 1.1)]
o += [T(200, 276, "一 乘 之 舆", 6.2, ZONG, ls=2)]
# 徒杠（十一月，窄方桥，可通徒行）
o += [P("M 370,326 L 470,324 L 470,331 L 370,333 Z", ZONG, 1.2, fill=SOFT),
      L(376, 333, 376, 384, ZONG, 1.0), L(464, 331, 464, 384, ZONG, 1.0)]
# 舆梁（十二月，宽桥，可通车舆）
o += [P("M 512,314 L 656,310 L 656,320 L 512,324 Z", ZONG, 1.3, fill=SOFT),
      L(520, 320, 656, 316, ZONG, 0.8),
      P("M 512,324 C 542,344 626,340 656,320", LINE, 0.9),
      L(520, 324, 520, 384, ZONG, 1.1), L(648, 320, 648, 384, ZONG, 1.1)]
o += [T(420, 312, "徒杠 · 十一月", 5.8, ZONG, ls=1), T(584, 300, "舆梁 · 十二月", 5.8, ZONG, ls=1)]
o += [T(200, 402, "车所济者，一人一时", 5.5, GREY)]
o += [T(380, 424, "桥成，则民未病涉", 6.2, GREY)]
o += tail2(h, "惠而不知为政。", "图一", "一车与两桥", "ch91a")
save("ch91a-che-yu-liangqiao.svg", o)

# ---------------------------------------------------------- 92 手足腹心
h = 540
o = head_("手 足 · 腹 心", "《孟子》离娄下　第九十二章　MZ092", h)
o.append(T(380, 112, "君之视臣如手足，则臣视君如腹心", 6.6, GREY, ls=1))
o += [T(210, 132, "君 视 臣", 7.0, ZONG, ls=3), T(550, 132, "臣 视 君", 7.0, ZONG, ls=3)]
# 第一行：手足 → 腹心
y1 = 186
o += [P(f"M 196,{y1+16} C 188,{y1} 196,{y1-12} 210,{y1-12} C 224,{y1-12} 232,{y1} 224,{y1+16} Z", INK, 1.0, fill=PALE),
      L(200, y1 - 12, 200, y1 - 30, INK, 1.0), L(207, y1 - 12, 207, y1 - 34, INK, 1.0),
      L(214, y1 - 12, 214, y1 - 33, INK, 1.0), L(221, y1 - 12, 221, y1 - 28, INK, 1.0),
      L(197, y1 + 2, 183, y1 - 8, INK, 1.0)]
o += [P(f"M 550,{y1+8} C 532,{y1-6} 534,{y1-22} 550,{y1-14} C 566,{y1-22} 568,{y1-6} 550,{y1+8} Z", ZHE, 1.2, fill=SOFT)]
o += arrow(300, y1 - 6, 470, y1 - 6, GREY, 1.0, 4.0)
o += [T(210, y1 + 44, "手足", 6.6, ZONG, ls=2), T(550, y1 + 44, "腹心", 6.6, ZONG, ls=2)]
# 第二行：犬马 → 国人
y2 = 278
o += [E(214, y2 - 8, 22, 9, INK, 1.0, fill=PALE),
      C(190, y2 - 16, 7, INK, 1.0, fill=PALE), L(188, y2 - 22, 184, y2 - 32, INK, 0.9),
      L(202, y2 + 1, 202, y2 + 16, INK, 1.0), L(210, y2 + 2, 210, y2 + 16, INK, 1.0),
      L(220, y2 + 2, 220, y2 + 16, INK, 1.0), L(228, y2 + 1, 228, y2 + 16, INK, 1.0),
      P(f"M 234,{y2-10} C 246,{y2-12} 248,{y2-24} 240,{y2-28}", INK, 0.9)]
o += [C(526, y2 - 26, 5.6, GREY, 0.8), L(526, y2 - 20, 526, y2 + 4, GREY, 0.8),
      L(526, y2 + 4, 520, y2 + 16, GREY, 0.8), L(526, y2 + 4, 532, y2 + 16, GREY, 0.8),
      C(568, y2 - 26, 5.6, GREY, 0.8), L(568, y2 - 20, 568, y2 + 4, GREY, 0.8),
      L(568, y2 + 4, 562, y2 + 16, GREY, 0.8), L(568, y2 + 4, 574, y2 + 16, GREY, 0.8)]
o += [L(538, y2 - 8, 558, y2 - 8, LINE, 1.0, "3,3")]
o += arrow(300, y2 - 6, 470, y2 - 6, GREY, 1.0, 4.0)
o += [T(210, y2 + 44, "犬马", 6.6, ZONG, ls=2), T(550, y2 + 44, "国人", 6.6, ZONG, ls=2)]
# 第三行：土芥 → 寇雠（戈）
y3 = 366
o += [P(f"M 188,{y3} C 198,{y3-16} 224,{y3-16} 234,{y3} Z", ZONG, 1.1, fill=SOFT),
      L(200, y3 - 6, 196, y3 - 24, GREY, 0.9), L(208, y3 - 8, 210, y3 - 26, GREY, 0.9),
      L(218, y3 - 8, 224, y3 - 22, GREY, 0.9)]
o += [P(f"M 544,{y3-34} L 552,{y3-34} L 552,{y3-2} L 548,{y3+4} L 544,{y3-2} Z", INK, 1.2, fill=PALE),
      L(536, y3 - 2, 560, y3 - 2, INK, 1.0),
      L(548, y3 + 4, 548, y3 + 16, ZONG, 1.6), C(548, y3 + 18, 3.0, ZONG, 0.9)]
o += arrow(300, y3 - 6, 470, y3 - 6, GREY, 1.0, 4.0)
o += [T(210, y3 + 44, "土芥", 6.6, ZONG, ls=2), T(550, y3 + 44, "寇雠", 6.6, ZONG, ls=2)]
o += [T(380, 424, "施与报，对等；视之轻，报之亦轻", 6.2, GREY)]
o += tail2(h, "君之视臣如手足，则臣视君如腹心。", "图一", "手足·腹心", "ch92a")
save("ch92a-shouzu-fuxin.svg", o)

# ---------------------------------------------------------- 93 三有礼
h = 540
o = head_("三 有 礼", "《孟子》离娄下　第九十三章　MZ093", h)
o.append(T(380, 112, "礼，为旧君有服　何如斯可为服矣", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 城门（门额 + 半开门扇）
o += [L(128, 262, 128, 404, LINE, 2.2), L(204, 262, 204, 404, LINE, 2.2),
      L(114, 262, 218, 262, LINE, 2.2), L(150, 404, 150, 322, ZONG, 1.1),
      P("M 204,268 L 176,278 L 176,396 L 204,398 Z", ZONG, 1.0, fill=SOFT)]
o += [T(166, 250, "出 疆", 6.0, ZONG, ls=3)]
# 路
o += [L(212, 396, 560, 388, GREY, 0.8, "6,4"), L(212, 386, 560, 378, GREY, 0.8, "6,4")]
# ① 导之出疆：引路者
o += stand(330, 396, 78, INK, 1.0, arms="point")
o += [T(330, 300, "导之出疆", 5.8, ZHE, ls=1)]
# ② 先于其所往：持节者
o += [L(462, 396, 462, 280, ZONG, 1.5),
      P("M 462,282 L 492,290 L 492,302 L 462,294 Z", ZHE, 1.0, fill=SOFT),
      stand(484, 396, 62, INK, 1.0)]
o += [T(474, 244, "先于其所往", 5.8, ZHE, ls=1)]
# ③ 三年而后收其田里
o += [R(582, 368, 80, 28, ZONG, 0.9, fill=SOFT)]
for i in (1, 2):
    o += [L(582 + i * 27, 368, 582 + i * 27, 396, ZONG, 0.6)]
o += [T(656, 346, "三年而后收其田里", 5.4, ZHE, ls=1, anchor="end")]
o += [T(380, 424, "导之、先之、待之三年：三礼具，则为之服", 6.0, GREY)]
o += tail2(h, "此之谓三有礼焉。", "图一", "三有礼", "ch93a")
save("ch93a-san-youli.svg", o)

# ---------------------------------------------------------- 94 见几而行
h = 540
o = head_("见 几 而 行", "《孟子》离娄下　第九十四章　MZ094", h)
o.append(T(380, 112, "无罪而杀士，则大夫可以去", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 案与刀（刀横陈案上）
o += desk(110, 344, 230)
o += [R(120, 332, 26, 10, ZONG, 1.0, fill=SOFT),
      P("M 146,330 L 192,325 C 204,325 206,343 190,344 L 146,344 Z", INK, 1.2, fill=PALE),
      L(150, 337, 190, 334, GREY, 0.6)]
o += [T(158, 316, "案上之刑", 5.6, GREY)]
o += [slip(212, 318, 116, 26)]
# 门（半开）
o += [L(548, 244, 548, 404, LINE, 2.2), L(664, 244, 664, 404, LINE, 2.2), L(540, 244, 672, 244, LINE, 2.2)]
o += [P("M 556,252 L 620,266 L 620,398 L 556,390 Z", ZONG, 1.2, fill=SOFT), L(600, 268, 600, 396, GREY, 0.7)]
# 提囊而出的人
o += stand(438, 404, 92, INK, 1.2, arms="down")
o += [P("M 404,340 C 396,356 398,376 412,376 C 426,376 428,356 420,340 Z", ZONG, 1.1, fill=SOFT),
      P("M 406,340 C 410,328 416,328 420,340", ZONG, 1.0),
      L(414, 340, 436, 326, ZONG, 1.0)]
o += [L(418, 372, 430, 348, GREY, 0.8)]
o += [T(430, 424, "见几而作，未迫则能去", 6.0, GREY)]
o += tail2(h, "无罪而杀士，则大夫可以去。", "图一", "见几而行", "ch94a")
save("ch94a-jianji-erxing.svg", o)

# ---------------------------------------------------------- 95 一灯与众影
h = 540
o = head_("一 灯 与 众 影", "《孟子》离娄下　第九十五章　MZ095", h)
o.append(T(380, 112, "君仁莫不仁，君义莫不义", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 灯
o += [L(232, 404, 232, 302, ZONG, 1.6), E(232, 300, 32, 9, ZONG, 1.3, fill=SOFT),
      P("M 232,296 C 224,284 226,268 232,258 C 238,268 240,284 232,296 Z", ZHE, 1.2, fill=ZHE)]
o += [T(232, 240, "君 · 一身", 6.0, ZHE, ls=2)]
# 光：两道短斜线，落到人影
o += [L(258, 296, 392, 386, LINE, 0.8), L(258, 302, 640, 396, LINE, 0.8)]
for i, x in enumerate((420, 466, 512, 558, 604)):
    o += child(x, 404, 60, ZONG, 0.9)
    o += [L(x - 9, 404, x + 9, 404, WARM, 1.8), L(x + 6, 400, x + 26, 404, GREY, 0.7)]
o += [T(512, 330, "莫 不 仁　莫 不 义", 6.2, ZONG, ls=2)]
o += [T(380, 424, "灯不移，影自随；君之一身，众人之影", 6.0, GREY)]
o += tail2(h, "君仁莫不仁，君义莫不义。", "图一", "一灯与众影", "ch95a")
save("ch95a-yideng-zhongying.svg", o)

# ---------------------------------------------------------- 96 正印与反印
h = 540
o = head_("正 印 与 反 印", "《孟子》离娄下　第九十六章　MZ096", h)
o.append(T(380, 112, "非礼之礼，非义之义，大人弗为", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(226, 280, 52, 26, ZONG, 1.3, fill=SOFT),
      P("M 236,280 C 236,262 268,262 268,280", ZONG, 1.2, fill=SOFT)]
o += [R(486, 280, 52, 26, ZONG, 1.3, fill=SOFT),
      P("M 496,280 C 496,262 528,262 528,280", ZONG, 1.2, fill=SOFT)]
o += [L(252, 306, 252, 330, GREY, 0.7, "3,3"), L(512, 306, 512, 330, GREY, 0.7, "3,3")]
o += [R(196, 336, 150, 60, ZONG, 0.9, fill=PALE), R(214, 346, 114, 40, ZHE, 1.0, fill=SOFT)]
o += [T(271, 376, "礼", 17, ZHE, ls=2)]
o += [R(414, 336, 150, 60, ZONG, 0.9, fill=PALE), R(432, 346, 114, 40, ZHE, 1.0, fill=SOFT)]
o += [f'  <g transform="translate(489,376) scale(-1,1)"><text x="0" y="0" text-anchor="middle" '
      f'font-size="17" letter-spacing="2" fill="{ZHE}">礼</text></g>']
o += [T(271, 414, "正 印：合礼", 5.8, ZONG, ls=1), T(489, 414, "反 印：非礼之礼", 5.8, ZHE, ls=1)]
o += [T(380, 424, "形似而实非：章句合，理不合", 6.0, GREY)]
o += tail2(h, "非礼之礼，非义之义，大人弗为。", "图一", "正印与反印", "ch96a")
save("ch96a-zhengyin-fanyin.svg", o)

# ---------------------------------------------------------- 97 养与弃
h = 540
o = head_("养 与 弃", "《孟子》离娄下　第九十七章　MZ097", h)
o.append(T(380, 112, "中也养不中，才也养不才", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 叶（两端尖的杏仁形）
def leaf2(cx, cy, ang, sz=14, col=ZHE, fill=PALE):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    x1, y1 = cx - sz * ca, cy - sz * sa
    x2, y2 = cx + sz * ca, cy + sz * sa
    px, py = -sz * 0.42 * sa, sz * 0.42 * ca
    return P(f"M {x1:.1f},{y1:.1f} C {cx+px:.1f},{cy+py:.1f} {cx+px:.1f},{cy+py:.1f} {x2:.1f},{y2:.1f} "
             f"C {cx-px:.1f},{cy-py:.1f} {cx-px:.1f},{cy-py:.1f} {x1:.1f},{y1:.1f}", col, 1.1, fill=fill)

# 左：被养之苗（土墩 + 两支架 + 水滴）
o += [P("M 196,404 L 202,392 C 210,386 250,386 258,392 L 264,404 Z", ZONG, 1.1, fill=SOFT),
      L(230, 396, 230, 346, ZONG, 1.6),
      leaf2(216, 340, -26), leaf2(244, 338, 26)]
o += [L(230, 396, 230, 372, GREY, 0.6, "4,3")]
o += [P("M 198,318 C 194,328 198,336 202,334 C 206,332 204,324 198,318 Z", GREY, 0.8),
      P("M 216,300 C 212,310 216,318 220,316 C 224,314 222,306 216,300 Z", GREY, 0.8)]
o += [T(230, 424, "养：涵育熏陶，俟其自化", 5.8, GREY)]
# 右：被弃之苗（连根拔起，横陈于地）
o += [L(472, 398, 556, 392, ZONG, 1.5),
      leaf2(508, 384, 116), leaf2(534, 380, -104),
      L(472, 398, 456, 390, ZONG, 1.0), L(472, 398, 458, 404, ZONG, 1.0),
      L(478, 396, 466, 384, ZONG, 0.9)]
o += [T(520, 424, "弃：遽绝之而不教", 5.8, GREY)]
# 中：不足一寸
o += [L(296, 368, 424, 368, ZONG, 2.4), L(296, 362, 296, 374, ZONG, 1.0), L(424, 362, 424, 374, ZONG, 1.0),
      L(340, 362, 340, 374, ZONG, 0.9), L(384, 362, 384, 374, ZONG, 0.9)]
o += [T(360, 352, "不能以寸", 6.0, ZHE, ls=2)]
o += [T(380, 322, "贤与不肖，其间几何", 6.0, GREY)]
o += tail2(h, "中也养不中，才也养不才。", "图一", "养与弃", "ch97a")
save("ch97a-yang-yu-qi.svg", o)

# ---------------------------------------------------------- 98 不为与有为
h = 540
o = head_("不 为 与 有 为", "《孟子》离娄下　第九十八章　MZ098", h)
o.append(T(380, 112, "人有不为也，而后可以有为", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 两条路：左手一条走到栅栏止，右手一条伸向远处
o += [L(300, 402, 158, 402, WARM, 2.6), L(300, 394, 158, 394, GREY, 0.6)]
o += [L(300, 402, 656, 402, WARM, 1.2, "7,4"), L(300, 394, 656, 394, GREY, 0.6, "7,4")]
o += stand(300, 404, 76, INK, 1.1, arms="point")
# 左：栅栏封路（立在路端）
o += [L(140, 402, 140, 352, ZONG, 1.3), L(152, 402, 152, 348, ZONG, 1.3), L(164, 402, 164, 352, ZONG, 1.3),
      L(134, 384, 170, 384, ZONG, 1.2), L(134, 366, 170, 366, ZONG, 1.2)]
o += [T(152, 336, "不 为", 6.8, ZHE, ls=3)]
# 右：通向远处
o += [C(652, 398, 3.2, GREY, 0.8)]
o += [T(610, 378, "有 为", 6.8, ZONG, ls=3)]
o += [T(380, 424, "知所择，然后能有所为", 6.0, GREY)]
o += tail2(h, "人有不为也，而后可以有为。", "图一", "不为与有为", "ch98a")
save("ch98a-buwei-youwei.svg", o)

# ---------------------------------------------------------- 99 出口之箭
h = 540
o = head_("出 口 之 箭", "《孟子》离娄下　第九十九章　MZ099", h)
o.append(T(380, 112, "言人之不善，当如后患何", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 弓（弦已松，箭已出）
o += [P("M 174,232 C 246,260 246,340 174,368", ZONG, 2.2),
      L(174, 232, 174, 368, WARM, 1.0),
      L(174, 232, 168, 226, ZONG, 1.0), L(174, 368, 168, 374, ZONG, 1.0)]
o += [T(150, 390, "弓已松，箭已出", 5.6, GREY)]
# 箭（已离弦，向右远去）
o += [L(330, 300, 466, 300, INK, 1.6),
      P("M 476,300 L 458,291 L 458,309 Z", INK, 1.2, fill=SOFT)]
o += [L(196, 300, 616, 300, GREY, 0.7, "5,4")]
# 患
o += [C(646, 296, 30, GREY, 0.8)]
o += [T(646, 302, "患", 15, ZHE, ls=2)]
o += [T(292, 330, "追之不及", 5.6, GREY), L(316, 320, 332, 306, LINE, 0.7)]
o += [T(380, 424, "一言出口，便成后患之端", 6.0, GREY)]
o += tail2(h, "言人之不善，当如后患何？", "图一", "出口之箭", "ch99a")
save("ch99a-chukou-zhijian.svg", o)
