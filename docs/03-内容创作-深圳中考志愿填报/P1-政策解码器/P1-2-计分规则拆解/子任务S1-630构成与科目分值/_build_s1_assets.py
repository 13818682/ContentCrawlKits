# -*- coding: utf-8 -*-
"""S1 头条/抖音/小红书 三平台配图（口径可对账 440+20+170=630）"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"


def base(w, h, gx=0.5, gy=0.18):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    g = np.exp(-(((x - w * gx) / (w * 0.32)) ** 2 + ((y - h * gy) / (h * 0.34)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-w * .18, -h * .08, w * .24, h * .16], fill=TOP + (34,))
    od.ellipse([w * .80, h * .82, w * 1.1, h * 1.04], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, w, bold=True, maxw=None):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else w - 120
    while f.size > 16:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


def pill(d, text, cy, size, w, pad=34):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > w - 180:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (w - tw) / 2 - pad, (w + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((w / 2, cy), text, font=f, fill=WHITE, anchor="mm")


# ---- 头条封面 1200×900 ----
im, d = base(1200, 900)
pill(d, "深圳中考 · 备考策略", 120, 30, 1200, pad=30)
put(d, "630分怎么来的？", (600, 330), 104, WHITE, 1200, True, 1080)
put(d, "8 科作战表 · 口径可对账", (600, 500), 86, GOLD, 1200, True, 1080)
put(d, "440笔试 ＋ 20理化实验 ＋ 170史道体 ＝ 630", (600, 660), 48, LIGHT, 1200, False, 1080)
put(d, "数据来源：深圳市教育局公开信息 · 人工核对", (600, 852), 22, SUB, 1200, False)
im.save(HERE + "02.今日头条/S1-630构成-头条-封面-1200x900.png")
print("saved 头条封面")

# ---- 抖音首图 1080×1920（右≤950 / 内容≤y1590） ----
im, d = base(1080, 1920, 0.5, 0.16)
fk = put(d, "深圳中考", (520, 150), 56, GOLD, 1080, True, 800)
tw = d.textlength("深圳中考", font=fk); d.line([(520 - tw/2 - 5, 222), (520 + tw/2 + 5, 222)], fill=GOLD, width=6)
put(d, "630", (520, 470), 230, GOLD, 1080, True, 760)
put(d, "＝ 440笔试 ＋ 20实验 ＋ 170史道体", (520, 730), 54, WHITE, 1080, True, 800)
put(d, "8科分值一张表 · 收藏不迷路", (520, 940), 46, LIGHT, 1080, False, 800)
pill(d, "关注我 · 政策解码器继续讲", 1500, 40, 1080, pad=34)
im.save(HERE + "03.抖音/S1-630构成-抖音-首图-1080x1920.png")
print("saved 抖音首图")

# ---- 小红书封面（互补版·封面标题=结论向） 1080×1440 ----
im, d = base(1080, 1440, 0.5, 0.18)
fk = put(d, "深圳中考 · 备考策略", (540, 130), 34, GOLD, 1080, True, 960)
tw = d.textlength("深圳中考 · 备考策略", font=fk); d.line([(540 - tw/2 - 4, 178), (540 + tw/2 + 4, 178)], fill=GOLD, width=4)
put(d, "8 科作战表", (540, 360), 116, WHITE, 1080, True, 960)
put(d, "630 口径可对账", (540, 560), 92, GOLD, 1080, True, 960)
put(d, "440笔试 ＋ 20实验 ＋ 170史道体 ＝ 630", (540, 800), 44, LIGHT, 1080, False, 960)
pill(d, "语文·数学·英语·物化笔试 = 440", 1060, 36, 1080, pad=40)
put(d, "备考策略 · 收藏不迷路 · 数据见正文", (540, 1280), 28, SUB, 1080, False)
im.save(HERE + "04.小红书/S1-630构成-小红书-封面-互补版-1080x1440.png")
print("saved 小红书封面")
print("done")
