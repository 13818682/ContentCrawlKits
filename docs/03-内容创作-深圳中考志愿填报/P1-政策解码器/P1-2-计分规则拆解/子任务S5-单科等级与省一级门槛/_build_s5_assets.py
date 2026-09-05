# -*- coding: utf-8 -*-
"""S5(单科等级与省一级门槛) 四平台封面/首图
公众号 900×383 + 头条 1200×900 + 抖音首图 1080×1920(安全区) + 小红书 1080×1440。
封面第一眼=深圳中考+问题；数字少用。口径：A+永远前5%；省一级录取须全科C+·体育C。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
BADS = []


def base(w, h, gx=0.5, gy=0.16):
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
    od.ellipse([w * .80, h * .84, w * 1.1, h * 1.05], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, w, bold=True, maxw=None, min_size=20, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else w - 120
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    b = d.textbbox(xy, text, font=f, anchor="mm")
    BADS.append((tag, w, b))
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


def check(name, right_limit=None, bottom_limit=None):
    bad = []
    for tag, w, bb in BADS:
        if bb[0] < 20 or bb[1] < 8 or bb[2] > w - 20:
            bad.append((tag, tuple(int(v) for v in bb)))
        if right_limit and bb[2] > right_limit:
            bad.append((tag + " R>%d" % right_limit, tuple(int(v) for v in bb)))
        if bottom_limit and bb[3] > bottom_limit:
            bad.append((tag + " B>%d" % bottom_limit, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| texts:", len(BADS), bad if bad else "")
    BADS.clear()


# ---------- 公众号 900×383 ----------
im, d = base(900, 383, 0.5, 0.15)
put(d, "深圳中考", (450, 42), 42, GOLD, 900, True, 860, tag="gzh")
f = put(d, "A+ 永远是前 5%", (450, 150), 56, WHITE, 900, True, 860, tag="gzh")
bb = d.textbbox((450, 150), "A+ 永远是前 5%", font=f, anchor="mm")
d.line([(450 - (bb[2]-bb[0])/2 - 6, 202), (450 + (bb[2]-bb[0])/2 + 6, 202)], fill=GOLD, width=5)
put(d, "别让任何一科掉 C", (450, 256), 38, LIGHT, 900, False, 860, tag="gzh")
put(d, "省一级公办普高的隐形门槛", (450, 330), 34, GOLD, 900, True, 860, tag="gzh")
im.save(HERE + "01.公众号/S5-单科等级与省一级门槛-公众号-封面-900x383.png")
check("公众号封面")

# ---------- 头条 1200×900 ----------
im, d = base(1200, 900)
pill(d, "深圳中考 · 备考策略", 120, 30, 1200, pad=30)
put(d, "A+ 永远是前 5%", (600, 330), 112, WHITE, 1200, True, 1080, tag="tt")
put(d, "别让任何一科掉 C", (600, 530), 72, GOLD, 1200, True, 1080, tag="tt")
put(d, "省一级公办普高录取门槛：全科 C+ · 体育 C｜总分够线不算数", (600, 680), 40, LIGHT, 1200, False, 1080, tag="tt")
put(d, "数据来源：深圳市教育局公开信息 · 人工核对", (600, 852), 22, SUB, 1200, False, tag="tt")
im.save(HERE + "02.今日头条/S5-单科等级与省一级门槛-头条-封面-1200x900.png")
check("头条封面")

# ---------- 抖音首图 1080×1920（安全区：右≤950，正文下≤1590）----------
im, d = base(1080, 1920)
f = put(d, "深圳中考", (520, 150), 92, GOLD, 1080, True, 780, tag="dy")
bb = d.textbbox((520, 150), "深圳中考", font=f, anchor="mm")
d.line([(520 - (bb[2]-bb[0])/2 - 8, 246), (520 + (bb[2]-bb[0])/2 + 8, 246)], fill=GOLD, width=9)
put(d, "A+ 永远是前 5%", (520, 560), 96, WHITE, 1080, True, 800, tag="dy")
put(d, "别让一科掉 C", (520, 800), 66, GOLD, 1080, True, 800, tag="dy")
put(d, "省一级录取门槛 · 总分够线不算数", (520, 980), 44, LIGHT, 1080, False, 800, tag="dy")
pill(d, "关注我 · 政策解码器继续讲", 1500, 40, 1080, pad=34)
im.save(HERE + "03.抖音/S5-单科等级与省一级门槛-抖音-首图-1080x1920.png")
check("抖音首图", right_limit=950, bottom_limit=1600)

# ---------- 小红书封面（互补版） 1080×1440 ----------
im, d = base(1080, 1440)
f = put(d, "深圳中考", (540, 150), 92, GOLD, 1080, True, 920, tag="xhs")
bb = d.textbbox((540, 150), "深圳中考", font=f, anchor="mm")
d.line([(540 - (bb[2]-bb[0])/2 - 8, 246), (540 + (bb[2]-bb[0])/2 + 8, 246)], fill=GOLD, width=9)
put(d, "别让一科掉 C", (540, 500), 118, WHITE, 1080, True, 920, tag="xhs")
put(d, "A+ 永远前 5%", (540, 700), 76, GOLD, 1080, True, 920, tag="xhs")
put(d, "省一级公办普高的隐形门槛 · 总分够线不算数", (540, 890), 40, LIGHT, 1080, False, 920, tag="xhs")
put(d, "备考策略 · 收藏不迷路 · 数据见正文", (540, 1280), 28, SUB, 1080, False, tag="xhs")
im.save(HERE + "04.小红书/S5-单科等级与省一级门槛-小红书-封面-互补版-1080x1440.png")
check("小红书封面")
print("done")
