# -*- coding: utf-8 -*-
import json, glob, io, os
base = r"E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\scripts"
for p in sorted(glob.glob(base + os.sep + "shot_batch_*.txt")):
    d = json.load(io.open(p, encoding="utf-8-sig"))
    s = d["shots"]["desktop"]["structure"]
    print(os.path.basename(p), "->", os.path.basename(d["src"]), "| title:", s["title"], "| img:", s["counts"]["img"], "| h1:", s.get("firstH1", "")[:30])
