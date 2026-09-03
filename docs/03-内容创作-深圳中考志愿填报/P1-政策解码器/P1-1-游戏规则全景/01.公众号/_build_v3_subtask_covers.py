# -*- coding: utf-8 -*-
"""P1-1 子任务封面 04/05/06 · 一句话触发点（定稿导语）——待目检，不覆盖原图"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
G = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/01.公众号/"


def base(w, h):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    dd = np.sqrt(((x - w * 0.15) / (w * 0.5)) ** 2 + ((y - h * 0.15) / (h * 0.5)) ** 2)
    a = a * (1 - 0.22 * np.clip(dd - 0.6, 0, None)[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([w - 300, -120, w + 100, 220], fill=TOP + (30,))
    od.ellipse([-140, h - 180, 150, h + 40], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, fnt, fill, maxw, name=""):
    f = fnt
    while maxw and f.size > 12:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(FB if f.path.endswith("msyhbd.ttc") else FR, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f, anchor="mm")
    x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
    x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
    if not (x0 >= -1 and x1 <= 901 and y0 >= -1 and y1 <= 384):
        print(f"[溢出] {name}: '{text}' 字{f.size}")
    d.text(xy, text, font=f, fill=fill, anchor="mm")


def cover(out, q, p):
    im, d = base(900, 383)
    put(d, "深圳中考", (450, 52), ImageFont.truetype(FB, 46), GOLD, 850, "kicker")
    kw = d.textlength("深圳中考", font=ImageFont.truetype(FB, 46))
    d.line([(450 - kw / 2 - 6, 52 + 50), (450 + kw / 2 + 6, 52 + 50)], fill=GOLD, width=5)
    put(d, q, (450, 190), ImageFont.truetype(FB, 50), WHITE, 850, "q")
    put(d, p, (450, 298), ImageFont.truetype(FB, 40), GOLD, 700, "p")
    im.save(out)
    print("saved", out.split("/")[-1])


cover(G + "04.子任务-批次顺序卡/P1-1-子任务04-公众号封面-一句话-900x383.png",
      "自招、指标、统招分五批走，你了解录取顺序吗？", "顺序搞错，努力白搭")
cover(G + "06.子任务-排队比喻卡/P1-1-子任务06-公众号封面-一句话-900x383.png",
      "分数高，就一定进得了最想去的学校吗？", "最优方案：把最想去的放前面")
cover(G + "05.子任务-时间线卡/P1-1-子任务05-公众号封面-一句话-900x383.png",
      "从报名到录取 6 个月，哪一步最容易错过？", "早做清单，不留遗憾")
