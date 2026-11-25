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
"""离娄下 图 100–109（v0.17.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
坑：C() 第五位是 fill，画空心圈写 C(x,y,r,INK,0.8)；P() 第五位才是 dash。
"""

def tail2(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 离娄下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


# ---------------------------------------------------------- 100 不为已甚
h = 540
o = head_("不 为 已 甚", "《孟子》离娄下　第一百章　MZ100", h)
o.append(T(380, 112, "圣人所为，本分之外，不加毫末", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(190, 316, 400, 26, WARM, 1.4, fill=SOFT)]
for i in range(11):
    x = 190 + i * 40
    o += [L(x, 316, x, 326 if i % 5 else 334, ZONG, 0.9)]
o += [L(550, 300, 550, 358, ZHE, 1.4)]
o += [T(550, 292, "本分", 6.2, ZHE, ls=2)]
o += [T(590, 330, "外", 5.4, GREY), T(590, 344, "不", 5.4, GREY), T(590, 358, "加", 5.4, GREY)]
o += [T(370, 306, "十寸之尺　取九寸", 5.8, GREY, ls=1)]
o += [T(380, 424, "满而不溢，平而不尖", 6.2, GREY)]
o += tail2(h, "仲尼不为已甚者。", "图十一", "不为已甚", "ch100a")
save("ch100a-buwei-yishen.svg", o)

# ---------------------------------------------------------- 101 惟义所在
h = 540
o = head_("惟 义 所 在", "《孟子》离娄下　第一百零一章　MZ101", h)
o.append(T(380, 112, "言不必信　行不必果", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [L(160, 300, 600, 300, ZONG, 1.8)]
for i in range(9):
    x = 200 + i * 40
    o += [L(x, 300, x, 307, ZONG, 0.7)]
o += [L(380, 300, 380, 244, ZONG, 1.4), C(380, 240, 4.0, ZONG, 1.0)]
o += [T(380, 232, "提纽", 5.4, ZONG)]
o += [L(160, 300, 160, 318, ZONG, 1.0), R(136, 318, 48, 34, ZONG, 1.2, fill=SOFT), T(160, 342, "信", 8.4, INK)]
o += [L(600, 300, 600, 318, ZONG, 1.0), R(576, 318, 48, 34, ZONG, 1.2, fill=SOFT), T(600, 342, "果", 8.4, INK)]
o += [T(380, 322, "义", 8.0, ZHE)]
o += [T(380, 424, "主于义，则信果在其中", 6.2, GREY)]
o += tail2(h, "言不必信，行不必果，惟义所在。", "图十二", "惟义所在", "ch101a")
save("ch101a-wei-yi-suoza.svg", o)

# ---------------------------------------------------------- 102 赤子之心
h = 540
o = head_("赤 子 之 心", "《孟子》离娄下　第一百零二章　MZ102", h)
o.append(T(380, 112, "大人者，不失其赤子之心者也", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [C(216, 332, 56, ZONG, 1.3), C(216, 332, 24, ZONG, 1.3)]
o += [C(544, 332, 56, ZONG, 1.3), C(544, 332, 24, ZONG, 1.3)]
for i in range(16):
    a = i * 22.5
    x1 = 544 + 26 * math.cos(math.radians(a)); y1 = 332 + 26 * math.sin(math.radians(a))
    x2 = 544 + 52 * math.cos(math.radians(a)); y2 = 332 + 52 * math.sin(math.radians(a))
    o += [L(round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1), GREY, 0.7)]
o += arrow(292, 332, 466, 332, ZHE, 1.0, 4.5)
o += [T(216, 262, "赤子之心", 6.4, ZONG, ls=2), T(216, 274, "纯一无伪", 5.6, GREY)]
o += [T(544, 262, "大人之心", 6.4, ZONG, ls=2), T(544, 274, "通达万变", 5.6, GREY)]
o += [T(380, 322, "扩而充之", 6.0, ZHE, ls=2)]
o += [T(380, 424, "不为物诱，全其本然", 6.2, GREY)]
o += tail2(h, "大人者，不失其赤子之心者也。", "图十三", "赤子之心", "ch102a")
save("ch102a-chizi-zhixin.svg", o)

# ---------------------------------------------------------- 103 送死大事
h = 540
o = head_("送 死 大 事", "《孟子》离娄下　第一百零三章　MZ103", h)
o.append(T(380, 112, "养生者不足以当大事，惟送死可以当大事", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += desk(120, 348, 210)
o += bowl(214, 336, 34, 11)
o += [L(252, 316, 268, 336, WARM, 1.0), L(258, 312, 274, 334, WARM, 1.0)]
o += [T(214, 300, "事生", 6.2, ZONG, ls=2), T(214, 386, "人道之常", 5.6, GREY)]
o += [P("M 440,404 C 470,346 560,346 590,404 Z", ZONG, 1.3, fill=SOFT)]
o += [R(506, 330, 20, 46, ZONG, 1.0, fill=PALE)]
o += [L(510, 344, 522, 344, GREY, 0.6), L(510, 356, 522, 356, GREY, 0.6)]
o += [T(516, 320, "送死", 6.2, ZONG, ls=2), T(516, 388, "人道之大变", 5.6, GREY)]
o += [L(380, 240, 380, 398, GREY, 0.7, "5,4")]
o += [T(380, 232, "大事", 7.0, ZHE, ls=3)]
o += [T(380, 424, "必诚必信，不使少有后日之悔", 6.2, GREY)]
o += tail2(h, "惟送死可以当大事。", "图十四", "送死大事", "ch103a")
save("ch103a-songsi-dashi.svg", o)

# ---------------------------------------------------------- 104 深造自得
h = 540
o = head_("深 造 自 得", "《孟子》离娄下　第一百零四章　MZ104", h)
o.append(T(380, 112, "深造之以道，欲其自得之也", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 244,332 L 352,332 L 372,352 L 224,352 Z", ZONG, 1.4, fill=SOFT)]
o += [P("M 256,336 L 340,336 L 354,348 L 242,348 Z", GREY, 0.9)]
o += [L(300, 336, 300, 348, GREY, 0.9), L(250, 340, 352, 340, GREY, 0.9)]
o += [L(224, 352, 228, 400, ZONG, 1.1), L(372, 352, 368, 400, ZONG, 1.1)]
o += [L(228, 392, 368, 392, ZONG, 1.0), P("M 236,386 C 258,380 282,392 304,384 C 326,378 350,390 362,386", WARM, 0.8)]
o += [L(300, 336, 300, 244, ZONG, 1.0), R(286, 224, 28, 22, ZONG, 1.0, fill=PALE)]
o += [P("M 286,226 C 292,214 308,214 314,226", ZONG, 0.9)]
o += [T(256, 322, "深造", 5.8, ZONG), T(300, 208, "汲", 5.4, GREY)]
o += arrow(250, 372, 198, 392, ZHE, 0.9, 4.0) + arrow(352, 372, 404, 392, ZHE, 0.9, 4.0)
o += [bowl(180, 392, 24, 9), bowl(422, 392, 24, 9)]
o += [T(380, 302, "取之左右逢其原", 6.0, ZHE, ls=1)]
o += [T(380, 424, "水在井底，须自汲；其原，则在己", 6.2, GREY)]
o += tail2(h, "故君子欲其自得之也。", "图十五", "深造自得", "ch104a")
save("ch104a-shenzao-zide.svg", o)

# ---------------------------------------------------------- 105 博学详说
h = 540
o = head_("博 学 详 说", "《孟子》离娄下　第一百零五章　MZ105", h)
o.append(T(380, 112, "博学而详说之，将以反说约也", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
for _x, _sy in ((120, 316), (146, 350), (120, 384)):
    o += [slip(_x, _sy, 116, 26)]
    for _i in range(7):
        o += [L(_x + 10 + _i * 15, _sy + 3, _x + 10 + _i * 15, _sy + 23, GREY, 0.5)]
o += [T(178, 300, "博学", 6.0, ZONG, ls=2), T(178, 372, "详说", 5.6, GREY)]
o += arrow(272, 350, 336, 350, ZHE, 1.1, 4.5)
o += [R(360, 292, 36, 96, ZONG, 1.4, fill=SOFT)]
o += [L(360, 316, 396, 316, ZHE, 1.0), L(360, 360, 396, 360, ZHE, 1.0)]
o += [E(378, 292, 18, 4, ZONG, 0.9), E(378, 388, 18, 4, ZONG, 0.9)]
o += [T(404, 286, "反说约", 6.2, ZHE, ls=2)]
o += [T(420, 336, "融会贯通", 5.6, GREY, anchor="start")]
o += [T(380, 424, "学非徒博，亦不可以径约", 6.2, GREY)]
o += tail2(h, "将以反说约也。", "图十六", "博学详说", "ch105a")
save("ch105a-boxue-xiangshuo.svg", o)

# ---------------------------------------------------------- 106 以善养人
h = 540
o = head_("以 善 养 人", "《孟子》离娄下　第一百零六章　MZ106", h)
o.append(T(380, 112, "以善服人者，未有能服人者也", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [stand(210, 404, 100, INK, 1.2, "point")]
o += [L(246, 300, 246, 226, ZONG, 1.4), R(236, 210, 36, 26, ZONG, 1.0, fill=SOFT), T(254, 228, "善", 7.4, INK)]
o += [L(190, 308, 214, 296, INK, 0.9)]
o += [T(210, 424 - 8 if False else 396, "", 5)]
o += [T(196, 194, "以善服人", 6.2, ZONG, ls=1), T(196, 208, "欲以取胜", 5.4, GREY)]
o += [stand(520, 404, 100, INK, 1.2)]
o += [bowl(556, 340, 30, 10), L(530, 330, 556, 340, INK, 1.0), L(546, 330, 566, 338, INK, 1.0)]
o += [T(560, 194, "以善养人", 6.2, ZONG, ls=1), T(560, 208, "同归于善", 5.4, GREY)]
o += [L(300, 260, 300, 396, GREY, 0.7, "5,4"), L(460, 260, 460, 396, GREY, 0.7, "5,4")]
o += [T(380, 356, "心之公私", 5.8, GREY, ls=1), T(380, 372, "向背顿殊", 5.8, GREY, ls=1)]
o += [T(380, 424, "天下不心服而王者，未之有也", 6.2, GREY)]
o += tail2(h, "以善养人，然后能服天下。", "图十七", "以善养人", "ch106a")
save("ch106a-yishan-yangren.svg", o)

# ---------------------------------------------------------- 107 蔽贤之实
h = 540
o = head_("蔽 贤 之 实", "《孟子》离娄下　第一百零七章　MZ107", h)
o.append(T(380, 112, "言无实不祥　不祥之实，蔽贤者当之", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [L(600, 404, 600, 316, ZONG, 1.4), E(600, 316, 24, 8, ZONG, 1.0)]
o += [P("M 600,310 C 592,298 594,282 600,272 C 606,282 608,298 600,310 Z", ZHE, 1.1)]
o += [L(624, 312, 656, 348, ZHE, 0.8, "4,3")]
o += [stand(462, 404, 96, INK, 1.2, "point")]
o += [P("M 480,282 L 516,274 L 516,352 L 480,344 Z", ZONG, 1.2, fill=SOFT)]
o += [T(508, 258, "蔽", 7.4, ZONG, ls=3)]
o += [L(538, 330, 528, 336, GREY, 0.7)]
o += [T(380, 424, "贤者之光，为一人所遮", 6.2, GREY)]
o += tail2(h, "不祥之实，蔽贤者当之。", "图十八", "蔽贤之实", "ch107a")
save("ch107a-bixian-zhishi.svg", o)

# ---------------------------------------------------------- 108 盈科后进
h = 540
o = head_("盈 科 后 进", "《孟子》离娄下　第一百零八章　MZ108", h)
o.append(T(380, 112, "原泉混混，不舍昼夜，盈科而后进", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [C(168, 372, 14, ZONG, 1.2), P("M 158,386 C 150,394 168,398 180,392", WARM, 0.8)]
for i in range(3):
    o += [P(f"M {148+i*8},{356-i*6} C {156+i*8},{348-i*6} {170+i*8},{364-i*6} {180+i*8},{356-i*6}", GREY, 0.8)]
o += [T(168, 340, "原泉", 6.0, ZONG, ls=2)]
o += [L(182, 372, 300, 372, ZONG, 1.3)]
o += [P("M 300,372 L 336,372 L 336,398 L 384,398 L 384,372 L 420,372", ZONG, 1.3)]
o += [L(338, 372, 382, 372, ZONG, 1.2)]
o += [P("M 344,382 C 356,386 370,382 380,386", WARM, 0.7)]
o += [T(360, 344, "科（坎）", 5.6, GREY)]
o += [T(360, 390, "盈而后进", 5.4, ZHE)]
o += [L(420, 372, 470, 372, ZONG, 1.3)]
o += [L(470, 380, 470, 400, ZONG, 1.0), L(486, 386, 486, 404, ZONG, 1.0)]
o += [P("M 470,382 C 492,374 530,390 556,382 C 582,374 618,390 648,380", ZONG, 1.4)]
o += [P("M 470,392 C 498,386 536,398 562,392 C 592,386 622,398 652,392", WARM, 0.9)]
o += [T(566, 366, "放乎四海", 6.0, ZONG, ls=2)]
o += [T(380, 424, "有本者如是　无本者，其涸可立待", 6.2, GREY)]
o += tail2(h, "有本者如是，是之取尔。", "图十九", "盈科后进", "ch108a")
save("ch108a-yingke-houjin.svg", o)

# ---------------------------------------------------------- 109 人禽几希
h = 540
o = head_("人 禽 几 希", "《孟子》离娄下　第一百零九章　MZ109", h)
o.append(T(380, 112, "人之所以异于禽兽者几希", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [L(380, 224, 380, 404, ZHE, 0.7)]
o += [T(380, 216, "几希", 6.4, ZHE, ls=3)]
o += [E(286, 368, 34, 17, ZONG, 1.2)]
o += [C(252, 352, 9, ZONG, 1.0), L(246, 344, 240, 336, ZONG, 0.9)]
o += [L(270, 385, 270, 402, ZONG, 1.0), L(290, 386, 290, 402, ZONG, 1.0),
      L(306, 385, 306, 402, ZONG, 1.0), L(318, 383, 320, 400, ZONG, 1.0)]
o += [P("M 320,360 C 340,352 348,342 344,332", ZONG, 1.0)]
o += [T(286, 424 - 6 if False else 396, "", 5)]
o += [T(286, 342 - 24, "禽兽", 6.2, ZONG, ls=2)]
o += [stand(474, 404, 96, INK, 1.2)]
o += [T(474, 290, "人", 7.0, INK, ls=4)]
o += arrow(356, 244, 306, 236, GREY, 0.9, 3.5) + [T(322, 222, "庶民去之", 5.6, GREY)]
o += arrow(404, 236, 454, 244, ZHE, 0.9, 3.5) + [T(438, 222, "君子存之", 5.6, ZHE)]
o += [T(380, 424, "存之者君子，存者圣人", 6.2, GREY)]
o += tail2(h, "人之所以异于禽兽者几希。", "图二十", "人禽几希", "ch109a")
save("ch109a-renqin-jixi.svg", o)
