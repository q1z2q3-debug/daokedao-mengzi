#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书体检：正文体例 / 图位键 / 图文件 / 章页产物 / 元数据。只读，不改任何文件。"""
import json, os, re, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

chs = json.load(open('book/chapters.json', encoding='utf-8'))
books = sorted(glob.glob('book/MZ*.md'))
figs = sorted(glob.glob('assets/fig/*.svg'))
pages = sorted(glob.glob('docs/ch/*.html'))

issues = collections.defaultdict(list)

# ---------- 正文 ----------
SECT = ['本章导读', '经文', '字义与句读', '今译', '章旨', '注家', '分寸与边界', '义理', '时代之问', '跨典', '存疑', '双卡与图']
allfigs_in_body = set()
WORDS = []
for f in books:
    t = open(f, encoding='utf-8').read()
    name = os.path.basename(f)
    # 章节标题层级
    for s in SECT:
        if not re.search(r'^##\s*[一二三四五六七八九十]+[、．]?\s*' + s, t, re.M):
            issues['缺节'].append(f'{name} 缺「{s}」')
    # 图位
    keys = re.findall(r'\{\{fig:([^|}]+)\|', t)
    if len(keys) == 0:
        issues['图位'].append(f'{name} 无图位')
    for k in keys:
        allfigs_in_body.add(k)
        if not glob.glob(f'assets/fig/{glob.escape(k)}-*.svg'):
            issues['图位'].append(f'{name} 图位键 {k} 无对应 SVG')
        num = int(name[2:5])
        want = 'ch%02da' % num
        if k != want:
            issues['图位'].append(f'{name} 图位键 {k}，按章号应为 {want}')
    # 长段/异常
    body = re.sub(r'^#.*$', '', t, flags=re.M)
    words = len(re.findall(r'[\u4e00-\u9fa5]', body))
    WORDS.append((words, name))
    # 半角标点混入（中文正文里的 , . ; :）
    bad = re.findall(r'[\u4e00-\u9fa5][,.;:](?=[\u4e00-\u9fa5])', body)
    if len(bad) > 3:
        issues['标点'].append(f'{name} 中文句间半角标点 {len(bad)} 处')
    # 禁词/占位
    for pat in ['TODO', '待补', 'XXX', 'placeholder', 'lorem']:
        if pat in t:
            issues['占位'].append(f'{name} 含 {pat}')
    # 未闭合花括号
    if body.count('{{') != body.count('}}'):
        issues['括号'].append(f'{name} {{ }} 不配对 {body.count("{{")}/{body.count("}}")}')

# ---------- 元数据 ----------
meta = chs['chapters']
if len(meta) != 261:
    issues['元数据'].append(f'chapters 条数 {len(meta)}')
for c in meta:
    n = c.get('id', '')
    m = re.match(r'MZ(\d+)$', str(n))
    if not m:
        issues['元数据'].append(f'章号异常 {n}')
        continue
    i = int(m.group(1))
    pg = c.get('page')
    if pg != 'ch/mz%03d.html' % i:
        issues['元数据'].append(f'{n} page={pg}')
    if c.get('state') != '已成':
        issues['元数据'].append(f'{n} state={c.get("state")}')
    if not c.get('章题'):
        issues['元数据'].append(f'{n} 无章题')
    if not os.path.exists('book/MZ%03d-' % i) and not glob.glob('book/MZ%03d-*.md' % i):
        issues['元数据'].append(f'{n} 无正文文件')

# 章页
for p in pages:
    if 'fig:' in open(p, encoding='utf-8').read():
        issues['章页'].append(f'{p} 残留未替换图位')
if len(pages) != 261:
    issues['章页'].append(f'章页数 {len(pages)}')

# ---------- SVG ----------
for f in figs:
    s = open(f, encoding='utf-8').read()
    name = os.path.basename(f)
    vb = re.search(r'viewBox="([^"]+)"', s)
    if not vb or vb.group(1) != '0 0 760 540':
        issues['SVG尺寸'].append(f'{name} viewBox={vb.group(1) if vb else "无"}')
    if s.count('<path') > 400:
        issues['SVG体量'].append(f'{name} path {s.count("<path")}')
    # 越界粗查：只在无变换的顶层坐标系上判（<g transform> 内是局部坐标，不适用）
    top = re.sub(r'<g\b[^>]*>.*?</g>', '', s, flags=re.S)
    for m in re.finditer(r'\b(cx|cy)="(-?[\d.]+)"', top):
        v = float(m.group(2))
        if (m.group(1) == 'cx' and (v > 760 or v < 0)) or (m.group(1) == 'cy' and (v > 540 or v < 0)):
            issues['SVG越界'].append(f'{name} {m.group(1)}={v}')
            break
    # 直接引用外部资源
    s2 = s.replace('http://www.w3.org/2000/svg', '')
    if 'http://' in s2 or 'https://' in s2:
        issues['SVG外链'].append(name)
    if '@import' in s or '<image' in s:
        issues['SVG外链'].append(name)

used = set()
for x in figs:
    used.add(os.path.basename(x).split('-')[0])
print('== 统计 ==')
print('正文', len(books), '· 图', len(figs), '· 章页', len(pages), '· 元数据', len(meta))
WORDS.sort()
print('篇幅：最短', WORDS[0], '中位', WORDS[len(WORDS)//2], '最长', WORDS[-1])
print('图位键被正文引用', len(allfigs_in_body), '/ 图文件', len(used), '未引用图', len(used - allfigs_in_body))
if used - allfigs_in_body:
    print('  未引用：', sorted(used - allfigs_in_body)[:10])
print()
for k, v in issues.items():
    print(f'== {k} （{len(v)}）')
    for line in v[:25]:
        print('  ', line)
    if len(v) > 25:
        print('   … 余', len(v) - 25, '条')
print()
print('FAIL合计', sum(len(v) for v in issues.values()))
