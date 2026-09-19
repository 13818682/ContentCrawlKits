# -*- coding: utf-8 -*-
"""S4 小红书图文 正文配图 x4（1080×1440，同封面视觉）
正文首图=封面互补版 → 轮播共 5 张。口径：体育总分50=过程14+现场36。
四卡：正文图1 怎么攒 / 正文图2 先查旧账 / 正文图3 现场考什么 / 正文图4 三件事。
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


# ---------- 正文图1：怎么攒 ----------
im, d = base()
center(d, "S4 · 体育 50 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "攒的那 14 分", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "过程性评价 · 几乎考'人到齐'", (W / 2, 356), 38, LIGHT, bold=False, min_size=30)
rule(d, 430)
rows = [
    ("1", "体质测试 9 分", ["初中三年每年测 · 及格即得 3 分"]),
    ("2", "体育课/大课间 3 分", ["每年 1 分 · 正常参与就给"]),
    ("3", "通识考试 2 分", ["初二下机考开卷 · 80 分以上满分"]),
]
y = 490
for n, t, subs in rows:
    y1 = y + 190
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 62), 46, WHITE, bold=True, min_size=34)
    for i, s in enumerate(subs):
        left(d, s, (x0, y + 122 + i * 46), 33, LIGHT, min_size=26)
    y = y1 + 26
center(d, "丢分多半是体测请假、体育课缺勤", (W / 2, 1300), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S4-体育三年累积-小红书-正文图1-怎么攒-1080x1440.png")
check("正文图1")

# ---------- 正文图2：先查旧账 ----------
im, d = base()
center(d, "S4 · 体育 50 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "升初三了，先查两笔旧账", (W / 2, 250), 60, WHITE, min_size=46)
center(d, "前两年约 8 分 · 基本已入档", (W / 2, 360), 38, LIGHT, bold=False, min_size=30)
rule(d, 430)
rows = [
    ("1", "体质测试", "初一初二两年各测了吗 · 及格了吗"),
    ("2", "体育课 / 大课间", "有没有长期缺勤 · 漏了哪次"),
    ("3", "通识考试", "初二下那场 · 有没有拿到满分"),
]
y = 490
for n, t, s in rows:
    y1 = y + 176
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 56), 44, WHITE, bold=True, min_size=32)
    left(d, s, (x0, y + 120), 32, LIGHT, min_size=26)
    y = y1 + 24
center(d, "找体育老师确认，别等中考前才发现", (W / 2, 1330), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 24) + 8, ("尾句压卡", y - 24, bb_last)
im.save(HERE + "S4-体育三年累积-小红书-正文图2-先查旧账-1080x1440.png")
check("正文图2")

# ---------- 正文图3：现场考什么 ----------
im, d = base()
center(d, "S4 · 体育 50 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "考的 36 分，选什么", (W / 2, 250), 66, WHITE, min_size=50)
center(d, "三大类 16 选项 · 每类选 1 项", (W / 2, 360), 38, LIGHT, bold=False, min_size=30)
rule(d, 430)
rows = [
    ("1", "一类 · 耐力（三选一）", "长跑800/1000米 · 200米游泳 · 4分钟跳绳"),
    ("2", "二类 · 速度力量灵敏（七选一）", "100米 · 50米游泳 · 实心球 · 跳绳 · 毽子 · 蛙跳 · 折返跑"),
    ("3", "三类 · 球类（六选一）", "足球 · 篮球 · 排球 · 乒乓球 · 羽毛球 · 网球"),
]
y = 490
for n, t, s in rows:
    y1 = y + 180
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 54), 42, WHITE, bold=True, min_size=32)
    left(d, s, (x0, y + 124), 31, LIGHT, min_size=24)
    y = y1 + 24
center(d, "平均 × 0.36 ＝ 36 分 · 4 月中下旬考", (W / 2, 1330), 38, GOLD, min_size=30)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 24) + 8, ("尾句压卡", y - 24, bb_last)
im.save(HERE + "S4-体育三年累积-小红书-正文图3-现场考什么-1080x1440.png")
check("正文图3")

# ---------- 正文图4：三件事 ----------
im, d = base()
center(d, "S4 · 体育 50 分", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "现在做三件事", (W / 2, 260), 68, WHITE, min_size=52)
center(d, "别等 4 月才突击", (W / 2, 370), 36, LIGHT, bold=False, min_size=28)
rule(d, 440)
rows = [
    ("1", "三类定项", "球类选能长期约到人、真练得起来的"),
    ("2", "查旧账", "前两年过程分有没有漏"),
    ("3", "每周练 3 次", "耐力是慢功夫，现在就开始"),
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
center(d, "攒的守住 · 考的早练", (W / 2, 1320), 62, GOLD, min_size=46)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S4-体育三年累积-小红书-正文图4-三件事-1080x1440.png")
check("正文图4")
print("done")
