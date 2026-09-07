# -*- coding: utf-8 -*-
"""P1-3 S3 AC/D分差 抖音口播分镜 ×6（1080×1920）

版式：顶部「深圳中考」金色大字标识（家族统一）+ 小标按 AC 段命名。
差异化（防与 S2 青蓝卡片档 / 主线纯居中档自我重复）：换紫罗兰蓝档 + 数字大字 hero 版式 + 分层段标。
安全区：正文右缘≤950、下界≤1590；底部 y≥1600 留空给字幕/图标。
镜头：01 设问钩子 / 02 四大 0分(≥587) / 03 中坚 2-9分(530-554)
 / 04 边缘 15-23分(500-529) / 05 新校综高 20-30分(<500) 别追新校区 / 06 CTA+预告S1(C类跨区)。
口径：2026住宿线实测·结论性数字（四大0/中坚2-9/边缘15-23/新校20-30）。
模板：S2 _build_s2_dy_shots.py（家族）差异化为紫罗兰+数字大字。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
# 紫罗兰蓝档（区别于主线 navy、S2 青 teal）
TOP = (52, 48, 122); BOT = (20, 18, 60)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (206, 203, 240); SUB = (222, 220, 246)
CARD = (40, 36, 96); EDGE = (122, 116, 204)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.16) / (H * 0.30)) ** 2))
    a = a + np.array((205, 200, 245), float)[None, None, :] * (g * 0.09)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    # 背景装饰：右侧竖向细条（区别于 S2 斜纹 / 主线无装饰）
    for i in range(4):
        xx = 800 + i * 90
        od.line([(xx, 1700), (xx, 300)], fill=(255, 255, 255) + (10,), width=70)
    od.ellipse([-W * .22, -H * .06, W * .22, H * .15], fill=TOP + (36,))
    od.ellipse([W * .82, H * .86, W * 1.14, H * 1.03], fill=TOP + (24,))
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
    """顶部深圳中考大字 + 金线 + 本镜 AC 段标（家族统一）"""
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


# 镜头01 设问钩子
im, d = base(); header(d, "S3 · AC/D分差全景")
ctext(d, "D类要多考多少分？", (W / 2, 620), 92, WHITE, maxw=880, min_size=72, tag="01")
ctext(d, "没有统一答案 · 分五层看", (W / 2, 820), 58, GOLD, maxw=880, min_size=46, tag="01")
rcard(d, 80, 1020, W - 80, 1240)
ctext(d, "同一所公办高中", (W / 2, 1090), 46, WHITE, maxw=760, min_size=38, tag="01")
ctext(d, "有的层一分不差 · 有的层多考20多分", (W / 2, 1190), 40, LIGHT, bold=False, maxw=820, min_size=34, tag="01")
ctext(d, "差距不在头部 · 在边缘段", (W / 2, 1420), 46, WHITE, min_size=38, tag="01")
check("镜头01")
im.save(HERE + "P1-3-S3-ACD分差全景-抖音-镜头01-D类要多考多少分-1080x1920.png")

# 镜头02 层① 四大（≥587）0分
im, d = base(); header(d, "AC 587分以上 · 四大名校")
ctext(d, "0 分", (W / 2, 620), 150, GOLD, maxw=560, min_size=110, tag="02")
ctext(d, "四大 D类同分进", (W / 2, 830), 56, WHITE, maxw=880, min_size=44, tag="02")
rcard(d, 80, 960, W - 80, 1160)
ctext(d, "深中 592 = D 类 592", (W / 2, 1030), 50, WHITE, maxw=800, min_size=40, tag="02")
ctext(d, "深外 587 · 深实验 590 · 深高 587 同理", (W / 2, 1125), 36, LIGHT, bold=False, maxw=820, min_size=30, tag="02")
ctext(d, "冲四大 · 户籍不卡你", (W / 2, 1400), 48, WHITE, min_size=40, tag="02")
check("镜头02")
im.save(HERE + "P1-3-S3-ACD分差全景-抖音-镜头02-四大零分-1080x1920.png")

# 镜头03 层③ 中坚（530-554）2-9分
im, d = base(); header(d, "AC 530-554 · 区属中坚")
ctext(d, "2-9 分", (W / 2, 620), 148, WHITE, maxw=600, min_size=112, tag="03")
ctext(d, "分差开始稳定出现", (W / 2, 830), 56, GOLD, maxw=880, min_size=44, tag="03")
rcard(d, 80, 960, W - 80, 1160)
ctext(d, "七高 530→535 · 差5分", (W / 2, 1030), 50, WHITE, maxw=820, min_size=40, tag="03")
ctext(d, "福海 535→544 · 平冈 540→546", (W / 2, 1125), 38, LIGHT, bold=False, maxw=820, min_size=30, tag="03")
ctext(d, "这段开始 · D类要多留几分", (W / 2, 1400), 48, WHITE, min_size=40, tag="03")
check("镜头03")
im.save(HERE + "P1-3-S3-ACD分差全景-抖音-镜头03-中坚2到9分-1080x1920.png")

# 镜头04 层④ 边缘（500-529）15-23分
im, d = base(); header(d, "AC 500-529 · 公办边缘")
ctext(d, "15-23 分", (W / 2, 620), 150, GOLD, maxw=660, min_size=112, tag="04")
ctext(d, "D类要明显多考 · 最该警惕", (W / 2, 830), 54, WHITE, maxw=900, min_size=44, tag="04")
rcard(d, 80, 960, W - 80, 1160)
ctext(d, "深实崇文 506 → D 529 · 差23分", (W / 2, 1030), 46, WHITE, maxw=840, min_size=38, tag="04")
ctext(d, "22所里16所 D高10分以上", (W / 2, 1125), 38, LIGHT, bold=False, maxw=840, min_size=30, tag="04")
ctext(d, "“能上但不确定哪所”· 策略比刷题重要", (W / 2, 1420), 44, WHITE, min_size=36, tag="04")
check("镜头04")
im.save(HERE + "P1-3-S3-ACD分差全景-抖音-镜头04-边缘差到23-1080x1920.png")

# 镜头05 层⑤ 新校/综合高中班（<500）20-30分
im, d = base(); header(d, "AC 500以下 · 新校·综合高中班")
ctext(d, "20-30 分", (W / 2, 620), 150, WHITE, maxw=700, min_size=112, tag="05")
ctext(d, "分差最狠的一档", (W / 2, 830), 54, GOLD, maxw=880, min_size=44, tag="05")
rcard(d, 80, 960, W - 80, 1160)
ctext(d, "曙光(综高) 497 → D 526 · 差29分", (W / 2, 1030), 46, WHITE, maxw=860, min_size=38, tag="05")
ctext(d, "别信“新校区好考” · 2026它们分差最大", (W / 2, 1125), 38, LIGHT, bold=False, maxw=880, min_size=30, tag="05")
ctext(d, "要友好 · 看成熟区属校真实分差", (W / 2, 1400), 46, WHITE, min_size=38, tag="05")
check("镜头05")
im.save(HERE + "P1-3-S3-ACD分差全景-抖音-镜头05-新校20到30-1080x1920.png")

# 镜头06 CTA
im, d = base(); header(d, "S3 · 一句话记牢")
ctext(d, "四大0分", (W / 2, 560), 88, WHITE, maxw=880, min_size=70, tag="06")
ctext(d, "越往“勉强上公办”那段 · 差越多", (W / 2, 740), 54, GOLD, maxw=920, min_size=44, tag="06")
rcard(d, 80, 920, W - 80, 1140)
ctext(d, "孩子分数在哪层？", (W / 2, 1000), 48, WHITE, maxw=820, min_size=40, tag="06")
ctext(d, "去查目标校真实 D 线 · 别听人云亦云", (W / 2, 1100), 42, LIGHT, bold=False, maxw=860, min_size=34, tag="06")
ctext(d, "关注我 · 下条讲深户跨区 C 类", (W / 2, 1420), 56, WHITE, min_size=46, tag="06")
check("镜头06")
im.save(HERE + "P1-3-S3-ACD分差全景-抖音-镜头06-CTA-1080x1920.png")
print("done")
