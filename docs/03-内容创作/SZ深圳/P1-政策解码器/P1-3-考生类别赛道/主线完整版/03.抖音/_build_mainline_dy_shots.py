# -*- coding: utf-8 -*-
"""P1-3 主线完整版·抖音身份预告 分镜头图（1080×1920 ×6）

版式要点（2026-09-06 用户定稿）：
1. 每页顶部「深圳中考」金色大字标识（~90px + 金线）—— 每帧锁定主题；
2. 每镜关键话用白大字（主观点）+ 金色（关键信息）双层级突出；
3. 安全区：内容右缘 ≤950、正文下界 ≤1590；底部 y≥1600 整段留空给字幕/图标。
镜头对齐口播 5 段 + CTA → 6 镜：01你是A还是D / 02三类速览 / 03 D类别慌(四大持平)
 / 04真正分差在中下层 / 05现在做3件事 / 06 CTA(关注+S1-S6预告)。
口径：ACD三类；四大AC=D持平(2026参考)；D类5条件官方版。
模板：S6 _build_s6_dy_shots.py + douyin-safe-area-rule。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1920
BADS = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.16) / (H * 0.32)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .05, W * .24, H * .12], fill=TOP + (36,))
    od.ellipse([W * .80, H * .86, W * 1.1, H * 1.03], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def ctext(d, text, xy, size, fill, bold=True, maxw=840, min_size=40, tag=""):
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


def header(d):
    """每页顶部「深圳中考」金色大字标识 + 金线（用户要求·每帧锁定主题）"""
    f = ctext(d, "深圳中考", (W / 2, 130), 92, GOLD, maxw=820, min_size=72, tag="HEAD")
    bb = d.textbbox((W / 2, 130), "深圳中考", font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 6
    d.line([W / 2 - half, 212, W / 2 + half, 212], fill=GOLD, width=6)
    ctext(d, "考生类别赛道 · 身份预告", (W / 2, 300), 40, LIGHT, bold=False, min_size=32, tag="SUB")


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 30 or bb[2] > 950:
            bad.append((tag + " 右", tuple(int(v) for v in bb)))
        if bb[1] < 60 or bb[3] > 1590:
            bad.append((tag + " 下", tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, bad if bad else "")
    BADS.clear()


# 镜头01 你是A还是D
im, d = base(); header(d)
ctext(d, "你是 A 还是 D？", (W / 2, 640), 100, WHITE, maxw=840, min_size=76, tag="01")
ctext(d, "A  C  D", (W / 2, 980), 120, GOLD, maxw=840, min_size=88, tag="01")
ctext(d, "三个字母 = 三条赛道", (W / 2, 1260), 48, LIGHT, bold=False, min_size=40, tag="01")
check("镜头01")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-抖音-镜头01-你是A还是D-1080x1920.png")

# 镜头02 三类速览
im, d = base(); header(d)
ctext(d, "A 深户 · 学籍同区", (W / 2, 560), 64, WHITE, min_size=48, tag="02")
ctext(d, "最宽赛道 · 公办都能报", (W / 2, 700), 40, LIGHT, bold=False, min_size=32, tag="02")
ctext(d, "C 深户 · 学籍跨区", (W / 2, 920), 64, GOLD, min_size=48, tag="02")
ctext(d, "报名要二选一 · 别忽略", (W / 2, 1060), 40, LIGHT, bold=False, min_size=32, tag="02")
ctext(d, "D 非深户", (W / 2, 1280), 64, WHITE, min_size=48, tag="02")
ctext(d, "占考生一半多 · 公办指标只 23%", (W / 2, 1420), 40, LIGHT, bold=False, min_size=32, tag="02")
check("镜头02")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-抖音-镜头02-三类速览-1080x1920.png")

# 镜头03 D类别慌·四大持平
im, d = base(); header(d)
ctext(d, "D 类 · 别慌", (W / 2, 600), 96, WHITE, maxw=840, min_size=72, tag="03")
ctext(d, "四大名校 AC = D 已持平", (W / 2, 900), 68, GOLD, maxw=840, min_size=52, tag="03")
ctext(d, "分数到了 · 户籍不卡你", (W / 2, 1160), 46, LIGHT, bold=False, min_size=38, tag="03")
check("镜头03")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-抖音-镜头03-D类别慌-1080x1920.png")

# 镜头04 真正分差在中下层
im, d = base(); header(d)
ctext(d, "真正的分差", (W / 2, 600), 88, WHITE, maxw=840, min_size=66, tag="04")
ctext(d, "在中下层", (W / 2, 800), 96, GOLD, maxw=840, min_size=74, tag="04")
ctext(d, "越往下的学校 · D 类要考的分越高", (W / 2, 1120), 46, LIGHT, bold=False, min_size=38, tag="04")
ctext(d, "先认赛道 · 再谈分数", (W / 2, 1400), 52, WHITE, min_size=42, tag="04")
check("镜头04")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-抖音-镜头04-分差在中下层-1080x1920.png")

# 镜头05 现在做3件事
im, d = base(); header(d)
ctext(d, "现在 · 做 3 件事", (W / 2, 480), 68, WHITE, min_size=54, tag="05")
lines = [
    ("①", "查社保：一个险种满 3 年", 720),
    ("②", "看居住证：别过期", 960),
    ("③", "办租赁凭证：要提前", 1200),
]
for n, t, yy in lines:
    ctext(d, n, (170, yy), 56, GOLD, min_size=44, maxw=120, tag="05")
    ctext(d, t, (600, yy), 50, WHITE, maxw=720, min_size=40, tag="05")
ctext(d, "别等 3 月报名才手忙脚乱", (W / 2, 1450), 42, LIGHT, bold=False, min_size=34, tag="05")
check("镜头05")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-抖音-镜头05-做三件事-1080x1920.png")

# 镜头06 CTA
im, d = base(); header(d)
ctext(d, "你是哪一类？", (W / 2, 620), 88, WHITE, maxw=840, min_size=66, tag="06")
ctext(d, "评论区告诉我", (W / 2, 840), 60, GOLD, min_size=46, tag="06")
ctext(d, "明起 S1-S6 连更 · 一条讲透一个点", (W / 2, 1120), 44, LIGHT, bold=False, min_size=36, tag="06")
ctext(d, "关注我 · 深圳中考系列", (W / 2, 1380), 52, WHITE, min_size=42, tag="06")
check("镜头06")
im.save(HERE + "P1-3-主线完整版-AC类还是D类-抖音-镜头06-CTA-1080x1920.png")
print("done")
