# -*- coding: utf-8 -*-
"""
P1-2 主线 · 今日头条配图生成脚本（1200×900）一次产出 6 张
========================================================
  - 封面1-主标题 / 封面2-数据对撞(552PK) / 封面3-答案大字(别只看分数)
  - 微头条①-科目性价比(440/20/170三卡) / ②-单科等级制(五档表) / ③-隐形战场(双卡)
风格沿用 P1-1 头条 _build_p1_1_tt.py：蓝系家族渐变+金色+光晕+徽章胶囊+页脚来源
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

BANNER = "深圳中考 · P1系列 · 630背后的隐藏规则"
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


# ---------- 封面1 · 主标题 ----------
def cover_title():
    th = BLUES["navy"]
    im = img(th, "v", "glow-tr", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 118
    y = block(d, "630背后的\n3个隐藏规则", ImageFont.truetype(FB, 60), (255, 255, 255), y, 820, name="封面1-标题")
    block(d, "性价比 · 等级制 · 隐形战场", ImageFont.truetype(FB, 36), th["accent"], y + 38, 900, name="封面1-副题")
    f = ImageFont.truetype(FB, 30); txt = "分数会骗人 · 规则不会"
    bb = d.textbbox((0, 0), txt, font=f); pad = 40
    x0 = (W - (bb[2] + pad * 2)) / 2; y0 = H - 186; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=44, outline=th["accent"], width=2)
    T(d, ((x0 + x1) / 2, (y0 + y1) / 2), txt, f, th["accent"], "mm", "封面1-胶囊")
    footer(d)
    return im


# ---------- 封面2 · 数据对撞 552 PK ----------
def cover_pk():
    th = BLUES["royal"]
    im = img(th, "radial", "spot", "rings"); d = ImageDraw.Draw(im)
    y0 = badge(d, BANNER, th["accent"]) + 92
    block(d, "同样都是552分，凭什么一个录上一个落选？", ImageFont.truetype(FB, 34), (235, 242, 250), y0, 940, name="封面2-引言")
    fN = ImageFont.truetype(FB, 118)
    fL = ImageFont.truetype(FB, 32); fS = ImageFont.truetype(FR, 26)
    # 左：录取
    T(d, (336, 410), "552", fN, th["accent"], "mm", "封面2-左分")
    T(d, (336, 556), "生地 96 · 被录取", fL, (255, 246, 214), "mm", "封面2-左标签")
    T(d, (336, 606), "考生A", fS, (222, 230, 240), "mm", "封面2-左名")
    # 中：VS
    T(d, (600, 436), "VS", ImageFont.truetype(FB, 86), (255, 255, 255), "mm", "封面2-VS")
    # 右：落选
    T(d, (864, 410), "552", fN, (196, 205, 216), "mm", "封面2-右分")
    T(d, (864, 556), "生地 82 · 落选", fL, (200, 206, 215), "mm", "封面2-右标签")
    T(d, (864, 606), "考生B", fS, (200, 206, 215), "mm", "封面2-右名")
    yc = block(d, "同分先比生地：96 > 82，14分差出一个高中学位", ImageFont.truetype(FB, 38), th["accent"], 660, 1000, name="封面2-结论")
    footer(d)
    return im


# ---------- 封面3 · 答案大字 ----------
def cover_answer():
    th = BLUES["steel"]
    im = img(th, "d1", "beam", "slash"); d = ImageDraw.Draw(im)
    y0 = badge(d, BANNER, th["accent"]) + 140
    T(d, (W / 2, y0 + 52), "别只看分数", font=ImageFont.truetype(FB, 146), fill=th["accent"], anchor="mm", name="封面3-大字")
    block(d, "同样的630分，凭什么别人录上了、你家没有？", ImageFont.truetype(FB, 44), (255, 255, 255), y0 + 208, 980, name="封面3-主句")
    block(d, "性价比 · 等级制 · 隐形战场——3个隐藏规则，一次讲透", ImageFont.truetype(FR, 32), (228, 236, 246), y0 + 308, 1000, name="封面3-副句")
    footer(d)
    return im


# ---------- 微头条① · 科目性价比 三卡 ----------
def card_value():
    th = BLUES["deep"]
    im = img(th, "v", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 80
    block(d, "同样的时间 · 花在哪最划算", ImageFont.truetype(FB, 50), (255, 255, 255), y, 820, name="性价比-标题")
    cards = [
        ("440", "语数英物化 · 主战场", (255, 255, 255)),
        ("20", "理化实验 · 2026涨到20分", th["accent"]),
        ("170", "史·道·体 · 稳定即可", (255, 255, 255)),
    ]
    cx = [230, 600, 970]; cw = 340; cy = 336; ch = 340
    fN = ImageFont.truetype(FB, 78); fL = ImageFont.truetype(FR, 30)
    for (num, lab, col), xc in zip(cards, cx):
        card(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fill_alpha=16, outline=(255, 255, 255), outline_alpha=80, radius=26)
        T(d, (xc + 3, cy + 118), num, fN, (0, 18, 40), "mm", "性价比-投影")
        T(d, (xc, cy + 116), num, fN, col, "mm", "性价比-数字")
        d.line([(xc - 60, cy + 232), (xc + 60, cy + 232)], fill=(255, 255, 255, 100), width=2)
        T(d, (xc, cy + 262), lab, fL, (240, 246, 252), "mm", "性价比-标签")
    block(d, "实验那8分增量 = 性价比之王：认真练就白送，刷题拿不到", ImageFont.truetype(FB, 34), th["accent"], cy + ch + 74, 1060, name="性价比-结论")
    footer(d)
    return im


# ---------- 微头条② · 单科等级制 五档表 ----------
def card_grade():
    th = BLUES["ink"]
    im = img(th, "d2", "glow-bl", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 78
    block(d, "看分数会走眼 · 看等级不会", ImageFont.truetype(FB, 50), (255, 255, 255), y, 820, name="等级-标题")
    rows = [
        ("A+", "全市前 5%", "单科顶尖", False),
        ("A", "前 5%-25%", "录取线稳定盘", False),
        ("B+", "前 25%-50%", "中等竞争区", False),
        ("B", "前 50%-75%", "—", False),
        ("C+", "前 75%-95%", "省一级报考门槛！", True),
    ]
    fT = ImageFont.truetype(FB, 32); fP = ImageFont.truetype(FB, 30); fN = ImageFont.truetype(FR, 28)
    yy = 320
    for name, pct, note, hot in rows:
        col = th["accent"] if hot else (255, 255, 255)
        card(im, [80, yy, 1120, yy + 60], fill_alpha=22 if hot else 12, outline=(255, 255, 255) if hot else None, outline_alpha=110 if hot else 0, radius=18)
        T(d, (196, yy + 30), name, fT, col, "lm", "等级-档")
        T(d, (430, yy + 30), pct, fP, col, "lm", "等级-占比")
        T(d, (760, yy + 30), note, fN, (232, 240, 248), "lm", "等级-说明")
        yy += 70
    block(d, "全科 C+ 及以上 · 体育 C 即可 —— 报省一级学校的硬门槛", ImageFont.truetype(FB, 34), th["accent"], 716, 1000, name="等级-结论")
    footer(d)
    return im


# ---------- 微头条③ · 隐形战场 双卡 ----------
def card_hidden():
    th = BLUES["cobalt"]
    im = img(th, "v", "center", "grid"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 78
    block(d, "不计入630分 · 却可能决定录取", ImageFont.truetype(FB, 50), (255, 255, 255), y, 900, name="隐形-标题")
    fH1 = ImageFont.truetype(FB, 40); fB = ImageFont.truetype(FR, 30); fG = ImageFont.truetype(FB, 34)
    # 左卡：生地
    card(im, [90, 340, 585, 650], fill_alpha=16, outline=th["accent"], outline_alpha=150, radius=26)
    T(d, (337, 420), "生物 · 地理", fH1, (255, 255, 255), "mm", "隐形-生地标题")
    T(d, (337, 495), "合卷100分 · 不计总分", fB, (220, 230, 242), "mm", "隐形-生地说明")
    T(d, (337, 576), "同分PK · 先比生地", fG, th["accent"], "mm", "隐形-生地金句")
    # 右卡：信技艺术
    card(im, [615, 340, 1110, 650], fill_alpha=10, outline=(255, 255, 255), outline_alpha=90, radius=26)
    T(d, (862, 420), "信息科技 · 艺术", fH1, (255, 255, 255), "mm", "隐形-信技标题")
    T(d, (862, 495), "不计总分 · 报省一级须合格", fB, (220, 230, 242), "mm", "隐形-信技说明")
    T(d, (862, 576), "别让合格考翻车", fG, (255, 255, 255), "mm", "隐形-信技金句")
    block(d, "生地是底牌 · 信技艺术是入场券 —— 提前确认，别到填报才慌", ImageFont.truetype(FB, 34), th["accent"], 700, 1080, name="隐形-结论")
    footer(d)
    return im


# ---------- 主流程 ----------
def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    jobs = [
        ("P1-2-今日头条-封面1-主标题-1200x900.png", cover_title),
        ("P1-2-今日头条-封面2-数据对撞-1200x900.png", cover_pk),
        ("P1-2-今日头条-封面3-答案大字-1200x900.png", cover_answer),
        ("微头条/微头条①-科目性价比-配图.png", card_value),
        ("微头条/微头条②-单科等级制-配图.png", card_grade),
        ("微头条/微头条③-隐形战场-配图.png", card_hidden),
    ]
    for rel, fn in jobs:
        im = fn()
        path = os.path.join(out, rel)
        im.save(path)
        print("OK", path)


if __name__ == "__main__":
    main()
