# -*- coding: utf-8 -*-
"""S3 公众号封面 精简版（900×383，3行，对齐 S4/S5/S6 精简版风格）
深圳中考保留 + 第二句主题保留（道德与法治·改开卷）+ 第三/四句整合为 1 句钩子：
  原第三句「能带书，≠能得分」（金句主体）× 原第四句「唯一能带纸质材料进考场的笔试」
  → 整合「能带书 ≠ 能得分 · 会查才得分」（反差+方法悬念，吸引点击）。
封面第一眼=深圳中考+问题；无数字，达标。
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


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 10 or bb[1] < 4 or bb[2] > W - 10 or bb[3] > H - 4:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| texts:", len(BADS), bad if bad else "")
    BADS.clear()


# ---------- S3 公众号封面 精简版（3行） ----------
im, d = base()
put(d, "深圳中考", (W / 2, 52), 40, GOLD, tag="s3b")
f = put(d, "道德与法治，改开卷", (W / 2, 170), 56, WHITE, maxw=860, min_size=44, tag="s3b")
bb = d.textbbox((W / 2, 170), "道德与法治，改开卷", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 232, W / 2 + half, 232], fill=GOLD, width=5)
put(d, "能带书 ≠ 能得分 · 会查才得分", (W / 2, 312), 44, GOLD, maxw=880, min_size=36, tag="s3b")
im.save(HERE + "S3-道德与法治开卷-公众号-封面-精炼版-900x383.png")
check("S3 公众号封面 精简版")
print("done")
