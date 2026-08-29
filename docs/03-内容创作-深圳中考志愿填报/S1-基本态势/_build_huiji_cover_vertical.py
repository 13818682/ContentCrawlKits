# -*- coding: utf-8 -*-
"""深圳中考信息合集 · 公众号合集封面 → 配套手机竖版首页图（1080×1920, 9:16）
设计继承 13-深圳中考信息合集-公众号合集封面.svg：
深蓝三段渐变(#1b3a5c→#142a44→#0d1e30) + 金色强调(#f5c66b) + 关键词网格"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1080, 1920
STOP0 = (27, 58, 92)     # #1b3a5c
STOP1 = (20, 42, 68)     # #142a44
STOP2 = (13, 30, 48)     # #0d1e30
WHITE = (255, 255, 255)
GOLD = (245, 198, 107)   # #f5c66b
LIGHT = (157, 184, 212)  # #9db8d4
SUB = (138, 166, 192)    # #8aa6c0
BODY = (201, 217, 232)   # #c9d9e8
CARD = (38, 74, 118)     # #264a76
EDGE = (58, 100, 148)    # #3a6494


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def new_canvas():
    c0 = np.array(STOP0, dtype=np.float32)
    c1 = np.array(STOP1, dtype=np.float32)
    c2 = np.array(STOP2, dtype=np.float32)
    img = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.6:
            k = p / 0.6
            img[y, :, :] = c0 * (1 - k) + c1 * k
        else:
            k = (p - 0.6) / 0.4
            img[y, :, :] = c1 * (1 - k) + c2 * k
    im = Image.fromarray(img.astype(np.uint8), "RGB")
    return im, ImageDraw.Draw(im)


def put(d, checks, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
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
    checks.append((text, fnt, xy, anchor))


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=22):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=3)


def verify(d, checks, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy})")
    print(f"{name}: 共{len(checks)}处文字，{bad}处越界")


img, d = new_canvas()
checks = []

# 顶部品牌行 + 金色装饰线
put(d, checks, "HSEE · 深圳中考志愿规划", font(34), (84, 118), anchor="lm", color=LIGHT, maxw=900)
d.rectangle([84, 168, 234, 173], fill=GOLD)

# 主标题 / 强调行 / 副标语
put(d, checks, "深圳中考信息合集", font(108, True), (W // 2, 430), color=WHITE, maxw=1000)
put(d, checks, "2027届家长必读", font(58, True), (W // 2, 575), color=GOLD, maxw=1000)
put(d, checks, "数据驱动 · 不贩卖焦虑", font(40), (W // 2, 680), color=BODY, maxw=1000)

# 关键词网格（2 行 × 3 卡）
keywords = [
    ("考生规模", "录取率", "志愿填报"),
    ("指标生", "非深户D类", "出路全景"),
]
cw, ch, cgap = 300, 120, 34
x0 = (W - (cw * 3 + cgap * 2)) // 2
row1_y = 840
for ri, row in enumerate(keywords):
    ry = row1_y + ri * (ch + 46)
    for ci, kw in enumerate(row):
        cx = x0 + ci * (cw + cgap)
        box(d, cx, ry, cw, ch, r=26)
        put(d, checks, kw, font(36, True), (cx + cw // 2, ry + ch // 2), color=WHITE, maxw=cw - 24)

# CTA 强调条
box(d, 120, 1210, W - 240, 108, r=54)
put(d, checks, "7篇文章 · 从「完全不懂」到「心中有数」", font(36, True), (W // 2, 1264), color=GOLD, maxw=W - 300)

# 底部来源
put(d, checks, "数据来源：深圳市教育局官方公开信息 · 逐条人工核对", font(26), (W // 2, 1800), color=SUB, maxw=1000)

# 右上装饰圆（同心圆，模拟 SVG 半透明描边）
d.ellipse([850, 50, 1090, 290], outline=(42, 77, 112), width=3)
d.ellipse([886, 94, 1054, 262], outline=(42, 77, 112), width=2)

verify(d, checks, "合集封面·手机竖版首页图")
out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/13-深圳中考信息合集-公众号合集封面-手机竖版首页-1080x1920.png"
img.save(out)
print("已生成:", out)
