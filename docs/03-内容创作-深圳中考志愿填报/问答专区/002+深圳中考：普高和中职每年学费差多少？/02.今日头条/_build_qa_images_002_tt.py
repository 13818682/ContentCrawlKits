# -*- coding: utf-8 -*-
"""
深圳中考 · 问答系列 · 002 今日头条配图生成脚本（1200×900）
============================================================
文章：普高和中职每年学费差多少？
产出：头条 6 张（1200×900，命名沿用 001 惯例）
  - 封面1-主标题 / 封面2-数据对撞 / 封面3-答案大字
  - 正文图-三年总账表 / 正文图-贯通名额 / 微头条配图-3关键数字
设计：统一蓝色系家族(6档) + 金色强调 + 顶部胶囊徽章「深圳中考·问答系列·002」
      + 底部数据来源 + 微软雅黑 + 版心安全区。复用自 001 _build_qa_images.py 头条段。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1200, 900
FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

BLUES = {
    "navy":   dict(top=(20, 59, 115),  bot=(10, 32, 60),  accent=(242, 184, 75),  sec=(150, 205, 255)),
    "royal":  dict(top=(22, 70, 130),  bot=(10, 32, 64),  accent=(242, 184, 75),  sec=(140, 200, 255)),
    "steel":  dict(top=(42, 66, 106),  bot=(18, 30, 52),  accent=(242, 184, 75),  sec=(168, 202, 244)),
    "cobalt": dict(top=(16, 58, 120),  bot=(7, 26, 60),   accent=(242, 184, 75),  sec=(126, 188, 255)),
    "ink":    dict(top=(30, 48, 86),   bot=(12, 20, 40),  accent=(242, 184, 75),  sec=(150, 180, 232)),
    "deep":   dict(top=(14, 84, 140),  bot=(8, 36, 70),   accent=(242, 184, 75),  sec=(182, 220, 255)),
}

BANNER = "深圳中考 · 问答系列 · 002"
FOOT   = "数据来源：深圳市教育局2026年招生计划 · 逐条人工核对"


def T(d, xy, text, font, fill, anchor="mm", name="", pad=6):
    """带越界校验的文本绘制：超出画布即打印警告。"""
    bb = d.textbbox((0, 0), text, font=font)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    cx, cy = xy
    if anchor == "mm":
        x0, y0 = cx - bw / 2, cy - bh / 2
    elif anchor == "lm":
        x0, y0 = cx, cy - bh / 2
    elif anchor == "rm":
        x0, y0 = cx - bw, cy - bh / 2
    else:
        x0, y0 = cx, cy
    if x0 < pad or x0 + bw > W - pad or y0 < pad or y0 + bh > H - pad:
        print(f"[溢出警告] {name}: '{text}' 宽{bw} x0={x0:.0f}->{x0+bw:.0f} y0={y0:.0f}->{y0+bh:.0f}")
    d.text(xy, text, font=font, fill=fill, anchor=anchor)
    return (x0, y0, x0 + bw, y0 + bh)


def make_base(theme, direction="v", w=W, h=H):
    T0 = np.array(theme["top"], float); B = np.array(theme["bot"], float)
    if direction == "v":
        t = np.linspace(0, 1, h)[:, None, None]
        a = T0[None, None, :] * (1 - t) + B[None, None, :] * t
        a = np.repeat(a, w, axis=1)
    elif direction == "d1":
        x = np.linspace(0, 1, w)[None, :, None]; y = np.linspace(0, 1, h)[:, None, None]
        t = (x + y) / 2; a = T0[None, None, :] * (1 - t) + B[None, None, :] * t
    elif direction == "d2":
        x = np.linspace(0, 1, w)[None, :, None]; y = np.linspace(0, 1, h)[:, None, None]
        t = (1 - x + y) / 2; a = T0[None, None, :] * (1 - t) + B[None, None, :] * t
    else:
        t = np.linspace(0, 1, h)[:, None, None]
        a = T0[None, None, :] * (1 - t) + B[None, None, :] * t
        a = np.repeat(a, w, axis=1)
        y, x = np.mgrid[0:h, 0:w]
        d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
        a = a * (1 - 0.38 * np.clip(d - 0.55, 0, None)[..., None])
    return a


def add_light(a, kind, color=(255, 255, 255), w=W, h=H):
    y, x = np.mgrid[0:h, 0:w]; c = np.array(color, float)
    if kind == "glow-tr":
        d = np.sqrt((x - w * 0.86) ** 2 + (y - h * 0.10) ** 2); g = np.exp(-d ** 2 / (2 * 400 ** 2)) * 0.30
    elif kind == "glow-bl":
        d = np.sqrt((x - w * 0.14) ** 2 + (y - h * 0.88) ** 2); g = np.exp(-d ** 2 / (2 * 420 ** 2)) * 0.28
    elif kind == "beam":
        d = np.abs(1.8 * x - y - 150) / np.sqrt(1.8 ** 2 + 1); g = np.exp(-d ** 2 / (2 * 300 ** 2)) * 0.22
    elif kind == "spot":
        d = np.sqrt((x - w / 2) ** 2 + (y - h * 0.18) ** 2); g = np.exp(-d ** 2 / (2 * 430 ** 2)) * 0.30
    else:
        d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
        g = np.clip(0.30 * (1 - d), 0, None) * 0.9
    return np.clip(a + c * g[..., None], 0, 255)


def img(theme, direction, light_kind, pattern):
    a = make_base(theme, direction)
    a = add_light(a, light_kind)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    decor(im, theme, pattern)
    return im


def decor(im, theme, pattern):
    top = theme["top"]; accent = theme["accent"]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if pattern == "circles":
        od.ellipse([W - 430, -200, W + 140, 350], fill=top + (36,))
        od.ellipse([-210, H - 340, 250, H + 70], fill=top + (24,))
        od.ellipse([W - 300, -110, W - 60, 130], outline=accent + (110,), width=3)
    elif pattern == "rings":
        cx, cy = W - 190, H - 230
        for r in (170, 240, 310):
            od.ellipse([cx - r, cy - r, cx + r, cy + r], outline=top + (55,), width=2)
        od.ellipse([110, 110, 350, 350], outline=accent + (70,), width=2)
    elif pattern == "slash":
        for i in range(6):
            x0 = 170 + i * 195
            od.line([(x0, -60), (x0 + 160, H)], fill=top + (40,), width=64)
        od.line([(W - 130, -80), (W + 80, H)], fill=accent + (60,), width=28)
    elif pattern == "grid":
        for x in range(70, W, 92):
            for y in range(70, H, 92):
                od.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 20))
    im.paste(ov, (0, 0), ov)


def badge(d, text, accent, y=82):
    f = ImageFont.truetype(FB, 25)
    bb = d.textbbox((0, 0), text, font=f); pad = 30
    x0 = (W - (bb[2] + pad * 2)) / 2; y0 = y; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=36, outline=accent, width=2)
    T(d, ((x0 + x1) / 2, (y0 + y1) / 2), text, f, accent, "mm", "badge")
    return y1


def footer(d):
    f = ImageFont.truetype(FR, 21)
    T(d, (W / 2, H - 46), FOOT, f, (206, 214, 222), "mm", "footer")


def wrap(text, font, maxw, d):
    out = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if d.textlength(cur + ch, font=font) <= maxw:
                cur += ch
            else:
                out.append(cur); cur = ch
        if cur:
            out.append(cur)
    return out


def block(d, text, font, fill, y, maxw, lh=1.22, x=W / 2, name=""):
    for ln in wrap(text, font, maxw, d):
        T(d, (x, y), ln, font, fill, "mm", name)
        y += font.size * lh
    return y


def card(im, box, fill_alpha=0, outline=None, outline_alpha=255, radius=22, width=2):
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fill_alpha))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


# ---------- 封面1-主标题 ----------
def cover_title():
    th = BLUES["navy"]
    im = img(th, "v", "glow-tr", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 120
    y = block(d, "同样读三年书\n有人花1万 · 有人花30万", ImageFont.truetype(FB, 66), (255, 255, 255), y, 820, name="封面1-标题")
    block(d, "普高和中职的学费差 · 家长现在就得看清", ImageFont.truetype(FB, 36), th["accent"], y + 40, 820, name="封面1-副题")
    f = ImageFont.truetype(FB, 28); txt = "约一半考生进不了公办普高"
    bb = d.textbbox((0, 0), txt, font=f); pad = 34
    x0 = (W - (bb[2] + pad * 2)) / 2; y0 = H - 190; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=40, outline=th["accent"], width=2)
    T(d, ((x0 + x1) / 2, (y0 + y1) / 2), txt, f, th["accent"], "mm", "封面1-胶囊")
    footer(d)
    return im


# ---------- 封面2-数据对撞 ----------
def cover_data():
    th = BLUES["royal"]
    im = img(th, "radial", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 150
    fN1 = ImageFont.truetype(FB, 116); fN2 = ImageFont.truetype(FB, 82); fL = ImageFont.truetype(FR, 34)
    T(d, (W * 0.30, y), "约1万", fN1, th["accent"], "mm", "封面2-左数字")
    T(d, (W * 0.30, y + 130), "公办普高 · 三年总花费", fL, (255, 255, 255), "mm", "封面2-左标签")
    T(d, (W * 0.70, y), "21万-36万", fN2, (255, 255, 255), "mm", "封面2-右数字")
    T(d, (W * 0.70, y + 130), "民办普高 · 三年总花费", fL, (255, 255, 255), "mm", "封面2-右标签")
    d.line([(W / 2, y - 130), (W / 2, y + 160)], fill=th["accent"], width=3)
    block(d, "同样是读三年书 · 差的二十几万，可能是几年的积蓄", ImageFont.truetype(FB, 34), (255, 255, 255), y + 270, 860, name="封面2-结论")
    footer(d)
    return im


# ---------- 封面3-答案大字 ----------
def cover_answer():
    th = BLUES["steel"]
    im = img(th, "d1", "beam", "slash"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 150
    T(d, (W / 2, y), "约一半", font=ImageFont.truetype(FB, 210), fill=th["accent"], anchor="mm", name="封面3-大字")
    block(d, "考生进不了公办普高", ImageFont.truetype(FB, 52), (255, 255, 255), y + 160, 800, name="封面3-主句")
    block(d, "民办学杂费是公办的25-40倍 · 家长现在就得看清", ImageFont.truetype(FR, 32), (230, 238, 248), y + 255, 900, name="封面3-副句")
    footer(d)
    return im


# ---------- 正文图-三年总账表 ----------
def table_total():
    th = BLUES["cobalt"]
    im = img(th, "v", "center", "grid"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 76
    block(d, "同样读三年书 · 四类学校总账", ImageFont.truetype(FB, 50), (255, 255, 255), y, 760, name="总账-标题")
    tx0, tx1 = 80, 1120
    fH = ImageFont.truetype(FB, 30)
    card(im, [tx0, 330, tx1, 386], fill_alpha=26, radius=16)
    hx = {0: 210, 1: 470, 2: 740, 3: 1010}
    for xi, htxt in [(0, "学校类型"), (1, "招生人数(2026)"), (2, "三年总花费(约)"), (3, "与公办比")]:
        T(d, (hx[xi], 358), htxt, fH, (255, 255, 255), "mm", "总账-表头")
    rows = [
        ("公办普高", "80,303人", "约1万", "基准", (255, 255, 255)),
        ("民办普高", "33,195人", "21万-36万", "贵约25-40倍", th["accent"]),
        ("公办中职", "15,924人", "约3千", "免学费", (255, 255, 255)),
        ("民办中职", "17,330人", "5万-10万", "贵约20-35倍", th["accent"]),
    ]
    fT = ImageFont.truetype(FB, 34); fC = ImageFont.truetype(FR, 30); fN = ImageFont.truetype(FB, 38); fS = ImageFont.truetype(FR, 28)
    ry0 = 398; row_h = 86
    for i, (label, cnt, num, note, col) in enumerate(rows):
        ry = ry0 + i * row_h
        if i % 2 == 0:
            card(im, [tx0, ry, tx1, ry + row_h], fill_alpha=12, radius=14)
        T(d, (210, ry + row_h / 2), label, fT, (255, 255, 255), "mm", "总账-类型")
        T(d, (470, ry + row_h / 2), cnt, fC, (235, 243, 252), "mm", "总账-人数")
        T(d, (740, ry + row_h / 2), num, fN, col, "mm", "总账-花费")
        T(d, (1010, ry + row_h / 2), note, fS, (225, 236, 248), "mm", "总账-对比")
    footer(d)
    return im


# ---------- 正文图-贯通名额 ----------
def guantong():
    th = BLUES["ink"]
    im = img(th, "d2", "glow-bl", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 80
    block(d, "公办中职 · 便宜但名额少", ImageFont.truetype(FB, 54), (255, 255, 255), y, 700, name="贯通-标题")
    T(d, (W / 2, 440), "约2,300个", font=ImageFont.truetype(FB, 160), fill=th["accent"], anchor="mm", name="贯通-大数字")
    T(d, (W / 2, 570), "公办中职贯通本科名额", font=ImageFont.truetype(FB, 40), fill=(255, 255, 255), anchor="mm", name="贯通-标签")
    subs = [
        ("3+4中本贯通", "仅300个", th["accent"]),
        ("3+2 · 公办部分", "约1,960个", (255, 255, 255)),
        ("全市中职合计", "约3,000多个", th["sec"]),
    ]
    fT = ImageFont.truetype(FB, 32); fN = ImageFont.truetype(FB, 40)
    cx = [285, 600, 915]; cw = 280; cy = 640; ch = 150
    for (t, n, col), xc in zip(subs, cx):
        card(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fill_alpha=16, outline=(255, 255, 255), outline_alpha=70, radius=22)
        T(d, (xc, cy + 46), t, fT, (235, 243, 252), "mm", "贯通-卡标题")
        T(d, (xc, cy + 108), n, fN, col, "mm", "贯通-卡数字")
    footer(d)
    return im


# ---------- 微头条配图-3关键数字 ----------
def three_numbers():
    th = BLUES["deep"]
    im = img(th, "v", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 80
    block(d, "普高和中职 · 3个关键数字", ImageFont.truetype(FB, 50), (255, 255, 255), y, 700, name="3数-标题")
    cards = [
        ("33%", "考生家庭读民办", th["accent"]),
        ("25-40倍", "民办比公办贵", (255, 255, 255)),
        ("9.9万/年", "深圳私营平均工资", th["sec"]),
    ]
    cx = [230, 600, 970]; cw = 340; cy = 330; ch = 400
    fN = ImageFont.truetype(FB, 72); fL = ImageFont.truetype(FR, 32)
    for (num, lab, col), xc in zip(cards, cx):
        card(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fill_alpha=18, outline=(255, 255, 255), outline_alpha=80, radius=26)
        T(d, (xc + 2, cy + 120), num, fN, (0, 18, 40), "mm", "3数-投影")
        T(d, (xc, cy + 118), num, fN, col, "mm", "3数-数字")
        d.line([(xc - 60, cy + 252), (xc + 60, cy + 252)], fill=(255, 255, 255, 100), width=2)
        T(d, (xc, cy + 290), lab, fL, (240, 246, 252), "mm", "3数-标签")
    footer(d)
    return im


# ---------- 主流程 ----------
def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    jobs = [
        ("今日头条-封面1-主标题-1200x900.png", cover_title),
        ("今日头条-封面2-数据对撞-1200x900.png", cover_data),
        ("今日头条-封面3-答案大字-1200x900.png", cover_answer),
        ("今日头条-正文图-三年总账表-1200x900.png", table_total),
        ("今日头条-正文图-贯通名额-1200x900.png", guantong),
        ("今日头条-微头条配图-3关键数字-1200x900.png", three_numbers),
    ]
    for name, fn in jobs:
        im = fn()
        path = os.path.join(out, name)
        im.save(path)
        print("OK", path)


if __name__ == "__main__":
    main()
