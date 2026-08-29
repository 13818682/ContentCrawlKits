# -*- coding: utf-8 -*-
"""S1-7 知乎配图：回答配图（1600×900 5阶段时间线）+ 想法配图（1080×1080 时间窗口数据卡）"""
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
# 一、知乎回答配图：5阶段时间线 1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []
d.rectangle([120, 84, 130, 180], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 2027深圳中考备考", font(28, True), (166, 82), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "9个月备考时间线", font(64, True), (166, 144), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "5个阶段 · 孩子与家长每月做什么 · 志愿只有10天", font(30), (166, 212), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 246, 240, 246], fill=GOLD, width=4)

rows = [
    ("8-9月", "建立认知框架", "三组数字 · AC/D/C类 · 指标生 · 体育14分累积"),
    ("10-12月", "信息收集期", "指标生名额 · 目标学校 · 11月期中考定位"),
    ("1-3月", "定位校准期", "一模定位 · 政策发布 · 3月下旬中考报名"),
    ("4-5月", "决策冲刺期", "二模 · 体育中考 · 草拟冲稳保 · 志愿填报10天"),
    ("6-8月", "考试录取", "中考 → 出分 → 录取 → 高一衔接"),
]
ry = 296
row_h = 80
for t, tag, b in rows:
    box(d, 110, ry, W - 220, row_h, r=14)
    put(d, checks, W, H, t, font(28, True), (150, ry + 28), anchor="lm", color=GOLD, maxw=200)
    put(d, checks, W, H, tag, font(30, True), (370, ry + 28), anchor="lm", color=WHITE, maxw=260)
    put(d, checks, W, H, b, font(25), (370, ry + 62), anchor="lm", color=SUB, maxw=1080)
    ry += row_h + 12

put(d, checks, W, H, "现在开始，你有9个月；明年才开始，只有10天", font(30, True), (W // 2, ry + 18), color=GOLD, maxw=1400)
put(d, checks, W, H, "志愿填报2026年为5月23日-6月1日 · 确认后不可更改", font(26, True), (W // 2, ry + 66), color=WHITE, maxw=1400)
put(d, checks, W, H, "来源：深教〔2026〕34号及深圳市教育局公开信息 · 逐条人工核对", font(22), (W // 2, ry + 118), color=SUB, maxw=1400)

verify(d, checks, W, H, "知乎回答配图")
out1 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/05.知乎/03-S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-知乎-回答配图-5阶段时间线-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：时间窗口数据卡 1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "2027深圳中考 · 时间窗口", font(40, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "准备时间，只剩这些了", font(26), (128, 162), anchor="lm", color=LIGHT, maxw=900)

rows = [
    ("300天", "到2027年6月中考", "现在开始 · 来得及"),
    ("9个月", "从现在到5月填志愿", "每天15分钟 · 建立信息优势"),
    ("10天", "志愿填报窗口", "5月下旬 · 确认后不可更改"),
]
row_y = 220
row_h, gap = 190, 24
for num, lab, note in rows:
    box(d2, 76, row_y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, num, font(58, True), (170, row_y + row_h // 2), anchor="lm", color=GOLD, maxw=380)
    put(d2, checks2, W2, H2, lab, font(34, True), (630, row_y + 62), anchor="lm", color=WHITE, maxw=350)
    put(d2, checks2, W2, H2, note, font(28), (630, row_y + 128), anchor="lm", color=SUB, maxw=350)
    row_y += row_h + gap

base = row_y - gap
put(d2, checks2, W2, H2, "现在开始，你有9个月；明年才开始，只有10天", font(28, True), (W2 // 2, base + 56), color=GOLD, maxw=920)
put(d2, checks2, W2, H2, "来源：深教〔2026〕34号 · 逐条人工核对", font(22), (W2 // 2, base + 108), color=SUB, maxw=920)

verify(d2, checks2, W2, H2, "知乎想法配图")
out2 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/05.知乎/04-S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-知乎-想法配图-时间线-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print("全部完成")
