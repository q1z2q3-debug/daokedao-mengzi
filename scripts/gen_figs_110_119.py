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
"""离娄下 图 110–119（v0.18.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
坑：C() 第五位是 fill；P() 第五位才是 dash。
"""

def tail2(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 离娄下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


# ---------------------------------------------------------- 110 逢蒙学射
h = 540
o = head_("逢 蒙 学 射", "《孟子》离娄下　第一百一十章　MZ110", h)
o.append(T(380, 112, "逢蒙学射于羿　尽羿之道　于是杀羿", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [C(280, 344, 62, ZONG, 1.3), C(280, 344, 18, ZONG, 1.0)]
for i in range(8):
    a = i * 45 + 20
    o += [L(round(280 + 18 * math.cos(math.radians(a))), round(344 + 18 * math.sin(math.radians(a))),
            round(280 + 62 * math.cos(math.radians(a))), round(344 + 62 * math.sin(math.radians(a))), ZONG, 0.9)]
o += [T(280, 268, "轮", 6.2, ZONG, ls=3)]
o += [P("M 470,282 C 430,306 430,382 470,404", ZONG, 1.5)]
o += [L(470, 282, 470, 404, GREY, 0.9)]
o += [T(438, 272, "弓", 6.0, ZONG)]
for i in range(4):
    o += [L(500, 322 + i * 20, 584, 322 + i * 20, ZONG, 1.2)]
    o += [L(492, 316 + i * 20, 500, 322 + i * 20, ZONG, 0.9), L(492, 328 + i * 20, 500, 322 + i * 20, ZONG, 0.9)]
o += [P("M 604,394 L 614,388 L 610,400 Z", ZHE, 0.9, fill=PALE)]
o += [P("M 620,394 L 630,388 L 626,400 Z", ZHE, 0.9, fill=PALE)]
o += [T(616, 412, "镞，去之", 5.2, ZHE)]
o += [T(552, 300, "乘矢四发　去其金", 5.8, ZHE, ls=1)]
o += [T(380, 424, "取友必端：以夫子之道，反害夫子", 6.2, GREY)]
o += tail2(h, "其取友必端矣。", "图二十一", "逢蒙学射", "ch110a")
save("ch110a-qiyou-biduan.svg", o)

# ---------------------------------------------------------- 111 西子蒙不洁
h = 540
o = head_("西 子 蒙 不 洁", "《孟子》离娄下　第一百一十一章　MZ111", h)
o.append(T(380, 112, "西子蒙不洁，则人皆掩鼻而过之", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [stand(196, 404, 104, INK, 1.2)]
o += [P("M 188,324 C 182,332 190,338 184,346 C 178,354 188,358 182,366", GREY, 0.9)]
o += [P("M 204,326 C 210,336 202,344 208,352", GREY, 0.9)]
o += [C(180, 336, 3.0, WARM, 0.8), C(212, 348, 2.4, WARM, 0.8)]
o += [T(196, 270, "蒙不洁", 5.8, ZONG, ls=1)]
o += [stand(292, 404, 80, INK, 1.0)]
o += [L(292, 356, 300, 338, INK, 0.9), C(301, 334, 3.6, INK, 0.9)]
o += [T(300, 268, "掩鼻而过", 5.6, GREY)]
o += [L(380, 250, 380, 396, GREY, 0.7, "5,4")]
o += [E(470, 392, 52, 12, ZONG, 1.2, fill=SOFT)]
o += [E(470, 388, 44, 8, GREY, 0.7)]
o += [P("M 434,392 C 448,384 496,384 508,392", WARM, 0.8)]
o += [T(470, 372, "沐浴", 5.4, ZONG)]
o += [stand(556, 404, 88, ZONG, 1.1)]
o += [T(556, 296, "齐戒沐浴", 5.6, ZHE)]
o += [T(556, 310, "可以祀上帝", 5.4, GREY)]
o += [T(380, 424, "不洁可洗，丧善难复；此章戒丧善而勉自新", 6.2, GREY)]
o += tail2(h, "虽有恶人，齐戒沐浴，则可以祀上帝。", "图二十二", "西子蒙不洁", "ch111a")
save("ch111a-xizi-mengbujie.svg", o)

# ---------------------------------------------------------- 112 则故而已
h = 540
o = head_("则 故 而 已", "《孟子》离娄下　第一百一十二章　MZ112", h)
o.append(T(380, 112, "天下之言性也，则故而已矣　故者以利为本", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [L(300, 300, 300, 400, ZONG, 1.8)]
o += [E(300, 300, 8, 3, ZONG, 1.0)]
o += [L(200, 396, 560, 396, ZONG, 1.3)]
for i in range(9):
    o += [L(216 + i * 40, 396, 216 + i * 40, 404, ZONG, 0.8)]
o += [R(302, 391, 140, 9, GREY, 0.6, fill=SOFT)]
o += [L(302, 391, 442, 391, GREY, 0.6), L(302, 400, 442, 400, GREY, 0.6)]
o += [T(300, 288, "表", 6.0, ZONG, ls=2)]
o += [T(464, 388, "影", 5.4, GREY)]
o += [T(300, 372, "求其故", 5.8, ZHE, ls=1)]

o += [T(380, 424, "千岁之日至，可坐而致；所恶于智者，为其凿也", 6.2, GREY)]
o += tail2(h, "苟求其故，千岁之日至，可坐而致也。", "图二十三", "则故而已", "ch112a")
save("ch112a-ze-gu-eryi.svg", o)

# ---------------------------------------------------------- 113 朝廷不历位
h = 540
o = head_("不 历 位", "《孟子》离娄下　第一百一十三章　MZ113", h)
o.append(T(380, 112, "朝廷不历位而相与言，不逾阶而相揖", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
for i in range(5):
    o += [E(190 + i * 88, 400, 32, 6, ZONG, 1.0, fill=SOFT)]
o += [T(380, 376, "位　次", 5.4, GREY, ls=8)]
o += [stand(190, 392, 92, INK, 1.1)]
o += [stand(278, 392, 92, INK, 1.1, "point")]
o += [P("M 190,392 C 230,360 250,352 262,352", ZHE, 0.8, "none", "4,3")]
o += arrow(262, 350, 330, 344, ZHE, 0.9, 4.0)
o += [T(286, 336, "历位", 5.4, ZHE)]
o += [T(278, 300, "就人位而言", 5.2, GREY)]
o += [T(420, 268, "不历位而相与言", 6.0, ZONG, ls=1)]
o += [T(380, 424, "我欲行礼，子敖以我为简，不亦异乎", 6.2, GREY)]
o += tail2(h, "我欲行礼，子敖以我为简，不亦异乎？", "图二十四", "不历位", "ch113a")
save("ch113a-chaoting-buliwei.svg", o)

# ---------------------------------------------------------- 114 以仁存心
h = 540
o = head_("以 仁 存 心", "《孟子》离娄下　第一百一十四章　MZ114", h)
o.append(T(380, 112, "君子以仁存心，以礼存心", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 380,300 C 350,270 300,296 322,330 C 340,356 380,382 380,382 C 380,382 420,356 438,330 C 460,296 410,270 380,300 Z", ZHE, 1.2, fill=SOFT)]
o += [T(380, 344, "仁", 9.0, ZHE)]
o += arrow(180, 300, 306, 300, GREY, 1.0, 4.5)
o += arrow(180, 340, 300, 336, GREY, 1.0, 4.5)
o += arrow(180, 380, 322, 366, GREY, 1.0, 4.5)
o += [T(232, 288, "横逆", 6.0, GREY, ls=2)]
o += [T(232, 400, "其待我以横逆", 5.6, GREY)]
o += arrow(468, 330, 560, 330, ZHE, 1.0, 4.5)
o += [T(516, 318, "自反", 6.0, ZHE, ls=2)]
o += [T(516, 352, "不仁？无礼？不忠？", 5.4, GREY)]
o += [T(380, 258, "存 心", 6.2, ZONG, ls=4)]
o += [T(380, 424, "君子有终身之忧，无一朝之患", 6.2, GREY)]
o += tail2(h, "君子以仁存心，以礼存心。", "图二十五", "以仁存心", "ch114a")
save("ch114a-yiren-cunxin.svg", o)

# ---------------------------------------------------------- 115 禹稷颜回
h = 540
o = head_("禹 稷 颜 回", "《孟子》离娄下　第一百一十五章　MZ115", h)
o.append(T(380, 112, "禹稷当平世，三过其门而不入", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(160, 262, 22, 142, ZONG, 1.2, fill=SOFT), R(226, 262, 22, 142, ZONG, 1.2, fill=SOFT)]
o += [L(154, 262, 254, 262, ZONG, 1.4), L(154, 404, 254, 404, ZONG, 1.2)]
o += [P("M 182,272 L 226,282 L 226,368 L 182,358 Z", ZONG, 0.9, fill=PALE)]
o += [T(204, 250, "门", 6.2, ZONG, ls=2)]
o += [L(126, 396, 286, 396, GREY, 0.8)]
for i in range(4):
    o += [E(146 + i * 34, 396, 8, 3.4, GREY, 0.7)]
o += [T(200, 388, "三过不入", 5.4, GREY)]
o += [L(300, 250, 300, 396, GREY, 0.7, "5,4")]
o += [R(342, 262, 18, 142, ZONG, 1.2, fill=SOFT), R(486, 262, 18, 142, ZONG, 1.2, fill=SOFT)]
o += [L(342, 404, 504, 404, ZONG, 0.9, "4,3")]
o += [L(360, 396, 486, 396, ZONG, 0.7)]
o += [stand(430, 396, 88, INK, 1.1)]
o += [bowl(452, 356, 20, 8)]
o += [T(430, 250, "陋巷", 6.2, ZONG, ls=2)]
o += [T(430, 388, "一箪食　一瓢饮", 5.4, GREY)]
o += [T(380, 424, "禹稷颜回同道：易地则皆然", 6.2, GREY)]
o += tail2(h, "禹、稷、颜回同道。", "图二十六", "禹稷颜回", "ch115a")
save("ch115a-yuji-yanhui.svg", o)

# ---------------------------------------------------------- 116 责善贼恩
h = 540
o = head_("责 善 贼 恩", "《孟子》离娄下　第一百一十六章　MZ116", h)
o.append(T(380, 112, "父子责善，贼恩之大者", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [L(150, 330, 340, 330, ZONG, 2.0), L(420, 330, 610, 330, ZONG, 2.0)]
o += [L(340, 330, 354, 330, ZHE, 1.2, "3,3"), L(406, 330, 420, 330, ZHE, 1.2, "3,3")]
o += [T(380, 322, "断", 6.4, ZHE, ls=3)]
o += [R(338, 352, 40, 9, ZONG, 1.0, fill=SOFT)]
o += [P("M 378,351 L 424,351 L 434,356 L 424,362 L 378,362 Z", INK, 1.2, fill=PALE)]
o += [T(380, 340, "责善", 5.8, INK, ls=2)]
o += [T(216, 288, "朋友", 5.8, ZONG, ls=2), T(544, 288, "父子", 5.8, ZHE, ls=2)]
o += [T(216, 356, "可以责", 5.4, GREY), T(544, 356, "不可以责", 5.4, ZHE)]
o += [T(380, 424, "贼恩之大者；章子出妻屏子，终身不养", 6.2, GREY)]
o += tail2(h, "父子责善，贼恩之大者。", "图二十七", "责善贼恩", "ch116a")
save("ch116a-zeshan-zeien.svg", o)

# ---------------------------------------------------------- 117 易地皆然
h = 540
o = head_("易 地 皆 然", "《孟子》离娄下　第一百一十七章　MZ117", h)
o.append(T(380, 112, "曾子，师也，父兄也；子思，臣也，微也", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(130, 250, 20, 154, ZONG, 1.2, fill=SOFT), R(196, 250, 20, 154, ZONG, 1.2, fill=SOFT)]
o += [L(124, 250, 222, 250, ZONG, 1.4)]
o += [stand(270, 404, 88, INK, 1.1, "point")]
o += [P("M 250,340 C 240,352 244,372 258,372 C 272,372 276,352 266,340 Z", ZONG, 1.0, fill=SOFT)]
o += [T(163, 240, "曾子居武城", 5.8, ZONG, ls=1)]
o += [T(270, 388, "寇至则去", 5.4, GREY)]
o += [L(370, 250, 370, 396, GREY, 0.7, "5,4")]
o += [R(452, 250, 20, 154, ZONG, 1.2, fill=SOFT), R(518, 250, 20, 154, ZONG, 1.2, fill=SOFT)]
o += [L(446, 250, 544, 250, ZONG, 1.4)]
o += [stand(432, 404, 88, INK, 1.1)]
o += [T(495, 240, "子思居于卫", 5.8, ZONG, ls=1)]
o += [T(432, 388, "寇至则守", 5.4, ZHE)]
o += [T(380, 424, "或远害，或死难：所处之地不同，其心一也", 6.2, GREY)]
o += tail2(h, "曾子、子思易地则皆然。", "图二十八", "易地皆然", "ch117a")
save("ch117a-yidi-jieran.svg", o)

# ---------------------------------------------------------- 118 尧舜同人
h = 540
o = head_("尧 舜 同 人", "《孟子》离娄下　第一百一十八章　MZ118", h)
o.append(T(380, 112, "王使人瞷夫子，果有以异于人乎", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [R(300, 268, 22, 136, ZONG, 1.4, fill=SOFT)]
o += [T(311, 256, "墙", 6.0, ZONG, ls=2)]
for i in range(6):
    o += [L(300, 292 + i * 18, 322, 292 + i * 18, GREY, 0.6)]
o += [E(311, 330, 5, 9, GREY, 0.9)]
o += [stand(250, 404, 84, INK, 1.1, "point")]
o += [L(266, 326, 302, 320, INK, 0.9)]
o += [T(250, 300, "瞷", 6.6, ZONG, ls=3)]
o += [stand(430, 404, 84, INK, 1.1)]
o += [R(452, 366, 26, 14, WARM, 1.0, fill=PALE)]
o += [T(430, 300, "夫子", 5.8, GREY, ls=2)]
o += [T(380, 424, "圣人亦人耳；尧舜与人同", 6.2, GREY)]
o += tail2(h, "尧舜与人同耳。", "图二十九", "尧舜同人", "ch118a")
save("ch118a-yaoshun-tongren.svg", o)

# ---------------------------------------------------------- 119 齐人之羞
h = 540
o = head_("齐 人 之 羞", "《孟子》离娄下　第一百一十九章　MZ119", h)
o.append(T(380, 112, "卒之东郭墦间，之祭者，乞其余", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 150,404 C 176,356 244,356 270,404 Z", ZONG, 1.1, fill=SOFT)]
o += [R(200, 336, 18, 44, ZONG, 1.0, fill=PALE)]
o += [T(210, 328, "墦", 5.8, ZONG, ls=2)]
o += [C(236, 372, 11, WARM, 1.0), L(236, 362, 236, 378, WARM, 0.8)]
o += [stand(300, 404, 80, INK, 1.1, "point")]
o += [bowl(336, 384, 18, 7)]
o += [T(300, 298, "乞其余", 5.6, GREY)]
o += [L(400, 250, 400, 396, GREY, 0.7, "5,4")]
o += [stand(452, 404, 92, INK, 1.1)]
o += [stand(514, 404, 78, INK, 1.1)]
o += [L(466, 344, 452, 366, INK, 0.8), L(500, 340, 514, 366, INK, 0.8)]
o += [T(483, 250, "中庭", 5.8, ZONG, ls=2)]
o += [C(470, 300 - 6, 2.2, ZHE, 0.8)]
o += [C(494, 300 - 6, 2.2, ZHE, 0.8)]
o += [T(483, 386, "相泣", 5.4, ZHE)]
o += [T(380, 424, "所仰望而终身者，今若此；其妻妾不羞者几希", 6.2, GREY)]
o += tail2(h, "其妻妾不羞也，而不相泣者，几希矣。", "图三十", "齐人之羞", "ch119a")
save("ch119a-qiren-zhixiu.svg", o)
