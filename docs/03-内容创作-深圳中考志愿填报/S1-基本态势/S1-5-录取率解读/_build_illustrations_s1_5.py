# -*- coding: utf-8 -*-
"""S1-5 精简版 · 配套插图生成（封面 900×383 + 章节条 900×220 + 数据卡 900×400）
风格同 S1-4：深蓝渐变 + 金竖条章节头 + 金色数据，PIL 直出。"""
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

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-5-录取率解读/01-公众号/S1-5-公办普高52%录取率意味着什么？2027届家长该知道的3个真相-公众号"

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
put(d, ck, "深圳中考 · S1 基本态势 · 系列第5篇", font(13, True), (50, 40), anchor="lm", color=GOLD)
put(d, ck, "52%录取率背后的3个真相", font(34, True), (50, 88), anchor="lm")
put(d, ck, "52%只是公办率 · 全市普高超73% · D类家长看的是另一个数字", font(15), (50, 132), anchor="lm", color=LIGHT)
d.line([50, 164, 140, 164], fill=GOLD, width=3)
covers = [
    (50, "52%", "公办普高录取率"),
    (310, "超73%", "全市普高率（含民办）"),
    (570, "146,752", "高中阶段学位（普高+中职）"),
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

chapter_strip(BASE + "-插图-01-章节条-真相一-52与73.png", "01",
              "真相一 · 52%是公办率", "全市普高率超73% · 113,498个普高学位")
chapter_strip(BASE + "-插图-03-章节条-真相二-稳定低位.png", "02",
              "真相二 · 52%是稳定低位", "不是下滑的悬崖 · 44%(2020)→52%(2026)")
chapter_strip(BASE + "-插图-05-章节条-真相三-D类23.png", "03",
              "真相三 · D类看的是约23%", "AC类61,797 · D类18,506 · 但23%≠没希望")
chapter_strip(BASE + "-插图-07-章节条-三个世界.png", "04",
              "一个数字读出三个世界", "同一句52%，三类家长看到不同的世界")

# ========== 数据卡 900×400 ==========
def data_card(fname, title, draw_body):
    img, d, ck = new_canvas(400)
    put(d, ck, title, font(26, True), (50, 50), anchor="lm")
    d.line([50, 78, 140, 78], fill=GOLD, width=3)
    draw_body(d, ck)
    img.save(fname)
    print(fname.split('/')[-1], verify(ck, 400, fname.split('/')[-1][:10]))

# 插图-02 三层含义：三格并列卡
def body02(d, ck):
    cards = [
        (40, "52%", "公办普高录取率", "2026年"),
        (320, "超73%", "全市普高率（含民办）", "113,498个学位"),
        (600, "146,752", "高中阶段学位", "普高+中职 · 几乎人人有书读"),
    ]
    for x, num, lab, note in cards:
        box(d, x, 130, 260, 220)
        put(d, ck, num, font(42, True), (x + 130, 190), color=GOLD)
        put(d, ck, lab, font(17, True), (x + 130, 250), color=WHITE)
        put(d, ck, note, font(13), (x + 130, 290), color=SUB)
data_card(BASE + "-插图-02-数据卡-三层含义.png", "一个数字，三层含义", body02)

# 插图-04 历年录取率：柱状
def body04(d, ck):
    basey = 330
    d.line([80, basey, 820, basey], fill=EDGE, width=2)
    data = [("2020", 44, GOLD), ("2022", 53, LIGHT), ("2024", 52, LIGHT), ("2025", 52, LIGHT), ("2026", 52, GOLD)]
    cx = 140
    for yr, val, color in data:
        bh = val / 60.0 * 260
        d.rectangle([cx - 36, basey - bh, cx + 36, basey], fill=color)
        put(d, ck, f"{val}%", font(16, True), (cx, basey - bh - 14), color=GOLD if val == 44 or yr == "2026" else WHITE)
        put(d, ck, yr, font(14), (cx, basey + 22), color=LIGHT)
        cx += 150
    put(d, ck, "2020年后连续4年稳定在52%上下 · 学位在追着考生跑", font(13), (450, 372), color=SUB)
data_card(BASE + "-插图-04-数据卡-历年录取率.png", "52%是稳定低位，不是下滑悬崖", body04)

# 插图-06 D类占比：堆叠条 + 四点希望
def body06(d, ck):
    put(d, ck, "公办8万招生指标", font(16, True), (50, 108), anchor="lm")
    ac_w = int(620 * 61797 / 80303)
    d.rectangle([50, 128, 50 + ac_w, 158], fill=LIGHT)
    d.rectangle([50 + ac_w, 128, 670, 158], fill=GOLD)
    put(d, ck, "AC类 61,797人（约77%）", font(14), (200, 182), color=WHITE)
    put(d, ck, "D类 18,506人（约23%）", font(14), (560, 182), color=GOLD)
    put(d, ck, "但 23% ≠ 没希望：", font(16, True), (50, 224), anchor="lm", color=GOLD)
    lines = [
        "指标生已实现D类全覆盖 · 你所在初中一定有D类指标名额",
        "四大名校D线与AC持平（2026深中 AC 592 / D 592）",
        "民办高中对AC/D一视同仁",
        "3+4中本贯通是D类中低分段的新出路",
    ]
    yy = 258
    for ln in lines:
        put(d, ck, ln, font(14), (50, yy), anchor="lm", color=WHITE)
        yy += 28
data_card(BASE + "-插图-06-数据卡-D类占比.png", "D类家长面对的是约23%", body06)

# 插图-08 三类家长并列卡
def body08(d, ck):
    cards = [
        (40, "AC类高分段", "稳定赛道", "精确择校 + 用好指标生", GOLD),
        (320, "D类中分段", "提前布局的赛场", "Plan B 不是可选而是必备", GOLD),
        (600, "低分段", "被低估的路", "中本贯通/3+2 是正经出路", LIGHT),
    ]
    for x, tag, sub, detail, tc in cards:
        box(d, x, 130, 260, 220)
        put(d, ck, tag, font(18, True), (x + 130, 172), color=tc)
        put(d, ck, sub, font(14), (x + 130, 210), color=SUB)
        put(d, ck, detail, font(13), (x + 130, 260), color=WHITE)
data_card(BASE + "-插图-08-数据卡-三类家长.png", "一个数字读出三个世界", body08)

# ========== 汇总 ==========
total = sum(b for _, b in all_checks)
print("TOTAL OVERFLOW:", "PASS" if total == 0 else f"FAIL {total}")
