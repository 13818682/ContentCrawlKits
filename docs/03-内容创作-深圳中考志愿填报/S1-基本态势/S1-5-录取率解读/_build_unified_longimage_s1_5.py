# -*- coding: utf-8 -*-
"""S1-5 极简版 · 统一长图（风格同 S1-1/2/3/4：金竖条章节头/行盒/系列钩子卡，连续渐变）
内容：三数字卡(52%/73%/146752) + 历年录取率迷你表 + 真相三行盒 + 对号入座 + 系列第5篇钩子"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 2580
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:                       # 正文文字统一放大1.35倍，展示大字不受影响
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)
FBD = font(34, True)

t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
d = ImageDraw.Draw(img)

checks = []
def put(text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
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
    checks.append((text, fnt, xy, anchor, color, maxw))

def box(x, y, w, h, fill=CARD, outline=EDGE, r=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def chapter(ty, txt):
    d.rectangle([50, ty - 27, 58, ty + 27], fill=GOLD)
    put(txt, font(36, True), (78, ty), anchor="lm", color=WHITE)
    d.line([50, ty + 45, 140, ty + 45], fill=GOLD, width=3)

def row(ry, tag, detail, tagcolor=GOLD):
    box(40, ry, W - 80, 95)
    put(tag, font(17, True), (76, ry + 30), anchor="lm", color=tagcolor)
    put(detail, font(14), (76, ry + 64), anchor="lm", color=WHITE, maxw=720)

def takeaway(ty, txt):
    put(txt, font(15, True), (W / 2, ty), color=GOLD, maxw=W - 80)

# ---------- 页眉 ----------
put("深圳中考 · S1 基本态势 · 系列第5篇", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("52%录取率背后的3个真相", FBD, (50, 74), anchor="lm", color=WHITE)
put("52%只是公办率 · 全市普高超73% · D类家长看的是另一个数字", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 三数字卡 ----------
chapter(208, "01 · 一个数字，三层含义")
card_specs = [
    (40, "52%", "公办普高录取率", "2026年 · 不是全部故事"),
    (320, "超73%", "全市普高率（含民办）", "公办8万 + 民办33,195 = 113,498学位"),
    (600, "146,752", "高中阶段学位", "普高+中职 · 几乎所有孩子有书读"),
]
for x, num, lab, note in card_specs:
    box(x, 275, 260, 220)
    put(num, font(42, True), (x + 130, 275 + 60), color=GOLD)
    put(lab, font(17, True), (x + 130, 275 + 116), color=WHITE)
    put(note, font(12), (x + 130, 275 + 154), color=SUB, maxw=230)
takeaway(540, "这意味着什么：“一半孩子没高中读”是误解——约七成上普高，加上中职几乎人人有书读。")

# ---------- 02 真相二：历年录取率迷你表 ----------
chapter(595, "02 · 真相：52%是稳定低位，不是下滑悬崖")
box(40, 660, W - 80, 300)
put("年份", font(15, True), (300, 692), anchor="mm", color=LIGHT)
put("公办录取率", font(15, True), (600, 692), anchor="mm", color=LIGHT)
d.line([90, 716, 810, 716], fill=GOLD, width=2)
rate_rows = [
    ("2020", "约44%"),
    ("2022", "约53%"),
    ("2024", "约52%"),
    ("2025", "约52%"),
    ("2026", "约52%"),
]
ry0 = 756
for yr, rate in rate_rows:
    put(yr, font(16, True), (300, ry0), anchor="mm", color=WHITE)
    put(rate, font(16, True), (600, ry0), anchor="mm", color=GOLD if yr in ("2020", "2026") else WHITE)
    ry0 += 40
put("2020年跌至44%：考生8.92万 vs 学位约4.1万没跟上 · 之后学位开始追赶",
    font(13), (W / 2, 945), color=SUB, maxw=W - 100)
takeaway(1005, "这意味着什么：52%不是越来越难，是规划支撑的稳定——学位在追着考生跑。")

# ---------- 03 真相三：D类看23% ----------
chapter(1060, "03 · 但D类家长看的是另一个比例：约23%")
rows_03 = [
    ("公办8万指标", "AC类61,797人 · D类18,506人 · D类占比仅约23%", GOLD),
    ("但23%≠没希望", "指标生全覆盖 · 四大持平(592/592) · 民办一视同仁 · 3+4新出路", LIGHT),
]
ry = 1125
for tag, detail, tc in rows_03:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1370, "这意味着什么：路更窄，但不是死胡同——关键是更早出发。")

# ---------- 04 对号入座 ----------
chapter(1425, "04 · 一个数字，三种家长")
rows_04 = [
    ("AC类高分段", "稳定赛道 · 挑战在精确择校 + 用好指标生", GOLD),
    ("D类中分段", "Plan B（民办/中职/中本贯通）不是可选而是必备", GOLD),
    ("低分段", "被低估的路 · 中本贯通/3+2/优质民办是正经出路", LIGHT),
]
ry4 = 1490
for tag, detail, tc in rows_04:
    row(ry4, tag, detail, tc)
    ry4 += 110

# ---------- 05 系列第5篇 · 共7篇 ----------
chapter(1865, "05 · 这只是第5篇 · 共7篇")
band_y = 1935
box(40, band_y, W - 80, 385, r=18)
put("你现在读的是《基本态势》系列第5篇 · 共7篇", font(16, True), (W / 2, band_y + 40), color=GOLD)
put("这个系列帮你从零建立深圳中考的完整认知", font(13), (W / 2, band_y + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？",
    "2026年数据复盘：给2027届的5个启示",
    "一张图看懂竞争格局",
    "8年考生人数翻倍：深度拆解",
    "52%录取率背后的3个真相（本篇）",
    "深圳中考全部出路可视化",
    "2027届考生备考时间线",
]
sy = band_y + 110
for i, s in enumerate(series, 1):
    put(f"0{i}  {s}", font(14), (76, sy), anchor="lm", color=WHITE)
    put(f"0{i}", font(14, True), (76, sy), anchor="lm", color=GOLD)
    sy += 34
put("建议按顺序读 · 第6篇：把普高/中职/3+4/3+2全部出路画成一张图。",
    font(14, True), (W / 2, band_y + 360), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = band_y + 430
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 36), color=WHITE)
put("数据不可怕，可怕的是只看到数据的一半。", font(16), (W / 2, divy + 76), color=LIGHT)
put("2027最新政策发布 · HSEE第一时间更新", font(14), (W / 2, divy + 114), color=SUB)
put("打开HSEE小程序 · 查各校录取率 / 普高学位 / 3+4·3+2专业名单", font(13), (W / 2, divy + 146), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 188), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-5-录取率解读/01-公众号/05-S1-5-公办普高52%录取率意味着什么？2027届家长该知道的3个真相-公众号-长图-极简版.png"
img.save(out)
print("saved", out, img.size)

# ---------- 校验 ----------
bad = 0; bxs = []
for (text, fnt, (cx, cy), anchor, color, maxw) in checks:
    bbox = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
    x0, y0 = bbox[0] + cx, bbox[1] + cy
    x1, y1 = bbox[2] + cx, bbox[3] + cy
    w = x1 - x0
    bxs.append(((x0, y0, x1, y1), text, (cx, cy)))
    ok = (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1)
    if maxw and w > maxw + 2: ok = False
    if not ok:
        bad += 1
        print(f"OVERFLOW [{text[:20]}] x=({x0:.0f},{x1:.0f}) y=({y0:.0f},{y1:.0f}) maxw={maxw}")
print("OVERFLOW:", "PASS" if bad == 0 else f"FAIL {bad}")
ov = 0
for i in range(len(bxs)):
    for j in range(i + 1, len(bxs)):
        (ax0, ay0, ax1, ay1), at, ac = bxs[i]
        (bx0, by0, bx1, by1), bt, bc = bxs[j]
        if ac == bc:
            continue
        ox = max(0, min(ax1, bx1) - max(ax0, bx0))
        oy = max(0, min(ay1, by1) - max(ay0, by0))
        if ox > 4 and oy > 4:
            ov += 1
            print(f"OVERLAP: [{at[:14]}] x [{bt[:14]}]")
print("OVERLAP:", "PASS" if ov == 0 else f"FAIL {ov}")

# ---------- 采样：渐变 + 章节金竖条 + 数字卡 ----------
arr2 = np.array(img)
col = arr2[:, 899, :].astype(int)
mono = all(col[y][0] >= col[y + 1][0] and col[y][2] >= col[y + 1][2] for y in range(0, H - 1, 200))
print("GRADIENT MONOTONE:", "PASS" if mono else "FAIL")
for cy, lbl in [(208, "ch01"), (595, "ch02"), (1060, "ch03")]:
    print(f"GOLDBAR {lbl} @({54},{cy}):", arr2[cy, 54, :].tolist())
print("CARD1 num @(170,335):", arr2[335, 170, :].tolist(), "CARD3 num @(730,335):", arr2[335, 730, :].tolist())
