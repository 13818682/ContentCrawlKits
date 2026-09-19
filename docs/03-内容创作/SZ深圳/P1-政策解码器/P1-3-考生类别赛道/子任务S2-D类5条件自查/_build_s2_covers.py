# -*- coding: utf-8 -*-
"""P1-3 S2 D类5条件自查 封面 · 精简版（对齐 S5 定稿规范）

公众号 900×383（3行）+ 今日头条 1200×900。
钩子跨平台统一：「别等报名才翻材料」→ 精简为「先自查这3项 · 别等报名翻材料」
主标题=「D类报考的 5 个条件」（搜索向「非深户D类报考 5条件」）。
数字≤2。模板：_build_s5_*_simplified.py。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"

KICK = "5个条件缺一不可 · 现在先自查"   # 一句金钩


def base(w, h, gx=0.5, gy=0.16):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    g = np.exp(-(((x - w * gx) / (w * 0.34)) ** 2 + ((y - h * gy) / (h * 0.32)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-w * .18, -h * .10, w * .26, h * .18], fill=TOP + (36,))
    od.ellipse([w * .78, h * .80, w * 1.1, h * 1.08], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=None, min_size=18, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else 860
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


def pill(d, text, cy, size, w, pad=30):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > w - 220:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (w - tw) / 2 - pad, (w + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((w / 2, cy), text, font=f, fill=WHITE, anchor="mm")


# 公众号 900×383
W, H = 900, 383
im, d = base(W, H)
put(d, "深圳中考", (W / 2, 52), 40, GOLD, maxw=860, tag="gzh")
f = put(d, "D类报考的 5 个条件", (W / 2, 168), 56, WHITE, maxw=880, min_size=44, tag="gzh")
bb = d.textbbox((W / 2, 168), "D类报考的 5 个条件", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 230, W / 2 + half, 230], fill=GOLD, width=5)
put(d, "5个条件缺一不可 · 现在先自查", (W / 2, 312), 40, GOLD, maxw=880, min_size=34, tag="gzh")
im.save(HERE + "01.公众号/P1-3-S2-D类5条件自查-公众号-封面-精炼版-900x383.png")
print("saved S2 公众号封面")

# 头条 1200×900
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
f = put(d, "D类报考的 5 个条件", (W / 2, 360), 120, WHITE, maxw=1120, min_size=90, tag="tt")
bb = d.textbbox((W / 2, 360), "D类报考的 5 个条件", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 490, W / 2 + half, 490], fill=GOLD, width=6)
put(d, "社保满3年 · 居住证有效 · 租赁凭证 · 3年学籍", (W / 2, 640), 66, GOLD, maxw=1100, min_size=50, tag="tt")
put(d, "数据来源：深圳市教育局公开信息 · 人工核对（2026参考）", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt")
im.save(HERE + "02.今日头条/P1-3-S2-D类5条件自查-头条-封面-精炼版-1200x900.png")
print("saved S2 头条封面")

# 小红书 1080×1440（精简版）
W, H = 1080, 1440
im, d = base(W, H, gy=0.12)
put(d, "深圳中考", (W / 2, 180), 96, GOLD, maxw=1000, tag="xhs")
f = put(d, "非深户≠没书读", (W / 2, 560), 132, WHITE, maxw=1000, min_size=100, tag="xhs")
bb = d.textbbox((W / 2, 560), "非深户≠没书读", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 690, W / 2 + half, 690], fill=GOLD, width=8)
put(d, "D类报考 5个条件 · 缺一不可", (W / 2, 960), 68, GOLD, maxw=1000, min_size=56, tag="xhs")
put(d, "备考策略 · 收藏不迷路 · 数据见正文", (W / 2, 1360), 30, SUB, bold=False, maxw=980, min_size=24, tag="xhs")
im.save(HERE + "04.小红书/P1-3-S2-D类5条件自查-小红书-封面-精炼版-1080x1440.png")
print("saved S2 小红书封面")
print("done")
