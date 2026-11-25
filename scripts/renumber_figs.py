#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图号统一：MZ090–MZ261 的「图N」整体后移 89，使全书图号＝章号。
只改正文 {{fig}} caption / 图位行 / SVG 尾部署名；dry-run 默认。"""
import re, glob, os, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRY = '--apply' not in sys.argv

D = {c: i for i, c in enumerate('零一二三四五六七八九')}
D['〇'] = 0


def cn2int(s):
    total = 0
    if '百' in s:
        pre, post = s.split('百', 1)
        total += (D[pre] if pre else 1) * 100
        s = post
    if '十' in s:
        pre, post = s.split('十', 1)
        total += (D[pre] if pre else 1) * 10
        s = post
    if s:
        total += D[s[0]]
    return total


def int2cn(n):
    if n < 10:
        return '一二三四五六七八九'[n - 1]
    if n < 20:
        return '十' + ('一二三四五六七八九'[n - 11] if n > 10 else '')
    if n < 100:
        a, b = divmod(n, 10)
        return '一二三四五六七八九'[a - 1] + '十' + ('一二三四五六七八九'[b - 1] if b else '')
    a, b = divmod(n, 100)
    s = '一二三四五六七八九'[a - 1] + '百'
    if b == 0:
        return s
    if b < 10:
        return s + '零' + '一二三四五六七八九'[b - 1]
    c, d = divmod(b, 10)
    return s + '一二三四五六七八九'[c - 1] + '十' + ('一二三四五六七八九'[d - 1] if d else '')


changed = 0
samples = []
for f in sorted(glob.glob('book/MZ*.md')):
    n = int(os.path.basename(f)[2:5])
    s = open(f, encoding='utf-8').read()
    def rep(m):
        if cn2int(m.group(1)) == n:
            return m.group(0)
        return '图' + int2cn(n)
    new = re.sub(r'图([一二三四五六七八九十百零〇]+)(?=[｜·])', rep, s)
    if new != s:
        changed += 1
        if len(samples) < 3:
            for a, b in zip(s.split('\n'), new.split('\n')):
                if a != b:
                    samples.append((os.path.basename(f), a.strip()[:80], b.strip()[:80]))
        if not DRY:
            open(f, 'w', encoding='utf-8').write(new)

sv = 0
for f in sorted(glob.glob('assets/fig/*.svg')):
    n = int(re.match(r'ch(\d+)a', os.path.basename(f)).group(1))
    s = open(f, encoding='utf-8').read()
    def rep(m):
        if cn2int(m.group(1)) == n:
            return m.group(0)
        return '图' + int2cn(n) + ' ·'
    new = re.sub(r'图([一二三四五六七八九十百零〇]+)\s*·', rep, s)
    if new != s:
        sv += 1
        if not DRY:
            open(f, 'w', encoding='utf-8').write(new)

print(('【预演】' if DRY else '【已改】'), '正文', changed, '章 · SVG', sv, '张')
for x in samples:
    print(' 旧：', x[1])
    print(' 新：', x[2])
