# -*- coding: utf-8 -*-
"""S6 公众号封面 两版（900×383）
版A「完整版」= 现有 4 行模板：深圳中考 / 主题句 / 说明句 / 钩子句。
版B「精炼版」= 深圳中考 + 第二句主题保留 + 第三/四句整合为 1 句钩子（吸引点击）。
封面第一眼=深圳中考+问题；数字≤2。口径：生地不计入630、同分先比生地。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 900, 383
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.18) / (H * 0.34)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .10, W * .26, H * .18], fill=TOP + (36,))
    od.ellipse([W * .78, H * .80, W * 1.1, H * 1.08], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=860, min_size=24, tag=""):
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


def line(d, cy, cx=W // 2, half=None):
    if half is None:
        half = d.textbbox((0, 0), "主", font=ImageFont.truetype(FB, 40))[2] // 2 + 30
    d.line([cx - half, cy, cx + half, cy], fill=GOLD, width=4)


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 10 or bb[1] < 4 or bb[2] > W - 10 or bb[3] > H - 4:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| texts:", len(BADS), bad if bad else "")
    BADS.clear()


# ============ 版A 完整版（4行模板） ============
im, d = base()
put(d, "深圳中考", (W / 2, 44), 40, GOLD, tag="A")
f = put(d, "生地不计分，却先定录取", (W / 2, 152), 52, WHITE, maxw=860, min_size=40)
bb = d.textbbox((W / 2, 152), "生地不计分，却先定录取", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 206, W / 2 + half, 206], fill=GOLD, width=4)
put(d, "总分相同时 · 先比生地 · 高者进", (W / 2, 262), 34, LIGHT, bold=False, maxw=860, tag="A")
put(d, "生地 96 vs 82 · 差 1 分定一个学位", (W / 2, 336), 32, GOLD, maxw=860, tag="A")
im.save(HERE + "S6-不计分的隐形战场-公众号-封面-900x383.png")
check("版A 完整版")

# ============ 版B 精炼版（3行：深圳中考+主题+整合钩子） ============
im, d = base()
put(d, "深圳中考", (W / 2, 52), 40, GOLD, tag="B")
f = put(d, "生地不计分，却先定录取", (W / 2, 170), 56, WHITE, maxw=860, min_size=44)
bb = d.textbbox((W / 2, 170), "生地不计分，却先定录取", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 232, W / 2 + half, 232], fill=GOLD, width=5)
put(d, "高 1 分，也能定学位", (W / 2, 310), 46, GOLD, maxw=880, min_size=38, tag="B")
im.save(HERE + "S6-不计分的隐形战场-公众号-封面-精炼版-900x383.png")
check("版B 精炼版")
print("done")
