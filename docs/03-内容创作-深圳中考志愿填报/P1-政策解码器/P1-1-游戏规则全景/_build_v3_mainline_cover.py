# -*- coding: utf-8 -*-
"""P1-1 主线封面 · 一句话触发点（C 定稿）+ 顶部地域标识 三尺寸——待目检，不覆盖原图
顶部小字「深圳中考」（可换东莞/广州复用）；文案：考得好≠填得好？／搞懂规则本身就是优势／30分钟建立全景地图
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107); LIGHT = (157, 184, 212); SUB = (201, 217, 232)
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"


def base(w, h):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    glow = np.exp(-(((x - w * 0.5) / (w * 0.3)) ** 2 + ((y - h * 0.2) / (h * 0.42)) ** 2))
    a = a + np.array((180, 205, 235), float)[None, None, :] * (glow * 0.10)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([w - 300, -140, w + 120, 260], fill=TOP + (26,))
    od.ellipse([-160, h - 220, 170, h + 20], fill=TOP + (16,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, fnt, fill, maxw, w, h, name=""):
    f = fnt
    while maxw and f.size > 12:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(FB if f.path.endswith("msyhbd.ttc") else FR, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f, anchor="mm")
    x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
    x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
    if not (x0 >= -1 and x1 <= w + 1 and y0 >= -1 and y1 <= h + 1):
        print(f"[溢出] {name}: '{text}' 字{f.size}")
    d.text(xy, text, font=f, fill=fill, anchor="mm")


def cover(w, h, cx, ys, fs, out):
    im, d = base(w, h)
    k_y, q_y, p_y, t_y = ys
    k_f, q_f, p_f, t_f = fs
    put(d, "深圳中考", (cx, k_y), ImageFont.truetype(FB, k_f), GOLD, w - 60, w, h, "kicker")
    kw = d.textlength("深圳中考", font=ImageFont.truetype(FB, k_f))
    d.line([(cx - kw / 2 - 6, k_y + int(k_f * 1.08)), (cx + kw / 2 + 6, k_y + int(k_f * 1.08))],
           fill=GOLD, width=max(3, k_f // 10))
    put(d, "考得好 ≠ 填得好？", (cx, q_y), ImageFont.truetype(FB, q_f), WHITE, w - 60, w, h, "q")
    put(d, "搞懂规则，本身就是优势", (cx, p_y), ImageFont.truetype(FB, p_f), GOLD, w - 60, w, h, "p")
    put(d, "30 分钟 · 建立你的全景地图", (cx, t_y), ImageFont.truetype(FB, t_f), SUB, w - 60, w, h, "t")
    im.save(out)
    print("saved", out.split("/")[-1])


cover(900, 383, 450, (52, 176, 252, 336), (48, 54, 60, 22),
      ROOT + "01.公众号/01.主线/P1-1-主线-公众号-首图-一句话-900x383.png")
cover(1200, 900, 600, (160, 440, 630, 800), (76, 90, 100, 40),
      ROOT + "02.今日头条/P1-1-主线-头条-封面-一句话-1200x900.png")
for sub in ["01.视频", "02.图文"]:
    cover(1080, 1440, 540, (360, 700, 950, 1170), (88, 100, 112, 50),
          ROOT + f"04.小红书/{sub}/P1-1-主线-小红书-首图-一句话-1080x1440.png")
print("完成")
