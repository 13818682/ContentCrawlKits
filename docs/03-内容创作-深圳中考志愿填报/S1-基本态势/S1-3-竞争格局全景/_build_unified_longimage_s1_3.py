# -*- coding: utf-8 -*-
"""S1-3 极简版 · 统一长图 v2（补承前启后"这意味着什么" + 系列第3篇·共7篇钩子）
风格：参照插图合集（金竖条章节头/三数字卡/金色柱对比/三层/对号入座），连续渐变无拼接缝。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 2690
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

# 连续渐变背景
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

def chapter(ty, txt):  # 插图章节条风格
    d.rectangle([50, ty - 27, 58, ty + 27], fill=GOLD)
    put(txt, font(36, True), (78, ty), anchor="lm", color=WHITE)
    d.line([50, ty + 45, 140, ty + 45], fill=GOLD, width=3)

# ---------- 页眉 ----------
put("深圳中考 · S1 基本态势 · 竞争格局", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("2027深圳中考竞争格局", FBD, (50, 74), anchor="lm", color=WHITE)
put("家长必读 · 一张图看懂 · 1分钟读完", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 三组数字 ----------
chapter(208, "01 · 先记三组数字")
box_data = [
    ("16-18万", "2027预计考生", "2026年为15.30万"),
    ("约8万", "2026公办学位", "101所·年增约6千"),
    ("52%", "公办录取率", "多年稳定"),
]
for i, (num, lab, note) in enumerate(box_data):
    x = 40 + i * 280
    box(x, 283, 260, 220)
    put(num, font(42, True), (x + 130, 283 + 66), color=GOLD)
    put(lab, font(17, True), (x + 130, 283 + 124), color=WHITE)
    put(note, font(13), (x + 130, 283 + 162), color=SUB)

# ---------- 02 8年翻倍（金色柱对比）----------
chapter(545, "02 · 8年翻倍，学位在追着跑")
band_x, band_y, band_w, band_h = 40, 617, 820, 285
box(band_x, band_y, band_w, band_h, r=18)
baseline = band_y + 235; maxh = 150
def bh(v): return maxh * v / 15.30
gx_18, gx_26 = 260, 640; bw = 64
def bar(cx, val, col):
    top = baseline - bh(val)
    d.rounded_rectangle([cx - bw // 2, top, cx + bw // 2, baseline], radius=6, fill=col)
    put(f"{val}万", font(15, True), (cx, top - 14), color=(GOLD if col == GOLD else LIGHT))
put("2018", font(20, True), (gx_18, band_y + 38), color=WHITE)
bar(gx_18 - 40, 7.21, GOLD); bar(gx_18 + 40, 5.9, LIGHT)
put("2026", font(20, True), (gx_26, band_y + 38), color=WHITE)
bar(gx_26 - 40, 15.30, GOLD); bar(gx_26 + 40, 8.0, LIGHT)
put("■ 考生  (金)    ■ 公办学位  (浅蓝)", font(13), (band_x + band_w / 2, band_y + 46), color=SUB)
put("录取率稳在52% · 学位建设追着考生跑", font(15, True), (band_x + band_w / 2, band_y + 258), color=GOLD)
put("“十四五”新增11.8万学位 · “十五五”(2026-2030)再增10万", font(14), (W / 2, band_y + band_h + 26), color=SUB)
put("这意味着什么：孩子正处在压力最大的几年，但学位在同步加码，方向在变好。",
    font(15, True), (W / 2, band_y + band_h + 62), color=GOLD, maxw=W - 80)

# ---------- 03 出路全景 ----------
chapter(1002, "03 · 出路全景：不是“一半没书读”")
rows3 = [
    ("公办普高", "约8万 · 101所", "约52%的孩子能上"),
    ("民办普高", "33,195人 · 49所", "加上公办，超73%能上普高"),
    ("中职及技工", "33,254人 · 30所", "3+4中本贯通 · 中职直升本科"),
]
ry = 1072
for name, cnt, note in rows3:
    box(40, ry, W - 80, 90)
    put(name, font(18, True), (76, ry + 32), anchor="lm", color=GOLD)
    put(cnt, font(18, True), (76, ry + 66), anchor="lm", color=WHITE)
    put(note, font(14), (W - 76, ry + 46), anchor="rm", color=SUB)
    ry += 90 + 15
put("总学位 146,752 = 覆盖全部 15.30万考生", font(16, True), (W / 2, ry + 2), color=GOLD)
put("这意味着什么：“一半人没书读”是误传——孩子不是在被淘汰，而是在被选择。",
    font(15, True), (W / 2, ry + 38), color=GOLD, maxw=W - 80)

# ---------- 04 这些数据，对你意味着什么 ----------
chapter(1476, "04 · 这些数据，对你意味着什么？")
rows4 = [
    ("非深户(D类)", "公办指标仅占约23%，但指标生已实现全覆盖", "路窄，不是死胡同"),
    ("成绩400分左右", "别只盯公办——3+4中本贯通是最新窗口", "很多家长还不知道"),
    ("初二家长", "时间就是优势，规则+数据现在就开始准备", "早准备一年，焦虑少一半"),
]
ry4 = 1546
for tag, l1, l2 in rows4:
    box(40, ry4, W - 80, 100)
    put(tag, font(17, True), (76, ry4 + 32), anchor="lm", color=GOLD)
    put(l1, font(14), (76, ry4 + 66), anchor="lm", color=WHITE, maxw=600)
    put(l2, font(16, True), (W - 76, ry4 + 50), anchor="rm", color=GOLD)
    ry4 += 100 + 15
put("你属于哪一类，就带走哪一句话 · 具体怎么做，答案在后面几篇文章里。",
    font(14, True), (W / 2, ry4 + 4), color=LIGHT, maxw=W - 80)

# ---------- 05 系列第3篇 · 共7篇 钩子 ----------
chapter(1954, "05 · 这只是第3篇 · 共7篇")
band_y5 = 2024
box(40, band_y5, W - 80, 372, r=18)
put("你现在读的是《基本态势》系列第3篇 · 共7篇", font(16, True), (W / 2, band_y5 + 40), color=GOLD)
put("这个系列帮你从零建立深圳中考的完整认知", font(13), (W / 2, band_y5 + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？",
    "2026年数据复盘：给2027届的5个启示",
    "一张图看懂竞争格局（你正在读的这篇）",
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
put("建议按顺序读 · 第4篇：考生为什么8年翻了一倍？还会持续多久？",
    font(14, True), (W / 2, sy + 4), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = sy + 56
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 40), color=WHITE)
put("竞争存在，但方向在好转。", font(16), (W / 2, divy + 82), color=LIGHT)
put("2027最新数据发布 · HSEE第一时间更新", font(14), (W / 2, divy + 124), color=SUB)
put("打开HSEE小程序 · 历年数据透明、可查、可验证", font(13), (W / 2, divy + 158), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 204), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-3-竞争格局全景/01-公众号/08-S1-3-2027深圳中考家长必读：一张图看懂竞争格局-公众号-长图-极简版.png"
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
        if ac == bc:  # 同锚点叠绘（金色编号叠在白色编号上）为有意设计
            continue
        ox = max(0, min(ax1, bx1) - max(ax0, bx0))
        oy = max(0, min(ay1, by1) - max(ay0, by0))
        if ox > 4 and oy > 4:
            ov += 1
            print(f"OVERLAP: [{at[:14]}] x [{bt[:14]}]")
print("OVERLAP:", "PASS" if ov == 0 else f"FAIL {ov}")
