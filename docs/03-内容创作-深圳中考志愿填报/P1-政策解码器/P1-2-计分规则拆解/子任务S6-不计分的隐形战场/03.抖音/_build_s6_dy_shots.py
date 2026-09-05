# -*- coding: utf-8 -*-
"""S6 抖音口播 分镜头图 x6（1080×1920，文字放大·安全区：右≤950／下正文≤1590）
镜头按口播分段：01核心观点 02同分顺序 03真实案例 04顺序误区 05三件事 06CTA。
口径：同分=先生地合卷·后语数英（FAQ-7）；生地初二下已考完。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.18) / (H * 0.32)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .05, W * .24, H * .12], fill=TOP + (36,))
    od.ellipse([W * .80, H * .86, W * 1.1, H * 1.03], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def ctext(d, text, xy, size, fill, bold=True, maxw=820, min_size=40):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BADS.append((text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def pill(d, text, cy=1510, size=42, pad=36):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > W - 190:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (W - tw) / 2 - pad, (W + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((W / 2, cy), text, font=f, fill=WHITE, anchor="mm")
    return x1


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 30 or bb[2] > 950:
            bad.append((tag + " X", tuple(int(v) for v in bb)))
        if bb[1] < 60 or bb[3] > 1590:
            bad.append((tag + " Y", tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, bad if bad else "")
    BADS.clear()


# 镜头01 核心观点
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S6", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "生地不计分", (W / 2, 560), 96, WHITE, maxw=800)
ctext(d, "同分，却先比它", (W / 2, 800), 66, GOLD)
ctext(d, "630 之外 · 可能定录取的那 100 分", (W / 2, 1000), 44, LIGHT, bold=False)
check("镜头01")
im.save(HERE + "S6-不计分的隐形战场-抖音-镜头01-核心观点-1080x1920.png")

# 镜头02 同分顺序
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S6", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "同分怎么比？", (W / 2, 500), 84, WHITE)
ctext(d, "第 1 步：比生地合卷", (W / 2, 760), 60, GOLD)
ctext(d, "第 2 步：生地同 → 语数英", (W / 2, 950), 56, WHITE)
ctext(d, "顺序不能反 · 高者先进", (W / 2, 1140), 44, LIGHT, bold=False)
check("镜头02")
im.save(HERE + "S6-不计分的隐形战场-抖音-镜头02-同分顺序-1080x1920.png")

# 镜头03 真实案例
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S6", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "真实案例：总分同 552", (W / 2, 520), 78, WHITE)
ctext(d, "生地 96 分 → 录", (W / 2, 800), 66, GOLD)
ctext(d, "生地 82 分 → 落", (W / 2, 980), 66, WHITE)
ctext(d, "差不在语数英，在两年前那场生地考", (W / 2, 1200), 40, LIGHT, bold=False)
check("镜头03")
im.save(HERE + "S6-不计分的隐形战场-抖音-镜头03-真实案例-1080x1920.png")

# 镜头04 顺序误区
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S6", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "别误会：语数英对冲不了生地", (W / 2, 470), 60, WHITE, maxw=800, min_size=40)
ctext(d, "生地才是第一道闸", (W / 2, 690), 66, GOLD)
ctext(d, "生地不同 · 不比语数英", (W / 2, 880), 48, LIGHT, bold=False)
check("镜头04")
im.save(HERE + "S6-不计分的隐形战场-抖音-镜头04-顺序误区-1080x1920.png")

# 镜头05 三件事
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S6", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "生地已定格 · 现在做 3 件事", (W / 2, 460), 66, WHITE)
lines = [
    ("1", "确认生地成绩没记错"),
    ("2", "生地弱：拉高总分才稳"),
    ("3", "目标线设得比往年高一点"),
]
y = 720
for n, t in lines:
    ctext(d, n, (180, y), 60, GOLD, min_size=44, maxw=80)
    ctext(d, t, (590, y), 48, WHITE, maxw=700, min_size=36)
    y += 210
check("镜头05")
im.save(HERE + "S6-不计分的隐形战场-抖音-镜头05-三件事-1080x1920.png")

# 镜头06 CTA
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S6", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "读懂规则 · 把总分做扎实", (W / 2, 560), 72, WHITE)
ctext(d, "P1-2 六篇收官", (W / 2, 800), 60, GOLD)
ctext(d, "关注我 · 下个系列见", (W / 2, 1040), 46, LIGHT, bold=False)
pill(d, "政策解码器 · 一条条讲给你", 1400)
check("镜头06")
im.save(HERE + "S6-不计分的隐形战场-抖音-镜头06-CTA-1080x1920.png")
print("done")
