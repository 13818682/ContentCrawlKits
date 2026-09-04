# -*- coding: utf-8 -*-
"""P1-2 试点 · 小红书 Step1 封面PK 两候选（1080×1440 3:4）
A=互补版（封面标题=结论向，≠正文） / B=现状近似版（封面≈正文标题）
走 13-3 字号下限与留白（主标题 92-104px 级可上调；正文说明≥30px）。
不覆盖任何旧图。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.22) / (H * 0.30)) ** 2))
    a = a + np.array((190, 210, 235), float)[None, None, :] * (glow * 0.12)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-160, -120, 240, 220], fill=TOP + (40,))
    od.ellipse([W - 220, H - 260, W + 120, H + 60], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=W - 120, name=""):
    fpath = FB if bold else FR
    f = ImageFont.truetype(fpath, size)
    while f.size > 18:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(fpath, f.size - 1)
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


def pill(d, cy, text, size, w=W - 200):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    x0, x1 = (W - tw) / 2 - 46, (W + tw) / 2 + 46
    hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2,
                        outline=GOLD, width=3)
    d.text((W / 2, cy), text, font=f, fill=WHITE, anchor="mm")


def tag(d, text, y):
    f = ImageFont.truetype(FB, 34)
    d.text((W / 2, y), text, font=f, fill=GOLD, anchor="mm")
    tw = d.textlength(text, font=f)
    d.line([(W / 2 - tw / 2 - 4, y + 36), (W / 2 + tw / 2 + 4, y + 36)],
           fill=GOLD, width=4)


# ===== A 互补版（结论向） =====
im, d = base()
tag(d, "深圳中考 · 备考策略", 140)
put(d, "语数英物化", (W / 2, 360), 120, WHITE, True)
put(d, "440 分 · 主战场", (W / 2, 540), 118, GOLD, True)
put(d, "副科稳住就好", (W / 2, 720), 74, WHITE, True)
put(d, "历史70 + 道法50 + 体育50 ＝ 170", (W / 2, 880), 44, LIGHT, False)
pill(d, 1060, "实验今年20分 · 多出的8分要动手练", 38)
put(d, "备考策略 · 收藏不迷路 · 数据见正文", (W / 2, 1290), 30, SUB, False)
im.save(OUT + "科目性价比-封面A-互补版-1080x1440.png")
print("saved A")

# ===== B 现状近似版（封面≈正文标题） =====
im, d = base()
tag(d, "深圳中考 · 备考策略", 140)
put(d, "同样的复习时间", (W / 2, 360), 96, WHITE, True)
put(d, "花在哪科涨分最快？", (W / 2, 530), 106, GOLD, True)
put(d, "语数英物化440 · 实验+8分 · 副科170", (W / 2, 760), 42, LIGHT, False)
pill(d, 1060, "实验今年20分 · 多出的8分要动手练", 38)
put(d, "备考策略 · 收藏不迷路 · 数据见正文", (W / 2, 1290), 30, SUB, False)
im.save(OUT + "科目性价比-封面B-现状近似版-1080x1440.png")
print("saved B")
print("done")
