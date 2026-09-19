# -*- coding: utf-8 -*-
"""ACD 封面 方案B · 归属定位式（一句话触发点）——待目检，不覆盖原图"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"


def base(w, h):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    dd = np.sqrt(((x - w * 0.15) / (w * 0.5)) ** 2 + ((y - h * 0.15) / (h * 0.5)) ** 2)
    a = a * (1 - 0.22 * np.clip(dd - 0.6, 0, None)[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([w - 300, -120, w + 100, 220], fill=TOP + (30,))
    od.ellipse([-140, h - 180, 150, h + 40], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, fnt, fill, maxw, name=""):
    f = fnt
    while maxw and f.size > 12:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(FB if f.path.endswith("msyhbd.ttc") else FR, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f, anchor="mm")
    x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
    x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
    if not (x0 >= -1 and x1 <= 901 and y0 >= -1 and y1 <= 384):
        print(f"[溢出] {name}: '{text}' 字{f.size} 盒{x0:.0f},{y0:.0f}->{x1:.0f},{y1:.0f}")
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


im, d = base(900, 383)
put(d, "深圳考生分 A C D 三类，你孩子是哪类？", (450, 160),
    ImageFont.truetype(FB, 48), WHITE, 850, "q")
put(d, "先定位，才知道能报哪些学校", (450, 272),
    ImageFont.truetype(FB, 40), GOLD, 700, "p")
im.save(OUT + "P1-1-子任务03-公众号封面-方案B-一句话-900x383.png")
print("saved 封面B(归属定位式)")
