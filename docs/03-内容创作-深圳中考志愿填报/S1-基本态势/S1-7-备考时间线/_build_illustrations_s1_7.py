# -*- coding: utf-8 -*-
"""S1-7 精简版 · 配套插图生成（封面 900×383 + 章节条 900×220 + 数据卡 900×400）
风格同 S1-4/5/6：深蓝渐变 + 金竖条章节头 + 金色数据，PIL 直出。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = 900
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/01-公众号/S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-公众号"

all_checks = []
def new_canvas(h):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img), []

def put(d, checks, text, fnt, xy, anchor="mm", color=WHITE):
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    checks.append((text, fnt, xy, anchor))

def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def verify(checks, H, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bbox = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bbox[0] + cx, bbox[1] + cy
        x1, y1 = bbox[2] + cx, bbox[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  OVERFLOW [{name}] [{text[:14]}] x=({x0:.0f},{x1:.0f}) y=({y0:.0f},{y1:.0f})")
    all_checks.append((name, bad))
    return bad

# ========== 封面 900×383 ==========
img, d, ck = new_canvas(383)
put(d, ck, "深圳中考 · S1 基本态势 · 系列第7篇·收官", font(13, True), (50, 40), anchor="lm", color=GOLD)
put(d, ck, "2027届考生备考时间线", font(34, True), (50, 88), anchor="lm")
put(d, ck, "从今天起，9个月每月该做什么 · 现在开始刚刚好", font(15), (50, 132), anchor="lm", color=LIGHT)
d.line([50, 164, 140, 164], fill=GOLD, width=3)
covers = [
    (50, "9个月", "备考时间窗口"),
    (310, "5个", "备考阶段"),
    (570, "10天", "志愿填报窗口"),
]
for x, num, lab in covers:
    box(d, x, 230, 260, 110)
    put(d, ck, num, font(32, True), (x + 130, 272), color=GOLD)
    put(d, ck, lab, font(14), (x + 130, 316), color=WHITE)
img.save(BASE + "-封面.png")
print("封面", verify(ck, 383, "封面"))

# ========== 章节条 900×220 ==========
def chapter_strip(fname, num, title, subtitle):
    img, d, ck = new_canvas(220)
    d.rectangle([50, 110 - 27, 58, 110 + 27], fill=GOLD)
    put(d, ck, f"{num}  {title}", font(36, True), (78, 100), anchor="lm")
    put(d, ck, subtitle, font(14), (78, 148), anchor="lm", color=LIGHT)
    d.line([50, 172, 140, 172], fill=GOLD, width=3)
    img.save(fname)
    print(fname.split('/')[-1], verify(ck, 220, fname.split('/')[-1][:10]))

chapter_strip(BASE + "-插图-01-章节条-建立认知框架.png", "01",
              "现在（8-9月）· 建立认知框架", "三组基本数字 · AC/D类 · 指标生 · 体育过程性评价14分")
chapter_strip(BASE + "-插图-03-章节条-决策冲刺期.png", "02",
              "4-5月 · 决策冲刺期", "最关键的两个月 · 二模+体育中考+理化实验 · 志愿草拟")
chapter_strip(BASE + "-插图-05-章节条-录取与复盘.png", "03",
              "6-8月 · 考试+录取+复盘", "6月下旬中考 → 7月中旬出分 → 7-8月录取 → 高一衔接")

# ========== 数据卡 900×400 ==========
def data_card(fname, title, draw_body):
    img, d, ck = new_canvas(400)
    put(d, ck, title, font(26, True), (50, 50), anchor="lm")
    d.line([50, 78, 140, 78], fill=GOLD, width=3)
    draw_body(d, ck)
    img.save(fname)
    print(fname.split('/')[-1], verify(ck, 400, fname.split('/')[-1][:10]))

# 插图-02 全年速查表
def body02(d, ck):
    box(d, 40, 130, 820, 230)
    put(d, ck, "时间", font(13, True), (95, 152), color=LIGHT)
    put(d, ck, "孩子重点", font(13, True), (285, 152), color=LIGHT)
    put(d, ck, "家长重点", font(13, True), (520, 152), color=LIGHT)
    put(d, ck, "关键节点", font(13, True), (760, 152), color=LIGHT)
    d.line([80, 168, 820, 168], fill=GOLD, width=2)
    rows = [
        ("8-9月", "开学+体育选项", "建立认知框架", "体育过程性评价"),
        ("10-12月", "期中+期末冲刺", "研究指标生+目标学校", "一模（部分区）"),
        ("1-3月", "一模定位", "政策发布+材料准备", "中考报名"),
        ("4-5月", "二模+体育+实验", "志愿草拟+最终方案", "志愿填报（10天）"),
        ("6-8月", "中考", "录取跟进+高一衔接", "录取公布"),
    ]
    ry = 190
    for a, b, c, node in rows:
        put(d, ck, a, font(13, True), (95, ry), color=GOLD)
        put(d, ck, b, font(13), (285, ry), color=WHITE)
        put(d, ck, c, font(13), (520, ry), color=WHITE)
        put(d, ck, node, font(13), (760, ry), color=WHITE)
        ry += 34
data_card(BASE + "-插图-02-数据卡-全年速查表.png", "全年备考速查表（建议截图保存）", body02)

# 插图-04 志愿填报10天窗口
def body04(d, ck):
    put(d, ck, "5月下旬 · 约10天窗口", font(16, True), (50, 112), anchor="lm", color=GOLD)
    put(d, ck, "2026年为5月23日 - 6月1日（2027年以当年公告为准）", font(13), (50, 142), anchor="lm", color=LIGHT)
    for i in range(10):
        x = 50 + i * 80
        box(d, x, 168, 68, 76, fill=CARD if i < 9 else GOLD, outline=EDGE, r=10)
        put(d, ck, f"{i+1}", font(20, True), (x + 34, 200), color=GOLD if i < 9 else (27, 58, 92))
    put(d, ck, "前8个月所有准备，都在这一刻兑现", font(15, True), (50, 268), anchor="lm", color=WHITE)
    lines = [
        "用上你之前所有准备的关键时刻",
        "确定最终志愿方案——确认后不可更改",
        "检查每所学校：分数线 · 招生人数 · 走读/住宿要求",
    ]
    yy = 304
    for ln in lines:
        put(d, ck, ln, font(14), (50, yy), anchor="lm", color=WHITE)
        yy += 28
data_card(BASE + "-插图-04-数据卡-志愿10天.png", "志愿填报：10天窗口，定稿不可改", body04)

# 插图-06 家长每月15分钟×9个月
def body06(d, ck):
    put(d, ck, "从现在（8月）到明年5月填志愿：9个月窗口", font(16, True), (50, 108), anchor="lm", color=GOLD)
    months = ["8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月", "4月", "5月"]
    stages = ["认知", "认知", "信息", "信息", "信息", "定位", "定位", "定位", "决策", "决策"]
    cx = 45
    for i, (m, st) in enumerate(zip(months, stages)):
        box(d, cx, 136, 78, 96, fill=GOLD if i in (8, 9) else CARD, outline=EDGE, r=10)
        put(d, ck, m, font(18, True), (cx + 39, 168), color=(27, 58, 92) if i in (8, 9) else GOLD)
        put(d, ck, st, font(13), (cx + 39, 200), color=WHITE)
        cx += 82
    put(d, ck, "每天花15分钟了解一个信息点", font(15, True), (50, 262), anchor="lm", color=WHITE)
    put(d, ck, "8-9月认知框架 → 10-12月信息收集 → 1-3月定位校准 → 4-5月决策冲刺", font(14), (50, 300), anchor="lm", color=LIGHT)
    put(d, ck, "到明年5月，你已比90%临时抱佛脚的家长更清楚孩子该怎么做", font(13, True), (50, 338), anchor="lm", color=GOLD)
data_card(BASE + "-插图-06-数据卡-家长每月15分.png", "家长节奏：9个月 × 每月15分钟", body06)

# ========== 汇总 ==========
total = sum(b for _, b in all_checks)
print("TOTAL OVERFLOW:", "PASS" if total == 0 else f"FAIL {total}")
