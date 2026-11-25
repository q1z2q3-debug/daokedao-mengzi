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
"""尽心上 图 218–223（v0.30.0）
拼装：head -144 gen_figs_072_081.py + _helpers_082_089.py + 本文件
"""


def tail10(h, q, label, name, key):
    return [L(120, h - 104, 640, h - 104, LINE, 1),
            T(380, h - 80, q, 8.6, INK, ls=2),
            f'  <text x="120" y="{h-46}" font-size="5.6" fill="{ZONG}">孟子 · 尽心上</text>',
            f'  <text x="640" y="{h-46}" text-anchor="end" font-size="5.6" fill="{ZONG}">{label} · {name} · {key}</text>']


h = 540

# ---------------------------------------------------------- 218 引而不发
o = head_("引 而 不 发", "《孟子》尽心上　第二百一十八章　MZ218", h)
o += [T(380, 112, "道则高矣，美矣，宜若登天然，似不可及也", 5.8, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 166, "引 而 不 发，跃 如 也", 6.6, INK, ls=2)]
# 弓：弓身右凸、两弰外翘、弦折向左、箭搭弦上而未出
o += [P("M 270,214 Q 350,300 270,386", INK, 1.6)]
o += [P("M 270,214 L 196,300 L 270,386", INK, 1.0)]
o += [L(270, 214, 256, 204, INK, 1.4), L(270, 386, 256, 396, INK, 1.4)]
o += [arrow(198, 300, 292, 300, ZONG, 1.2, 4)]
o += [T(186, 284, "引", 6.6, ZONG, ls=1)]
o += [T(346, 284, "不 发", 4.8, GREY, ls=1)]
o += [T(300, 424, "彀 率", 5.2, GREY, ls=1)]
# 中道而立
o += [P("M 470,200 L 470,404", LINE, 1.0, "none", "4,4")]
o += [stand(470, 404, 120, INK, 1.2)]
o += [T(470, 424, "中 道 而 立", 5.2, ZONG, ls=1)]
o += [T(440, 188, "非 难 非 易", 4.6, GREY, ls=1)]
# 绳墨
o += [L(576, 404, 576, 356, WARM, 1.2), L(680, 404, 680, 356, WARM, 1.2)]
o += [L(576, 356, 680, 356, INK, 1.6)]
o += [T(628, 424, "绳 墨", 5.2, GREY, ls=1)]
o += [T(628, 340, "大 匠 不 改", 4.7, ZONG, ls=1)]
o += tail10(h, "大匠不为拙工改废绳墨，羿不为拙射变其彀率。", "图一百二十九", "引而不发", "ch218a")
save("ch218a-yin-er-bufa.svg", o)

# ---------------------------------------------------------- 219 以道殉身
o = head_("以 道 殉 身", "《孟子》尽心上　第二百一十九章　MZ219", h)
o += [T(380, 112, "天下有道，以道殉身；天下无道，以身殉道", 5.9, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 162, "殉 者，以 死 随 物 之 名", 6.2, INK, ls=2)]
o += [P("M 380,200 L 380,366", INK, 1.3)]
o += [T(380, 388, "道", 7.4, ZONG, ls=1)]
# 左：有道
o += [T(206, 202, "天 下 有 道", 5.2, GREY, ls=1)]
o += [stand(226, 404, 110, INK, 1.2)]
o += [arrow(262, 346, 366, 346, ZONG, 1.1, 4)]
o += [T(226, 424, "以 道 殉 身", 5.4, ZONG, ls=1)]
o += [T(236, 372, "身 出 则 道 在 必 行", 4.7, ZONG, ls=1)]
# 右：无道
o += [T(552, 202, "天 下 无 道", 5.2, GREY, ls=1)]
o += [stand(534, 404, 110, INK, 1.2)]
o += [arrow(498, 346, 394, 346, ZHE, 1.1, 4)]
o += [T(534, 424, "以 身 殉 道", 5.4, ZHE, ls=1)]
o += [T(524, 372, "道 屈 则 身 在 必 退", 4.7, ZHE, ls=1)]
o += [P("M 180,428 L 568,428", LINE, 0.9, "none", "4,4")]
o += [T(380, 434, "未 闻 以 道 殉 乎 人 者 也", 4.8, GREY, ls=1)]
o += tail10(h, "天下有道，以道殉身；天下无道，以身殉道。", "图一百三十", "以道殉身", "ch219a")
save("ch219a-yidao-xunshen.svg", o)

# ---------------------------------------------------------- 220 五挟不答
o = head_("五 挟 不 答", "《孟子》尽心上　第二百二十章　MZ220", h)
o += [T(380, 112, "挟贵、挟贤、挟长、挟勋劳、挟故而问，皆所不答也", 5.7, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 164, "有 所 挟，则 受 道 之 心 不 专", 6.0, INK, ls=2)]
bx = [136, 222, 462, 548, 634]
bt = ["贵", "贤", "长", "勋", "故"]
for i in range(5):
    o += [R(bx[i], 344, 70, 60, WARM, 1.1, fill=SOFT)]
    o += [T(bx[i] + 35, 386, bt[i], 10.5, ZONG)]
    o += [T(bx[i] + 35, 332, "挟", 5.2, GREY, ls=1)]
o += [stand(380, 404, 116, INK, 1.3)]
o += [T(438, 330, "不 答", 6.0, ZHE, ls=1)]
# 滕更有二
o += [C(179, 356, 2.6, ZHE, 1.0, ZHE), C(265, 356, 2.6, ZHE, 1.0, ZHE)]
o += [T(214, 424, "滕 更 有 二 焉", 4.8, ZHE, ls=1)]
o += [T(600, 424, "挟 者 五，一 无 所 受", 4.6, GREY, ls=1)]
o += tail10(h, "挟贵而问，挟贤而问，皆所不答也。滕更有二焉。", "图一百三十一", "五挟不答", "ch220a")
save("ch220a-wuxie-buda.svg", o)

# ---------------------------------------------------------- 221 进锐退速
o = head_("进 锐 退 速", "《孟子》尽心上　第二百二十一章　MZ221", h)
o += [T(380, 112, "于不可已而已者，无所不已；于所厚者薄，无所不薄也", 5.6, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 168, "三 者 之 弊，同 归 于 废 弛", 6.2, INK, ls=2)]
# 左：路断（不可已而已）
o += [L(140, 368, 196, 368, WARM, 1.3), L(140, 390, 196, 390, WARM, 1.3)]
o += [L(216, 368, 272, 368, WARM, 1.3), L(216, 390, 272, 390, WARM, 1.3)]
o += [L(196, 366, 196, 392, LINE, 0.9), L(216, 366, 216, 392, LINE, 0.9)]
o += [T(206, 384, "止", 6.6, ZHE, ls=1)]
o += [T(206, 424, "于 不 可 已 而 已", 4.9, INK, ls=1)]
# 中：尖峰
o += [P("M 312,392 L 392,248 L 472,394", ZHE, 1.4)]
o += [C(392, 248, 4, ZHE, 1.0, ZHE)]
o += [T(392, 232, "锐", 6.4, ZHE, ls=1)]
o += [T(392, 424, "其 进 锐 者，其 退 速", 4.9, INK, ls=1)]
# 右：厚薄
o += [R(512, 336, 104, 22, WARM, 1.1, SOFT)]
o += [R(512, 378, 104, 12, WARM, 1.1, SOFT)]
o += [T(500, 352, "厚", 5.4, ZONG, ls=1, anchor="end")]
o += [T(500, 392, "薄", 5.4, ZONG, ls=1, anchor="end")]
o += [T(564, 424, "于 所 厚 者 薄", 4.9, INK, ls=1)]
o += tail10(h, "其进锐者，其退速。", "图一百三十二", "进锐退速", "ch221a")
save("ch221a-jinrui-tuikuai.svg", o)

# ---------------------------------------------------------- 222 亲亲仁民
o = head_("亲 亲 仁 民", "《孟子》尽心上　第二百二十二章　MZ222", h)
o += [T(380, 112, "君子之于物也，爱之而弗仁；于民也，仁之而弗亲", 5.6, GREY, ls=1)]
o += [T(380, 152, "理 一 而 分 殊", 6.6, INK, ls=2)]
o += [T(380, 170, "统 而 言 之 则 皆 仁，分 而 言 之 则 有 序", 4.7, GREY, ls=1)]
o += [C(380, 300, 40, ZONG, 1.1)]
o += [C(380, 300, 80, ZONG, 1.0)]
o += [C(380, 300, 118, GREY, 1.0)]
o += [T(380, 306, "亲", 8.0, ZONG, ls=1)]
o += [T(380, 242, "民", 7.2, GREY, ls=1)]
o += [T(380, 198, "物", 6.8, GREY, ls=1)]
o += [T(380, 430, "亲 亲 → 仁 民 → 爱 物", 4.9, ZONG, ls=1)]
o += tail10(h, "亲亲而仁民，仁民而爱物。", "图一百三十三", "亲亲仁民", "ch222a")
save("ch222a-qinqin-renmin.svg", o)

# ---------------------------------------------------------- 223 当务为急
o = head_("当 务 为 急", "《孟子》尽心上　第二百二十三章　MZ223", h)
o += [T(380, 112, "知者无不知也，当务之为急；仁者无不爱也，急亲贤之为务", 5.5, GREY, ls=1)]
o += [L(120, 404, 660, 404, WARM, 1.2)]
o += [T(380, 150, "尧 舜 之 知 而 不 遍 物，急 先 务 也", 4.8, GREY, ls=1)]
# 左：众务
for cx, cy, r in [(158, 384, 5), (188, 392, 4), (212, 376, 5), (240, 390, 4),
                  (176, 360, 4), (206, 350, 4), (232, 362, 5), (150, 356, 3)]:
    o += [C(cx, cy, r, GREY, 0.9)]
o += [T(196, 424, "遍 物", 5.0, GREY, ls=1)]
o += [arrow(258, 366, 316, 348, ZONG, 1.0, 4)]
# 右：先务
o += [C(400, 310, 58, ZONG, 1.3)]
o += [T(400, 318, "贤", 11.0, ZONG, ls=1)]
o += [T(400, 236, "当 务 之 为 急", 5.2, ZONG, ls=1)]
o += [T(400, 424, "亲 贤", 5.0, ZONG, ls=1)]
o += [T(576, 306, "不 能 三 年 之 丧", 4.7, GREY, ls=1)]
o += [T(576, 322, "而 缌 小 功 之 察", 4.7, GREY, ls=1)]
o += [T(576, 340, "是 之 谓 不 知 务", 4.7, ZHE, ls=1)]
o += tail10(h, "知者无不知也，当务之为急。", "图一百三十四", "当务为急", "ch223a")
save("ch223a-dangwu-weiji.svg", o)
