# -*- coding: utf-8 -*-
"""P1-3 S5 AC类别松懈 封面 · 精简版（对齐精简版规范 + 头条3图规则）

公众号 900×383 + 头条 1200×900（封面1主标题/封面2数据对撞/封面3答案行动）+ 小红书 1080×1440。
主标题=「深户别松气」；钩子=「AC类不缺名额 · 缺的是目标校位次」。
**套图视觉（用户2026-09-08 定稿规律）**：主色统一深蓝系；S5 档 = steel 冷蓝 + **右上主光 + 右上→左下斜射光束 + 同心圆环装饰**，
与 S4(royal·左上光) / 主线(navy·居中) 只差深浅×光影×角度×装饰，不换色相。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (46, 78, 132); BOT = (14, 24, 50)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (168, 196, 238); SUB = (214, 228, 248)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"

KICK = "AC类不缺名额 · 缺的是目标校位次"   # 一句金钩（跨平台统一）


def rings(d, w, h, cx=0.84, cy=0.08):
    for i, rw in enumerate([0.10, 0.19, 0.28]):
        x0, y0 = cx * w - rw * w, cy * h - rw * w
        x1, y1 = cx * w + rw * w, cy * h + rw * w
        col = (245, 198, 107, 46) if i == 0 else (255, 255, 255, 20)
        d.ellipse([x0, y0, x1, y1], outline=col, width=3)


def base(w, h, gx=0.82, gy=0.12):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    # 主光：右上 radial（光线角度=右上方，与 S4 左光相反）
    g = np.exp(-(((x - w * gx) / (w * 0.36)) ** 2 + ((y - h * gy) / (h * 0.30)) ** 2))
    a = a + np.array((205, 222, 250), float)[None, None, :] * (g * 0.13)[..., None]
    # 右上→左下斜射光束（镜像 S4 方向）
    for k, amp, wid in [(0.32, 0.09, 0.30 * w), (0.95, 0.06, 0.24 * w)]:
        u = (w - x) - k * y
        g2 = np.exp(-((u / wid) ** 2))
        a = a + np.array((210, 226, 252), float)[None, None, :] * (g2 * amp)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    rings(od, w, h)
    od.ellipse([-w * .16, -h * .86, w * .20, h * .24], fill=(30, 46, 90, 40))  # 左下反向补光
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, bold=True, maxw=None, min_size=18, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else 860
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


def pill(d, text, cy, size, w, pad=30):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > w - 220:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (w - tw) / 2 - pad, (w + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((w / 2, cy), text, font=f, fill=WHITE, anchor="mm")


# ---------- 公众号 900×383 ----------
W, H = 900, 383
im, d = base(W, H)
put(d, "深圳中考", (W / 2, 52), 40, GOLD, maxw=860, tag="gzh")
f = put(d, "深户，也别觉得稳了", (W / 2, 166), 58, WHITE, maxw=880, min_size=48, tag="gzh")
bb = d.textbbox((W / 2, 166), "深户，也别觉得稳了", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 232, W / 2 + half, 232], fill=GOLD, width=5)
put(d, KICK, (W / 2, 320), 40, GOLD, maxw=880, min_size=33, tag="gzh")
im.save(HERE + "01.公众号/P1-3-S5-AC类别松懈-公众号-封面-精炼版-900x383.png")
print("saved 公众号封面")

# ---------- 头条 1200×900 · 封面1 主标题 ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 深户AC类", 120, 42, W)
f = put(d, "深户，也别觉得稳了", (W / 2, 360), 120, WHITE, maxw=1120, min_size=96, tag="tt1")
bb = d.textbbox((W / 2, 360), "深户，也别觉得稳了", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 500, W / 2 + half, 500], fill=GOLD, width=6)
put(d, KICK, (W / 2, 636), 66, GOLD, maxw=1120, min_size=52, tag="tt1")
put(d, "数据来源：深圳市教育局2026公办普高招生计划 · 逐校求和核对", (W / 2, 856), 24, SUB, bold=False, min_size=18, tag="tt1")
im.save(HERE + "02.今日头条/P1-3-S5-AC类别松懈-头条-封面1-主标题-1200x900.png")
print("saved 头条封面1")

# ---------- 头条 · 封面2 数据对撞（77% vs 23%） ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 公办名额结构", 120, 42, W)
put(d, "77%", (W * 0.30, 430), 150, GOLD, maxw=420, min_size=120, tag="tt2")
put(d, "公办名额 · 深户AC类", (W * 0.30, 585), 44, WHITE, maxw=470, min_size=36, tag="tt2")
put(d, "23%", (W * 0.70, 430), 150, WHITE, maxw=420, min_size=120, tag="tt2")
put(d, "公办名额 · D类", (W * 0.70, 585), 44, WHITE, maxw=470, min_size=36, tag="tt2")
d.line([(W / 2, 300), (W / 2, 660)], fill=GOLD, width=4)
put(d, "名额不缺 · 缺的是目标校位次", (W / 2, 745), 54, GOLD, maxw=1120, min_size=44, tag="tt2")
put(d, "数据来源：深圳市教育局2026公办普高招生计划 · 逐校求和核对", (W / 2, 856), 24, SUB, bold=False, min_size=18, tag="tt2")
im.save(HERE + "02.今日头条/P1-3-S5-AC类别松懈-头条-封面2-数据对撞-1200x900.png")
print("saved 头条封面2")

# ---------- 头条 · 封面3 答案/行动 ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
put(d, "把位次排上去", (W / 2, 380), 120, WHITE, maxw=1120, min_size=96, tag="tt3")
put(d, "别拿深户当免死金牌", (W / 2, 566), 116, GOLD, maxw=1120, min_size=94, tag="tt3")
d.line([(W / 2 - 260, 676), (W / 2 + 260, 676)], fill=GOLD, width=5)
put(d, "查本校AC位次 · 摆出目标校AC线", (W / 2, 762), 52, LIGHT, maxw=1120, min_size=42, tag="tt3")
put(d, "数据来源：深圳市教育局2026公办普高招生计划 · 逐校求和核对", (W / 2, 856), 24, SUB, bold=False, min_size=18, tag="tt3")
im.save(HERE + "02.今日头条/P1-3-S5-AC类别松懈-头条-封面3-答案行动-1200x900.png")
print("saved 头条封面3")

# ---------- 小红书 1080×1440 ----------
W, H = 1080, 1440
im, d = base(W, H, gy=0.11)
put(d, "深圳中考", (W / 2, 180), 96, GOLD, maxw=1000, tag="xhs")
f = put(d, "深户，也别觉得稳了", (W / 2, 560), 124, WHITE, maxw=1000, min_size=102, tag="xhs")
bb = d.textbbox((W / 2, 560), "深户，也别觉得稳了", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 700, W / 2 + half, 700], fill=GOLD, width=8)
put(d, KICK, (W / 2, 960), 68, GOLD, maxw=1000, min_size=54, tag="xhs")
put(d, "深户AC类 · 收藏不迷路 · 数据2026官方", (W / 2, 1360), 30, SUB, bold=False, maxw=980, min_size=24, tag="xhs")
im.save(HERE + "04.小红书/P1-3-S5-AC类别松懈-小红书-封面-精炼版-1080x1440.png")
print("saved 小红书封面")
print("done")
