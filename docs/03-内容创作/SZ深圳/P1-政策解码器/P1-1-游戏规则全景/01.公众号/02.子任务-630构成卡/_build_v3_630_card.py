# -*- coding: utf-8 -*-
"""P1-1 子任务02·630构成卡 方案 v3（待目检，不覆盖原图）
封面定稿 A：一句话触发点（问题式）
内容卡美化：构成带(440/+20/170) + 两列等高明细(左语数英物化笔试5行｜右实验+史道体5行)；
已去底部「每1分都有它的位置」。
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


def put(d, im, text, xy, fnt, fill=WHITE, anchor="mm", maxw=None, w=900, h=600, name=""):
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


im, d = base(900, 600)

# 1) 标题
put(d, im, "深圳中考 630 分，怎么构成的？", (450, 64),
    ImageFont.truetype(FB, 42), WHITE, "mm", 860, 900, 600, "title")

# 2) 构成带三卡（数字+一句角色）
chips = [
    (180, "440", "≈70% 主战场", GOLD),
    (450, "+20", "理化实验 · 另算", GOLD),
    (720, "170", "中分段定公办民办", WHITE),
]
cw, chh, cy0 = 250, 100, 122
for cx, num, role, col in chips:
    x0, x1 = cx - cw / 2, cx + cw / 2
    rbox(d, im, [x0, cy0, x1, cy0 + chh], radius=18,
         fill_alpha=18, outline=GOLD if col == GOLD else EDGE,
         outline_alpha=140 if col == GOLD else 100, width=2)
    put(d, im, num, (cx, cy0 + 36), ImageFont.truetype(FB, 46), col, "mm", cw - 20, 900, 600, f"n{cx}")
    put(d, im, role, (cx, cy0 + 84), ImageFont.truetype(FR, 19),
        GOLD if col == GOLD else LIGHT, "mm", cw - 30, 900, 600, f"r{cx}")

# 3) 两列等高明细（各5行）——左：语数英物化笔试440；右：理化实验+史道体170
def srow(x0c, x1c, y, nm, sc, nt, gold_bg=False, score_col=None):
    if gold_bg:
        rbox(d, im, [x0c, y, x1c, y + 46], radius=12, fill=GOLD, fill_alpha=255)
    else:
        rbox(d, im, [x0c, y, x1c, y + 46], radius=12, fill=None, fill_alpha=10,
             outline=EDGE, outline_alpha=70, width=2)
    nmcol = NAVY if gold_bg else WHITE
    fnm = ImageFont.truetype(FB, 21)
    put(d, im, nm, (x0c + 18, y + 23), fnm, nmcol, "lm", 150, 900, 600, f"nm-{nm}")
    scpos = x1c - 18
    if nt:
        nx = x0c + 18 + fnm.getlength(nm) + 14
        put(d, im, nt, (nx, y + 23), ImageFont.truetype(FR, 15),
            NAVY if gold_bg else SUB, "lm", scpos - 64 - nx, 900, 600, f"nt-{nm}")
    put(d, im, sc, (scpos, y + 23), ImageFont.truetype(FB, 24),
        NAVY if gold_bg else (score_col or GOLD), "rm", 80, 900, 600, f"sc-{nm}")

LX0, LX1 = 60, 440     # 左列
RX0, RX1 = 470, 840    # 右列
yS = 292
# 左列5行：语文/数学/英语/物理/化学
for i, (nm, sc, nt) in enumerate([
        ("语文", "120", ""), ("数学", "100", ""), ("英语", "100", "笔试75+听口25"),
        ("物理", "70", ""), ("化学", "50", "")]):
    srow(LX0, LX1, yS + i * 52, nm, sc, nt)
# 右列5行：实验(金卡)/历史/道法/体育/170结论
r_items = [("理化实验", "+20", "操作考", True, GOLD), ("历史", "70", "", False, WHITE),
           ("道德与法治", "50", "开卷", False, WHITE), ("体育", "50", "过程14+现场36", False, WHITE)]
for i, (nm, sc, nt, gold, scol) in enumerate(r_items):
    srow(RX0, RX1, yS + i * 52, nm, sc, nt, gold_bg=gold, score_col=scol)
# 右列第5行 = md 结论卡
y5 = yS + 4 * 52
rbox(d, im, [RX0, y5, RX1, y5 + 46], radius=12, fill_alpha=18, outline=GOLD, outline_alpha=160, width=2)
put(d, im, "这 170 分 · 中等分段定公办民办", (655, y5 + 23),
    ImageFont.truetype(FB, 20), GOLD, "mm", 340, 900, 600, "md170")

im.save(OUT + "P1-1-子任务02-630构成卡-明细-口径修正-美化-900x600.png")
print("saved 内容卡 v3（美化）")
