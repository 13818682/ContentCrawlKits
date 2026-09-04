# -*- coding: utf-8 -*-
"""S1 抖音分镜头图 1080×1920（按口播文案分段 · 文字统一放大）
安全区：内容右缘≤950、下缘≤1590（douyin-safe-area）。
每镜头纵向三行结构：数字(金,巨大) / 标题(白,大) / 说明(浅,统一字号)。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
CX = 520          # 中心略左（给右侧图标区留空：内容右缘 ≤950）
MW = 820          # 最大行宽（保证右缘 ≤ 950）
BOTTOM = 1590     # 内容下缘上限


def base(seed):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    gx = [0.5, 0.22, 0.78, 0.5][seed % 4]
    gy = [0.14, 0.30, 0.16, 0.5][seed % 4]
    g = np.exp(-(((x - W * gx) / (W * 0.34)) ** 2 + ((y - H * gy) / (H * 0.36)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-180, -140, 260, 240], fill=TOP + (36,))
    od.ellipse([W - 220, H - 300, W + 120, H - 60], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, cy, size, fill, bold=True):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    while f.size > 16:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= MW + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    d.text((CX, cy), text, font=f, fill=fill, anchor="mm")
    return f.size


def shot(name, lines, seed):
    """lines: [(text, size, color, bold)]，按行绘制（垂直居中区，纵向下移由调用者给定绝对cy）"""
    im, d = base(seed)
    for text, cy, size, color, bold in lines:
        put(d, text, cy, size, color, bold)
    im.save(HERE + name)
    print("saved", name)


# 镜01 核心观点（与首图同口径）
shot("S1-630构成-抖音-镜头01-核心观点-1080x1920.png", [
    ("深圳中考", 170, 92, GOLD, True),
    ("8科怎么考、怎么给分？", 700, 96, WHITE, True),
    ("630分拆解 · 一张表看懂", 1000, 62, GOLD, True),
    ("考什么｜多少分｜精力怎么分", 1220, 46, LIGHT, False),
], 0)

# 镜02 Hook：提问
shot("S1-630构成-抖音-镜头02-Hook-1080x1920.png", [
    ("630分到底怎么来的？", 620, 104, WHITE, True),
    ("很多家长说不清", 900, 64, GOLD, True),
    ("其实一句话就讲得完", 1120, 44, LIGHT, False),
], 1)

# 镜03 主科 440
shot("S1-630构成-抖音-镜头03-主科440-1080x1920.png", [
    ("440", 560, 300, GOLD, True),
    ("笔试主科 · 决定位置", 980, 72, WHITE, True),
    ("语文120 + 数学100 + 英语100(含听口) + 物化笔试120", 1180, 40, LIGHT, False),
], 2)

# 镜04 实验 20
shot("S1-630构成-抖音-镜头04-实验20-1080x1920.png", [
    ("20", 560, 300, GOLD, True),
    ("理化实验 · 2026为20分", 980, 72, WHITE, True),
    ("操作分刷题刷不出来 · 要真动手练", 1180, 40, LIGHT, False),
], 3)

# 镜05 稳定 170
shot("S1-630构成-抖音-镜头05-稳定170-1080x1920.png", [
    ("170", 560, 300, GOLD, True),
    ("历史70 + 道法50 + 体育50", 980, 72, WHITE, True),
    ("稳住即可 · 别拖后腿", 1180, 40, LIGHT, False),
], 0)

# 镜06 CTA：加总 + 关注
shot("S1-630构成-抖音-镜头06-CTA-1080x1920.png", [
    ("加起来，正好 630", 620, 92, WHITE, True),
    ("8科一张表 · 收藏不迷路", 900, 60, GOLD, True),
    ("关注我 · 政策解码器继续讲", 1500, 44, LIGHT, True),
], 1)
print("done")
