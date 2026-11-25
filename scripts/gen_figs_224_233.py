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
"""尽心下 图 224–233（v0.31.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""


def tail11(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 尽心下</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


def heap(cx, base, w, hh, col=WARM, sw=1.1):
    """谷堆：锥形加底，内数道斜向谷纹。"""
    o = [P(f"M {cx-w/2},{base} L {cx},{base-hh} L {cx+w/2},{base}", col, sw, fill=SOFT),
         L(cx - w * 0.6, base, cx + w * 0.6, base, WARM, 1.2)]
    for i in range(4):
        t = (i + 1) / 5.0
        o += [L(cx - w * 0.46 * t, base - hh * t * 0.85,
                cx + w * 0.30 * t, base - hh * t * 0.85 + hh * 0.10, GREY, 0.6)]
    return o


def gate(cx, base, w=100, hh=90, col=INK, sw=1.3):
    """关门：两柱、一横梁、中分两扇。"""
    o = [L(cx - w / 2, base, cx - w / 2, base - hh, col, sw),
         L(cx + w / 2, base, cx + w / 2, base - hh, col, sw),
         L(cx - w / 2 - 8, base - hh, cx + w / 2 + 8, base - hh, col, sw * 1.2),
         L(cx, base, cx, base - hh + 6, GREY, 0.9),
         L(cx - w / 2, base - hh * 0.55, cx + w / 2, base - hh * 0.55, GREY, 0.7)]
    return o


def coin(cx, cy, r=13, col=ZONG, sw=1.1):
    """方孔钱。"""
    return [C(cx, cy, r, col, sw),
            R(cx - r * 0.36, cy - r * 0.36, r * 0.72, r * 0.72, col, sw)]


def square_rule(x, y, w=38, hh=30, col=INK, sw=1.2):
    """矩：L 形曲尺。"""
    return [L(x, y, x, y + hh, col, sw), L(x, y, x + w, y, col, sw),
            L(x, y, x + w * 0.42, y + hh * 0.55, GREY, 0.6)]


def qarc(cx, cy, r, col=ZONG, sw=0.9):
    """问答弧：以口为心，向右三道弧。"""
    return [P(f"M {cx+r*0.4},{cy-r*0.5} A {r} {r} 0 0 1 {cx+r*0.4},{cy+r*0.5}", col, sw),
            P(f"M {cx+r*0.8},{cy-r*0.8} A {r*1.4} {r*1.4} 0 0 1 {cx+r*0.8},{cy+r*0.8}", col, sw),
            P(f"M {cx+r*1.2},{cy-r*1.1} A {r*1.8} {r*1.8} 0 0 1 {cx+r*1.2},{cy+r*1.1}", col, sw)]


def robe(cx, base, H, col=INK, sw=1.1, fill=SOFT):
    """着袍之人：头、双肩外张、袍身下阔，不见分腿。"""
    hr = max(5, H * 0.075)
    top = base - H
    sh = top + hr * 2 + H * 0.10
    o = [C(cx, top + hr, hr, col, sw),
         L(cx, top + hr * 2, cx, sh, col, sw * 1.2),
         P(f"M {cx-H*0.05},{sh} L {cx-H*0.20},{sh+H*0.14} L {cx-H*0.24},{base} "
           f"L {cx+H*0.24},{base} L {cx+H*0.20},{sh+H*0.14} L {cx+H*0.05},{sh} Z",
           col, sw, fill=fill),
         L(cx - H * 0.12, sh + H * 0.30, cx, base - 2, col, sw * 0.7),
         L(cx + H * 0.12, sh + H * 0.30, cx, base - 2, col, sw * 0.7)]
    return o


h = 540

# ---------------------------------------------------------- 224 以爱及不爱
o = head_("以 爱 及 不 爱", "《孟子》尽心下　第二百二十四章　MZ224", h)
o += [T(380, 112, "不仁哉，梁惠王也！", 5.9, GREY, ls=1)]
o += [T(380, 150, "仁者：以 所 爱，及 所 不 爱", 6.0, INK, ls=2)]
o += [T(380, 172, "不仁者：以 所 不 爱，及 所 爱", 6.0, ZHE, ls=2)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [P("M 380,200 L 380,404", LINE, 0.9, "none", "4,4")]
# 左：由内向外
o += [stand(216, 404, 126, INK, 1.2)]
o += [C(216, 330, 4.2, ZONG, 1.0, ZONG)]
o += [arrow(222, 326, 296, 268, ZONG, 0.9, 3.4)]
o += [arrow(222, 330, 304, 322, ZONG, 0.9, 3.4)]
o += [arrow(222, 334, 296, 382, ZONG, 0.9, 3.4)]
o += [T(216, 424, "以 所 爱 及 所 不 爱", 4.9, ZONG, ls=1)]
# 右：由外向内
for i in range(3):
    o += [L(470, 366 + i * 12, 610, 366 + i * 12, WARM, 1.1)]
o += [T(540, 340, "土 地", 5.0, GREY, ls=1)]
o += [arrow(612, 362, 660, 344, ZHE, 1.1, 4)]
o += [child(676, 404, 54, ZHE, 1.0)]
o += [T(676, 424, "所 爱 子 弟", 4.9, ZHE, ls=1)]
o += [T(470, 424, "糜 烂 其 民", 4.6, GREY, ls=1)]
o += tail11(h, "仁人之恩，自内及外；不仁之祸，由疏逮亲。", "图一百三十五", "以爱及不爱", "ch224a")
save("ch224a-yiai-ji-buai.svg", o)

# ---------------------------------------------------------- 225 春秋无义战
o = head_("春 秋 无 义 战", "《孟子》尽心下　第二百二十五章　MZ225", h)
o += [T(380, 112, "彼善于此，则有之矣；征者，上伐下也，敌国不相征也", 5.7, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [slip(300, 168, 160, 26)]
o += [T(380, 160, "《春 秋》", 4.8, ZONG, ls=1)]
o += [T(380, 226, "无 义 战", 7.4, ZHE, ls=2)]
for i in range(3):
    o += [stand(176 + i * 42, 404, 66, INK, 0.9)]
    o += [stand(584 - i * 42, 404, 66, INK, 0.9)]
o += [T(218, 424, "彼", 6.0, GREY, ls=1)]
o += [T(542, 424, "此", 6.0, GREY, ls=1)]
o += [arrow(292, 356, 344, 356, ZHE, 1.0, 4)]
o += [arrow(468, 356, 416, 356, ZHE, 1.0, 4)]
o += [T(380, 372, "相 征", 4.8, GREY, ls=1)]
o += [T(380, 396, "敌 国 不 相 征", 4.8, ZONG, ls=1)]
o += tail11(h, "《春秋》无义战。", "图一百三十六", "春秋无义战", "ch225a")
save("ch225a-chunqiu-wu-yizhan.svg", o)

# ---------------------------------------------------------- 226 尽信书
o = head_("尽 信 书", "《孟子》尽心下　第二百二十六章　MZ226", h)
o += [T(380, 112, "尽信《书》，则不如无《书》。吾于《武成》，取二三策而已矣", 5.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 158, "取 二 三 策 而 已 矣", 6.4, INK, ls=2)]
# 原册
o += [R(196, 300, 200, 84, WARM, 1.2, SOFT)]
for i in range(5):
    o += [L(222 + i * 38, 304, 222 + i * 38, 380, GREY, 0.6)]
o += [L(196, 312, 396, 312, ZONG, 0.7), L(196, 372, 396, 372, ZONG, 0.7)]
o += [T(296, 412, "《武 成》", 5.4, ZONG, ls=1)]
# 不可信处打叉
o += [L(360, 330, 380, 356, ZHE, 1.2), L(380, 330, 360, 356, ZHE, 1.2)]
o += [T(470, 366, "血 流 漂 杵", 4.8, ZHE, ls=1)]
o += [P("M 397,344 L 440,352", LINE, 0.8, "none", "3,2")]
# 抽出三策
for i in range(3):
    o += [R(486 + i * 46, 306, 30, 74, ZONG, 1.0, PALE)]
    o += [L(486 + i * 46, 330, 516 + i * 46, 330, GREY, 0.6)]
o += [T(552, 396, "二 三 策", 4.8, ZONG, ls=1)]
o += [T(552, 412, "奉 天 伐 暴", 4.6, GREY, ls=1)]
o += [T(380, 240, "仁 人 无 敌 于 天 下", 5.6, INK, ls=2)]
o += tail11(h, "以至仁伐至不仁，而何其血之流杵也？", "图一百三十七", "尽信书", "ch226a")
save("ch226a-jinxin-shu.svg", o)

# ---------------------------------------------------------- 227 我善为战
o = head_("我 善 为 战", "《孟子》尽心下　第二百二十七章　MZ227", h)
o += [T(380, 112, "有人曰：我善为陈，我善为战。大罪也", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(180, 404, 120, INK, 1.2, arms="point")]
o += [qarc(190, 314, 8, ZHE, 0.9)]
o += [T(180, 424, "我 善 为 陈", 4.9, ZHE, ls=1)]
o += [T(180, 260, "大 罪 也", 5.6, ZHE, ls=1)]
# 阵列
for r in range(2):
    for c in range(3):
        o += [stand(330 + c * 46, 404 - r * 44, 40, INK, 0.8)]
o += [T(430, 366, "陈", 5.2, GREY, ls=1)]
# 仁
o += [C(594, 322, 46, ZONG, 1.3)]
o += [T(594, 330, "仁", 12.0, ZONG)]
o += [arrow(548, 322, 470, 322, ZONG, 1.1, 4)]
o += [T(594, 396, "国 君 好 仁", 4.8, ZONG, ls=1)]
o += [T(594, 412, "天 下 无 敌", 4.8, ZONG, ls=1)]
o += tail11(h, "征之为言正也，各欲正己也，焉用战？", "图一百三十八", "我善为战", "ch227a")
save("ch227a-wo-shan-weizhan.svg", o)

# ---------------------------------------------------------- 228 与人规矩
o = head_("与 人 规 矩", "《孟子》尽心下　第二百二十八章　MZ228", h)
o += [T(380, 112, "梓匠轮舆能与人规矩，不能使人巧", 6.2, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [stand(200, 404, 120, INK, 1.2, arms="point")]
o += [square_rule(236, 300, 40, 32)]
o += [T(200, 424, "梓 匠 轮 舆", 4.9, GREY, ls=1)]
o += [stand(440, 404, 112, INK, 1.1, arms="down")]
o += [square_rule(420, 330, 40, 32)]
o += [T(440, 424, "受 规 矩 者", 4.9, GREY, ls=1)]
o += [P("M 282,316 L 412,336", LINE, 1.0, "none", "5,3")]
o += [T(344, 296, "能 与 人 规 矩", 4.8, ZONG, ls=1)]
o += [T(600, 268, "巧", 10.0, ZONG, ls=2)]
o += [P("M 576,278 L 556,292", LINE, 1.0, "none", "5,3")]
o += [P("M 536,304 L 514,330", LINE, 1.0, "none", "5,3")]
o += [T(604, 292, "不 能 使 人 巧", 4.6, ZHE, ls=1)]
o += tail11(h, "规矩，法度可告者也；巧则在其人。", "图一百三十九", "与人规矩", "ch228a")
save("ch228a-yu-ren-guiju.svg", o)

# ---------------------------------------------------------- 229 饭糗茹草
o = head_("饭 糗 茹 草", "《孟子》尽心下　第二百二十九章　MZ229", h)
o += [T(380, 112, "舜之饭糗茹草也，若将终身焉；及其为天子也，被袗衣，鼓琴", 5.5, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 160, "随 遇 而 安，无 预 于 己", 6.2, INK, ls=2)]
o += [P("M 380,182 L 380,404", LINE, 0.9, "none", "4,4")]
# 左：饭糗
o += [stand(206, 404, 118, INK, 1.1, arms="down")]
o += [bowl(262, 322, 24, 8)]
o += [L(210, 330, 242, 324, INK, 0.9)]
o += [T(212, 424, "饭 糗 茹 草", 4.9, GREY, ls=1)]
o += [T(206, 254, "若 将 终 身 焉", 4.6, ZONG, ls=1)]
# 右：为天子
o += [robe(560, 404, 128, INK, 1.2)]
o += [child(492, 404, 62, GREY, 0.9)]
o += [child(628, 404, 62, GREY, 0.9)]
o += [T(560, 424, "被 袗 衣，鼓 琴", 4.9, GREY, ls=1)]
o += [T(560, 262, "二 女 侍，若 固 有 之", 4.6, ZONG, ls=1)]
o += tail11(h, "圣人之心，不以贫贱而有慕于外，不以富贵而有动于中。", "图一百四十", "饭糗茹草", "ch229a")
save("ch229a-fan-qiu-rucao.svg", o)

# ---------------------------------------------------------- 230 杀人亲
o = head_("杀 人 之 亲", "《孟子》尽心下　第二百三十章　MZ230", h)
o += [T(380, 112, "杀人之父，人亦杀其父；杀人之兄，人亦杀其兄", 5.8, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 158, "非 自 杀 之 也，一 闲 耳", 6.4, INK, ls=2)]
o += [oldman(178, 404, 96, GREY, 0.9)]
o += [oldman(582, 404, 96, GREY, 0.9)]
o += [T(178, 424, "人 之 父", 4.9, GREY, ls=1)]
o += [T(582, 424, "吾 之 父", 4.9, GREY, ls=1)]
o += [stand(268, 404, 112, INK, 1.1)]
o += [stand(492, 404, 112, INK, 1.1)]
o += [arrow(276, 300, 540, 342, ZHE, 1.1, 4)]
o += [arrow(484, 300, 220, 342, ZHE, 1.1, 4)]
o += [T(380, 300, "我 往", 4.6, ZHE, ls=1)]
o += [T(380, 316, "彼 来", 4.6, ZHE, ls=1)]
o += tail11(h, "一闲者，我往彼来，间一人耳。", "图一百四十一", "杀人之亲", "ch230a")
save("ch230a-sha-ren-qin.svg", o)

# ---------------------------------------------------------- 231 为关
o = head_("为 关", "《孟子》尽心下　第二百三十一章　MZ231", h)
o += [T(380, 112, "古之为关也，将以御暴；今之为关也，将以为暴", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [gate(380, 404, 104, 96)]
o += [T(380, 424, "关", 6.2, ZONG, ls=1)]
o += [T(380, 156, "同 一 关 也，古 今 两 心", 6.2, INK, ls=2)]
# 左：御暴
o += [P("M 172,320 Q 206,306 240,320 L 240,354 Q 206,394 172,354 Z", ZONG, 1.2, SOFT)]
o += [P("M 206,318 L 206,384", GREY, 0.7)]
o += [T(206, 424, "御 暴", 5.2, ZONG, ls=1)]
o += [arrow(248, 350, 320, 350, ZONG, 0.9, 4)]
# 右：为暴
o += [coin(500, 350, 14)]
o += [coin(536, 362, 14)]
o += [T(518, 424, "为 暴", 5.2, ZHE, ls=1)]
o += [arrow(440, 350, 478, 350, ZHE, 0.9, 4)]
o += [T(380, 268, "关", 5.0, GREY, ls=1)]
o += tail11(h, "古之为关也，将以御暴；今之为关也，将以为暴。", "图一百四十二", "为关", "ch231a")
save("ch231a-wei-guan.svg", o)

# ---------------------------------------------------------- 232 身不行道
o = head_("身 不 行 道", "《孟子》尽心下　第二百三十二章　MZ232", h)
o += [T(380, 112, "身不行道，不行于妻子；使人不以道，不能行于妻子", 5.8, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 158, "道 不 行 也，非 人 不 从", 6.2, INK, ls=2)]
o += [stand(190, 404, 122, INK, 1.3)]
o += [T(190, 424, "身", 6.2, ZONG, ls=1)]
o += [house(560, 404, 150, 96)]
o += [stand(516, 404, 82, GREY, 0.9)]
o += [stand(604, 404, 72, GREY, 0.9)]
o += [T(560, 424, "妻 与 子", 5.0, GREY, ls=1)]
o += [L(228, 336, 340, 336, LINE, 1.0, "5,3")]
o += [L(374, 336, 478, 336, LINE, 1.0, "5,3")]
o += [L(340, 330, 340, 342, GREY, 0.8), L(374, 330, 374, 342, GREY, 0.8)]
o += [T(357, 322, "不 行", 4.8, ZHE, ls=1)]
o += tail11(h, "身不行道者，以行言之；使人不以道者，以事言之。", "图一百四十三", "身不行道", "ch232a")
save("ch232a-shen-bu-xingdao.svg", o)

# ---------------------------------------------------------- 233 周于德
o = head_("周 于 德", "《孟子》尽心下　第二百三十三章　MZ233", h)
o += [T(380, 112, "周于利者，凶年不能杀；周于德者，邪世不能乱", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 158, "周，足 也；积 之 厚，则 用 有 余", 6.0, INK, ls=2)]
o += [heap(222, 404, 128, 62)]
o += [T(222, 424, "周 于 利", 5.0, GREY, ls=1)]
o += [T(222, 320, "凶 年 不 能 杀", 4.6, ZONG, ls=1)]
o += [T(222, 380, "满", 4.8, GREY, ls=1)]
o += [heap(534, 404, 176, 108)]
o += [T(534, 424, "周 于 德", 5.0, ZONG, ls=1)]
o += [T(534, 276, "邪 世 不 能 乱", 4.6, ZONG, ls=1)]
o += [T(534, 378, "满", 5.0, GREY, ls=1)]
o += [T(380, 300, "积", 6.0, GREY, ls=1)]
o += tail11(h, "周于利者，凶年不能杀；周于德者，邪世不能乱。", "图一百四十四", "周于德", "ch233a")
save("ch233a-zhou-yu-de.svg", o)
