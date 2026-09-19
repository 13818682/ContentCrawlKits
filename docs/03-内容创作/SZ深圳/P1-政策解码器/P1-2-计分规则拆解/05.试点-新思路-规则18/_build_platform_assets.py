# -*- coding: utf-8 -*-
"""P1-2 试点 · 四平台发布配图（规则18 新思路）
01.公众号/封面 900x383 · 02.今日头条/封面 1200x900
03.抖音/首图 1080x1920（安全区 右≤950 / 内容≤y1590）
04.小红书/封面 A互补版 B现状近似版 1080x1440
口径：理化实验一律写「2026涨到20分」，不含"较前一年+分/8分"表述。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"


def base(w, h, glow=(0.5, 0.20, 0.34, 0.12)):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    g = np.exp(-(((x - w * glow[0]) / (w * glow[2])) ** 2 + ((y - h * glow[1]) / (h * glow[2])) ** 2))
    a = a + np.array((190, 210, 235), float)[None, None, :] * (g * glow[3])[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-w * 0.18, -h * 0.10, w * 0.24, h * 0.16], fill=TOP + (36,))
    od.ellipse([w * 0.80, h * 0.82, w * 1.12, h * 1.06], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, w, bold=True, maxw=None, name=""):
    fpath = FB if bold else FR
    f = ImageFont.truetype(fpath, size)
    mw = maxw if maxw else w - 120
    while f.size > 16:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fpath, f.size - 1)
    d.text(xy, text, font=f, fill=fill, anchor="mm")


def pill(d, text, cy, size, w, pad=46, text_fill=WHITE, line=GOLD, lw=3, maxw=None):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    mw = (maxw if maxw else w - 160)
    while tw > mw:
        size -= 1
        f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f)
        tw = bb[2] - bb[0]
    x0, x1 = (w - tw) / 2 - pad, (w + tw) / 2 + pad
    hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=line, width=lw)
    d.text((w / 2, cy), text, font=f, fill=text_fill, anchor="mm")


def underline(d, cx, text, f, y, color=GOLD, width=5):
    tw = d.textlength(text, font=f)
    d.line([(cx - tw / 2 - 5, y), (cx + tw / 2 + 5, y)], fill=color, width=width)


# ============ 01.公众号封面 900×383 ============
im, d = base(900, 383, (0.5, 0.18, 0.32, 0.10))
f = ImageFont.truetype(FB, 44)
put(d, "深圳中考", (450, 46), 44, GOLD, 900, True, 850)
underline(d, 450, "深圳中考", f, 92)
put(d, "同样的复习时间，先给哪科？", (450, 178), 50, WHITE, 900, True, 860)
put(d, "语数英物化＝440 · 主战场", (450, 292), 42, GOLD, 900, True, 860)
im.save(ROOT + "01.公众号/科目性价比-公众号-封面-900x383.png")
print("saved 公众号封面")

# ============ 02.今日头条封面 1200×900 ============
im, d = base(1200, 900, (0.5, 0.20, 0.34, 0.10))
pill(d, "深圳中考 · 备考策略", 118, 30, 1200, pad=30)
put(d, "复习时间，先给哪科？", (600, 300), 96, WHITE, 1200, True, 1080)
put(d, "语数英物化 ＝ 440 · 主战场", (600, 470), 84, GOLD, 1200, True, 1080)
put(d, "2026 理化实验涨到 20 分 · 操作分要动手练", (600, 640), 44, LIGHT, 1200, False, 1080)
put(d, "历史70＋道法50＋体育50＝170 · 稳住即可", (600, 720), 40, SUB, 1200, False, 1080)
put(d, "数据来源：深圳市教育局公开信息 · 逐条人工核对", (600, 852), 22, SUB, 1200, False)
im.save(ROOT + "02.今日头条/科目性价比-头条-封面-1200x900.png")
print("saved 头条封面")

# ============ 03.抖音首图 1080×1920（安全区 右≤950 内容≤y1590） ============
im, d = base(1080, 1920, (0.5, 0.16, 0.34, 0.12))
f = ImageFont.truetype(FB, 56)
put(d, "深圳中考", (520, 150), 56, GOLD, 1080, True, 800)
underline(d, 520, "深圳中考", f, 224, width=6)
put(d, "440", (520, 440), 220, GOLD, 1080, True, 800)
put(d, "语数英物化 · 主战场", (520, 680), 84, WHITE, 1080, True, 800)
put(d, "2026理化实验涨到20分", (520, 900), 46, LIGHT, 1080, False, 800)
put(d, "操作分 · 要真动手练", (520, 972), 40, SUB, 1080, False, 800)
put(d, "历史70+道法50+体育50=170 · 稳住", (520, 1140), 36, SUB, 1080, False, 800)
pill(d, "关注我 · 政策解码器继续讲", 1470, 40, 1080, pad=34, maxw=800)
im.save(ROOT + "03.抖音/科目性价比-抖音-首图-1080x1920.png")
print("saved 抖音首图")

# ============ 04.小红书封面 A/B 1080×1440（封面PK） ============
def xhs_cover(a_variant):
    im, d = base(1080, 1440, (0.5, 0.20, 0.34, 0.12))
    f = ImageFont.truetype(FB, 34)
    put(d, "深圳中考 · 备考策略", (540, 130), 34, GOLD, 1080, True, 960)
    underline(d, 540, "深圳中考 · 备考策略", f, 182, width=4)
    if a_variant:
        put(d, "语数英物化", (540, 360), 112, WHITE, 1080, True, 960)
        put(d, "440 分 · 主战场", (540, 540), 108, GOLD, 1080, True, 960)
        put(d, "副科稳住就好", (540, 700), 72, WHITE, 1080, True, 960)
        put(d, "历史70 + 道法50 + 体育50 ＝ 170", (540, 860), 42, LIGHT, 1080, False, 960)
    else:
        put(d, "同样的复习时间", (540, 350), 92, WHITE, 1080, True, 960)
        put(d, "花在哪科涨分最快？", (540, 520), 102, GOLD, 1080, True, 960)
        put(d, "语数英物化440 · 理化实验20 · 副科170", (540, 760), 40, LIGHT, 1080, False, 960)
    pill(d, "2026理化实验涨到20分 · 操作分要动手练", 1040, 36, 1080, pad=40, maxw=920)
    put(d, "备考策略 · 收藏不迷路 · 数据见正文", (540, 1280), 28, SUB, 1080, False)
    if a_variant:
        out = ROOT + "04.小红书/封面/科目性价比-封面A-互补版-1080x1440.png"
        tag = "A-互补版"
    else:
        out = ROOT + "04.小红书/封面/科目性价比-封面B-现状近似版-1080x1440.png"
        tag = "B-现状近似版"
    im.save(out)
    print("saved 小红书封面", tag)

xhs_cover(True)
xhs_cover(False)
print("done")
