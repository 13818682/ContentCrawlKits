# -*- coding: utf-8 -*-
"""S1-5 今日头条配图 6张（1200×900）：封面1主标题/封面2录取率73%/封面3D类23%/微头条配图52vs73/正文图2录取率对比/正文图3三个世界"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1200, 900
TOP = (20, 59, 115); BOT = (11, 37, 69)
WHITE = (255, 255, 255); GOLD = (242, 184, 75)
LIGHT = (170, 196, 224); SUB = (150, 172, 200)
CARD = (26, 62, 116); EDGE = (66, 108, 164)
TEAL = (53, 184, 163); ORANGE = (240, 120, 72)

def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

def new_canvas():
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)

def put(d, checks, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
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

def badge(d, txt, y=66, size=26, color=GOLD):
    f = font(size, True)
    bb = d.textbbox((0, 0), txt, font=f)
    pad = 26; x0 = (W - (bb[2] - bb[0] + pad * 2)) / 2; x1 = x0 + (bb[2] - bb[0]) + pad * 2
    y1 = y + (bb[3] - bb[0]) + pad * 1.5
    d.rounded_rectangle([x0, y, x1, y1], radius=30, outline=color, width=2)
    d.text(((x0 + x1) / 2, (y + y1) / 2), txt, font=f, fill=color, anchor="mm")

def verify(d, checks, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy})")
    print(f"{name}: {len(checks)}处文字, {bad}处越界")

def source_line(d, checks, txt="数据来源：深圳市教育局公开信息 · 逐条人工核对"):
    put(d, checks, txt, font(22), (W / 2, H - 42), color=SUB, maxw=1080)

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-5-录取率解读/02-今日头条/"
P = "08-S1-5-公办普高52%录取率意味着什么？2027届家长该知道的3个真相-今日头条"

# 封面1 主标题
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 2027届备考")
put(d, checks, "52%≠一半人没书读", font(76, True), (W / 2, 340), color=WHITE, maxw=1060)
put(d, checks, "全市普高（含民办）录取率超73% · 3个真相", font(32), (W / 2, 460), color=GOLD, maxw=1060)
box(d, 230, 560, 740, 96, r=48)
put(d, checks, "稳定低位 · 不是悬崖 · D类另有真相", font(28, True), (W / 2, 608), color=WHITE, maxw=700)
source_line(d, checks)
verify(d, checks, "封面1-主标题")
img.save(BASE + P + "-封面1-主标题-1200x900.png")

# 封面2 录取率73%
img, d = new_canvas(); checks = []
badge(d, "2027届深圳中考 · 关键数据")
put(d, checks, "73%", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "全市普高（含民办）录取率", font(44, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "公办约52% + 民办33,195人 · 别再只看一半", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面2-录取率73%")
img.save(BASE + P + "-封面2-录取率73%-1200x900.png")

# 封面3 D类23%
img, d = new_canvas(); checks = []
badge(d, "D类家长 · 面对另一个比例")
put(d, checks, "23%", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "公办指标中D类占比", font(44, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "18,506人 · 指标生已全覆盖 · 路窄不是死胡同", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面3-D类23%")
img.save(BASE + P + "-封面3-D类23%-1200x900.png")

# 微头条配图 52 vs 73
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 录取率别再只看一半")
put(d, checks, "52% vs 73%", font(68, True), (W / 2, 230), color=WHITE, maxw=1000)
cw, ch, gap = 380, 330, 60
x0 = (W - (cw * 2 + gap)) // 2
y0 = 330
for i, (num, lab, note, col) in enumerate([("52%", "公办普高录取率", "约一半上公办", GOLD), ("73%", "全市普高（含民办）", "超七成能上普高", TEAL)]):
    x = x0 + i * (cw + gap)
    box(d, x, y0, cw, ch, r=20)
    d.rectangle([x, y0, x + 6, y0 + ch], fill=col)
    put(d, checks, num, font(90, True), (x + cw // 2, y0 + 96), color=col, maxw=cw - 30)
    put(d, checks, lab, font(30, True), (x + cw // 2, y0 + 220), color=WHITE, maxw=cw - 30)
    put(d, checks, note, font(24), (x + cw // 2, y0 + 278), color=SUB, maxw=cw - 36)
put(d, checks, "加上中职，总学位146,752覆盖全部考生", font(30, True), (W / 2, y0 + ch + 60), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "微头条配图-52vs73")
img.save(BASE + P + "-微头条配图-52vs73-1200x900.png")

# 正文图2 录取率对比
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 录取率走势")
put(d, checks, "稳定低位 · 不是悬崖", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
years = [("2020", "约44%", "近年最低"), ("2022", "约53%", ""), ("2024", "约52%", ""), ("2025", "约52%", ""), ("2026", "约52%", "预计")]
ry = 270
for yr, num, note in years:
    box(d, 120, ry, W - 240, 72, r=14)
    put(d, checks, yr, font(28, True), (190, ry + 36), anchor="lm", color=WHITE, maxw=120)
    put(d, checks, num, font(36, True), (620, ry + 36), anchor="lm", color=GOLD, maxw=180)
    put(d, checks, note, font(24), (760, ry + 36), anchor="lm", color=SUB, maxw=340)
    ry += 72 + 12
put(d, checks, "2020低点后是「十四五」11.8万+「十五五」10万学位托住的 · 是规划不是运气", font(26, True), (W / 2, 760), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "正文图2-录取率对比")
img.save(BASE + P + "-正文图2-录取率对比-1200x900.png")

# 正文图3 三个世界
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 一个52%三个世界")
put(d, checks, "同一个数字，三种家长", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("AC类高分段", "稳定赛道", "精确择校 · 用好指标生 · 分数价值最大化"),
    ("D类中分段", "提前布局", "公办D类仅约23% · Plan B是必备不是可选"),
    ("低分段", "被低估的路", "中本贯通 · 3+2 · 优质民办是正经出路"),
]
ry = 260
for tag, a, b in rows:
    box(d, 90, ry, W - 180, 120, r=16)
    d.rectangle([90, ry, 100, ry + 120], fill=GOLD)
    put(d, checks, tag, font(34, True), (140, ry + 38), anchor="lm", color=GOLD, maxw=300)
    put(d, checks, a, font(30, True), (470, ry + 38), anchor="lm", color=WHITE, maxw=420)
    put(d, checks, b, font(24), (470, ry + 82), anchor="lm", color=SUB, maxw=620)
    ry += 120 + 16
put(d, checks, "数据不可怕 · 可怕的是只看到数据的一半", font(30, True), (W / 2, 826), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "正文图3-三个世界")
img.save(BASE + P + "-正文图3-三个世界-1200x900.png")

print("S1-5 今日头条 6张 全部完成")
