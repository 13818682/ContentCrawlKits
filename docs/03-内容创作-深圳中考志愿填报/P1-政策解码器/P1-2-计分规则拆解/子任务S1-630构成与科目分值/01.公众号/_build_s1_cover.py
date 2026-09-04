# -*- coding: utf-8 -*-
"""S1 公众号封面 900×383：信息前置（结论可对账口径为视觉焦点）"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 900, 383
T = np.array(TOP, float); B = np.array(BOT, float)
t = np.linspace(0, 1, H)[:, None, None]
a = T[None, None, :] * (1 - t) + B[None, None, :] * t
a = np.repeat(a, W, axis=1)
y, x = np.mgrid[0:H, 0:W]
g = np.exp(-(((x - W * 0.5) / (W * 0.30)) ** 2 + ((y - H * 0.16) / (H * 0.42)) ** 2))
a = a + np.array((180, 205, 235), float)[None, None, :] * (g * 0.10)[..., None]
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
d = ImageDraw.Draw(im)


def put(txt, xy, size, fill, bold=True, maxw=850):
    fpath = FB if bold else "C:/Windows/Fonts/msyh.ttc"
    f = ImageFont.truetype(fpath, size)
    while f.size > 14:
        bb = d.textbbox((0, 0), txt, font=f, anchor="mm")
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(fpath, f.size - 1)
    d.text(xy, txt, font=f, fill=fill, anchor="mm")
    return f


fk = put("深圳中考", (W / 2, 46), 44, GOLD)
tw = d.textlength("深圳中考", font=fk)
d.line([(W / 2 - tw / 2 - 5, 92), (W / 2 + tw / 2 + 5, 92)], fill=GOLD, width=5)
put("630分怎么来？一张表看懂", (W / 2, 172), 52, WHITE)
put("440笔试＋20实验＋170史道体 ＝ 630", (W / 2, 300), 38, GOLD, True, 840)
im.save(OUT + "S1-630构成与科目分值-公众号-封面-900x383.png")
print("saved S1 公众号封面")
