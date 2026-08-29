# -*- coding: utf-8 -*-
"""S1-1 知乎配图生成：回答配图（1600×900 数据信息图）+ 想法配图（1080×1080 数据卡）
风格同 S1-1 长图：深蓝渐变 + 金竖条/金数字 + 三组数字卡，PIL 直出。
v2：正文（标签/说明/来源）整体放大一档，卡片加高重排。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

def font(size, bold=False):
    if size <= 17:                       # 正文文字统一放大1.35倍，展示大字不受影响
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

def new_canvas(w, h):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(w, axis=1).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)

def put(d, checks, W, H, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:                                   # 越界自适应：超出maxw/画布则缩小字号
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

def verify(checks, W, H, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy}) 边({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
    print(f"{name}: 共{len(checks)}处文字，{bad}处越界")

# =====================================================================
# 一、知乎回答配图：数据信息图（三组数字）1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []

# 金竖条标题区
d.rectangle([120, 88, 130, 184], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 2027届家长现在该做什么？", font(28, True), (166, 86), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "先记住三组数字", font(78, True), (166, 148), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "深圳中考 · 2026年数据刚收官 · 数据均来自官方文件，逐条人工核验", font(34), (166, 222), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 264, 240, 264], fill=GOLD, width=4)

# 三组数字卡（正文放大版）
box_data = [
    ("16-18万", "2027年预计考生人数", "2026年为15.30万"),
    ("约8万", "公办普高招生人数", "101所学校"),
    ("约52%", "公办普高录取率", "含民办超73%"),
]
card_w, card_h = 420, 390
gap = 60
x0 = (W - (card_w * 3 + gap * 2)) // 2
y0 = 318
for i, (num, lab, note) in enumerate(box_data):
    x = x0 + i * (card_w + gap)
    box(d, x, y0, card_w, card_h, r=20)
    d.rectangle([x, y0, x + 8, y0 + card_h], fill=GOLD)
    put(d, checks, W, H, num, font(84, True), (x + card_w // 2, y0 + 98), color=GOLD, maxw=card_w - 40)
    put(d, checks, W, H, lab, font(40, True), (x + card_w // 2, y0 + 204), color=WHITE, maxw=card_w - 40)
    put(d, checks, W, H, note, font(32), (x + card_w // 2, y0 + 294), color=SUB, maxw=card_w - 60)

# 底部金句 + 来源
put(d, checks, W, H, "记住这3个数字，再看任何中考信息，你都知道它在坐标系上的位置", font(38, True), (W // 2, y0 + card_h + 52), color=GOLD, maxw=1400)
put(d, checks, W, H, "数据来源：深圳市教育局深教〔2026〕34号通知及2026年招生计划通知（官方文件，逐条人工核对）", font(26), (W // 2, y0 + card_h + 106), color=SUB, maxw=1400)

verify(checks, W, H, "知乎回答配图")
out1 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-1-启点-现在做什么/05.知乎/03-S1-1-2026年深圳中考已结束，2027届家长现在该做什么？-知乎-回答配图-三组数字-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：数据卡（三组数字）1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "2027届家长 · 先记住三组数字", font(44, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "深圳中考 · 2026数据刚收官", font(30), (128, 162), anchor="lm", color=LIGHT, maxw=900)

rows = [
    ("16-18万", "2027年预计考生人数", "2026年15.30万"),
    ("约8万", "公办普高招生人数", "101所学校"),
    ("约52%", "公办普高录取率", "含民办超73%"),
]
row_y = 212
row_h = 200
for i, (num, lab, note) in enumerate(rows):
    y = row_y + i * (row_h + 24)
    box(d2, 76, y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, num, font(66, True), (168, y + row_h // 2), anchor="lm", color=GOLD, maxw=380)
    put(d2, checks2, W2, H2, lab, font(38, True), (640, y + 62), anchor="lm", color=WHITE, maxw=360)
    put(d2, checks2, W2, H2, note, font(30), (640, y + 132), anchor="lm", color=SUB, maxw=360)

base = row_y + 3 * (row_h + 24) - 24
put(d2, checks2, W2, H2, "深圳中考先填志愿、后考试 · 明年5月填报窗口只有10天", font(34, True), (W2 // 2, base + 52), color=GOLD, maxw=940)
put(d2, checks2, W2, H2, "现在开始，你比明年才动手的家长多9个月信息优势", font(30), (W2 // 2, base + 104), color=WHITE, maxw=940)
put(d2, checks2, W2, H2, "数据来源：深圳市教育局官方文件，逐条人工核对", font(26), (W2 // 2, base + 156), color=SUB, maxw=940)

verify(checks2, W2, H2, "知乎想法配图")
out2 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-1-启点-现在做什么/05.知乎/04-S1-1-2026年深圳中考已结束，2027届家长现在该做什么？-知乎-想法配图-三组数字-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print("全部完成")
