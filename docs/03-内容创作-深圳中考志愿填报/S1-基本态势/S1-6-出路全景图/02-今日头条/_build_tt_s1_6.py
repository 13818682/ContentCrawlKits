# -*- coding: utf-8 -*-
"""S1-6 今日头条配图 6张（1200×900）：封面1主标题/封面2总学位/封面3中职3+4/微头条配图4层全景/正文图2中职两条路/正文图3按分选路"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1200, 900
TOP = (20, 59, 115); BOT = (11, 37, 69)
WHITE = (255, 255, 255); GOLD = (242, 184, 75)
LIGHT = (170, 196, 224); SUB = (150, 172, 200)
CARD = (26, 62, 116); EDGE = (66, 108, 164)
TEAL = (53, 184, 163)

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

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-6-出路全景图/02-今日头条/"
P = "08-S1-6-一张图看懂深圳中考全部出路-今日头条"

# 封面1 主标题
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 2027届备考")
put(d, checks, "4层出路，一次看全", font(76, True), (W / 2, 340), color=WHITE, maxw=1060)
put(d, checks, "146,752个学位 · 180所学校 · 覆盖全部考生", font(32), (W / 2, 460), color=GOLD, maxw=1060)
box(d, 230, 560, 740, 96, r=48)
put(d, checks, "公办52% · 普高73% · 中职3+4可读本科", font(28, True), (W / 2, 608), color=WHITE, maxw=700)
source_line(d, checks)
verify(d, checks, "封面1-主标题")
img.save(BASE + P + "-封面1-主标题-1200x900.png")

# 封面2 总学位
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 全部出路")
put(d, checks, "146,752", font(130, True), (W / 2, 350), color=GOLD, maxw=980)
put(d, checks, "高中阶段总学位 · 180所学校", font(44, True), (W / 2, 540), color=WHITE, maxw=1060)
put(d, checks, "公办+民办+中职 · 覆盖全部15.3万考生", font(30), (W / 2, 640), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面2-总学位")
img.save(BASE + P + "-封面2-总学位-1200x900.png")

# 封面3 中职3+4
img, d = new_canvas(); checks = []
badge(d, "被低估的路 · 中职3+4")
put(d, checks, "300", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "中本贯通名额", font(44, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "中职3年→本科4年 · 全日制本科文凭 · 一职对口深技大", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面3-中职3+4")
img.save(BASE + P + "-封面3-中职3+4-1200x900.png")

# 微头条配图 4层全景
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 4层出路")
put(d, checks, "4层出路 · 146,752个学位", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("公办普高", "约8万 · 101所", "约52% · AC 61,797 · D 18,506"),
    ("民办普高", "33,195 · 49所", "AC/D同分录取 · 学费3万-15万/年"),
    ("中职及技工", "33,254 · 30所", "3+4中本贯通300 · 3+2中高贯通2,853"),
    ("合计", "146,752 · 180所", "覆盖全部考生"),
]
ry = 260
for tag, a, b in rows:
    box(d, 90, ry, W - 180, 104, r=16)
    d.rectangle([90, ry, 100, ry + 104], fill=GOLD)
    put(d, checks, tag, font(32, True), (140, ry + 32), anchor="lm", color=GOLD, maxw=240)
    put(d, checks, a, font(28, True), (420, ry + 32), anchor="lm", color=WHITE, maxw=400)
    put(d, checks, b, font(22), (420, ry + 74), anchor="lm", color=SUB, maxw=620)
    ry += 104 + 12
put(d, checks, "全市普高（含民办）录取率超73%", font(28, True), (W / 2, ry + 28), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "微头条配图-4层全景")
img.save(BASE + P + "-微头条配图-4层全景-1200x900.png")

# 正文图2 中职两条路
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 中职不是没出路")
put(d, checks, "中职 · 曲线读大学", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
cw, ch, gap = 480, 380, 60
x0 = (W - (cw * 2 + gap)) // 2
y0 = 300
for i, (num, lab, note, note2, col) in enumerate([
    ("3+4", "中本贯通 · 300名额", "中职3年 → 本科4年", "全日制本科文凭 · 一职对口深技大", GOLD),
    ("3+2", "中高贯通 · 2,853人", "中职3年 → 高职2年", "63个专业 · 公办41+民办22", TEAL)]):
    x = x0 + i * (cw + gap)
    box(d, x, y0, cw, ch, r=20)
    d.rectangle([x, y0, x + 6, y0 + ch], fill=col)
    put(d, checks, num, font(90, True), (x + cw // 2, y0 + 92), color=col, maxw=cw - 30)
    put(d, checks, lab, font(30, True), (x + cw // 2, y0 + 214), color=WHITE, maxw=cw - 30)
    put(d, checks, note, font(26), (x + cw // 2, y0 + 272), color=LIGHT, maxw=cw - 36)
    put(d, checks, note2, font(22), (x + cw // 2, y0 + 322), color=SUB, maxw=cw - 40)
put(d, checks, "中职→大学这条路 · 知道的人还不多", font(30, True), (W / 2, y0 + ch + 58), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "正文图2-中职两条路")
img.save(BASE + P + "-正文图2-中职两条路-1200x900.png")

# 正文图3 按分选路
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 按分数怎么选")
put(d, checks, "行动建议 · 对号入座", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("公办线以上", "主攻公办 · 民办作保底不要忽略"),
    ("公办线边缘", "公办+民办+中本贯通 · 三条腿走路"),
    ("D类考生", "民办和中职路径 · 需要更早了解"),
    ("无论分数", "收藏这张图 · 填志愿前再看一遍"),
]
ry = 260
for tag, a in rows:
    box(d, 90, ry, W - 180, 100, r=16)
    d.rectangle([90, ry, 100, ry + 100], fill=GOLD)
    put(d, checks, tag, font(32, True), (150, ry + 50), anchor="lm", color=GOLD, maxw=300)
    put(d, checks, a, font(28, True), (500, ry + 50), anchor="lm", color=WHITE, maxw=560)
    ry += 100 + 14
put(d, checks, "别让孩子只有一条路", font(30, True), (W / 2, ry + 30), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "正文图3-按分选路")
img.save(BASE + P + "-正文图3-按分选路-1200x900.png")

print("S1-6 今日头条 6张 全部完成")
