# -*- coding: utf-8 -*-
"""
P1-1 主线 · 今日头条配图生成脚本（1200×900）
============================================
文章：深圳中考游戏规则：30分钟从入门到看懂
产出：头条 6 张（1200×900）
  - 封面1-主标题 / 封面2-数据对撞(630 vs 170) / 封面3-答案大字(四句话)
  - 正文图-批次顺序表 / 正文图-时间线 / 微头条配图-3关键数字
设计：统一蓝色系家族(6档) + 金色强调 + 顶部胶囊徽章「深圳中考·P1系列·游戏规则全景」
      + 底部数据来源 + 微软雅黑 + 版心安全区。复用 QA-003 _build_qa_images_003_tt.py 框架。
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

BANNER = "深圳中考 · P1系列 · 游戏规则全景"
FOOT   = "数据来源：《2026年深圳市高中阶段学校考生报考指导手册》· 逐条人工核对"


def T(d, xy, text, font, fill, anchor="mm", name="", pad=6):
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
    y = block(d, "深圳中考游戏规则\n30分钟从入门到看懂", ImageFont.truetype(FB, 62), (255, 255, 255), y, 900, name="封面1-标题")
    block(d, "总分630 · ACD三类 · 五批次 · 16个志愿", ImageFont.truetype(FB, 34), th["accent"], y + 40, 880, name="封面1-副题")
    f = ImageFont.truetype(FB, 28); txt = "四句话，讲完深圳中考的游戏规则"
    bb = d.textbbox((0, 0), txt, font=f); pad = 34
    x0 = (W - (bb[2] + pad * 2)) / 2; y0 = H - 190; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=40, outline=th["accent"], width=2)
    T(d, ((x0 + x1) / 2, (y0 + y1) / 2), txt, f, th["accent"], "mm", "封面1-胶囊")
    footer(d)
    return im


# ---------- 封面2-数据对撞 630 vs 170 ----------
def cover_data():
    th = BLUES["royal"]
    im = img(th, "radial", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 150
    fN1 = ImageFont.truetype(FB, 116); fN2 = ImageFont.truetype(FB, 82); fL = ImageFont.truetype(FR, 34)
    T(d, (W * 0.30, y), "440分", fN1, th["accent"], "mm", "封面2-左数字")
    T(d, (W * 0.30, y + 130), "语数英物化 · 主战场", fL, (255, 255, 255), "mm", "封面2-左标签")
    T(d, (W * 0.70, y), "170分", fN2, (255, 255, 255), "mm", "封面2-右数字")
    T(d, (W * 0.70, y + 130), "史道体 · 定公办民办", fL, (255, 255, 255), "mm", "封面2-右标签")
    d.line([(W / 2, y - 130), (W / 2, y + 160)], fill=th["accent"], width=3)
    block(d, "630分怎么构成，决定每1分的备考价值", ImageFont.truetype(FB, 34), (255, 255, 255), y + 270, 880, name="封面2-结论")
    footer(d)
    return im


# ---------- 封面3-答案大字 ----------
def cover_answer():
    th = BLUES["steel"]
    im = img(th, "d1", "beam", "slash"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 150
    T(d, (W / 2, y), "搞懂规则", font=ImageFont.truetype(FB, 150), fill=th["accent"], anchor="mm", name="封面3-大字")
    block(d, "就是最大的优势\n不犯低级错误 · 本身就是优势", ImageFont.truetype(FB, 46), (255, 255, 255), y + 170, 860, name="封面3-主句")
    block(d, "总分630 · 三类 · 五批 · 16志愿按分排队——四句话建立全景", ImageFont.truetype(FR, 32), (230, 238, 248), y + 320, 900, name="封面3-副句")
    footer(d)
    return im


# ---------- 正文图-批次顺序表 ----------
def table_batch():
    th = BLUES["cobalt"]
    im = img(th, "v", "center", "grid"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 76
    block(d, "录取分五个批次 · 前一批录了后面全作废", ImageFont.truetype(FB, 46), (255, 255, 255), y, 820, name="批次-标题")
    tx0, tx1 = 80, 1120
    fH = ImageFont.truetype(FB, 30)
    card(im, [tx0, 330, tx1, 386], fill_alpha=26, radius=16)
    hx = {0: 210, 1: 480, 2: 740, 3: 1000}
    for xi, htxt in [(0, "批次"), (1, "志愿数"), (2, "可填报"), (3, "关键")]:
        T(d, (hx[xi], 358), htxt, fH, (255, 255, 255), "mm", "批次-表头")
    rows = [
        ("1自招", "1", "自招高中/中职", "录了全作废", (255, 255, 255)),
        ("2名额分配", "1", "1所公办普高", "指标生", (255, 255, 255)),
        ("3统一招生第一批", "16", "普高≤12+中职≤4", "核心批次", th["accent"]),
        ("4统一招生第二批", "18", "本市中职技校", "—", (255, 255, 255)),
        ("5统一招生第三批", "6", "外省中职", "—", (255, 255, 255)),
    ]
    fT = ImageFont.truetype(FB, 30); fC = ImageFont.truetype(FR, 28); fN = ImageFont.truetype(FB, 34)
    ry0 = 398; row_h = 78
    for i, (rk, sch, sc, note, col) in enumerate(rows):
        ry = ry0 + i * row_h
        if i % 2 == 0:
            card(im, [tx0, ry, tx1, ry + row_h], fill_alpha=12, radius=14)
        T(d, (210, ry + row_h / 2), rk, fT, (255, 255, 255), "mm", "批次-名")
        T(d, (480, ry + row_h / 2), sch, fN, col, "mm", "批次-志愿数")
        T(d, (740, ry + row_h / 2), sc, fC, (235, 243, 252), "mm", "批次-内容")
        T(d, (1000, ry + row_h / 2), note, fC, (235, 243, 252), "mm", "批次-关键")
    footer(d)
    return im


# ---------- 正文图-时间线 ----------
def timeline():
    th = BLUES["ink"]
    im = img(th, "d2", "glow-bl", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 76
    block(d, "从报名到录取 · 整整6个月", ImageFont.truetype(FB, 46), (255, 255, 255), y, 700, name="时间-标题")
    events = [
        ("3月", "中考报名", "D类5项材料备齐", False),
        ("4月", "体育中考", "36分现场", False),
        ("5月", "实验20+听说25", "2026实验操作计入", False),
        ("5月下旬", "志愿填报", "全年最重要10天！", True),
        ("6月", "自招+文化课", "6.26-28考试", False),
        ("7月16日", "成绩公布", "含单科等级", False),
        ("7-8月", "分批录取", "自招→指标→第1/2/3批", False),
    ]
    fT = ImageFont.truetype(FB, 32); fC = ImageFont.truetype(FR, 26); fN = ImageFont.truetype(FB, 28)
    yy = 330
    for tm, ev, note, hot in events:
        col = th["accent"] if hot else (255, 255, 255)
        card(im, [80, yy, 1120, yy + 58], fill_alpha=12 if not hot else 26, outline=(255, 255, 255) if hot else None, outline_alpha=90 if hot else 0, radius=16)
        T(d, (180, yy + 29), tm, fT, col, "mm", "时间-时间")
        T(d, (360, yy + 29), ev, fN, col, "lm", "时间-事项")
        T(d, (700, yy + 29), note, fC, (235, 243, 252), "lm", "时间-提醒")
        yy += 70
    footer(d)
    return im


# ---------- 微头条配图-3关键数字 ----------
def three_numbers():
    th = BLUES["deep"]
    im = img(th, "v", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 80
    block(d, "深圳中考 · 3个关键数字", ImageFont.truetype(FB, 50), (255, 255, 255), y, 700, name="3数-标题")
    cards = [
        ("630", "总分 · 8科", th["accent"]),
        ("440", "语数英物化 · 占70%", (255, 255, 255)),
        ("16", "第一批志愿数", th["sec"]),
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
        ("今日头条-正文图-批次顺序表-1200x900.png", table_batch),
        ("今日头条-正文图-时间线-1200x900.png", timeline),
        ("今日头条-微头条配图-3关键数字-1200x900.png", three_numbers),
    ]
    for name, fn in jobs:
        im = fn()
        path = os.path.join(out, name)
        im.save(path)
        print("OK", path)


if __name__ == "__main__":
    main()
