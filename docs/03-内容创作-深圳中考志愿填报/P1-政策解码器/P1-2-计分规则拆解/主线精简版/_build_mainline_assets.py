# -*- coding: utf-8 -*-
"""主线精简 封面生成（公众号 900×383 + 今日头条 1200×900）

平台分工（2026-09-04 定）：大长篇只在公众号/今日头条出完整版，
抖音/小红书不产"大总览"，其发布单元 = 各子任务（S1–S6）逐条产文案+配图。
故本脚本只保留公众号 + 头条两个平台封面。
口径：630=440笔试(含听口)+20实验+170史道体。
"""
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
    while f.size > 14:
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


# 公众号 900×383
im, d = base(900, 383, 0.5, 0.16)
fk = put(d, "深圳中考", (450, 44), 44, GOLD, 900, True, 860)
tw = d.textlength("深圳中考", font=fk); d.line([(450 - tw/2 - 5, 88), (450 + tw/2 + 5, 88)], fill=GOLD, width=5)
put(d, "630分，一篇讲透", (450, 168), 52, WHITE, 900, True, 860)
put(d, "构成 · 三大变化 · 单科等级 · 隐形战场", (450, 250), 34, LIGHT, 900, False, 860)
put(d, "440笔试 ＋ 20实验 ＋ 170史道体 ＝ 630", (450, 318), 36, GOLD, 900, True, 860)
im.save(HERE + "01.公众号/主线精简版-公众号-封面-900x383.png")
print("saved 公众号封面")

# 头条 1200×900
im, d = base(1200, 900)
pill(d, "深圳中考 · 备考策略", 120, 30, 1200, pad=30)
put(d, "630 分，一篇讲透", (600, 330), 100, WHITE, 1200, True, 1080)
put(d, "440笔试 ＋ 20实验 ＋ 170史道体 ＝ 630", (600, 510), 74, GOLD, 1200, True, 1080)
put(d, "三大变化 · 单科等级(A+前5%) · 同分PK(生地) · 隐形战场", (600, 660), 40, LIGHT, 1200, False, 1080)
put(d, "数据来源：深圳市教育局公开信息 · 人工核对", (600, 852), 22, SUB, 1200, False)
im.save(HERE + "02.今日头条/主线精简版-头条-封面-1200x900.png")
print("saved 头条封面")
print("done")
