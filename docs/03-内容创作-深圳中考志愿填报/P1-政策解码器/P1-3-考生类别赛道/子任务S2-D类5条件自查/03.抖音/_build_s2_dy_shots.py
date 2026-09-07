# -*- coding: utf-8 -*-
"""P1-3 S2 抖音口播 分镜头图 ×6（1080×1920）

版式：顶部「深圳中考」金色大字标识（家族统一）+ 小标「S2 · D类5条件自查」。
差异化（防与主线分镜雷同感）：换蓝档(copper 偏青) + 背景斜纹装饰 + 卡片式版面（主线=纯居中大字）。
安全区：右缘≤950、正文下界≤1590；底部 y≥1600 留空给字幕/图标。
镜头：01 非深户≠没书读(破误解) / 02 满足5条件就能报(列表) / 03 社保最易翻车(强调卡)
 / 04 自查①社保记录 / 05 自查②居住证+③租赁凭证 / 06 CTA(关注+下条预告 S3)。
口径：D类5条件官方版(居住证/社保养老+医疗·一个险种满3年·补缴不计/3年学籍)。
模板：主线 _build_mainline_dy_shots.py（家族）差异化为卡片+装饰。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
# 差异化蓝档（copper/cobalt，偏青，区别于主线 navy）
TOP = (18, 74, 128); BOT = (8, 32, 66)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 196, 220); SUB = (201, 220, 232)
CARD = (24, 60, 100); EDGE = (64, 110, 158)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.16) / (H * 0.32)) ** 2))
    a = a + np.array((185, 215, 240), float)[None, None, :] * (g * 0.10)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    # 背景装饰（斜纹，区别于主线无装饰）
    for i in range(7):
        x0 = -200 + i * 260
        od.line([(x0, 1300), (x0 + 900, -60)], fill=TOP + (30,), width=90)
    od.ellipse([-W * .20, -H * .06, W * .22, H * .14], fill=TOP + (34,))
    od.ellipse([W * .84, H * .86, W * 1.12, H * 1.02], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def ctext(d, text, xy, size, fill, bold=True, maxw=840, min_size=40, tag=""):
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
    BADS.append((tag or text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE, radius=24):
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=wfill, outline=wout, width=3)


def header(d, tag):
    """顶部深圳中考大字 + 金线 + 本镜小标（家族统一）"""
    f = ctext(d, "深圳中考", (W / 2, 130), 92, GOLD, maxw=820, min_size=72, tag="H")
    bb = d.textbbox((W / 2, 130), "深圳中考", font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 6
    d.line([W / 2 - half, 214, W / 2 + half, 214], fill=GOLD, width=6)
    ctext(d, tag, (W / 2, 300), 40, LIGHT, bold=False, min_size=32, tag="S")


def check(name):
    bad = []
    for tagn, bb in BADS:
        if bb[0] < 30 or bb[2] > 950:
            bad.append((tagn + " 右", tuple(int(v) for v in bb)))
        if bb[1] < 60 or bb[3] > 1590:
            bad.append((tagn + " 下", tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, bad if bad else "")
    BADS.clear()


# 镜头01 破误解
im, d = base(); header(d, "S2 · D类5条件自查")
ctext(d, "非深户 ≠ 没书读", (W / 2, 620), 92, WHITE, maxw=860, min_size=70, tag="01")
ctext(d, "满足 5 个条件，就能读深圳公办", (W / 2, 820), 56, GOLD, maxw=880, min_size=44, tag="01")
ctext(d, "很多家长以为没资格 · 其实是条件没备齐", (W / 2, 1180), 42, LIGHT, bold=False, min_size=34, tag="01")
ctext(d, "这篇教你怎么自查", (W / 2, 1400), 44, WHITE, min_size=36, tag="01")
check("镜头01")
im.save(HERE + "P1-3-S2-D类5条件自查-抖音-镜头01-非深户不等于没书读-1080x1920.png")

# 镜头02 5条件速览（卡片列表）
im, d = base(); header(d, "S2 · 5 个报名条件")
ctext(d, "想读公办 · 这 5 个缺一不可", (W / 2, 420), 54, WHITE, maxw=880, min_size=42, tag="02")
rows = [
    ("1", "合法稳定职业", "父母一方在深有工作"),
    ("2", "合法稳定住所", "租房要租赁凭证"),
    ("3", "持有效居住证", "别过期"),
    ("4", "社保 养老+医疗", "一个险种满 3 年"),
    ("5", "3 年完整初中学籍", "在深读完初中"),
]
y = 520
for n, t, s in rows:
    y1 = y + 178
    rcard(d, 60, y, W - 60, y1)
    ctext(d, n, (150, (y + y1) / 2), 74, GOLD, maxw=120, min_size=54, tag="02")
    ctext(d, t, (430, (y + y1) / 2 - 8), 46, WHITE, maxw=560, min_size=36, tag="02")
    ctext(d, s, (430, (y + y1) / 2 + 52), 32, LIGHT, bold=False, maxw=560, min_size=26, tag="02")
    y = y1 + 22
check("镜头02")
im.save(HERE + "P1-3-S2-D类5条件自查-抖音-镜头02-5个条件-1080x1920.png")

# 镜头03 社保最易翻车（强调卡）
im, d = base(); header(d, "S2 · 最易翻车的一项")
ctext(d, "社保 · 最容易翻车", (W / 2, 480), 70, WHITE, maxw=880, min_size=56, tag="03")
rcard(d, 60, 660, W - 60, 900)
ctext(d, "养老 + 医疗都缴", (W / 2, 730), 52, WHITE, maxw=760, min_size=42, tag="03")
ctext(d, "只需一个险种累计满 3 年", (W / 2, 852), 44, GOLD, maxw=840, min_size=36, tag="03")
rcard(d, 60, 980, W - 60, 1160)
ctext(d, "补缴年限不计 · 断缴要留意", (W / 2, 1070), 44, WHITE, maxw=840, min_size=36, tag="03")
ctext(d, "现在就去拉社保记录数一数", (W / 2, 1400), 42, LIGHT, bold=False, min_size=34, tag="03")
check("镜头03")
im.save(HERE + "P1-3-S2-D类5条件自查-抖音-镜头03-社保最易翻车-1080x1920.png")

# 镜头04 自查①社保
im, d = base(); header(d, "S2 · 现在自查 ①")
ctext(d, "查社保记录", (W / 2, 560), 88, WHITE, maxw=860, min_size=68, tag="04")
ctext(d, "满 3 年了吗？断缴没？", (W / 2, 760), 58, GOLD, maxw=880, min_size=46, tag="04")
rcard(d, 100, 1000, W - 100, 1240)
ctext(d, "补缴不计 · 一个险种满 3 年才算", (W / 2, 1120), 40, WHITE, maxw=760, min_size=32, tag="04")
ctext(d, "别等 3 月报名才发现不够", (W / 2, 1430), 42, LIGHT, bold=False, min_size=34, tag="04")
check("镜头04")
im.save(HERE + "P1-3-S2-D类5条件自查-抖音-镜头04-自查社保-1080x1920.png")

# 镜头05 自查②居住证③租赁凭证
im, d = base(); header(d, "S2 · 现在自查 ②③")
ctext(d, "还有两样要提前办", (W / 2, 430), 54, WHITE, maxw=880, min_size=42, tag="05")
rcard(d, 60, 560, W - 60, 820)
ctext(d, "② 居住证", (W / 2, 630), 60, GOLD, maxw=760, min_size=48, tag="05")
ctext(d, "别过期 · 过期赶紧续签", (W / 2, 748), 42, WHITE, maxw=800, min_size=34, tag="05")
rcard(d, 60, 860, W - 60, 1120)
ctext(d, "③ 租赁凭证", (W / 2, 930), 60, GOLD, maxw=760, min_size=48, tag="05")
ctext(d, "租房要有凭证 · 不是普通合同", (W / 2, 1048), 42, WHITE, maxw=820, min_size=34, tag="05")
ctext(d, "这三样都要提前办 · 越早越从容", (W / 2, 1380), 44, LIGHT, bold=False, min_size=36, tag="05")
check("镜头05")
im.save(HERE + "P1-3-S2-D类5条件自查-抖音-镜头05-自查居住证租赁凭证-1080x1920.png")

# 镜头06 CTA
im, d = base(); header(d, "S2 · 下条预告")
ctext(d, "非深户 ≠ 没书读", (W / 2, 560), 80, WHITE, maxw=880, min_size=62, tag="06")
ctext(d, "5 个条件 · 现在查 3 样", (W / 2, 760), 54, GOLD, maxw=880, min_size=42, tag="06")
ctext(d, "下条：D 类和深户，录取到底差多少分", (W / 2, 1100), 46, LIGHT, bold=False, maxw=880, min_size=38, tag="06")
ctext(d, "关注我 · 深圳中考系列", (W / 2, 1400), 56, WHITE, min_size=44, tag="06")
check("镜头06")
im.save(HERE + "P1-3-S2-D类5条件自查-抖音-镜头06-CTA-1080x1920.png")
print("done")
