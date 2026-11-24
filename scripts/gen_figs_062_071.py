# -*- coding: utf-8 -*-
"""离娄上 图 62–71（v0.13.0 二稿）
用法：python3 scripts/gen_figs_062_071.py
注意：P() 第三位之后依次是 fill、dash；画虚线时须显式传 fill="none"。
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


def save(name, lines):
    s = "\n".join(lines) + "\n</svg>\n"
    with open(os.path.join(FIG, name), "w", encoding="utf-8") as f:
        f.write(s)
    print(name, len(s))


def compass(ax, ay, cx, cy, px, py, col=ZONG, sw=1.3):
    """圆规：顶点在圆外上方，一脚落圆心，一脚落圆周。"""
    return [L(ax, ay, cx, cy, col, sw), L(ax, ay, px, py, col, sw),
            L(ax - 9, ay + 4, ax + 9, ay + 4, col, sw * 0.9),
            C(ax, ay, 2.6, col, sw, fill=PALE),
            C(cx, cy, 1.8, col, sw, fill=INK),
            L(px, py, px + 4, py + 7, col, sw * 0.9)]


def tube(x, y, w=11, hh=60, col=ZONG, sw=1.1):
    return [R(x, y, w, hh, col, sw, fill=SOFT), E(x + w / 2, y, w / 2, 2.4, col, sw)]


def vessel(cx, base, s=1.0, col=ZONG, sw=1.1):
    """爵：一器三足。"""
    w = 11 * s; hh = 24 * s
    return [P(f"M {cx-w},{base} L {cx+w},{base} L {cx+w*0.62},{base-hh} L {cx-w*0.62},{base-hh} Z",
              col, sw, fill=PALE),
            E(cx, base - hh, w * 0.62, 2.4 * s, col, sw),
            P(f"M {cx-w},{base-hh*0.55} L {cx-w*1.9},{base-hh*0.2} L {cx-w*1.4},{base-hh*0.85}",
              col, sw),
            L(cx - w * 0.5, base, cx - w * 0.7, base + 7, col, sw * 0.9),
            L(cx + w * 0.5, base, cx + w * 0.7, base + 7, col, sw * 0.9),
            L(cx, base, cx, base + 8, col, sw * 0.9)]


# ---------------------------------------------------------- 62 规矩·六律·仁政
h = 540
o = head_("规矩 · 六律 · 仁政", "《孟子》离娄上　第六十二章　MZ062", h)
o += [L(300, 96, 300, 424, LINE, 1), L(464, 96, 464, 424, LINE, 1)]
# 左：规画圆
o += [C(188, 208, 54, INK, 1.4)]
o += compass(188, 126, 188, 208, 226, 246)
o.append(T(148, 122, "规", 8, ZONG))
# 左：矩画方
o += [R(142, 288, 92, 92, INK, 1.4),
      L(126, 288, 126, 380, INK, 2.4), L(126, 380, 234, 380, INK, 2.4),
      L(126, 292, 126, 288, ZONG, 1.0), L(230, 380, 234, 380, ZONG, 1.0)]
o.append(T(240, 280, "矩", 8, ZONG))
o.append(T(188, 412, "不以规矩　不能成方员", 6.2, ZONG))
# 中：六律
base = 374
o.append(L(310, base, 452, base, WARM, 1.2))
for i, hh in enumerate((44, 54, 64, 74, 84, 92)):
    o += tube(318 + i * 21, base - hh, 11, hh)
o += [T(384, 128, "六律", 8.4, ZONG), L(384, 134, 384, 146, LINE, 0.8),
      T(384, 392, "阴阳各六　以正五音", 6.2, ZONG)]
# 右：仁政
o += [L(484, 340, 636, 340, ZONG, 1.0),
      L(484, 348, 636, 348, WARM, 1.6),
      L(484, 356, 636, 356, GREY, 0.6)]
for xx in (496, 516, 536, 556, 576, 596, 616):
    o.append(L(xx, 342, xx + 9, 332, ZONG, 0.9))
o += stand(560, 344, 96, INK, 1.2, arms="down")
o.append(T(560, 236, "仁政", 8.4, ZHE, ls=2))
o.append(T(560, 384, "平治天下　非心之独任", 6.0, ZONG))
o += tail_(h, "徒善不足以为政，徒法不能以自行。", "图一", "规矩·六律·仁政", "ch62a")
save("ch62a-guiju-liulu-renzheng.svg", o)

# ---------------------------------------------------------- 63 方员之至·人伦之至
h = 540
o = head_("方员之至 · 人伦之至", "《孟子》离娄上　第六十三章　MZ063", h)
o += [L(120, 204, 640, 204, ZONG, 1.0, "8,4"), T(380, 192, "至", 9, ZONG, ls=2)]
o += [C(206, 262, 58, INK, 1.4)]
o += compass(206, 140, 206, 262, 247, 303)
o += stand(520, 400, 196, INK, 1.3, arms="down")
o += [L(486, 400, 554, 400, WARM, 1.4),
      L(470, 208, 470, 400, ZONG, 1.0, "5,3"),
      P("M 463,400 L 470,414 L 477,400 Z", ZONG, 1.0, fill=SOFT),
      T(462, 264, "绳", 5.8, ZONG, anchor="end")]
o.append(T(206, 348, "方员之至", 7, ZONG))
o.append(T(596, 300, "人伦之至", 7, ZHE))
o += [T(206, 372, "规矩尽所以为方员之理", 5.8, GREY),
      T(206, 386, "犹圣人尽所以为人之道", 5.8, GREY)]
o += tail_(h, "规矩，方员之至也；圣人，人伦之至也。", "图一", "方员之至·人伦之至", "ch63a")
save("ch63a-fangyuan-renlun.svg", o)

# ---------------------------------------------------------- 64 四级失守
h = 540
o = head_("四 级 失 守", "《孟子》离娄上　第六十四章　MZ064", h)
o.append(T(380, 112, "不仁者，先失其位，后失其身", 6.4, GREY, ls=1))
bars = [(200, 400, "天子", "四海"), (250, 300, "诸侯", "社稷"),
        (300, 220, "卿大夫", "宗庙"), (350, 140, "士庶人", "四体")]
for i, (yy, wd, who, what) in enumerate(bars):
    o += [R(200, yy, wd, 10, ZONG, 1.0, fill=SOFT),
          L(200, yy + 10, 200 + wd, yy + 10, ZHE, 1.6),
          T(188, yy + 9, who, 6.6, INK, anchor="end"),
          T(200 + wd + 8, yy + 9, what, 6.6, ZONG, anchor="start")]
o += [L(600, 206, 340, 356, GREY, 1.0, "4,4")]
o += stand(392, 396, 54, INK, 1.0, arms="down")
o.append(T(474, 330, "一级比一级贴身", 6.2, GREY, anchor="start"))
o += tail_(h, "天子不仁，不保四海；士庶人不仁，不保四体。", "图一", "四级失守", "ch64a")
save("ch64a-siji-shishou.svg", o)

# ---------------------------------------------------------- 65 射不中·反求诸身
h = 540
o = head_("射 不 中 · 反 求 诸 身", "《孟子》离娄上　第六十五章　MZ065", h)
# 靶
o += [C(596, 252, 44, INK, 1.4), C(596, 252, 30, ZONG, 1.2), C(596, 252, 16, ZHE, 1.2),
      C(596, 252, 3, INK, 1.0, fill=INK)]
o += [L(578, 294, 570, 400, WARM, 1.2), L(614, 294, 622, 400, WARM, 1.2),
      L(556, 400, 640, 400, WARM, 1.2)]
o += [L(590, 250, 604, 244, INK, 1.0), L(586, 258, 602, 254, INK, 1.0),
      L(592, 262, 598, 256, INK, 1.0)]
# 偏出的箭
o += [L(596, 168, 644, 128, INK, 1.3), P("M 644,128 L 634,127 L 639,136 Z", INK, 1.2, fill=INK),
      L(600, 176, 596, 166, ZONG, 0.9)]
o.append(T(626, 116, "不中", 6.4, ZHE))
# 射者与弓
o += stand(272, 400, 190, INK, 1.3, arms="")
o += [P("M 308,244 C 320,262 328,278 334,292", ZONG, 2.0),
      P("M 334,300 C 328,314 320,330 308,346", ZONG, 2.0),
      L(308, 244, 308, 346, INK, 0.9),
      R(328, 289, 10, 14, ZONG, 1.2, fill=SOFT),
      L(272, 296, 308, 296, INK, 1.2),
      L(308, 296, 356, 296, ZONG, 1.3),
      P("M 356,296 L 368,292 L 368,300 Z", INK, 1.2, fill=INK),
      L(310, 292, 318, 288, ZONG, 0.8), L(310, 300, 318, 304, ZONG, 0.8)]
o.append(T(316, 236, "弓", 5.8, ZONG))
o.append(T(268, 352, "反求诸己", 6.4, ZONG))
o.append(T(206, 398, "射者正己而后发", 6.0, GREY))
o += tail_(h, "行有不得者，皆反求诸己。", "图一", "射不中·反求诸身", "ch65a")
save("ch65a-she-buzhong.svg", o)

# ---------------------------------------------------------- 66 一条向下走的链
h = 540
o = head_("一 条 向 下 走 的 链", "《孟子》离娄上　第六十六章　MZ066", h)
o.append(T(380, 112, "人有恒言　皆曰天下国家", 6.2, GREY, ls=1))
o += [L(150, 344, 610, 344, WARM, 1.4), L(150, 350, 610, 350, GREY, 0.6)]
# 根
o += [P("M 380,344 C 378,378 374,404 372,428", ZONG, 3.4),
      P("M 374,380 C 356,392 336,398 318,400", ZONG, 2.2),
      P("M 386,386 C 404,398 424,402 442,402", ZONG, 2.2),
      P("M 320,398 C 308,408 300,414 292,420", ZONG, 1.3),
      P("M 440,400 C 452,410 460,416 468,420", ZONG, 1.3),
      P("M 376,404 C 362,414 352,420 344,424", ZONG, 1.3),
      P("M 384,406 C 396,416 404,420 412,424", ZONG, 1.3)]
# 干
o += [P("M 362,344 L 366,290 L 394,290 L 398,344 Z", ZONG, 1.2, fill=SOFT)]
# 枝
o += [P("M 380,290 C 380,250 410,232 444,222", ZONG, 1.6),
      P("M 380,290 C 380,250 350,232 316,222", ZONG, 1.6),
      P("M 444,222 C 466,214 484,208 496,202", ZONG, 1.1),
      P("M 316,222 C 294,214 276,208 264,202", ZONG, 1.1)]
# 冠
o += [P("M 244,208 C 250,182 264,172 282,168 C 300,150 336,144 364,146 "
        "C 392,144 424,152 442,168 C 466,174 494,182 512,206 "
        "C 470,220 452,212 434,218 C 408,226 386,214 364,220 C 340,226 318,214 296,218 C 274,222 256,214 244,208 Z", ZONG, 1.3, fill=SOFT)]
o += [P("M 300,186 C 316,172 340,166 358,168", ZONG, 0.9),
      P("M 400,168 C 418,166 440,172 456,184", ZONG, 0.9),
      P("M 330,200 C 352,190 386,188 410,196", ZONG, 0.9)]
o += [T(380, 190, "天下", 8.4, ZHE, ls=2)]
# 标签
o += [T(402, 320, "家", 8, INK), L(396, 316, 382, 314, LINE, 0.8)]
o += [T(456, 250, "国", 7.6, ZONG), L(448, 254, 420, 244, LINE, 0.8)]
o += [T(458, 404, "身", 8.4, ZHE), L(446, 400, 400, 398, LINE, 0.8)]
o += tail_(h, "天下之本在国，国之本在家，家之本在身。", "图一", "一条向下走的链", "ch66a")
save("ch66a-tianxia-guojia.svg", o)

# ---------------------------------------------------------- 67 巨室之门
h = 540
o = head_("巨 室 之 门", "《孟子》离娄上　第六十七章　MZ067", h)
o.append(T(380, 112, "门不上锁　不须锁", 6.2, GREY, ls=1))
o += [L(300, 190, 300, 404, INK, 2.0), L(460, 190, 460, 404, INK, 2.0),
      L(294, 190, 466, 190, INK, 2.2), L(292, 404, 468, 404, WARM, 1.6),
      L(316, 190, 316, 404, ZONG, 1.0), L(444, 190, 444, 404, ZONG, 1.0)]
# 门内之人（坐）
o += [C(380, 262, 12, INK, 1.2),
      P("M 380,274 C 366,282 362,300 362,318 L 398,318 C 398,300 394,282 380,274 Z",
        INK, 1.2, fill=SOFT),
      P("M 362,318 C 350,330 352,340 366,344 L 394,344 C 408,340 410,330 398,318",
        INK, 1.2, fill=SOFT),
      L(372, 286, 362, 324, INK, 1.0), L(388, 286, 398, 324, INK, 1.0),
      C(362, 326, 4, INK, 1.0, fill=PALE), C(398, 326, 4, INK, 1.0, fill=PALE),
      R(340, 344, 80, 7, WARM, 1.2, fill=PALE)]
# 门外之人
o += stand(206, 400, 74, INK, 1.1, arms="down") + stand(252, 404, 62, INK, 1.0, arms="down")
o += stand(548, 402, 70, INK, 1.1, arms="down") + stand(592, 404, 58, INK, 0.9, arms="down")
o.append(T(206, 420, "国人望门", 6.0, ZONG))
# 水纹外漫
o += [P("M 372,404 C 330,412 296,418 262,418", ZONG, 1.2, "none", "3,3"),
      P("M 376,414 C 336,422 302,428 272,428", ZONG, 1.0, "none", "3,3"),
      P("M 388,404 C 430,412 464,418 498,418", ZONG, 1.2, "none", "3,3"),
      P("M 384,414 C 424,422 458,428 488,428", ZONG, 1.0, "none", "3,3")]
o.append(T(300, 178, "巨室之所慕", 6.0, ZONG))
o += tail_(h, "巨室之所慕，一国慕之；沛然德教溢乎四海。", "图一", "巨室之门", "ch67a")
save("ch67a-jushi-zhi-men.svg", o)

# ---------------------------------------------------------- 68 执热而不以濯
h = 540
o = head_("执 热 而 不 以 濯", "《孟子》离娄上　第六十八章　MZ068", h)
o.append(T(380, 112, "谁能执热　逝不以濯", 6.2, GREY, ls=1))
# 火钳与炭
o += [L(196, 176, 292, 304, INK, 2.2), L(214, 186, 306, 292, INK, 2.2),
      P("M 196,176 C 200,164 212,164 214,186", INK, 1.3),
      L(292, 304, 300, 310, INK, 1.6), L(306, 292, 314, 298, INK, 1.6),
      L(180, 172, 196, 176, INK, 1.0)]
o += [P("M 288,298 L 308,288 L 324,300 L 318,320 L 298,324 L 286,312 Z", INK, 1.3, fill=ZHE)]
o += [L(296, 306, 312, 300, PALE, 0.8), L(300, 316, 314, 310, PALE, 0.8)]
o += [L(330, 302, 338, 300, ZHE, 0.9), L(330, 310, 338, 312, ZHE, 0.9),
      L(310, 282, 312, 274, ZHE, 0.9), L(298, 328, 296, 336, ZHE, 0.9)]
# 热气
o += [P("M 278,274 C 272,260 282,250 276,236", GREY, 1.1),
      P("M 294,272 C 290,258 300,248 296,234", GREY, 1.1),
      P("M 310,276 C 310,262 318,252 314,238", GREY, 1.1),
      P("M 324,282 C 326,268 334,260 330,246", GREY, 1.0)]
o.append(T(288, 232, "热", 7.2, ZHE))
o.append(T(228, 392, "执 热", 6.4, ZONG))
# 水盆
o += [E(520, 322, 82, 22, ZONG, 1.4, fill=SOFT), E(520, 322, 72, 16, ZONG, 0.9),
      P("M 450,318 C 480,324 560,324 590,318", WARM, 1.1),
      L(456, 344, 452, 392, WARM, 1.1), L(584, 344, 588, 392, WARM, 1.1)]
o.append(T(520, 306, "水", 7.4, ZONG))
o.append(T(520, 412, "就在手边　无人去用", 6.2, ZONG))
o += tail_(h, "欲无敌于天下而不以仁，是犹执热而不以濯也。", "图一", "执热而不以濯", "ch68a")
save("ch68a-zhire-buyizhuo.svg", o)

# ---------------------------------------------------------- 69 清斯濯缨 浊斯濯足
h = 540
o = head_("清 斯 濯 缨 · 浊 斯 濯 足", "《孟子》离娄上　第六十九章　MZ069", h)
o += [L(380, 100, 380, 424, LINE, 1)]
o += [T(200, 124, "清", 11, ZONG, ls=4), T(560, 124, "浊", 11, ZHE, ls=4)]
# 左：清水
o += [P("M 126,300 C 180,296 226,304 300,300", WARM, 1.3),
      P("M 300,300 L 300,340", LINE, 0.8),
      L(132, 316, 180, 314, ZONG, 0.8), L(206, 324, 252, 322, ZONG, 0.8),
      L(160, 334, 200, 332, ZONG, 0.8)]
# 缨
o += [L(240, 176, 240, 282, INK, 1.2),
      C(240, 288, 7.5, ZHE, 1.4, fill=SOFT),
      P("M 234,290 C 228,298 226,306 224,314", ZHE, 1.2),
      P("M 240,294 C 240,304 240,310 240,318", ZHE, 1.2),
      P("M 246,290 C 252,298 254,306 256,314", ZHE, 1.2),
      L(224, 314, 218, 322, ZHE, 0.9), L(240, 318, 236, 328, ZHE, 0.9),
      L(256, 314, 262, 322, ZHE, 0.9)]
o.append(T(268, 206, "濯缨", 7, ZHE, anchor="start"))
o.append(T(196, 372, "缨在头上　故用清水", 5.8, GREY))
# 右：浊水
o += [P("M 420,300 C 480,296 530,304 620,300", WARM, 1.3)]
for i in range(5):
    yy = 314 + i * 12
    o.append(P(f"M 430,{yy} C 470,{yy-5} 520,{yy+5} 600,{yy}", ZONG, 0.9))
for dx, dy in ((444, 310), (486, 326), (528, 318), (568, 336), (600, 308)):
    o.append(C(dx, dy, 1.6, ZONG, 0.8, fill=ZONG))
# 足
o += [L(540, 206, 540, 292, INK, 1.4),
      L(540, 292, 520, 302, INK, 1.3),
      L(520, 302, 562, 312, INK, 1.3),
      L(540, 292, 562, 312, INK, 1.3),
      L(536, 299, 554, 308, INK, 0.8), L(548, 304, 560, 311, INK, 0.8)]
o += [P("M 514,312 C 530,320 552,320 570,310", ZONG, 1.0, "none", "3,2")]
o.append(T(566, 200, "濯足", 7, ZONG, anchor="start"))
o.append(T(538, 372, "足在底下　故用浊水", 5.8, GREY))
o.append(T(380, 424, "水之清浊　有以自取之也", 6.2, ZONG))
o += tail_(h, "清斯濯缨，浊斯濯足矣，自取之也。", "图一", "清斯濯缨·浊斯濯足", "ch69a")
save("ch69a-qingying-zhuozu.svg", o)

# ---------------------------------------------------------- 70 三驱
h = 560
o = head_("三 驱", "《孟子》离娄上　第七十章　MZ070", h)
o += [L(296, 100, 296, 428, LINE, 1), L(468, 100, 468, 428, LINE, 1)]
o += [T(206, 118, "为渊驱鱼", 6.4, ZONG), T(382, 118, "为丛驱爵", 6.4, ZONG),
      T(556, 118, "为汤武驱民", 6.4, ZONG)]
# 左：渊与獭
o += [P("M 128,318 C 160,310 240,310 274,320 L 274,384 C 240,396 160,396 128,384 Z",
        ZONG, 1.2, fill=SOFT)]
o += [P("M 128,334 C 160,328 240,328 274,336", GREY, 0.8, "none", "4,3"),
      P("M 128,352 C 160,346 240,346 274,354", GREY, 0.8, "none", "4,3")]
for fx, fy in ((170, 358), (214, 368), (252, 352)):
    o += [E(fx, fy, 12, 5, INK, 1.0, fill=PALE),
          P(f"M {fx+11},{fy} L {fx+20},{fy-6} L {fx+20},{fy+6} Z", INK, 1.0, fill=PALE),
          C(fx - 8, fy - 2, 1.0, INK, 0.7, fill=INK)]
o += [E(152, 300, 24, 11, INK, 1.2, fill=PALE), C(126, 293, 8, INK, 1.2),
      P("M 122,290 L 112,286", INK, 0.9), P("M 122,295 L 112,296", INK, 0.9),
      P("M 176,296 C 190,290 196,278 194,268", INK, 1.1),
      L(148, 311, 146, 322, INK, 1.0), L(160, 311, 160, 322, INK, 1.0)]
o += arrow(190, 306, 222, 338, ZHE, 1.1, size=4)
o.append(T(206, 418, "獭 逐 鱼　鱼 入 渊", 6.0, ZONG))
# 中：丛与鹯
o += arrow(344, 292, 336, 344, ZHE, 0.9, size=3.4) + arrow(414, 292, 426, 348, ZHE, 0.9, size=3.4)
o += [P("M 314,398 L 314,318", ZONG, 1.6), P("M 336,400 L 336,308", ZONG, 1.6),
      P("M 358,398 L 358,316", ZONG, 1.6), P("M 380,400 L 380,306", ZONG, 1.6),
      P("M 402,398 L 402,314", ZONG, 1.6), P("M 424,400 L 424,310", ZONG, 1.6),
      P("M 446,398 L 446,322", ZONG, 1.6)]
for xx, yy in ((330, 362), (388, 354), (430, 366)):
    o += [E(xx, yy, 6.5, 3.6, INK, 1.0, fill=PALE), C(xx + 5, yy - 2.6, 1.9, INK, 0.9),
          P(f"M {xx},{yy} C {xx-4},{yy-8} {xx+2},{yy-9} {xx+3},{yy-4}", INK, 0.9),
          P(f"M {xx+5},{yy-1} L {xx+11},{yy-5} L {xx+11},{yy-1}", INK, 0.9)]
# 鹯
o += [P("M 372,258 C 356,238 334,240 328,254 L 344,266 Z", ZONG, 1.2, fill=SOFT),
      P("M 388,258 C 404,238 426,240 432,254 L 416,266 Z", ZONG, 1.2, fill=SOFT),
      E(380, 266, 10, 7, ZONG, 1.2, fill=SOFT), C(391, 260, 4.6, ZONG, 1.1),
      P("M 395,258 L 404,256 L 395,261", ZONG, 1.0),
      P("M 372,272 L 362,282 L 372,283", ZONG, 1.0)]
o += arrow(380, 284, 380, 320, ZHE, 1.1, size=4)
o.append(T(382, 418, "鹯 逐 雀　雀 入 丛", 6.0, ZONG))
# 右：民与桀纣
o += [L(622, 300, 622, 410, WARM, 1.8), P("M 622,300 L 648,308 L 622,316 Z", ZHE, 1.3, fill=SOFT)]
o.append(T(636, 288, "汤武", 6.4, ZHE))
o += [C(492, 300, 8.6, INK, 1.1), L(492, 309, 492, 350, INK, 1.2),
      L(492, 350, 486, 402, INK, 1.1), L(492, 350, 498, 402, INK, 1.1),
      L(492, 318, 510, 344, INK, 1.1)]
o += [L(502, 300, 514, 402, ZONG, 1.4)]
o.append(T(486, 284, "桀纣", 6.4, INK))
o += stand(548, 404, 74, INK, 1.2, arms="down") + stand(580, 406, 62, INK, 1.0, arms="down")
o += arrow(596, 384, 614, 384, ZHE, 1.1, size=4)
o.append(T(566, 420, "民 向 前 走", 6.0, ZONG))
o += tail_(h, "为汤武驱民者，桀与纣也。", "图一", "三驱", "ch70a")
save("ch70a-sanqu.svg", o)

# ---------------------------------------------------------- 71 旷安宅 舍正路
h = 540
o = head_("旷 安 宅 · 舍 正 路", "《孟子》离娄上　第七十一章　MZ071", h)
o.append(T(380, 112, "门开着　屋空着　路直着", 6.2, GREY, ls=1))
# 空宅
o += [P("M 138,254 L 196,196 L 254,254 Z", INK, 1.6, fill=SOFT),
      L(152, 254, 152, 384, INK, 1.4), L(240, 254, 240, 384, INK, 1.4),
      L(146, 384, 246, 384, WARM, 1.4)]
o += [R(184, 318, 26, 66, ZONG, 1.2, fill=PALE),
      L(210, 318, 228, 300, ZONG, 1.1), L(210, 384, 228, 366, ZONG, 1.1)]
o.append(T(196, 408, "旷 安 宅", 6.6, ZONG))
o.append(T(196, 424, "仁，人之安宅也", 5.8, GREY))
# 正路
o += [L(414, 400, 568, 240, INK, 1.4), L(506, 400, 592, 240, INK, 1.4)]
o += [L(448, 380, 466, 358, ZONG, 0.9, "4,3"), L(482, 340, 500, 320, ZONG, 0.9, "4,3"),
      L(516, 300, 534, 280, ZONG, 0.9, "4,3"), L(550, 260, 566, 242, ZONG, 0.9, "4,3")]
o.append(T(586, 228, "正 路", 6.6, ZONG))
# 弯径与草
o += [P("M 604,404 C 642,368 652,330 640,298", ZONG, 1.3, "none", "4,3")]
for i, (gx, gy) in enumerate(((614, 390), (620, 366), (627, 342), (634, 320))):
    o += [P(f"M {gx},{gy} l -6,-9", ZONG, 0.9), P(f"M {gx},{gy} l 4,-8", ZONG, 0.9)]
o.append(T(636, 428, "路 旁 生 草", 5.8, ZONG))
o += stand(596, 404, 80, INK, 1.2, arms="down")
o += tail_(h, "旷安宅而弗居，舍正路而不由，哀哉！", "图一", "旷安宅·舍正路", "ch71a")
save("ch71a-kuanganzhai.svg", o)
