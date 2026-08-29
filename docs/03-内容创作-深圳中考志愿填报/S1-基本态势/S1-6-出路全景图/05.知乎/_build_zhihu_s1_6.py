# -*- coding: utf-8 -*-
"""S1-6 知乎配图：回答配图（1600×900 4层出路）+ 想法配图（1080×1080 4层出路数据卡）"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

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

# =====================================================================
# 一、知乎回答配图：4层出路 1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []
d.rectangle([120, 84, 130, 180], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 深圳中考出路全景", font(28, True), (166, 82), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "4层出路 · 146,752个学位", font(64, True), (166, 144), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "2026年招生计划数据 · 覆盖全部考生", font(30), (166, 212), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 246, 240, 246], fill=GOLD, width=4)

cards = [
    ("公办普高", "约8万 · 101所", "约52% · D类占比约23%"),
    ("民办普高", "33,195 · 49所", "AC/D同分录取"),
    ("中职技工", "33,254 · 30所", "3+4中本贯通300 · 3+2共2,853"),
]
cw, ch, gap = 430, 340, 50
x0 = (W - (cw * 3 + gap * 2)) // 2
y0 = 296
for i, (tag, a, b) in enumerate(cards):
    x = x0 + i * (cw + gap)
    box(d, x, y0, cw, ch, r=20)
    d.rectangle([x, y0, x + 8, y0 + ch], fill=GOLD)
    put(d, checks, W, H, tag, font(40, True), (x + cw // 2, y0 + 86), color=GOLD, maxw=cw - 40)
    put(d, checks, W, H, a, font(36, True), (x + cw // 2, y0 + 186), color=WHITE, maxw=cw - 40)
    put(d, checks, W, H, b, font(27), (x + cw // 2, y0 + 268), color=SUB, maxw=cw - 52)

box(d, 120, y0 + ch + 36, W - 240, 70, r=16)
put(d, checks, W, H, "合计 146,752 学位 · 180 所学校 · 覆盖全部考生", font(32, True), (W // 2, y0 + ch + 71), color=GOLD, maxw=1300)
put(d, checks, W, H, "全市普高（含民办）录取率超73% · 中职3+4可读全日制本科", font(28, True), (W // 2, y0 + ch + 150), color=WHITE, maxw=1400)
put(d, checks, W, H, "来源：深圳市教育局2026年招生计划通知 · 逐条人工核对", font(22), (W // 2, y0 + ch + 206), color=SUB, maxw=1400)

verify(d, checks, W, H, "知乎回答配图")
out1 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-6-出路全景图/05.知乎/03-S1-6-一张图看懂深圳中考全部出路-知乎-回答配图-4层出路-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：4层出路数据卡 1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "深圳中考 · 不止公办一条路", font(40, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "4层出路 · 146,752个学位", font(26), (128, 162), anchor="lm", color=LIGHT, maxw=900)

rows = [
    ("约8万", "公办普高 · 101所", "约52% · D类占比约23%"),
    ("33,195", "民办普高 · 49所", "AC/D同分录取"),
    ("33,254", "中职技工 · 30所", "3+4中本贯通300 · 3+2共2,853"),
    ("146,752", "高中阶段总学位", "180所 · 覆盖全部考生"),
]
row_y = 210
row_h, gap = 172, 18
for num, lab, note in rows:
    box(d2, 76, row_y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, num, font(52, True), (176, row_y + row_h // 2), anchor="lm", color=GOLD, maxw=400)
    put(d2, checks2, W2, H2, lab, font(32, True), (630, row_y + 56), anchor="lm", color=WHITE, maxw=350)
    put(d2, checks2, W2, H2, note, font(26), (630, row_y + 120), anchor="lm", color=SUB, maxw=350)
    row_y += row_h + gap

base = row_y - gap
put(d2, checks2, W2, H2, "别让孩子只有一条路", font(30, True), (W2 // 2, base + 50), color=GOLD, maxw=920)
put(d2, checks2, W2, H2, "来源：深圳市教育局招生计划通知 · 逐条人工核对", font(22), (W2 // 2, base + 102), color=SUB, maxw=920)

verify(d2, checks2, W2, H2, "知乎想法配图")
out2 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-6-出路全景图/05.知乎/04-S1-6-一张图看懂深圳中考全部出路-知乎-想法配图-4层出路-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print("全部完成")
