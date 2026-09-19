# -*- coding: utf-8 -*-
"""P1-3 S4 D类三张牌 封面 · 精简版（对齐精简版规范 + 头条3图规则）

公众号 900×383（3行）+ 头条 1200×900（封面1主标题/封面2数据对撞/封面3答案行动）+ 小红书 1080×1440。
主标题=「D类不是死胡同」；钩子跨平台统一=「三张牌：指标生 · 民办 · 3+4」。
**套图视觉（2026-09-08 用户确认规律）**：主色统一深蓝系，本期=S4 档 royal 蓝 + 左上主光 + 左上→右下斜射光束，
与抖音分镜共用同一套"蓝系内光影差异化"语言；子任务之间靠深浅×光影×光线角度×装饰×版式区分，不换色相。
模板：S3 _build_s3_covers.py（版式沿用；底/光影换 royal 蓝·左光档）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (31, 76, 150); BOT = (13, 29, 72)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (162, 192, 238); SUB = (214, 227, 248)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"

KICK = "三张牌：指标生 · 民办 · 3+4"   # 一句金钩（跨平台统一）


def base(w, h, gx=0.26, gy=0.14):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    # 主光：左上 radial（光线角度=左上方，与抖音分镜同档）
    g = np.exp(-(((x - w * gx) / (w * 0.38)) ** 2 + ((y - h * gy) / (h * 0.32)) ** 2))
    a = a + np.array((196, 214, 250), float)[None, None, :] * (g * 0.13)[..., None]
    # 左上→右下斜射光束（同抖音分镜光线角度）
    for k, amp, wid in [(0.32, 0.09, 0.30 * w), (0.95, 0.06, 0.24 * w)]:
        u = x - k * y
        g2 = np.exp(-((u / wid) ** 2))
        a = a + np.array((205, 222, 252), float)[None, None, :] * (g2 * amp)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-w * .18, -h * .10, w * .26, h * .18], fill=TOP + (46,))
    od.ellipse([w * .78, h * .80, w * 1.1, h * 1.08], fill=TOP + (24,))
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


# ---------- 公众号 900×383 精简版（3行） ----------
W, H = 900, 383
im, d = base(W, H)
put(d, "深圳中考", (W / 2, 52), 40, GOLD, maxw=860, tag="gzh")
f = put(d, "D类不是死胡同", (W / 2, 168), 58, WHITE, maxw=880, min_size=48, tag="gzh")
bb = d.textbbox((W / 2, 168), "D类不是死胡同", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 4
d.line([W / 2 - half, 232, W / 2 + half, 232], fill=GOLD, width=5)
put(d, KICK, (W / 2, 318), 40, GOLD, maxw=880, min_size=34, tag="gzh")
im.save(HERE + "01.公众号/P1-3-S4-D类三张牌-公众号-封面-精炼版-900x383.png")
print("saved 公众号封面 精炼版")

# ---------- 今日头条 1200×900 · 封面1 主标题 ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 非深户报考", 120, 42, W)
f = put(d, "D类不是死胡同？", (W / 2, 360), 124, WHITE, maxw=1120, min_size=100, tag="tt1")
bb = d.textbbox((W / 2, 360), "D类不是死胡同？", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 6
d.line([W / 2 - half, 500, W / 2 + half, 500], fill=GOLD, width=6)
put(d, KICK, (W / 2, 640), 70, GOLD, maxw=1120, min_size=56, tag="tt1")
put(d, "数据来源：深圳市教育局2026招生计划与第一批录取标准 · 人工核对", (W / 2, 856), 24, SUB, bold=False, min_size=18, tag="tt1")
im.save(HERE + "02.今日头条/P1-3-S4-D类三张牌-头条-封面1-主标题-1200x900.png")
print("saved 头条封面1-主标题")

# ---------- 今日头条 · 封面2 数据对撞（23分 vs 0分差） ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · D类出路", 120, 42, W)
put(d, "23 分", (W * 0.30, 430), 150, GOLD, maxw=420, min_size=120, tag="tt2")
put(d, "公办边缘 D类要多考", (W * 0.30, 585), 42, WHITE, maxw=480, min_size=34, tag="tt2")
put(d, "0 分差", (W * 0.70, 430), 150, WHITE, maxw=420, min_size=120, tag="tt2")
put(d, "民办 · 3+4 都 ACD 同线", (W * 0.70, 585), 42, WHITE, maxw=480, min_size=34, tag="tt2")
d.line([(W / 2, 300), (W / 2, 660)], fill=GOLD, width=4)
put(d, "分数线上挤不过公办？还有同一条线的路", (W / 2, 745), 52, GOLD, maxw=1120, min_size=42, tag="tt2")
put(d, "数据来源：深圳市教育局2026招生计划与第一批录取标准 · 人工核对", (W / 2, 856), 24, SUB, bold=False, min_size=18, tag="tt2")
im.save(HERE + "02.今日头条/P1-3-S4-D类三张牌-头条-封面2-数据对撞-1200x900.png")
print("saved 头条封面2-数据对撞")

# ---------- 今日头条 · 封面3 答案/行动（别只看分数线 · 把三张牌摆上桌） ----------
W, H = 1200, 900
im, d = base(W, H)
pill(d, "深圳中考 · 备考策略", 120, 42, W)
put(d, "别只看分数线", (W / 2, 380), 122, WHITE, maxw=1120, min_size=98, tag="tt3")
put(d, "把三张牌摆上桌", (W / 2, 570), 122, GOLD, maxw=1120, min_size=98, tag="tt3")
d.line([(W / 2 - 260, 676), (W / 2 + 260, 676)], fill=GOLD, width=5)
put(d, "对号入座再选：指标生 · 民办 · 3+4", (W / 2, 760), 52, LIGHT, maxw=1120, min_size=42, tag="tt3")
put(d, "数据来源：深圳市教育局2026招生计划与第一批录取标准 · 人工核对", (W / 2, 856), 24, SUB, bold=False, min_size=18, tag="tt3")
im.save(HERE + "02.今日头条/P1-3-S4-D类三张牌-头条-封面3-答案行动-1200x900.png")
print("saved 头条封面3-答案行动")

# ---------- 小红书 1080×1440（精简版） ----------
W, H = 1080, 1440
im, d = base(W, H, gy=0.12)
put(d, "深圳中考", (W / 2, 180), 96, GOLD, maxw=1000, tag="xhs")
f = put(d, "D类不是死胡同", (W / 2, 560), 126, WHITE, maxw=1000, min_size=104, tag="xhs")
bb = d.textbbox((W / 2, 560), "D类不是死胡同", font=f, anchor="mm")
half = (bb[2] - bb[0]) / 2 + 8
d.line([W / 2 - half, 700, W / 2 + half, 700], fill=GOLD, width=8)
put(d, KICK, (W / 2, 966), 70, GOLD, maxw=1000, min_size=56, tag="xhs")
put(d, "非深户出路 · 收藏不迷路 · 数据2026官方", (W / 2, 1360), 30, SUB, bold=False, maxw=980, min_size=24, tag="xhs")
im.save(HERE + "04.小红书/P1-3-S4-D类三张牌-小红书-封面-精炼版-1080x1440.png")
print("saved 小红书封面")
print("done")
