# -*- coding: utf-8 -*-
"""QA-003 知乎配图：回答配图（1600×900 排名区间表）+ 想法配图（1080×1080 三数字卡）
配色/排版/verify 复用 S1-7 知乎脚本。数据：2026 第一批 AC 住宿线 555±4 分档。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
NAVY = (18, 30, 55)

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/003+中考滑档去了深圳排名40左右的高中怎么办？/05.知乎/"
N = "QA-003-中考滑档去了深圳排名40左右的高中怎么办"


def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def new_canvas(w, h):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(w, axis=1).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


def put(d, checks, W, H, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 8:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    checks.append((text, fnt, xy, anchor))


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)


def verify(d, checks, W, H, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy})")
    print(f"{name}: 共{len(checks)}处文字，{bad}处越界")
    return bad == 0


# =====================================================================
# 一、知乎回答配图：排名区间表 1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []
d.rectangle([120, 84, 130, 180], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 深圳中考滑档", font(28, True), (166, 82), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "排名40的高中，到底算什么水平？", font(62, True), (166, 148), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "按2026第一批录取线（AC类住宿）排序 · 深圳无官方排名", font(30), (166, 216), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 248, 240, 248], fill=GOLD, width=4)

rows = [
    ("第35-38名", "东师大附中深圳 / 深理工附中 / 龙岗区实验 / 红山中学", "559分"),
    ("第39名", "罗湖外语学校", "558分"),
    ("第40名", "深圳市高级中学创新高中", "557分"),
    ("第41名", "松岗中学", "557分"),
    ("第42-45名", "福田中学 / 深大附中盐田 / 宝安第一外国语 / 格致中学", "553-554分"),
]
ry = 296
row_h = 78
for t, name, sc in rows:
    box(d, 110, ry, W - 220, row_h, r=14)
    put(d, checks, W, H, t, font(28, True), (150, ry + row_h // 2), anchor="lm", color=GOLD, maxw=200)
    put(d, checks, W, H, name, font(27), (410, ry + row_h // 2), anchor="lm", color=WHITE, maxw=820)
    put(d, checks, W, H, sc, font(28, True), (1340, ry + row_h // 2), anchor="rm", color=GOLD, maxw=None)
    ry += row_h + 12

put(d, checks, W, H, "所谓排名40，不过是一两分的差距、一个志愿梯度的落差", font(30, True), (W // 2, ry + 10), color=GOLD, maxw=1400)
put(d, checks, W, H, "孩子负责学习好，家长负责决策优 —— 滑档≠人生完蛋", font(28, True), (W // 2, ry + 62), color=WHITE, maxw=1400)
put(d, checks, W, H, "来源：深圳市2026年高中阶段学校第一批录取标准 · 逐条人工核对", font(22), (W // 2, ry + 114), color=SUB, maxw=1400)

ok1 = verify(d, checks, W, H, "知乎回答配图")
out1 = BASE + f"03-{N}-知乎-回答配图-排名区间-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：三数字卡 1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "深圳中考 · 滑档真相", font(40, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "排名40，到底是什么水平", font(26), (128, 162), anchor="lm", color=LIGHT, maxw=900)

rows = [
    ("557分", "第40名高中录取线", "深高创新 / 松岗 · 公办普高"),
    ("553-561分", "第35-45名区间", "一两分，就是一个名次"),
    ("555±4分", "排名40左右的分数带", "不是没学上，是没填好"),
]
row_y = 220
row_h, gap = 190, 24
for num, lab, note in rows:
    box(d2, 76, row_y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, num, font(56, True), (170, row_y + row_h // 2), anchor="lm", color=GOLD, maxw=380)
    put(d2, checks2, W2, H2, lab, font(33, True), (620, row_y + 62), anchor="lm", color=WHITE, maxw=360)
    put(d2, checks2, W2, H2, note, font(27), (620, row_y + 128), anchor="lm", color=SUB, maxw=360)
    row_y += row_h + gap

base = row_y - gap
put(d2, checks2, W2, H2, "孩子负责学习好，家长负责决策优", font(28, True), (W2 // 2, base + 56), color=GOLD, maxw=920)
put(d2, checks2, W2, H2, "来源：2026第一批录取标准 · 逐条人工核对", font(22), (W2 // 2, base + 108), color=SUB, maxw=920)

ok2 = verify(d2, checks2, W2, H2, "知乎想法配图")
out2 = BASE + f"04-{N}-知乎-想法配图-排名分数带-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print()
print("全部 OK =", ok1 and ok2)
