# -*- coding: utf-8 -*-
"""S5 抖音口播 分镜头图 x6（1080×1920，文字放大·安全区：右≤950／下正文≤1590）
镜头按口播分段：01核心观点 02等级怎么划 03隐形门槛 04掉C后果 05防掉C 06CTA。
口径：A+前5%；省一级录取须语数英物化历史道法C+·体育C（FAQ-8）。
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
    g = np.exp(-(((x - W * 0.5) / (W * 0.34)) ** 2 + ((y - H * 0.18) / (H * 0.32)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .05, W * .24, H * .12], fill=TOP + (36,))
    od.ellipse([W * .80, H * .86, W * 1.1, H * 1.03], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def ctext(d, text, xy, size, fill, bold=True, maxw=820, min_size=40):
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
    BADS.append((text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def pill(d, text, cy=1510, size=42, pad=36):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > W - 190:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (W - tw) / 2 - pad, (W + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((W / 2, cy), text, font=f, fill=WHITE, anchor="mm")
    return x1


def check(name):
    bad = []
    for tag, bb in BADS:
        if bb[0] < 30 or bb[2] > 950:
            bad.append((tag + " X", tuple(int(v) for v in bb)))
        if bb[1] < 60 or bb[3] > 1590:
            bad.append((tag + " Y", tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, bad if bad else "")
    BADS.clear()


# 镜头01 核心观点
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S5", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "A+ 永远是前 5%", (W / 2, 600), 96, WHITE, maxw=800)
ctext(d, "别让任何一科掉 C", (W / 2, 840), 64, GOLD)
ctext(d, "省一级的隐形门槛", (W / 2, 1040), 46, LIGHT, bold=False)
check("镜头01")
im.save(HERE + "S5-单科等级与省一级门槛-抖音-镜头01-核心观点-1080x1920.png")

# 镜头02 等级怎么划
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S5", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "等级怎么划？", (W / 2, 520), 84, WHITE)
ctext(d, "按原始分 · 全市比例", (W / 2, 760), 60, GOLD)
ctext(d, "A+ 前5% → C 后5%", (W / 2, 950), 54, WHITE)
ctext(d, "卷子难不难，不影响比例", (W / 2, 1150), 44, LIGHT, bold=False)
check("镜头02")
im.save(HERE + "S5-单科等级与省一级门槛-抖音-镜头02-等级怎么划-1080x1920.png")

# 镜头03 隐形门槛
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S5", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "隐形门槛", (W / 2, 540), 92, WHITE)
ctext(d, "省一级公办普高录取", (W / 2, 800), 60, GOLD)
ctext(d, "全科 C+ · 体育 C", (W / 2, 1000), 60, GOLD)
ctext(d, "语数英物化 · 历史道法", (W / 2, 1180), 42, LIGHT, bold=False)
check("镜头03")
im.save(HERE + "S5-单科等级与省一级门槛-抖音-镜头03-隐形门槛-1080x1920.png")

# 镜头04 掉C后果
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S5", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "有一科掉到 C", (W / 2, 560), 88, WHITE)
ctext(d, "总分够线，也不算数", (W / 2, 830), 62, GOLD)
ctext(d, "不符合省一级录取资格", (W / 2, 1030), 48, LIGHT, bold=False)
check("镜头04")
im.save(HERE + "S5-单科等级与省一级门槛-抖音-镜头04-掉C后果-1080x1920.png")

# 镜头05 防掉C
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S5", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "最易悄悄掉 C 的科目", (W / 2, 470), 66, WHITE)
lines = [
    ("1", "历史、道法——背多分，别放松"),
    ("2", "先补'接近 C 的那一科'"),
    ("3", "确认综合素质评价达标"),
]
y = 740
for n, t in lines:
    ctext(d, n, (180, y), 60, GOLD, min_size=44, maxw=80)
    ctext(d, t, (590, y), 46, WHITE, maxw=700, min_size=34)
    y += 200
check("镜头05")
im.save(HERE + "S5-单科等级与省一级门槛-抖音-镜头05-防掉C-1080x1920.png")

# 镜头06 CTA
im, d = base()
ctext(d, "深圳中考 · 政策解码器 S5", (W / 2, 150), 34, GOLD, bold=False, min_size=26)
ctext(d, "P1-2 收官预告", (W / 2, 560), 84, WHITE)
ctext(d, "生地同分 PK + 两门入场券", (W / 2, 800), 56, GOLD)
ctext(d, "关注我，最后一条 S6", (W / 2, 1040), 46, LIGHT, bold=False)
pill(d, "政策解码器 · 一条条讲给你", 1400)
check("镜头06")
im.save(HERE + "S5-单科等级与省一级门槛-抖音-镜头06-CTA-1080x1920.png")
print("done")
