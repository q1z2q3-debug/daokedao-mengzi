#!/usr/bin/env python3
"""孟子库站点构建：book/MZ###-*.md → docs/ch/mz###.html，并重写 sitemap。

图以 {{fig:键|caption}} 占位，构建时内联 assets/fig/<键>*.svg（单文件自包含，无外链）。
用法：python3 scripts/build_site.py
"""
import datetime, glob, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
FIG = os.path.join(ROOT, "assets", "fig")
DOCS = os.path.join(ROOT, "docs")
SITE = "https://q1z2q3-debug.github.io/daokedao-mengzi"
VER = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
DATE = datetime.date.today().isoformat()

EXTRA = """
table{border-collapse:collapse;margin:18px 0;font-size:14.5px;line-height:1.8;width:100%}
table th,table td{padding:8px 16px 8px 0;text-align:left;vertical-align:top;border-bottom:1px solid #E7E0D4}
table th{color:#994433;font-weight:600;letter-spacing:.06em}
figure.fig{margin:26px 0 8px;padding:0;overflow-x:auto;-webkit-overflow-scrolling:touch}
figure.fig svg{width:100%;height:auto;display:block}
figure.fig figcaption{font-size:12.5px;color:#7C6D5C;letter-spacing:.08em;margin-top:8px;text-align:center}
figure.fig figcaption a{color:#994433;text-decoration:none;border-bottom:1px solid #DCD5C8}
@media (max-width:640px){figure.fig figcaption{font-size:11.5px;padding:0 8px}
figure.fig svg{width:620px;max-width:none;margin:0 4px}}
"""


BASE = "https://q1z2q3-debug.github.io/daokedao-mengzi/"


def head(path="book.html", desc=None):
    shell = open(os.path.join(ROOT, "scripts/_shell_book.html"), encoding="utf-8").read()
    h = shell[:shell.index("</head>") + 7]
    h = re.sub(r"<title>.*?</title>", "<title>__TITLE__</title>", h, count=1, flags=re.S)
    h = re.sub(r'<link rel="canonical" href="[^"]*">',
               '<link rel="canonical" href="%s%s"><meta property="og:url" content="%s%s">'
               % (BASE, path, BASE, path), h, count=1)
    if desc:
        h = re.sub(r'<meta name="description" content="[^"]*">',
                   '<meta name="description" content="%s">' % desc, h, count=1)
        h = re.sub(r'<meta property="og:description" content="[^"]*">',
                   '<meta property="og:description" content="%s">' % desc, h, count=1)
    return h.replace("</style>", EXTRA + "</style>")


def fig_inline(key, caption):
    hits = sorted(glob.glob(os.path.join(FIG, key + "*.svg")))
    if not hits:
        return '<p class="todo">（缺图：%s）</p>' % key
    svg = open(hits[0], encoding="utf-8").read()
    name = os.path.basename(hits[0])
    return ('<figure class="fig">%s<figcaption>%s　<a href="../assets/fig/%s" target="_blank" rel="noopener">原图 ↗</a></figcaption></figure>'
            % (svg, caption, name))


def main():
    d = json.load(open(os.path.join(BOOK, "chapters.json"), encoding="utf-8"))
    os.makedirs(os.path.join(DOCS, "ch"), exist_ok=True)
    pages = []
    for ch in d["chapters"]:
        hits = sorted(glob.glob(os.path.join(BOOK, ch["id"] + "-*.md")))
        if not hits:
            continue
        md = hits[0]
        title = os.path.basename(md)[:-3].split("-", 1)[1]
        raw = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--no-highlight", md],
                             capture_output=True, text=True, check=True).stdout
        raw = re.sub(r"<p>\s*\{\{fig:([a-z0-9]+)\|([^}]+)\}\}\s*</p>",
                     lambda m: fig_inline(m.group(1), m.group(2)), raw)
        raw = re.sub(r"\{\{fig:([a-z0-9]+)\|([^}]+)\}\}",
                     lambda m: fig_inline(m.group(1), m.group(2)), raw)
        raw = raw.replace("<h1>", '<h1 class="ch">', 1)
        page = "ch/%s.html" % ch["id"].lower()
        desc = "《孟子》%s·%s：经文本义、赵岐与朱子注、义理与时代之问，一页一章。" % (ch["篇"], title)
        doc = (head(page, desc).replace("__TITLE__", "润泽说 道可道之孟子 · %s %s" % (ch["id"], title))
               + '<body>\n<div class="bar"><div><a href="../index.html">← 目录</a></div>'
                 '<div><span class="bname">润 泽 说 · 道 可 道 之 孟 子　</span>%s</div></div>\n' % ch["id"]
               + '<div class="wrap">\n' + raw + '\n'
               + '<div class="foot"><div>润泽说 道可道之孟子　v%s　（%s）</div>'
                 '<div><a href="../book.html">卷首</a><a href="../index.html">目录</a>'
                 '<a href="https://github.com/q1z2q3-debug/daokedao-mengzi">GitHub</a></div></div>\n'
                 '</div>\n</body>\n</html>\n' % (VER, DATE))
        open(os.path.join(DOCS, page), "w", encoding="utf-8").write(doc)
        ch["page"] = page
        ch["章题"] = title
        ch["state"] = "已成"
        pages.append(page)

    urls = ['<url><loc>%s/</loc><priority>1.0</priority><lastmod>%s</lastmod></url>' % (SITE, DATE),
            '<url><loc>%s/book.html</loc><priority>0.9</priority><lastmod>%s</lastmod></url>' % (SITE, DATE)]
    for p in pages:
        urls.append('<url><loc>%s/%s</loc><priority>0.8</priority><lastmod>%s</lastmod></url>' % (SITE, p, DATE))
    open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  '
        + "\n  ".join(urls) + "\n</urlset>\n")
    json.dump(d, open(os.path.join(BOOK, "chapters.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # 图另存一份到站内，供 SVG 直链
    dest = os.path.join(DOCS, "assets", "fig")
    os.makedirs(dest, exist_ok=True)
    n_fig = 0
    for f in sorted(os.listdir(FIG)):
        if f.endswith(".svg"):
            shutil.copyfile(os.path.join(FIG, f), os.path.join(dest, f))
            n_fig += 1
    print("图另存 %d 张到 docs/assets/fig" % n_fig)
    print("章页 %d 张：%s" % (len(pages), "、".join(pages) or "无"))


if __name__ == "__main__":
    sys.exit(main())
