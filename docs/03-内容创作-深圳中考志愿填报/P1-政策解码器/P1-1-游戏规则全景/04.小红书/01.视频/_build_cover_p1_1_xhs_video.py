# -*- coding: utf-8 -*-
"""P1-1 小红书视频笔记首图（1080×1440 · 3:4 大字版封面）
「深圳中考游戏规则 · 四句话就讲完」+ 「630分」数字对撞放大为视觉主角；13-3 大字版规范。
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
    return img, ImageDraw.Draw(img)


def save(img, fn):
    img.save(BASE + fn)
    print("已保存:", fn)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/04.小红书/01.视频/"
N = "01-P1-1-深圳中考游戏规则-四句话看懂-小红书"

results = {}

# ================= 视频首图 1080x1440 =================
img, d = new_canvas(0); ck = []
put(d, ck, "深圳中考 · 政策解码器 · 第1篇", font(28, True), (540, 100), color=GOLD)
put(d, ck, "深圳中考游戏规则", font(64, True), (540, 250), color=WHITE, maxw=1000)
put(d, ck, "四句话就讲完", font(120, True), (540, 500), color=GOLD, maxw=980)
put(d, ck, "不是考试 · 是一套游戏规则", font(38), (540, 640), color=LIGHT, maxw=1000)
chip_w, chip_h, chip_gap = 460, 160, 36
cx0 = (W - (2 * chip_w + chip_gap)) // 2
cy0 = 770
for i, (lab, num) in enumerate([("总分", "630分"), ("第一批志愿", "16个")]):
    cx = cx0 + i * (chip_w + chip_gap)
    box(d, cx, cy0, chip_w, chip_h, r=22)
    put(d, ck, lab, font(30), (cx + chip_w // 2, cy0 + 48), color=WHITE, maxw=chip_w - 20)
    put(d, ck, num, font(52, True), (cx + chip_w // 2, cy0 + 118), color=GOLD, maxw=chip_w - 20)
put(d, ck, "ACD三类 · 五批次 · 排队录取", font(30), (540, 1080), color=LIGHT, maxw=1000)
d.rounded_rectangle([220, 1160, 860, 1290], radius=60, fill=GOLD)
put(d, ck, "收藏这张 · 慢慢对照", font(40, True), (540, 1225), color=NAVY)
put(d, ck, "搞懂规则 · 填志愿不踩坑", font(28, True), (540, 1380), color=GOLD, maxw=1000)
results["cover"] = verify(d, ck, "视频首图")
save(img, N + "-首图-1080x1440.png")

print()
print("全部 OK =", all(results.values()))
