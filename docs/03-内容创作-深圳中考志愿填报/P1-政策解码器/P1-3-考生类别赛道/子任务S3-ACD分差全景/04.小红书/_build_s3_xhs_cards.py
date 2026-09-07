# -*- coding: utf-8 -*-
"""P1-3 S3 AC/D分差 小红书正文图卡 ×4（1080×1440，封面已有精炼版）
正文图1-分差五层总表(收藏) / 图2-四大0分 / 图3-边缘之痛(15-23) / 图4-新校反转(20-31)。
口径：2026住宿线实测（95所公办普高）；短载体只给结论数字。
模板：S2 _build_s2_xhs_cards.py（同视觉 navy）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440
HM = 80
BOXES = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.32)) ** 2 + ((y - H * 0.16) / (H * 0.30)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .08, W * .24, H * .16], fill=TOP + (34,))
    od.ellipse([W * .80, H * .84, W * 1.1, H * 1.05], fill=TOP + (22,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def center(d, text, xy, size, fill, bold=True, maxw=None, min_size=28):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else W - 2 * HM
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "center too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BOXES.append(("C:" + text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def left(d, text, xy, size, fill, right=None, bold=False, min_size=30):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    r = right if right else W - HM
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= (r - xy[0]) + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= (r - xy[0]) + 1, "left too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="lm")
    BOXES.append(("L:" + text[:14], d.textbbox(xy, text, font=f, anchor="lm")))
    return f


def rtext(d, text, xy, size, fill, bold=True, min_size=24):
    """右对齐文字（右侧限界 W-HM-20），用于卡内右侧差分"""
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    r = W - HM - 20
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if (xy[0] - (bb[2] - bb[0])) >= 20:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert xy[0] - (bb[2] - bb[0]) >= 20, "rtext too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="rm")
    BOXES.append(("R:" + text[:12], d.textbbox(xy, text, font=f, anchor="rm")))
    return f


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE):
    d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=wfill, outline=wout, width=2)


def footer(d):
    center(d, "数据来源：深圳市教育局2026第一批录取标准·住宿线实测（人工核对）", (W / 2, 1390), 22, SUB, bold=False, min_size=17)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 8:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ========== 正文图1：分差五层总表（收藏） ==========
im, d = base()
center(d, "D类要多考多少分 · 分五层", (W / 2, 90), 34, GOLD, min_size=27)
center(d, "AC / D 录取分差总表", (W / 2, 250), 56, WHITE, min_size=44)
center(d, "2026住宿线实测 · 95所公办普高", (W / 2, 352), 32, LIGHT, bold=False, min_size=25)
rows = [
    ("四大头部", "AC 587+", "分差 0 · 深中592=D592"),
    ("八大·二十大", "AC 555-584", "分差 0-5 · 红岭584=D584"),
    ("区属中坚", "AC 530-554", "分差 2-9 · 七高530→535"),
    ("公办边缘", "AC 500-529", "分差 15-23 · 深实崇文506→529"),
    ("集团新校/综合高中班", "AC <500", "分差 20-31 · 曙光497→526"),
]
y = 420
for i, (t, a, s) in enumerate(rows):
    y1 = y + 148
    rcard(d, HM, y, W - HM, y1)
    center(d, str(i + 1), (HM + 90, (y + y1) / 2), 60, GOLD, maxw=110, min_size=44)
    x0 = HM + 200
    left(d, t + " · " + a, (x0, y + 52), 38, WHITE, bold=True, min_size=30)
    left(d, s, (x0, y + 112), 30, LIGHT, min_size=24)
    y = y1 + 16
center(d, "规律：四大0分 · 越往边缘越多考", (W / 2, 1320), 40, GOLD, min_size=32)
footer(d)
check("正文图1")
im.save(HERE + "P1-3-S3-ACD分差全景-小红书-正文图1-分差五层总表-1080x1440.png")

# ========== 正文图2：四大0分 ==========
im, d = base()
center(d, "第1层 · 四大名校", (W / 2, 90), 34, GOLD, min_size=27)
center(d, "0 分", (W / 2, 330), 150, WHITE, min_size=120)
center(d, "AC 和 D 同分进", (W / 2, 500), 50, GOLD, min_size=40)
sc = [
    ("深圳中学", "592", "592"),
    ("深实验(高中部)", "590", "590"),
    ("深圳外国语", "587", "587"),
    ("深高级(中心校区)", "587", "587"),
]
y = 560
for name, a, dd in sc:
    y1 = y + 108
    rcard(d, HM, y, W - HM, y1)
    left(d, name, (HM + 60, (y + y1) / 2), 42, WHITE, bold=True, min_size=32)
    left(d, "AC " + a, (W - 430, (y + y1) / 2), 34, LIGHT, min_size=28)
    left(d, "D " + dd, (W - 200, (y + y1) / 2), 34, GOLD, min_size=28)
    y = y1 + 16
center(d, "冲四大 · 户籍不卡你", (W / 2, 1180), 44, WHITE, min_size=36)
center(d, "D类尖子和深户尖子 · 同一条线拼分", (W / 2, 1290), 32, LIGHT, bold=False, min_size=26)
footer(d)
check("正文图2")
im.save(HERE + "P1-3-S3-ACD分差全景-小红书-正文图2-四大0分-1080x1440.png")

# ========== 正文图3：边缘之痛（500-529）15-23分 ==========
im, d = base()
center(d, "第4层 · 公办边缘 AC500-529", (W / 2, 90), 34, GOLD, min_size=27)
center(d, "15-23 分", (W / 2, 330), 150, WHITE, min_size=120)
center(d, "D类要明显多考 · 最该警惕的一段", (W / 2, 500), 46, GOLD, min_size=38)
rows = [
    ("深实崇文高中", "AC 506 → D 529", "差 23 分", WHITE),
    ("益新中学", "AC 517 → D 536", "差 19 分", WHITE),
    ("龙岗区第二高级中学", "AC 504 → D 522", "差 18 分", WHITE),
]
y = 600
for name, line, gap, col in rows:
    y1 = y + 176
    rcard(d, HM, y, W - HM, y1)
    left(d, name, (HM + 60, y + 52), 40, col, bold=True, min_size=32, right=640)
    rtext(d, gap, (980, y + 52), 40, GOLD)
    left(d, line, (HM + 60, y + 130), 30, LIGHT, min_size=25)
    y = y1 + 20
center(d, "22所里16所 D高10分以上", (W / 2, 1240), 40, WHITE, min_size=32)
center(d, "分数“能上但不确定哪所” · 这里策略比刷题重要", (W / 2, 1290), 32, LIGHT, bold=False, min_size=26)
footer(d)
check("正文图3")
im.save(HERE + "P1-3-S3-ACD分差全景-小红书-正文图3-边缘之痛-1080x1440.png")

# ========== 正文图4：新校反转（<500）20-31分 ==========
im, d = base()
center(d, "第5层 · 集团新校/综合高中班 AC<500", (W / 2, 90), 32, GOLD, min_size=26)
center(d, "20-31 分", (W / 2, 330), 150, WHITE, min_size=120)
center(d, "别信“新校区好考” · 2026它们分差最大", (W / 2, 500), 44, GOLD, min_size=36)
rows = [
    ("创新高级中学(综高)", "AC 487 → D 518", "差 31 分"),
    ("曙光中学(综合高中班)", "AC 497 → D 526", "差 29 分"),
    ("深圳中学数理高中", "AC 492 → D 517", "差 25 分"),
]
y = 600
for name, line, gap in rows:
    y1 = y + 176
    rcard(d, HM, y, W - HM, y1)
    left(d, name, (HM + 60, y + 52), 38, WHITE, bold=True, min_size=30, right=620)
    rtext(d, gap, (980, y + 52), 38, GOLD)
    left(d, line, (HM + 60, y + 130), 30, LIGHT, min_size=25)
    y = y1 + 20
center(d, "真正友好的是成熟区属校", (W / 2, 1240), 42, WHITE, min_size=34)
center(d, "科高龙岗分校 AC/D 同567 · 龙城高中同576", (W / 2, 1320), 32, LIGHT, bold=False, min_size=26)
footer(d)
check("正文图4")
im.save(HERE + "P1-3-S3-ACD分差全景-小红书-正文图4-新校反转-1080x1440.png")
print("done")
