# -*- coding: utf-8 -*-
"""S1 小红书图文 正文配图 x4（1080×1440，与封面互补版同款视觉：深蓝渐变+金）
正文首图=封面互补版(已有) → 轮播共 5 张。口径：630=440笔试主科(含听口)+20实验+170史道体。
四卡：正文图1 630对账总表 / 正文图2 精力三档 / 正文图3 三步用表 / 正文图4 一句话总纲。
设计约束：行文本预拆分到短行，字号不低于下限（手机上约≥11px），超宽即报错提醒改文案。
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
YL = 60; YH = 1410
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


def center(d, text, xy, size, fill, bold=True, maxw=None, min_size=30):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else W - 2 * HM
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "center too long (%d>%d): %s" % (bb[2], mw, text)
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BOXES.append(("C:" + text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def left(d, text, xy, size, fill, right=None, bold=False, min_size=32):
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


def rcard(d, y0, y1):
    d.rounded_rectangle([HM, y0, W - HM, y1], radius=24, fill=CARD, outline=EDGE, width=2)


def rule(d, cy):
    d.line([HM, cy, W - HM, cy], fill=EDGE, width=2)


def footer(d):
    center(d, "数据来源：深圳市教育局公开文件 · 人工核对", (W / 2, 1392), 23, SUB, bold=False, min_size=18)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < YL or bb[1] < 6 or bb[2] > W - YL or bb[3] > YH + 34:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ---------- 正文图1：630 对账总表 ----------
im, d = base()
center(d, "S1 · 8科分值 · 对账版", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "630 分 ＝ 440 ＋ 20 ＋ 170", (W / 2, 250), 74, GOLD, min_size=56)
center(d, "8科分值，一分不差——这张表收藏就够用", (W / 2, 350), 38, LIGHT, bold=False, min_size=30)
rule(d, 424)

rows = [
    ("440", "笔试主科 · 决定你站哪档",
     ["语文120 · 数学100 · 英语100（含听口25）",
      "物化笔试120"]),
    ("20", "理化实验 · 2026 = 20 分",
     ["物理/化学各做1个实验 · 现场动手",
      "纯操作分——刷题刷不出来"]),
    ("170", "历史·道法·体育 · 稳住即可",
     ["历史70 · 道法50 · 体育50",
      "体育=过程14+现场36 · 道法2026开卷"]),
]
y = 468
for num, title, subs in rows:
    y1 = y + 224
    rcard(d, y, y1)
    center(d, num, (HM + 130, (y + y1) / 2), 100, GOLD, maxw=230, min_size=64)
    x0 = HM + 300
    left(d, title, (x0, y + 58), 45, WHITE, bold=True, min_size=34)
    for i, s in enumerate(subs):
        left(d, s, (x0, y + 120 + i * 50), 34, LIGHT, min_size=28)
    y = y1 + 24
band_end = y - 24
f = center(d, "主科优先 · 实验跟练 · 副科稳住", (W / 2, 1300), 40, WHITE, min_size=32)
bb = d.textbbox((W / 2, 1300), "主科优先 · 实验跟练 · 副科稳住", font=f, anchor="mm")
assert bb[1] >= band_end + 12, ("尾句压最后卡片底边", band_end, bb)
footer(d)
im.save(HERE + "S1-630构成-小红书-正文图1-630对账总表-1080x1440.png")
check("正文图1")

# ---------- 正文图2：精力三档 ----------
im, d = base()
center(d, "S1 · 630构成 · 精力三档", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "三档精力，照着分", (W / 2, 250), 68, WHITE, min_size=52)
center(d, "别平均用力——同一小时在不同科，回报差很多", (W / 2, 350), 37, LIGHT, bold=False, min_size=30)
rule(d, 424)

rows = [
    ("主战场", "440 分 · 语数英＋物化笔试", ["决定你进哪一档", "黄金时间先给它们"]),
    ("动手分", "20 分 · 理化实验", ["2026=20分 · 纯操作分", "跟住学校实验课真练"]),
    ("稳定分", "170 分 · 历史·道法·体育", ["稳住即可", "别让副科题海吃掉主科时间"]),
]
y = 468
for kind, sub, lines in rows:
    y1 = y + 224
    rcard(d, y, y1)
    center(d, kind, (HM + 145, (y + y1) / 2), 56, GOLD, maxw=200, min_size=40)
    x0 = HM + 300
    left(d, sub, (x0, y + 58), 45, WHITE, bold=True, min_size=34)
    for i, s in enumerate(lines):
        left(d, s, (x0, y + 118 + i * 46), 32, LIGHT, min_size=26)
    y = y1 + 24
band_end = y - 24
f1 = center(d, "再锁两分确定性高：英语听口 25（5月先考）", (W / 2, 1280), 34, GOLD, min_size=28)
bb1 = d.textbbox((W / 2, 1280), "再锁两分确定性高：英语听口 25（5月先考）", font=f1, anchor="mm")
assert bb1[1] >= band_end + 12, ("尾句压最后卡片底边", band_end, bb1)
center(d, "体育过程 14（已累积就确认）", (W / 2, 1342), 34, GOLD, min_size=28)
footer(d)
im.save(HERE + "S1-630构成-小红书-正文图2-精力三档-1080x1440.png")
check("正文图2")

# ---------- 正文图3：三步用表 ----------
im, d = base()
center(d, "S1 · 8科分值 · 拿来就用", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "这张表怎么用？三步", (W / 2, 250), 64, WHITE, min_size=50)
center(d, "先分清主次，再谈提分", (W / 2, 344), 37, LIGHT, bold=False, min_size=30)
rule(d, 414)

steps = [
    ("1", "对一遍成绩单", ["分清「主战场（主科）」与「稳定分（史道体）」"]),
    ("2", "早锁确定性高分", ["英语听口 25 分（5月先机考）", "体育过程 14 分（已累积就确认）"]),
    ("3", "主抓两个拉分点", ["语文作文 50 分", "数学压轴题"]),
]
y = 470
for n, t, lines in steps:
    y1 = y + 245
    rcard(d, y, y1)
    center(d, n, (HM + 120, (y + y1) / 2), 92, GOLD, maxw=150, min_size=60)
    x0 = HM + 270
    left(d, t, (x0, y + 70), 46, WHITE, bold=True, min_size=34)
    for i, s in enumerate(lines):
        left(d, s, (x0, y + 140 + i * 50), 34, LIGHT, min_size=28)
    y = y1 + 30
footer(d)
im.save(HERE + "S1-630构成-小红书-正文图3-三步用表-1080x1440.png")
check("正文图3")

# ---------- 正文图4：一句话总纲 ----------
im, d = base()
center(d, "S1 · 8科分值 · 收好这句", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "一句话记住这张表", (W / 2, 320), 62, WHITE, min_size=48)
center(d, "主科优先", (W / 2, 610), 128, GOLD, maxw=880, min_size=84)
center(d, "实验跟练 · 副科稳住", (W / 2, 830), 78, WHITE, maxw=920, min_size=58)
center(d, "主科定你站哪档，副科别拖后腿", (W / 2, 1020), 42, LIGHT, bold=False, min_size=32)
center(d, "想看 8 科逐科怎么考？关注「政策解码器」", (W / 2, 1240), 38, WHITE, min_size=30)
center(d, "收藏本篇，不迷路", (W / 2, 1302), 34, GOLD, min_size=26)
footer(d)
im.save(HERE + "S1-630构成-小红书-正文图4-一句话总纲-1080x1440.png")
check("正文图4")
print("done")
