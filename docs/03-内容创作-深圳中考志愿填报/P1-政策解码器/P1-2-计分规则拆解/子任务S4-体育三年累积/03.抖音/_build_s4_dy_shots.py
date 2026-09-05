# -*- coding: utf-8 -*-
"""S4 抖音口播 分镜头图 x6（1080×1920，文字放大·安全区：右≤950／下正文≤1590）
镜头按口播分段：01核心观点 02过程14分 03丢分真相 04现场36分 05三件事 06CTA。
口径：体育总分50=过程14+现场36；14=体测9+参与3+通识2；现场三大类1+1+1·0.36权重·4月。
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
ctext(d, "深圳中考 · 政策解码器 S4", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "体育 50 分", (W / 2, 620), 96, WHITE, maxw=800)
ctext(d, "一半靠攒，一半靠考", (W / 2, 860), 62, GOLD)
ctext(d, "不是初三跑一次就完事", (W / 2, 1060), 46, LIGHT, bold=False)
check("镜头01")
im.save(HERE + "S4-体育三年累积-抖音-镜头01-核心观点-1080x1920.png")

# 镜头02 过程14分
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S4", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "攒的那 14 分", (W / 2, 560), 88, WHITE)
ctext(d, "体测 9 + 参与 3 + 通识 2", (W / 2, 820), 56, GOLD)
ctext(d, "每年及格·到场，就到手", (W / 2, 1020), 48, LIGHT, bold=False)
ctext(d, "从初一攒到初三", (W / 2, 1180), 44, LIGHT, bold=False)
check("镜头02")
im.save(HERE + "S4-体育三年累积-抖音-镜头02-过程14分-1080x1920.png")

# 镜头03 丢分真相
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S4", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "这 14 分，丢在哪？", (W / 2, 560), 84, WHITE)
ctext(d, "体测请假", (W / 2, 820), 62, GOLD)
ctext(d, "体育课缺勤", (W / 2, 1000), 62, GOLD)
ctext(d, "不是孩子不行，是人没到齐", (W / 2, 1200), 42, LIGHT, bold=False)
check("镜头03")
im.save(HERE + "S4-体育三年累积-抖音-镜头03-丢分真相-1080x1920.png")

# 镜头04 现场36分
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S4", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "考的 36 分，怎么考", (W / 2, 520), 80, WHITE)
ctext(d, "三大类 · 各选 1 项", (W / 2, 780), 62, GOLD)
ctext(d, "耐力 · 速度力量 · 球类", (W / 2, 960), 48, LIGHT, bold=False)
ctext(d, "平均分 × 0.36 · 4 月考", (W / 2, 1130), 44, LIGHT, bold=False)
ctext(d, "引体/仰卧起坐已移出，别练错", (W / 2, 1300), 38, LIGHT, bold=False)
check("镜头04")
im.save(HERE + "S4-体育三年累积-抖音-镜头04-现场36分-1080x1920.png")

# 镜头05 三件事
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S4", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "现在做三件事", (W / 2, 480), 76, WHITE)
lines = [
    ("1", "三类定项：球类选能练得起的"),
    ("2", "查旧账：前两年过程分有漏吗"),
    ("3", "耐力每周至少练 3 次"),
]
y = 760
for n, t in lines:
    ctext(d, n, (180, y), 60, GOLD, min_size=44, maxw=80)
    ctext(d, t, (590, y), 46, WHITE, maxw=700, min_size=34)
    y += 200
check("镜头05")
im.save(HERE + "S4-体育三年累积-抖音-镜头05-三件事-1080x1920.png")

# 镜头06 CTA
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S4", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "体育别让它拖后腿", (W / 2, 560), 84, WHITE)
ctext(d, "攒的守住 · 考的早练", (W / 2, 780), 62, GOLD)
ctext(d, "关注我，下一条：单科等级不能掉C", (W / 2, 1040), 44, LIGHT, bold=False)
pill(d, "政策解码器 · 一条条讲给你", 1400)
check("镜头06")
im.save(HERE + "S4-体育三年累积-抖音-镜头06-CTA-1080x1920.png")
print("done")
