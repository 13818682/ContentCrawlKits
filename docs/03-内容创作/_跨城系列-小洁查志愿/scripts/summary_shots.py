# -*- coding: utf-8 -*-
import json, glob, io, os
base = r"E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\scripts"
for p in sorted(glob.glob(base + os.sep + "shot_batch_*.txt")):
    d = json.load(io.open(p, encoding="utf-8-sig"))
    shots = d.get("shots", {})
    row = []
    for vp in ("desktop", "mobile"):
        s = shots.get(vp, {})
        row.append("%s: err=%d overflow=%d resErr=%d img=%d h=%d" % (
            vp,
            len(s.get("consoleErrors", [])),
            len(s.get("horizontalOverflow", [])),
            len(s.get("resourceErrors", [])),
            s.get("structure", {}).get("counts", {}).get("img", 0),
            s.get("structure", {}).get("fullpage", {}).get("h", 0)))
    print(os.path.basename(p), " || ".join(row))
