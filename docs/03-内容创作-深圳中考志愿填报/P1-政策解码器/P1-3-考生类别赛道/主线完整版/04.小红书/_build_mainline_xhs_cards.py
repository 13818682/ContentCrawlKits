# -*- coding: utf-8 -*-
"""P1-3 主线完整版 小红书图文卡（1080×1440 轮播：封面1 + 正文图5）
封面=精简版（深圳中考/AC类还是D类？/先弄清是哪一类，再谈分数）；
正文图5张：①三类一句话 ②D类5条件 ③分差五层 ④D类三张牌 ⑤现在4件事。
口径：ACD三类、D类5条件官方版、分差2026参考。收藏向，图承结论、文承关键词。
模板：S6 cards + S6 封面精简版。
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


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE):
    d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=wfill, outline=wout, width=2)


def rule(d, cy):
    d.line([HM, cy, W - HM, cy], fill=EDGE, width=2)


def footer(d):
    center(d, "数据来源：深圳市教育局公开文件 · 人工核对（2026参考）", (W / 2, 1390), 22, SUB, bold=False, min_size=17)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 8:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ========== 封面（精炼版）==========
im, d = base()
f = center(d, "深圳中考", (W / 2, 170), 96, GOLD, maxw=940, min_size=70)
bb = d.textbbox((W / 2, 170), "深圳中考", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 285, W / 2 + half, 285], fill=GOLD, width=8)
f2 = center(d, "AC类还是D类？", (W / 2, 540), 150, WHITE, maxw=980, min_size=112)
bb2 = d.textbbox((W / 2, 540), "AC类还是D类？", font=f2, anchor="mm")
half2 = (bb2[2] - bb2[0]) / 2 + 8
d.line([W / 2 - half2, 700, W / 2 + half2, 700], fill=GOLD, width=6)
center(d, "先弄清是哪一类，再谈分数", (W / 2, 850), 64, GOLD, maxw=980, min_size=50)
center(d, "备考策略 · 收藏不迷路 · 数据见正文", (W / 2, 1360), 26, SUB, bold=False, min_size=20)
check("封面")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-小红书-封面-精炼版-1080x1440.png")

# ========== 正文图1：三类一句话 ==========
im, d = base()
center(d, "ACD · 三类一句话", (W / 2, 84), 34, GOLD, min_size=26)
center(d, "先分清自己是哪一类", (W / 2, 250), 62, WHITE, min_size=46)
rows = [
    ("A", "深户 + 学籍同区", "最宽 · 公办都能报", GOLD),
    ("C", "深户 + 学籍跨区", "报名要二选一 · 别忽略", WHITE),
    ("D", "非深户", "占一半多 · 公办指标约23%", WHITE),
]
y = 400
for tag, t, s, col in rows:
    y1 = y + 250
    rcard(d, HM, y, W - HM, y1)
    center(d, tag, (HM + 120, (y + y1) / 2), 100, GOLD, maxw=170, min_size=70)
    x0 = HM + 260
    left(d, t, (x0, y + 70), 48, WHITE, bold=True, min_size=34)
    left(d, s, (x0, y + 155), 34, LIGHT, min_size=26)
    y = y1 + 30
center(d, "D 类非深户：竞争最激烈，信息准备回报也最高", (W / 2, 1330), 34, GOLD, min_size=27)
bb_last = BOXES[-1][1]
assert bb_last[1] >= y, ("尾句压卡", y, bb_last)
footer(d)
check("正文图1")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-小红书-正文图1-三类一句话-1080x1440.png")

# ========== 正文图2：D类5条件 ==========
im, d = base()
center(d, "D类 · 5 个报名条件", (W / 2, 84), 34, GOLD, min_size=26)
center(d, "缺一不可 · 材料要提前", (W / 2, 250), 58, WHITE, min_size=44)
rows = [
    ("1", "合法稳定职业", "父母一方在深"),
    ("2", "合法稳定住所", "租房要租赁凭证"),
    ("3", "持深圳有效居住证", "别过期"),
    ("4", "社保养老+医疗", "一个险种满3年·补缴不计"),
    ("5", "3年完整初中学籍", "在深读完初中"),
]
y = 380
for n, t, s in rows:
    y1 = y + 158
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 100, (y + y1) / 2), 72, GOLD, maxw=130, min_size=50)
    x0 = HM + 220
    left(d, t, (x0, y + 48), 40, WHITE, bold=True, min_size=30)
    left(d, s, (x0, y + 110), 30, LIGHT, min_size=24)
    y = y1 + 22
center(d, "条件不全也能考 · 但只限民办补录/中职", (W / 2, 1320), 32, GOLD, min_size=26)
footer(d)
check("正文图2")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-小红书-正文图2-D类5条件-1080x1440.png")

# ========== 正文图3：分差五层 ==========
im, d = base()
center(d, "AC vs D · 分差五层", (W / 2, 84), 34, GOLD, min_size=26)
center(d, "越顶尖 · D 类越不吃亏", (W / 2, 250), 56, WHITE, min_size=42)
rows = [
    ("四大名校", "0 分", GOLD),
    ("八大/十大", "0-5 分", WHITE),
    ("30强", "5-15 分", WHITE),
    ("50强", "10-20 分", WHITE),
    ("百强/新校", "5-15 分", WHITE),
]
y = 390
for t, s, col in rows:
    y1 = y + 150
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 60, (y + y1) / 2), 44, WHITE, bold=True, min_size=34)
    center(d, s, (W - HM - 140, (y + y1) / 2), 48, col, maxw=260, min_size=38)
    y = y1 + 20
center(d, "目标四大大胆冲 · 中下层策略比努力更重要", (W / 2, 1320), 32, GOLD, min_size=26)
footer(d)
check("正文图3")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-小红书-正文图3-分差五层-1080x1440.png")

# ========== 正文图4：D类三张牌 ==========
im, d = base()
center(d, "D 类 · 三张牌", (W / 2, 84), 34, GOLD, min_size=26)
center(d, "数据残酷，但出路不止一条", (W / 2, 260), 54, WHITE, min_size=42)
cards = [
    ("① 指标生已覆盖D类", "同校D类竞争 · 排名靠前降分大", GOLD),
    ("② 民办AC/D同分", "49所民办同分录取 · 直接保底", WHITE),
    ("③ 3+4中本贯通", "中职3年+本科4年 · 拿全日制本科", WHITE),
]
y = 400
for t, s, col in cards:
    y1 = y + 250
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 60, y + 90), 50, col, bold=True, min_size=36)
    left(d, s, (HM + 60, y + 175), 32, LIGHT, min_size=26)
    y = y1 + 30
center(d, "D 类不是死胡同 · 是路要选对", (W / 2, 1330), 42, GOLD, min_size=34)
footer(d)
check("正文图4")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-小红书-正文图4-D类三张牌-1080x1440.png")

# ========== 正文图5：现在4件事 ==========
im, d = base()
center(d, "不管哪一类 · 现在 4 件事", (W / 2, 84), 34, GOLD, min_size=26)
center(d, "先认赛道 · 再谈分数", (W / 2, 250), 56, WHITE, min_size=42)
rows = [
    ("1", "确认考生类别", "AC查学籍户籍 · D查5条件"),
    ("2", "查分差", "目标校 AC/D 差多少"),
    ("3", "研究指标生", "本校名额·校内排名"),
    ("4", "按类别筛校", "HSEE 按 D 类/AC 类筛选"),
]
y = 400
for n, t, s in rows:
    y1 = y + 185
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 110, (y + y1) / 2), 90, GOLD, maxw=150, min_size=60)
    x0 = HM + 250
    left(d, t, (x0, y + 60), 44, WHITE, bold=True, min_size=32)
    left(d, s, (x0, y + 128), 30, LIGHT, min_size=24)
    y = y1 + 24
center(d, "数据不会骗人 · 提前看，提前懂", (W / 2, 1330), 38, GOLD, min_size=30)
footer(d)
check("正文图5")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-小红书-正文图5-现在4件事-1080x1440.png")
print("done")
