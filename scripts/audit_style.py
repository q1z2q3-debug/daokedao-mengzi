#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""体例量化体检：逐章数「注家/不可/五问/跨典/存疑/双卡/读图」条目，找薄弱章。"""
import re, glob, os, json, collections

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECT_RE = re.compile(r'^##\s*[一二三四五六七八九十]+[、．]?\s*(.+?)\s*$', re.M)
rows = []
for f in sorted(glob.glob('book/MZ*.md')):
    t = open(f, encoding='utf-8').read()
    parts = SECT_RE.split(t)
    # parts = [前言, 节名1, 内容1, ...]
    sec = {}
    for i in range(1, len(parts), 2):
        sec[parts[i].strip()] = parts[i + 1]
    g = lambda k: sec.get(k, '')

    def count_lines(s):
        return len([l for l in s.split('\n') if l.strip().startswith('|') and not re.match(r'\s*\|[\s\-:|]+\|\s*$', l)])

    zj = g('注家')
    n_zhu = len(re.findall(r'朱[子熹]?[：:「]', zj)) + len(re.findall(r'朱熹', zj))
    n_zhao = len(re.findall(r'赵[岐氏]?[：:「]', zj)) + len(re.findall(r'赵岐', zj))
    bk = g('分寸与边界')
    n_bk = len(re.findall(r'不可', bk))
    sd = g('时代之问')
    n_wen = sd.count('？') + sd.count('?')
    kd = g('跨典')
    n_kd = len(re.findall(r'[《]', kd))
    cy = g('存疑')
    n_cy = len(re.findall(r'^[\-\*\d（(]', cy, re.M))
    dk = g('双卡与图')
    n_dk = count_lines(dk)
    rd = len(re.findall(r'读图', dk))
    rows.append({'f': os.path.basename(f), '注': n_zhu, '赵': n_zhao, '不可': n_bk, '问': n_wen,
                 '跨': n_kd, '疑': n_cy, '卡': n_dk, '读': rd,
                 '字': len(re.findall(r'[\u4e00-\u9fa5]', re.sub(r'^#.*$', '', t, flags=re.M)))})

def rep(key, lo, name):
    bad = [r for r in rows if r[key] < lo]
    print(f'-- {name}：低于 {lo} 的 {len(bad)} 章')
    for r in bad[:12]:
        print(f'   {r["f"]} {key}={r[key]} 字={r["字"]}')
    return bad

print('== 体例底线 ==')
bad1 = rep('注', 2, '注家（朱）条数')
bad2 = rep('不可', 5, '「不可」条数')
bad3 = rep('问', 5, '时代之问 问号')
bad4 = rep('疑', 5, '存疑条数')
bad5 = rep('读', 1, '读图标注')
bad6 = rep('卡', 6, '双卡表行数（表头+5 对）')
# 无赵岐对照
noz = [r['f'] for r in rows if r['赵'] == 0]
print(f'-- 无赵岐对照：{len(noz)} 章', noz[:10])
print()
print('== 篇幅后十 ==')
for r in sorted(rows, key=lambda x: x['字'])[:10]:
    print(f'   {r["字"]:5d} {r["f"]}')
json.dump(rows, open('.audit_rows.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('\n明细已存 .audit_rows.json')
