# -*- coding: utf-8 -*-
"""S1-7 极简版 · 统一长图（风格同 S1-5/6：金竖条章节头/行盒/系列钩子卡，连续渐变）
内容：5阶段速查表 + 现在就开始3件事 + 家长vs孩子 + 对号入座 + 系列第7篇收官钩子"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 2760
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:                       # 正文文字统一放大1.35倍，展示大字不受影响
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

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
    put(detail, font(14), (76, ry + 64), anchor="lm", color=WHITE, maxw=700)

def takeaway(ty, txt):
    put(txt, font(15, True), (W / 2, ty), color=GOLD, maxw=W - 80)

# ---------- 页眉 ----------
put("深圳中考 · S1 基本态势 · 系列第7篇·收官", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("2027届考生备考时间线", font(34, True), (50, 74), anchor="lm", color=WHITE)
put("9个月 · 5个阶段 · 每月该做什么一目了然 · 现在开始刚刚好", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 5阶段速查表 ----------
chapter(208, "01 · 9个月，5个阶段")
box(40, 275, W - 80, 360)
put("时间", font(15, True), (90, 302), anchor="mm", color=LIGHT)
put("关键动作", font(15, True), (380, 302), anchor="mm", color=LIGHT)
put("关键节点", font(15, True), (680, 302), anchor="mm", color=LIGHT)
d.line([80, 320, 820, 320], fill=GOLD, width=2)
rows = [
    ("8-9月（现在）", "建立认知框架", "体育过程性评价·14分开始"),
    ("10-12月", "研究指标生+目标学校", "11月期中定位"),
    ("1-3月", "一模定位+政策跟踪", "3月下旬中考报名"),
    ("4-5月", "志愿草拟+最终方案", "志愿填报（10天）"),
    ("6-8月", "中考+录取", "录取公布+高一衔接"),
]
ry = 352
for a, b, c in rows:
    put(a, font(15, True), (90, ry), anchor="mm", color=GOLD)
    put(b, font(14), (380, ry), anchor="mm", color=WHITE)
    put(c, font(14), (680, ry), anchor="mm", color=WHITE)
    ry += 56
takeaway(690, "这意味着什么：关键决策集中在4-5月，前8个月都是信息储备——谁准备得早，谁填志愿不慌。")

# ---------- 02 现在就要开始的3件事 ----------
chapter(745, "02 · 现在就要开始的3件事")
rows_02 = [
    ("① 体育过程性评价", "前两年已入账 · 初三这一年14分从现在累积 · 早练早拿分", GOLD),
    ("② 理化实验操作", "计入总分（630分制）· 不是走过场", LIGHT),
    ("③ 收集学校信息", "30分钟搞懂三组数字 · 弄清AC/D类 · 开始浏览目标学校", LIGHT),
]
ry = 810
for tag, detail, tc in rows_02:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1170, "这意味着什么：中考不只是孩子的事——家长的“信息准备”从今天就开始，也在拉开差距。")

# ---------- 03 家长 vs 孩子 ----------
chapter(1225, "03 · 家长 vs 孩子：两份答卷")
rows_03 = [
    ("孩子：拼分数", "新课→期中期末→一模→二模+体育中考→冲刺→中考", GOLD),
    ("家长：拼决策", "建认知框架→研究指标生→一模定位→草拟志愿→10天窗口内定稿→录取跟进", LIGHT),
]
ry = 1290
for tag, detail, tc in rows_03:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1540, "这意味着什么：孩子拼分数，家长拼决策——两份“试卷”都别交白卷。")

# ---------- 04 对号入座 ----------
chapter(1595, "04 · 对号入座")
rows_04 = [
    ("初三家长", "现在从“三组数字+指标生”开始 · 别等下学期", GOLD),
    ("D类家长", "提前备好社保、居住证等报名材料 · 3月下旬报名别卡壳", GOLD),
    ("初一初二家长", "收藏这篇 · 明年9月准时用 · 越早看越不慌", LIGHT),
]
ry = 1660
for tag, detail, tc in rows_04:
    row(ry, tag, detail, tc)
    ry += 110

# ---------- 05 系列第7篇 · 收官 ----------
chapter(2030, "05 · 系列收官 · 共7篇")
band_y = 2100
box(40, band_y, W - 80, 385, r=18)
put("你现在读的是《基本态势》系列第7篇·收官 · 共7篇", font(16, True), (W / 2, band_y + 40), color=GOLD)
put("7篇连起来，就是一张完整的深圳中考认知地图", font(13), (W / 2, band_y + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？",
    "2026年数据复盘：给2027届的5个启示",
    "一张图看懂竞争格局",
    "8年考生人数翻倍：深度拆解",
    "52%录取率背后的3个真相",
    "深圳中考全部出路可视化",
    "2027届考生备考时间线（本篇·收官）",
]
sy = band_y + 110
for i, s in enumerate(series, 1):
    put(f"0{i}  {s}", font(14), (76, sy), anchor="lm", color=WHITE)
    put(f"0{i}", font(14, True), (76, sy), anchor="lm", color=GOLD)
    sy += 34
put("建议从头按顺序读一遍 · 下一篇《政策解码器》继续拆指标生、自主招生。",
    font(14, True), (W / 2, band_y + 360), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = band_y + 430
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 36), color=WHITE)
put("中考拼的不只是分数，还有家庭的决策节奏。", font(16), (W / 2, divy + 76), color=LIGHT)
put("2027政策发布 · HSEE第一时间更新", font(14), (W / 2, divy + 114), color=SUB)
put("打开HSEE小程序 · 查各校数据 / 指标生名额 / 历年分数线", font(13), (W / 2, divy + 146), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 188), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/01-公众号/05-S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-公众号-长图-极简版.png"
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
for cy, lbl in [(208, "ch01"), (745, "ch02"), (1225, "ch03")]:
    print(f"GOLDBAR {lbl} @({54},{cy}):", arr2[cy, 54, :].tolist())
print("TABLE col1 @(90,400):", arr2[400, 90, :].tolist(), "TABLE col3 @(680,400):", arr2[400, 680, :].tolist())
