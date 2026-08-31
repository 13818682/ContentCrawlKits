# -*- coding: utf-8 -*-
"""QA-002 小红书图文配图（6张：首图 + 正文图1-5，全部 1080×1440 · 3:4）
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

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/002+深圳中考：普高和中职每年学费差多少？/03.小红书/02.图文/"
N = "01-QA-002-普高和中职学费差多少-小红书"


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
    return img, ImageDraw.Draw(img), []


def save(img, fn):
    img.save(BASE + fn)
    print("已保存:", fn)


results = {}

# ================= 1. 首图（封面）=================
img, d, ck = new_canvas(0)
put(d, ck, "深圳中考 · 问答专区 · 学费", font(28, True), (540, 100), color=GOLD)
put(d, ck, "普高和中职学费差多少？", font(64, True), (540, 250), color=WHITE, maxw=1020)
put(d, ck, "25-40倍", font(150, True), (540, 500), color=GOLD, maxw=1000)
put(d, ck, "同样读三年书 · 有人花1万，有人花30万", font(34), (540, 660), color=LIGHT, maxw=1000)
chip_w, chip_h, chip_gap = 360, 96, 40
cx0 = (W - (2 * chip_w + chip_gap)) // 2
cy0 = 780
for i, (lab, num) in enumerate([("公办·三年", "约1万"), ("民办·三年", "21万-36万")]):
    cx = cx0 + i * (chip_w + chip_gap)
    box(d, cx, cy0, chip_w, chip_h, r=22)
    put(d, ck, lab, font(30), (cx + 90, cy0 + chip_h // 2), color=WHITE)
    put(d, ck, num, font(34, True), (cx + 90 + 150, cy0 + chip_h // 2), color=GOLD)
put(d, ck, "收藏这张图 · 慢慢对账", font(30), (540, 1040), color=LIGHT)
d.rounded_rectangle([250, 1120, 830, 1240], radius=60, fill=GOLD)
put(d, ck, "关注 · 深圳中考系列连载", font(40, True), (540, 1180), color=NAVY)
put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(22), (540, 1340), color=SUB)
results["cover"] = verify(d, ck, "1 首图")
save(img, N + "-首图-1080x1440.png")

# ================= 2. 正文图1 · 三年总账 =================
img, d, ck = new_canvas(1)
put(d, ck, "普高 vs 中职 · 三年总账", font(34, True), (540, 100), color=GOLD)
put(d, ck, "同样读三年书，四类学校差多少", font(52, True), (540, 215), color=WHITE, maxw=1020)
rows = [
    ("公办普高", "80,303人", "约1万", GOLD),
    ("民办普高", "33,195人", "21万-36万", GOLD),
    ("公办中职", "15,924人", "约3千 · 免学费", GOLD),
    ("民办中职", "17,330人", "5万-10万", GOLD),
]
y0, rh, rg = 320, 190, 28
for i, (t, n, cost, tc) in enumerate(rows):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, t, font(44, True), (190, cy), color=WHITE, maxw=280)
    put(d, ck, n, font(30), (470, cy), color=LIGHT, maxw=280)
    put(d, ck, cost, font(40, True), (800, cy), color=GOLD, maxw=300)
put(d, ck, "同样读三年书 · 公办和民办能差几十倍", font(30, True), (540, 1360), color=GOLD)
results["table"] = verify(d, ck, "2 三年总账")
save(img, N + "-正文图1-三年总账-1080x1440.png")

# ================= 3. 正文图2 · 贵25到40倍 =================
img, d, ck = new_canvas(2)
put(d, ck, "贵在哪 · 一年贵25-40倍", font(34, True), (540, 100), color=GOLD)
put(d, ck, "民办普高一年7万-12万", font(52, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 320, 960, 220, r=24)
put(d, ck, "≈ 一个打工人全年工资", font(44, True), (540, 430), color=GOLD)
box(d, 60, 580, 960, 220, r=24)
put(d, ck, "公办普高一年约3,200元", font(40, True), (540, 690), color=WHITE)
put(d, ck, "≈ 普通打工人年工资的3%", font(30), (540, 760), color=LIGHT)
put(d, ck, "同样读一年高中，民办是公办的 25-40倍", font(34, True), (540, 900), color=GOLD, maxw=1020)
put(d, ck, "这钱差在哪？不是孩子成绩，是家长有没有提前看清", font(30), (540, 1000), color=LIGHT, maxw=1020)
put(d, ck, "下一张：这三年到底要干几年才挣得回？", font(26), (540, 1360), color=SUB)
results["mult"] = verify(d, ck, "3 贵25到40倍")
save(img, N + "-正文图2-贵25到40倍-1080x1440.png")

# ================= 4. 正文图3 · 工资负担 =================
img, d, ck = new_canvas(3)
put(d, ck, "这笔钱 · 谁扛得动", font(34, True), (540, 100), color=GOLD)
put(d, ck, "三年≈不吃不喝干2-3年", font(52, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 330, 960, 210, r=24)
put(d, ck, "民办普高三年 21万-36万", font(40, True), (540, 435), color=GOLD)
put(d, ck, "≈ 一个人不吃不喝干2-3年 · 可能是一家人几年积蓄", font(28), (540, 505), color=LIGHT, maxw=920)
box(d, 60, 580, 960, 240, r=24)
put(d, ck, "分数差不多的孩子", font(34), (540, 660), color=WHITE)
put(d, ck, "进公办：一年约3千", font(36, True), (330, 750), color=GOLD)
put(d, ck, "滑到民办：一年约7万", font(36, True), (750, 750), color=WHITE)
d.line([540, 720, 540, 790], fill=EDGE, width=2)
put(d, ck, "差的不是成绩，是提前看清的那一步", font(32, True), (540, 940), color=GOLD, maxw=1020)
put(d, ck, "下一张：便宜的路，可能藏着本科机会", font(26), (540, 1360), color=SUB)
results["wage"] = verify(d, ck, "4 工资负担")
save(img, N + "-正文图3-工资负担-1080x1440.png")

# ================= 5. 正文图4 · 贯通机会 =================
img, d, ck = new_canvas(0)
put(d, ck, "最被忽略的一条路", font(34, True), (540, 100), color=GOLD)
put(d, ck, "公办中职免学费 · 还有本科路", font(52, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 320, 960, 230, r=24)
put(d, ck, "3+4 中本贯通", font(44, True), (540, 405), color=GOLD)
put(d, ck, "中职3年 + 本科4年 · 拿全日制本科文凭 · 几乎不花学费", font(30), (540, 490), color=LIGHT, maxw=920)
box(d, 60, 590, 960, 200, r=24)
put(d, ck, "但名额少得可怜", font(38, True), (540, 690), color=WARN)
put(d, ck, "3+4仅约300个 · 加3+2约3000多个 · 15.3万考生抢", font(30), (540, 755), color=LIGHT, maxw=920)
put(d, ck, "便宜是真便宜，难进也是真难进——提前研究专业和名额", font(32, True), (540, 900), color=GOLD, maxw=1020)
put(d, ck, "下一张：现在就能做的三件事", font(26), (540, 1360), color=SUB)
results["path"] = verify(d, ck, "5 贯通机会")
save(img, N + "-正文图4-贯通机会-1080x1440.png")

# ================= 6. 正文图5 · 行动三件事 =================
img, d, ck = new_canvas(1)
put(d, ck, "现在就能做 · 三件事", font(34, True), (540, 100), color=GOLD)
put(d, ck, "别等出分才发现", font(52, True), (540, 212), color=WHITE, maxw=1020)
acts = [
    ("①", "现在开始看数据", "公办线 · 民办学费 · 中职贯通专业，全摆明面上"),
    ("②", "先定预算再谈志愿", "家里三年能扛多少，决定志愿表下限"),
    ("③", "公办优先 · 民办比价 · 中职看通道", "三条路没有绝对好坏，只看合不合适、扛不扛得起"),
]
y0, rh, rg = 320, 190, 28
for i, (num, t, s) in enumerate(acts):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, num, font(56, True), (140, cy), color=GOLD)
    block2_lm(d, ck, 230, cy, t, s, font(42, True), font(32), maxw=780)
put(d, ck, "学费这件事，永远是越早知道越好 · 收藏这张清单", font(34, True), (540, 1380), color=GOLD, maxw=1020)
results["action"] = verify(d, ck, "6 行动三件事")
save(img, N + "-正文图5-行动三件事-1080x1440.png")

print()
print("全部 OK =", all(results.values()))
