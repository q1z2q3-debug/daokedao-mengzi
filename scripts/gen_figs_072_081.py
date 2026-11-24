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


# ---------------------------------------------------------- 72 在迩与求远
h = 540
o = head_("在 迩 与 求 远", "《孟子》离娄上　第七十二章　MZ072", h)
o += [L(380, 100, 380, 424, LINE, 1)]
o += [T(200, 122, "在 迩", 10, ZONG, ls=4), T(566, 122, "求 诸 远", 10, ZONG, ls=3)]
o += [L(110, 404, 320, 404, WARM, 1.4)]
o += [C(180, 292, 10, INK, 1.3), L(180, 302, 180, 374, INK, 1.4),
      L(180, 374, 166, 404, INK, 1.2), L(180, 374, 196, 404, INK, 1.2),
      L(180, 318, 214, 332, INK, 1.2), C(218, 333, 4.2, INK, 1.0, fill=SOFT)]
o += [C(266, 326, 7, ZHE, 1.2), L(266, 333, 266, 384, ZHE, 1.2),
      L(266, 384, 256, 404, ZHE, 1.0), L(266, 384, 276, 404, ZHE, 1.0),
      L(266, 346, 240, 334, ZHE, 1.0), C(236, 333, 3.6, ZHE, 0.9, fill=SOFT)]
o += [L(222, 333, 234, 333, INK, 0.9)]
o += [T(196, 272, "亲其亲", 6.4, ZONG), L(214, 276, 226, 326, LINE, 0.8)]
o += [T(150, 424, "三步之内", 5.8, GREY, anchor="start")]
o += [L(136, 404, 136, 396, GREY, 0.8), L(166, 404, 166, 396, GREY, 0.8), L(196, 404, 196, 396, GREY, 0.8)]
o += [P("M 420,404 L 462,366 L 500,384 L 540,340 L 584,358 L 626,316 L 650,352", ZONG, 1.2)]
o += [P("M 654,404 L 706,404 L 682,318 Z", ZONG, 1.2, fill=SOFT)]
o += [L(420, 404, 700, 404, WARM, 1.3)]
o += [C(470, 292, 9.4, INK, 1.3), L(470, 301, 470, 372, INK, 1.4),
      L(470, 372, 456, 404, INK, 1.2), L(470, 372, 484, 404, INK, 1.2),
      L(470, 316, 452, 330, INK, 1.2), L(470, 316, 488, 332, INK, 1.2)]
o += [C(444, 352, 10, ZONG, 1.2, fill=SOFT), L(470, 318, 450, 344, ZONG, 0.9)]
o += [T(432, 366, "行囊", 6.0, ZONG, anchor="end")]
o += [T(560, 424, "路画得越长，越像在做事", 5.8, GREY)]
o += tail_(h, "道在尔而求诸远，事在易而求之难。", "图一", "在迩与求远", "ch72a")
save("ch72a-zaier-qiuquan.svg", o)

# ---------------------------------------------------------- 73 五级台阶
h = 540
o = head_("五 级 台 阶", "《孟子》离娄上　第七十三章　MZ073", h)
o.append(T(380, 112, "获上 → 信友 → 悦亲 → 诚身 → 明善", 6.6, GREY, ls=1))
steps = [(296, 388, "明善"), (356, 364, "诚身"), (416, 340, "悦亲"), (476, 316, "信友"), (536, 292, "获上")]
for xx, yy, name in steps:
    o += [R(xx, yy, 72, 24, ZONG, 1.0, fill=SOFT),
          L(xx, yy, xx, 422, ZONG, 0.8),
          T(xx + 36, yy + 17, name, 7.2, INK)]
o += [L(296, 422, 608, 422, WARM, 1.4)]
o += [R(200, 246, 60, 176, ZONG, 1.2, fill=SOFT), P("M 200,246 C 218,230 242,230 260,246", ZONG, 1.2)]
o += [T(230, 324, "诚", 24, ZHE, weight="700"), T(230, 350, "实也", 6.2, GREY)]
o += stand(658, 422, 112, INK, 1.2, arms="down")
o += [T(658, 440, "在下位者", 6.2, ZONG)]
o += tail_(h, "诚者，天之道也；思诚者，人之道也。", "图一", "五级台阶", "ch73a")
save("ch73a-wuji-taijie.svg", o)

# ---------------------------------------------------------- 74 二老归周
h = 560
o = head_("二 老 归 周", "《孟子》离娄上　第七十四章　MZ074", h)
o += [T(180, 116, "北 海 之 滨", 8, ZONG, ls=3), T(580, 116, "东 海 之 滨", 8, ZONG, ls=3)]
o += [P("M 96,398 C 140,392 200,392 244,398", ZONG, 1.3)]
for i in range(3):
    yy = 412 + i * 11
    o.append(P(f"M 104,{yy} C 140,{yy-4} 200,{yy+4} 238,{yy}", GREY, 0.7, "none", "4,3"))
o += oldman(176, 396, 104)
o += [T(176, 268, "伯夷", 6.4, INK)]
o += [P("M 516,398 C 560,392 620,392 664,398", ZONG, 1.3)]
for i in range(3):
    yy = 412 + i * 11
    o.append(P(f"M 522,{yy} C 560,{yy-4} 620,{yy+4} 656,{yy}", GREY, 0.7, "none", "4,3"))
o += oldman(594, 396, 104)
o += [T(594, 268, "太公", 6.4, INK)]
o += [L(330, 214, 330, 404, INK, 2.0), L(430, 214, 430, 404, INK, 2.0),
      R(318, 200, 124, 14, ZONG, 1.2, fill=SOFT), L(322, 404, 438, 404, WARM, 1.6)]
o += [R(336, 318, 84, 10, WARM, 1.3, fill=SOFT),
      L(350, 328, 350, 372, WARM, 1.0), L(406, 328, 406, 372, WARM, 1.0),
      E(354, 300, 9, 6, WARM, 1.1, fill=SOFT), R(351, 288, 6, 7, WARM, 1.0),
      P("M 360,296 C 366,294 367,288 364,283", WARM, 0.9),
      E(392, 306, 20, 8, WARM, 1.1, fill=SOFT),
      P("M 374,304 C 382,296 402,296 410,304", ZONG, 1.0, fill=SOFT)]
o += [T(380, 190, "西伯之政　先及鳏寡", 6.2, ZONG)]
o += arrow(240, 352, 312, 302, ZHE, 1.1, size=4.6) + arrow(530, 352, 452, 302, ZHE, 1.1, size=4.6)
o += [T(380, 428, "父归，则子焉往", 6.4, GREY)]
o += tail_(h, "天下之父归之，其子焉往？", "图一", "二老归周", "ch74a")
save("ch74a-erlao-guizhou.svg", o)

# ---------------------------------------------------------- 75 一面鼓，两只斗
h = 540
o = head_("一 面 鼓 · 两 只 斗", "《孟子》离娄上　第七十五章　MZ075", h)
o.append(T(380, 112, "赋粟倍他日", 6.4, GREY, ls=1))
o += [L(96, 404, 620, 404, LINE, 1.1)]
o += ['  <g transform="translate(0,40)">',
      E(184, 244, 54, 15, INK, 1.4, fill=SOFT), L(130, 244, 130, 348, INK, 1.3),
      L(238, 244, 238, 348, INK, 1.3), E(184, 348, 54, 15, INK, 1.4, fill=SOFT),
      L(184, 250, 184, 344, GREY, 0.8, "4,3"), '</g>']
o += [L(258, 398, 300, 396, WARM, 2.2), C(306, 395, 4.6, WARM, 1.0, fill=SOFT), T(300, 386, "槌", 5.8, WARM)]
o += [T(184, 266, "鼓", 7.4, ZONG), T(184, 424, "鸣鼓而攻", 6.0, GREY)]
o += dou(318, 320, 86, 76)
o += [P("M 320,326 L 402,326 L 388,390 L 334,390 Z", ZONG, 0.1, fill=SOFT), L(318, 326, 404, 326, ZONG, 1.2)]
for dx in (336, 356, 376, 392):
    o.append(C(dx, 334, 1.8, ZONG, 0.7, fill=ZONG))
o += [T(361, 312, "平", 6.4, ZONG), T(361, 412, "旧日之数", 5.8, ZONG)]
o += dou(468, 320, 86, 76)
o += [P("M 468,324 C 496,306 526,306 554,324", ZHE, 1.3, fill=SOFT), L(468, 324, 554, 324, ZHE, 1.2)]
for dx, dy in ((460, 308), (480, 300), (502, 306)):
    o.append(C(dx, dy, 1.9, ZHE, 0.7, fill=ZHE))
o += [T(511, 292, "溢", 7.0, ZHE), T(511, 412, "倍他日", 5.8, ZHE)]
o += tail_(h, "君不行仁政而富之，皆弃于孔子者也。", "图一", "一面鼓·两只斗", "ch75a")
save("ch75a-guo-liangdou.svg", o)

# ---------------------------------------------------------- 76 了与眊
h = 540
o = head_("了 与 眊", "《孟子》离娄上　第七十六章　MZ076", h)
o += [L(380, 100, 380, 424, LINE, 1)]
o += [T(200, 124, "胸 中 正", 9.4, ZONG, ls=4), T(566, 124, "胸 中 不 正", 9.4, ZHE, ls=3)]
o += [P("M 132,258 C 156,220 244,220 268,258", INK, 1.5),
      P("M 268,258 C 244,294 156,294 132,258", INK, 1.5)]
o += [C(200, 258, 26, ZONG, 1.2), C(200, 258, 11, INK, 1.2, fill=INK),
      C(193, 251, 3.6, PALE, 0.6, fill=PALE)]
o += [T(200, 316, "了", 9.4, ZONG, ls=2)]
o += [P("M 492,258 C 516,220 604,220 628,258", INK, 1.5),
      P("M 628,258 C 604,294 516,294 492,258", INK, 1.5)]
o += [C(560, 258, 25, GREY, 0.8), C(560, 258, 17, GREY, 0.6),
      C(560, 258, 11, ZONG, 1.1, fill=GREY)]
for a in range(0, 360, 45):
    x1 = 560 + 30 * math.cos(math.radians(a)); y1 = 258 + 30 * math.sin(math.radians(a))
    x2 = 560 + 36 * math.cos(math.radians(a)); y2 = 258 + 36 * math.sin(math.radians(a))
    o.append(L(f"{x1:.1f}", f"{y1:.1f}", f"{x2:.1f}", f"{y2:.1f}", GREY, 0.7))
o += [T(560, 316, "眊", 9.4, ZHE, ls=2)]
o += [R(120, 350, 160, 28, WARM, 1.0, fill=PALE), C(120, 364, 6, WARM, 1.0, fill=SOFT),
      C(280, 364, 6, WARM, 1.0, fill=SOFT)]
o += [L(138, 360, 262, 360, GREY, 0.6, "6,3"), L(138, 368, 246, 368, GREY, 0.6, "6,3")]
o += [R(480, 350, 160, 28, WARM, 1.0, fill=PALE), C(480, 364, 6, WARM, 1.0, fill=SOFT),
      C(640, 364, 6, WARM, 1.0, fill=SOFT)]
o += [L(498, 360, 622, 360, GREY, 0.6, "6,3"), L(498, 368, 606, 368, GREY, 0.6, "6,3")]
o += [T(200, 400, "听其言", 6.2, ZONG), T(560, 400, "听其言", 6.2, GREY)]
o += [T(380, 428, "言可伪，目不容伪", 6.2, GREY)]
o += tail_(h, "听其言也，观其眸子，人焉廋哉？", "图一", "了与眊", "ch76a")
save("ch76a-liao-yumao.svg", o)

# ---------------------------------------------------------- 77 垂手与推礼
h = 540
o = head_("垂 手 与 推 礼", "《孟子》离娄上　第七十七章　MZ077", h)
o += [L(380, 100, 380, 424, LINE, 1)]
o += [T(200, 124, "恭 者 不 侮 人", 8.6, ZONG, ls=2), T(566, 124, "俭 者 不 夺 人", 8.6, ZONG, ls=2)]
for cx in (156, 250):
    o += [C(cx, 264, 9.4, INK, 1.3), L(cx, 273, cx, 344, INK, 1.4),
          L(cx, 344, cx - 11, 388, INK, 1.1), L(cx, 344, cx + 11, 388, INK, 1.1)]
    o += [L(cx, 286, cx - 16, 338, INK, 1.1), L(cx, 286, cx + 16, 338, INK, 1.1),
          C(cx - 16, 341, 3.2, INK, 0.9, fill=SOFT), C(cx + 16, 341, 3.2, INK, 0.9, fill=SOFT)]
o += [L(150, 388, 256, 388, WARM, 1.2)]
o += [L(196, 320, 210, 320, GREY, 1.0, "4,3"), T(203, 338, "空", 5.8, GREY)]
o += [T(203, 410, "手垂而不侵", 5.8, GREY)]
o += [R(492, 300, 76, 52, ZONG, 1.3, fill=SOFT), L(492, 318, 568, 318, ZONG, 0.9), L(492, 334, 568, 334, ZONG, 0.9)]
o += [P("M 492,300 L 530,282 L 568,300", ZONG, 1.1)]
o += [L(690, 240, 646, 284, INK, 1.3), L(646, 284, 566, 304, INK, 1.3),
      R(556, 298, 22, 14, INK, 1.0, fill=SOFT)]
o += [L(556, 302, 546, 300, INK, 0.7), L(556, 306, 546, 306, INK, 0.7), L(556, 310, 547, 312, INK, 0.7)]
o += arrow(556, 356, 470, 356, ZHE, 1.2, size=4.4)
o += [T(512, 376, "推 回 去", 6.2, ZHE)]
o += [T(652, 268, "递 来", 5.8, ZONG, anchor="start")]
o += [T(540, 410, "不取别人手里的", 5.8, GREY)]
o += [T(380, 430, "声音笑貌，伪为于外", 6.2, GREY)]
o += tail_(h, "恭者不侮人，俭者不夺人。", "图一", "垂手与推礼", "ch77a")
save("ch77a-chuishou-tuili.svg", o)

# ---------------------------------------------------------- 78 手与秤
h = 540
o = head_("手 与 秤", "《孟子》离娄上　第七十八章　MZ078", h)
o.append(T(380, 112, "嫂溺援之以手　天下溺援之以道", 6.4, GREY, ls=1))
o += [L(80, 404, 240, 404, WARM, 1.4)]
o += [R(236, 348, 176, 56, ZONG, 0.1, fill=SOFT), P("M 236,348 C 290,342 360,354 412,348", ZONG, 1.3)]
for i in range(3):
    yy = 364 + i * 13
    o.append(P(f"M 250,{yy} C 290,{yy-5} 356,{yy+5} 400,{yy}", GREY, 0.8, "none", "4,3"))
o += [T(96, 344, "岸 上", 6.2, ZONG, anchor="start")]
o += [C(126, 286, 9.4, INK, 1.3), L(126, 295, 126, 360, INK, 1.4),
      P("M 126,312 C 170,330 214,344 246,352", INK, 1.4),
      L(126, 360, 112, 404, INK, 1.2), L(126, 360, 140, 404, INK, 1.2)]
o += [E(252, 354, 9, 4.6, INK, 1.1, fill=SOFT), L(252, 352, 246, 347, INK, 0.7)]
o += [T(196, 288, "岸上之手", 5.8, ZONG)]
o += [L(352, 404, 354, 356, INK, 1.3), E(354, 350, 9, 4.6, INK, 1.1, fill=SOFT)]
o += [L(351, 346, 351, 340, INK, 0.7), L(354, 345, 354, 339, INK, 0.7), L(357, 346, 357, 340, INK, 0.7)]
o += [P("M 336,352 C 344,346 366,346 372,352", GREY, 0.8)]
o += [T(392, 330, "水中之手", 5.8, ZHE, anchor="start")]
o += [L(500, 200, 700, 200, ZONG, 1.6), C(500, 200, 4, ZONG, 1.0, fill=INK)]
o += [L(700, 200, 700, 230, WARM, 1.0), R(684, 230, 32, 22, WARM, 1.1, fill=SOFT), T(700, 276, "物", 6.2, WARM)]
o += [L(600, 200, 600, 238, WARM, 1.0), P("M 588,238 L 612,238 L 606,272 L 594,272 Z", ZHE, 1.2, fill=SOFT)]
o += [T(600, 288, "权", 8.4, ZHE, ls=2)]
o += [L(556, 196, 656, 196, GREY, 0.8, "3,3")]
o += [T(606, 182, "权而得中", 6.2, ZONG)]
o += [T(600, 330, "称过轻重　才取这一点", 5.8, GREY)]
o += tail_(h, "嫂溺援之以手者，权也。", "图一", "手与秤", "ch78a")
save("ch78a-shou-yucheng.svg", o)

# ---------------------------------------------------------- 79 易子而教
h = 540
o = head_("易 子 而 教", "《孟子》离娄上　第七十九章　MZ079", h)
o.append(T(380, 112, "势不行也", 6.6, GREY, ls=1))
o += house(196, 392, 108, 80)
o += house(564, 392, 108, 80)
o += [L(120, 392, 300, 392, WARM, 1.2), L(460, 392, 640, 392, WARM, 1.2)]
o += stand(196, 392, 52, ZONG, 1.0, arms="down")
o += stand(564, 392, 52, ZONG, 1.0, arms="down")
o += [T(196, 412, "此家之子", 5.8, ZONG), T(564, 412, "彼家之子", 5.8, ZONG)]
o += [L(228, 334, 536, 354, ZHE, 1.2, "4,3"), L(532, 334, 232, 354, ZHE, 1.0, "4,3")]
o += [P("M 540,350 L 528,344 L 530,354 Z", ZHE, 0.9, fill=ZHE),
      P("M 232,358 L 244,352 L 242,364 Z", ZHE, 0.8, fill=ZHE)]
o += [T(380, 300, "互 换 而 教", 7.0, ZHE, ls=2)]
o += shoe(112, 392) + shoe(170, 392)
o += shoe(542, 392) + shoe(600, 392)
o += [T(380, 424, "鞋留下，人走开", 5.8, GREY)]
o += tail_(h, "父子之间不责善。责善则离，离则不祥莫大焉。", "图一", "易子而教", "ch79a")
save("ch79a-yizi-erjiao.svg", o)

# ---------------------------------------------------------- 80 撤席的一问
h = 540
o = head_("撤 席 的 一 问", "《孟子》离娄上　第八十章　MZ080", h)
o.append(T(380, 112, "将彻，必请所与", 6.4, GREY, ls=1))
o += [L(556, 176, 556, 396, LINE, 2.0), L(700, 176, 700, 396, LINE, 2.0), L(550, 176, 706, 176, LINE, 2.2)]
o += [L(700, 176, 664, 396, LINE, 1.4), C(672, 290, 3, ZONG, 0.8, fill=ZONG)]
o += [C(616, 264, 9, GREY, 1.0, fill=SOFT),
      P("M 616,273 C 604,292 600,320 602,352 L 630,352 C 632,320 628,292 616,273 Z", GREY, 0.9),
      L(608, 296, 592, 330, GREY, 0.9), L(624, 296, 638, 328, GREY, 0.9),
      L(606, 352, 600, 396, GREY, 0.9), L(626, 352, 632, 396, GREY, 0.9)]
o += [T(612, 424, "门 外 之 谁", 5.8, GREY)]
o += [R(250, 330, 190, 12, WARM, 1.3, fill=SOFT),
      L(266, 342, 266, 396, WARM, 1.1), L(424, 342, 424, 396, WARM, 1.1)]
o += [E(300, 314, 17, 10, ZONG, 1.2, fill=SOFT), R(296, 296, 8, 10, ZONG, 1.1),
      P("M 304,306 C 314,304 316,296 312,290", ZONG, 1.0),
      P("M 292,300 C 284,300 282,310 288,312", ZONG, 1.0)]
o += [E(360, 326, 27, 9, ZONG, 1.2, fill=SOFT), E(360, 322, 12, 5, ZHE, 1.0, fill=ZHE)]
o += [E(410, 324, 11, 5, ZONG, 1.0, fill=PALE), P("M 399,324 C 395,320 395,328 401,326", ZONG, 0.8),
      P("M 421,324 C 425,320 425,328 419,326", ZONG, 0.8)]
o += [L(446, 300, 496, 310, INK, 1.4), E(504, 314, 11, 5, INK, 1.1, fill=SOFT)]
o += [L(500, 318, 498, 323, INK, 0.7), L(505, 319, 504, 324, INK, 0.7), L(510, 318, 511, 323, INK, 0.7)]
o += [E(522, 306, 24, 8, ZONG, 1.1, fill=SOFT), E(522, 302, 9, 4, ZHE, 0.9, fill=ZHE)]
o += [T(524, 338, "余 食 外 递", 6.0, ZHE), L(516, 342, 508, 318, LINE, 0.8)]
o += oldman(190, 396, 106)
o += [T(190, 420, "曾皙", 6.2, INK)]
o += shoe(352, 404) + shoe(416, 404)
o += [T(412, 424, "鞋尖朝外", 5.8, GREY)]
o += tail_(h, "事亲若曾子者，可也。", "图一", "撤席的一问", "ch80a")
save("ch80a-chexi-yiwen.svg", o)

# ---------------------------------------------------------- 81 格心
h = 540
o = head_("格 心", "《孟子》离娄上　第八十一章　MZ081", h)
o.append(T(380, 112, "惟大人为能格君心之非", 6.6, GREY, ls=1))
o += [P("M 400,388 C 348,348 316,318 316,288 C 316,264 334,246 358,246 "
        "C 376,246 392,256 400,274 C 408,256 424,246 442,246 C 466,246 484,264 484,288 "
        "C 484,318 452,348 400,388 Z", INK, 1.5, fill=SOFT)]
o += [L(400, 250, 400, 384, GREY, 0.9, "5,4")]
o += [L(404, 282, 464, 282, ZHE, 3.0), L(404, 282, 404, 340, ZHE, 3.0),
      L(404, 292, 454, 292, ZHE, 0.9), L(414, 282, 414, 332, ZHE, 0.9)]
o += [T(486, 272, "格", 11, ZHE, ls=2, anchor="start")]
o += [T(504, 300, "物之所取正", 5.6, ZONG, anchor="start")]
o += [R(150, 262, 96, 58, ZONG, 1.1, fill=PALE), R(150, 336, 96, 58, ZONG, 1.1, fill=PALE)]
o += [T(198, 296, "用人", 7.0, GREY, ls=2), T(198, 370, "行政", 7.0, GREY, ls=2)]
o += arrow(264, 290, 226, 290, GREY, 0.9, size=4.0) + arrow(264, 366, 226, 366, GREY, 0.9, size=4.0)
o += [T(198, 424, "不足与适　不足间", 5.8, GREY)]
o += tail_(h, "一正君而国定矣。", "图一", "格心", "ch81a")
save("ch81a-gexin.svg", o)
