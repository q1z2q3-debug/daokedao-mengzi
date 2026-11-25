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
"""离娄下补章 图 120–123（v0.19.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail4(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 离娄下（补章）</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def zun(cx, base, H=96, col=ZONG, sw=1.3):
    """酒尊：侈口、鼓腹、圈足。"""
    return [E(cx, base - H, 30, 9, col, sw, fill=PALE),
            P(f"M {cx-22},{base-H+6} C {cx-34},{base-H*0.5} {cx-30},{base-H*0.18} {cx-16},{base-H*0.1}",
              col, sw, fill=SOFT),
            P(f"M {cx+22},{base-H+6} C {cx+34},{base-H*0.5} {cx+30},{base-H*0.18} {cx+16},{base-H*0.1}",
              col, sw, fill=SOFT),
            L(cx - 16, base - H * 0.1, cx + 16, base - H * 0.1, col, sw),
            L(cx - 18, base - H * 0.1, cx - 22, base, col, sw * 0.9),
            L(cx + 18, base - H * 0.1, cx + 22, base, col, sw * 0.9)]


def jian(cx, base, w=110, hh=118, col=WARM, sw=1.1):
    """立册：竖立的卷册。"""
    return [R(cx - w / 2, base - hh, w, hh, col, sw, fill=PALE),
            L(cx - w / 2 + 2, base - hh * 0.78, cx + w / 2 - 2, base - hh * 0.78, ZONG, 0.8),
            L(cx - w / 2 + 2, base - hh * 0.22, cx + w / 2 - 2, base - hh * 0.22, ZONG, 0.8),
            *[L(cx - w / 2 + 12 + i * (w - 24) / 5.0, base - hh + 10, cx - w / 2 + 12 + i * (w - 24) / 5.0,
               base - 10, GREY, 0.5) for i in range(5)]]


# ---------------------------------------------------------- 120 禹恶旨酒
h = 540
o = head_("禹 恶 旨 酒", "《孟子》离娄下　补章　MZ120", h)
o.append(T(380, 112, "禹恶旨酒而好善言　汤执中　文王视民如伤　周公思兼三王", 6.4, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 380,250 L 380,404", LINE, 1.0, "none", "4,4")]
o += zun(210, 404, 96, ZONG, 1.3)
o += [E(210, 400, 22, 6, ZHE, 1.0, fill=PALE)]
o += [C(244, 398, 3.0, ZHE, 0.8), C(252, 392, 2.4, ZHE, 0.8), C(260, 400, 2.8, ZHE, 0.8)]
o += [T(210, 292, "旨酒", 6.2, ZONG, ls=2), T(210, 280, "恶之", 5.2, ZHE)]
o += [T(210, 424, "仪狄作酒，禹饮而甘之，遂疏仪狄", 5.6, GREY)]
o += [stand(470, 404, 92, INK, 1.1)]
o += [L(470, 352, 492, 358, INK, 0.9), L(470, 344, 492, 350, INK, 0.9)]
o += [C(495, 354, 3.4, INK, 0.9)]
o += [L(478, 404, 466, 404, INK, 0.8)]
o += [T(470, 292, "禹拜昌言", 5.8, ZHE)]
o += [jian(566, 404, 92, 104, WARM, 1.1)]
o += [T(566, 292, "善言", 6.0, ZONG, ls=2)]
o += [T(380, 424, "其有不合者，仰而思之，夜以继日；幸而得之，坐以待旦", 5.8, GREY)]
o += tail4(h, "禹恶旨酒而好善言。", "图三十一", "禹恶旨酒", "ch120a")
save("ch120a-yu-ezhijiu.svg", o)


# ---------------------------------------------------------- 121 诗亡春秋
h = 540
o = head_("诗 亡 春 秋", "《孟子》离娄下　补章　MZ121", h)
o.append(T(380, 112, "王者之迹熄而诗亡　诗亡然后春秋作", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 380,250 L 380,404", LINE, 1.0, "none", "4,4")]
o += [L(210, 316, 210, 372, ZONG, 1.3), L(184, 372, 236, 372, ZONG, 1.2)]
o += [P("M 180,316 C 182,334 238,334 240,316", ZONG, 1.3, fill=SOFT)]
o += [L(210, 316, 210, 306, ZONG, 1.0), C(210, 303, 2.6, ZHE, 0.9)]
o += [P("M 206,286 C 210,272 214,266 212,258", GREY, 0.7)]
o += [P("M 218,284 C 224,272 228,264 226,254", GREY, 0.7)]
o += [T(210, 292 - 32, "灯无焰", 5.8, ZONG, ls=1)]
o += [T(210, 424, "迹熄：政教号令不及于天下", 5.6, GREY)]
o += [jian(520, 404, 116, 122, WARM, 1.2)]
o += [T(520, 274, "鲁之春秋", 6.2, ZONG, ls=1)]
o += [T(520, 424, "其事则齐桓晋文　其文则史　其义则丘窃取", 5.6, GREY)]
o += [T(380, 268, "晋之乘　楚之梼杌　鲁之春秋　一也", 5.8, ZHE)]
o += tail4(h, "诗亡然后春秋作。", "图三十二", "诗亡春秋", "ch121a")
save("ch121a-shiwang-chunqiu.svg", o)


# ---------------------------------------------------------- 122 五世之泽
h = 540
o = head_("五 世 之 泽", "《孟子》离娄下　补章　MZ122", h)
o.append(T(380, 112, "君子之泽五世而斩　予私淑诸人也", 6.6, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
o += [P("M 380,250 L 380,404", LINE, 1.0, "none", "4,4")]
lens = [200, 172, 144, 116, 88]
for i, ln in enumerate(lens):
    y = 300 + i * 22
    col = ZONG if i < 4 else GREY
    seg = ln / 4.0
    pts = []
    for k in range(5):
        pts.append("M %d,%d Q %d,%d %d,%d" % (140 + k * seg, y, 140 + k * seg + seg / 2, y - (5 if k % 2 == 0 else -5),
                                              140 + (k + 1) * seg, y))
    o += [P(" ".join(pts), col, 1.5 if i < 4 else 0.9)]
    o += [T(126, y + 3, "%d" % (i + 1), 5.4, GREY)]
o += [T(206, 286, "君子之泽", 6.4, ZONG, ls=2)]
o += [T(126, 424, "泽，流风余韵；五世而绝，斩者渐也", 5.6, GREY)]
o += [jian(520, 404, 104, 112, WARM, 1.1)]
o += [T(520, 284, "私淑诸人", 5.8, ZHE)]
o += [T(520, 424, "予未得为孔子徒也", 5.6, GREY)]
o += [T(380, 268, "孔子卒至孟子游梁，方百四十余年", 5.6, GREY)]
o += tail4(h, "五世而斩。", "图三十三", "五世之泽", "ch122a")
save("ch122a-wushi-zhize.svg", o)


# ---------------------------------------------------------- 123 取与死
h = 540
o = head_("取 与 死", "《孟子》离娄下　补章　MZ123", h)
o.append(T(380, 112, "可以取，可以无取　可以死，可以无死", 6.4, GREY, ls=1))
o += [L(96, 404, 664, 404, WARM, 1.3)]
# 左：斗（取）
o += [P("M 168,352 L 152,404", ZONG, 1.2), P("M 232,352 L 248,404", ZONG, 1.2)]
o += [E(200, 352, 32, 9, ZONG, 1.3, fill=SOFT)]
o += [L(200, 352, 200, 404, ZONG, 1.0)]
o += [T(200, 288, "可以取", 5.8, INK)]
o += [T(200, 304, "可以无取", 5.2, GREY)]
o += [T(200, 424, "取伤廉", 5.8, ZHE)]
# 中：碗（与）
o += bowl(380, 344, 40, 12)
o += [T(380, 288, "可以与", 5.8, INK)]
o += [T(380, 304, "可以无与", 5.2, GREY)]
o += [T(380, 424, "与伤惠", 5.8, ZHE)]
# 右：剑（死）
o += [R(556, 268, 6, 108, ZONG, 1.0, fill=PALE)]
o += [L(542, 372, 570, 372, ZONG, 1.2)]
o += [P("M 559,376 L 559,404", ZONG, 1.0)]
o += [T(556, 250, "可以死", 5.8, INK)]
o += [T(556, 238, "可以无死", 5.2, GREY)]
o += [T(556, 424, "死伤勇", 5.8, ZHE)]
o += [T(380, 268, "过犹不及：三事皆有其过", 5.8, GREY)]
o += tail4(h, "死伤勇。", "图三十四", "取与死", "ch123a")
save("ch123a-quyu-shang.svg", o)
