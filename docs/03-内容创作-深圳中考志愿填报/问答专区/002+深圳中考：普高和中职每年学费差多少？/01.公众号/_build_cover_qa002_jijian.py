# -*- coding: utf-8 -*-
"""QA-002 公众号首图 · 极简大字版（900×383）
要素与完整版首图一致（徽章/「同样读三年书」/「有人花1万·有人花30万」/副题/CTA胶囊），
但排版改为「1万 vs 30万」数字对撞大字版——关键数字放大为视觉主角，与完整版首图形成区分。
风格与全仓统一：深蓝渐变 + 金色数据 + 微软雅黑。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 383
TOP = (27, 58, 92); BOT = (13, 30, 48)
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


# ---------- 渐变画布 ----------
t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
d = ImageDraw.Draw(img)
ck = []

# ---------- 要素1 · 顶部徽章（同完整版 BANNER） ----------
d.rounded_rectangle([280, 24, 620, 54], radius=15, fill=BAND, outline=GOLD, width=2)
put(d, ck, "深圳中考 · 问答系列 · 002", font(15, True), (450, 39), color=GOLD)

# ---------- 要素2 · 主标题「同样读三年书」 ----------
put(d, ck, "同样读三年书", font(32, True), (450, 82), color=WHITE)

# ---------- 要素3 · 「有人花1万·有人花30万」→ 放大为巨型数字对撞 ----------
put(d, ck, "公办 · 三年", font(20, True), (215, 134), color=LIGHT)
put(d, ck, "民办 · 三年", font(20, True), (685, 134), color=LIGHT)
put(d, ck, "1万", font(88, True), (215, 212), color=GOLD, maxw=360)
put(d, ck, "30万", font(88, True), (685, 212), color=GOLD, maxw=360)
d.rounded_rectangle([398, 184, 502, 234], radius=25, fill=GOLD)
put(d, ck, "VS", font(28, True), (450, 209), color=NAVY)

# ---------- 要素4 · 副题（同完整版） ----------
put(d, ck, "普高和中职的学费差 · 家长现在就得看清", font(20, True), (450, 292), color=GOLD, maxw=820)

# ---------- 要素5 · CTA 胶囊（同完整版「三年总账·三个数字·三件事」）· 从底部定位留边距 ----------
t2 = "三年总账 · 三个数字 · 三件事"
fp = font(17, True)
bb = d.textbbox((0, 0), t2, font=fp)
pd = 16
py1 = H - 24                      # 底部留白 24px，从底部向上定位
py0 = py1 - bb[3] - pd
px0 = (W - (bb[2] + pd * 2)) / 2
px1 = px0 + bb[2] + pd * 2
d.rounded_rectangle([px0, py0, px1, py1], radius=30, outline=GOLD, width=2)
put(d, ck, t2, fp, ((px0 + px1) / 2, (py0 + py1) / 2), color=GOLD)

# ---------- 校验（文字越界 + 胶囊矩形越界/贴边） ----------
bad = 0
for (text, fnt, (cx, cy), anchor) in ck:
    bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
    x0, y0 = bb[0] + cx, bb[1] + cy
    x1, y1 = bb[2] + cx, bb[3] + cy
    if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
        bad += 1
        print(f"[越界] {text!r} @({cx},{cy})")
# 胶囊矩形边界：底部留白 ≥20px
if not (px0 >= 10 and px1 <= W - 10 and py0 >= 10 and py1 <= H - 20):
    bad += 1
    print(f"[胶囊越界/贴边] rect=({px0:.0f},{py0:.0f},{px1:.0f},{py1:.0f}) H={H} 底部留白={H - py1:.0f}px")
print(f"OVERFLOW: {'PASS' if bad == 0 else 'FAIL ' + str(bad)}（胶囊底部留白 {H - py1:.0f}px）")

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/002+深圳中考：普高和中职每年学费差多少？/01.公众号/002+深圳中考：普高和中职每年学费差多少？-公众号-首图-极简大字版-900x383.png"
img.save(out)
print("saved", out.split("/")[-1], img.size)
