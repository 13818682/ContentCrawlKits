# -*- coding: utf-8 -*-
"""P1-3 S4 小红书视频封面 ×1（1080×1440，3:4）——S4 视频适配版首图
与图文首图（…-封面-精炼版）画面区分，避免两篇笔记首图同款；视觉仍为 S4 套图档
（royal 蓝·左上主光+斜射光束·金强调），读作同系列。
版式：顶部「深圳中考」金字 + 主钩子「非深户有3条路」+ ▶播放钮 + 三张牌 chips。
若发布端只支持"从视频选帧"做封面 → 本图做视频第 0.4-0.6s 静止首帧嵌入。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (31, 76, 150); BOT = (13, 29, 72)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (162, 192, 238); SUB = (214, 227, 248)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.24) / (W * 0.38)) ** 2 + ((y - H * 0.12) / (H * 0.30)) ** 2))
    a = a + np.array((196, 214, 250), float)[None, None, :] * (g * 0.13)[..., None]
    for k, amp, wid in [(0.32, 0.09, 320), (0.95, 0.06, 260)]:
        u = x - k * y
        a = a + np.array((205, 222, 252), float)[None, None, :] * (np.exp(-((u / wid) ** 2)) * amp)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .08, W * .24, H * .16], fill=(44, 74, 140, 50))
    od.ellipse([W * .82, H * .86, W * 1.12, H * 1.06], fill=(12, 26, 64, 42))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=1000, min_size=22, anchor="mm"):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    return f


im, d = base()
# 品牌行
f = put(d, "深圳中考", (W / 2, 150), 88, GOLD, maxw=980, min_size=74)
bb = d.textbbox((W / 2, 150), "深圳中考", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 236, W / 2 + half, 236], fill=GOLD, width=7)
# 小标（视频版）
put(d, "S4 · 视频版 · D类出路", (W / 2, 320), 40, LIGHT, bold=False, maxw=980, min_size=34)
# 主钩子（与图文首图主句区分）
put(d, "非深户有3条路", (W / 2, 500), 112, WHITE, maxw=1000, min_size=96)
put(d, "3分钟讲清 · 附每张牌的代价", (W / 2, 680), 58, GOLD, maxw=1000, min_size=48)
# ▶ 播放钮
cx, cy, r = W / 2, 960, 92
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=7)
d.polygon([(cx - 26, cy - 52), (cx - 26, cy + 52), (cx + 52, cy)], fill=WHITE)
# 三张牌 chips
chips = ["① 指标生 · 同校比", "② 民办 · ACD同线", "③ 3+4 · 本科直通"]
cw, chh, gap = 332, 112, 16
x0 = (W - (cw * 3 + gap * 2)) / 2
for i, t in enumerate(chips):
    x = x0 + i * (cw + gap)
    d.rounded_rectangle([x, 1210 - chh / 2, x + cw, 1210 + chh / 2], radius=56, outline=GOLD, width=4)
    put(d, t, (x + cw / 2, 1210), 36, WHITE, maxw=cw - 28, min_size=30)
# 底部提示
put(d, "视频版 · 分条收藏细节版在图文那篇", (W / 2, 1390), 30, SUB, bold=False, maxw=1000, min_size=25)
im.save(HERE + "P1-3-S4-D类三张牌-小红书-视频-封面-1080x1440.png")
print("saved 小红书视频封面 1080x1440")
