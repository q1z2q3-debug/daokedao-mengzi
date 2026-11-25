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
"""告子下 图 172–177（v0.25.0 收卷）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""

def tail9(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 告子下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def gate(cx, base, w=96, hh=96, col=WARM, sw=1.2, label="", open_=True):
    """门：双柱、门楣、门槛，门扇可半掩。"""
    o = [L(cx - w / 2, base, cx - w / 2, base - hh, col, sw),
         L(cx + w / 2, base, cx + w / 2, base - hh, col, sw),
         L(cx - w / 2 - 6, base - hh, cx + w / 2 + 6, base - hh, col, sw * 1.3),
         L(cx - w / 2, base, cx + w / 2, base, col, sw * 1.1)]
    if open_:
        o += [R(cx - w / 2, base - hh + 4, w * 0.42, hh - 4, col, sw * 0.8, fill=PALE)]
    else:
        o += [R(cx - w / 2, base - hh + 4, w, hh - 4, col, sw * 0.8, fill=SOFT)]
    if label:
        o += [T(cx, base - hh - 12, label, 5.4, ZONG, ls=1)]
    return o


def hand(cx, cy, s=1.0, col=INK, sw=1.0, hold=True):
    """一只手的极简：掌、四指收、拇指。"""
    o = [P(f"M {cx},{cy} q {6*s},{-4*s} {10*s},{0}", col, sw)]
    for i in range(3):
        o += [P(f"M {cx - 4*s + i*4*s},{cy} q {2*s},{-8*s} {3*s},{-11*s}", col, sw * 0.9)]
    o += [P(f"M {cx + 2*s},{cy - 2*s} q {7*s},{-6*s} {9*s},{-2*s}", col, sw * 0.9)]
    return o


def face(cx, cy, r=26, col=WARM, sw=1.1, proud=True):
    """訑訑之面：圆面、双目、横嘴。"""
    o = [C(cx, cy, r, col, sw),
         L(cx - 10, cy - 6, cx - 4, cy - 6, col, sw * 0.8),
         L(cx + 4, cy - 6, cx + 10, cy - 6, col, sw * 0.8)]
    if proud:
        o += [P(f"M {cx-10},{cy+10} q 10,4 20,0", col, sw * 0.9)]
    return o


def loadman(cx, base, H=108, col=INK, sw=1.1):
    """挑担的人：肩上一扁担，两端垂物。"""
    o = [stand(cx, base, H, col, sw)]
    sy = base - H + H * 0.42
    o += [L(cx - 34, sy - 12, cx + 34, sy - 12, col, sw * 1.1),
          L(cx - 34, sy - 12, cx - 34, sy + 6, col, sw * 0.7),
          L(cx + 34, sy - 12, cx + 34, sy + 6, col, sw * 0.7),
          P(f"M {cx-42},{sy+6} q 8,10 16,0 q 8,-8 0,-4", col, sw * 0.9, fill=SOFT),
          P(f"M {cx+26},{sy+6} q 8,10 16,0 q 8,-8 0,-4", col, sw * 0.9, fill=SOFT)]
    return o


h = 540

# ---------------------------------------------------------- 172 以邻国为壑
o = head_("以 邻 为 壑", "《孟子》告子下　第一百七十二章　MZ172", h)
o += [T(380, 112, "禹之治水，水之道也；今吾子以邻国为壑", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [C(178, 300, 44, ZONG, 1.2)]
o += [P("M 148,296 q 12,-7 24,0 q 12,7 24,0", ZONG, 0.9),
      P("M 148,312 q 12,-7 24,0 q 12,7 24,0", ZONG, 0.9)]
o += [T(178, 360, "四 海", 6.4, ZONG, ls=2)]
o += [P("M 222,300 q 34,-8 66,0 q 34,8 70,0 q 34,-8 68,0", ZONG, 1.1),
      P("M 222,312 q 34,-8 66,0 q 34,8 70,0 q 34,-8 68,0", ZONG, 1.1)]
o += [T(330, 288, "顺 水 之 性", 5.0, GREY, ls=1)]
o += [P("M 436,404 L 456,300 L 480,300 L 500,404 Z", WARM, 1.2, fill=SOFT)]
o += [T(468, 424, "堤", 5.4, ZONG)]
o += [stand(372, 404, 94, INK, 1.0)]
o += [T(372, 424, "白 圭", 5.4, GREY)]
o += [L(390, 320, 452, 302, ZONG, 0.9)]
o += [P("M 480,300 q 44,26 62,64 q 8,16 10,26", ZONG, 1.2)]
o += [arrow(548, 394, 606, 396, ZHE, 1.1, 5)]
o += [R(612, 356, 78, 48, WARM, 1.2, fill=SOFT)]
for k in range(3):
    o += [R(616 + k * 26, 346, 12, 12, WARM, 1.0, fill=SOFT)]
o += [L(651, 404, 651, 372, WARM, 0.9)]
o += [T(651, 424, "邻 国", 5.6, ZONG, ls=2)]
o += [T(520, 338, "洚 水", 5.2, ZHE, ls=1)]
o += [T(380, 224, "禹以四海为壑　今吾子以邻国为壑", 5.4, GREY)]
o += tail9(h, "水逆行谓之洚水；洚水者，洪水也。", "图八十三", "以邻为壑", "ch172a")
save("ch172a-yilin-weihuo.svg", o)

# ---------------------------------------------------------- 173 不亮无执
o = head_("不 亮 无 执", "《孟子》告子下　第一百七十三章　MZ173", h)
o += [T(380, 112, "君子不亮，恶乎执？", 6.8, GREY, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
for cx, brk in ((268, False), (508, True)):
    o += [L(cx - 40, 404, cx - 40, 300, WARM, 1.1), L(cx + 40, 404, cx + 40, 300, WARM, 1.1)]
    if not brk:
        o += [L(cx - 48, 300, cx + 48, 300, WARM, 1.3),
              L(cx, 300, cx, 340, WARM, 0.8),
              R(cx - 11, 340, 22, 18, ZONG, 1.1, fill=SOFT)]
    else:
        o += [L(cx - 48, 300, cx - 12, 300, WARM, 1.3),
              L(cx + 12, 300, cx + 48, 300, WARM, 1.3),
              P(f"M {cx-12},{300} L {cx-16},{288}", WARM, 0.9),
              P(f"M {cx+12},{300} L {cx+16},{312}", WARM, 0.9),
              P("M 508,300 L 508,404", LINE, 0.8, "none", "3,3"),
              R(cx - 11, 386, 22, 18, ZONG, 1.1, fill=SOFT)]
o += [T(268, 424, "亮 而 后 执", 5.6, ZONG, ls=1)]
o += [T(508, 424, "不 亮", 5.6, ZHE, ls=1)]
o += [T(268, 274, "所执有信", 5.2, GREY)]
o += [T(508, 274, "所执无信", 5.2, GREY)]
o += [T(388, 250, "恶乎执", 6.0, ZHE, ls=2)]
o += tail9(h, "亮，信也，与谅同。", "图八十四", "不亮无执", "ch173a")
save("ch173a-buliang-wuzhi.svg", o)

# ---------------------------------------------------------- 174 好善优于天下
o = head_("好 善 优 天 下", "《孟子》告子下　第一百七十四章　MZ174", h)
o += [T(380, 112, "好善优于天下，而况鲁国乎", 6.4, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(340, 340, 96, INK, 1.2)]
o += [T(340, 366, "乐正子", 5.4, ZONG, ls=2)]
o += [arrow(150, 216, 296, 292, ZONG, 0.9, 4)]
o += [arrow(150, 356, 294, 334, ZONG, 0.9, 4)]
o += [arrow(586, 208, 388, 288, ZONG, 0.9, 4)]
o += [T(340, 184, "四海之内，皆将轻千里而来告之以善", 5.4, GREY)]
o += [face(596, 344, 22, WARM, 1.1, True)]
o += [T(596, 382, "訑 訑", 5.4, ZHE, ls=1)]
o += [arrow(624, 336, 658, 328, GREY, 0.9, 3)]
o += [T(596, 300, "距人千里", 5.0, GREY)]
o += tail9(h, "与谗谄面谀之人居，国欲治，可得乎？", "图八十五", "好善优于天下", "ch174a")
save("ch174a-haoshan-youtianxia.svg", o)

# ---------------------------------------------------------- 175 所就三所去三
o = head_("所 就 三 · 所 去 三", "《孟子》告子下　第一百七十五章　MZ175", h)
o += [T(380, 112, "古之君子何如则仕？所就三，所去三", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
rows = ((206, "迎致敬以有礼", "言将行其言", "就 之", "言弗行也", "去 之"),
        (306, "礼貌未衰", "言弗行也", "就 之", "礼貌衰", "去 之"),
        (390, "饥饿不能出门户", "君周之", "受 之", "免死而已", "止"))
for base, l1, l2, r1, r2, r3 in rows:
    o += gate(300, base, 80, 56, WARM, 1.1, "", True)
    o += [T(136, base - 36, l1, 5.0, GREY, ls=0),
          T(136, base - 14, l2, 5.0, GREY, ls=0)]
    o += [T(300, base - 68, r1, 6.0, ZHE, ls=2)]
    o += [arrow(344, base - 32, 384, base - 32, ZHE, 0.9, 4)]
    o += [T(394, base - 26, r2, 5.0, GREY, ls=0)]
    if r3 != "止":
        o += [arrow(344, base - 10, 384, base - 10, GREY, 0.9, 4)]
    else:
        o += [P(f"M 344,{base-10} L 384,{base-10}", GREY, 0.7, "none", "3,3")]
    o += [T(394, base - 4, r3, 5.0, ZONG, ls=0)]
o += tail9(h, "免死而已矣。", "图八十六", "所就三所去三", "ch175a")
save("ch175a-suojiu-san.svg", o)

# ---------------------------------------------------------- 176 生于忧患
o = head_("生 于 忧 患", "《孟子》告子下　第一百七十六章　MZ176", h)
o += [T(380, 112, "天将降大任于是人也，必先苦其心志，劳其筋骨", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
xs = (146, 190, 234)
o += [stand(xs[0], 404, 56, WARM, 0.8), stand(xs[1], 404, 52, WARM, 0.8), stand(xs[2], 404, 48, WARM, 0.8)]
o += [stand(xs[0], 330, 44, WARM, 0.8), stand(xs[1], 330, 42, WARM, 0.8), stand(xs[2], 330, 40, WARM, 0.8)]
o += [T(190, 424, "舜 · 傅说 · 胶鬲", 5.0, GREY, ls=0),
      T(190, 356, "管夷吾 · 孙叔敖 · 百里奚", 5.0, GREY, ls=0)]
o += [T(190, 250, "发 于 微 贱", 5.6, ZONG, ls=2)]
o += [P("M 296,150 L 476,268", LINE, 0.8, "none", "4,3")]
o += [arrow(310, 160, 466, 264, ZHE, 1.0, 5)]
o += [T(404, 210, "天 降 大 任", 5.6, ZHE, ls=2)]
o += loadman(520, 404, 108)
o += [T(520, 424, "苦志 · 劳骨 · 饿体", 5.0, ZONG, ls=0)]
o += gate(626, 404, 52, 66, GREY, 1.0, "", True)
o += [L(602, 336, 650, 352, GREY, 0.9), L(650, 336, 602, 352, GREY, 0.9)]
o += [T(626, 424, "无 法 家 拂 士", 4.6, GREY, ls=0)]
o += tail9(h, "生于忧患，而死于安乐也。", "图八十七", "生于忧患", "ch176a")
save("ch176a-shengyu-youhuan.svg", o)

# ---------------------------------------------------------- 177 教亦多术
o = head_("教 亦 多 术", "《孟子》告子下　第一百七十七章　MZ177", h)
o += [T(380, 112, "教亦多术矣。不屑之教诲也者，是亦教诲之而已矣", 6.0, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [L(170, 404, 260, 404, ZONG, 1.1), T(215, 424, "绳", 5.2, ZONG, ls=1)]
o += [P("M 200,404 L 200,320 L 300,320", WARM, 1.1), P("M 200,404 L 300,320", WARM, 0.9),
      T(250, 424 - 82, "矩", 5.2, WARM, ls=1)]
o += [E(420, 360, 46, 26, LINE, 0.8), P("M 420,360 L 420,322", ZONG, 1.1),
      P("M 420,322 L 450,330", ZONG, 0.9), T(420, 424 - 44, "规", 5.2, ZONG, ls=1)]
o += [T(300, 236, "多 术", 6.4, ZONG, ls=3)]
o += [gate(560, 404, 96, 96, GREY, 1.1, "", True)]
o += [stand(588, 404, 92, INK, 1.1)]
o += [T(588, 424, "师 在 内", 5.2, GREY)]
o += [stand(490, 404, 88, INK, 1.0)]
o += [T(490, 424, "弟 子 在 外", 5.2, ZHE)]
o += [P("M 512,300 L 560,300", LINE, 0.9, "none", "3,3")]
o += [T(560, 282, "不 屑 之 教 诲", 5.2, ZHE, ls=1)]
o += tail9(h, "是亦教诲之而已矣。", "图八十八", "教亦多术", "ch177a")
save("ch177a-jiao-yi-duoshu.svg", o)
