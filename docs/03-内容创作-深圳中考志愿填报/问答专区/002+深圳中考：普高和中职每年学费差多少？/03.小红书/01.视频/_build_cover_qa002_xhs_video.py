# -*- coding: utf-8 -*-
"""QA-002 小红书视频笔记首图（1080×1440 · 3:4 大字版封面）
把「公办1万 vs 民办30万」学费差对撞放大为视觉主角；13-3 大字版规范（主标题放大、数字金色高亮）。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
FD = "C:/Windows/Fonts/"


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

# 顶部金色标签
put(d, ck, "深圳中考 · 问答专区 · 学费", font(28, True), (540, 100), color=GOLD)

# 主标题
put(d, ck, "普高和中职学费差多少？", font(72, True), (540, 240), color=WHITE, maxw=1000)

# 数字对撞
put(d, ck, "公办 · 三年", font(30), (280, 450), color=LIGHT)
put(d, ck, "民办 · 三年", font(30), (800, 450), color=LIGHT)
put(d, ck, "1万", font(150, True), (280, 600), color=GOLD, maxw=360)
put(d, ck, "30万", font(150, True), (800, 600), color=GOLD, maxw=520)
d.rounded_rectangle([462, 565, 542, 625], radius=30, fill=GOLD)
put(d, ck, "VS", font(28, True), (502, 595), color=NAVY)

# 分隔线 + 倍差金句
d.line([430, 760, 650, 760], fill=GOLD, width=4)
put(d, ck, "一年学费差 25-40倍", font(46, True), (540, 850), color=GOLD)

# 提示 + CTA
put(d, ck, "收藏这张图 · 慢慢对账", font(30), (540, 980), color=LIGHT)
d.rounded_rectangle([250, 1120, 830, 1240], radius=60, fill=GOLD)
put(d, ck, "关注 · 深圳中考系列连载", font(40, True), (540, 1180), color=NAVY)
put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(22), (540, 1340), color=SUB)

ok = verify(d, ck, "QA-002 小红书视频首图")

OUT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/002+深圳中考：普高和中职每年学费差多少？/03.小红书/01.视频/01-QA-002-普高和中职学费差多少-小红书-首图-1080x1440.png"
img.save(OUT)
print("已保存:", OUT.split("/")[-1])
print("OK =", ok)
