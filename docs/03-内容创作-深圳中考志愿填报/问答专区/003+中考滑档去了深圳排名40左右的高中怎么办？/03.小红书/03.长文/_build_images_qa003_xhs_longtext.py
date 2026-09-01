# -*- coding: utf-8 -*-
"""QA-003 小红书长文配图（2张竖版数据图，1080×1440 · 3:4）
长文文字复用今日头条长文，配图为轻量辅助。1. 数据速览 2. 给家长三句话。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
NAVY = (18, 30, 55)
FD = "C:/Windows/Fonts/"

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/003+中考滑档去了深圳排名40左右的高中怎么办？/03.小红书/03.长文/"
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


def block2_lm(d, ck, x, cy, title, sub, tf, sf, maxw=720, tc=WHITE, sc=LIGHT):
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

# ================= 1. 数据速览 =================
img, d = new_canvas(0); ck = []
put(d, ck, "滑档去排名40 · 关键数字速览", font(34, True), (540, 100), color=GOLD)
put(d, ck, "一条看懂这个结果", font(56, True), (540, 215), color=WHITE, maxw=1000)
stats = [
    ("不叫滑档", "多数是冲档落空 · 志愿没填好"),
    ("557分", "第40名录取线 · 深高创新"),
    ("553-561", "第35-45名区间"),
    ("两条路", "接受并规划 · 或复读"),
]
cw, ch, gap = 430, 250, 40
cx0 = (W - (2 * cw + gap)) // 2
cy0, cy1 = 340, 630
pos = [(cx0, cy0), (cx0 + cw + gap, cy0), (cx0, cy1), (cx0 + cw + gap, cy1)]
for (num, lab), (bx, by) in zip(stats, pos):
    box(d, bx, by, cw, ch, r=26)
    put(d, ck, num, font(66, True), (bx + cw // 2, by + 82), color=GOLD, maxw=380)
    put(d, ck, lab, font(28), (bx + cw // 2, by + 178), color=WHITE, maxw=380)
d.line([540 - 110, 950, 540 + 110, 950], fill=GOLD, width=4)
put(d, ck, "排名40 · 仍是第一批公办普高 · 高考出口不差", font(36, True), (540, 1052), color=GOLD, maxw=1000)
put(d, ck, "滑档≠人生完蛋 · 以为滑档=完蛋的恐慌，才是损失", font(30), (540, 1136), color=LIGHT, maxw=1000)
put(d, ck, "数据来源：深圳市2026年第一批录取标准 · 逐条人工核对", font(24), (540, 1350), color=SUB)
results["data"] = verify(d, ck, "1 数据速览")
save(img, N + "-长文1-数据速览-1080x1440.png")

# ================= 2. 给家长三句话 =================
img, d = new_canvas(1); ck = []
put(d, ck, "给中考家长 · 三句话", font(34, True), (540, 100), color=GOLD)
put(d, ck, "记住这3句，心里有底", font(56, True), (540, 215), color=WHITE, maxw=1000)
lines = [
    ("先分清，别慌", "多数不是滑档，是志愿梯度没拉开"),
    ("排名40不差", "公办普高 · 稳定师资 · 正常高考出口"),
    ("孩子学习好 · 家长决策优", "政策 / 数据 / 志愿梯度，出分前做功课"),
]
y0, rh, rg = 340, 200, 40
for i, (t, s) in enumerate(lines):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=24)
    cy = y + rh // 2
    put(d, ck, str(i + 1), font(64, True), (132, cy), color=GOLD)
    block2_lm(d, ck, 216, cy, t, s, font(46, True), font(32), maxw=760)
put(d, ck, "别让孩子带着「我不行」读三年 · 你镇定，孩子才有底气", font(34, True), (540, 1180), color=GOLD, maxw=1020)
put(d, ck, "详细分析看长文 →", font(26), (540, 1360), color=SUB)
results["3line"] = verify(d, ck, "2 三句话")
save(img, N + "-长文2-三句话-1080x1440.png")

print()
print("全部 OK =", all(results.values()))
