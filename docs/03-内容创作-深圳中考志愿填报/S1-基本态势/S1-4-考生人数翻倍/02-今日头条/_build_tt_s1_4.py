# -*- coding: utf-8 -*-
"""S1-4 今日头条配图 6张（1200×900）：封面1主标题/封面2翻倍/封面3见顶/微头条配图翻倍趋势/正文图2三引擎/正文图3见顶信号
设计语言按 13-2 模板：深蓝渐变、金 #F2B84B、顶部胶囊徽章、底部来源。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1200, 900
TOP = (20, 59, 115); BOT = (11, 37, 69)
WHITE = (255, 255, 255); GOLD = (242, 184, 75)
LIGHT = (170, 196, 224); SUB = (150, 172, 200)
CARD = (26, 62, 116); EDGE = (66, 108, 164)

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

def source_line(d, checks, txt="数据来源：深圳市招考办公布历年数据 · 逐条人工核对"):
    put(d, checks, txt, font(22), (W / 2, H - 42), color=SUB, maxw=1080)

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-4-考生人数翻倍/02-今日头条/"
P = "08-S1-4-深圳中考8年考生人数翻倍：2027年你的孩子和多少人竞争？-今日头条"

# 封面1 主标题
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 2027届备考")
put(d, checks, "8年考生翻了一倍", font(76, True), (W / 2, 340), color=WHITE, maxw=1060)
put(d, checks, "2027年16-18万考生 · 你家孩子和多少人竞争", font(32), (W / 2, 460), color=GOLD, maxw=1060)
box(d, 250, 560, 700, 96, r=48)
put(d, checks, "三个引擎 · 学位在追 · 2027-2030见顶", font(28, True), (W / 2, 608), color=WHITE, maxw=660)
source_line(d, checks)
verify(d, checks, "封面1-主标题")
img.save(BASE + P + "-封面1-主标题-1200x900.png")

# 封面2 翻倍
img, d = new_canvas(); checks = []
badge(d, "2027届深圳中考 · 关键数据")
put(d, checks, "2倍", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "2018年7.21万 → 2027年16-18万", font(42, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "8年翻了一倍多 · 录取率稳回52%", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面2-翻倍")
img.save(BASE + P + "-封面2-翻倍-1200x900.png")

# 封面3 见顶
img, d = new_canvas(); checks = []
badge(d, "三个信号 · 峰值临近")
put(d, checks, "2030", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "考生规模见顶窗口", font(44, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "出生人口已过峰 · 流入减速 · 学位覆盖峰值", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面3-见顶")
img.save(BASE + P + "-封面3-见顶-1200x900.png")

# 微头条配图 翻倍趋势
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 考生8年翻倍")
put(d, checks, "考生在涨 · 学位也在涨", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
nodes = [("2018", "7.21万", "增长起点"), ("2022", "11.2万", "5.9万学位"), ("2026", "15.30万", "约8万学位"), ("2027", "16-18万", "预测值")]
nx = 170; step = 280; line_y = 430
d.line([nx - 40, line_y, nx + step * 3 + 20, line_y], fill=EDGE, width=4)
for i, (yr, num, note) in enumerate(nodes):
    x = nx + i * step
    hi = (i == len(nodes) - 1)
    d.ellipse([x - 14, line_y - 14, x + 14, line_y + 14], fill=GOLD if hi else EDGE, outline=GOLD if hi else EDGE, width=2)
    put(d, checks, yr, font(28, True), (x, line_y - 80), color=WHITE, maxw=240)
    put(d, checks, num, font(40, True), (x, line_y + 64), color=GOLD if hi else WHITE, maxw=250)
    put(d, checks, note, font(22), (x, line_y + 116), color=SUB, maxw=250)
put(d, checks, "公办学位 5.9万→约8万（+35%）· 录取率稳在52%", font(28, True), (W / 2, 700), color=GOLD, maxw=1060)
box(d, 250, 770, 700, 84, r=42)
put(d, checks, "压力在高位 · 方向在好转", font(28, True), (W / 2, 812), color=WHITE, maxw=660)
source_line(d, checks)
verify(d, checks, "微头条配图-翻倍趋势")
img.save(BASE + P + "-微头条配图-翻倍趋势-1200x900.png")

# 正文图2 三个引擎
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 增长三引擎")
put(d, checks, "为什么考生涨这么快", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("人口净流入", "常住人口7年净增约500万人", "2025年末1,824.85万 · 净增25.9万"),
    ("出生高峰", "2023年考生跳涨1.40万", "对应2008年前后出生人口高峰"),
    ("高转化率", "初中入学→中考 稳定95%-97%", "2024年入学人数≈2027年中考人数"),
]
ry = 260
for tag, a, b in rows:
    box(d, 90, ry, W - 180, 120, r=16)
    d.rectangle([90, ry, 100, ry + 120], fill=GOLD)
    put(d, checks, tag, font(34, True), (140, ry + 38), anchor="lm", color=GOLD, maxw=250)
    put(d, checks, a, font(30, True), (450, ry + 38), anchor="lm", color=WHITE, maxw=500)
    put(d, checks, b, font(24), (450, ry + 82), anchor="lm", color=SUB, maxw=640)
    ry += 120 + 16
put(d, checks, "三个引擎强度正在变化 · 增速已放缓", font(28, True), (W / 2, 826), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "正文图2-三个引擎")
img.save(BASE + P + "-正文图2-三个引擎-1200x900.png")

# 正文图3 见顶信号
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 何时见顶")
put(d, checks, "2027-2030 · 峰值窗口", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("出生拐点", "2016年出生人口达峰后下降", "2031年前后考生压力缓解"),
    ("流入减速", "净增从年40-50万回落到25.9万", "学龄人口新增供给减少"),
    ("十五五窗口", "2030年前再增10万学位", "恰好覆盖考生峰值区间"),
]
ry = 260
for tag, a, b in rows:
    box(d, 90, ry, W - 180, 120, r=16)
    d.rectangle([90, ry, 100, ry + 120], fill=GOLD)
    put(d, checks, tag, font(34, True), (140, ry + 38), anchor="lm", color=GOLD, maxw=250)
    put(d, checks, a, font(30, True), (450, ry + 38), anchor="lm", color=WHITE, maxw=500)
    put(d, checks, b, font(24), (450, ry + 82), anchor="lm", color=SUB, maxw=640)
    ry += 120 + 16
box(d, 250, 744, 700, 84, r=42)
put(d, checks, "最难的时候 · 也是规划最好的时候", font(28, True), (W / 2, 786), color=WHITE, maxw=660)
source_line(d, checks)
verify(d, checks, "正文图3-见顶信号")
img.save(BASE + P + "-正文图3-见顶信号-1200x900.png")

print("S1-4 今日头条 6张 全部完成")
