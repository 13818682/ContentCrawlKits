# -*- coding: utf-8 -*-
"""S1-2 知乎配图生成：回答配图（1600×900 5大启示信息图）+ 想法配图（1080×1080 4条数据卡）
风格同 13-5 模板/S1-1：深蓝渐变 + 金竖条 + 金标题 + 行盒数据，PIL 直出。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

def font(size, bold=False):
    if size <= 17:                       # 正文文字统一放大1.35倍，展示大字不受影响
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

def new_canvas(w, h):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(w, axis=1).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)

def put(d, checks, W, H, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:                                   # 越界自适应：超出maxw/画布则缩小字号
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

def verify(checks, W, H, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy}) 边({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
    print(f"{name}: 共{len(checks)}处文字，{bad}处越界")

# =====================================================================
# 一、知乎回答配图：5大启示信息图 1600×900
# =====================================================================
W, H = 1600, 900
img, d = new_canvas(W, H)
checks = []

# 标题区
d.rectangle([120, 84, 130, 180], fill=GOLD)
put(d, checks, W, H, "知乎回答 · 2026深圳中考数据复盘", font(28, True), (166, 82), anchor="lm", color=GOLD, maxw=1300)
put(d, checks, W, H, "5个启示，给2027届家长", font(64, True), (166, 142), anchor="lm", color=WHITE, maxw=1400)
put(d, checks, W, H, "数据来自2026年第一批录取标准公告 · 每条启示跟着行动指南", font(30), (166, 210), anchor="lm", color=LIGHT, maxw=1350)
d.line([120, 246, 240, 246], fill=GOLD, width=4)

# 5 大启示行盒
rows = [
    ("① 四大名校 AC=D 持平", "顶尖层户籍差距缩小 · 深中592/592 · 深实验590/590"),
    ("② 走读最高降35分", "崇文506→走读471 · 代价是不能住校 · 全市计划7,455人"),
    ("③ 新校首年分化", "最高559→最低487 · 选新校看「谁在办」"),
    ("④ 指标生控制线", "中间层降分5-15分 · 个别超20分 · 只能填1所"),
    ("⑤ D类占比约23%", "头部可冲 · 中下层480-530分段早备Plan B"),
]
row_y = 284
row_h, gap = 86, 12
for tag, detail in rows:
    box(d, 40, row_y, W - 80, row_h, r=14)
    put(d, checks, W, H, tag, font(28, True), (76, row_y + 28), anchor="lm", color=GOLD, maxw=680)
    put(d, checks, W, H, detail, font(26), (76, row_y + 60), anchor="lm", color=WHITE, maxw=1360)
    row_y += row_h + gap

# 底部金句 + 来源
put(d, checks, W, H, "数据不是用来焦虑的，是用来做决策的", font(30, True), (W // 2, 838), color=GOLD, maxw=1400)
put(d, checks, W, H, "来源：深圳市教育局2026年第一批录取标准公告 · 逐条人工核对", font(22), (W // 2, 882), color=SUB, maxw=1400)

verify(checks, W, H, "知乎回答配图")
out1 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-2-数据复盘-承前启后/05.知乎/03-S1-2-2026年深圳中考数据复盘：对2027届家长的5个启示-知乎-回答配图-5大启示-1600x900.png"
img.save(out1)
print("已生成:", out1)

# =====================================================================
# 二、知乎想法配图：4条数据卡 1080×1080
# =====================================================================
W2, H2 = 1080, 1080
img2, d2 = new_canvas(W2, H2)
checks2 = []
d2.rectangle([90, 74, 100, 142], fill=GOLD)
put(d2, checks2, W2, H2, "2026深圳中考 · 这4条数据值得看", font(40, True), (128, 104), anchor="lm", color=WHITE, maxw=900)
put(d2, checks2, W2, H2, "「涨没涨」不是重点 · 看懂才重要", font(24), (128, 160), anchor="lm", color=LIGHT, maxw=900)

rows4 = [
    ("四大 AC=D 全部持平", "深中592 · 深实验590 · 深外587"),
    ("走读最高降35分", "崇文506 → 走读471"),
    ("新校首年分化明显", "最高559 · 最低487"),
    ("D类占比约23%", "公办8万 · 18,506人"),
]
row_y = 200
row_h, gap = 170, 16
for line1, line2 in rows4:
    box(d2, 76, row_y, 928, row_h, r=18)
    put(d2, checks2, W2, H2, line1, font(34, True), (106, row_y + 52), anchor="lm", color=GOLD, maxw=860)
    put(d2, checks2, W2, H2, line2, font(28), (106, row_y + 122), anchor="lm", color=WHITE, maxw=860)
    row_y += row_h + gap

put(d2, checks2, W2, H2, "数据不是用来焦虑的，是用来做决策的", font(30, True), (W2 // 2, 976), color=GOLD, maxw=920)
put(d2, checks2, W2, H2, "来源：深圳市教育局2026年第一批录取标准公告", font(22), (W2 // 2, 1032), color=SUB, maxw=920)

verify(checks2, W2, H2, "知乎想法配图")
out2 = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-2-数据复盘-承前启后/05.知乎/04-S1-2-2026年深圳中考数据复盘：对2027届家长的5个启示-知乎-想法配图-4条数据-1080x1080.png"
img2.save(out2)
print("已生成:", out2)
print("全部完成")
