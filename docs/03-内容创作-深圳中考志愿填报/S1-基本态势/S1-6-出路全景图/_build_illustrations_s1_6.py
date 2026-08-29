# -*- coding: utf-8 -*-
"""S1-6 精简版 · 配套插图生成（封面 900×383 + 章节条 900×220 + 数据卡 900×400）
风格同 S1-4/5：深蓝渐变 + 金竖条章节头 + 金色数据，PIL 直出。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = 900
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    # 正文（<20）放大 1.4 倍；主标题/大数字（≥26）保持，层级分明
    if size < 20:
        size = int(round(size * 1.4))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-6-出路全景图/01-公众号/S1-6-一张图看懂深圳中考全部出路-公众号"

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

def verify(d, checks, H, name):
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
put(d, ck, "深圳中考 · S1 基本态势 · 系列第6篇", font(13, True), (50, 40), anchor="lm", color=GOLD)
put(d, ck, "深圳中考全部出路全景", font(34, True), (50, 88), anchor="lm")
put(d, ck, "公办+民办+中职+中本贯通 · 146,752个学位 · 4层出路", font(15), (50, 132), anchor="lm", color=LIGHT)
d.line([50, 164, 140, 164], fill=GOLD, width=3)
covers = [
    (122, "约52%", "公办普高录取率"),
    (350, "33,195", "民办普高招生"),
    (578, "33,254", "中职及技工招生"),
]
for x, num, lab in covers:
    box(d, x, 230, 200, 110)
    put(d, ck, num, font(32, True), (x + 100, 272), color=GOLD)
    put(d, ck, lab, font(14), (x + 100, 316), color=WHITE)
img.save(BASE + "-封面.png")
print("封面", verify(d, ck, 383, "封面"))

# ========== 章节条 900×220 ==========
def chapter_strip(fname, num, title, subtitle):
    img, d, ck = new_canvas(220)
    d.rectangle([50, 110 - 27, 58, 110 + 27], fill=GOLD)
    put(d, ck, f"{num}  {title}", font(36, True), (78, 100), anchor="lm")
    put(d, ck, subtitle, font(14), (78, 148), anchor="lm", color=LIGHT)
    d.line([50, 172, 140, 172], fill=GOLD, width=3)
    img.save(fname)
    print(fname.split('/')[-1], verify(d, ck, 220, fname.split('/')[-1][:10]))

chapter_strip(BASE + "-插图-01-章节条-公办普高.png", "01",
              "第一层 · 公办普高", "约8万人 · 101所 · AC类61,797 + D类18,506（约23%）· 2026新增7所")
chapter_strip(BASE + "-插图-03-章节条-民办普高.png", "02",
              "第二层 · 民办普高", "33,195人 · 49所 · 学费每年3万-15万")
chapter_strip(BASE + "-插图-05-章节条-中职曲线读大学.png", "03",
              "第三层 · 中职及技工", "33,254人 · 30所 · 公办15,924 + 民办17,330 · 两条曲线读大学")
chapter_strip(BASE + "-插图-07-章节条-行动建议.png", "04",
              "给你的行动建议", "公办线以上 / 公办线边缘 / D类 / 低分段 · 各有一套组合")

# ========== 数据卡 900×400 ==========
def data_card(fname, title, draw_body):
    img, d, ck = new_canvas(400)
    put(d, ck, title, font(26, True), (50, 50), anchor="lm")
    d.line([50, 78, 140, 78], fill=GOLD, width=3)
    draw_body(d, ck)
    img.save(fname)
    print(fname.split('/')[-1], verify(d, ck, 400, fname.split('/')[-1][:10]))

# 插图-02 三层学位并列 + 合计
def body02(d, ck):
    cards = [
        (20, "约8万", "公办普高", "101所 · 约52%"),
        (313, "33,195", "民办普高", "49所 · 学费3万-15万"),
        (606, "33,254", "中职及技工 · 30所", "公办15,924 + 民办17,330"),
    ]
    for x, num, lab, note in cards:
        box(d, x, 122, 273, 240)
        put(d, ck, num, font(42, True), (x + 137, 188), color=GOLD)
        put(d, ck, lab, font(17, True), (x + 137, 260), color=WHITE)
        put(d, ck, note, font(13), (x + 137, 322), color=SUB)
    put(d, ck, "合计 146,752 个学位 · 180 所学校 · 覆盖全部15.3万考生", font(14, True), (450, 384), color=GOLD)
data_card(BASE + "-插图-02-数据卡-三层学位.png", "四层出路，146,752个学位", body02)

# 插图-04 民办对AC/D一视同仁
def body04(d, ck):
    put(d, ck, "公办D类占比仅约23%", font(16, True), (50, 102), anchor="lm", color=GOLD)
    ac_w = int(620 * 61797 / 80303)
    d.rectangle([50, 126, 50 + ac_w, 158], fill=LIGHT)
    d.rectangle([50 + ac_w, 126, 670, 158], fill=GOLD)
    put(d, ck, "AC类 61,797人（约77%）", font(14), (210, 194), color=WHITE)
    put(d, ck, "D类 18,506人（约23%）", font(14), (560, 194), color=GOLD)
    put(d, ck, "但民办普高对AC/D类同分录取：", font(16, True), (50, 246), anchor="lm", color=GOLD)
    lines = [
        "对D类家长，优质民办是值得认真了解的选项",
        "部分优质校在艺术、国际方向有特色",
        "学费跨度大（3万-15万/年），以各校简章为准",
    ]
    yy = 282
    for ln in lines:
        put(d, ck, ln, font(14), (50, yy), anchor="lm", color=WHITE)
        yy += 40
data_card(BASE + "-插图-04-数据卡-民办同分.png", "民办对AC/D一视同仁", body04)

# 插图-06 两条曲线读大学
def body06(d, ck):
    cards = [
        (92, "3+4 中本贯通", "300名额", "中职3年→本科4年→全日制本科文凭", "一职对口深技大 · 二职对口深职大", GOLD),
        (468, "3+2 中高贯通", "2,853人·63专业", "中职3年→高职2年", "低分段被低估的选项", LIGHT),
    ]
    for i, (x, tag, num, detail, note, tc) in enumerate(cards):
        box(d, x, 116, 340, 252)
        cx = x + 170
        put(d, ck, tag, font(18, True), (cx, 174), color=tc)
        put(d, ck, num, font(30, True), (cx, 236), color=GOLD)
        put(d, ck, detail, font(13), (cx, 302), color=WHITE)
        put(d, ck, note, font(12), (cx, 344), color=SUB)
    put(d, ck, "中职≠没出路：两条路知道的人还不多，是低分段的宝贵选项", font(14, True), (450, 384), color=GOLD)
data_card(BASE + "-插图-06-数据卡-两条路径.png", "两条“曲线读大学”的路", body06)

# ========== 汇总 ==========
total = sum(b for _, b in all_checks)
print("TOTAL OVERFLOW:", "PASS" if total == 0 else f"FAIL {total}")
