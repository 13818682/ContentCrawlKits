# -*- coding: utf-8 -*-
"""S1-3 今日头条配图 6张（1200×900）：封面1主标题/封面2录取率52%/封面3学位增长2倍/微头条配图三组数字/正文图2出路全景/正文图3八年增长
设计语言按 13-2 模板：深蓝渐变 #143B73→#0B2545、金 #F2B84B、顶部胶囊徽章、底部来源、中心安全区。"""
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

def verify(checks, name):
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

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-3-竞争格局全景/02-今日头条/"
P = "08-S1-3-2027深圳中考家长必读：一张图看懂竞争格局-今日头条"

# ---------- 封面1 主标题 ----------
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 2027届备考")
put(d, checks, "一张图看懂竞争格局", font(72, True), (W / 2, 350), color=WHITE, maxw=1040)
put(d, checks, "16-18万考生 · 约8万公办学位 · 52%录取率", font(34), (W / 2, 470), color=GOLD, maxw=1040)
box(d, 250, 560, 700, 96, r=48)
put(d, checks, "考生翻倍 · 学位在追 · 出路不止公办", font(28, True), (W / 2, 608), color=WHITE, maxw=660)
source_line(d, checks)
verify(checks, "封面1-主标题")
img.save(BASE + P + "-封面1-主标题-1200x900.png")

# ---------- 封面2 录取率52% ----------
img, d = new_canvas(); checks = []
badge(d, "2027届深圳中考 · 关键数据")
put(d, checks, "52%", font(150, True), (W / 2, 360), color=GOLD, maxw=900)
put(d, checks, "公办普高录取率", font(44, True), (W / 2, 530), color=WHITE, maxw=1000)
put(d, checks, "全市普高（含民办）超73% · 2027届考生约16-18万", font(30), (W / 2, 630), color=LIGHT, maxw=1040)
source_line(d, checks)
verify(checks, "封面2-录取率数据")
img.save(BASE + P + "-封面2-录取率数据-1200x900.png")

# ---------- 封面3 学位增长 2倍 ----------
img, d = new_canvas(); checks = []
badge(d, "8年 · 学位追着考生跑")
put(d, checks, "2倍", font(150, True), (W / 2, 360), color=GOLD, maxw=900)
put(d, checks, "考生从7.21万涨到15.30万", font(44, True), (W / 2, 530), color=WHITE, maxw=1040)
put(d, checks, "公办学位同步从5.9万涨到约8万 · 录取率稳在52%", font(30), (W / 2, 630), color=LIGHT, maxw=1040)
source_line(d, checks)
verify(checks, "封面3-学位增长")
img.save(BASE + P + "-封面3-学位增长-1200x900.png")

# ---------- 微头条配图 三组数字 ----------
img, d = new_canvas(); checks = []
badge(d, "2027届深圳中考 · 三组数字")
put(d, checks, "先记住这3个数字", font(56, True), (W / 2, 210), color=WHITE, maxw=1000)
nums = [
    ("16-18万", "2027年预计考生人数", "2026年为15.30万"),
    ("约8万", "公办普高招生", "101所公办高中"),
    ("约52%", "公办普高录取率", "全市普高超73%"),
]
cw, ch, gap = 320, 340, 36
x0 = (W - (cw * 3 + gap * 2)) // 2
y0 = 300
for i, (num, lab, note) in enumerate(nums):
    x = x0 + i * (cw + gap)
    box(d, x, y0, cw, ch, r=20)
    d.rectangle([x, y0, x + 6, y0 + ch], fill=GOLD)
    put(d, checks, num, font(60, True), (x + cw // 2, y0 + 92), color=GOLD, maxw=cw - 30)
    put(d, checks, lab, font(30, True), (x + cw // 2, y0 + 200), color=WHITE, maxw=cw - 30)
    put(d, checks, note, font(22), (x + cw // 2, y0 + 272), color=SUB, maxw=cw - 36)
put(d, checks, "心里有这个坐标系，再看任何中考信息都不慌", font(30, True), (W / 2, y0 + ch + 64), color=GOLD, maxw=1040)
source_line(d, checks)
verify(checks, "微头条配图-三组数字")
img.save(BASE + P + "-微头条配图-三组数字-1200x900.png")

# ---------- 正文图2 出路全景 ----------
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 出路全景")
put(d, checks, "所有出路，一次看清", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("公办普高", "约8万 · 101所", "约52% · D类占比约23%"),
    ("民办普高", "33,195 · 49所", "学费3万-15万/年不等"),
    ("中职及技工", "33,254 · 30所", "3+4中本贯通可拿全日制本科"),
]
ry = 260
for tag, a, b in rows:
    box(d, 90, ry, W - 180, 120, r=16)
    d.rectangle([90, ry, 100, ry + 120], fill=GOLD)
    put(d, checks, tag, font(34, True), (140, ry + 38), anchor="lm", color=GOLD, maxw=260)
    put(d, checks, a, font(30, True), (460, ry + 38), anchor="lm", color=WHITE, maxw=430)
    put(d, checks, b, font(24), (460, ry + 82), anchor="lm", color=SUB, maxw=580)
    ry += 120 + 16
box(d, 90, ry, W - 180, 96, r=16)
put(d, checks, "合计 146,752 学位 · 180 所学校", font(30, True), (W / 2, ry + 48), color=GOLD, maxw=900)
put(d, checks, "约52%上公办 · 超73%上普高 · 几乎所有孩子有学上", font(28, True), (W / 2, 810), color=WHITE, maxw=1040)
source_line(d, checks, "数据来源：深圳市教育局2026年招生计划通知 · 逐条人工核对")
verify(checks, "正文图2-出路全景")
img.save(BASE + P + "-正文图2-出路全景-1200x900.png")

# ---------- 正文图3 8年增长时间轴 ----------
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 考生8年翻倍")
put(d, checks, "考生在涨，学位也在涨", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
nodes = [
    ("2018", "7.21万", "录取率约53%"),
    ("2020", "8.92万", "约44%（低点）"),
    ("2022", "11.2万", "5.9万学位"),
    ("2024", "13.52万", "6.9万学位"),
    ("2026", "15.30万", "约8万学位"),
]
nx = 150
step = 225
line_y = 430
d.line([nx - 40, line_y, nx + step * 4 + 20, line_y], fill=EDGE, width=4)
for i, (yr, num, note) in enumerate(nodes):
    x = nx + i * step
    hi = (i == len(nodes) - 1)
    d.ellipse([x - 14, line_y - 14, x + 14, line_y + 14], fill=GOLD if hi else EDGE, outline=GOLD if hi else EDGE, width=2)
    put(d, checks, yr, font(28, True), (x, line_y - 80), color=WHITE, maxw=200)
    put(d, checks, num, font(40, True), (x, line_y + 64), color=GOLD if hi else WHITE, maxw=210)
    put(d, checks, note, font(22), (x, line_y + 116), color=SUB, maxw=210)
put(d, checks, "考生翻倍+1倍多 · 公办学位增长35% · 录取率稳在52%", font(28, True), (W / 2, 700), color=GOLD, maxw=1040)
box(d, 250, 770, 700, 84, r=42)
put(d, checks, "学位建设在追着考生增长跑", font(28, True), (W / 2, 812), color=WHITE, maxw=660)
source_line(d, checks, "数据来源：深圳市招考办公布历年数据 · 逐条人工核对")
verify(checks, "正文图3-8年增长")
img.save(BASE + P + "-正文图3-8年增长-1200x900.png")

print("今日头条 6张 全部完成")
