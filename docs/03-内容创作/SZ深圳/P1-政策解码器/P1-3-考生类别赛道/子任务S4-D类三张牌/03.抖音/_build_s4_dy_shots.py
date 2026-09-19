# -*- coding: utf-8 -*-
"""P1-3 S4 D类三张牌 抖音口播分镜 ×6（1080×1920）

主色调：**统一深蓝系（royal/steel 蓝档）**，不换色相。与其它子任务的区分只来自
"蓝色深浅 × 光影方向 × 光线角度 × 装饰纹理 × 版式"（QA 系列既定视觉语言），而非换成绿/紫等异色：
- 深浅档：royal 蓝（较主线 navy 更饱和、较 S2 青蓝更纯蓝、较 S3 紫罗兰去红向）
- 光影/角度：光源取**左上方** + 左上→右下**斜射光束带** + 顶部左侧暖光晕（区别于 S3 顶部居中光+右竖条）
- 装饰：右缘三枚金章"牌点阵"（三张牌语义，家族统一金强调）
版式：顶部「深圳中考」金字大字（家族统一）+ 金章小标（圆角章）。
安全区：正文右缘≤950、下界≤1590；底部 y≥1600 留空给字幕/图标。
镜头：01 反转型钩子 / 02 牌①指标生(同校比) / 03 牌②民办(同一条线)
 / 04 牌③3+4贯通(职校3+本科4) / 05 没有白送的牌(三代价) / 06 CTA+预告S5(AC类)。
口径：2026官方结论数字（民办49所/33,195学位/ACD同线；3+4共300名额/D类可报；指标生全覆盖），不给民办分档分数线、不给3+4专业线。
模板：S3 _build_s3_dy_shots.py（家族函数）换深浅档+换光影角度+换装饰。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
# royal 蓝档（深蓝系内更饱和一档；光影：左上主光 + 斜射光束）
TOP = (31, 76, 150); BOT = (13, 29, 72)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (162, 192, 238); SUB = (214, 227, 248)
CARD = (20, 46, 100); EDGE = (70, 118, 196)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    # 主光：左上方 radial 暖光（角度区别于 S3 顶部居中光 / S2 视觉）
    g = np.exp(-(((x - W * 0.20) / (W * 0.42)) ** 2 + ((y - H * 0.12) / (H * 0.34)) ** 2))
    a = a + np.array((196, 214, 250), float)[None, None, :] * (g * 0.13)[..., None]
    # 左上→右下斜射光束（模拟侧面入射光角度 ~30°），沿 u = x - k*y 形成亮纹
    for k, amp, wid in [(0.32, 0.10, 320), (0.95, 0.07, 260)]:
        u = x - k * y
        g2 = np.exp(-((u / wid) ** 2))
        a = a + np.array((205, 222, 252), float)[None, None, :] * (g2 * amp)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    # 装饰：右缘三枚金章"牌点阵"（三张牌语义；区别于 S3 右竖条 / 主线无装饰）
    for i in range(3):
        cy = 700 + i * 320
        od.rounded_rectangle([876, cy - 26, 928, cy + 26], radius=26, outline=(245, 198, 107, 72), width=6)
    od.ellipse([-W * .22, -H * .05, W * .22, H * .16], fill=(44, 74, 140, 60))
    od.ellipse([W * .84, H * .88, W * 1.14, H * 1.06], fill=(12, 26, 64, 40))
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
    """顶部深圳中考大字 + 金章小标（圆角章·本档装饰）"""
    f = ctext(d, "深圳中考", (W / 2, 130), 92, GOLD, maxw=820, min_size=72, tag="H")
    bb = d.textbbox((W / 2, 130), "深圳中考", font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 6
    d.line([W / 2 - half, 214, W / 2 + half, 214], fill=GOLD, width=6)
    f2 = ImageFont.truetype(FB, 40)
    bb2 = d.textbbox((0, 0), tag, font=f2)
    tw = bb2[2] - bb2[0]
    pad = 40
    d.rounded_rectangle([W / 2 - tw / 2 - pad, 250, W / 2 + tw / 2 + pad, 350], radius=50,
                        outline=GOLD, width=3)
    d.text((W / 2, 300), tag, font=f2, fill=LIGHT, anchor="mm")
    BADS.append((tag[:12], (W / 2 - tw / 2 - pad, 250, W / 2 + tw / 2 + pad, 350)))


def check(name):
    bad = []
    for tagn, bb in BADS:
        if bb[0] < 26 or bb[2] > 950:
            bad.append((tagn + " 右", tuple(int(v) for v in bb)))
        if bb[1] < 60 or bb[3] > 1590:
            bad.append((tagn + " 下", tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, bad if bad else "")
    BADS.clear()


# 镜头01 反转型钩子
im, d = base(); header(d, "S4 · D类三张牌")
ctext(d, "D类不是死胡同？", (W / 2, 600), 92, WHITE, maxw=880, min_size=74, tag="01")
ctext(d, "出路，不止公办一条", (W / 2, 792), 56, GOLD, maxw=880, min_size=46, tag="01")
rcard(d, 80, 960, W - 80, 1180)
ctext(d, "指标生 · 民办 · 3+4", (W / 2, 1028), 46, WHITE, maxw=820, min_size=38, tag="01")
ctext(d, "三张牌 = 把混战变小 · 把线拉平 · 换赛道", (W / 2, 1120), 34, LIGHT, bold=False, maxw=840, min_size=28, tag="01")
ctext(d, "D类难在：没人把话讲全", (W / 2, 1440), 46, WHITE, maxw=820, min_size=38, tag="01")
check("镜头01")
im.save(HERE + "P1-3-S4-D类三张牌-抖音-镜头01-D类不是死胡同-1080x1920.png")

# 镜头02 牌① 指标生
im, d = base(); header(d, "牌① · 指标生")
ctext(d, "指标生", (W / 2, 620), 148, WHITE, maxw=820, min_size=116, tag="02")
ctext(d, "把“和全市抢”变成“和同校比”", (W / 2, 836), 50, GOLD, maxw=880, min_size=40, tag="02")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "名额到校 · D 类单列", (W / 2, 1016), 46, WHITE, maxw=820, min_size=38, tag="02")
ctext(d, "报同一校指标生 → 拼校内 D 类位次", (W / 2, 1104), 34, LIGHT, bold=False, maxw=840, min_size=28, tag="02")
ctext(d, "目标公办 · 先查本校 D 类名额", (W / 2, 1400), 46, WHITE, min_size=38, tag="02")
check("镜头02")
im.save(HERE + "P1-3-S4-D类三张牌-抖音-镜头02-指标生-1080x1920.png")

# 镜头03 牌② 民办
im, d = base(); header(d, "牌② · 民办普高")
ctext(d, "同一条线", (W / 2, 620), 142, WHITE, maxw=840, min_size=114, tag="03")
ctext(d, "民办录取 · AC / D 一视同仁", (W / 2, 836), 52, GOLD, maxw=880, min_size=42, tag="03")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "49 所民办 · 三万三千学位", (W / 2, 1016), 44, WHITE, maxw=820, min_size=36, tag="03")
ctext(d, "够不到公办 D 线 · 这里也有普高可上", (W / 2, 1104), 34, LIGHT, bold=False, maxw=840, min_size=28, tag="03")
ctext(d, "线低换学费高 · 兜底不是首选", (W / 2, 1400), 44, WHITE, min_size=36, tag="03")
check("镜头03")
im.save(HERE + "P1-3-S4-D类三张牌-抖音-镜头03-民办同一条线-1080x1920.png")

# 镜头04 牌③ 3+4
im, d = base(); header(d, "牌③ · 3+4 中本贯通")
ctext(d, "3+4 贯通", (W / 2, 620), 142, WHITE, maxw=860, min_size=112, tag="04")
ctext(d, "职校3年 + 本科4年 = 本科文凭", (W / 2, 836), 50, GOLD, maxw=880, min_size=40, tag="04")
rcard(d, 80, 950, W - 80, 1150)
ctext(d, "300 名额试点 · D 类可报 · 同线", (W / 2, 1016), 44, WHITE, maxw=820, min_size=36, tag="04")
ctext(d, "走中职批次 · 不进公办 D 类名额池", (W / 2, 1104), 34, LIGHT, bold=False, maxw=840, min_size=28, tag="04")
ctext(d, "第一批试点 · 知道的人还不多", (W / 2, 1400), 44, WHITE, min_size=36, tag="04")
check("镜头04")
im.save(HERE + "P1-3-S4-D类三张牌-抖音-镜头04-3加4贯通-1080x1920.png")

# 镜头05 没有白送的牌
im, d = base(); header(d, "三张牌 · 都要代价")
ctext(d, "没有白送的牌", (W / 2, 600), 84, WHITE, maxw=880, min_size=68, tag="05")
rows = ["指标生 → 拼校内排名", "民办 → 学费 3 万起/年", "3+4 → 接受读 3 年职校"]
y = 840
for i, t in enumerate(rows):
    y1 = y + 158
    rcard(d, 80, y, W - 80, y1)
    ctext(d, t, (W / 2, (y + y1) / 2), 46, WHITE if i % 2 == 0 else GOLD, maxw=860, min_size=38, tag="05")
    y = y1 + 20
ctext(d, "先对号入座 · 别听一句“有路”就冲", (W / 2, 1430), 44, LIGHT, bold=False, maxw=880, min_size=36, tag="05")
check("镜头05")
im.save(HERE + "P1-3-S4-D类三张牌-抖音-镜头05-没有白送的牌-1080x1920.png")

# 镜头06 CTA
im, d = base(); header(d, "S4 · 一句话记牢")
ctext(d, "D类不是死胡同", (W / 2, 560), 88, WHITE, maxw=880, min_size=70, tag="06")
ctext(d, "把“分数线的焦虑”", (W / 2, 716), 46, GOLD, maxw=880, min_size=38, tag="06")
ctext(d, "换成“三张牌的选择”", (W / 2, 800), 46, GOLD, maxw=880, min_size=38, tag="06")
rcard(d, 80, 940, W - 80, 1160)
ctext(d, "你家该用哪张牌？", (W / 2, 1016), 48, WHITE, maxw=820, min_size=40, tag="06")
ctext(d, "查目标校真实录取线 · 别把路走窄", (W / 2, 1104), 36, LIGHT, bold=False, maxw=860, min_size=30, tag="06")
ctext(d, "关注我 · 下条讲 AC 类家长别大意", (W / 2, 1440), 54, WHITE, min_size=44, tag="06")
check("镜头06")
im.save(HERE + "P1-3-S4-D类三张牌-抖音-镜头06-CTA-1080x1920.png")
print("done")
