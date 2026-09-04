# -*- coding: utf-8 -*-
"""S1 公众号封面 900×383（v2）：第一眼=深圳中考；主句=问题+承诺；等式不上封面"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107); LIGHT = (157, 184, 212); SUB = (201, 217, 232)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 900, 383
T = np.array(TOP, float); B = np.array(BOT, float)
t = np.linspace(0, 1, H)[:, None, None]
a = T[None, None, :] * (1 - t) + B[None, None, :] * t
a = np.repeat(a, W, axis=1)
y, x = np.mgrid[0:H, 0:W]
g = np.exp(-(((x - W * 0.5) / (W * 0.30)) ** 2 + ((y - H * 0.14) / (H * 0.40)) ** 2))
a = a + np.array((180, 205, 235), float)[None, None, :] * (g * 0.10)[..., None]
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
d = ImageDraw.Draw(im)


def put(txt, xy, size, fill, maxw=860):
    f = ImageFont.truetype(FB, size)
    while f.size > 12:
        bb = d.textbbox((0, 0), txt, font=f, anchor="mm")
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(FB, f.size - 1)
    d.text(xy, txt, font=f, fill=fill, anchor="mm")
    return f


# 第一眼：深圳中考（大金字 + 下划线）
fk = put("深圳中考", (W / 2, 62), 58, GOLD)
tw = d.textlength("深圳中考", font=fk)
d.line([(W / 2 - tw / 2 - 6, 122), (W / 2 + tw / 2 + 6, 122)], fill=GOLD, width=6)
# 主句（问题）+ 承诺
put("8科怎么考、怎么给分？", (W / 2, 216), 52, WHITE)
put("630分拆解 · 一张表看懂", (W / 2, 316), 40, GOLD)
im.save(OUT + "S1-630构成与科目分值-公众号-封面-900x383.png")
print("saved S1 公众号封面 v2")
