# -*- coding: utf-8 -*-
"""
P1-2 主线 · 公众号两张首图（900×383）一次产出
============================================
① 精简版：两行46px居中式（区别于子任务封面）
② 极简大字版：「3」巨型数字对撞 3 条规则名，与精简版排版区分
配色：系列统一深蓝渐变 + 金色。底部留白 ≥20px。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 383
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
FD = "C:/Windows/Fonts/"
BADGE_TXT = "深圳中考 · P1系列 · 630背后的隐藏规则"

def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

def new_canvas():
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    glow = np.exp(-(((x - W * 0.5) / (W * 0.6)) ** 2 + ((y - H * 0.15) / (H * 0.5)) ** 2)) * 0.15
    img2 = Image.fromarray(np.clip(np.array(img, float) + np.array((210, 225, 250))[None, None, :] * glow[:, :, None], 0, 255).astype(np.uint8), "RGB")
    return img2, ImageDraw.Draw(img2)

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
    return fnt

def badge(d, ck):
    x0, x1 = 260, 640
    d.rounded_rectangle([x0, 24, x1, 54], radius=15, fill=BAND, outline=GOLD, width=2)
    put(d, ck, BADGE_TXT, font(15, True), (450, 39), color=GOLD, maxw=360)

def verify(d, ck, name, rects=()):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1; print(f"  [越界] {text!r}")
    for r in rects:
        if not (r[0] >= 0 and r[2] <= W and r[1] >= 0 and r[3] <= H - 20):
            bad += 1; print(f"  [胶囊贴边] {r} 底部留白={H - r[3]:.0f}px")
    print(f"{name}: OVERFLOW {'PASS' if bad == 0 else 'FAIL ' + str(bad)}")
    return bad == 0

OUT = os.path.dirname(os.path.abspath(__file__))

# ================= ① 精简版首图：两行46px居中 =================
img, d = new_canvas(); ck = []
badge(d, ck)
put(d, ck, "630背后的", font(46, True), (450, 124), color=WHITE)
put(d, ck, "3个隐藏规则", font(46, True), (450, 182), color=WHITE)
put(d, ck, "性价比 · 等级制 · 隐形战场", font(25, True), (450, 244), color=GOLD, maxw=820)
t2 = "同样的630分 · 用法不一样 · 决定录取的往往不在分数"
fp = font(19, True)
bb = d.textbbox((0, 0), t2, font=fp); pd = 18
py1 = H - 22; py0 = py1 - bb[3] - pd
px0 = (W - (bb[2] + pd * 2)) / 2; px1 = px0 + bb[2] + pd * 2
d.rounded_rectangle([px0, py0, px1, py1], radius=30, outline=GOLD, width=2)
put(d, ck, t2, fp, ((px0 + px1) / 2, (py0 + py1) / 2), color=GOLD)
ok1 = verify(d, ck, "精简版", [(px0, py0, px1, py1)])
img.save(os.path.join(OUT, "P1-2-主线-公众号-首图-精简版-900x383.png"))

# ================= ② 极简大字版：「3」对撞三条规则（紧凑居中） =================
img, d = new_canvas(); ck = []
badge(d, ck)
put(d, ck, "630背后的隐藏规则", font(28, True), (450, 82), color=WHITE, maxw=820)
# 巨型数字 3（视觉主角）+ 三行规则名（紧凑组合：数字右侧紧贴文字列）
put(d, ck, "3", font(112, True), (296, 200), color=GOLD, maxw=220)
rules = ["① 性价比 · 花对地方", "② 等级制 · 看准位置", "③ 隐形战场 · 别踩门槛"]
fy = 170
for r in rules:
    put(d, ck, r, font(24, True), (430, fy), color=WHITE, anchor="lm", maxw=420)
    fy += 44
# 副题金色（留足与 CTA 胶囊间距） + CTA
put(d, ck, "分数会骗人 · 规则不会", font(20, True), (450, 300), color=GOLD, maxw=820)
t2 = "630分怎么用 · 一次讲透"
fp = font(17, True)
bb = d.textbbox((0, 0), t2, font=fp); pd = 16
py1 = H - 20; py0 = py1 - bb[3] - pd
px0 = (W - (bb[2] + pd * 2)) / 2; px1 = px0 + bb[2] + pd * 2
d.rounded_rectangle([px0, py0, px1, py1], radius=30, fill=GOLD)
put(d, ck, t2, fp, ((px0 + px1) / 2, (py0 + py1) / 2), color=NAVY)
ok2 = verify(d, ck, "极简大字版", [(px0, py0, px1, py1)])
img.save(os.path.join(OUT, "P1-2-主线-公众号-首图-极简大字版-900x383.png"))

print("ALL OK =", ok1 and ok2)
