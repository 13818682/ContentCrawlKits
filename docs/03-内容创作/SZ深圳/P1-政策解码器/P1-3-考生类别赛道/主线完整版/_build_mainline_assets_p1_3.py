# -*- coding: utf-8 -*-
"""P1-3 主线完整版 封面生成 · 精简版规范（2026-09-06 对齐 S5 定稿）

公众号 900×383（严格3行）+ 今日头条 1200×900（pill42/主标题124/1句金钩/来源）。
钩子跨平台统一：「先弄清是哪一类，再谈分数」（顺序错位反差，0数字，最聚焦）。
主标题=已定 A 标题核心「AC类还是D类？」。
模板：S5 公众号/头条精简版 _build_s5_*_simplified.py（2026-09-05 用户定稿规范）
口径：ACD三类；D类5条件官方版；分差区间标2026参考。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"

# 精简版统一文案（跨平台）
KICK = "先弄清是哪一类，再谈分数"   # 一句金钩（公众号/头条统一）


def base(w, h, gx=0.5, gy=0.16, r1=True, r2=True):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    g = np.exp(-(((x - w * gx) / (w * 0.34)) ** 2 + ((y - h * gy) / (h * 0.32)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if r1: od.ellipse([-w * .18, -h * .10, w * .26, h * .18], fill=TOP + (36,))
    if r2: od.ellipse([w * .78, h * .80, w * 1.1, h * 1.08], fill=TOP + (22,))
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
f = put(d, "AC类还是D类？", (W / 2, 168), 56, WHITE, maxw=860, min_size=44, tag="gzh")
bb = d.textbbox((W / 2, 168), "AC类还是D类？", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 230, W / 2 + half, 230], fill=GOLD, width=5)
put(d, KICK, (W / 2, 312), 44, GOLD, maxw=880, min_size=36, tag="gzh")
im.save(HERE + "01.公众号/P1-3-主线完整版-AC类还是D类-公众号-封面-精炼版-900x383.png")
print("saved 公众号封面 精炼版")

# ---------- 今日头条 1200×900 · 封面1 主标题（精简版） ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
f = put(d, "AC类还是D类？", (W / 2, 360), 124, WHITE, maxw=1100, min_size=92, tag="tt1")
bb = d.textbbox((W / 2, 360), "AC类还是D类？", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 486, W / 2 + half, 486], fill=GOLD, width=6)
put(d, KICK, (W / 2, 630), 70, GOLD, maxw=1080, min_size=54, tag="tt1")
put(d, "数据来源：深圳市教育局公开信息 · 人工核对（2026参考）", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt1")
im.save(HERE + "02.今日头条/P1-3-主线完整版-AC类还是D类-头条-封面1-主标题-1200x900.png")
print("saved 头条封面1-主标题")

# ---------- 今日头条 · 封面2 数据对撞（54% vs 23%） ----------
im, d = base(W, H, gx=0.5, gy=0.2)
pill(d, "深圳中考 · 考生类别", 120, 42, W)
fN1 = 150; fL = 44
put(d, "54%", (W * 0.30, 430), fN1, GOLD, maxw=360, min_size=120, tag="tt2")
put(d, "考生是D类（非深户）", (W * 0.30, 560), fL, WHITE, maxw=420, min_size=36, tag="tt2")
put(d, "23%", (W * 0.70, 430), fN1, WHITE, maxw=360, min_size=120, tag="tt2")
put(d, "公办普高D类指标占比", (W * 0.70, 560), fL, WHITE, maxw=420, min_size=36, tag="tt2")
d.line([(W / 2, 330), (W / 2, 600)], fill=GOLD, width=4)
put(d, "半数以上的考生，抢不到两成半的公办指标", (W / 2, 730), 52, GOLD, maxw=1080, min_size=42, tag="tt2")
put(d, "数据来源：深圳市教育局公开信息 · 人工核对（2026参考）", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt2")
im.save(HERE + "02.今日头条/P1-3-主线完整版-AC类还是D类-头条-封面2-数据对撞-1200x900.png")
print("saved 头条封面2-数据对撞")

# ---------- 今日头条 · 封面3 答案/行动（先认赛道，再谈分数） ----------
im, d = base(W, H, gx=0.5, gy=0.2)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
put(d, "D类不是没路", (W / 2, 380), 132, WHITE, maxw=1100, min_size=100, tag="tt3")
put(d, "是路要选对", (W / 2, 560), 132, GOLD, maxw=1100, min_size=100, tag="tt3")
d.line([(W / 2 - 240, 660), (W / 2 + 240, 660)], fill=GOLD, width=5)
put(d, "指标生全覆盖 · 民办同分 · 3+4中本贯通", (W / 2, 730), 54, LIGHT, maxw=1100, min_size=44, tag="tt3")
put(d, "数据来源：深圳市教育局公开信息 · 人工核对（2026参考）", (W / 2, 858), 24, SUB, bold=False, min_size=18, tag="tt3")
im.save(HERE + "02.今日头条/P1-3-主线完整版-AC类还是D类-头条-封面3-答案行动-1200x900.png")
print("saved 头条封面3-答案行动")
print("done")
