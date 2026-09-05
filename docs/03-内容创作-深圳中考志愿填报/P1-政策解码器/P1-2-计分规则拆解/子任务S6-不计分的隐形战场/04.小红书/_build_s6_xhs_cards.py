# -*- coding: utf-8 -*-
"""S6 小红书图文 正文配图 x4（1080×1440，同封面视觉）
正文首图=封面精炼版 → 轮播共 5 张。口径：同分=先生地合卷·后语数英（FAQ-7）。
四卡：正文图1 同分怎么比 / 正文图2 真实案例 / 正文图3 生地已定格 / 正文图4 三件事。
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


# ---------- 正文图1：同分怎么比 ----------
im, d = base()
center(d, "S6 · 同分怎么比", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "官方就比两样，顺序不能反", (W / 2, 250), 60, WHITE, min_size=46)
center(d, "中考总分相同才触发 · 不同分不比", (W / 2, 360), 36, LIGHT, bold=False, min_size=28)
rule(d, 430)
rows = [
    ("1", "先比：生地（合卷）分数", ["高者优先录取"]),
    ("2", "生地同 → 再比：语数英总分", ["生地完全相同才看这层"]),
]
y = 490
for n, t, subs in rows:
    y1 = y + 200
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 92, GOLD, maxw=150, min_size=58)
    x0 = HM + 250
    left(d, t, (x0, y + 70), 44, WHITE, bold=True, min_size=32)
    for i, s in enumerate(subs):
        left(d, s, (x0, y + 138 + i * 40), 32, LIGHT, min_size=26)
    y = y1 + 26
rcard(d, HM, y, W - HM, y + 150)
left(d, "生地是第一道闸", (HM + 40, y + 54), 42, GOLD, right=W - HM - 40, bold=True, min_size=32)
left(d, "语数英对冲不了生地劣势", (HM + 40, y + 112), 32, LIGHT, right=W - HM - 40, min_size=26)
y = y + 150
center(d, "顺序反了，就是最大的误会", (W / 2, 1335), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= y + 12, ("尾句压卡", y, bb_last)
im.save(HERE + "S6-不计分的隐形战场-小红书-正文图1-同分怎么比-1080x1440.png")
check("正文图1")

# ---------- 正文图2：真实案例 ----------
im, d = base()
center(d, "S6 · 同分 PK", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "差 1 分，定一个学位", (W / 2, 250), 64, WHITE, min_size=48)
center(d, "往年真实录取 · 某校最后一个名额", (W / 2, 360), 34, LIGHT, bold=False, min_size=27)
# 左右对照卡
cw = (W - 2 * HM - 40) // 2
xc0 = HM; xc1 = HM + cw
rcard(d, xc0, 470, xc1, 1000)
center(d, "考生 A", ((xc0 + xc1) / 2, 560), 52, GOLD, min_size=42)
center(d, "生地 96 分", ((xc0 + xc1) / 2, 700), 56, WHITE, min_size=44)
center(d, "录 取", ((xc0 + xc1) / 2, 900), 60, GOLD, min_size=46)
yc0 = xc1 + 40; yc1 = W - HM
rcard(d, yc0, 470, yc1, 1000)
center(d, "考生 B", ((yc0 + yc1) / 2, 560), 52, GOLD, min_size=42)
center(d, "生地 82 分", ((yc0 + yc1) / 2, 700), 56, WHITE, min_size=44)
center(d, "落 选", ((yc0 + yc1) / 2, 900), 60, WHITE, min_size=46)
center(d, "总分相同 · 都是 552", (W / 2, 1120), 44, GOLD, min_size=34)
center(d, "差不在语数英，在两年前那场生地考", (W / 2, 1330), 38, WHITE, min_size=30)
bb_last = BOXES[-1][1]
assert bb_last[1] >= 1170, ("尾句撞金句行", bb_last)   # 尾句顶 ≥ y1120 行底(~1150)+20
assert bb_last[3] <= H - 8, ("尾句越底", bb_last)
im.save(HERE + "S6-不计分的隐形战场-小红书-正文图2-真实案例-1080x1440.png")
check("正文图2")

# ---------- 正文图3：生地已定格 ----------
im, d = base()
center(d, "S6 · 生地已定格", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "生地，已经考完了", (W / 2, 250), 64, WHITE, min_size=48)
center(d, "初二下学期考 · 分数定格不改", (W / 2, 360), 36, LIGHT, bold=False, min_size=28)
rule(d, 430)
rows = [
    ("已定", "生地分数改不了", "纠结无用 · 读懂规则更重要"),
    ("只在同分", "PK 才触发", "大部分录取在总分就分胜负"),
    ("能做的", "拉高总分", "语数英物化才是更稳的路"),
]
y = 490
for t, a, b in rows:
    y1 = y + 176
    rcard(d, HM, y, W - HM, y1)
    center(d, t, (HM + 130, (y + y1) / 2), 48, GOLD, maxw=220, min_size=36)
    x0 = HM + 280
    left(d, a, (x0, y + 54), 42, WHITE, bold=True, min_size=32)
    left(d, b, (x0, y + 120), 32, LIGHT, min_size=26)
    y = y1 + 24
center(d, "生地不理想别慌，把总分做扎实", (W / 2, 1335), 36, WHITE, min_size=28)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 24) + 8, ("尾句压卡", y - 24, bb_last)
im.save(HERE + "S6-不计分的隐形战场-小红书-正文图3-生地已定格-1080x1440.png")
check("正文图3")

# ---------- 正文图4：三件事 ----------
im, d = base()
center(d, "S6 · 现在能做的三件事", (W / 2, 74), 33, GOLD, min_size=24)
center(d, "别等填志愿才发现", (W / 2, 260), 64, WHITE, min_size=48)
center(d, "生地已定 · 剩下交给总分", (W / 2, 370), 34, LIGHT, bold=False, min_size=27)
rule(d, 440)
rows = [
    ("1", "确认生地成绩", "同分 PK 第一依据 · 别记错分"),
    ("2", "拉高总分", "生地弱就靠语数英物化拉开"),
    ("3", "目标设高一点", "比心仪校往年线高 · 避开 PK 区"),
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
center(d, "读懂规则，就是优势", (W / 2, 1320), 58, GOLD, min_size=44)
bb_last = BOXES[-1][1]
assert bb_last[1] >= (y - 26) + 12, ("尾句压卡", y - 26, bb_last)
footer(d)
im.save(HERE + "S6-不计分的隐形战场-小红书-正文图4-三件事-1080x1440.png")
check("正文图4")
print("done")
