# -*- coding: utf-8 -*-
"""S5 今日头条封面 精简版（1200×900，对齐公众号精简理念）
深圳中考 pill 保留 + 主题主标题保留放大 + 一句金色钩子 + 来源。
钩子整合原「别让任何一科掉C」与「省一级公办普高录取门槛」→「一科掉 C，就够不上省一级」。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1200, 900
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.16) / (H * 0.32)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .08, W * .24, H * .16], fill=TOP + (34,))
    od.ellipse([W * .80, H * .84, W * 1.1, H * 1.05], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=None, min_size=24, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else W - 120
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


def pill(d, text, cy, size, pad=30):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > W - 220:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (W - tw) / 2 - pad, (W + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((W / 2, cy), text, font=f, fill=WHITE, anchor="mm")


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 15 or bb[1] < 8 or bb[2] > W - 15 or bb[3] > H - 8:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| texts:", len(BADS), bad if bad else "")
    BADS.clear()


# ---------- S5 头条封面 精简版 ----------
im, d = base()
pill(d, "深圳中考 · 备考策略", 120, 42)
f = put(d, "A+ 永远是前 5%", (W / 2, 360), 124, WHITE, maxw=1100, min_size=92, tag="s5tt")
bb = d.textbbox((W / 2, 360), "A+ 永远是前 5%", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 486, W / 2 + half, 486], fill=GOLD, width=6)
put(d, "一科掉 C，就够不上省一级", (W / 2, 630), 70, GOLD, maxw=1080, min_size=54, tag="s5tt")
put(d, "数据来源：深圳市教育局公开信息 · 人工核对", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="s5tt")
im.save(HERE + "02.今日头条/S5-单科等级与省一级门槛-头条-封面-精炼版-1200x900.png")
check("S5 头条封面 精简版")
print("done")
