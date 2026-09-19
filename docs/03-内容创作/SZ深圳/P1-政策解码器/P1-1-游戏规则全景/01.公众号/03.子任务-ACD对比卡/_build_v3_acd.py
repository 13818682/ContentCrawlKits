# -*- coding: utf-8 -*-
"""P1-1 子任务03·ACD对比卡 · 630 规则样板铺开（待目检，不覆盖原图）
封面=一句话触发点；内容卡=标题+三类定义三卡+D类核心数据带+三条关键+结论金卡，无装饰句。
数据口径：md 07/05 终稿「三类定义 + D类三件事」原句。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
EDGE = (58, 100, 148); NAVY = (18, 30, 55)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"


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


def put(d, im, text, xy, fnt, fill=WHITE, anchor="mm", maxw=None, w=900, h=700, name=""):
    f = fnt
    while maxw is not None and f.size > 12:
        bb = d.textbbox((0, 0), text, font=f, anchor=anchor)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(FB if f.path.endswith("msyhbd.ttc") else FR, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f, anchor=anchor)
    x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
    x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
    if not (x0 >= -1 and x1 <= w + 1 and y0 >= -1 and y1 <= h + 1):
        print(f"[溢出] {name}: '{text}' 字{f.size} 盒{x0:.0f},{y0:.0f}->{x1:.0f},{y1:.0f}")
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    return f


def rbox(d, im, box, radius=14, fill=None, fill_alpha=0, outline=None, outline_alpha=255, width=2):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if fill is not None and fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=fill + (fill_alpha,))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


# ============ 内容卡 900×700 ============
im, d = base(900, 700)
W, H = 900, 700
# 1) 标题
put(d, im, "考生分 A / C / D 三类，你在哪条赛道？", (450, 58),
    ImageFont.truetype(FB, 40), WHITE, "mm", 860, W, H, "title")

# 2) 三类定义三卡
defs = [
    (180, "A 类", "深户 + 学籍同区", "最宽赛道 · 所有学校都能报", GOLD),
    (450, "C 类", "深户 + 学籍跨区", "部分学校受限 · 有政策优惠", WHITE),
    (720, "D 类", "非深户", "窄赛道但有弯道 · 公办指标约23%", LIGHT),
]
cw, chh, cy0 = 250, 134, 118
for cx, lab, cond, take, col in defs:
    x0, x1 = cx - cw / 2, cx + cw / 2
    rbox(d, im, [x0, cy0, x1, cy0 + chh], radius=16,
         fill_alpha=16, outline=EDGE, outline_alpha=100, width=2)
    put(d, im, lab, (cx, cy0 + 34), ImageFont.truetype(FB, 34), col, "mm", cw - 20, W, H, f"lab{cx}")
    put(d, im, cond, (cx, cy0 + 72), ImageFont.truetype(FR, 20), WHITE, "mm", cw - 30, W, H, f"cond{cx}")
    put(d, im, take, (cx, cy0 + 112), ImageFont.truetype(FR, 17),
        GOLD if col == GOLD else SUB, "mm", cw - 30, W, H, f"take{cx}")

# 3) D类核心背景条
rbox(d, im, [60, 300, 840, 358], radius=14, fill_alpha=18, outline=EDGE, outline_alpha=130, width=2)
put(d, im, "D 类家长：考生一半以上是 D 类 · 公办普高招生指标仅约 23%", (450, 329),
    ImageFont.truetype(FB, 22), WHITE, "mm", 750, W, H, "bg")

# 4) 三条关键数据
put(d, im, "D 类 · 三组关键数据", (450, 392), ImageFont.truetype(FB, 22), GOLD, "mm", 500, W, H, "sec")
rows = [
    ("①", "四大名校：AC / D 分数线已基本持平（深中 AC592＝D592）"),
    ("②", "中下层次：D 类分数线仍比 AC 类高 5-15 分"),
    ("③", "指标生：已实现 D 类全覆盖 —— 最重要的降分通道"),
]
y = 424
for no, txt in rows:
    rbox(d, im, [60, y, 840, y + 48], radius=12, fill_alpha=10, outline=EDGE, outline_alpha=70, width=2)
    put(d, im, no, (90, y + 24), ImageFont.truetype(FB, 22), GOLD, "lm", 40, W, H, "no")
    put(d, im, txt, (150, y + 24), ImageFont.truetype(FR, 20), WHITE, "lm", 660, W, H, f"row{txt[:2]}")
    y += 62

# 5) 结论金卡（实心金底）
rbox(d, im, [60, y + 8, 840, y + 76], radius=16, fill=GOLD, fill_alpha=255)
put(d, im, "信息准备，对 D 类家长更重要", (450, y + 42), ImageFont.truetype(FB, 30), NAVY, "mm", 700, W, H, "concl")

im.save(OUT + "P1-1-子任务03-ACD对比卡-规则样板-900x700.png")
print("saved 内容卡 ACD")
