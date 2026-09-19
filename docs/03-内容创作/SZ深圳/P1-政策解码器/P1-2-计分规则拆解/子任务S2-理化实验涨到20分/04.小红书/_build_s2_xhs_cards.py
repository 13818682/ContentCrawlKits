# -*- coding: utf-8 -*-
"""S2 小红书图文 正文配图 x4（1080×1440，同封面视觉）
正文首图=封面互补版 → 轮播共 5 张。口径(短载体)：理化实验 2026 涨到 20 分，不写原 12 分。
四卡：正文图1 怎么考 / 正文图2 丢分三坑 / 正文图3 三招怎么练 / 正文图4 物化重点+总纲。
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


# ---------- 正文图1：怎么考 ----------
im, d = base()
center(d, "S2 · 理化实验 20 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "这 20 分，怎么考？", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "物化 140 ＝ 笔试 120 ＋ 实验 20", (W / 2, 356), 44, GOLD, min_size=34)
rule(d, 424)
rows = [
    ("1", "物、化各考 1 个实验", ["现场动手做"]),
    ("2", "每科 10 分钟", ["共 20 分 · 5 月进行"]),
    ("3", "评分到每一步", ["连接 · 读数 · 记录 · 复位"]),
]
y = 470
for n, t, subs in rows:
    y1 = y + 190
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 62), 46, WHITE, bold=True, min_size=34)
    for i, s in enumerate(subs):
        left(d, s, (x0, y + 122 + i * 46), 33, LIGHT, min_size=26)
    y = y1 + 26
center(d, "纯操作分——刷题刷不出来，练了就稳", (W / 2, 1300), 38, WHITE, min_size=30)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S2-理化实验涨到20分-小红书-正文图1-怎么考-1080x1440.png")
check("正文图1")

# ---------- 正文图2：丢分三坑 ----------
im, d = base()
center(d, "S2 · 理化实验 20 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "丢一半分，多半是这个原因", (W / 2, 250), 58, WHITE, min_size=44)
center(d, "看同学做、抄报告", (W / 2, 430), 88, GOLD, min_size=64)
center(d, "＝ 从没亲手完整做一遍", (W / 2, 560), 46, WHITE, min_size=36)
center(d, "进考场不是不会，是手生", (W / 2, 660), 40, LIGHT, bold=False, min_size=32)
rule(d, 730)
rows = [
    ("只看没做", "实验课坐后排看别人动手 → 考场第一分钟就卡"),
    ("步骤乱、会漏", "只记结论不记顺序 → 忘读数、漏复位"),
    ("一紧张就超时", "10 分钟限时 → 做不完比做错更亏"),
]
y = 790
for t, s in rows:
    y1 = y + 156
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 40, y + 52), 42, GOLD, right=W - HM - 40, bold=True, min_size=32)
    left(d, s, (HM + 40, y + 112), 32, LIGHT, right=W - HM - 40, min_size=26)
    y = y1 + 24
center(d, "三步自查，看看孩子中了几条", (W / 2, 1360), 34, WHITE, min_size=26)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 24) + 8, ("尾句压卡", y - 24, bb_last)
im.save(HERE + "S2-理化实验涨到20分-小红书-正文图2-丢分三坑-1080x1440.png")
check("正文图2")

# ---------- 正文图3：三招怎么练 ----------
im, d = base()
center(d, "S2 · 理化实验 20 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "怎么练？三招就够", (W / 2, 260), 68, WHITE, min_size=52)
center(d, "实验靠肌肉记忆，突击不了一个月", (W / 2, 370), 38, LIGHT, bold=False, min_size=30)
rule(d, 440)
rows = [
    ("1", "这学期起", "每节实验课自己动手，当主科上，别再做观众"),
    ("2", "考前 1-2 个月", "学校集中练——黄金期，一节都别请假"),
    ("3", "随时", "录一次自己操作回看，扣分点一眼看出"),
]
y = 500
for n, t, s in rows:
    y1 = y + 190
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 60), 46, WHITE, bold=True, min_size=34)
    left(d, s, (x0, y + 130), 34, LIGHT, min_size=28)
    y = y1 + 26
center(d, "练了就基本稳", (W / 2, 1320), 66, GOLD, min_size=50)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S2-理化实验涨到20分-小红书-正文图3-三招怎么练-1080x1440.png")
check("正文图3")

# ---------- 正文图4：物化重点+总纲 ----------
im, d = base()
center(d, "S2 · 理化实验 20 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "物理 / 化学，各练什么", (W / 2, 250), 60, WHITE, min_size=46)
center(d, "跟紧学校实验的抓手", (W / 2, 350), 36, LIGHT, bold=False, min_size=28)
cw = (W - 2 * HM - 40) // 2
# 左卡：物理
xc0 = HM
xc1 = HM + cw
rcard(d, xc0, 440, xc1, 1120)
center(d, "物理", ((xc0 + xc1) / 2, 540), 64, GOLD, min_size=48)
center(d, "电路连接与测量", ((xc0 + xc1) / 2, 700), 48, WHITE, min_size=36)
center(d, "接线顺序", ((xc0 + xc1) / 2, 850), 36, LIGHT, bold=False, min_size=28)
center(d, "电流表 / 电压表读数", ((xc0 + xc1) / 2, 940), 36, LIGHT, bold=False, min_size=28)
# 右卡：化学
yc0 = xc1 + 40
yc1 = W - HM
rcard(d, yc0, 440, yc1, 1120)
center(d, "化学", ((yc0 + yc1) / 2, 540), 64, GOLD, min_size=48)
center(d, "气体制取与检验", ((yc0 + yc1) / 2, 700), 46, WHITE, min_size=36)
center(d, "物质的鉴别与分离", ((yc0 + yc1) / 2, 800), 46, WHITE, min_size=36)
center(d, "先检验，后收集", ((yc0 + yc1) / 2, 940), 36, LIGHT, bold=False, min_size=28)
center(d, "动手的 20 分，练了就基本稳", (W / 2, 1260), 56, GOLD, min_size=42)
footer(d)
im.save(HERE + "S2-理化实验涨到20分-小红书-正文图4-物化重点-1080x1440.png")
check("正文图4")
print("done")
