# -*- coding: utf-8 -*-
"""S1-1 极简版 · 统一长图（风格同 S1-3：金竖条章节头/三数字卡/行盒/系列钩子卡，连续渐变）"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 2200
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

# ---------- 页眉 ----------
put("深圳中考 · S1 基本态势 · 系列第1篇", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("2027届家长，现在该做什么？", FBD, (50, 74), anchor="lm", color=WHITE)
put("中考填志愿只有10天 · 现在开始，多9个月信息优势", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 三组数字 ----------
chapter(208, "01 · 先记三组数字")
box_data = [
    ("16-18万", "2027预计考生", "2026年为15.30万"),
    ("约8万", "公办普高招生", "101所学校"),
    ("约52%", "公办录取率", "含民办超73%"),
]
for i, (num, lab, note) in enumerate(box_data):
    x = 40 + i * 280
    box(x, 283, 260, 220)
    put(num, font(42, True), (x + 130, 283 + 66), color=GOLD)
    put(lab, font(17, True), (x + 130, 283 + 124), color=WHITE)
    put(note, font(13), (x + 130, 283 + 162), color=SUB)
put("这意味着什么：记住这3个数字，再看任何信息都不会慌。",
    font(15, True), (W / 2, 540), color=GOLD, maxw=W - 80)

# ---------- 02 现在该做的3件事 ----------
chapter(575, "02 · 现在该做的3件事")
rows_do = [
    ("① 5分钟记住三组数字", "16-18万考生 · 8万学位 · 52%录取率，HSEE可查完整可视化"),
    ("② 2026数据当教材预习", "看分数线涨跌、认识四大八大；D类家长先研究指标生降分通道"),
    ("③ 关注体育过程性评价", "14分从初一累积；确认历史分，规划初三耐力/技能/球类训练"),
]
ry = 645
for tag, detail in rows_do:
    row(ry, tag, detail, GOLD)
    ry += 95 + 15
put("这意味着什么：这三件事今天就能做 · 先搭框架，5月填志愿就是往里填数据。",
    font(15, True), (W / 2, ry + 2), color=GOLD, maxw=W - 80)

# ---------- 03 现在不必焦虑的3件事 ----------
chapter(1030, "03 · 现在不必焦虑的3件事")
rows_no = [
    ("① 志愿怎么填？", "2027年5月的事，现在只需搭认知框架，到时候往里填数据"),
    ("② 分数够不够？", "离中考还有约300天，一模成绩才作数，别拿初二分数对标中考线"),
    ("③ 政策会不会变？", "会变，变了HSEE第一时间更新；630总分/16志愿框架大概率延续"),
]
ry3 = 1100
for tag, detail in rows_no:
    row(ry3, tag, detail, LIGHT)
    ry3 += 95 + 15
put("这意味着什么：焦虑来自信息差 · 行动，是缩小信息差最好的方式。",
    font(15, True), (W / 2, ry3 + 2), color=GOLD, maxw=W - 80)

# ---------- 04 系列第1篇 · 共7篇 ----------
chapter(1485, "04 · 这只是第1篇 · 共7篇")
band_y5 = 1555
box(40, band_y5, W - 80, 372, r=18)
put("你现在读的是《基本态势》系列第1篇 · 共7篇", font(16, True), (W / 2, band_y5 + 40), color=GOLD)
put("这个系列帮你从零建立深圳中考的完整认知", font(13), (W / 2, band_y5 + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？（本篇）",
    "2026年数据复盘：给2027届的5个启示",
    "一张图看懂竞争格局",
    "8年考生人数翻倍：深度拆解",
    "52%录取率背后的3个真相",
    "深圳中考全部出路可视化",
    "2027届考生备考时间线",
]
sy = band_y5 + 110
for i, s in enumerate(series, 1):
    put(f"0{i}  {s}", font(14), (76, sy), anchor="lm", color=WHITE)
    put(f"0{i}", font(14, True), (76, sy), anchor="lm", color=GOLD)
    sy += 34
put("建议按顺序读 · 第2篇：用2026年真实录取数据，讲清最该盯的5个变化。",
    font(14, True), (W / 2, sy + 4), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = sy + 56
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 40), color=WHITE)
put("中考考的不是孩子，是家庭的信息获取和决策能力。", font(16), (W / 2, divy + 82), color=LIGHT)
put("2027最新政策发布 · HSEE第一时间更新", font(14), (W / 2, divy + 124), color=SUB)
put("打开HSEE小程序 · 查录取数据 / 历年分数线 / 指标生名额", font(13), (W / 2, divy + 158), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 204), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-1-启点-现在做什么/01-公众号/06-S1-1-2026年深圳中考已结束，2027届家长现在该做什么？-公众号-长图-极简版.png"
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
