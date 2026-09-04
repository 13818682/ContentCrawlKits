# -*- coding: utf-8 -*-
"""化繁为简样板：P1-2 小红书首图（1080×1440）
去掉顶部徽章小字 / 中部说明 / 底部金句，只留 主标题 + 3规则 pill + 收藏CTA。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
FD = "C:/Windows/Fonts/"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 18:
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
    print(f"{name}: {bad}处越界")
    return bad == 0


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=24, width=2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)


def new_canvas():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.5:
            k = p / 0.5; col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.5) / 0.5; col = c_mid * (1 - k) + c_bot * k
        globs = col
    base = np.zeros((H, W, 3), np.float32)
    t = np.linspace(0, 1, H)[:, None, None]
    base = np.repeat(c_top[None, None, :] * (1 - t) + c_bot[None, None, :] * t, W, axis=1)
    diag = np.clip((xx / W * 0.3 + yy / H * 0.7), 0, 1)[:, :, None]
    base *= (0.72 + 0.28 * diag)
    sx, sy = 0.8, 0.12; col = np.array((150, 200, 240), np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.5)) ** 2 + ((yy - sy * H) / (H * 0.5)) ** 2)
    base += col[None, None, :] * (np.exp(-dist * dist) * 0.32)[:, :, None]
    sx, sy = 0.15, 0.9; col = np.array((90, 160, 230), np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.5)) ** 2 + ((yy - sy * H) / (H * 0.4)) ** 2)
    base += col[None, None, :] * (np.exp(-dist * dist) * 0.18)[:, :, None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


img, d = new_canvas(); ck = []
# 主体：两行标题
put(d, ck, "630分背后", font(58, True), (540, 320), color=WHITE, maxw=1000)
put(d, ck, "藏着3个规则", font(120, True), (540, 560), color=GOLD, maxw=1000)
# 3 规则 pill（放大的唯一信息点）
labs = ["性价比", "等级制", "隐形战场"]
pw, pg, ph = 230, 45, 96
px0 = (W - (3 * pw + 2 * pg)) // 2
py0 = 880
for i, lab in enumerate(labs):
    px = px0 + i * (pw + pg)
    d.rounded_rectangle([px, py0, px + pw, py0 + ph], radius=ph // 2, fill=BAND, outline=GOLD, width=3)
    put(d, ck, lab, font(40, True), (px + pw // 2, py0 + ph // 2), color=GOLD, maxw=pw - 16)
# 底部唯一 CTA
d.rounded_rectangle([280, 1190, 800, 1320], radius=65, fill=GOLD)
put(d, ck, "收藏 · 备考对照", font(44, True), (540, 1255), color=NAVY)
ok = verify(d, ck, "化繁为简样板")
img.save("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/04.小红书/化繁为简-P1-2-小红书首图-1080x1440.png")
print("saved 化繁为简样板", ok)
