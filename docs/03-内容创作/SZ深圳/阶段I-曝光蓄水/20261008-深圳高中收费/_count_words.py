# -*- coding: utf-8 -*-
"""发布稿净字数实测（口径：2026-09-27 定）

去除 markdown 标记与空白后的可见字符数，**不含「数据来源」行**。
正文＝文稿里第一个 ``` 代码块（发布正文）。只读，不改稿。
"""
import sys, re, os, glob

sys.stdout.reconfigure(encoding="utf-8")

FENCE = chr(96) * 3


def net(path):
    t = open(path, encoding="utf-8").read()
    blocks = re.findall(FENCE + r"\n(.*?)\n" + FENCE, t, re.S)
    if not blocks:
        return None
    # 小红书文稿含 标题/封面文案/发布正文 三块，取最长的那块＝发布正文
    body = max(blocks, key=len)
    lines = [l for l in body.split("\n")
             if not l.strip().startswith("数据来源")]
    s = "\n".join(lines)
    s = re.sub(r"^#+\s*", "", s, flags=re.M)
    s = re.sub("[" + chr(96) + r"*>]", "", s)
    s = re.sub(r"\s+", "", s)
    return len(s)


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    par = os.path.dirname(base)
    for d in sorted(glob.glob(os.path.join(par, "2026100*"))):
        for p in sorted(glob.glob(os.path.join(d, "2026*.md"))):
            n = net(p)
            print(f"{n if n is not None else '?':>5}  {os.path.basename(p)}")
