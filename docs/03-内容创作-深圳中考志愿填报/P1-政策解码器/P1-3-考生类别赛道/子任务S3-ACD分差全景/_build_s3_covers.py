# -*- coding: utf-8 -*-
"""P1-3 S3 AC/D分差全景 封面 · 精简版（对齐 S5 定稿规范 + 头条3图规则 2026-09-06）

公众号 900×383（3行）+ 头条 1200×900（封面1主标题/封面2数据对撞/封面3答案行动）+ 小红书 1080×1440。
钩子跨平台统一：「四大0分 · 越往下差越大」。
主标题=「D类要多考多少分？」（数字0）。
模板：主线 _build_mainline_assets_p1_3.py（头条3封面）+ S2 _build_s2_covers.py。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"

KICK = "四大0分 · 越往下差越大"   # 一句金钩（跨平台统一）


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


# ---------- 公众号 900×383 精简版（3行） ----------
W, H = 900, 383
im, d = base(W, H)
put(d, "深圳中考", (W / 2, 52), 40, GOLD, maxw=860, tag="gzh")
f = put(d, "D类要多考多少分？", (W / 2, 170), 54, WHITE, maxw=880, min_size=44, tag="gzh")
bb = d.textbbox((W / 2, 170), "D类要多考多少分？", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 232, W / 2 + half, 232], fill=GOLD, width=5)
put(d, KICK, (W / 2, 314), 40, GOLD, maxw=880, min_size=34, tag="gzh")
im.save(HERE + "01.公众号/P1-3-S3-ACD分差全景-公众号-封面-精炼版-900x383.png")
print("saved 公众号封面 精炼版")

# ---------- 今日头条 1200×900 · 封面1 主标题 ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
f = put(d, "D类要多考多少分？", (W / 2, 368), 118, WHITE, maxw=1100, min_size=92, tag="tt1")
bb = d.textbbox((W / 2, 368), "D类要多考多少分？", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 496, W / 2 + half, 496], fill=GOLD, width=6)
put(d, KICK, (W / 2, 636), 68, GOLD, maxw=1100, min_size=54, tag="tt1")
put(d, "2026住宿线实测 · 深圳家长分五层看 · 来源：深圳市教育局", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt1")
im.save(HERE + "02.今日头条/P1-3-S3-ACD分差全景-头条-封面1-主标题-1200x900.png")
print("saved 头条封面1-主标题")

# ---------- 今日头条 · 封面2 数据对撞（0分 vs 23分） ----------
im, d = base(W, H, gx=0.5, gy=0.2)
pill(d, "深圳中考 · AC/D 分差", 120, 42, W)
put(d, "0 分", (W * 0.30, 430), 150, GOLD, maxw=380, min_size=120, tag="tt2")
put(d, "四大名校 D类同分进", (W * 0.30, 585), 46, WHITE, maxw=460, min_size=36, tag="tt2")
put(d, "23 分", (W * 0.70, 430), 150, WHITE, maxw=380, min_size=120, tag="tt2")
put(d, "公办边缘 深实崇文 506→529", (W * 0.70, 585), 42, WHITE, maxw=470, min_size=34, tag="tt2")
d.line([(W / 2, 300), (W / 2, 660)], fill=GOLD, width=4)
put(d, "D类的差距不在头部 · 在500分边缘段", (W / 2, 740), 54, GOLD, maxw=1100, min_size=44, tag="tt2")
put(d, "数据来源：深圳市教育局2026第一批录取标准·住宿线实测", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt2")
im.save(HERE + "02.今日头条/P1-3-S3-ACD分差全景-头条-封面2-数据对撞-1200x900.png")
print("saved 头条封面2-数据对撞")

# ---------- 今日头条 · 封面3 答案/行动（先分层·再对校查分差） ----------
im, d = base(W, H, gx=0.5, gy=0.2)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
put(d, "先分五层", (W / 2, 386), 128, WHITE, maxw=1100, min_size=100, tag="tt3")
put(d, "再对校查分差", (W / 2, 566), 128, GOLD, maxw=1100, min_size=100, tag="tt3")
d.line([(W / 2 - 260, 672), (W / 2 + 260, 672)], fill=GOLD, width=5)
put(d, "查目标校真实D线 · 别听“新校好考”", (W / 2, 750), 52, LIGHT, maxw=1100, min_size=42, tag="tt3")
put(d, "数据来源：深圳市教育局2026第一批录取标准·住宿线实测", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt3")
im.save(HERE + "02.今日头条/P1-3-S3-ACD分差全景-头条-封面3-答案行动-1200x900.png")
print("saved 头条封面3-答案行动")

# ---------- 小红书 1080×1440（精简版） ----------
W, H = 1080, 1440
im, d = base(W, H, gy=0.12)
put(d, "深圳中考", (W / 2, 180), 96, GOLD, maxw=1000, tag="xhs")
f = put(d, "D类要多考多少分？", (W / 2, 566), 120, WHITE, maxw=1000, min_size=100, tag="xhs")
bb = d.textbbox((W / 2, 566), "D类要多考多少分？", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 700, W / 2 + half, 700], fill=GOLD, width=8)
put(d, KICK, (W / 2, 966), 66, GOLD, maxw=1000, min_size=54, tag="xhs")
put(d, "分五层 · 收藏不迷路 · 数据2026实测", (W / 2, 1360), 30, SUB, bold=False, maxw=980, min_size=24, tag="xhs")
im.save(HERE + "04.小红书/P1-3-S3-ACD分差全景-小红书-封面-精炼版-1080x1440.png")
print("saved 小红书封面")
print("done")
