# -*- coding: utf-8 -*-
"""S5 小红书长文配图：等级比例表转图（1080×1440）
小红书长文正文复用头条长文，但长文不支持 markdown 表格 → 把头条长文里的等级表转成一张图插入。
三列结构：等级（左）/ 占全市比例（中）/ 一句话含义（右），表头行 GOLD + 6 数据行。
口径同头条长文：A+前5%、A前5-25%、B+25-50%、B50-75%、C+75-95%、C后5%（手册 §三-2）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440
HM = 70
BOXES = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.32)) ** 2 + ((y - H * 0.14) / (H * 0.28)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .07, W * .24, H * .15], fill=TOP + (34,))
    od.ellipse([W * .80, H * .86, W * 1.1, H * 1.05], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, anchor="mm", maxw=None, min_size=28, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    if maxw:
        while f.size > min_size:
            bb = d.textbbox((0, 0), text, font=f)
            if bb[2] - bb[0] <= maxw + 1:
                break
            f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= (maxw + 1 if maxw else 1e9), "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    BOXES.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor=anchor)))
    return f


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE):
    d.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=wfill, outline=wout, width=2)


# 三列锚点：等级/比例中心对齐；含义右对齐到版心右缘
CX1 = HM + 100          # 等级（mm）
CX2 = HM + 360          # 占全市比例（mm）
CX3R = W - HM - 10      # 含义右缘（rm）
COLS = ["等级", "占全市比例", "一句话含义"]
COLS_X = [CX1, CX2, CX3R]

im, d = base()
put(d, "S5 · 单科等级", (W / 2, 70), 32, GOLD, bold=False, min_size=24)
put(d, "六级等级，按全市比例划", (W / 2, 226), 62, WHITE, maxw=950, min_size=48)
put(d, "看等级比看分数更能定位位置", (W / 2, 318), 32, LIGHT, bold=False, min_size=26)

# 表头行
hy = 392
for colx, ct in zip(COLS_X, COLS):
    put(d, ct, (colx, hy), 32, GOLD, anchor=("rm" if colx == CX3R else "mm"), maxw=300, min_size=26)
d.line([HM + 10, hy + 30, W - HM - 10, hy + 30], fill=EDGE, width=2)

# 6 数据行
rows = [
    ("A+", "前 5%", "单科全市顶尖"),
    ("A", "前 5%~25%", "单科优秀"),
    ("B+", "前 25%~50%", "中等偏上"),
    ("B", "前 50%~75%", "中等"),
    ("C+", "前 75%~95%", "偏下，需留意"),
    ("C", "后 5%", "该科全市靠后"),
]
row_h = 108
gap = 14
y0 = 470
for i, (lv, rng, desc) in enumerate(rows):
    ytop = y0 + i * (row_h + gap)
    ybot = ytop + row_h
    rcard(d, HM, ytop, W - HM, ybot)
    put(d, lv, (CX1, (ytop + ybot) / 2), 52, GOLD, maxw=150, min_size=42)
    put(d, rng, (CX2, (ytop + ybot) / 2), 40, WHITE, maxw=260, min_size=32)
    put(d, desc, (CX3R, (ytop + ybot) / 2), 36, LIGHT, bold=False, anchor="rm", maxw=340, min_size=28)

# 尾注
put(d, "每科按单科原始分划定 · 卷子难不难不影响比例", (W / 2, 1346), 30, SUB, bold=False, min_size=24)
put(d, "数据来源：报考指导手册 §三-2 · 人工核对", (W / 2, 1394), 22, SUB, bold=False, min_size=18)

# 越界自检
bad = []
for tag, bb in BOXES:
    if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 6:
        bad.append((tag, tuple(int(v) for v in bb)))
print(("OK  " if not bad else "!!  ") + "S5 长文等级表", "| texts:", len(BOXES), bad if bad else "")
im.save(HERE + "S5-单科等级与省一级门槛-小红书-长文-等级表-1080x1440.png")
print("done")
