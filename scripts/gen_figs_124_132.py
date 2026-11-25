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
"""万章上 图 124–132（v0.20.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail5(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 万章上</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def kneel(cx, base, H=74, col=INK, sw=1.0):
    hr = 5.0
    top = base - H
    return [C(cx, top + hr, hr, col, sw),
            L(cx, top + hr * 2, cx, base - H * 0.34, col, sw),
            L(cx, base - H * 0.34, cx - 14, base, col, sw),
            L(cx, base - H * 0.34, cx + 14, base, col, sw),
            L(cx, top + hr * 2 + 6, cx - 12, base - H * 0.5, col, sw * 0.9),
            L(cx, top + hr * 2 + 6, cx + 12, base - H * 0.5, col, sw * 0.9)]


def city(x, y, w=120, hh=76, col=WARM, sw=1.1):
    """城：城墙、垛口、一门。"""
    o = [R(x, y, w, hh, col, sw, fill=PALE)]
    for i in range(4):
        o += [R(x + 6 + i * 30, y - 9, 14, 10, col, sw * 0.9, fill=PALE)]
    o += [R(x + w / 2 - 14, y + hh - 34, 28, 34, col, sw * 0.9, fill=SOFT)]
    return o


def sheep(x, y, w=90, hh=34, col=ZONG, sw=1.0):
    """羊皮：四角略起的一张皮。"""
    o = [P(f"M {x},{y+4} C {x+8},{y-4} {x+w-8},{y-4} {x+w},{y+4} "
           f"L {x+w-6},{y+hh} L {x+6},{y+hh} Z", col, sw, fill=SOFT)]
    o += [L(x + 14, y + 8, x + 14, y + hh - 6, GREY, 0.5),
          L(x + w - 14, y + 8, x + w - 14, y + hh - 6, GREY, 0.5)]
    return o


def ding(cx, base, w=76, hh=54, col=ZONG, sw=1.2):
    """鼎：三足、双耳、鼓腹。"""
    return [E(cx, base - hh, w / 2, 9, col, sw, fill=SOFT),
            P(f"M {cx-w/2},{base-hh+6} C {cx-w/2-8},{base-hh*0.62} {cx+w/2+8},{base-hh*0.62} {cx+w/2},{base-hh+6}",
              col, sw, fill=SOFT),
            L(cx - w / 2 + 8, base - hh + 10, cx - w / 2 + 4, base - 4, col, sw * 0.9),
            L(cx, base - hh + 12, cx, base, col, sw * 0.9),
            L(cx + w / 2 - 8, base - hh + 10, cx + w / 2 - 4, base - 4, col, sw * 0.9),
            P(f"M {cx-18},{base-hh+2} C {cx-14},{base-hh-10} {cx-8},{base-hh-12} {cx-4},{base-hh-2}", col, sw * 0.8),
            P(f"M {cx+18},{base-hh+2} C {cx+14},{base-hh-10} {cx+8},{base-hh-12} {cx+4},{base-hh-2}", col, sw * 0.8)]


# ---------------------------------------------------------- 124 号泣旻天
h = 540
o = head_("号 泣 旻 天", "《孟子》万章上　第一百二十四章　MZ124", h)
o.append(T(380, 112, "舜往于田，号泣于旻天　何为其号泣也", 6.4, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
for i in range(4):
    o += [L(110, 344 + i * 16, 300, 344 + i * 16, LINE, 0.8)]
o += [T(205, 332, "历山　　畎亩", 5.6, ZONG, ls=1)]
o += kneel(300, 404, 78, INK, 1.1)
o += [L(296, 337, 296, 360, ZHE, 0.8), L(306, 337, 306, 356, ZHE, 0.8)]
o += [P("M 200,268 C 262,196 498,196 560,268", GREY, 1.1)]
o += [T(380, 216, "旻天", 7.0, ZONG, ls=6)]
o += [T(380, 232, "仁覆闵下", 5.2, GREY, ls=2)]
o += [T(380, 424, "惟顺于父母，可以解忧　五十而慕", 6.0, GREY)]
o += tail5(h, "怨慕也。", "图三十五", "号泣旻天", "ch124a")
save("ch124a-haogi-mintian.svg", o)


# ---------------------------------------------------------- 125 不告而娶
h = 540
o = head_("不 告 而 娶", "《孟子》万章上　第一百二十五章　MZ125", h)
o.append(T(380, 112, "娶妻如之何？必告父母　舜之不告而娶，何也", 6.2, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(440, 300, 150, 92, WARM, 1.2, fill=PALE)]
o += [L(432, 292, 440, 300, WARM, 1.0), L(590, 292, 598, 300, WARM, 1.0), L(424, 290, 604, 290, WARM, 1.2)]
o += [R(470, 316, 60, 76, WARM, 0.9, fill=SOFT)]
o += [T(515, 284, "父母之门", 5.8, ZONG)]
o += kneel(300, 404, 76, INK, 1.1)
o += [L(318, 350, 344, 336, INK, 0.9), C(347, 334, 4.0, ZONG, 0.8)]
o += [T(300, 292, "舜", 5.6, ZONG)]
o += [P("M 340,372 C 392,372 396,318 452,318", ZHE, 1.1, "none", "5,3")]
o += [T(384, 386, "不告", 5.8, ZHE)]
o += [T(380, 424, "告则废人之大伦，以怼父母，是以不告也", 5.8, GREY)]
o += tail5(h, "是以不告也。", "图三十六", "不告而娶", "ch125a")
save("ch125a-bugao-erqu.svg", o)


# ---------------------------------------------------------- 126 封之有庳
h = 540
o = head_("封 之 有 庳", "《孟子》万章上　第一百二十六章　MZ126", h)
o.append(T(380, 112, "四罪而天下咸服　象至不仁，封之有庳", 6.4, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
for i, nm in enumerate(["共工", "驩兜", "三苗", "鲧"]):
    x = 104 + i * 56
    o += [R(x, 352, 40, 40, GREY, 0.9, fill=PALE)]
    o += [L(x + 6, 358, x + 34, 384, ZHE, 1.0), L(x + 34, 358, x + 6, 384, ZHE, 1.0)]
    o += [T(x + 20, 342, nm, 5.0, GREY)]
o += [T(190, 288, "四罪：在他人则诛", 5.6, ZONG, ls=1)]
o += city(408, 306, 150, 96, WARM, 1.2)
o += kneel(455, 404, 60, INK, 1.0)
o += [T(455, 298, "象", 5.4, ZHE)]
o += [stand(560, 404, 68, ZONG, 1.0)]
o += [T(586, 320, "使吏治其国", 5.4, ZONG)]
o += [T(380, 424, "不藏怒，不宿怨，亲爱之而已矣", 5.8, GREY)]
o += tail5(h, "封之有庳，富贵之也。", "图三十七", "封之有庳", "ch126a")
save("ch126a-fengzhi-youbi.svg", o)


# ---------------------------------------------------------- 127 以意逆志
h = 540
o = head_("以 意 逆 志", "《孟子》万章上　第一百二十七章　MZ127", h)
o.append(T(380, 112, "不以文害辞，不以辞害志　以意逆志，是为得之", 6.0, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(150, 254, 110, 130, WARM, 1.1, fill=PALE),
      L(150, 282, 260, 282, ZONG, 0.7), L(150, 340, 260, 340, ZONG, 0.7)]
for i in range(5):
    o += [L(162 + i * 22, 262, 162 + i * 22, 390, GREY, 0.5)]
o += [T(205, 244, "诗", 6.4, ZONG, ls=2)]
o += [L(292, 300, 470, 300, GREY, 0.8), T(292, 292, "文", 5.2, GREY, anchor="start")]
o += [L(292, 340, 520, 340, GREY, 0.8), T(292, 332, "辞", 5.2, GREY, anchor="start")]
o += [L(292, 380, 566, 380, GREY, 0.8), T(292, 372, "志", 5.2, GREY, anchor="start")]
o += [P("M 322,254 C 400,214 520,244 592,290", ZHE, 1.3)]
o += [P("M 592,290 L 580,278 L 596,272 Z", ZHE, 1.0, fill=PALE)]
o += [T(430, 236, "以意逆之", 6.0, ZHE, ls=2)]
o += [T(380, 424, "以己意迎取作者之志，乃可得之", 5.8, GREY)]
o += tail5(h, "以意逆志，是为得之。", "图三十八", "以意逆志", "ch127a")
save("ch127a-yiyi-nizhi.svg", o)


# ---------------------------------------------------------- 128 天与之
h = 540
o = head_("天 与 之", "《孟子》万章上　第一百二十八章　MZ128", h)
o.append(T(380, 112, "天子不能以天下与人　天与之", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 180,246 C 262,170 498,170 580,246", GREY, 1.2)]
o += [T(380, 196, "天", 8.0, ZONG, ls=8)]
o += [P("M 380,250 L 380,392", LINE, 0.9, "none", "4,4")]
o += [T(380, 322, "行与事", 5.8, ZHE, ls=1)]
for i in range(3):
    o += [stand(300 + i * 80, 404, 66, INK, 1.0)]
o += [T(380, 344, "民", 5.8, ZONG, ls=2)]
o += [T(380, 424, "天视自我民视，天听自我民听", 6.0, GREY)]
o += tail5(h, "天与之。", "图三十九", "天与之", "ch128a")
save("ch128a-tian-yuzhi.svg", o)


# ---------------------------------------------------------- 129 天与贤
h = 540
o = head_("天 与 贤", "《孟子》万章上　第一百二十九章　MZ129", h)
o.append(T(380, 112, "天与贤，则与贤；天与子，则与子", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [L(200, 276, 560, 276, ZONG, 1.4), L(380, 276, 380, 258, ZONG, 1.2)]
o += [C(380, 252, 6, ZONG, 1.0)]
o += [L(214, 276, 214, 316, GREY, 0.9), L(546, 276, 546, 316, GREY, 0.9)]
o += [E(214, 322, 34, 7, ZONG, 1.1, fill=SOFT)]
o += [E(546, 322, 34, 7, ZONG, 1.1, fill=SOFT)]
o += [T(214, 240, "贤", 7.0, INK, ls=2), T(546, 240, "子", 7.0, INK, ls=2)]
o += [T(214, 348, "舜禹益", 5.2, GREY), T(546, 348, "启太甲成王", 5.2, GREY)]
o += [T(380, 424, "莫之为而为者，天也；莫之致而至者，命也", 5.8, GREY)]
o += tail5(h, "其义一也。", "图四十", "天与贤", "ch129a")
save("ch129a-tian-yuxian.svg", o)


# ---------------------------------------------------------- 130 割烹要汤
h = 540
o = head_("割 烹 要 汤", "《孟子》万章上　第一百三十章　MZ130", h)
o.append(T(380, 112, "伊尹以割烹要汤　有诸", 6.4, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += ding(200, 404, 80, 56)
o += [P("M 200,332 C 214,318 226,320 232,332", GREY, 0.7)]
o += [T(200, 288, "鼎", 6.2, ZONG, ls=3)]
o += [T(200, 424, "割烹：传说所诬", 5.4, GREY)]
o += kneel(330, 404, 74, INK, 1.1)
o += [P("M 330,292 L 366,276", ZHE, 1.2, "none", "4,3")]
o += [T(336, 288, "非其义也，弗顾", 5.2, ZHE)]
for i in range(3):
    o += [L(500, 300 + i * 14, 600, 300 + i * 14, ZONG, 1.2)]
    o += [L(500, 300 + i * 14, 508, 304 + i * 14, ZONG, 0.8)]
o += [T(550, 288, "币聘", 6.0, ZONG, ls=2)]
o += [T(550, 424, "汤三使往聘之", 5.4, GREY)]
o += tail5(h, "吾闻其以尧舜之道要汤。", "图四十一", "割烹要汤", "ch130a")
save("ch130a-geqing-yaotang.svg", o)


# ---------------------------------------------------------- 131 观其所主
h = 540
o = head_("观 其 所 主", "《孟子》万章上　第一百三十一章　MZ131", h)
o.append(T(380, 112, "孔子于卫主痈疽　于齐主侍人瘠环　有诸", 6.0, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(320, 300, 130, 96, WARM, 1.2, fill=PALE)]
o += [L(312, 292, 320, 300, WARM, 1.0), L(450, 292, 458, 300, WARM, 1.0), L(304, 290, 466, 290, WARM, 1.2)]
o += [R(342, 322, 54, 70, WARM, 0.9, fill=SOFT)]
o += [T(385, 284, "所主之家", 5.6, ZONG)]
o += [stand(270, 404, 70, INK, 1.0)]
o += [T(256, 316, "远臣", 5.2, GREY, anchor="end")]
o += [stand(516, 404, 70, INK, 1.0)]
o += [T(530, 316, "近臣", 5.2, GREY, anchor="start")]
o += [P("M 286,352 L 476,352", ZHE, 0.9, "none", "4,3")]
o += [T(380, 424, "观近臣以其所为主，观远臣以其所主", 5.8, GREY)]
o += tail5(h, "何以为孔子。", "图四十二", "观其所主", "ch131a")
save("ch131a-guanqisuo-zhu.svg", o)


# ---------------------------------------------------------- 132 百里奚自鬻
h = 540
o = head_("百 里 奚 自 鬻", "《孟子》万章上　第一百三十二章　MZ132", h)
o.append(T(380, 112, "百里奚自鬻于秦养牲者　五羊之皮，食牛", 6.0, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
for i in range(5):
    o += sheep(140 + i * 6, 330 + i * 16, 96, 34, ZONG, 0.9)
o += [T(200, 300, "五羊之皮", 6.2, ZONG, ls=1)]
o += [T(200, 424, "自鬻之说，好事者为之", 5.4, GREY)]
o += kneel(400, 404, 72, INK, 1.0)
o += [T(400, 300, "百里奚", 5.6, ZONG)]
o += [T(512, 380, "年已七十", 5.6, ZHE)]
o += [P("M 440,356 L 500,356", GREY, 0.8, "none", "4,3")]
o += [T(512, 344, "知虞公之不可谏而去", 5.2, GREY)]
o += tail5(h, "贤者为之乎？", "图四十三", "百里奚自鬻", "ch132a")
save("ch132a-bailixi-ziyu.svg", o)
