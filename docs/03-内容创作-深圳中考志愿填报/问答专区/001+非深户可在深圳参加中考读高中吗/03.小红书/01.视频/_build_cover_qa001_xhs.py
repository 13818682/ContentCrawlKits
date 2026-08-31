# -*- coding: utf-8 -*-
"""QA-001 小红书首图（1080×1440 · 3:4 大字版封面）
规范（13-3-小红书模板 2026-08-31 定稿）：
  - 画布 1080×1440，必须带文字标题，决定点击率
  - 大字版：主标题/关键数字放大到 92-104px，冲击力钩子金色高亮，缩略图一眼可读
  - 风格延续全仓：深蓝渐变 + 金色数据 + 微软雅黑
封面文案（QA-001 首图封面文字）：
  「非深户能读高中吗？能！」 + 5项条件 · 3条路
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66)
NAVY = (18, 30, 55)
FD = "C:/Windows/Fonts/"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 22:
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


img, d, ck = new_canvas(0)

# 1) 顶部金色标签
put(d, ck, "深圳中考 · 问答专区 · 非深户", font(28, True), (540, 96), color=GOLD)

# 2) 大字主标题（92px，白）
put(d, ck, "非深户能读高中吗？", font(92, True), (540, 268), color=WHITE, maxw=960)

# 3) 巨型金色冲击钩子「能！」
put(d, ck, "能！", font(220, True), (540, 540), color=GOLD, maxw=940)

# 4) 金色点缀线
d.line([540 - 120, 668, 540 + 120, 668], fill=GOLD, width=4)

# 5) 数据带：5项条件 · 3条路（金色数字）
put(d, ck, "只要满足", font(34), (540, 772), color=LIGHT)

chip_w, chip_h, chip_gap = 300, 96, 40
chip_w_total = 2 * chip_w + chip_gap
cx0 = (W - chip_w_total) // 2
cy0 = 836
for i, (num, lab) in enumerate([("5项", "条件"), ("3条", "出路")]):
    cx = cx0 + i * (chip_w + chip_gap)
    d.rounded_rectangle([cx, cy0, cx + chip_w, cy0 + chip_h], radius=22, fill=CARD, outline=EDGE, width=2)
    put(d, ck, num, font(44, True), (cx + 96, cy0 + chip_h // 2), color=GOLD)
    put(d, ck, lab, font(34), (cx + 96 + 74, cy0 + chip_h // 2), color=WHITE)

# 6) 提示语
put(d, ck, "收藏慢慢核对 · 别让孩子输在信息上", font(30), (540, 1040), color=LIGHT)

# 7) 金色 CTA 胶囊
d.rounded_rectangle([250, 1120, 830, 1240], radius=60, fill=GOLD)
put(d, ck, "关注 · 深圳中考系列连载", font(40, True), (540, 1180), color=NAVY)

# 8) 底部数据来源
put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(22), (540, 1340), color=SUB)

ok = verify(d, ck, "QA-001 小红书首图")

OUT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/001+非深户可在深圳参加中考读高中吗/03.小红书/01-QA-001-非深户能在深圳读高中吗-小红书-首图-1080x1440.png"
img.save(OUT)
print("已保存:", OUT.split("/")[-1])
print("OK =", ok)
