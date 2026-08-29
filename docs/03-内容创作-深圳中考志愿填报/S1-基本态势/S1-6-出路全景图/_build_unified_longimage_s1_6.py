# -*- coding: utf-8 -*-
"""S1-6 极简版 · 统一长图（风格同 S1-5：金竖条章节头/行盒/系列钩子卡，连续渐变）
内容：四数字卡(52%/33,195/33,254/146,752) + 三层出路行盒 + 两条曲线读大学 + 三条真相 + 对号入座 + 系列第6篇钩子"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 3140
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
put("深圳中考 · S1 基本态势 · 系列第6篇", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("深圳中考全部出路全景", font(34, True), (50, 74), anchor="lm", color=WHITE)
put("公办+民办+中职+中本贯通 · 146,752个学位 · 4层出路可选", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 四数字卡 ----------
chapter(208, "01 · 4 个数字，看清全貌")
card_specs = [
    (40, "约52%", "公办普高录取率", "约8万人 · 101所"),
    (250, "33,195", "民办普高招生", "49所 · 学费3万-15万"),
    (460, "33,254", "中职及技工招生", "30所 · 公办15,924+民办17,330"),
    (670, "146,752", "高中阶段总学位", "180所 · 覆盖全部考生"),
]
for x, num, lab, note in card_specs:
    box(x, 275, 190, 220)
    put(num, font(36, True), (x + 95, 275 + 55), color=GOLD)
    put(lab, font(15, True), (x + 95, 275 + 108), color=WHITE)
    put(note, font(12), (x + 95, 275 + 150), color=SUB, maxw=175)
takeaway(540, "这意味着什么：学位几乎人人够得着——关键不是有没有学上，而是为孩子选对哪条路。")

# ---------- 02 三层出路 ----------
chapter(600, "02 · 三层出路，每层都有价值")
rows_02 = [
    ("公办普高 · 约52%", "约8万人 · 101所 · AC类61,797 · D类18,506（约23%）· 2026新增7所", GOLD),
    ("民办普高", "33,195人 · 49所 · 学费3万-15万/年 · AC/D类同分录取", LIGHT),
    ("中职及技工", "33,254人 · 30所 · 公办15,924 + 民办17,330 · 两条曲线读大学", LIGHT),
]
ry = 665
for tag, detail, tc in rows_02:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1000, "这意味着什么：三层都能通向好出路，中职尤其被低估。")

# ---------- 03 两条曲线读大学 ----------
chapter(1060, "03 · 两条“曲线读大学”的路")
rows_03 = [
    ("3+4 中本贯通", "300名额 · 中职3年→本科4年→全日制本科 · 一职对口深技大 · 二职对口深职大", GOLD),
    ("3+2 中高贯通", "2,853人 · 63专业 · 中职3年→高职2年 · 低分段被低估的选项", LIGHT),
]
ry = 1125
for tag, detail, tc in rows_03:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1370, "这意味着什么：中职≠没出路，这两条路知道的人还不多。")

# ---------- 04 三条真相 ----------
chapter(1430, "04 · 三个被忽略的真相")
rows_04 = [
    ("真相一 · 普高率超73%", "公办8万+民办33,195=113,498个普高学位 · “一半人没高中读”是误解", GOLD),
    ("真相二 · 民办对D类一视同仁", "公办D类仅约23% · 民办对AC/D同分录取 · D类家长的重要补充", LIGHT),
    ("真相三 · 中职非死胡同", "3+4拿全日制本科文凭 · 和高考考上的本科一样", LIGHT),
]
ry = 1495
for tag, detail, tc in rows_04:
    row(ry, tag, detail, tc)
    ry += 110
takeaway(1830, "这意味着什么：出路比你想象的宽——但信息差，决定孩子去哪条路。")

# ---------- 05 对号入座 ----------
chapter(1890, "05 · 对号入座")
rows_05 = [
    ("公办线以上", "主攻公办 · 民办作保底别忽略", GOLD),
    ("公办线边缘", "公办+民办+中本贯通 · 三条腿走路", GOLD),
    ("D类考生", "民办和中职路径 · 更早了解更主动", LIGHT),
    ("低分段", "3+4 / 3+2 / 优质民办 · 正经出路", LIGHT),
]
ry = 1955
for tag, detail, tc in rows_05:
    row(ry, tag, detail, tc)
    ry += 110

# ---------- 06 系列第6篇 · 共7篇 ----------
chapter(2410, "06 · 这只是第6篇 · 共7篇")
band_y = 2480
box(40, band_y, W - 80, 385, r=18)
put("你现在读的是《基本态势》系列第6篇 · 共7篇", font(16, True), (W / 2, band_y + 40), color=GOLD)
put("这个系列帮你从零建立深圳中考的完整认知", font(13), (W / 2, band_y + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？",
    "2026年数据复盘：给2027届的5个启示",
    "一张图看懂竞争格局",
    "8年考生人数翻倍：深度拆解",
    "52%录取率背后的3个真相",
    "深圳中考全部出路可视化（本篇）",
    "2027届考生备考时间线",
]
sy = band_y + 110
for i, s in enumerate(series, 1):
    put(f"0{i}  {s}", font(14), (76, sy), anchor="lm", color=WHITE)
    put(f"0{i}", font(14, True), (76, sy), anchor="lm", color=GOLD)
    sy += 34
put("建议按顺序读 · 第7篇（收官）：初三一年每个月该做什么，一目了然。",
    font(14, True), (W / 2, band_y + 360), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = band_y + 430
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 36), color=WHITE)
put("出路不止公办一条——孩子值得看到全部地图。", font(16), (W / 2, divy + 76), color=LIGHT)
put("2027最新招生计划发布 · HSEE第一时间更新", font(14), (W / 2, divy + 114), color=SUB)
put("打开HSEE小程序 · 查各校招生 / AC·D线 / 3+4·3+2专业名单", font(13), (W / 2, divy + 146), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 188), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-6-出路全景图/01-公众号/05-S1-6-一张图看懂深圳中考全部出路-公众号-长图-极简版.png"
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
for cy, lbl in [(208, "ch01"), (600, "ch02"), (1060, "ch03")]:
    print(f"GOLDBAR {lbl} @({54},{cy}):", arr2[cy, 54, :].tolist())
print("CARD1 num @(135,330):", arr2[330, 135, :].tolist(), "CARD4 num @(765,330):", arr2[330, 765, :].tolist())
