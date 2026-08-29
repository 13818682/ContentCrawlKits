# -*- coding: utf-8 -*-
"""S1-4 知乎配图：回答配图（1600×900 翻倍时间线）+ 想法配图（1080×1080 翻倍数据卡）"""
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
# 一、知乎回答配图：翻倍时间线 1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []
d.rectangle([120, 84, 130, 180], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 深圳中考8年翻倍", font(28, True), (166, 82), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "考生翻倍 · 学位在追", font(64, True), (166, 144), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "2018→2027 · 数据来自深圳市招考办与官方推估", font(30), (166, 212), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 246, 240, 246], fill=GOLD, width=4)

nodes = [("2018", "7.21万", "增长起点"), ("2022", "11.2万", "突破11万"), ("2026", "15.30万", "约8万学位"), ("2027", "16-18万", "预测·待确认")]
nx = 250; step = 370; line_y = 520
d.line([nx - 60, line_y, nx + step * 3 + 40, line_y], fill=EDGE, width=5)
for i, (yr, num, note) in enumerate(nodes):
    x = nx + i * step
    hi = (i == len(nodes) - 1)
    d.ellipse([x - 18, line_y - 18, x + 18, line_y + 18], fill=GOLD if hi else EDGE, outline=GOLD if hi else EDGE, width=3)
    put(d, checks, W, H, yr, font(30, True), (x, line_y - 100), color=WHITE, maxw=320)
    put(d, checks, W, H, num, font(46, True), (x, line_y + 78), color=GOLD if hi else WHITE, maxw=320)
    put(d, checks, W, H, note, font(24), (x, line_y + 138), color=SUB, maxw=320)

put(d, checks, W, H, "公办学位 5.9万→约8万（+35%）· 录取率从44%回稳到52%", font(30, True), (W // 2, 746), color=GOLD, maxw=1400)
put(d, checks, W, H, "压力在高位 · 方向在好转 · 2027-2030见顶", font(28, True), (W // 2, 810), color=WHITE, maxw=1400)
put(d, checks, W, H, "来源：深圳市招考办公布历年数据 · 逐条人工核对", font(22), (W // 2, 864), color=SUB, maxw=1400)

verify(d, checks, W, H, "知乎回答配图")
out1 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-4-考生人数翻倍/05.知乎/03-S1-4-深圳中考8年考生人数翻倍：2027年你的孩子和多少人竞争？-知乎-回答配图-翻倍时间线-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：翻倍数据卡 1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "深圳中考 · 8年翻倍", font(40, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "看懂增长逻辑，就不慌", font(26), (128, 162), anchor="lm", color=LIGHT, maxw=900)

rows = [
    ("16-18万", "2027年预计考生人数", "2018年7.21万 · 8年翻倍"),
    ("约8万", "公办普高学位", "5.9万→8万 · 增长35%"),
    ("2027-30", "考生见顶窗口", "出生人口已过峰 · 学位覆盖峰值"),
]
row_y = 220
row_h, gap = 190, 24
for num, lab, note in rows:
    box(d2, 76, row_y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, num, font(58, True), (166, row_y + row_h // 2), anchor="lm", color=GOLD, maxw=400)
    put(d2, checks2, W2, H2, lab, font(34, True), (620, row_y + 62), anchor="lm", color=WHITE, maxw=360)
    put(d2, checks2, W2, H2, note, font(28), (620, row_y + 128), anchor="lm", color=SUB, maxw=360)
    row_y += row_h + gap

base = row_y - gap
put(d2, checks2, W2, H2, "压力在高位 · 方向在好转", font(30, True), (W2 // 2, base + 58), color=GOLD, maxw=920)
put(d2, checks2, W2, H2, "来源：深圳市招考办公布历年数据 · 逐条人工核对", font(22), (W2 // 2, base + 112), color=SUB, maxw=920)

verify(d2, checks2, W2, H2, "知乎想法配图")
out2 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-4-考生人数翻倍/05.知乎/04-S1-4-深圳中考8年考生人数翻倍：2027年你的孩子和多少人竞争？-知乎-想法配图-翻倍数据-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print("全部完成")
