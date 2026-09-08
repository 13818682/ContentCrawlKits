# -*- coding: utf-8 -*-
"""P1-3 S5 AC类别松懈 小红书正文图卡 ×4（1080×1440，封面另有精炼版）
正文图1-名额结构总览(收藏) / 图2-AC线硬线 / 图3-指标生本校AC抢 / 图4-顶尖0分差。
口径：AC 61,797(约77%)/D 18,506(约23%)/总80,303·101所、四大0分差——官方结论；不给具体校AC线、不给校例。
**套图视觉（2026-09-08 定稿规律）**：深蓝系 steel 冷蓝档 + 右上主光 + 右上→左下斜光 + 同心圆环；与 S4(royal·左光) 只差深浅×光影×角度×装饰。
模板：S4 _build_s4_xhs_cards.py（函数族）换档+换光向+换装饰。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (46, 78, 132); BOT = (14, 24, 50)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (168, 196, 238); SUB = (214, 228, 248)
CARD = (24, 44, 88); EDGE = (84, 128, 200)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440
HM = 80
BOXES = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.84) / (W * 0.34)) ** 2 + ((y - H * 0.10) / (H * 0.30)) ** 2))
    a = a + np.array((205, 222, 250), float)[None, None, :] * (g * 0.12)[..., None]
    for k, amp, wid in [(0.32, 0.08, 300), (0.95, 0.05, 240)]:
        u = (W - x) - k * y
        g2 = np.exp(-((u / wid) ** 2))
        a = a + np.array((210, 226, 252), float)[None, None, :] * (g2 * amp)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for rw in [0.12, 0.22]:
        od.ellipse([W * 1.04 - rw * W, -H * 0.03 - rw * W, W * 1.04 + rw * W, -H * 0.03 + rw * W],
                   outline=(245, 198, 107, 40), width=4)
    od.ellipse([-W * .18, -H * .05, W * .20, H * .16], fill=(40, 60, 110, 55))
    od.ellipse([W * .84, H * .90, W * 1.12, H * 1.07], fill=(10, 16, 40, 40))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def center(d, text, xy, size, fill, bold=True, maxw=None, min_size=22):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else W - 2 * HM
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "center too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BOXES.append(("C:" + text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def left(d, text, xy, size, fill, right=None, bold=False, min_size=20):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    r = right if right else W - HM - 10
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= (r - xy[0]) + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= (r - xy[0]) + 1, "left too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="lm")
    BOXES.append(("L:" + text[:14], d.textbbox(xy, text, font=f, anchor="lm")))
    return f


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE, rad=22):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=wfill, outline=wout, width=2)


def footer(d):
    center(d, "数据来源：深圳市教育局2026公办普高招生计划 · 逐校求和核对", (W / 2, 1390), 21, SUB, bold=False, min_size=16)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 6:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ========== 正文图1：名额结构总览（收藏） ==========
im, d = base()
center(d, "S5 · 深户AC类", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "公办名额 · 深户不缺", (W / 2, 210), 54, WHITE, min_size=44)
center(d, "2026 公办普高招生计划 · 101所", (W / 2, 296), 28, LIGHT, bold=False, min_size=22)
tiles = [
    ("80,303", "公办学位总数"),
    ("61,797 · 77%", "AC类(深户)名额"),
    ("18,506 · 23%", "D类名额"),
]
tw, th, gap = 280, 216, 24
x0 = (W - (tw * 3 + gap * 2)) / 2
for i, (big, lab) in enumerate(tiles):
    x = x0 + i * (tw + gap)
    rcard(d, x, 360, x + tw, 360 + th)
    center(d, big, (x + tw / 2, 438), 46, GOLD if i == 1 else WHITE, maxw=tw - 24, min_size=34)
    center(d, lab, (x + tw / 2, 530), 25, LIGHT, bold=False, min_size=20)
center(d, "名额结构：大头在深户 → 你的坎不是名额", (W / 2, 668), 34, WHITE, min_size=28)
rows = [
    ("🚧 坎①", "AC 线是硬线", "目标校普通通道 · 差一分进不去"),
    ("🎯 坎②", "指标生 = 本校AC抢", "名额到校 · 拼校内 AC 位次"),
    ("⚔️ 坎③", "顶尖层 0 分差", "四大 AC=D · 对手里有 D 尖子"),
]
y = 740
for lab, t, s in rows:
    y1 = y + 150
    rcard(d, HM, y, W - HM, y1)
    left(d, lab, (HM + 60, (y + y1) / 2), 40, GOLD, min_size=32)
    left(d, t, (HM + 250, y + 52), 38, WHITE, bold=True, min_size=30)
    left(d, s, (HM + 250, y + 116), 27, LIGHT, min_size=22)
    y = y1 + 18
center(d, "深户缺的不是名额 · 是目标校里的位次", (W / 2, 1320), 34, WHITE, min_size=28)
footer(d)
check("正文图1")
im.save(HERE + "P1-3-S5-AC类别松懈-小红书-正文图1-名额结构总览-1080x1440.png")

# ========== 正文图2：AC线是硬线 ==========
im, d = base()
center(d, "坎① · AC线是硬线", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "差一分 · 就是进不去", (W / 2, 260), 58, WHITE, min_size=48)
center(d, "想进哪所公办 · 普通通道看它当年 AC 线", (W / 2, 356), 30, LIGHT, bold=False, min_size=24)
rows = [
    ("深户 ≠ 免死金牌", "能报的范围更大，不等于进得去"),
    ("AC 线 = 硬门槛", "够线才进 · 不够线就是不够线"),
    ("同分有规则", "同分比的是末位同分比较，不看户口"),
]
y = 430
for t, s in rows:
    y1 = y + 148
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 60, y + 56), 38, WHITE, bold=True, min_size=30)
    left(d, s, (HM + 60, y + 116), 27, LIGHT, min_size=22)
    y = y1 + 16
center(d, "把 2-3 所目标校的 AC 线贴桌上", (W / 2, 1030), 34, WHITE, min_size=28)
center(d, "先回答：够不够得着 · 差多少", (W / 2, 1100), 28, LIGHT, bold=False, min_size=23)
center(d, "别拿“深户”当加分", (W / 2, 1290), 40, GOLD, min_size=32)
footer(d)
check("正文图2")
im.save(HERE + "P1-3-S5-AC类别松懈-小红书-正文图2-AC线硬线-1080x1440.png")

# ========== 正文图3：指标生=本校AC抢 ==========
im, d = base()
center(d, "坎② · 指标生", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "本校 AC 之间抢", (W / 2, 260), 62, WHITE, min_size=50)
center(d, "报同一校指标生 · 比的是本校 AC 位次，不是全市", (W / 2, 360), 30, LIGHT, bold=False, min_size=24)
rows = [
    ("① 名额到校", "公办指标生名额分到各初中"),
    ("② AC 类单列", "深户孩子只和本校深户比"),
    ("③ 看位次", "校内 AC 排名靠前 → 通道才宽"),
]
y = 440
for t, s in rows:
    y1 = y + 140
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 60, y + 56), 38, WHITE, bold=True, min_size=30)
    left(d, s, (HM + 60, y + 116), 27, LIGHT, min_size=22)
    y = y1 + 16
center(d, "现在做：问本校 AC 指标名额 + 估孩子位次", (W / 2, 1028), 33, WHITE, min_size=27)
center(d, "校内排不上 · 宽通道也窄", (W / 2, 1292), 40, GOLD, min_size=32)
footer(d)
check("正文图3")
im.save(HERE + "P1-3-S5-AC类别松懈-小红书-正文图3-指标生本校AC抢-1080x1440.png")

# ========== 正文图4：顶尖层 0分差 ==========
im, d = base()
center(d, "坎③ · 顶尖层", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "0 分差", (W / 2, 320), 170, GOLD, min_size=140)
center(d, "四大 2026 · AC=D 同一条线", (W / 2, 520), 46, WHITE, min_size=38)
rows = [
    ("四大全部同分进", "深中/深外/深实验/深高 AC=D"),
    ("冲到最顶尖那层", "你的对手里有 D 类尖子"),
    ("纯拼分", "深户身份在这里无优势"),
]
y = 610
for t, s in rows:
    y1 = y + 132
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 60, y + 50), 36, WHITE, bold=True, min_size=28)
    left(d, s, (HM + 60, y + 106), 26, LIGHT, min_size=21)
    y = y1 + 16
center(d, "冲四大：别默认“D类考不过我们”", (W / 2, 1050), 32, WHITE, min_size=26)
center(d, "顶尖层没户籍差 · 谁分高谁进", (W / 2, 1300), 40, GOLD, min_size=32)
footer(d)
check("正文图4")
im.save(HERE + "P1-3-S5-AC类别松懈-小红书-正文图4-顶尖零分差-1080x1440.png")
print("done")
