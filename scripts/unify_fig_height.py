# -*- coding: utf-8 -*-
"""把全书 SVG 画幅统一到体例 760×540：内容按比例归入 [20,520]，字号同比补偿，边框重设。"""
import glob, re, os, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPLY = '--apply' in sys.argv
W, H = 760, 540

for f in sorted(glob.glob('assets/fig/*.svg')):
    s = open(f, encoding='utf-8').read()
    m = re.search(r'viewBox="0 0 760 (\d+)"', s)
    if not m:
        print('跳过（无标准 viewBox）', os.path.basename(f))
        continue
    h = int(m.group(1))
    if h == H:
        continue
    core = s.strip()
    if core.endswith('</svg>'):
        core = core[: -len('</svg>')]
    lines = core.split('\n')
    head, body = lines[:4], lines[4:]
    sy = (H - 40) / (h - 40)
    ty = 20 - 20 * sy

    def fsz(x):
        return 'font-size="%.2f"' % (float(x.group(1)) * (1 / sy))

    body_txt = '\n'.join(body)
    body_txt = re.sub(r'font-size="([0-9.]+)"', fsz, body_txt)
    head[0] = re.sub(r'viewBox="0 0 760 \d+"', 'viewBox="0 0 760 %d"' % H, head[0])
    head[0] = re.sub(r'height="\d+"', 'height="%d"' % H, head[0])
    head[1] = re.sub(r'height="\d+"', 'height="%d"' % H, head[1])
    head[2] = re.sub(r'height="\d+"', 'height="%d"' % (H - 40), head[2])
    head[3] = re.sub(r'height="\d+"', 'height="%d"' % (H - 48), head[3])
    new = ('\n'.join(head)
           + '\n  <g transform="translate(0,%.3f) scale(1,%.6f)">\n' % (ty, sy)
           + body_txt
           + '\n  </g>\n</svg>\n')
    if APPLY:
        open(f, 'w', encoding='utf-8').write(new)
    print(('改' if APPLY else '预览'), os.path.basename(f), h, '->', H, 'sy=%.3f' % sy)
