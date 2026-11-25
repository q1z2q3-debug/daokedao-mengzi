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
"""尽心上 图 178–187（v0.26.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail10(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 尽心上</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def ring(cx, cy, r, col=ZONG, sw=1.2, n=0):
    """同心环；n 为环上刻度数（0 则无）。"""
    o = [C(cx, cy, r, col, sw)]
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        o += [L(cx + r * math.cos(a), cy + r * math.sin(a),
                cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a), col, sw * 0.7)]
    return o


def crackwall(x, base, w=90, hh=120, col=WARM, sw=1.2):
    """危墙：墙面一道斜裂，顶部参差。"""
    o = [P(f"M {x},{base} L {x},{base-hh} L {x+18},{base-hh-8} L {x+36},{base-hh} "
           f"L {x+56},{base-hh-6} L {x+w},{base-hh} L {x+w},{base} Z", col, sw, fill=SOFT)]
    ys = base - 8
    o += [P(f"M {x+w*0.55},{base-hh+4} L {x+w*0.42},{base-hh*0.62} L {x+w*0.58},{base-hh*0.4} "
            f"L {x+w*0.46},{base-6}", ZHE, 1.0)]
    return o


def cangue(cx, cy, w=76, hh=26, col=WARM, sw=1.1):
    """桎梏：一板两孔。"""
    o = [R(cx - w / 2, cy - hh / 2, w, hh, col, sw, fill=SOFT),
         E(cx - 18, cy, 8, 9, col, sw * 0.9), E(cx + 18, cy, 8, 9, col, sw * 0.9)]
    return o


def gear(cx, cy, r=34, col=WARM, sw=1.1, teeth=8):
    """机变之巧：齿轮。"""
    o = [C(cx, cy, r, col, sw), C(cx, cy, r * 0.32, col, sw * 0.9)]
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
        x1, y1 = cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)
        o += [L(x0, y0, x1, y1, col, sw * 1.4)]
    return o


def mirror(cx, base, rx=40, ry=56, col=WARM, sw=1.2):
    """镜：椭圆镜面加短柄。"""
    o = [E(cx, base - ry - 12, rx, ry, col, sw, fill=PALE),
         L(cx, base - 12, cx, base - 2, col, sw * 1.1),
         P(f"M {cx-14},{base-2} q 14,4 28,0", col, sw * 1.1)]
    return o


def cape(cx, base, H=112, col=INK, sw=1.1):
    """布衣之士：宽袖，无冠。"""
    o = [C(cx, base - H + 9, 9, col, sw), L(cx, base - H + 18, cx, base - H * 0.24, col, sw * 1.2)]
    o += [P(f"M {cx},{base-H*0.72} L {cx-22},{base-H*0.5} L {cx-16},{base-H*0.16} L {cx},{base-H*0.2} "
            f"L {cx+16},{base-H*0.16} L {cx+22},{base-H*0.5} Z", col, sw, fill=PALE)]
    o += [L(cx, base - H * 0.24, cx - 9, base, col, sw), L(cx, base - H * 0.24, cx + 9, base, col, sw)]
    return o


h = 540

# ---------------------------------------------------------- 178 尽心知性
o = head_("尽 心 知 性", "《孟子》尽心上　第一百七十八章　MZ178", h)
o += [T(380, 112, "尽其心者，知其性也；知其性，则知天矣", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += ring(300, 292, 88, LINE, 0.9)
o += ring(300, 292, 62, ZONG, 1.1)
o += ring(300, 292, 34, ZONG, 1.3, 8)
o += [T(300, 297, "心", 9.4, INK, ls=2)]
o += [T(300, 218, "性", 7.2, ZONG, ls=2)]
o += [T(300, 192, "天", 7.2, GREY, ls=2)]
o += [arrow(300, 210, 300, 258, ZONG, 0.8, 3), arrow(300, 340, 300, 372, ZONG, 0.8, 3)]
o += [T(336, 344, "存 养", 5.2, ZONG)]
o += [T(336, 212, "知", 5.2, GREY)]
o += [L(520, 404, 520, 356, INK, 1.2)]
o += [L(520, 356, 540, 404, INK, 1.0)]
o += [T(520, 424, "立 命", 5.6, ZONG, ls=2)]
o += [L(586, 404, 586, 330, GREY, 1.0), L(612, 404, 612, 300, GREY, 1.0)]
o += [T(586, 424, "殀", 5.4, GREY), T(612, 424, "寿", 5.4, GREY)]
o += [P("M 570,300 L 628,300", LINE, 0.9), T(600, 294, "不贰", 5.0, GREY)]
o += tail10(h, "殀寿不贰，修身以俟之，所以立命也。", "图八十九", "尽心知性", "ch178a")
save("ch178a-jinxin-zhixing.svg", o)

# ---------------------------------------------------------- 179 正命
o = head_("正 命", "《孟子》尽心上　第一百七十九章　MZ179", h)
o += [T(380, 112, "莫非命也，顺受其正；知命者不立乎岩墙之下", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += crackwall(150, 404, 96, 128)
o += [T(198, 424, "岩 墙", 5.6, ZONG, ls=1)]
o += [stand(300, 404, 92, INK, 1.1)]
o += [P("M 272,320 L 204,300", LINE, 0.9, "none", "3,3")]
o += [T(240, 288, "不 立", 5.4, ZHE, ls=1)]
o += [L(400, 354, 560, 354, ZONG, 1.1), C(560, 354, 12, ZONG, 1.2), T(560, 358, "终", 7.0, INK)]
o += [T(480, 344, "尽 其 道", 5.2, ZONG)]
o += [stand(616, 404, 96, INK, 0.9)]
o += [cangue(616, 344, 66, 20)]
o += [T(616, 424, "桎 梏 者", 5.0, GREY, ls=0)]
o += [T(470, 210, "桎梏死者，非正命也", 5.2, ZHE)]
o += tail10(h, "尽其道而死者，正命也。", "图九十", "正命", "ch179a")
save("ch179a-zhengming.svg", o)

# ---------------------------------------------------------- 180 求在我
o = head_("求 在 我", "《孟子》尽心上　第一百八十章　MZ180", h)
o += [T(380, 112, "求则得之，舍则失之，是求有益于得也，求在我者也", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [C(300, 300, 92, ZONG, 1.3)]
for i, ch in enumerate(("仁", "义", "礼", "智")):
    x, y = 268 + (i % 2) * 64, 268 + (i // 2) * 56
    o += [T(x, y, ch, 8.6, INK, ls=1)]
o += [T(300, 424, "在 我 者", 5.8, ZONG, ls=2)]
o += [arrow(180, 300, 246, 300, ZONG, 0.9, 4)]
o += [T(212, 288, "求", 5.4, ZONG)]
o += [R(516, 258, 34, 26, WARM, 1.1, fill=SOFT), L(516, 258, 550, 258, WARM, 1.2)]
o += [T(533, 246, "冠", 5.4, GREY)]
o += [R(516, 320, 46, 22, WARM, 1.1, fill=PALE), T(539, 336, "币", 5.4, GREY)]
o += [P("M 440,300 L 500,300", GREY, 0.8, "none", "4,3")]
o += [T(470, 288, "求在外者", 5.0, GREY)]
o += [T(560, 296, "得之有命", 5.2, GREY)]
o += tail10(h, "求之有道，得之有命。", "图九十一", "求在我", "ch180a")
save("ch180a-qiu-zaiwo.svg", o)

# ---------------------------------------------------------- 181 万物皆备
o = head_("万 物 皆 备", "《孟子》尽心上　第一百八十一章　MZ181", h)
o += [T(380, 112, "万物皆备于我矣。反身而诚，乐莫大焉", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(340, 404, 120, INK, 1.3)]
o += [C(340, 330, 30, ZONG, 1.2)]
for i in range(9):
    a = 2 * math.pi * i / 9
    o += [C(340 + 17 * math.cos(a), 330 + 13 * math.sin(a), 2.4, ZONG, 0.7)]
o += [T(340, 424, "反身", 5.4, ZONG)]
o += mirror(196, 404, 34, 46)
o += [T(196, 424, "反身而诚", 5.0, GREY)]
o += [arrow(232, 330, 300, 330, ZONG, 0.9, 4)]
o += [stand(520, 404, 96, INK, 1.0)]
o += [P("M 384,320 q 40,-6 76,0", ZONG, 0.9)]
o += [arrow(392, 318, 470, 322, ZONG, 0.9, 4)]
o += [T(430, 300, "强 恕", 5.4, ZONG)]
o += [T(520, 424, "推己及人", 5.0, GREY)]
o += tail10(h, "强恕而行，求仁莫近焉。", "图九十二", "万物皆备", "ch181a")
save("ch181a-wanwu-jiebei.svg", o)

# ---------------------------------------------------------- 182 习而不察
o = head_("习 而 不 察", "《孟子》尽心上　第一百八十二章　MZ182", h)
o += [T(380, 112, "终身由之而不知其道者，众也", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [C(380, 296, 96, ZONG, 1.1), C(380, 296, 66, LINE, 0.8)]
for i, a in enumerate((0.6, 2.4, 4.2)):
    x, y = 380 + 96 * math.cos(a), 296 + 96 * math.sin(a)
    o += [P(f"M {x-6},{y} q 6,-5 12,0", ZONG, 0.9),
          P(f"M {x-6},{y+4} q 6,-5 12,0", ZONG, 0.9)]
o += [C(380, 296, 12, LINE, 0.8)]
o += [T(380, 424, "终身由之", 5.6, ZONG, ls=1)]
o += [stand(300, 386, 66, INK, 1.0)]
o += [T(268, 372, "行", 5.0, GREY)]
o += [T(300, 214, "习", 5.0, GREY)]
o += [P("M 380,296 L 380,370", LINE, 0.8, "none", "3,3")]
o += [T(380, 388, "不知其道", 5.2, ZHE)]
o += tail10(h, "行之而不著，习矣而不察。", "图九十三", "习而不察", "ch182a")
save("ch182a-xi-er-bucha.svg", o)

# ---------------------------------------------------------- 183 无耻之耻
o = head_("无 耻 之 耻", "《孟子》尽心上　第一百八十三章　MZ183", h)
o += [T(380, 112, "人不可以无耻。无耻之耻，无耻矣", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [C(246, 292, 46, WARM, 1.2)]
o += [L(230, 282, 236, 282, INK, 0.8), L(256, 282, 262, 282, INK, 0.8),
      L(236, 312, 256, 312, WARM, 0.9)]
o += [T(246, 424, "无 耻", 5.6, GREY, ls=1)]
o += [C(508, 292, 46, ZONG, 1.2)]
o += [L(492, 282, 498, 282, INK, 0.7), L(518, 282, 524, 282, INK, 0.7),
      P("M 496,314 q 6,-4 12,0 q 6,4 12,0", ZHE, 0.9)]
o += [P("M 470,270 L 486,296", ZHE, 0.8), P("M 486,262 L 500,290", ZHE, 0.8),
      P("M 502,258 L 516,288", ZHE, 0.8)]
o += [T(508, 424, "耻 其 无 耻", 5.4, ZHE, ls=1)]
o += [arrow(310, 292, 446, 292, ZONG, 1.0, 5)]
o += [T(378, 274, "反 而 耻 之", 5.2, GREY)]
o += tail10(h, "人能耻己之无所耻，则终身无复耻辱之累。", "图九十四", "无耻之耻", "ch183a")
save("ch183a-wuchi-zhichi.svg", o)

# ---------------------------------------------------------- 184 耻之大
o = head_("耻 之 大", "《孟子》尽心上　第一百八十四章　MZ184", h)
o += [T(380, 112, "为机变之巧者，无所用耻焉；不耻不若人，何若人有", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += gear(230, 300, 40, WARM, 1.1, 8)
o += [R(150, 352, 96, 12, WARM, 1.0, fill=SOFT)]
for k in range(7):
    o += [R(154 + k * 13, 340, 7, 12, WARM, 0.9, fill=SOFT)]
o += gear(300, 236, 26, WARM, 1.0, 8)
o += [stand(300, 404, 96, INK, 1.1)]
o += [T(300, 424, "自以为得计", 5.0, GREY)]
o += [P("M 352,300 L 372,296", LINE, 0.9, "none", "3,3")]
o += [T(368, 282, "无所用耻", 5.0, ZHE)]
o += [L(470, 404, 470, 300, INK, 1.0), C(470, 292, 7, INK, 1.0)]
o += [L(470, 320, 454, 356, INK, 0.9), L(470, 320, 486, 356, INK, 0.9)]
o += [L(560, 404, 560, 344, GREY, 0.9), C(560, 336, 6, GREY, 0.9)]
o += [L(560, 356, 548, 386, GREY, 0.8), L(560, 356, 572, 386, GREY, 0.8)]
o += [P("M 492,300 L 542,300", LINE, 0.9), T(516, 292, "不 如", 4.8, GREY)]
o += [T(520, 424, "不耻不若人", 5.0, ZONG)]
o += tail10(h, "耻之于人大矣：存之则进于圣贤，失之则入于禽兽。", "图九十五", "耻之大", "ch184a")
save("ch184a-chizhi-da.svg", o)

# ---------------------------------------------------------- 185 好善忘势
o = head_("好 善 忘 势", "《孟子》尽心上　第一百八十五章　MZ185", h)
o += [T(380, 112, "古之贤王好善而忘势，古之贤士乐其道而忘人之势", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [R(178, 372, 96, 10, WARM, 1.1, fill=SOFT)]
o += [L(192, 352, 268, 352, ZONG, 1.3)]
o += [P("M 210,352 q 20,-22 40,0", ZONG, 1.0)]
for k in range(3):
    o += [L(206 + k * 16, 352, 206 + k * 16, 366, ZONG, 0.8)]
o += [T(226, 424, "势 在 案 上", 5.0, GREY)]
o += [stand(340, 404, 116, INK, 1.2)]
o += [T(340, 424, "贤 王", 5.4, ZONG)]
o += [T(400, 250, "善", 10, ZHE, ls=1)]
o += [cape(470, 404, 112, INK, 1.1)]
o += [T(470, 424, "贤 士", 5.4, ZONG)]
o += [P("M 356,286 L 446,296", LINE, 0.9, "none", "3,3")]
o += [T(400, 306, "忘 势", 4.8, GREY)]
o += [R(566, 316, 58, 88, GREY, 1.0), L(566, 316, 624, 316, GREY, 1.1),
      L(624, 316, 624, 404, GREY, 1.0)]
o += [T(595, 424, "不 得 亟 见", 4.8, GREY)]
o += tail10(h, "王公不致敬尽礼，则不得亟见之。", "图九十六", "好善忘势", "ch185a")
save("ch185a-haoshan-wangshi.svg", o)

# ---------------------------------------------------------- 186 嚣嚣
o = head_("嚣 嚣", "《孟子》尽心上　第一百八十六章　MZ186", h)
o += [T(380, 112, "人知之，亦嚣嚣；人不知，亦嚣嚣", 6.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(380, 404, 120, INK, 1.3)]
o += [C(380, 330, 26, ZONG, 1.1)]
o += [T(380, 334, "德", 7.6, INK)]
o += [T(380, 424, "尊德乐义", 5.4, ZONG)]
for i in range(3):
    x = 214 + i * 34
    o += [C(x, 318, 5, WARM, 0.9), L(x, 323, x, 356, WARM, 0.9),
          L(x, 356, x - 6, 380, WARM, 0.8), L(x, 356, x + 6, 380, WARM, 0.8),
          L(x, 332, x - 8, 316, WARM, 0.8), L(x, 332, x + 8, 316, WARM, 0.8)]
o += [T(248, 296, "人 知 之", 5.2, GREY)]
o += [P("M 200,340 L 340,340", LINE, 0.9, "none", "4,3")]
o += [T(560, 300, "人不知", 5.4, GREY)]
o += [P("M 470,300 L 620,300", LINE, 0.9, "none", "3,3")]
o += [T(556, 336, "空 无 一 人", 5.0, GREY)]
o += [T(280, 180, "穷 则 独 善 其 身", 5.4, ZONG, ls=1)]
o += [T(500, 180, "达 则 兼 善 天 下", 5.4, ZONG, ls=1)]
o += tail10(h, "穷则独善其身，达则兼善天下。", "图九十七", "嚣嚣", "ch186a")
save("ch186a-xiaoxiao.svg", o)

# ---------------------------------------------------------- 187 豪杰
o = head_("豪 杰 之 士", "《孟子》尽心上　第一百八十七章　MZ187", h)
o += [T(380, 112, "待文王而后兴者，凡民也；豪杰之士，虽无文王犹兴", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [R(150, 316, 66, 88, WARM, 1.0), L(150, 316, 216, 316, WARM, 1.1)]
o += [T(183, 424, "文 王 未 至", 4.8, GREY)]
o += [C(183, 268, 16, LINE, 0.9), T(183, 272, "空", 5.6, GREY)]
o += [stand(330, 404, 76, WARM, 0.9)]
o += [T(330, 424, "凡 民 待 之", 5.0, GREY)]
o += [T(330, 268, "坐 而 待", 4.8, GREY)]
o += [P("M 470,404 L 500,376 L 540,376 L 540,404 Z", ZONG, 1.2, fill=SOFT)]
o += [stand(520, 376, 104, INK, 1.2)]
o += [T(520, 424, "豪 杰 自 兴", 5.2, ZHE)]
o += [arrow(500, 330, 520, 300, ZONG, 0.9, 4)]
o += [T(566, 262, "虽 无 文 王", 5.4, ZHE)]
o += tail10(h, "若夫豪杰之士，虽无文王犹兴。", "图九十八", "豪杰", "ch187a")
save("ch187a-haojie.svg", o)
