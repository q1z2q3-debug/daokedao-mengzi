#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""章页与重复句体检：导航链接、标题一致、跨章模板句滥用。"""
import re, glob, os, json, collections

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---- 章页导航 ----
bad = []
for i in range(1, 262):
    p = f'docs/ch/mz{i:03d}.html'
    s = open(p, encoding='utf-8').read()
    if i > 1 and f'mz{i-1:03d}.html' not in s:
        bad.append((p, '缺上一章链接'))
    if i < 261 and f'mz{i+1:03d}.html' not in s:
        bad.append((p, '缺下一章链接'))
    if 'assets/fig/ch%da-' % i not in s:
        bad.append((p, '缺图链接'))
    if '<title>' not in s or '孟子' not in s.split('<title>')[1][:80]:
        bad.append((p, 'title 异常'))
print('== 章页导航 ==', len(bad))
for b in bad[:20]:
    print('  ', b[0], b[1])

# ---- 元数据章题 vs 文件名 vs 页面标题 ----
meta = {c['id']: c for c in json.load(open('book/chapters.json', encoding='utf-8'))['chapters']}
mis = []
for f in sorted(glob.glob('book/MZ*.md')):
    name = os.path.basename(f)
    cid = name[:5]
    title = name[6:-3]
    m = meta[cid]
    if m['章题'] != title:
        mis.append((cid, m['章题'], title))
print('== 章题与文件名不一致 ==', len(mis))
for x in mis[:20]:
    print('  ', x)

# ---- 页面里的章题是否等于元数据 ----
pgmis = []
for cid, m in meta.items():
    s = open('docs/' + m['page'], encoding='utf-8').read()
    if m['章题'] not in s:
        pgmis.append((cid, m['章题']))
print('== 章题未出现于章页 ==', len(pgmis), pgmis[:10])

# ---- 重复句 ----
SECT_RE = re.compile(r'^##\s*[一二三四五六七八九十]+[、．]?\s*(.+?)\s*$', re.M)
sent_counter = collections.Counter()
where = collections.defaultdict(set)
for f in sorted(glob.glob('book/MZ*.md')):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'^#.*$', '', t, flags=re.M)
    for s in re.split(r'[。！？\n]', t):
        s = s.strip().strip('|').strip()
        if 8 <= len(s) <= 40 and re.search(r'[\u4e00-\u9fa5]', s):
            sent_counter[s] += 1
            where[s].add(os.path.basename(f)[:5])
rep = [(s, n) for s, n in sent_counter.items() if n >= 8]
print('== 跨章重复句（出现≥8次）==', len(rep))
for s, n in sorted(rep, key=lambda x: -x[1])[:15]:
    print(f'   {n}次 {len(where[s])}章  «{s}»')
