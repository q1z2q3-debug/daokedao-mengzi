#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SVG 图面体检：画幅、最小字号、越界文字、信息量。"""
import re, glob, os, collections

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = []
for f in sorted(glob.glob('assets/fig/*.svg')):
    s = open(f, encoding='utf-8').read()
    name = os.path.basename(f)
    vb = re.search(r'viewBox="0 0 760 (\d+)"', s)
    H = int(vb.group(1)) if vb else 0
    sizes = [float(x) for x in re.findall(r'font-size="([\d.]+)"', s)]
    texts = re.findall(r'<text[^>]*>([^<]*)</text>', s)
    # 真正有字的 text
    nt = len([t for t in texts if t.strip()])
    tiny = len([x for x in sizes if x < 5.5])
    over = 0
    for m in re.finditer(r'<text\s+x="(-?[\d.]+)"\s+y="([\d.]+)"[^>]*font-size="([\d.]+)"[^>]*>([^<]*)</text>', s):
        x, y, fs, txt = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        if not txt.strip():
            continue
        if y > H - 8 or x < 12 or x > 748:
            over += 1
    rows.append({'f': name, 'H': H, 'min': min(sizes) if sizes else 0, 'tiny': tiny, 'nt': nt, 'over': over})

print('== 画幅分布 ==', collections.Counter(r['H'] for r in rows))
print()
print('== 最小字号分布 ==', collections.Counter(r['min'] for r in rows).most_common())
print()
bad_tiny = [r for r in rows if r['tiny'] >= 3]
print('== 小字（<5.5）≥3 处的图 ==', len(bad_tiny))
for r in bad_tiny[:30]:
    print(f'   {r["f"]} 最小 {r["min"]} 小字处 {r["tiny"]} 文字条目 {r["nt"]}')
print()
bo = [r for r in rows if r['over']]
print('== 文字越界（贴边/出画）==', len(bo))
for r in bo[:20]:
    print('   ', r['f'], '越界条', r['over'], 'H', r['H'])
print()
thin = [r for r in rows if r['nt'] < 8]
print('== 图内文字条目 <8（信息偏少）==', len(thin), [r['f'] for r in thin][:12])
