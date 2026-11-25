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
"""尽心下 图 145–154（v0.31.0 首批十图）
跨批 helper 不复用：本文件内重定义 plate/step/shad/foot/wind/plate_glyph。
"""


def plate(x, y, w, hh, label, col=ZONG, sw=1.3):
    """牌：方框＋内字。"""
    return [R(x, y, w, hh, col, sw, fill=SOFT),
            T(x + w / 2, y + hh / 2 + 3.6, label, 9.0, col, ls=2)]


def step(x, y, w, hh, label):
    """台阶一级：横长条＋面上字。"""
    return [R(x, y, w, hh, ZONG, 1.2, fill=SOFT),
            L(x, y, x + w, y, ZONG, 1.5),
            T(x + w / 2, y + hh - 8, label, 8.0, INK, ls=3)]


def shad(x, fy, H, kind="bent"):
    """虚影人：全虚线，bent 弯背，arm 并臂。"""
    top = fy - H
    hr = max(4, H * 0.07)
    o = [C(x, top + hr, hr, LINE, 0.9),
         P(f"M {x},{top+hr*2} L {x},{fy-H*0.22}", LINE, 0.9, "none", "3,3,0.1")]
    if kind == "bent":
        o += [P(f"M {x},{top+hr*2} L {x+H*0.12},{top+H*0.34}", LINE, 0.9, "none", "3,3,0.1"),
              P(f"M {x},{top+H*0.36} L {x-H*0.10},{top+H*0.52}", LINE, 0.9, "none", "3,3,0.1"),
              P(f"M {x},{top+H*0.52} L {x-H*0.07},{fy}", LINE, 0.9, "none", "3,3,0.1")]
    else:
        o += [P(f"M {x},{top+hr*2} L {x-H*0.09},{top+H*0.34}", LINE, 0.9, "none", "3,3,0.1"),
              P(f"M {x},{top+hr*2} L {x+H*0.04},{top+H*0.36}", LINE, 0.9, "none", "3,3,0.1"),
              P(f"M {x},{top+H*0.54} L {x-H*0.06},{fy}", LINE, 0.9, "none", "3,3,0.1"),
              P(f"M {x},{top+H*0.54} L {x+H*0.06},{fy}", LINE, 0.9, "none", "3,3,0.1")]
    return o


def foot(x, y, w=4.6):
    """足迹：一枚小椭圆。"""
    return E(x, y, w, w * 0.55, WARM, 0.7, WARM)


def wind(x, y1, y2, col=ZONG, sw=0.8):
    """风弧：自像下垂三道竖曲。"""
    d = y2 - y1
    return [P(f"M {x-9},{y1} C {x-16},{y1+d*0.35} {x-4},{y1+d*0.65} {x-9},{y2}", col, sw),
            P(f"M {x},{y1} C {x-7},{y1+d*0.35} {x+5},{y1+d*0.65} {x},{y2}", col, sw),
            P(f"M {x+9},{y1} C {x+2},{y1+d*0.35} {x+14},{y1+d*0.65} {x+9},{y2}", col, sw)]


def mouth(x, y, s=26, hh=18):
    """口：小方框内一字。"""
    return [R(x - s / 2, y - hh / 2, s, hh, ZONG, 1.0, fill=PALE),
            T(x, y + 3.0, "口", 7.4, ZONG, ls=1)]


h = 540

# 图一百四十五 · 让千乘之国
o = head_("让 千 乘 之 国", "《孟子》尽心下　第二百三十四章　MZ234", h)
o += [T(380, 112, "好名之人，能让千乘之国；苟非其人，箪食豆羹见于色", 6.0, ZONG, ls=1.4)]
o += [stand(268, 404, 130, INK, 1.2, arms="point")]
o += [plate(352, 286, 156, 68, "千 乘 之 国")]
o += [L(352, 320, 336, 322, GREY, 0.7)]
o += [bowl(356, 376, 26, 8)]
o += [E(410, 380, 12, 5.4, ZONG, 1.0, SOFT)]
o += [C(368, 368, 2.0, ZHE, 0.8, ZHE)]
o += [T(300, 268, "双手推出", 4.8, GREY, ls=0)]
o += [T(356, 400, "豆", 5.0, ZONG, ls=1)]
o += [T(410, 400, "箪", 5.0, ZONG, ls=1)]
o += [T(500, 366, "碗沿一点，藏不住", 4.6, ZHE, ls=0)]
o += [T(230, 430, "大处是他用力之处", 4.8, WARM, ls=0.5)]
o += [T(540, 430, "小处是他不经意之处", 4.8, WARM, ls=0.5)]
o += tail_(h, "看人不在其所勉，而在其所忽。", "图一百四十五", "让千乘之国", "ch234a")
save("ch234a-hao-ming-zhi-ren.svg", o)

# 图一百四十六 · 国空虚
o = head_("国 空 虚", "《孟子》尽心下　第二百三十五章　MZ235", h)
o += [T(380, 112, "不信仁贤，则国空虚；无礼义，则上下乱；无政事，则财用不足", 6.0, ZONG, ls=1.4)]
o += [R(170, 168, 420, 226, INK, 1.3, PALE)]
o += [L(170, 168, 590, 168, INK, 1.3)]
o += [L(310, 168, 310, 394, GREY, 0.9)]
o += [L(450, 168, 450, 394, GREY, 0.9)]
o += [T(240, 190, "信仁贤", 5.4, ZONG, ls=1)]
o += [T(380, 190, "礼义", 5.4, ZONG, ls=1)]
o += [T(520, 190, "政事", 5.4, ZONG, ls=1)]
# 左格：空墙与两枚足迹
o += [L(196, 352, 284, 352, GREY, 1.0)]
o += [foot(232, 380), foot(252, 380)]
o += [T(240, 330, "若无人然", 5.0, WARM, ls=1)]
# 中格：一正一倒
o += [C(380, 246, 4.0, ZONG, 0.9), L(380, 242, 380, 206, ZONG, 1.0),
      L(380, 206, 372, 196, ZONG, 0.9), L(380, 206, 388, 196, ZONG, 0.9)]
o += [stand(380, 378, 64, INK, 1.0)]
o += [T(332, 236, "上下倒", 4.6, WARM, ls=0.5)]
# 右格：空碗
o += [bowl(520, 348, 24, 8)]
o += [C(534, 340, 2.0, ZHE, 0.8, ZHE)]
o += [T(520, 372, "财用不足", 4.8, WARM, ls=1)]
o += [T(380, 418, "三症一因：三者以仁贤为本", 6.2, INK, ls=1.6)]
o += tail_(h, "人、序、财三症，根只有一个：信不信仁贤。", "图一百四十六", "国空虚", "ch235a")
save("ch235a-bu-xin-renxian.svg", o)

# 图一百四十七 · 不仁得国
o = head_("不 仁 得 国", "《孟子》尽心下　第二百三十六章　MZ236", h)
o += [T(380, 112, "不仁而得国者，有之矣；不仁而得天下，未之有也", 6.0, ZONG, ls=1.4)]
o += [plate(150, 288, 108, 52, "国")]
o += [L(324, 286, 266, 298, INK, 1.5), L(266, 298, 258, 290, INK, 1.1),
      L(266, 298, 256, 300, INK, 1.1), L(266, 298, 260, 306, INK, 1.1)]
o += [T(216, 272, "私智", 5.0, WARM, ls=1)]
o += [T(204, 356, "可盗", 5.2, ZHE, ls=1)]
o += [C(556, 300, 78, INK, 1.3)]
o += [L(506, 300, 606, 300, GREY, 0.9)]
o += [T(556, 268, "天下", 6.4, ZONG, ls=3)]
o += [T(556, 392, "丘民之心", 5.2, WARM, ls=1)]
o += [P("M 318,300 L 388,300", LINE, 1.0, "none", "6,4")]
o += [P("M 418,300 L 470,300", LINE, 1.0, "none", "6,4")]
o += [T(404, 288, "未 之 有", 6.4, ZHE, ls=2)]
o += [T(760 / 2, 424, "得而复失，犹不得也", 6.0, ZONG, ls=2)]
o += tail_(h, "小国可以盗，天下只能得。", "图一百四十七", "不仁得国", "ch236a")
save("ch236a-bu-ren-de-guo.svg", o)

# 图一百四十八 · 民为贵
o = head_("民 为 贵", "《孟子》尽心下　第二百三十七章　MZ237", h)
o += [T(380, 112, "民为贵，社稷次之，君为轻", 6.0, ZONG, ls=1.6)]
o += [step(320, 168, 120, 26, "君")]
o += [step(250, 194, 260, 26, "社 稷")]
o += [R(180, 220, 400, 26, ZONG, 1.4, SOFT), L(180, 220, 580, 220, ZONG, 1.8),
      T(380, 240, "民", 11.0, INK, ls=5)]
o += [L(180, 246, 180, 404, ZONG, 1.2)]
o += [L(180, 404, 580, 404, ZONG, 1.4)]
o += [T(600, 178, "系于二者", 4.8, WARM, ls=0)]
o += [T(540, 204, "为民而立", 4.8, WARM, ls=0)]
o += [T(380, 270, "得乎丘民而为天子", 5.2, ZHE, ls=1.4)]
o += [arrow(660, 392, 660, 180, ZHE, 1.2)]
o += [T(688, 292, "贵", 8.0, ZHE, ls=1)]
o += [T(380, 424, "越宽越在下——位置不是权利，是职责", 6.2, INK, ls=1.4)]
o += tail_(h, "位置尽不了职，位置就收回。", "图一百四十八", "民为贵", "ch237a")
save("ch237a-min-wei-gui.svg", o)

# 图一百四十九 · 百世之师
o = head_("百 世 之 师", "《孟子》尽心下　第二百三十八章　MZ238", h)
o += [T(380, 112, "圣人，百世之师也，伯夷、柳下惠是也", 6.0, ZONG, ls=1.4)]
o += [stand(230, 190, 74, INK, 1.1)]
o += [L(216, 112, 244, 112, ZONG, 1.2)]
o += [stand(530, 190, 74, INK, 1.1)]
o += [L(514, 160, 500, 268, ZONG, 0.9), L(546, 160, 560, 268, ZONG, 0.9)]
o += [T(230, 208, "伯夷", 5.6, ZONG, ls=2)]
o += [T(530, 208, "柳下惠", 5.6, ZONG, ls=2)]
o += [wind(230, 222, 300)]
o += [wind(530, 222, 300)]
o += [T(230, 322, "闻伯夷之风者", 4.6, WARM, ls=0.5)]
o += [T(530, 322, "闻柳下惠之风者", 4.6, WARM, ls=0.5)]
# 左组：弯背旧形 → 直立新形
o += [shad(196, 404, 84, "bent")]
o += [arrow(226, 350, 254, 350, ZHE, 1.0, 4)]
o += [stand(282, 404, 92, INK, 1.1)]
o += [T(196, 424, "顽夫·懦夫", 4.6, WARM, ls=0)]
o += [T(282, 424, "廉·有立志", 4.8, ZHE, ls=0)]
# 右组：并臂旧形 → 展臂新形
o += [shad(448, 404, 84, "arm")]
o += [arrow(478, 350, 506, 350, ZHE, 1.0, 4)]
o += [stand(534, 404, 92, INK, 1.1, arms="point")]
o += [T(448, 424, "薄夫·鄙夫", 4.6, WARM, ls=0)]
o += [T(534, 424, "敦·宽", 4.8, ZHE, ls=0)]
o += [T(380, 424, "百世之下，闻者莫不兴起", 6.2, INK, ls=2)]
o += tail_(h, "君靠位，师靠风；风隔百世还吹。", "图一百四十九", "百世之师", "ch238a")
save("ch238a-baishi-zhi-shi.svg", o)

# 图一百五十 · 仁也者人也
o = head_("仁 也 者 人 也", "《孟子》尽心下　第二百三十九章　MZ239", h)
o += [T(380, 112, "仁也者，人也。合而言之，道也", 6.2, ZONG, ls=2)]
o += [C(380, 300, 116, ZONG, 1.2)]
o += [T(380, 178, "道", 10.0, ZONG, ls=2)]
o += [C(380, 262, 11, INK, 1.2)]
o += [L(380, 274, 380, 292, INK, 1.2)]
o += [L(348, 300, 412, 300, INK, 1.2)]
o += [L(348, 300, 332, 338, INK, 1.0), L(412, 300, 428, 338, INK, 1.0)]
o += [L(362, 316, 352, 404, INK, 1.2), L(398, 316, 408, 404, INK, 1.2)]
o += [L(380, 292, 380, 314, INK, 0.9)]
o += [T(380, 344, "仁", 12.0, ZHE, ls=2)]
o += [T(380, 366, "人之所以为人之理", 4.4, WARM, ls=0)]
o += [T(380, 428, "理在物上，才成道", 5.8, INK, ls=1.6)]
o += tail_(h, "理不落物是空的，物不合理是野的。", "图一百五十", "仁也者人也", "ch239a")
save("ch239a-ren-ye-zhe-ren.svg", o)

# 图一百五十一 · 迟迟吾行
o = head_("迟 迟 吾 行", "《孟子》尽心下　第二百四十章　MZ240", h)
o += [T(380, 112, "去父母国，迟迟吾行；去他国，接淅而行", 6.0, ZONG, ls=1.4)]
o += [L(120, 404, 640, 404, ZONG, 1.4)]
o += [stand(220, 404, 122, INK, 1.2, arms="down")]

for i in range(7):
    o += [foot(246 + i * 8, 400 if i % 2 == 0 else 396, 4.2)]
o += [T(220, 250, "迟迟吾行也", 5.0, ZHE, ls=1.4)]
o += [stand(500, 404, 122, INK, 1.2, arms="point")]
o += [bowl(586, 340, 18, 6)]
o += [L(574, 358, 574, 368, GREY, 0.9), L(586, 360, 586, 372, GREY, 0.9), L(598, 358, 598, 368, GREY, 0.9)]
o += [T(600, 322, "接淅", 5.0, ZHE, ls=1)]
for i in range(3):
    o += [foot(368 + i * 44, 398, 4.6)]
o += [T(420, 250, "接淅而行", 5.0, ZHE, ls=1.4)]
o += [T(380, 428, "同一双脚，两种走法；差别只在脚下的土", 6.0, INK, ls=1.4)]
o += tail_(h, "去国有差等，亲疏定其迟速。", "图一百五十一", "迟迟吾行", "ch240a")
save("ch240a-chichi-wu-xing.svg", o)

# 图一百五十二 · 厄于陈蔡
o = head_("厄 于 陈 蔡", "《孟子》尽心下　第二百四十一章　MZ241", h)
o += [T(380, 112, "君子之戹于陈蔡之闲，无上下之交也", 6.0, ZONG, ls=1.4)]
o += [T(380, 178, "君", 6.4, WARM, ls=2)]
o += [R(180, 190, 400, 14, ZONG, 1.2, SOFT)]
o += [stand(380, 390, 116, INK, 1.2, arms="down")]
o += [R(180, 390, 400, 14, ZONG, 1.2, SOFT)]
o += [T(380, 422, "臣", 6.4, WARM, ls=2)]
o += [P("M 140,300 L 214,300", LINE, 1.0, "none", "5,4")]
o += [P("M 246,300 L 330,300", LINE, 1.0, "none", "5,4")]
o += [P("M 430,300 L 514,300", LINE, 1.0, "none", "5,4")]
o += [P("M 546,300 L 620,300", LINE, 1.0, "none", "5,4")]
o += [T(380, 224, "无 上 下 之 交", 5.8, ZHE, ls=2)]

o += tail_(h, "圣人之困，不在无道，在无交。", "图一百五十二", "厄于陈蔡", "ch241a")
save("ch241a-e-yu-chencai.svg", o)

# 图一百五十三 · 不理于口
o = head_("不 理 于 口", "《孟子》尽心下　第二百四十二章　MZ242", h)
o += [T(380, 112, "无伤也。士憎兹多口", 6.0, ZONG, ls=1.6)]
o += [stand(380, 404, 118, INK, 1.2, arms="down")]
o += mouth(250, 226) + [arrow(250, 240, 320, 292, ZHE, 0.9, 4)]
o += mouth(510, 226) + [arrow(510, 240, 440, 292, ZHE, 0.9, 4)]
o += mouth(206, 330) + [arrow(222, 330, 318, 340, ZHE, 0.9, 4)]
o += mouth(554, 330) + [arrow(538, 330, 442, 340, ZHE, 0.9, 4)]
o += mouth(380, 190) + [arrow(380, 204, 380, 268, ZHE, 0.9, 4)]
o += [T(250, 384, "忧心悄悄，愠于群小——孔子也", 4.8, WARM, ls=0.5)]
o += [T(380, 424, "肆不殄厥愠，亦不陨厥问——文王也", 5.0, INK, ls=0.8)]
o += tail_(h, "多口是士之常；被恼而不失声问。", "图一百五十三", "不理于口", "ch242a")
save("ch242a-da-bu-li-yu-kou.svg", o)

# 图一百五十四 · 以其昭昭
o = head_("以 其 昭 昭", "《孟子》尽心下　第二百四十三章　MZ243", h)
o += [T(380, 112, "贤者以其昭昭，使人昭昭；今以其昏昏，使人昭昭", 6.0, ZONG, ls=1.2)]
o += [stand(210, 404, 122, INK, 1.2, arms="down")]
o += [C(210, 266, 15, ZONG, 1.2)]
o += [L(224, 274, 292, 302, ZONG, 0.8), L(220, 282, 290, 314, ZONG, 0.7)]
o += [stand(316, 404, 100, INK, 1.1, arms="down")]
o += [C(316, 306, 6.4, ZONG, 0.9)]
o += [T(210, 240, "昭昭", 5.2, ZHE, ls=2)]
o += [P("M 388,180 L 388,404", LINE, 1.0, "none", "6,4")]
o += [stand(462, 404, 122, INK, 1.2, arms="point")]
o += [C(462, 268, 14, GREY, 0.9)]
o += [P("M 454,262 L 472,274", GREY, 0.8), P("M 456,274 L 468,262", GREY, 0.8),
      P("M 462,258 L 462,280", GREY, 0.8)]
o += [L(520, 340, 552, 336, INK, 1.0), L(552, 336, 552, 322, INK, 1.0)]
o += [P("M 544,322 L 560,322 L 556,334 L 548,334 Z", ZONG, 1.0, SOFT)]
o += [P("M 546,318 C 550,312 554,312 558,318", ZHE, 0.7),
      P("M 548,314 C 552,308 556,310 558,316", ZHE, 0.6)]
o += [L(568, 322, 592, 318, GREY, 0.9)]
o += [stand(614, 404, 96, GREY, 0.9)]
o += [C(614, 310, 5.4, GREY, 0.7)]
o += [T(462, 240, "昏昏", 5.2, WARM, ls=2)]
o += [T(676, 322, "仍暗", 4.8, WARM, ls=1)]
o += [T(380, 432, "先自昭，然后昭人", 6.2, INK, ls=2)]
o += tail_(h, "教的不是话，是人。", "图一百五十四", "以其昭昭", "ch243a")
save("ch243a-zhao-zhao-hun-hun.svg", o)
