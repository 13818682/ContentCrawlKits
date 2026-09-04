# -*- coding: utf-8 -*-
"""
P1-2 子任务04 · 隐形战场 两页版（900×600）
========================================
页A：生地同分PK —— 用 552 分真实案例生动说明（两名考生怎么一决胜负）
页B：信息科技/艺术 —— 省一级学校的隐形入场券
版式统一：徽章 + 标题 + 案例卡 + 结论金句
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

TOP = (27, 58, 92)
BOT = (13, 30, 48)
WHITE = (255, 255, 255)
GOLD = (245, 198, 107)
LIGHT = (157, 184, 212)
SUB = (201, 217, 232)
CARD = (31, 66, 106)
EDGE = (58, 100, 148)
WARN = (245, 156, 96)

W, H = 900, 600


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    dd = np.sqrt(((x - W * 0.15) / (W * 0.5)) ** 2 + ((y - H * 0.15) / (H * 0.5)) ** 2)
    a = a * (1 - 0.22 * np.clip(dd - 0.6, 0, None)[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([W - 300, -120, W + 100, 220], fill=TOP + (30,))
    od.ellipse([-140, H - 180, 150, H + 40], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def card(d, box, fill_alpha=0, outline=None, outline_alpha=255, radius=16, width=2):
    im = d._image
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fill_alpha))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


def draw_check(d, cx, cy, size, color=GOLD):
    d.line([(cx - size, cy), (cx - size * 0.3, cy + size * 0.7)], fill=color, width=4)
    d.line([(cx - size * 0.3, cy + size * 0.7), (cx + size, cy - size * 0.5)], fill=color, width=4)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 10:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    ck.append((text, fnt, xy, anchor))


FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def build_header(d, ck, tag):
    d.rounded_rectangle([280, 22, 620, 52], radius=15, fill=(17, 38, 66), outline=GOLD, width=2)
    put(d, ck, tag, font(16, True), (450, 37), color=GOLD)


def verify(d, ck, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} @({cx},{cy})")
    print(f"{name}: OVERFLOW {'PASS' if bad == 0 else 'FAIL ' + str(bad)}")
    return bad == 0


OUT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/01.公众号/04.子任务-隐形战场/"

# ================= 页A · 生地同分PK 552案例 =================
img, d = base(); ck = []
build_header(d, ck, "深圳中考 · P1系列 · 630背后的隐藏规则③")
put(d, ck, "生地会考 · 决定命运的'隐形战场'", font(34, True), (450, 95), color=WHITE, maxw=860)
# 案例叙述卡
card(d, [60, 130, 840, 300], fill_alpha=10, radius=20)
put(d, ck, "一个真实的录取故事", font(24, True), (450, 170), color=GOLD)
put(d, ck, "2026年某区属高中最后1个名额，两名考生总分都是 552 分——", font(20), (450, 215), color=WHITE, maxw=740)
put(d, ck, "一个名额，两个人，怎么分？", font(22, True), (450, 252), color=GOLD)
# 对比卡
cw2, ch2 = 360, 130
cx_a, cx_b = 210, 690
cy2 = 320
card(d, [cx_a - 180, cy2, cx_a + 180, cy2 + ch2], fill_alpha=16, outline=GOLD, outline_alpha=180, radius=18)
put(d, ck, "考生A", font(22, True), (cx_a, cy2 + 32), color=WHITE)
put(d, ck, "总分 552", font(26, True), (cx_a - 70, cy2 + 82), color=GOLD)
put(d, ck, "生地 96", font(22, True), (cx_a + 70, cy2 + 82), color=GOLD)
card(d, [cx_b - 180, cy2, cx_b + 180, cy2 + ch2], fill_alpha=10, outline=EDGE, outline_alpha=100, radius=18)
put(d, ck, "考生B", font(22, True), (cx_b, cy2 + 32), color=WHITE)
put(d, ck, "总分 552", font(26, True), (cx_b - 70, cy2 + 82), color=WHITE)
put(d, ck, "生地 82", font(22, True), (cx_b + 70, cy2 + 82), color=SUB)
# 结论金句
draw_check(d, 170, 510, 12)
put(d, ck, "总分相同 → 比生地 → 96 > 82，考生A录取", font(24, True), (300, 510), color=WHITE, anchor="lm", maxw=560)
put(d, ck, "14分的生地差距 · 一个高中学位", font(20, True), (450, 556), color=GOLD)
verify(d, ck, "页A 生地PK")
img.save(OUT + "P1-2-子任务04a-生地同分PK-900x600.png")
print("saved 页A")

# ================= 页B · 信息科技/艺术 入场券 =================
img, d = base(); ck = []
build_header(d, ck, "深圳中考 · P1系列 · 630背后的隐藏规则③")
put(d, ck, "信息科技 & 艺术 · 隐形入场券", font(34, True), (450, 95), color=WHITE, maxw=860)
# 上部说明卡（加高，容纳三行）
card(d, [60, 140, 840, 330], fill_alpha=10, radius=20)
put(d, ck, "想报考省一级学校？先过这关", font(28, True), (450, 188), color=GOLD)
put(d, ck, "信息科技、艺术必须「合格」", font(22, True), (450, 240), color=WHITE)
put(d, ck, "才能报考省一级公办普高", font(22, True), (450, 284), color=WHITE)
put(d, ck, "（深圳大多数公办普高都是省一级）", font(18), (450, 320), color=LIGHT)
# 门槛提示（紧接上部卡，间距 24px）
card(d, [60, 370, 840, 530], fill_alpha=16, outline=WARN, outline_alpha=160, radius=16)
put(d, ck, "别让「合格考」翻车", font(28, True), (450, 414), color=WARN)
put(d, ck, "这科通常由学校自行组织考核", font(20), (450, 462), color=WHITE)
put(d, ck, "绝大多数学生都能合格 · 但一定要确认", font(20), (450, 502), color=WHITE)
put(d, ck, "被忽略的隐性门槛 · 也可能卡住人", font(20, True), (450, 570), color=GOLD)
verify(d, ck, "页B 信技门槛")
img.save(OUT + "P1-2-子任务04b-信技艺术门槛-900x600.png")
print("saved 页B")
