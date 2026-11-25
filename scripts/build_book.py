#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建《润泽说 道可道之孟子》卷首页与站首页。

源：book/*.md（前言、序、体例、卷表）；章文件 book/MZ###-*.md（有则并入目录）
产出：docs/book.html（封面·扉页·前言·序·体例·卷表）、docs/index.html（目录入口）
用法：python3 scripts/build_book.py
"""
import os, re, subprocess, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import daokedao_book as kit  # noqa: E402

SITE = "https://q1z2q3-debug.github.io/daokedao-mengzi"
REPO = "https://github.com/q1z2q3-debug/daokedao-mengzi"
VER = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
DATE = "2026-11-23"
CSS = open(os.path.join(ROOT, "scripts/_style.css"), encoding="utf-8").read()
book = os.path.join(ROOT, "book")
docs = os.path.join(ROOT, "docs")


def md2html(path):
    """pandoc 转 html 片段，去 wrapper。"""
    out = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5",
                          "--no-highlight", path],
                         capture_output=True, text=True, check=True).stdout
    return out


COVER = kit.cover(
    title="孟子",
    tag="七 篇 · 十 四 卷",
    seal="仁",
    gatha_first=("民为贵", "君为轻"),
    gatha_second=("富贵不能淫", "威武不能屈"),
    meta=["底本　朱熹《孟子集注》", "参校　《孟子注疏》赵岐注 孙奭疏",
          "体例　七篇十四卷 · 一章十二节", "v" + VER + " · 二〇二六"],
)

FRONTIS = kit.frontis(
    title="润泽说 道可道之孟子",
    sub="孟子 · 通释读本",
    lines=[
        ("底本", "朱熹《四书章句集注·孟子集注》，七篇十四卷，二百六十章"),
        ("参校", "《孟子注疏》赵岐注、孙奭疏（注家分歧逐章入「存疑」）"),
        ("体例", "一章一页；每章十二节；孟子三判：驳谁／立什么／留给后人什么"),
        ("章次", "MZ001–MZ261，按篇卷序连排"),
        ("图", "义理图手写 SVG，一图一文件，纸墨五色"),
        ("版本", "v%s · 二〇二六" % VER),
    ],
)

SECTIONS = [("前言", "前言-读孟子之前.md"), ("序", "序-为什么读孟子.md"),
            ("体例", "体例.md"), ("卷表", "卷表.md")]
body = []
for name, fn in SECTIONS:
    p = os.path.join(book, fn)
    if os.path.exists(p):
        body.append('<section class="ch" id="%s">%s</section>' % (name, md2html(p)))

SHELL_OLD = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>润泽说 道可道之孟子 · 卷首</title>
<style>%std,th{padding:4px 16px 4px 0;}table{border-collapse:collapse;}th{font-weight:600;color:#7C6D5C}</style>
</head>
<body>
<div class="bar"><div><a href="index.html">← 目录</a></div><div>润 泽 说 · 道 可 道 之 孟 子　卷首</div></div>
<div class="wrap">
%s
%s
%s
</div>
<div class="foot"><div>润泽说 道可道之孟子 · 卷首　v%s　（%s）</div>
<div>底本：朱熹《四书章句集注·孟子集注》　参校：《孟子注疏》赵岐注、孙奭疏</div>
<div><a href="index.html">目录</a><a href="%s">GitHub</a></div></div>
</body>
</html>
""" % (CSS, COVER, FRONTIS, "\n".join(body), VER, DATE, REPO)

TPL = open(os.path.join(ROOT, "scripts/_shell_book.html"), encoding="utf-8").read()
SHELL = (TPL.replace("__COVER__", COVER).replace("__FRONTIS__", FRONTIS)
            .replace("__BODY__", "\n".join(body))
            .replace("__VER__", VER).replace("__DATE__", DATE))
os.makedirs(docs, exist_ok=True)
open(os.path.join(docs, "book.html"), "w", encoding="utf-8").write(SHELL)

# 首页：卷表 + 入口 + 已成章清单
ch_files = sorted(glob.glob(os.path.join(book, "MZ*.md")))
rows = []
for f in ch_files:
    b = os.path.basename(f)[:-3]
    m = re.match(r"(MZ\d{3})-(.+)", b)
    rows.append((m.group(1), m.group(2)))
chs = "".join('<li><a href="ch/%s.html">%s　%s</a></li>' % (i.lower(), i, t) for i, t in rows) \
      or '<li class="todo">正文尚未开笔——按卷推进，第一卷「梁惠王上」在建。</li>'

VOLTABLE = "\n".join("<tr><td>%s</td><td>%s</td><td>%d</td><td>%s–%s</td></tr>" % (
    v["卷"], v["篇"], v["章数"], v["起"], v["止"]) for v in json.load(open(os.path.join(book, "chapters.json"), encoding="utf-8"))["volumes"])

INDEX = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>润泽说 道可道之孟子</title>
<style>%s</style>
</head>
<body>
<div class="bar"><div></div><div>润 泽 说 · 道 可 道 之 孟 子</div></div>
<div class="wrap">
<h1 class="ch">润泽说 道可道之孟子</h1>
<p>七篇十四卷，二百六十章。底本朱熹《孟子集注》。一章一页，每章十二节，另立「孟子三判」：此章驳谁、立什么、留给后人什么。</p>
<p><a href="book.html">▸ 进入卷首（封面 · 扉页 · 前言 · 序 · 体例 · 卷表）</a></p>
<h2>已成之章</h2>
<ul class="list">%s</ul>
<h2>七篇十四卷</h2>
<table class="t" style="width:auto;min-width:560px"><thead><tr><th style="width:64px">卷</th><th style="width:150px">篇</th><th style="width:88px">章数</th><th>章号</th></tr></thead>
<tbody>
%s
</tbody></table>
<div class="foot"><div>润泽说 道可道之孟子　v%s　（%s）</div>
<div><a href="book.html">卷首</a><a href="%s">GitHub</a></div></div>
</div>
</body>
</html>
""" % (CSS, chs, VOLTABLE, VER, DATE, SITE)

open(os.path.join(docs, "index.html"), "w", encoding="utf-8").write(INDEX)
open(os.path.join(docs, "robots.txt"), "w", encoding="utf-8").write(
    "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
# sitemap 由 build_site.py 统一生成（含章页），此处不再覆盖
print("卷首页 %s 字节；首页已写；已成章 %d" % (
    os.path.getsize(os.path.join(docs, "book.html")), len(ch_files)))
