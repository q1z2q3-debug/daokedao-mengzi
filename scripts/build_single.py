# -*- coding: utf-8 -*-
"""生成离线单文件全本 HTML：内联全部 261 页正文与图，带卷册目录，零外链。"""
import json, re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

meta = json.load(open('book/chapters.json', encoding='utf-8'))
ver = open('VERSION', encoding='utf-8').read().strip()

probe = open('docs/ch/mz001.html', encoding='utf-8').read()
css = re.search(r'<style>(.*?)</style>', probe, re.S).group(1)

def body(html):
    m = re.search(r'<div class="wrap">(.*?)\n<div class="foot">', html, re.S)
    t = m.group(1)
    t = re.sub(r'<a[^>]*>原图\s*↗?</a>', '', t)     # 离线无外部图，去掉直链
    t = re.sub(r'href="(?!\#)[^"]*"', 'href="#"', t)  # 其余站内链接降为空锚，免断链
    return t.strip()

chapters = meta['chapters']
groups = []
for c in chapters:
    key = (c['卷'], c['篇'])
    if not groups or groups[-1][0] != key:
        groups.append([key, []])
    groups[-1][1].append(c)

toc = ['<nav class="toc"><h1 class="title">润泽说 道可道之孟子</h1>',
       '<p class="sub">全本离线版　v%s　七篇十四卷　二百六十章（二百六十一页）</p>' % ver]
for (juan, pian), cs in groups:
    toc.append('<h3>%s · %s</h3><ul>' % (juan, pian))
    for c in cs:
        toc.append('<li>%03d　<a href="#mz%03d">%s</a></li>' % (int(c['id'][2:]), int(c['id'][2:]), c['章题']))
    toc.append('</ul>')
toc.append('</nav>')

secs = []
for c in chapters:
    html = open('docs/ch/' + c['page'].split('/')[-1], encoding='utf-8').read()
    secs.append('<section class="chap" id="mz%03d">%s</section>' % (int(c['id'][2:]), body(html)))

out = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>润泽说 道可道之孟子 · 全本离线版 v%s</title>
<meta name="author" content="润泽">
<style>
%s
.toc{max-width:780px;margin:0 auto;padding:40px 22px 24px;border-bottom:2px solid #DCD5C8}
.toc .sub{color:#7C6D5C;font-size:13px;letter-spacing:.08em}
.toc h3{margin:26px 0 6px}
.toc ul{list-style:none;padding:0;margin:0;columns:2;column-gap:28px}
.toc li{font-size:14px;line-height:1.9;color:#7C6D5C}
.chap{border-bottom:1px solid #E6E0D4;padding-top:8px}
.foot{max-width:780px;margin:0 auto;padding:24px 22px 60px;color:#7C6D5C;font-size:12px}
body{overflow-x:hidden}html{overflow-x:hidden}
.toc,.chap,.foot{max-width:100%%}
</style>
</head>
<body>
""" % (ver, css) + '\n'.join(toc) + '\n' + '\n'.join(secs) + """
<div class="foot">润泽说 道可道之孟子　全本离线版 v%s　%s　CC BY-NC-SA 4.0</div>
</body>
</html>
""" % (ver, '2026-11-26')

os.makedirs('dist', exist_ok=True)
fp = 'dist/道可道之孟子-v%s-全本离线.html' % ver
open(fp, 'w', encoding='utf-8').write(out)
print(fp, '%.1f MB' % (os.path.getsize(fp) / 1048576), '章', len(secs))
