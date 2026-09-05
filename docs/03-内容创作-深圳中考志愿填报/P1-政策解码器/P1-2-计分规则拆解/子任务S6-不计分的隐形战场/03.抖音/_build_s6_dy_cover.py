# -*- coding: utf-8 -*-
"""S6 抖音首图 精简版（1080×1920，安全区：右≤950／下正文≤1590）
深圳中考 + 生地不计分却先定录取 + 高1分也能定学位（与公众号/头条/小红书精简版同款文案）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.16) / (H * 0.30)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .06, W * .24, H * .14], fill=TOP + (36,))
    od.ellipse([W * .80, H * .85, W * 1.1, H * 1.04], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=800, min_size=40, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def pill(d, text, cy, size, pad=30):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > W - 200:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (W - tw) / 2 - pad, (W + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((W / 2, cy), text, font=f, fill=WHITE, anchor="mm")


def check(name, right_limit=950, bottom_limit=1600):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 20 or bb[1] < 8 or bb[2] > right_limit or bb[3] > bottom_limit:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| texts:", len(BADS), bad if bad else "")
    BADS.clear()


im, d = base()
pill(d, "深圳中考 · 政策解码器", 150, 40)
f = put(d, "生地不计分", (W / 2, 560), 100, WHITE, maxw=820, min_size=72)
bb = d.textbbox((W / 2, 560), "生地不计分", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 700, W / 2 + half, 700], fill=GOLD, width=7)
put(d, "却先定录取", (W / 2, 870), 66, GOLD, maxw=820, min_size=50)
put(d, "同分先比生地 · 高 1 分也能定学位", (W / 2, 1080), 44, LIGHT, bold=False, maxw=840, min_size=36)
pill(d, "关注我 · P1-2 收官", 1500, 40)
im.save(HERE + "S6-不计分的隐形战场-抖音-首图-1080x1920.png")
check("S6 抖音首图 精简版")
print("done")
