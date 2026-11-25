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
"""尽心上 图 198–207（v0.28.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""


def tail10(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 尽心上</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def crown(cx, cy, w=56, col=INK, sw=1.1):
    """冕：横版一块，下三垂旒，旒端各有珠。"""
    o = [R(cx - w / 2, cy, w, 15, col, sw, fill=SOFT),
         L(cx - w / 2, cy + 3, cx + w / 2, cy + 3, ZONG, 0.8)]
    for i in range(3):
        x = cx - w * 0.26 + i * w * 0.26
        o += [L(x, cy + 15, x, cy + 26, col, sw * 0.8), C(x, cy + 29, 1.9, col, sw * 0.6)]
    return o


def rooster(x, base, H=52, col=INK, sw=1.0):
    """鸡：身椭圆、头小圆、冠一点、尾三线、两足。"""
    by = base - H * 0.62
    o = [E(x, by, H * 0.42, H * 0.30, col, sw, fill=SOFT),
         C(x + H * 0.42, by - H * 0.30, H * 0.135, col, sw),
         P(f"M {x+H*0.36},{by-H*0.44} q 3,-5 7,-2", ZHE, 1.0),
         L(x + H * 0.52, by - H * 0.26, x + H * 0.64, by - H * 0.20, col, sw * 0.7),
         P(f"M {x-H*0.40},{by-H*0.08} q -14,-10 -16,-18", col, sw * 0.8),
         P(f"M {x-H*0.40},{by} q -16,-4 -20,-10", col, sw * 0.8),
         L(x - H * 0.06, by + H * 0.26, x - H * 0.06, base, col, sw),
         L(x + H * 0.12, by + H * 0.26, x + H * 0.12, base, col, sw)]
    return o


def heng(x, y, w=300, col=WARM, sw=1.3):
    """衡：横杆加支点。"""
    o = [L(x, y, x + w, y, col, sw),
         P(f"M {x+w/2-13},{y+26} L {x+w/2},{y+2} L {x+w/2+13},{y+26} Z", col, sw * 0.9, fill=SOFT)]
    return o


def wellprof(x, top, base, w=70, col=WARM, sw=1.1, water=False):
    """井的剖面：井口横木、两壁内收、壁外套土纹；water 为真则底作水波。"""
    o = [L(x - 16, top, x + w + 16, top, ZONG, 1.8),
         L(x - 10, top + 7, x + w + 10, top + 7, LINE, 0.7),
         L(x, top + 7, x + 2, base, col, sw),
         L(x + w, top + 7, x + w - 2, base, col, sw)]
    for i in range(3):
        yy = top + 26 + i * 26
        o += [L(x - 12, yy, x - 4, yy + 6, GREY, 0.7), L(x + w + 4, yy + 6, x + w + 12, yy, GREY, 0.7)]
    if water:
        o += [P(f"M {x+2},{base-16} q {w*0.25},-8 {w*0.5},0 q {w*0.25},8 {w*0.5},0", ZONG, 1.2),
              P(f"M {x+2},{base-7} q {w*0.25},-6 {w*0.5},0 q {w*0.25},6 {w*0.5},0", ZONG, 0.9),
              T(x + w / 2, base + 18, "泉", 5.4, ZONG, ls=1)]
    else:
        o += [L(x + 4, base - 5, x + w - 4, base - 5, GREY, 0.9),
              T(x + w / 2, base + 18, "无 泉", 5.2, ZHE, ls=1)]
    return o


def fence(x, base, w=120, n=5, hh=44, col=WARM, sw=0.9):
    """墙下一段栅：立柱若干、两横。"""
    o = [L(x, base - 12, x + w, base - 12, col, sw), L(x, base - 28, x + w, base - 28, col, sw)]
    for i in range(n):
        xx = x + i * w / (n - 1)
        o += [L(xx, base, xx, base - hh, col, sw)]
    return o


def kindling(x, y, w=46, col=WARM, sw=1.0):
    """一束薪：两横一斜，上出一焰。"""
    o = [L(x, y, x + w, y - 6, col, sw * 1.1), L(x + 4, y - 9, x + w - 2, y - 3, col, sw * 0.9)]
    for dx, sc in ((-9, 0.72), (0, 1.0), (10, 0.8)):
        cx = x + w * 0.5 + dx
        o += [P(f"M {cx},{y-10} q {6*sc},{-10*sc} {2*sc},{-20*sc} q {-2*sc},{-6*sc} {-5*sc},{-8*sc} "
                f"q {1*sc},{9*sc} {3*sc},{16*sc}", ZHE, 1.1)]
    return o


def dougra(x, y, w=56, hh=46, col=ZONG, sw=1.3):
    """斗：上宽下窄的开口量器，口上一撮谷。"""
    o = [P(f"M {x},{y} L {x+w},{y} L {x+w*0.82},{y+hh} L {x+w*0.18},{y+hh} Z", col, sw, fill=SOFT),
         L(x, y, x + w, y, col, sw)]
    for i in range(6):
        o += [C(x + 8 + i * 8, y - 3 - (i % 2) * 3, 1.6, GREY, 0.6)]
    return o


h = 540

# ---------------------------------------------------------- 198 所性
o = head_("所 性", "《孟子》尽心上　第一百九十八章　MZ198", h)
o += [T(380, 112, "广土众民，君子欲之，所乐不存焉；君子所性，仁义礼智根于心", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(380, 404, 96, INK, 1.2)]
o += [C(380, 214, 36, ZONG, 1.2)]
for i, ch in enumerate(("仁", "义", "礼", "智")):
    xx = 363 + (i % 2) * 34
    yy = 206 + (i // 2) * 26
    o += [T(xx, yy, ch, 6.2, INK)]
o += [P("M 380,250 L 380,300", GREY, 0.9, "none", "3,3")]
o += [T(424, 284, "根 于 心", 5.0, ZONG, ls=1)]
o += [C(228, 330, 62, LINE, 1.0, fill=PALE), C(532, 330, 62, LINE, 1.0, fill=PALE)]
o += [T(228, 336, "大 行", 7.4, GREY, ls=2), T(532, 336, "穷 居", 7.4, GREY, ls=2)]
o += [L(176, 428, 228, 428, GREY, 0.8), L(228, 428, 228, 396, GREY, 0.8)]
o += [L(532, 428, 584, 428, GREY, 0.8), L(532, 428, 532, 396, GREY, 0.8)]
o += [T(430, 396, "分 定", 5.4, ZONG, ls=2)]
o += tail10(h, "虽大行不加焉，虽穷居不损焉，分定故也。", "图一百〇九", "所性", "ch198a")
save("ch198a-suo-xing.svg", o)

# ---------------------------------------------------------- 199 善养老
o = head_("善 养 老", "《孟子》尽心上　第一百九十九章　MZ199", h)
o += [T(380, 112, "伯夷辟纣，居北海之滨；太公辟纣，居东海之滨，闻文王作兴", 5.7, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [P("M 128,392 q 26,-14 52,0 q 26,14 52,0", ZONG, 1.2), P("M 128,404 q 26,-10 52,0 q 26,10 52,0", ZONG, 0.9)]
o += [P("M 528,392 q 26,-14 52,0 q 26,14 52,0", ZONG, 1.2), P("M 528,404 q 26,-10 52,0 q 26,10 52,0", ZONG, 0.9)]
o += [stand(220, 404, 100, INK, 1.1)]
o += [T(220, 428, "伯 夷 · 北 海 之 滨", 5.2, ZONG, ls=1)]
o += [stand(546, 404, 100, INK, 1.1)]
o += [T(546, 428, "太 公 · 东 海 之 滨", 5.2, ZONG, ls=1)]
o += house(380, 404, 96, 62)
o += [T(380, 428, "西 伯 · 善 养 老", 5.4, ZONG, ls=1)]
o += [arrow(258, 358, 318, 358, ZONG, 0.9, 4), arrow(504, 358, 444, 358, ZONG, 0.9, 4)]
o += [T(288, 344, "盍 归", 4.8, ZONG, ls=1), T(474, 344, "盍 归", 4.8, ZONG, ls=1)]
o += [T(380, 214, "天 下 有 善 养 老", 6.6, INK, ls=2)]
o += [T(380, 236, "则 仁 人 以 为 己 归", 4.9, GREY, ls=1)]
o += tail10(h, "天下有善养老，则仁人以为己归矣。", "图一百一十", "善养老", "ch199a")
save("ch199a-shan-yanglao.svg", o)

# ---------------------------------------------------------- 200 菽粟如水火
o = head_("菽 粟 如 水 火", "《孟子》尽心上　第二百章　MZ200", h)
o += [T(380, 112, "民非水火不生活，昏暮叩人之门户，求水火，无弗与者，至足矣", 5.8, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [R(300, 250, 118, 154, WARM, 1.3, fill=SOFT), L(359, 250, 359, 404, WARM, 0.8)]
o += [C(332, 336, 3.2, INK, 1.0), C(386, 336, 3.2, INK, 1.0)]
o += [T(359, 230, "昏 暮 叩 门", 5.6, ZONG, ls=1)]
o += bowl(160, 372, 40, 13)
o += [T(160, 424, "水 · 无 弗 与", 5.2, ZONG, ls=1)]
o += kindling(470, 380, 48)
o += [T(494, 424, "火 · 无 弗 与", 5.2, ZONG, ls=1)]
o += dougra(548, 336, 56, 46)
o += [T(576, 424, "菽 粟", 5.6, ZONG, ls=1)]
o += [stand(240, 404, 84, INK, 0.9, arms="point")]
o += [T(380, 190, "至 足 矣", 7.2, INK, ls=3)]
o += tail10(h, "菽粟如水火，而民焉有不仁者乎？", "图一百一十一", "菽粟如水火", "ch200a")
save("ch200a-shusu-rushuihuo.svg", o)

# ---------------------------------------------------------- 201 登东山
o = head_("登 东 山", "《孟子》尽心上　第二百〇一章　MZ201", h)
o += [T(380, 112, "孔子登东山而小鲁，登太山而小天下", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [P("M 130,404 L 190,306 L 250,404 Z", WARM, 1.1, fill=SOFT)]
o += [P("M 286,404 L 388,214 L 490,404 Z", WARM, 1.3, fill=SOFT)]
o += [stand(388, 214, 32, INK, 0.9)]
o += [T(190, 424, "东 山 · 小 鲁", 5.4, GREY, ls=1)]
o += [T(388, 424, "太 山 · 小 天下", 5.4, ZONG, ls=1)]
o += [P("M 496,262 C 532,252 546,300 580,300 C 612,300 620,332 648,336", ZONG, 1.3)]
o += [P("M 496,288 C 528,278 542,318 574,318 C 604,318 612,348 640,352", ZONG, 1.0)]
o += [T(560, 242, "观 水 必 观 其 澜", 5.2, ZONG, ls=1)]
o += [P("M 510,404 L 510,384 L 552,384 L 552,364 L 604,364 L 604,344 L 660,344", LINE, 1.1)]
o += [T(586, 432, "不 盈 科 不 行", 5.2, GREY, ls=1)]
o += tail10(h, "流水之为物也，不盈科不行；君子之志于道也，不成章不达。", "图一百一十二", "登东山", "ch201a")
save("ch201a-deng-dongshan.svg", o)

# ---------------------------------------------------------- 202 舜跖之分
o = head_("舜 跖 之 分", "《孟子》尽心上　第二百〇二章　MZ202", h)
o += [T(380, 112, "鸡鸣而起，孳孳为善者，舜之徒也；孳孳为利者，跖之徒也", 5.8, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += rooster(188, 404, 54)
o += [T(188, 424, "鸡 鸣 而 起", 5.4, ZONG, ls=1)]
o += [L(380, 262, 380, 404, LINE, 0.9)]
o += [stand(296, 404, 96, INK, 1.1)]
o += [T(296, 424, "善", 7.0, ZONG, ls=2)]
o += [stand(466, 404, 96, GREY, 1.0)]
o += [T(466, 424, "利", 7.0, GREY, ls=2)]
o += [T(296, 274, "舜 之 徒", 5.4, ZONG, ls=1), T(466, 274, "跖 之 徒", 5.4, GREY, ls=1)]
o += [T(380, 214, "利 与 善 之 间", 6.8, INK, ls=3)]
o += [T(380, 236, "所 争 毫 末", 4.8, GREY, ls=1)]
o += tail10(h, "欲知舜与跖之分，无他，利与善之间也。", "图一百一十三", "舜跖之分", "ch202a")
save("ch202a-shun-zhi-zhi-fen.svg", o)

# ---------------------------------------------------------- 203 执中无权
o = head_("执 中 无 权", "《孟子》尽心上　第二百〇三章　MZ203", h)
o += [T(380, 112, "杨子取为我，墨子兼爱，子莫执中；执中无权，犹执一也", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += heng(206, 252, 348)
o += [L(380, 252, 380, 292, WARM, 0.9)]
o += [C(380, 306, 15, WARM, 1.2, fill=SOFT)]
o += [T(380, 394, "执 中", 5.8, ZONG, ls=1)]
o += [T(380, 338, "权", 5.2, GREY)]
o += [T(424, 340, "锤 不 动", 4.8, ZHE, ls=1)]
o += [stand(200, 404, 84, INK, 0.9)]
o += [T(200, 424, "为 我", 5.4, GREY, ls=1)]
o += [stand(566, 404, 84, INK, 0.9, arms="point")]
o += [T(566, 424, "兼 爱", 5.4, GREY, ls=1)]
o += [T(200, 224, "拔 一 毛 而 不 为", 4.8, GREY, ls=1), T(566, 224, "摩 顶 放 踵", 4.8, GREY, ls=1)]
o += tail10(h, "所恶执一者，为其贼道也，举一而废百也。", "图一百一十四", "执中无权", "ch203a")
save("ch203a-zhizhong-wuquan.svg", o)

# ---------------------------------------------------------- 204 饥渴之害
o = head_("饥 渴 之 害", "《孟子》尽心上　第二百〇四章　MZ204", h)
o += [T(380, 112, "饥者甘食，渴者甘饮，是未得饮食之正也，饥渴害之也", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(252, 404, 108, INK, 1.1, arms="down")]
o += bowl(318, 384, 24, 9)
o += [T(286, 428, "饥 者 甘 食", 5.6, ZONG, ls=1)]
o += bowl(490, 352, 34, 10)
o += [T(490, 428, "渴 者 甘 饮", 5.6, ZONG, ls=1)]
o += [L(360, 300, 448, 300, LINE, 0.9, "4,3")]
o += [T(404, 288, "正 味", 4.8, GREY, ls=1)]
o += [C(618, 326, 22, ZONG, 1.2)]
o += [T(618, 331, "心", 6.2, INK)]
o += [T(618, 288, "贫 贱 害 之", 4.8, ZHE, ls=1)]
o += tail10(h, "人能无以饥渴之害为心害，则不及人不为忧矣。", "图一百一十五", "饥渴之害", "ch204a")
save("ch204a-jike-zhihai.svg", o)

# ---------------------------------------------------------- 205 不易其介
o = head_("不 易 其 介", "《孟子》尽心上　第二百〇五章　MZ205", h)
o += [T(380, 112, "柳下惠不以三公易其介", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += desk(128, 316, 132, 10)
o += crown(194, 282, 66, INK, 1.2)
o += [T(194, 348, "三 公 之 冕", 5.2, GREY, ls=1)]
o += [arrow(246, 306, 392, 306, ZHE, 1.0, 4)]
o += [T(320, 294, "易 之", 5.2, ZHE, ls=1)]
o += [T(320, 330, "不 受", 5.4, ZONG, ls=1)]
o += [stand(420, 404, 120, INK, 1.3)]
o += [T(420, 250, "介", 8.6, INK, ls=2)]
o += [L(372, 418, 386, 418, GREY, 0.9), L(398, 418, 412, 418, GREY, 0.9), L(424, 418, 438, 418, GREY, 0.9)]
o += [T(405, 434, "三 黜", 5.0, GREY, ls=1)]
o += [T(596, 424, "和 而 不 流", 5.4, ZONG, ls=1)]
o += tail10(h, "柳下惠不以三公易其介。", "图一百一十六", "不易其介", "ch205a")
save("ch205a-buyi-qijie.svg", o)

# ---------------------------------------------------------- 206 掘井及泉
o = head_("掘 井 及 泉", "《孟子》尽心上　第二百〇六章　MZ206", h)
o += [T(380, 112, "有为者辟若掘井，掘井九轫而不及泉，犹为弃井也", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += wellprof(214, 296, 404, 62, WARM, 1.0, water=False)
o += [T(245, 428, "九 轫 而 不 及 泉", 5.4, ZHE, ls=1)]
o += [T(245, 276, "弃 井", 6.2, ZHE, ls=2)]
o += wellprof(456, 296, 404, 62, WARM, 1.0, water=True)
o += [T(487, 428, "及 泉", 5.6, ZONG, ls=1)]
o += [L(380, 240, 380, 400, LINE, 0.9)]
o += [T(380, 228, "同 深 而 异 果", 5.4, GREY, ls=1)]
o += tail10(h, "掘井九轫而不及泉，犹为弃井也。", "图一百一十七", "掘井及泉", "ch206a")
save("ch206a-juejing-jiquan.svg", o)

# ---------------------------------------------------------- 207 性之身之假之
o = head_("性 之 · 身 之 · 假 之", "《孟子》尽心上　第二百〇七章　MZ207", h)
o += [T(380, 112, "尧舜，性之也；汤武，身之也；五霸，假之也", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [L(300, 160, 300, 404, LINE, 0.8), L(470, 160, 470, 404, LINE, 0.8)]
o += [stand(206, 404, 108, INK, 1.2)]
o += [T(206, 424, "性 之", 5.8, ZONG, ls=2)]
o += [T(206, 268, "无 所 假", 4.8, GREY, ls=1)]
o += [stand(384, 404, 104, INK, 1.1)]
o += [arrow(414, 400, 414, 306, ZONG, 1.0, 3.6)]
o += [T(430, 352, "履 之", 5.0, ZONG, ls=1)]
o += [T(384, 424, "身 之", 5.8, ZONG, ls=2)]
o += [stand(566, 404, 106, INK, 1.0)]
o += crown(566, 284, 46, GREY, 1.0)
o += [T(566, 424, "假 之", 5.8, GREY, ls=2)]
o += [T(630, 300, "借 来 之 冕", 4.8, GREY, ls=1)]
o += tail10(h, "久假而不归，恶知其非有也。", "图一百一十八", "性之身之假之", "ch207a")
save("ch207a-xing-zhi-shen-zhi-jia-zhi.svg", o)
