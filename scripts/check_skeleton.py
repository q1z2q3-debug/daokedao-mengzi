#!/usr/bin/env python3
"""孟子库骨架自检：卷表—chapters.json—文档三处一账。正文落笔后另走 check_book.py。"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
fails, warns = [], []

def fail(m): fails.append(m)
def warn(m): warns.append(m)

def main():
    ver = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
    d = json.load(open(os.path.join(ROOT, "book/chapters.json"), encoding="utf-8"))
    chs = d["chapters"]
    if d["version"] != ver: fail("chapters.json 版本 %s ≠ VERSION %s" % (d["version"], ver))
    if len(chs) != 260: fail("章数 %d ≠ 260" % len(chs))
    ids = [c["id"] for c in chs]
    if ids != ["MZ%03d" % i for i in range(1, 261)]: fail("章号不是 MZ001–MZ260 连排")
    n = 0
    for v in d["volumes"]:
        got = [c["id"] for c in chs if c["卷"] == v["卷"]]
        if len(got) != v["章数"]: fail("卷%s 章数 %d ≠ %d" % (v["卷"], len(got), v["章数"]))
        if got[0] != v["起"] or got[-1] != v["止"]: fail("卷%s 章号区间不符" % v["卷"])
        n += v["章数"]
    if n != 260: fail("卷章数合计 %d ≠ 260" % n)
    # 卷表.md 与 chapters.json 一致
    jb = open(os.path.join(ROOT, "book/卷表.md"), encoding="utf-8").read()
    for v in d["volumes"]:
        if "卷%s　%s" % (v["卷"], v["篇"]) not in jb: fail("卷表缺 卷%s %s" % (v["卷"], v["篇"]))
    # 文档
    for f in ("book.html", "index.html"):
        p = os.path.join(DOCS, f)
        if not os.path.exists(p): fail("缺 docs/%s" % f); continue
        s = open(p, encoding="utf-8").read()
        if "__COVER__" in s or "__VER__" in s or "__BODY__" in s: fail("%s 有未替换占位符" % f)
        if re.search(r"<img|src=\"http", s): fail("%s 含位图或外链" % f)
        if "v" + ver not in s: warn("%s 未见当前版本号" % f)
    sm = open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8").read() if os.path.exists(os.path.join(DOCS, "sitemap.xml")) else ""
    if sm.count("<url>") < 2: fail("sitemap 不足 2 条")
    pages = [c["page"] for c in chs if c.get("page")]
    for p in pages:
        if p not in sm: fail("sitemap 缺 %s" % p)
    print(json.dumps({"version": ver, "chapters": len(chs), "已成": len(pages),
                      "FAIL": fails, "WARN": warns}, ensure_ascii=False, indent=1))
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
