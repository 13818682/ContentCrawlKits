# -*- coding: utf-8 -*-
"""S3 小红书图文 正文配图 x4（1080×1440，同封面视觉）
正文首图=封面互补版 → 轮播共 5 张。口径(短载体)：2026 道法闭卷→开卷、能带纸质材料/禁电子设备（官方说明）。
四卡：正文图1 怎么变 / 正文图2 能带什么 / 正文图3 为什么不是送分 / 正文图4 三件事怎么练。
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


# ---------- 正文图1：怎么变 ----------
im, d = base()
center(d, "S3 · 道法改开卷", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "它到底怎么变？", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "50 分 · 50 分钟都不变", (W / 2, 356), 44, GOLD, min_size=34)
rule(d, 424)
rows = [
    ("1", "闭卷 → 开卷", ["深圳中考计分笔试里唯一开卷"]),
    ("2", "考法变了", ["考记忆 → 考理解与会用材料"]),
    ("3", "日期定了", ["2026 · 6 月 27 日下午场"]),
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
center(d, "分值没涨——但考法，比涨分更要命", (W / 2, 1300), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S3-道德与法治开卷-小红书-正文图1-怎么变-1080x1440.png")
check("正文图1")

# ---------- 正文图2：能带什么 ----------
im, d = base()
center(d, "S3 · 道法改开卷", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "能带什么进场？", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "官方说明 · 别被误导", (W / 2, 350), 38, LIGHT, bold=False, min_size=30)
rule(d, 424)
rows = [
    ("可带", "教科书等纸质材料", "自己整理的笔记、速查页也能带"),
    ("禁带", "手机 / 电子存储设备", "通讯工具、记忆录放设备都不行"),
]
y = 480
for n, t, s in rows:
    y1 = y + 176
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 52, GOLD, maxw=190, min_size=36)
    x0 = HM + 250
    left(d, t, (x0, y + 60), 46, WHITE, bold=True, min_size=34)
    left(d, s, (x0, y + 122), 33, LIGHT, min_size=26)
    y = y1 + 26
rcard(d, HM, y, W - HM, y + 170)
left(d, "'只能带教材' 是谣言", (HM + 40, y + 62), 42, GOLD, right=W - HM - 40, bold=True, min_size=32)
left(d, "官方已辟谣：无此规定", (HM + 40, y + 122), 32, LIGHT, right=W - HM - 40, min_size=26)
y = y + 170
center(d, "纸质材料越早备好，开卷越加分", (W / 2, 1330), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= y + 12, ("尾句压卡", y, bb_last)
im.save(HERE + "S3-道德与法治开卷-小红书-正文图2-能带什么-1080x1440.png")
check("正文图2")

# ---------- 正文图3：为什么不是送分 ----------
im, d = base()
center(d, "S3 · 道法改开卷", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "开卷 ≠ 送分", (W / 2, 250), 68, WHITE, min_size=52)
center(d, "三个最容易被忽视的坑", (W / 2, 360), 38, LIGHT, bold=False, min_size=30)
rule(d, 430)
rows = [
    ("书里没答案", "考理解与综合——材料题抄不到分点"),
    ("翻书很慢", "50 分钟，每道题都翻就做不完"),
    ("死背没用", "减的是死记硬背，考的是会用材料"),
]
y = 490
for t, s in rows:
    y1 = y + 170
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 40, y + 56), 44, GOLD, right=W - HM - 40, bold=True, min_size=32)
    left(d, s, (HM + 40, y + 122), 33, LIGHT, right=W - HM - 40, min_size=26)
    y = y1 + 24
center(d, "差距不在带多少，在 3 秒能不能找到", (W / 2, 1340), 34, WHITE, min_size=26)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 24) + 8, ("尾句压卡", y - 24, bb_last)
im.save(HERE + "S3-道德与法治开卷-小红书-正文图3-为什么不是送分-1080x1440.png")
check("正文图3")

# ---------- 正文图4：三件事怎么练 ----------
im, d = base()
center(d, "S3 · 道法改开卷", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "怎么练？三件事", (W / 2, 260), 68, WHITE, min_size=52)
center(d, "把书从'要背的'改成'能查的'", (W / 2, 370), 36, LIGHT, bold=False, min_size=28)
rule(d, 440)
rows = [
    ("1", "做快速索引", "按单元标考点页码，贴书前"),
    ("2", "备纸质速查页", "时政热词、易混概念一页纸"),
    ("3", "开卷视角复盘", "错在找不到，还是找到了不会用？"),
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
center(d, "会查，比带得多重要", (W / 2, 1320), 62, GOLD, min_size=46)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S3-道德与法治开卷-小红书-正文图4-三件事怎么练-1080x1440.png")
check("正文图4")
print("done")
