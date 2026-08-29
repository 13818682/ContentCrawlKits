# -*- coding: utf-8 -*-
"""S1-4 极简版 · 统一长图（风格同 S1-1/2/3：金竖条章节头/行盒/系列钩子卡，连续渐变）
内容：翻倍数字卡 + 金色柱状时间线(2018-2027) + 三引擎/学位/见顶行盒 + 对号入座 + 系列第4篇钩子"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 3490
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
put("深圳中考 · S1 基本态势 · 系列第4篇", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("8年考生人数翻倍：2027年你的孩子和多少人竞争？", FBD, (50, 74), anchor="lm", color=WHITE)
put("7.21万 → 约16-18万 · 翻倍的数字最吓人，看懂背后的逻辑才值钱", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 关键数字卡 ----------
chapter(208, "01 · 先记两件事：翻倍，但录取率在恢复")
card_specs = [
    (40, "16-18万", "2027年预计考生", "8年翻倍：7.21万 → 16-18万 · 2026年为15.30万"),
    (480, "52%", "公办普高录取率(2026)", "2020年最低仅44% · 学位在追着考生跑"),
]
for x, num, lab, note in card_specs:
    box(x, 275, 380, 200)
    put(num, font(42, True), (x + 190, 275 + 60), color=GOLD)
    put(lab, font(17, True), (x + 190, 275 + 118), color=WHITE)
    put(note, font(13), (x + 190, 275 + 154), color=SUB, maxw=340)
takeaway(520, "这意味着什么：考生在涨，但录取率没崩——学位在追着考生跑。")

# ---------- 02 金色柱状时间线 ----------
chapter(575, "02 · 8年翻倍的时间线")
basey = 900
d.line([90, basey, 810, basey], fill=EDGE, width=2)
bars = [
    (130, 7.21, "2018"), (260, 8.92, "2020"), (390, 11.2, "2022"),
    (520, 13.52, "2024"), (650, 15.30, "2026"), (780, 17.0, "2027"),
]
for cx, val, yr in bars:
    h = val / 18.0 * 380
    color = GOLD if yr == "2027" else LIGHT
    d.rectangle([cx - 40, basey - h, cx + 40, basey], fill=color)
    vlab = "16-18万" if yr == "2027" else str(val)
    put(vlab, font(14, True), (cx, basey - h - 16), anchor="mm", color=GOLD if yr == "2027" else WHITE)
    put(yr + ("E" if yr == "2027" else ""), font(13), (cx, basey + 26), anchor="mm", color=LIGHT)
put("考生人数（万人）· 2027为线性推估 · 待初中入学数据确认", font(13), (W / 2, basey + 62), color=SUB)
takeaway(1015, "这意味着什么：“16-18万”不是拍脑袋，是8年数据支撑的趋势外推。")

# ---------- 03 三个引擎 ----------
chapter(1070, "03 · 增长靠三个引擎")
rows_03 = [
    ("① 人口净流入", "常住人口 约1,300万 → 1,824.85万 · 7年净增约500万，2025年净增25.90万已放缓", GOLD),
    ("② 出生人口高峰", "2016年出生1,786万达峰 · 2014-2016次高峰对应2029-2031年还有一波", LIGHT),
    ("③ 初中→中考高转化率", "稳定95%-97% · 2024初中入学人数 ≈ 2027中考人数预测", LIGHT),
]
ry = 1135
for tag, detail, tc in rows_03:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1470, "这意味着什么：三个引擎里，前两个都在减速——趋势在转。")

# ---------- 04 学位在追着考生跑 ----------
chapter(1525, "04 · 学位在追着考生跑")
rows_04 = [
    ("公办普高招生", "约5.9万 → 8万 · 增长约35% · 101所学校", GOLD),
    ("两轮大建设", "十四五：49所新改扩建 + 11.8万学位 · 十五五：再增10万学位", LIGHT),
]
ry4 = 1590
for tag, detail, tc in rows_04:
    row(ry4, tag, detail, tc)
    ry4 += 110
takeaway(1835, "这意味着什么：考生翻倍、学位涨35%、录取率却稳在52%——不是奇迹，是规划。")

# ---------- 05 何时见顶 ----------
chapter(1890, "05 · 何时见顶？2027-2030")
rows_05 = [
    ("信号一 · 出生人口拐点", "2016年1,786万出生达峰后持续下降 · 2031年前后压力开始缓解", GOLD),
    ("信号二 · 流入减速", "深圳2025净增25.90万人仍全国第一 · 但已从年增40-50万回落", LIGHT),
    ("信号三 · 十五五窗口", "2026-2030再增10万学位 · 恰好覆盖考生峰值区间", LIGHT),
]
ry5 = 1955
for tag, detail, tc in rows_05:
    row(ry5, tag, detail, tc)
    ry5 += 110
takeaway(2290, "这意味着什么：你现在经历的，可能就是最难的时候——但这是拐点前的冲刺。")

# ---------- 06 对号入座 ----------
chapter(2345, "06 · 这些数据，对你意味着什么？")
rows_06 = [
    ("2027届考生", "正处人数高位 · 别恐慌，用数据精准定位孩子的竞争位置", GOLD),
    ("2028届及以后", "下降曙光 · 但四大/八大是存量博弈，顶尖层竞争不缓解", GOLD),
    ("初二家长观望", "2027数据是你最好的预测工具 · 早准备一年，判断力早成熟一年", LIGHT),
]
ry6 = 2410
for tag, detail, tc in rows_06:
    row(ry6, tag, detail, tc)
    ry6 += 110

# ---------- 07 系列第4篇 · 共7篇 ----------
chapter(2795, "07 · 这只是第4篇 · 共7篇")
band_y = 2865
box(40, band_y, W - 80, 385, r=18)
put("你现在读的是《基本态势》系列第4篇 · 共7篇", font(16, True), (W / 2, band_y + 40), color=GOLD)
put("这个系列帮你从零建立深圳中考的完整认知", font(13), (W / 2, band_y + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？",
    "2026年数据复盘：给2027届的5个启示",
    "一张图看懂竞争格局",
    "8年考生人数翻倍：深度拆解（本篇）",
    "52%录取率背后的3个真相",
    "深圳中考全部出路可视化",
    "2027届考生备考时间线",
]
sy = band_y + 110
for i, s in enumerate(series, 1):
    put(f"0{i}  {s}", font(14), (76, sy), anchor="lm", color=WHITE)
    put(f"0{i}", font(14, True), (76, sy), anchor="lm", color=GOLD)
    sy += 34
put("建议按顺序读 · 第5篇：52%录取率背后的3个真相——稳在哪里，松在哪里。",
    font(14, True), (W / 2, band_y + 360), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = band_y + 430
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 36), color=WHITE)
put("压力虽在高位，但方向在好转——读懂趋势，比记住数字更重要。", font(16), (W / 2, divy + 76), color=LIGHT)
put("2027最新政策发布 · HSEE第一时间更新", font(14), (W / 2, divy + 114), color=SUB)
put("打开HSEE小程序 · 查历年考生人数 / 录取率走势 / 各校分数线", font(13), (W / 2, divy + 146), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 188), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-4-考生人数翻倍/01-公众号/05-S1-4-深圳中考8年考生人数翻倍：2027年你的孩子和多少人竞争？-公众号-长图-极简版.png"
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

# ---------- 采样：渐变 + 章节金竖条 + 柱图 ----------
arr2 = np.array(img)
col = arr2[:, 899, :].astype(int)
mono = all(col[y][0] >= col[y + 1][0] and col[y][2] >= col[y + 1][2] for y in range(0, H - 1, 200))
print("GRADIENT MONOTONE:", "PASS" if mono else "FAIL")
for cy, lbl in [(208, "ch01"), (575, "ch02"), (1070, "ch03")]:
    print(f"GOLDBAR {lbl} @({54},{cy}):", arr2[cy, 54, :].tolist())
print("BAR2027 @(780,760):", arr2[760, 780, :].tolist(), "BAR2018 @(130,820):", arr2[820, 130, :].tolist())
