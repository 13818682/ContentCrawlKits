# -*- coding: utf-8 -*-
"""QA-003 小红书图文配图（6张：首图 + 正文图1-5，全部 1080×1440 · 3:4）
一卡一个信息点；序号与文字块共中线（block2_lm）；正文文字≥1.5倍；框内留白/框间距达标。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
WARN = (245, 156, 96)
FD = "C:/Windows/Fonts/"

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/003+中考滑档去了深圳排名40左右的高中怎么办？/03.小红书/02.图文/"
N = "01-QA-003-中考滑档去了深圳排名40左右的高中怎么办-小红书"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 20:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    ck.append((text, fnt, xy, anchor))
    return fnt


def verify(d, ck, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} @({cx},{cy})")
    print(f"{name}: 共{len(ck)}处文字，{bad}处越界")
    return bad == 0


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=24, width=2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)


def block2_lm(d, ck, x, cy, title, sub, tf, sf, maxw=760, tc=WHITE, sc=LIGHT):
    tb = d.textbbox((0, 0), title, font=tf, anchor="lm")
    sb = d.textbbox((0, 0), sub, font=sf, anchor="lm")
    th, sh = tb[3] - tb[1], sb[3] - sb[1]
    gap = 10
    total = th + gap + sh
    ty = cy - total / 2 + th / 2
    sy = cy + total / 2 - sh / 2
    put(d, ck, title, tf, (x, ty), anchor="lm", color=tc, maxw=maxw)
    put(d, ck, sub, sf, (x, sy), anchor="lm", color=sc, maxw=maxw)


def new_canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.5:
            k = p / 0.5
            col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.5) / 0.5
            col = c_mid * (1 - k) + c_bot * k
        base[y, :, :] = col
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.62 + 0.38 * diag)
    spots = [
        ((0.80, 0.14), (150, 200, 240)),
        ((0.20, 0.20), (120, 180, 235)),
        ((0.74, 0.74), (95, 160, 225)),
        ((0.28, 0.86), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]
    col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    g = np.exp(-dist * dist) * 0.30
    base += col[None, None, :] * g[:, :, None]
    base = np.clip(base, 0, 255)
    img = Image.fromarray(base.astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


def save(img, fn):
    img.save(BASE + fn)
    print("已保存:", fn)


results = {}

# ================= 1. 首图（封面）=================
img, d = new_canvas(0); ck = []
put(d, ck, "深圳中考 · 问答专区", font(28, True), (540, 100), color=GOLD)
put(d, ck, "滑档去了排名40的高中？", font(62, True), (540, 250), color=WHITE, maxw=1000)
put(d, ck, "不叫滑档", font(130, True), (540, 510), color=GOLD, maxw=980)
put(d, ck, "多半是志愿没填好", font(38), (540, 650), color=LIGHT, maxw=1000)
chip_w, chip_h, chip_gap = 460, 100, 36
cx0 = (W - (2 * chip_w + chip_gap)) // 2
cy0 = 790
for i, (lab, num) in enumerate([("第40名录取线", "557分"), ("第35-45名区间", "553-561")]):
    cx = cx0 + i * (chip_w + chip_gap)
    box(d, cx, cy0, chip_w, chip_h, r=22)
    put(d, ck, lab, font(28), (cx + 90, cy0 + chip_h // 2), color=WHITE)
    put(d, ck, num, font(34, True), (cx + 150 + 80, cy0 + chip_h // 2), color=GOLD)
put(d, ck, "两条路：接受并规划 · 或复读（慎选）", font(30), (540, 1040), color=LIGHT, maxw=1000)
d.rounded_rectangle([220, 1150, 860, 1280], radius=60, fill=GOLD)
put(d, ck, "收藏这张 · 慢慢对照", font(40, True), (540, 1215), color=NAVY)
put(d, ck, "孩子负责学习好 · 家长负责决策优", font(28, True), (540, 1380), color=GOLD, maxw=1000)
results["cover"] = verify(d, ck, "1 首图")
save(img, N + "-首图-1080x1440.png")

# ================= 2. 正文图1 · 不叫滑档 =================
img, d = new_canvas(1); ck = []
put(d, ck, "先分清 · 你是不是真滑档", font(34, True), (540, 100), color=GOLD)
put(d, ck, "你多半不是滑档", font(52, True), (540, 215), color=WHITE, maxw=1020)
rows = [
    ("真滑档", "第一批志愿全没接住", "才需要补救", SUB),
    ("冲档落空", "冲太高 · 落到稳/保志愿", "你的情况", GOLD),
]
y0, rh, rg = 330, 190, 28
for i, (t, s, tag, tc) in enumerate(rows):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, t, font(44, True), (200, cy), color=tc, maxw=240)
    put(d, ck, s, font(34), (430, cy), color=WHITE, maxw=420)
    put(d, ck, tag, font(28, True), (820, cy), color=tc, maxw=200)
box(d, 60, 790, 960, 220, r=24)
put(d, ck, "问题不在孩子分数", font(40, True), (540, 880), color=GOLD, maxw=920)
put(d, ck, "在志愿梯度没拉开 · 出分前就该填对", font(32), (540, 950), color=LIGHT, maxw=920)
put(d, ck, "下一张：排名40，到底什么水平？", font(26), (540, 1360), color=SUB)
results["slide"] = verify(d, ck, "2 不叫滑档")
save(img, N + "-正文图1-不叫滑档-1080x1440.png")

# ================= 3. 正文图2 · 排名40区间 =================
img, d = new_canvas(2); ck = []
put(d, ck, "排名40 · 到底什么水平", font(34, True), (540, 100), color=GOLD)
put(d, ck, "2026录取线 · AC类住宿", font(52, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 330, 960, 220, r=24)
put(d, ck, "第40名 · 深高创新高中", font(36, True), (540, 410), color=WHITE, maxw=920)
put(d, ck, "557分", font(90, True), (540, 510), color=GOLD, maxw=900)
box(d, 60, 600, 960, 180, r=24)
put(d, ck, "第35-45名区间", font(32, True), (330, 660), color=WHITE, maxw=380)
put(d, ck, "553-561分", font(44, True), (740, 660), color=GOLD, maxw=400)
put(d, ck, "第一批中后段公办普高 · 师资不差 · 高考出口正常", font(32, True), (540, 880), color=GOLD, maxw=1020)
put(d, ck, "滑档 ≠ 人生完蛋", font(42, True), (540, 970), color=WHITE, maxw=1020)
put(d, ck, "下一张：你只有两条路", font(26), (540, 1360), color=SUB)
results["rank"] = verify(d, ck, "3 排名40区间")
save(img, N + "-正文图2-排名40区间-1080x1440.png")

# ================= 4. 正文图3 · 两条路 =================
img, d = new_canvas(3); ck = []
put(d, ck, "你只有两条路", font(34, True), (540, 100), color=GOLD)
put(d, ck, "补录跟你没关系", font(52, True), (540, 215), color=WHITE, maxw=1020)
put(d, ck, "补录回的是民办普高 · 是降级不是补救", font(30), (540, 290), color=LIGHT, maxw=1020)
acts = [
    ("①", "接受并规划", "主路 · 想通排名40不差，把高中三年读好"),
    ("②", "复读（慎选）", "不能报指标生 · 不能参加自主招生"),
]
y0, rh, rg = 380, 220, 30
for i, (num, t, s) in enumerate(acts):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=24)
    cy = y + rh // 2
    put(d, ck, num, font(64, True), (140, cy), color=GOLD)
    block2_lm(d, ck, 230, cy, t, s, font(44, True), font(32), maxw=780)
put(d, ck, "复读值不值得 · 先过三关：失常？自愿？抗压？", font(30, True), (540, 950), color=GOLD, maxw=1020)
put(d, ck, "下一张：家长和孩子，分工不一样", font(26), (540, 1360), color=SUB)
results["paths"] = verify(d, ck, "4 两条路")
save(img, N + "-正文图3-两条路-1080x1440.png")

# ================= 5. 正文图4 · 分工论 =================
img, d = new_canvas(0); ck = []
put(d, ck, "中考 · 分工不一样", font(34, True), (540, 100), color=GOLD)
put(d, ck, "孩子学习好 · 家长决策优", font(52, True), (540, 215), color=WHITE, maxw=1020)
rows = [
    ("孩子", "负责学习好 · 把书读好、把试考好", GOLD),
    ("家长", "理解政策 · 研究数据 · 排好志愿梯度", GOLD),
]
y0, rh, rg = 330, 200, 28
for i, (t, s, tc) in enumerate(rows):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, t, font(46, True), (200, cy), color=tc, maxw=240)
    put(d, ck, s, font(32), (480, cy), color=WHITE, maxw=520)
box(d, 60, 790, 960, 220, r=24)
put(d, ck, "很多家庭输在这步", font(40, True), (540, 880), color=WARN, maxw=920)
put(d, ck, "不是孩子不努力 · 是家长没做功课", font(32), (540, 950), color=LIGHT, maxw=920)
put(d, ck, "下一张：现在该做什么", font(26), (540, 1360), color=SUB)
results["div"] = verify(d, ck, "5 分工论")
save(img, N + "-正文图4-分工论-1080x1440.png")

# ================= 6. 正文图5 · 现在该做什么 =================
img, d = new_canvas(1); ck = []
put(d, ck, "现在就能做 · 三件事", font(34, True), (540, 100), color=GOLD)
put(d, ck, "别等出分才发现", font(52, True), (540, 212), color=WHITE, maxw=1020)
acts = [
    ("①", "对号入座", "确认你是冲档落空——那就接受，这是志愿梯度正常运作"),
    ("②", "接受并规划", "查学校出口数据 · 特色班 · 升学路径，把高中三年规划好"),
    ("③", "转给明年中考的家庭", "把「政策 / 数据 / 志愿梯度」三件事提前告诉他们"),
]
y0, rh, rg = 320, 200, 28
for i, (num, t, s) in enumerate(acts):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, num, font(56, True), (140, cy), color=GOLD)
    block2_lm(d, ck, 230, cy, t, s, font(42, True), font(32), maxw=790)
put(d, ck, "孩子负责学习好 · 家长负责决策优 · 收藏这张清单", font(32, True), (540, 1380), color=GOLD, maxw=1020)
results["action"] = verify(d, ck, "6 行动三件事")
save(img, N + "-正文图5-现在该做什么-1080x1440.png")

print()
print("全部 OK =", all(results.values()))
