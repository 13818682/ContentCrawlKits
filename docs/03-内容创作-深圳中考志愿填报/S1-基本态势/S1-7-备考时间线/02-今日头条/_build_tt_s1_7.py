# -*- coding: utf-8 -*-
"""S1-7 今日头条配图 6张（1200×900）：封面1主标题/封面2九个月/封面3志愿10天/微头条配图5阶段/正文图2关键节点/正文图3速查表"""
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

def source_line(d, checks, txt="数据来源：深圳市教育局官方公开信息 · 逐条人工核对"):
    put(d, checks, txt, font(22), (W / 2, H - 42), color=SUB, maxw=1080)

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/02-今日头条/"
P = "08-S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-今日头条"

# 封面1 主标题
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 2027届备考")
put(d, checks, "备考时间线", font(80, True), (W / 2, 330), color=WHITE, maxw=1000)
put(d, checks, "从今天起，每个月要做什么", font(34), (W / 2, 460), color=GOLD, maxw=1060)
box(d, 230, 560, 740, 96, r=48)
put(d, checks, "9个月窗口 · 5个阶段 · 志愿只有10天", font(28, True), (W / 2, 608), color=WHITE, maxw=700)
source_line(d, checks)
verify(d, checks, "封面1-主标题")
img.save(BASE + P + "-封面1-主标题-1200x900.png")

# 封面2 九个月
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 时间窗口")
put(d, checks, "9个月", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "从现在到明年5月填志愿", font(44, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "每天15分钟 · 比90%临时抱佛脚的家长从容", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面2-九个月")
img.save(BASE + P + "-封面2-九个月-1200x900.png")

# 封面3 志愿10天
img, d = new_canvas(); checks = []
badge(d, "最关键 · 志愿填报")
put(d, checks, "10天", font(150, True), (W / 2, 350), color=GOLD, maxw=800)
put(d, checks, "志愿填报窗口", font(44, True), (W / 2, 530), color=WHITE, maxw=1060)
put(d, checks, "2026年为5月23日-6月1日 · 确认后不可更改", font(30), (W / 2, 630), color=LIGHT, maxw=1060)
source_line(d, checks)
verify(d, checks, "封面3-志愿10天")
img.save(BASE + P + "-封面3-志愿10天-1200x900.png")

# 微头条配图 5阶段时间线
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 备考5阶段")
put(d, checks, "9个月怎么安排", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("8-9月", "建立认知框架", "三组数字 · AC/D/C类 · 指标生 · 体育14分开始累积"),
    ("10-12月", "信息收集期", "研究指标生名额 · 目标学校 · 11月期中考定位"),
    ("1-3月", "定位校准期", "一模定位 · 政策发布 · 3月下旬报名(D类社保居住证)"),
    ("4-5月", "决策冲刺期", "二模 · 体育中考 · 草拟冲稳保 · 5月志愿填报10天"),
    ("6-8月", "考试录取", "中考 → 出分 → 录取 → 高一衔接"),
]
ry = 250
for t, tag, b in rows:
    box(d, 90, ry, W - 180, 86, r=14)
    put(d, checks, t, font(28, True), (130, ry + 28), anchor="lm", color=GOLD, maxw=150)
    put(d, checks, tag, font(30, True), (310, ry + 28), anchor="lm", color=WHITE, maxw=260)
    put(d, checks, b, font(22), (310, ry + 62), anchor="lm", color=SUB, maxw=820)
    ry += 86 + 10
put(d, checks, "现在开始，你有9个月；明年才开始，只有10天", font(28, True), (W / 2, ry + 22), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "微头条配图-5阶段")
img.save(BASE + P + "-微头条配图-5阶段时间线-1200x900.png")

# 正文图2 关键节点时间轴
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 关键节点")
put(d, checks, "关键节点速查", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
nodes = [("现在", "体育14分累积"), ("11月", "期中考定位"), ("1-3月", "一模"), ("3月", "中考报名"), ("5月下旬", "志愿填报10天"), ("6月", "中考笔试")]
nx = 140; step = 184; line_y = 430
d.line([nx - 30, line_y, nx + step * 5 + 20, line_y], fill=EDGE, width=4)
for i, (t, note) in enumerate(nodes):
    x = nx + i * step
    hi = (i == 4)
    d.ellipse([x - 13, line_y - 13, x + 13, line_y + 13], fill=GOLD if hi else EDGE, outline=GOLD if hi else EDGE, width=2)
    put(d, checks, t, font(26, True), (x, line_y - 76), color=WHITE, maxw=170)
    put(d, checks, note, font(22), (x, line_y + 48), color=GOLD if hi else SUB, maxw=170)
put(d, checks, "最关键的10天在5月下旬志愿填报", font(30, True), (W / 2, 700), color=GOLD, maxw=1060)
box(d, 230, 760, 740, 84, r=42)
put(d, checks, "确认后不可更改 · 提前准备是唯一解", font(28, True), (W / 2, 802), color=WHITE, maxw=700)
source_line(d, checks)
verify(d, checks, "正文图2-关键节点")
img.save(BASE + P + "-正文图2-关键节点-1200x900.png")

# 正文图3 速查表
img, d = new_canvas(); checks = []
badge(d, "深圳中考 · 每月速查表")
put(d, checks, "孩子做什么 · 家长做什么", font(52, True), (W / 2, 190), color=WHITE, maxw=1000)
rows = [
    ("8-9月", "初三开学+体育选项", "建立认知框架 · 体育14分"),
    ("10-12月", "期中期末冲刺", "研究指标生+目标学校"),
    ("1-3月", "一模定位", "政策跟踪+材料准备"),
    ("4-5月", "二模+体育+实验", "志愿草拟+最终方案"),
    ("6-8月", "中考", "录取跟进+高一衔接"),
]
ry = 250
for t, a, b in rows:
    box(d, 90, ry, W - 180, 82, r=14)
    put(d, checks, t, font(28, True), (130, ry + 28), anchor="lm", color=GOLD, maxw=150)
    put(d, checks, a, font(26, True), (320, ry + 28), anchor="lm", color=WHITE, maxw=360)
    put(d, checks, b, font(24), (700, ry + 28), anchor="lm", color=SUB, maxw=420)
    ry += 82 + 10
put(d, checks, "收藏这张表 · 贴在家里显眼的地方", font(30, True), (W / 2, ry + 24), color=GOLD, maxw=1060)
source_line(d, checks)
verify(d, checks, "正文图3-速查表")
img.save(BASE + P + "-正文图3-速查表-1200x900.png")

print("S1-7 今日头条 6张 全部完成")
