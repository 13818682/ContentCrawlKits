# -*- coding: utf-8 -*-
import json, glob, io, os
base = r"E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\scripts"
lines = []
for p in sorted(glob.glob(base + os.sep + "shot_batch_*.txt")):
    d = json.load(io.open(p, encoding="utf-8-sig"))
    shots = d["shots"]
    lines.append(os.path.basename(p) + " -> " + os.path.basename(d["src"]))
    for vp in ("desktop", "mobile"):
        s = shots.get(vp, {})
        rci = s.get("responsiveChartIssues", [])
        lines.append("   %s: rci=%d %s" % (vp, len(rci), rci[:3]))
with io.open(base + os.sep + "rci_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("written")
