# -*- coding: utf-8 -*-
"""P1-3 S5 AC类别松懈 抖音口播分镜 ×6（1080×1920）

主色调：统一深蓝系（**steel 冷蓝档**，去饱和偏灰，区别于 S4 royal / 主线 navy），不换色相。
光影差异化：主光在**右上** + 右上→左下**斜射光束**（与 S4 左上光方向相反）+ **同心圆环装饰**（右上）+ 数据/大字版式。
安全区：正文右缘≤950、下界≤1590；底部 y≥1600 留空给字幕/图标。
镜头：01 反转钩子 / 02 名额结构(77%) / 03 坎①AC线硬线 / 04 坎②本校AC抢 / 05 坎③顶尖0分差 / 06 CTA+预告S6。
口径：深户AC占公办约77% / 四大0分差 / 指标生=本校AC抢——官方结论数字；不给具体校AC线、不给校例。
模板：S4 _build_s4_dy_shots.py（家族函数）换深浅档+换光向+换装饰。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (46, 78, 132); BOT = (14, 24, 50)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (168, 196, 238); SUB = (214, 228, 248)
CARD = (24, 44, 88); EDGE = (84, 128, 200)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


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
    # 同心圆环（右上，区别于 S4 金章点阵 / 主线无装饰）
    for rw in [0.10, 0.19, 0.28]:
        x0, y0 = W * 1.02 - rw * W, -H * 0.02 - rw * W
        x1, y1 = W * 1.02 + rw * W, -H * 0.02 + rw * W
        od.ellipse([x0, y0, x1, y1], outline=(245, 198, 107, 50), width=4)
    od.ellipse([-W * .22, -H * .05, W * .22, H * .16], fill=(40, 60, 110, 55))
    od.ellipse([W * .84, H * .90, W * 1.14, H * 1.07], fill=(10, 16, 40, 46))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def ctext(d, text, xy, size, fill, bold=True, maxw=820, min_size=36, tag=""):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BADS.append((tag or text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE, radius=26):
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=wfill, outline=wout, width=3)


def header(d, tag):
    f = ctext(d, "深圳中考", (W / 2, 130), 92, GOLD, maxw=820, min_size=72, tag="H")
    bb = d.textbbox((W / 2, 130), "深圳中考", font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 6
    d.line([W / 2 - half, 214, W / 2 + half, 214], fill=GOLD, width=6)
    f2 = ImageFont.truetype(FB, 40)
    bb2 = d.textbbox((0, 0), tag, font=f2)
    tw = bb2[2] - bb2[0]
    pad = 40
    d.rounded_rectangle([W / 2 - tw / 2 - pad, 252, W / 2 + tw / 2 + pad, 352], radius=50, outline=GOLD, width=3)
    d.text((W / 2, 302), tag, font=f2, fill=LIGHT, anchor="mm")
    BADS.append((tag[:12], (W / 2 - tw / 2 - pad, 252, W / 2 + tw / 2 + pad, 352)))


def check(name):
    bad = []
    for tagn, bb in BADS:
        if bb[0] < 26 or bb[2] > 950:
            bad.append((tagn + " 右", tuple(int(v) for v in bb)))
        if bb[1] < 60 or bb[3] > 1590:
            bad.append((tagn + " 下", tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, bad if bad else "")
    BADS.clear()


# 镜头01 反转钩子
im, d = base(); header(d, "S5 · AC类别松懈")
ctext(d, "深户，也别觉得稳了", (W / 2, 620), 88, WHITE, maxw=900, min_size=70, tag="01")
ctext(d, "AC类不缺名额 · 坎在后面", (W / 2, 800), 52, GOLD, maxw=880, min_size=42, tag="01")
rcard(d, 80, 950, W - 80, 1170)
ctext(d, "公办8万学位 · 深户占约77%", (W / 2, 1022), 44, WHITE, maxw=860, min_size=36, tag="01")
ctext(d, "但你冲的是目标校 · 不是随便一所", (W / 2, 1112), 34, LIGHT, bold=False, maxw=880, min_size=28, tag="01")
ctext(d, "先把这个误区放下", (W / 2, 1420), 46, WHITE, min_size=38, tag="01")
check("镜头01")
im.save(HERE + "P1-3-S5-AC类别松懈-抖音-镜头01-深户也别觉得稳了-1080x1920.png")

# 镜头02 名额结构
im, d = base(); header(d, "公办名额 · 深户AC类")
ctext(d, "77%", (W / 2, 640), 172, GOLD, maxw=700, min_size=130, tag="02")
ctext(d, "公办名额里 深户拿走的大头", (W / 2, 830), 46, WHITE, maxw=900, min_size=38, tag="02")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "AC类 61,797·约77%　D类 18,506·约23%", (W / 2, 1020), 36, WHITE, maxw=760, min_size=28, tag="02")
ctext(d, "总 80,303 / 101所公办 · 2026", (W / 2, 1104), 32, LIGHT, bold=False, maxw=880, min_size=26, tag="02")
ctext(d, "所以你的坎 · 不在名额", (W / 2, 1400), 46, WHITE, min_size=38, tag="02")
check("镜头02")
im.save(HERE + "P1-3-S5-AC类别松懈-抖音-镜头02-名额77-1080x1920.png")

# 镜头03 坎① AC线是硬线
im, d = base(); header(d, "坎① · AC线是硬线")
ctext(d, "AC线是硬线", (W / 2, 640), 118, WHITE, maxw=880, min_size=96, tag="03")
ctext(d, "想进哪所 · 看它当年 AC 线", (W / 2, 820), 50, GOLD, maxw=900, min_size=40, tag="03")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "差一分，就是进不去", (W / 2, 1016), 46, WHITE, maxw=860, min_size=38, tag="03")
ctext(d, "深户只是能报的范围更大 · 不是免死金牌", (W / 2, 1104), 33, LIGHT, bold=False, maxw=880, min_size=27, tag="03")
ctext(d, "别拿“深户”当加分", (W / 2, 1400), 46, WHITE, min_size=38, tag="03")
check("镜头03")
im.save(HERE + "P1-3-S5-AC类别松懈-抖音-镜头03-AC线硬线-1080x1920.png")

# 镜头04 坎② 指标生=本校AC抢
im, d = base(); header(d, "坎② · 指标生")
ctext(d, "本校AC之间抢", (W / 2, 640), 116, WHITE, maxw=880, min_size=94, tag="04")
ctext(d, "名额到校 · AC 单列", (W / 2, 820), 50, GOLD, maxw=880, min_size=40, tag="04")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "报同一校指标生 → 拼校内 AC 位次", (W / 2, 1016), 40, WHITE, maxw=880, min_size=32, tag="04")
ctext(d, "不是和全市深户比 · 是本校择优", (W / 2, 1104), 33, LIGHT, bold=False, maxw=880, min_size=27, tag="04")
ctext(d, "校内排不上 · 宽通道也窄", (W / 2, 1400), 46, WHITE, min_size=38, tag="04")
check("镜头04")
im.save(HERE + "P1-3-S5-AC类别松懈-抖音-镜头04-本校AC抢-1080x1920.png")

# 镜头05 坎③ 顶尖0分差
im, d = base(); header(d, "坎③ · 顶尖层")
ctext(d, "0 分差", (W / 2, 640), 172, GOLD, maxw=700, min_size=130, tag="05")
ctext(d, "四大 AC=D 同线", (W / 2, 830), 48, WHITE, maxw=880, min_size=40, tag="05")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "冲到顶尖 → 对手里有 D 类尖子", (W / 2, 1016), 40, WHITE, maxw=880, min_size=32, tag="05")
ctext(d, "纯拼分 · 深户身份在这没用", (W / 2, 1104), 33, LIGHT, bold=False, maxw=880, min_size=27, tag="05")
ctext(d, "没有“深户加成”", (W / 2, 1400), 46, WHITE, min_size=38, tag="05")
check("镜头05")
im.save(HERE + "P1-3-S5-AC类别松懈-抖音-镜头05-顶尖零分差-1080x1920.png")

# 镜头06 CTA
im, d = base(); header(d, "S5 · 一句话记牢")
ctext(d, "深户不缺名额", (W / 2, 560), 88, WHITE, maxw=880, min_size=70, tag="06")
ctext(d, "缺的是 把位次排到目标校前面", (W / 2, 740), 46, GOLD, maxw=900, min_size=38, tag="06")
rcard(d, 80, 940, W - 80, 1160)
ctext(d, "查本校AC位次 · 摆出目标校AC线", (W / 2, 1016), 40, WHITE, maxw=880, min_size=32, tag="06")
ctext(d, "把“我是深户”从安慰剂 变成起点", (W / 2, 1104), 34, LIGHT, bold=False, maxw=880, min_size=28, tag="06")
ctext(d, "关注我 · 下条：现在该做的4件事", (W / 2, 1440), 54, WHITE, min_size=44, tag="06")
check("镜头06")
im.save(HERE + "P1-3-S5-AC类别松懈-抖音-镜头06-CTA-1080x1920.png")
print("done")
