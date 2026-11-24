# -*- coding: utf-8 -*-
"""滕文公下 图 52 / 56 修订稿（v0.12.0）
用法：python3 scripts/gen_fig_52_56.py   仅重绘 ch52a 与 ch56a 两张。
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


def deer(cx, cy, s=1.0, col=INK, sw=1.2, forest=0):
    o = [f'  <g transform="translate({cx},{cy}) scale({s})">',
         P("M -30,6 C -31,-8 -18,-14 2,-13 C 18,-12 27,-7 27,1 C 27,10 18,14 0,14 C -14,14 -29,12 -30,6 Z",
           col, sw, fill=PALE),
         P("M 21,-7 C 25,-15 27,-21 28,-27", col, sw * 1.5),
         P("M 27,-4 C 31,-12 33,-18 34,-25", col, sw * 1.5)]
    if not forest:
        o += [P("M 28,-33 C 25,-39 22,-41 19,-43", col, sw * 1.1),
              P("M 32,-34 C 32,-41 34,-44 37,-47", col, sw * 1.1),
              P("M 33,-38 L 29,-41", col, sw * 0.9), P("M 35,-41 L 38,-44", col, sw * 0.9)]
    else:
        o += [P("M 28,-33 C 25,-38 24,-40 23,-42", col, sw * 1.1),
              P("M 35,-34 C 40,-37 43,-38 46,-38", col, sw * 1.1)]
    o += [E(33, -29, 8, 5.4, col, sw),
          P("M 40,-27 C 43,-25 42,-22 38,-22", col, sw),
          C(35, -30.5, 1.1, col, sw * 0.8),
          P("M -30,2 C -35,-3 -36,4 -30,5", col, sw * 1.1),
          P("M -20,13 C -23,18 -22,22 -20,26", col, sw), L(-20, 26, -24, 32, col, sw),
          P("M -8,14 C -10,19 -9,23 -7,27", col, sw), L(-7, 27, -10, 32, col, sw),
          P("M 12,13 C 10,18 11,22 13,26", col, sw), L(13, 26, 10, 32, col, sw),
          P("M 20,10 C 21,16 23,20 24,25", col, sw), L(24, 25, 23, 31, col, sw)]
    o.append('  </g>')
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


def tail_(h, q, vol, label, name, key):
    return [
        L(120, h - 104, 640, h - 104, LINE, 1),
        T(380, h - 80, q, 8.6, INK, ls=2),
        f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · {vol}</text>',
        f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>',
    ]


def save(name, lines):
    s = "\n".join(lines) + "\n</svg>\n"
    with open(os.path.join(FIG, name), "w", encoding="utf-8") as f:
        f.write(s)
    print(name, len(s))


# ---------------------------------------------------------------- 52 范与诡
h = 560
o = head_("范 与 诡", "《孟子》滕文公下　第五十二章　MZ052", h)
o.append(T(380, 172, "同一辆车　一条直道　一条斜道", 6.2, GREY, ls=1))
o.append(L(385, 190, 385, 436, LINE, 0.8))
o.append(T(245, 136, "范", 10, ZHE, ls=3))
o.append(T(525, 136, "诡", 10, ZONG, ls=3))
o += [L(120, 408, 340, 408, WARM, 1.8), L(120, 416, 340, 416, GREY, 0.6)]
o += [C(166, 400, 10, ZHE, 1.3), C(208, 400, 10, ZHE, 1.3), R(154, 362, 62, 26, ZHE, 1.4),
      L(216, 369, 250, 358, ZHE, 1.5)]
o += [C(248, 344, 5.5, ZHE, 1.2), L(248, 350, 248, 374, ZHE, 1.3),
      L(248, 374, 240, 398, ZHE, 1.1), L(248, 374, 256, 398, ZHE, 1.1)]
o.append(T(258, 334, "请辞", 6, ZONG))
o += deer(316, 358, 1.5, INK, 1.2, forest=0)
o.append(T(238, 438, "范我驰驱", 7, ZHE))
o.append(T(238, 452, "终日不获一", 6, GREY))
o += [P("M 400,412 L 650,356", WARM, 2.2), P("M 400,420 L 650,364", GREY, 0.6)]
o.append('  <g transform="rotate(-13 490 380)">')
o += [C(478, 380, 9.5, ZONG, 1.2), C(514, 380, 9.5, ZONG, 1.2), R(470, 346, 54, 26, ZONG, 1.4),
      L(524, 353, 558, 342, ZONG, 1.5), C(557, 330, 5, ZONG, 1.1),
      L(557, 335, 557, 354, ZONG, 1.2), L(557, 354, 550, 370, ZONG, 1), L(557, 354, 564, 370, ZONG, 1)]
o.append('  </g>')
o += deer(614, 320, 1.35, INK, 1.2, forest=1)
o += arrow(548, 316, 590, 326, INK, 1.1)
o += arrow(542, 330, 588, 334, INK, 1.1)
o += arrow(556, 300, 592, 318, INK, 1.1)
o.append(T(548, 438, "诡遇", 7, ZONG))
o.append(T(548, 452, "一朝而获十", 6, GREY))
o += tail_(h, "枉己者，未有能直人者也。", "滕文公下", "图一", "范与诡", "ch52a")
save("ch52a-fan-yu-gui.svg", o)

# ---------------------------------------------------------------- 56 大旱望雨
h = 560
o = head_("大 旱 望 雨", "《孟子》滕文公下　第五十六章　MZ056", h)
o += [R(120, 300, 272, 116, WARM, 0.0, fill=SOFT)]
o += [L(126, 400, 386, 400, WARM, 2)]
o += [P("M 150,352 l 14,9 l -8,10 l 16,8", ZONG, 0.9),
      P("M 232,344 l 14,9 l -10,11 l 14,9", ZONG, 0.9),
      P("M 322,350 l 14,9 l -8,10 l 16,8", ZONG, 0.9)]


def sprout(x, base, hh, col=ZONG):
    return [P(f"M {x},{base} L {x},{base-hh}", col, 1.5),
            P(f"M {x},{base-hh+6} C {x-7},{base-hh-2} {x-13},{base-hh-6} {x-19},{base-hh-4}", col, 1.2),
            P(f"M {x},{base-hh*0.55} C {x+8},{base-hh*0.55-5} {x+14},{base-hh*0.55-8} {x+20},{base-hh*0.55-5}", col, 1.2)]


for x, hh in ((162, 38), (208, 28), (254, 34), (300, 24), (342, 32)):
    o += sprout(x, 398, hh)
o += [L(140, 392, 154, 392, ZONG, 0.8), L(180, 394, 194, 394, ZONG, 0.8),
      L(270, 394, 284, 394, ZONG, 0.8), L(312, 392, 326, 392, ZONG, 0.8),
      L(352, 394, 366, 394, ZONG, 0.8)]
o.append(T(190, 294, "裂田枯苗", 6.4, ZONG))
for cx, cy, r in ((502, 190, 15), (528, 180, 20), (552, 190, 13)):
    o.append(C(cx, cy, r, GREY, 1.2, fill=SOFT))
o += [L(484, 200, 570, 200, GREY, 1.1)]
for xx in (496, 518, 540, 560):
    o.append(L(xx, 208, xx - 9, 226, ZONG, 1.1, dash="3,2"))
o += [P("M 596,214 A 32,32 0 0 1 660,214", WARM, 1.5),
      P("M 602,218 A 26,26 0 0 1 654,218", ZHE, 1.2)]
o.append(T(516, 250, "雨", 6.6, ZONG))
o.append(T(628, 240, "霓", 6.4, ZHE))
o += [R(556, 352, 96, 9, WARM, 1.3, fill=SOFT), L(562, 361, 562, 392, WARM, 1.1),
      L(646, 361, 646, 392, WARM, 1.1),
      P("M 562,352 C 562,334 582,334 582,352", ZHE, 1.2),
      P("M 588,352 C 588,336 606,336 606,352", ZHE, 1.2),
      R(612, 342, 34, 10, ZONG, 1.1, fill=PALE)]
o.append(T(604, 416, "归市者不止", 6.4, ZONG))
o += stand(676, 396, 64, INK, 1.2, arms="")
o.append(L(676, 348, 690, 356, INK, 1.1))
o += [L(690, 356, 712, 384, WARM, 1.4), P("M 712,384 L 700,392 L 714,396 Z", INK, 1.2, fill=SOFT)]
o.append(T(686, 424, "耕者不变", 6.2, INK))
o += tail_(h, "苟行王政，四海之内皆举首而望之。", "滕文公下", "图一", "大旱望雨", "ch56a")
save("ch56a-dahan-wang-yu.svg", o)
