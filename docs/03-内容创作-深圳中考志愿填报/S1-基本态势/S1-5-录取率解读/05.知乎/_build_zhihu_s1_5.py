# -*- coding: utf-8 -*-
"""S1-5 知乎配图：回答配图（1600×900 录取率三层）+ 想法配图（1080×1080 录取率数据卡）"""
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
# 一、知乎回答配图：录取率三层 1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []
d.rectangle([120, 84, 130, 180], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 深圳中考录取率", font(28, True), (166, 82), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "录取率 · 三层真相", font(64, True), (166, 144), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "别再只看一个数字 · 2026年官方数据", font(30), (166, 212), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 246, 240, 246], fill=GOLD, width=4)

cards = [
    ("52%", "公办普高录取率", "约一半考生上公办"),
    ("73%", "全市普高（含民办）", "公办约8万+民办33,195"),
    ("146,752", "高中阶段总学位", "公办+民办+中职 · 覆盖全部考生"),
]
cw, ch, gap = 430, 360, 50
x0 = (W - (cw * 3 + gap * 2)) // 2
y0 = 296
for i, (num, lab, note) in enumerate(cards):
    x = x0 + i * (cw + gap)
    box(d, x, y0, cw, ch, r=20)
    d.rectangle([x, y0, x + 8, y0 + ch], fill=GOLD)
    put(d, checks, W, H, num, font(72, True), (x + cw // 2, y0 + 110), color=GOLD, maxw=cw - 30)
    put(d, checks, W, H, lab, font(36, True), (x + cw // 2, y0 + 230), color=WHITE, maxw=cw - 40)
    put(d, checks, W, H, note, font(28), (x + cw // 2, y0 + 300), color=SUB, maxw=cw - 48)

put(d, checks, W, H, "52%是稳定低位，不是下滑悬崖", font(30, True), (W // 2, y0 + ch + 60), color=GOLD, maxw=1400)
put(d, checks, W, H, "数据不可怕 · 可怕的是只看到数据的一半", font(28, True), (W // 2, y0 + ch + 122), color=WHITE, maxw=1400)
put(d, checks, W, H, "来源：深圳市教育局2026年招生计划通知 · 逐条人工核对", font(22), (W // 2, y0 + ch + 180), color=SUB, maxw=1400)

verify(d, checks, W, H, "知乎回答配图")
out1 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-5-录取率解读/05.知乎/03-S1-5-公办普高52%录取率意味着什么？2027届家长该知道的3个真相-知乎-回答配图-录取率三层-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：录取率数据卡 1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "深圳中考录取率 · 别再只看一个数", font(38, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "同一组数据 · 有人绝望 · 有人看见路", font(26), (128, 162), anchor="lm", color=LIGHT, maxw=900)

rows = [
    ("52%", "公办普高录取率", "约一半考生上公办"),
    ("73%", "全市普高（含民办）", "公办约8万 + 民办33,195"),
    ("146,752", "高中阶段总学位", "覆盖全部15.3万考生"),
]
row_y = 220
row_h, gap = 190, 24
for num, lab, note in rows:
    box(d2, 76, row_y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, num, font(60, True), (166, row_y + row_h // 2), anchor="lm", color=GOLD, maxw=430)
    put(d2, checks2, W2, H2, lab, font(34, True), (640, row_y + 62), anchor="lm", color=WHITE, maxw=340)
    put(d2, checks2, W2, H2, note, font(28), (640, row_y + 128), anchor="lm", color=SUB, maxw=340)
    row_y += row_h + gap

base = row_y - gap
put(d2, checks2, W2, H2, "52%是稳定低位 · 不是下滑悬崖", font(30, True), (W2 // 2, base + 58), color=GOLD, maxw=920)
put(d2, checks2, W2, H2, "来源：深圳市教育局招生计划通知 · 逐条人工核对", font(22), (W2 // 2, base + 112), color=SUB, maxw=920)

verify(d2, checks2, W2, H2, "知乎想法配图")
out2 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-5-录取率解读/05.知乎/04-S1-5-公办普高52%录取率意味着什么？2027届家长该知道的3个真相-知乎-想法配图-录取率数据-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print("全部完成")
