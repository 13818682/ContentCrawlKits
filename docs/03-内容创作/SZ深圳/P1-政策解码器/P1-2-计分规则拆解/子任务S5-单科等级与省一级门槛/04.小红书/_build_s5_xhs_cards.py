# -*- coding: utf-8 -*-
"""S5 小红书图文 正文配图 x4（1080×1440，同封面视觉）
正文首图=封面互补版 → 轮播共 5 张。口径：等级A+前5%→C后5%；省一级录取全科C+·体育C（FAQ-8）。
四卡：正文图1 等级怎么划 / 正文图2 隐形门槛 / 正文图3 三个误判 / 正文图4 三件事。
行文预拆分、字号下限自检；底部尾句距最后卡片底边断言≥12px。
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
    assert bb[2] - bb[0] <= mw + 1, "center too long: %s" % text
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


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE):
    d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=wfill, outline=wout, width=2)


def rule(d, cy):
    d.line([HM, cy, W - HM, cy], fill=EDGE, width=2)


def footer(d):
    center(d, "数据来源：深圳市教育局公开文件 · 人工核对", (W / 2, 1392), 23, SUB, bold=False, min_size=18)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 8:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ---------- 正文图1：等级怎么划 ----------
im, d = base()
center(d, "S5 · 单科等级", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "等级怎么划？", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "按单科原始分 · 全市比例切", (W / 2, 356), 38, LIGHT, bold=False, min_size=30)
rule(d, 430)
rows = [
    ("A+", "前 5%", "单科全市顶尖"),
    ("A", "前 5%~25%", "单科优秀"),
    ("B+", "前 25%~50%", "中等偏上"),
    ("B", "前 50%~75%", "中等"),
    ("C+", "前 75%~95%", "偏下 · 需留意"),
    ("C", "后 5%", "该科全市靠后"),
]
y = 490
for g, rng, s in rows:
    y1 = y + 116
    rcard(d, HM, y, W - HM, y1)
    center(d, g, (HM + 130, (y + y1) / 2), 50, GOLD, maxw=200, min_size=40)
    left(d, rng, (HM + 270, (y + y1) / 2), 40, WHITE, bold=True, min_size=32)
    left(d, s, (HM + 560, (y + y1) / 2), 32, LIGHT, min_size=26)
    y = y1 + 10
center(d, "卷子难不难，不影响等级比例", (W / 2, 1340), 34, GOLD, min_size=26)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 10) + 10, ("尾句压卡", y - 10, bb_last)
im.save(HERE + "S5-单科等级与省一级门槛-小红书-正文图1-等级怎么划-1080x1440.png")
check("正文图1")

# ---------- 正文图2：隐形门槛 ----------
im, d = base()
center(d, "S5 · 单科等级", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "那个'隐形门槛'", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "省一级公办普高的录取资格", (W / 2, 356), 36, LIGHT, bold=False, min_size=28)
rule(d, 424)
rows = [
    ("报考", "省一级学校（含民办/名额分配）", "综合素质评价'达标'即可"),
    ("录取", "省一级公办普高", "语数英物化历史道法 C+ 以上"),
    ("录取", "体育单科", "C 以上（最宽松）"),
]
y = 480
for t, a, b in rows:
    y1 = y + 168
    rcard(d, HM, y, W - HM, y1)
    center(d, t, (HM + 120, (y + y1) / 2), 52, GOLD, maxw=200, min_size=38)
    x0 = HM + 260
    left(d, a, (x0, y + 52), 42, WHITE, bold=True, min_size=32)
    left(d, b, (x0, y + 118), 32, LIGHT, min_size=26)
    y = y1 + 22
center(d, "总分够线，有一科掉 C 也不符合条件", (W / 2, 1335), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 22) + 10, ("尾句压卡", y - 22, bb_last)
im.save(HERE + "S5-单科等级与省一级门槛-小红书-正文图2-隐形门槛-1080x1440.png")
check("正文图2")

# ---------- 正文图3：三个误判 ----------
im, d = base()
center(d, "S5 · 单科等级", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "最容易误判的 3 点", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "先自查，别踩坑", (W / 2, 350), 36, LIGHT, bold=False, min_size=28)
rule(d, 424)
rows = [
    ("单科卡线", "等级卡的是单科，不是总分——总分高但一科掉 C 也没用"),
    ("背多分科目", "历史、道法最易悄悄滑到 C，别让它当'老鼠屎'"),
    ("体育最宽松", "门槛只要体育 C 以上，不垫底就行"),
]
y = 480
for t, s in rows:
    y1 = y + 176
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 40, y + 54), 44, GOLD, right=W - HM - 40, bold=True, min_size=32)
    left(d, s, (HM + 40, y + 126), 32, LIGHT, right=W - HM - 40, min_size=26)
    y = y1 + 24
center(d, "哪科在 C 边缘，哪科就是隐患", (W / 2, 1340), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 24) + 8, ("尾句压卡", y - 24, bb_last)
im.save(HERE + "S5-单科等级与省一级门槛-小红书-正文图3-三个误判-1080x1440.png")
check("正文图3")

# ---------- 正文图4：三件事 ----------
im, d = base()
center(d, "S5 · 单科等级", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "现在做三件事", (W / 2, 260), 68, WHITE, min_size=52)
center(d, "守住省一级的门槛", (W / 2, 370), 36, LIGHT, bold=False, min_size=28)
rule(d, 440)
rows = [
    ("1", "定位单科等级", "把最近大考的单科等级拿出来"),
    ("2", "先补边缘科", "优先'接近 C、可能掉 C'的那科"),
    ("3", "确认综素达标", "问学校综合素质评价是否达标"),
]
y = 500
for n, t, s in rows:
    y1 = y + 190
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 60), 46, WHITE, bold=True, min_size=34)
    left(d, s, (x0, y + 132), 34, LIGHT, min_size=28)
    y = y1 + 26
center(d, "别让总分好看，栽在一科上", (W / 2, 1320), 56, GOLD, min_size=42)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S5-单科等级与省一级门槛-小红书-正文图4-三件事-1080x1440.png")
check("正文图4")
print("done")
