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
"""尽心下 图 165–172（v0.34.0 收尾八图，全书末批）
跨批 helper 不复用：本文件内重定义 tail_（卷名尽心下）/palhand/hoeblade。
"""

H = 540


def tail_(h, q, label, name, key):
    return [
        L(120, h - 104, 640, h - 104, LINE, 1),
        T(380, h - 80, q, 8.6, INK, ls=2),
        f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 尽心下</text>',
        f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>',
    ]


def palhand(x, y, sgn=1, col=ZONG, sw=1.2):
    """停在半空的手掌：掌面＋两指（sgn=1 指向下）。"""
    o = [P(f"M {x-9},{y} L {x+3},{y} L {x+3},{y+sgn*9} L {x-9},{y+sgn*9} Z", col, sw, SOFT)]
    for i in range(2):
        o += [L(x - 6 + i * 6, y + sgn * 9, x - 5 + i * 6, y + sgn * 17, col, sw * 0.9)]
    return o


def hoeblade(x, y, col=WARM):
    """锄刃：手柄尽头一枚厚短刃。"""
    return [L(x - 2, y - 11, x + 2, y + 11, col, 3.4),
            L(x - 2, y - 11, x + 2, y - 11, col, 1.0)]


def jian(x, y, w=96, hh=26, n=7, col=ZONG, sw=0.9):
    """简册一捆：n 枚窄简并排，两道编绳。"""
    o = []
    step = w / float(n - 1)
    for i in range(n):
        xx = x + i * step
        o += [L(xx, y, xx, y + hh, col, sw)]
    o += [L(x - 3, y + 7, x + w + 3, y + 7, WARM, 0.8),
          L(x - 3, y + hh - 7, x + w + 3, y + hh - 7, WARM, 0.8)]
    o += [L(x - 3, y - 1, x + w + 3, y - 1, ZONG, 1.1),
          L(x - 3, y + hh + 1, x + w + 3, y + hh + 1, ZONG, 1.1)]
    return o


def roll(x, y, w=90, hh=24, col=ZONG, sw=1.0):
    """横放的一卷：两端圆卷，中段两道束带，右端一枚卷头。"""
    cy = y + hh / 2.0
    return [E(x, cy, 5.2, hh / 2.0, col, sw, SOFT), E(x + w, cy, 5.2, hh / 2.0, col, sw, SOFT),
            L(x, y, x + w, y, col, sw), L(x, y + hh, x + w, y + hh, col, sw),
            L(x + w * 0.34, y, x + w * 0.34, y + hh, WARM, 0.8),
            L(x + w * 0.62, y, x + w * 0.62, y + hh, WARM, 0.8),
            P(f"M {x+w},{cy} C {x+w+4},{cy-5} {x+w+7},{cy+4} {x+w+4},{cy+6}", col, sw * 0.9)]


# ---------------------------------------------------------- 165 人皆有所不忍
o = head_("人 皆 有 所 不 忍", "《孟子》尽心下　第二百五十四章　MZ254", H)
o += [T(380, 112, "人皆有所不忍，达之于其所忍，仁也", 5.6, ZONG, ls=1.0)]
# 竖直界线
o += [L(380, 130, 380, 306, GREY, 0.9, "5,5")]
# 左小圈：不忍
o += [C(264, 196, 44, ZONG, 1.4, SOFT)]
o += [T(264, 200, "不忍", 6.6, INK, ls=1.5)]
o += [T(264, 152, "人人本有", 4.6, WARM, ls=0.5)]
# 右大圈：不忍所忍
o += [C(500, 196, 78, ZHE, 1.4, PALE)]
o += [T(500, 190, "不忍", 5.6, ZONG, ls=1)]
o += [T(500, 206, "所忍", 5.6, ZONG, ls=1)]
o += [T(500, 132, "达 · 推而广之", 4.8, ZHE, ls=1)]
# 推箭
o += arrow(314, 196, 416, 196, ZHE, 1.3, 6)
o += [T(366, 182, "达", 5.4, ZHE, ls=1)]
# 下方：墙·洞·越墙之人
for x0, x1 in ((210, 330), (396, 560)):
    o += [P(f"M {x0},356 L {x1},356 L {x1},376 L {x0},376 Z", ZONG, 1.2, SOFT)]
for x in range(220, 330, 24):
    o += [L(x, 358, x, 374, GREY, 0.5)]
for x in range(404, 560, 24):
    o += [L(x, 358, x, 374, GREY, 0.5)]
o += [L(330, 352, 330, 380, ZONG, 1.6), L(396, 352, 396, 380, ZONG, 1.6)]
o += [T(240, 344, "墙", 4.8, ZONG, ls=1), T(414, 344, "洞", 4.4, ZHE, ls=1)]
# 越墙者：身过洞，腿一内一外
o += [C(363, 334, 7.4, INK, 1.1)]
o += [L(363, 342, 363, 368, INK, 1.3)]
o += [L(363, 350, 351, 342, INK, 1.0), L(363, 350, 375, 342, INK, 1.0)]
o += [L(363, 368, 351, 392, INK, 1.1), L(363, 368, 373, 392, INK, 1.1)]
o += [T(363, 418, "逾", 4.6, WARM, ls=1)]
o += [T(500, 418, "穿逾之类，亦是探", 4.8, ZONG, ls=0.6)]
o += tail_(H, "仁只是一个推字；推不到处，正是所忍处。", "图一百六十五", "人皆有所不忍", "ch254a")
save("ch254a-chong-wu-chuan-yu.svg", o)

# ---------------------------------------------------------- 166 言近而指远
o = head_("言 近 而 指 远", "《孟子》尽心下　第二百五十五章　MZ255", H)
o += [T(380, 112, "言近而指远者，善言也；守约而施博者，善道也", 5.4, ZONG, ls=0.8)]
# 腰带：两道横线＋带钩
o += [L(148, 160, 452, 160, ZONG, 2.2), L(148, 169, 452, 169, ZONG, 1.0)]
o += [R(286, 156, 26, 17, ZONG, 1.0, SOFT), L(292, 164, 306, 164, GREY, 0.6)]
# 带上一捆简
o += roll(186, 118, 92, 26)
o += [T(232, 112, "约 · 目前近事", 4.6, ZONG, ls=0.5)]
# 长箭指向至理
o += arrow(292, 134, 628, 152, ZHE, 1.2, 6)
o += [T(660, 152, "至 理", 8.0, ZHE, ls=3)]
o += [T(380, 178, "不下带而道存焉", 4.8, WARM, ls=1.2)]
# 下：两田（左荒·右锄）
o += [L(148, 300, 322, 300, ZONG, 1.4), L(148, 372, 322, 372, ZONG, 1.0)]

for yy in (312, 324, 336, 348, 360):
    o += [L(154, yy, 318, yy, ZONG, 0.8)]
o += [L(430, 300, 606, 300, ZONG, 1.4), L(430, 372, 606, 372, ZONG, 1.0)]

for yy in (312, 324, 336, 348, 360):
    o += [L(436, yy, 600, yy, ZONG, 0.8)]
o += [T(235, 392, "己田 · 荒", 5.0, ZONG, ls=1)]
o += [T(518, 392, "人田", 5.0, ZONG, ls=1)]
# 左田生草
for x, y0, y1 in ((170, 306, 296), (200, 318, 306), (228, 330, 320), (258, 342, 332),
                  (284, 354, 344), (196, 342, 332), (250, 366, 356), (300, 318, 308)):
    o += [P(f"M {x},{y0} C {x-3},{y0-4} {x-2},{y1+2} {x+1},{y1}", ZONG, 0.9)]
    o += [P(f"M {x},{y0} C {x+4},{y0-3} {x+4},{y1+3} {x+5},{y1+1}", ZONG, 0.8)]
# 锄者立在左田边，锄头伸向右田
o += [C(374, 296, 8.2, INK, 1.1)]
o += [L(374, 304, 374, 350, INK, 1.3)]
o += [L(374, 350, 364, 404, INK, 1.1), L(374, 350, 384, 404, INK, 1.1)]
o += [L(374, 316, 360, 344, INK, 1.0), L(374, 316, 392, 330, INK, 1.0)]
o += [L(392, 330, 470, 352, ZONG, 1.7)]
o += [L(466, 338, 476, 368, WARM, 3.6), L(466, 338, 470, 336, WARM, 1.0)]
o += [T(374, 424, "舍己田而芸人田", 5.4, ZHE, ls=0.8)]
o += [T(360, 288, "守约", 4.6, ZONG, ls=1)]
o += tail_(H, "所求于人者重，所以自任者轻。", "图一百六十六", "言近而指远", "ch255a")
save("ch255a-yan-jin-zhi-yuan.svg", o)

# ---------------------------------------------------------- 167 尧舜性者也
o = head_("尧 舜 性 者 也", "《孟子》尽心下　第二百五十六章　MZ256", H)
o += [T(380, 112, "性之与反之，及其成功则一也", 5.8, ZONG, ls=1.2)]
o += [T(330, 130, "天", 9.4, INK, ls=3)]
# 性者：一条直线，由天直落
o += [L(330, 146, 330, 348, ZONG, 1.9)]
# 反之：下行，中途一顿而折，再入同一个圣
o += [L(352, 152, 502, 300, ZONG, 1.5)]
o += [L(502, 300, 452, 336, ZONG, 1.5)]
o += [L(452, 336, 348, 362, ZONG, 1.5)]
o += [T(316, 250, "性者·尧舜", 5.2, WARM, anchor="end", ls=0.8)]
o += [T(300, 190, "得全于天", 4.6, ZONG, anchor="end", ls=1.0)]
o += [T(518, 268, "反之·汤武", 5.2, WARM, anchor="start", ls=0.8)]
o += [T(510, 316, "折", 5.0, ZHE, anchor="start", ls=1)]
o += [T(518, 232, "修为以复其性", 4.6, ZONG, anchor="start", ls=0.4)]
o += [C(330, 368, 19, ZHE, 1.3, SOFT)]
o += [T(330, 373, "圣", 9.4, ZHE, ls=1)]
o += [T(380, 420, "性者无意而安行，反者有意利行而至于无意", 5.8, INK, ls=0.9)]
o += tail_(H, "两路不同，到头是一个圣。", "图一百六十七", "尧舜性者也", "ch256a")
save("ch256a-xing-zhi-fan-zhi.svg", o)

# ---------------------------------------------------------- 168 说大人则藐之
o = head_("说 大 人 则 藐 之", "《孟子》尽心下　第二百五十七章　MZ257", H)
o += [T(380, 112, "堂高数仞，食前方丈，后车千乘：皆我所不为", 5.4, ZONG, ls=0.8)]
# 三重檐高堂（右上）
cx = 540
o += [L(410, 336, 674, 336, ZONG, 1.8), L(410, 348, 674, 348, ZONG, 1.2)]
for x in (420, 470, 540, 610, 664):
    o += [L(x, 336, x, 348, GREY, 0.7)]
for yy, ww in ((208, 92), (256, 104), (302, 116)):
    o += [P(f"M {cx-ww+14},{yy} L {cx+ww-14},{yy} L {cx+ww},{yy+15} "
           f"L {cx+ww*0.62},{yy+21} L {cx-ww*0.62},{yy+21} L {cx-ww},{yy+15} Z",
           ZONG, 1.3, SOFT)]
    o += [L(cx - ww + 14, yy, cx + ww - 14, yy, ZONG, 1.6)]
    o += [L(cx - ww * 0.48, yy + 21, cx - ww * 0.48, yy + 46, ZONG, 1.0),
          L(cx + ww * 0.48, yy + 21, cx + ww * 0.48, yy + 46, ZONG, 1.0)]
o += [P(f"M {cx-58},208 L {cx},184 L {cx+58},208", ZONG, 1.6)]
for yy, ww in ((208, 92), (256, 104), (302, 116)):
    o += [P(f"M {cx+ww},{yy+15} C {cx+ww+8},{yy+9} {cx+ww+12},{yy+4} {cx+ww+17},{yy-1}", ZONG, 1.1),
          P(f"M {cx-ww},{yy+15} C {cx-ww-8},{yy+9} {cx-ww-12},{yy+4} {cx-ww-17},{yy-1}", ZONG, 1.1)]
o += [T(540, 178, "堂高数仞", 4.6, WARM, ls=0.8)]
# 三列排场
o += [R(228, 362, 46, 8, ZONG, 1.0, SOFT)]
for dx in (8, 22, 36):
    o += [C(228 + dx, 360, 3.4, ZONG, 0.8, ZONG)]
o += [T(251, 386, "食前方丈", 4.4, WARM, ls=0.2)]
# 后车：车身＋两轮＋辕
o += [P("M 344,356 L 386,356 L 392,374 L 338,374 Z", ZONG, 1.2, SOFT)]
o += [C(352, 380, 8.2, ZONG, 1.1), C(382, 380, 8.2, ZONG, 1.1)]
o += [L(392, 362, 424, 356, ZONG, 1.4)]
o += [T(368, 400, "后车千乘", 4.4, WARM, ls=0.2)]
# 乐人二
o += [stand(644, 396, 52, ZONG, 1.0), stand(676, 396, 52, ZONG, 1.0)]
o += [T(660, 414, "般乐", 4.4, WARM, ls=0.6)]
# 堂下之人：仰而不俯，持一卷简
o += [stand(180, 404, 120, INK, 1.3)]
o += roll(196, 322, 54, 20)
o += [T(226, 354, "古之制", 4.8, ZHE, anchor="start", ls=0.6)]
o += [L(180, 318, 192, 330, INK, 0.9)]
o += [T(380, 420, "在彼者皆我所不为，在我者皆古之制", 5.6, INK, ls=0.9)]
o += tail_(H, "他有三样我不要的东西，我有一件他没有的东西。", "图一百六十八", "说大人则藐之", "ch257a")
save("ch257a-shuo-daren-ze-miao-zhi.svg", o)

# ---------------------------------------------------------- 169 养心莫善于寡欲
o = head_("养 心 莫 善 于 寡 欲", "《孟子》尽心下　第二百五十八章　MZ258", H)
o += [T(380, 112, "其为人也寡欲，虽有不存焉者，寡矣", 5.4, ZONG, ls=0.8)]
ecx, ecy, er = 380, 246, 78
a1, a2 = math.radians(20), math.radians(-20)
p1 = (ecx + er * math.cos(a1), ecy + er * math.sin(a1))
p2 = (ecx + er * math.cos(a2), ecy + er * math.sin(a2))
o += [P(f"M {p1[0]:.1f},{p1[1]:.1f} A {er},{er} 0 1 1 {p2[0]:.1f},{p2[1]:.1f}", ZONG, 1.6, SOFT)]
o += [P(f"M {p2[0]:.1f},{p2[1]:.1f} Q {ecx+er*0.52:.1f},{ecy} {p1[0]:.1f},{p1[1]:.1f}", ZHE, 1.4, PALE)]
o += [T(380, 252, "心", 10.0, INK, ls=2)]
# 左三细流
for y0, y1 in ((150, 214), (206, 236), (262, 260)):
    o += [P(f"M 156,{y0} C 226,{y0+4} 274,{y1+10} 306,{y1+22}", ZONG, 1.0)]
o += [T(156, 128, "寡", 6.0, ZONG, ls=2)]
# 右十余密流
for i in range(10):
    ang = math.radians(-24 + i * 5.4)
    ex = ecx + er * 0.99 * math.cos(ang)
    ey = ecy + er * 0.99 * math.sin(ang)
    sy = ecy + (i - 4.5) * 22
    o += [P(f"M 616,{sy:.0f} C 552,{sy:.0f} 520,{(sy+ey)/2:.0f} {ex:.1f},{ey:.1f}", ZHE, 0.8)]
o += [T(616, 128, "多", 6.0, ZHE, ls=2)]
o += [T(210, 400, "寡欲 · 存者多", 5.0, ZONG, ls=0.8)]
o += [T(556, 400, "多欲 · 存者少", 5.0, ZHE, ls=0.8)]
o += [T(380, 306, "缺口不在外，在被挤出来的那一处", 4.6, WARM, ls=0.4)]
o += tail_(H, "寡，非无也；节而已。", "图一百六十九", "养心莫善于寡欲", "ch258a")
save("ch258a-guayu-yangxin.svg", o)

# ---------------------------------------------------------- 170 曾皙嗜羊枣
o = head_("曾 皙 嗜 羊 枣", "《孟子》尽心下　第二百五十九章　MZ259", H)
o += [T(380, 112, "脍炙所同也，羊枣所独也", 6.0, ZONG, ls=1.2)]
o += [desk(230, 330, 340)]
# 左小盘：羊枣
o += [E(316, 330, 44, 12, ZONG, 1.1, SOFT), E(316, 330, 33, 8, GREY, 0.6)]
for dx, dy, r in ((-14, -2, 4.2), (0, -4, 4.6), (14, -2, 4.2), (-6, -8, 3.6), (8, -8, 3.6)):
    o += [C(316 + dx, 330 + dy, r, ZONG, 0.8, ZONG)]
o += [T(316, 356, "所独", 5.0, ZHE, ls=1)]
# 右大盘：脍炙
o += [E(496, 330, 66, 15, ZONG, 1.1, SOFT), E(496, 330, 53, 11, GREY, 0.6)]
for i in range(5):
    x = 466 + i * 15
    o += [P(f"M {x},{336} L {x+9},{322}", ZONG, 0.9), P(f"M {x+3},{338} L {x+12},{324}", ZONG, 0.7)]
for i in range(3):
    x = 476 + i * 20
    o += [L(x, 330, x + 13, 328, WARM, 2.4)]
o += [T(496, 356, "所同", 5.0, ZONG, ls=1)]
# 曾子：右手抬起停在羊枣上方
o += [stand(180, 404, 140, INK, 1.3)]
o += [P("M 194,318 C 238,318 268,314 288,306", INK, 1.2)]
o += palhand(294, 304, 1, ZONG, 1.2)
o += [T(258, 288, "手不落", 4.8, ZHE, ls=0.6)]
o += [T(180, 424, "曾子", 4.6, WARM, ls=1)]
o += tail_(H, "凡是独的，都碰不得。", "图一百七十", "曾皙嗜羊枣", "ch259a")
save("ch259a-yangzao-kuaizhi.svg", o)

# ---------------------------------------------------------- 171 孔子在陈
o = head_("孔 子 在 陈", "《孟子》尽心下　第二百六十章　MZ260", H)
o += [T(380, 112, "狂者进取，獧者有所不为；乡原，德之贼也", 5.2, ZONG, ls=0.6)]
# 左：狂者，仰头举手
o += [C(160, 294, 8.8, INK, 1.1)]
o += [L(160, 303, 160, 352, INK, 1.3)]
o += [L(160, 312, 144, 282, INK, 1.1), L(160, 312, 178, 334, INK, 1.0)]
o += [L(160, 352, 150, 404, INK, 1.1), L(160, 352, 172, 404, INK, 1.1)]
o += [C(206, 288, 19, ZHE, 1.1, PALE)]
o += [T(206, 291, "古之人", 4.4, ZHE, ls=0.2)]
o += [T(160, 418, "狂", 6.0, INK, ls=3)]
# 中：乡原，两手向左右，两侧各二人倾身
o += [C(380, 294, 8.8, INK, 1.1)]
o += [L(380, 303, 380, 352, INK, 1.3)]
o += [L(380, 312, 338, 320, INK, 1.0), L(380, 312, 422, 320, INK, 1.0)]
o += [P("M 334,318 L 338,326 L 330,326 Z", INK, 0.9, SOFT), P("M 422,318 L 426,326 L 418,326 Z", INK, 0.9, SOFT)]
o += [L(380, 352, 370, 404, INK, 1.1), L(380, 352, 392, 404, INK, 1.1)]
for x, hh in ((306, 56), (336, 50)):
    o += child(x, 404, hh)
    o += [L(x + 9, 372, x + 20, 356, ZONG, 0.8)]
for x, hh in ((424, 56), (454, 50)):
    o += child(x, 404, hh)
    o += [L(x - 9, 372, x - 20, 356, ZONG, 0.8)]
o += [L(364, 264, 396, 282, ZHE, 1.7), L(396, 264, 364, 282, ZHE, 1.7)]
o += [T(380, 252, "德之贼", 4.8, ZHE, ls=1)]
o += [T(380, 418, "乡原", 6.0, INK, ls=2)]
# 右：獧者，抱臂，身前一道矮墙
o += [C(620, 294, 8.8, INK, 1.1)]
o += [L(620, 303, 620, 352, INK, 1.3)]
o += [L(620, 314, 600, 328, ZONG, 1.2), L(620, 314, 640, 340, ZONG, 1.2)]
o += [L(620, 352, 610, 404, INK, 1.1), L(620, 352, 630, 404, INK, 1.1)]
for x in (556, 588, 620, 652, 684):
    o += [L(x, 372, x, 402, ZONG, 1.2)]
    o += [P(f"M {x-3},380 L {x},372 L {x+3},380", ZONG, 1.0)]
o += [L(552, 380, 688, 380, ZONG, 1.4), L(552, 392, 688, 392, ZONG, 1.0)]
o += [T(688, 366, "矮墙 · 界", 4.6, ZONG, anchor="end", ls=0.8)]
o += [T(620, 418, "獧", 6.0, INK, ls=3)]
o += tail_(H, "狂獧可教，乡原不可入；君子反经而已。", "图一百七十一", "孔子在陈", "ch260a")
save("ch260a-kuang-juan-xiangyuan.svg", o)

# ---------------------------------------------------------- 172 由尧舜至于汤
o = head_("由 尧 舜 至 于 汤", "《孟子》尽心下　第二百六十一章　MZ261　篇终", H)
o += [T(380, 112, "见而知之，闻而知之；五百有余岁", 5.4, ZONG, ls=0.8)]
o += [T(380, 138, "道 统 相 接", 5.0, WARM, ls=2)]
nodes = ((170, "尧舜"), (320, "汤"), (470, "文王"), (620, "孔子"))
o += [L(170, 250, 320, 250, ZONG, 1.8), L(320, 250, 470, 250, ZONG, 1.8),
      L(470, 250, 620, 250, ZONG, 1.8)]
o += [L(620, 250, 700, 250, GREY, 1.0, "4,6")]
for x, nm in nodes:
    o += [C(x, 250, 5.2, INK, 1.2, INK)]
    o += [T(x, 274, nm, 6.2, INK, ls=1.2)]
o += [T(704, 258, "？", 13.0, ZHE, ls=0)]
o += [T(668, 230, "今", 5.6, ZHE, ls=1)]
# 段内：见者实点、闻者虚点
for seg, sees, hears in (((170, 320), "禹·皋陶", "汤"),
                         ((320, 470), "伊尹·莱朱", "文王"),
                         ((470, 620), "太公望·散宜生", "孔子")):
    a, b = seg
    xs = a + (b - a) / 3.0
    xh = a + (b - a) * 2 / 3.0
    o += [C(xs, 250, 3.4, INK, 0.9, INK), C(xh, 250, 3.4, INK, 0.9)]
    o += [T(xs, 234, "见", 5.4, INK), T(xh, 234, "闻", 5.4, GREY)]
    o += [T(xs, 300, sees, 5.2, ZONG, ls=0.2)]
o += [T(380, 336, "前三段，段段有人接；末一段，接的人不见", 5.2, WARM, ls=0.8)]
o += [T(380, 366, "见者，同时之臣；闻者，即次一代之圣", 5.0, ZONG, ls=0.6)]
o += [T(380, 392, "去圣人之世未远，近圣人之居甚近", 5.6, ZONG, ls=1.0)]
o += [T(380, 414, "然而无有乎尔，则亦无有乎尔", 6.6, INK, ls=1.8)]
o += tail_(H, "链到孔子，线还在往前；前面是实的，末端是空的。", "图一百七十二", "由尧舜至于汤", "ch261a")
save("ch261a-you-yaoshun-zhitang.svg", o)
