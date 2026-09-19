# -*- coding: utf-8 -*-
"""S2 抖音口播 分镜头图 x6（1080×1920，文字放大·安全区：右≤950／下正文≤1590）
镜头按口播分段：01核心观点 02怎么考 03评分到每一步 04丢分坑 05三招怎么练 06CTA。
口径(短载体)：理化实验涨到20分，不写原12分。
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
ctext(d, "深圳中考 · 政策解码器 S2", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "理化实验，涨到 20 分", (W / 2, 640), 92, WHITE, maxw=800)
ctext(d, "纯操作分 · 刷题刷不出来", (W / 2, 880), 60, GOLD)
ctext(d, "动手练，就基本稳", (W / 2, 1060), 44, LIGHT, bold=False)
check("镜头01")
im.save(HERE + "S2-理化实验涨到20分-抖音-镜头01-核心观点-1080x1920.png")

# 镜头02 怎么考
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S2", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "物、化 各考 1 个实验", (W / 2, 600), 84, WHITE)
ctext(d, "现场动手 · 每科 10 分钟", (W / 2, 820), 60, GOLD)
ctext(d, "5 月进行 · 别等到考前", (W / 2, 1000), 44, LIGHT, bold=False)
ctext(d, "物化 140 ＝ 笔试 120 ＋ 实验 20", (W / 2, 1200), 46, LIGHT, bold=False)
check("镜头02")
im.save(HERE + "S2-理化实验涨到20分-抖音-镜头02-怎么考-1080x1920.png")

# 镜头03 评分到每一步
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S2", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "评分到每一步", (W / 2, 620), 92, WHITE)
ctext(d, "连接 · 读数 · 记录 · 复位", (W / 2, 850), 62, GOLD)
ctext(d, "漏一步，就少一分", (W / 2, 1060), 46, LIGHT, bold=False)
check("镜头03")
im.save(HERE + "S2-理化实验涨到20分-抖音-镜头03-评分到每一步-1080x1920.png")

# 镜头04 丢分坑
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S2", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "看同学做、抄报告", (W / 2, 600), 88, WHITE)
ctext(d, "进考场，就是手生", (W / 2, 830), 62, GOLD)
ctext(d, "这 20 分，能丢一半以上", (W / 2, 1030), 46, LIGHT, bold=False)
check("镜头04")
im.save(HERE + "S2-理化实验涨到20分-抖音-镜头04-丢分坑-1080x1920.png")

# 镜头05 三招怎么练
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S2", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "三招，练了就稳", (W / 2, 480), 72, WHITE)
lines = [
    ("1", "实验课自己动手，当主科上"),
    ("2", "学校集中练，一节别请假"),
    ("3", "录操作回看，扣分点一眼看出"),
]
y = 760
for n, t in lines:
    ctext(d, n, (180, y), 60, GOLD, min_size=44, maxw=80)
    ctext(d, t, (590, y), 48, WHITE, maxw=700, min_size=36)
    y += 190
check("镜头05")
im.save(HERE + "S2-理化实验涨到20分-抖音-镜头05-三招怎么练-1080x1920.png")

# 镜头06 CTA
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S2", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "动手的 20 分", (W / 2, 560), 84, WHITE)
ctext(d, "练了就基本稳", (W / 2, 780), 66, GOLD)
ctext(d, "关注我，下一条：道法改开卷怎么办", (W / 2, 1040), 46, LIGHT, bold=False)
pill(d, "政策解码器 · 一条条讲给你", 1400)
check("镜头06")
im.save(HERE + "S2-理化实验涨到20分-抖音-镜头06-CTA-1080x1920.png")
print("done")
