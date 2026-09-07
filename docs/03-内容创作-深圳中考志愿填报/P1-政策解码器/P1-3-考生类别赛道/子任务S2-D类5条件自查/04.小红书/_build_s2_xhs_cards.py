# -*- coding: utf-8 -*-
"""P1-3 S2 小红书正文图卡 ×3（1080×1440，封面已有精炼版）
正文图1-5个条件清单 / 正文图2-现在先查3项 / 正文图3-条件不全→民办/中职。
口径：D类5条件官方版（居住证/社保养老+医疗·一个险种满3年·补缴不计/3年学籍）。
模板：主线完整版 _build_mainline_xhs_cards.py（同视觉）。
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


def footer(d):
    center(d, "数据来源：深圳市教育局公开文件 · 人工核对（2026参考）", (W / 2, 1390), 22, SUB, bold=False, min_size=17)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 8:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ========== 正文图1：5个条件清单 ==========
im, d = base()
center(d, "D类 · 5个报名条件", (W / 2, 90), 36, GOLD, min_size=28)
center(d, "缺一不可 · 现在自查", (W / 2, 270), 60, WHITE, min_size=46)
center(d, "官方口径 · 非深户报考公办", (W / 2, 380), 34, LIGHT, bold=False, min_size=26)
rows = [
    ("1", "合法稳定职业", "父母一方在深就业证明"),
    ("2", "合法稳定住所", "租房要租赁凭证"),
    ("3", "持深圳有效居住证", "别过期，及时续签"),
    ("4", "社保 养老+医疗", "两险都缴 · 一个险种满3年 · 补缴不计"),
    ("5", "3年完整初中学籍", "在深读完3年初中"),
]
y = 440
for n, t, s in rows:
    y1 = y + 150
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 95, (y + y1) / 2), 66, GOLD, maxw=120, min_size=46)
    x0 = HM + 200
    left(d, t, (x0, y + 46), 40, WHITE, bold=True, min_size=30)
    left(d, s, (x0, y + 105), 28, LIGHT, min_size=22)
    y = y1 + 18
center(d, "社保 · 是 5 项里最容易翻车的一项", (W / 2, 1330), 34, GOLD, min_size=27)
footer(d)
check("正文图1")
im.save(HERE + "P1-3-S2-D类5条件自查-小红书-正文图1-5个条件-1080x1440.png")

# ========== 正文图2：现在先查3项 ==========
im, d = base()
center(d, "现在 · 先查这 3 项", (W / 2, 90), 36, GOLD, min_size=28)
center(d, "这三样要提前办 · 花时间", (W / 2, 260), 54, WHITE, min_size=40)
center(d, "别等 3 月报名才手忙脚乱", (W / 2, 370), 34, LIGHT, bold=False, min_size=26)
rows = [
    ("①", "社保满没满3年", "拉社保记录数一数 · 断缴要留意（补缴不计）", GOLD),
    ("②", "居住证过期没", "有效期一看便知 · 过期赶紧续签", WHITE),
    ("③", "租赁凭证办没办", "租房要租赁凭证 · 不是普通合同", WHITE),
]
y = 430
for n, t, s, col in rows:
    y1 = y + 260
    rcard(d, HM, y, W - HM, y1)
    center(d, n, (HM + 120, (y + y1) / 2), 90, GOLD, maxw=150, min_size=64)
    x0 = HM + 260
    left(d, t, (x0, y + 75), 46, col, bold=True, min_size=34)
    left(d, s, (x0, y + 160), 30, LIGHT, min_size=24)
    y = y1 + 26
center(d, "查一遍 · 心里就有底了", (W / 2, 1330), 40, GOLD, min_size=32)
footer(d)
check("正文图2")
im.save(HERE + "P1-3-S2-D类5条件自查-小红书-正文图2-先查3项-1080x1440.png")

# ========== 正文图3：条件不全 → 民办/中职 ==========
im, d = base()
center(d, "条件不全 · 也别慌", (W / 2, 90), 36, GOLD, min_size=28)
center(d, "不是没学上，是路不一样", (W / 2, 260), 52, WHITE, min_size=40)
center(d, "仍可参加中考 · 但范围受限", (W / 2, 380), 34, LIGHT, bold=False, min_size=26)
rows = [
    ("可以", "参加中考", "但不进公办划线录取"),
    ("只限", "民办普高补录", "公办线后补录窗口"),
    ("只限", "中职注册入学", "中职/技工直接注册"),
]
y = 440
for t, a, s in rows:
    y1 = y + 220
    rcard(d, HM, y, W - HM, y1)
    center(d, t, (HM + 120, (y + y1) / 2), 60, GOLD, maxw=200, min_size=44)
    x0 = HM + 280
    left(d, a, (x0, y + 70), 46, WHITE, bold=True, min_size=34)
    left(d, s, (x0, y + 145), 30, LIGHT, min_size=24)
    y = y1 + 24
center(d, "公办路窄 · 民办/中职也是正经路", (W / 2, 1330), 36, GOLD, min_size=29)
footer(d)
check("正文图3")
im.save(HERE + "P1-3-S2-D类5条件自查-小红书-正文图3-条件不全-1080x1440.png")
print("done")
