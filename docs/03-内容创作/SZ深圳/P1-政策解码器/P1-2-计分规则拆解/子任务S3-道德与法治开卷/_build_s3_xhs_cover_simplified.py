# -*- coding: utf-8 -*-
"""S3 小红书封面 精简版（1080×1440，对齐公众号/头条精简理念，D3互补）
深圳中考标识 + 大字主题（白）+ 金线下一句钩子 + 底注。
把原互补版三层（大字/金句/浅句）压缩为：主题「道法，改开卷」+ 钩子「能带书≠能得分·会查才得分」。
封面结论向≠正文标题（问题向），符合 D3。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.32)) ** 2 + ((y - H * 0.14) / (H * 0.30)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .07, W * .24, H * .15], fill=TOP + (34,))
    od.ellipse([W * .80, H * .86, W * 1.1, H * 1.05], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=None, min_size=24, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else W - 140
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 15 or bb[1] < 6 or bb[2] > W - 15 or bb[3] > H - 6:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| texts:", len(BADS), bad if bad else "")
    BADS.clear()


# ---------- S3 小红书封面 精简版 ----------
im, d = base()
f = put(d, "深圳中考", (W / 2, 170), 96, GOLD, maxw=940, min_size=70, tag="s3x")
bb = d.textbbox((W / 2, 170), "深圳中考", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 285, W / 2 + half, 285], fill=GOLD, width=8)
f2 = put(d, "道法，改开卷", (W / 2, 560), 148, WHITE, maxw=960, min_size=110, tag="s3x")
bb2 = d.textbbox((W / 2, 560), "道法，改开卷", font=f2, anchor="mm")
half2 = (bb2[2] - bb2[0]) / 2 + 8
d.line([W / 2 - half2, 716, W / 2 + half2, 716], fill=GOLD, width=6)
put(d, "能带书 ≠ 能得分 · 会查才得分", (W / 2, 880), 68, GOLD, maxw=940, min_size=54, tag="s3x")
put(d, "备考策略 · 收藏不迷路 · 数据见正文", (W / 2, 1360), 26, SUB, bold=False, min_size=20, tag="s3x")
im.save(HERE + "04.小红书/S3-道德与法治开卷-小红书-封面-精炼版-1080x1440.png")
check("S3 小红书封面 精简版")
print("done")
