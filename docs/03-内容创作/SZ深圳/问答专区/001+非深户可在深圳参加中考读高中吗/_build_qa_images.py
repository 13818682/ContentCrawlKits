# -*- coding: utf-8 -*-
"""
深圳中考 · 问答系列 配图生成脚本（001 非深户可在深圳参加中考读高中吗）
============================================================
设计目标：统一蓝色系家族 + 光影/渐变制造变化（杜绝跨图跳色）。
家族常量（统一识别）：全部深蓝色系底 + 金色强调 + 顶部胶囊徽章「深圳中考 · 问答系列」+
                     底部数据来源 + 微软雅黑 + 版心安全区。
变化轴（新鲜感，不靠换色）：蓝色深浅 (6档) × 渐变方向 (v/radial/d1/d2) ×
                     光影效果 (glow-tr/glow-bl/spot/beam/center) × 装饰纹理 (circles/rings/slash/grid)。

复制本脚本改「CONTENT」与「TITLE」即可为后续问答(002+...)产图。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1200, 900
FB = "C:/Windows/Fonts/msyhbd.ttc"   # 微软雅黑粗体
FR = "C:/Windows/Fonts/msyh.ttc"     # 微软雅黑

# ---- 6 档蓝色系主题（全部深蓝 + 金色强调，仅深浅/冷暖有别） ----
BLUES = {
    "navy":   dict(top=(20, 59, 115),  bot=(10, 32, 60),  accent=(242, 184, 75),  sec=(150, 205, 255)),
    "royal":  dict(top=(22, 70, 130),  bot=(10, 32, 64),  accent=(242, 184, 75),  sec=(140, 200, 255)),
    "steel":  dict(top=(42, 66, 106),  bot=(18, 30, 52),  accent=(242, 184, 75),  sec=(168, 202, 244)),
    "cobalt": dict(top=(16, 58, 120),  bot=(7, 26, 60),   accent=(242, 184, 75),  sec=(126, 188, 255)),
    "ink":    dict(top=(30, 48, 86),   bot=(12, 20, 40),  accent=(242, 184, 75),  sec=(150, 180, 232)),
    "deep":   dict(top=(14, 84, 140),  bot=(8, 36, 70),   accent=(242, 184, 75),  sec=(182, 220, 255)),
}

BANNER = "深圳中考 · 问答系列 · 001"
FOOT   = "数据来源：深圳市教育局公开信息 · 逐条人工核对"


# ---------- 基础：蓝色渐变（多方向） + 光影 ----------
def make_base(theme, direction="v", w=W, h=H):
    """返回 (h,w,3) 蓝色渐变数组，方向：v / d1 / d2 / radial"""
    T = np.array(theme["top"], float); B = np.array(theme["bot"], float)
    if direction == "v":
        t = np.linspace(0, 1, h)[:, None, None]
        a = T[None, None, :] * (1 - t) + B[None, None, :] * t
        a = np.repeat(a, w, axis=1)
    elif direction == "d1":          # 左上→右下
        x = np.linspace(0, 1, w)[None, :, None]; y = np.linspace(0, 1, h)[:, None, None]
        t = (x + y) / 2; a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    elif direction == "d2":          # 右上→左下
        x = np.linspace(0, 1, w)[None, :, None]; y = np.linspace(0, 1, h)[:, None, None]
        t = (1 - x + y) / 2; a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    else:                            # radial：中心亮、四角暗
        t = np.linspace(0, 1, h)[:, None, None]
        a = T[None, None, :] * (1 - t) + B[None, None, :] * t
        a = np.repeat(a, w, axis=1)
        y, x = np.mgrid[0:h, 0:w]
        d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
        a = a * (1 - 0.38 * np.clip(d - 0.55, 0, None)[..., None])
    return a


def add_light(a, kind, color=(255, 255, 255), w=W, h=H):
    """光影：glow-tr 右上角光 / glow-bl 左下角光 / spot 顶部中心光 / beam 斜光带 / center 中心光"""
    y, x = np.mgrid[0:h, 0:w]; c = np.array(color, float)
    if kind == "glow-tr":
        d = np.sqrt((x - w * 0.86) ** 2 + (y - h * 0.10) ** 2); g = np.exp(-d ** 2 / (2 * 400 ** 2)) * 0.30
    elif kind == "glow-bl":
        d = np.sqrt((x - w * 0.14) ** 2 + (y - h * 0.88) ** 2); g = np.exp(-d ** 2 / (2 * 420 ** 2)) * 0.28
    elif kind == "beam":
        d = np.abs(1.8 * x - y - 150) / np.sqrt(1.8 ** 2 + 1); g = np.exp(-d ** 2 / (2 * 300 ** 2)) * 0.22
    elif kind == "spot":
        d = np.sqrt((x - w / 2) ** 2 + (y - h * 0.18) ** 2); g = np.exp(-d ** 2 / (2 * 430 ** 2)) * 0.30
    else:                            # center 中心光
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
    """半透明装饰纹理：circles 圆 / rings 圆环 / slash 斜带 / grid 点阵"""
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
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), text, font=f, fill=accent, anchor="mm")
    return y1


def footer(d):
    f = ImageFont.truetype(FR, 21)
    d.text((W / 2, H - 46), FOOT, font=f, fill=(206, 214, 222), anchor="mm")


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


def block(d, text, font, fill, y, maxw, lh=1.22, x=W / 2):
    for ln in wrap(text, font, maxw, d):
        d.text((x, y), ln, font=font, fill=fill, anchor="mm")
        y += font.size * lh
    return y


def card(im, box, fill_alpha=0, outline=None, outline_alpha=255, radius=22, width=2):
    """半透明卡片：在 RGBA 覆盖层绘制后合成，避免在 RGB 上直接画被当成实色。画布尺寸随图。"""
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fill_alpha))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


# ---------- 布局（每张 = 蓝系档位 × 渐变方向 × 光影 × 纹理，各不相同） ----------
def cover_title():
    th = BLUES["navy"]
    im = img(th, "v", "glow-tr", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 120
    y = block(d, "非深户能在深圳\n中考、读高中吗？", ImageFont.truetype(FB, 66), (255, 255, 255), y, 640)
    block(d, "答案：可以 · 但要分清两条路", ImageFont.truetype(FB, 38), th["accent"], y + 40, 800)
    f = ImageFont.truetype(FB, 28); txt = "5项条件 · 3条出路 一次讲清"
    bb = d.textbbox((0, 0), txt, font=f); pad = 34
    x0 = (W - (bb[2] + pad * 2)) / 2; y0 = H - 190; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=40, outline=th["accent"], width=2)
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), txt, font=f, fill=th["accent"], anchor="mm")
    footer(d)
    return im


def cover_data():
    th = BLUES["royal"]
    im = img(th, "radial", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 150
    fN = ImageFont.truetype(FB, 148); fL = ImageFont.truetype(FR, 34)
    d.text((W * 0.30, y), "54%", font=fN, fill=th["accent"], anchor="mm")
    d.text((W * 0.30, y + 120), "非深户考生占比", font=fL, fill=(255, 255, 255), anchor="mm")
    d.text((W * 0.70, y), "23%", font=fN, fill=(255, 255, 255), anchor="mm")
    d.text((W * 0.70, y + 120), "公办D类指标占比", font=fL, fill=(255, 255, 255), anchor="mm")
    d.line([(W / 2, y - 120), (W / 2, y + 150)], fill=th["accent"], width=3)
    block(d, "约54%的考生 · 竞争约23%的公办指标", ImageFont.truetype(FB, 34), (255, 255, 255), y + 250, 760)
    footer(d)
    return im


def cover_answer():
    th = BLUES["steel"]
    im = img(th, "d1", "beam", "slash"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 150
    d.text((W / 2, y), "可以", font=ImageFont.truetype(FB, 210), fill=th["accent"], anchor="mm")
    block(d, "非深户能在深圳参加中考、读高中", ImageFont.truetype(FB, 42), (255, 255, 255), y + 160, 820)
    block(d, "满足5项条件 → 公办/民办/中职都能报", ImageFont.truetype(FR, 30), (230, 238, 248), y + 250, 860)
    footer(d)
    return im


def table_conditions():
    th = BLUES["cobalt"]
    im = img(th, "v", "center", "grid"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 78
    block(d, "非深户报考公办高中的5项条件", ImageFont.truetype(FB, 46), (255, 255, 255), y, 780)
    rows = [
        ("1", "合法稳定职业", "父母一方在深有合法稳定职业"),
        ("2", "合法稳定住所", "父母一方在深有合法稳定住所"),
        ("3", "持有有效居住证", "父母一方持有，注意有效期"),
        ("4", "社保累计满3年", "两险都缴，至少一个险种满3年（补缴不计）"),
        ("5", "3年完整初中学籍", "在深完成3年完整初中"),
    ]
    tx0, tx2 = 340, 1140
    c1, c2 = 420, 660
    ty0 = 264; row_h = 96
    card(im, [tx0, ty0, tx2, ty0 + 60], fill_alpha=26, radius=16)
    fH = ImageFont.truetype(FB, 28)
    d.text((c1, ty0 + 30), "条件", font=fH, fill=(255, 255, 255), anchor="lm")
    d.text((c2, ty0 + 30), "关键要点", font=fH, fill=(255, 255, 255), anchor="lm")
    fN = ImageFont.truetype(FB, 30); fC = ImageFont.truetype(FR, 28); fD = ImageFont.truetype(FR, 25)
    for i, (n, c, desc) in enumerate(rows):
        ry = ty0 + 60 + i * row_h
        if i % 2 == 0:
            card(im, [tx0, ry, tx2, ry + row_h], fill_alpha=12, radius=14)
        d.ellipse([tx0 + 22, ry + row_h / 2 - 18, tx0 + 58, ry + row_h / 2 + 18], fill=th["accent"])
        d.text((tx0 + 40, ry + row_h / 2), n, font=fN, fill=(15, 40, 62), anchor="mm")
        d.text((c1, ry + row_h / 2), c, font=fC, fill=(255, 255, 255), anchor="lm")
        lines = wrap(desc, fD, tx2 - 30 - c2, d)
        if len(lines) == 1:
            d.text((c2, ry + row_h / 2), lines[0], font=fD, fill=(225, 236, 248), anchor="lm")
        else:
            for j, ln in enumerate(lines):
                d.text((c2, ry + row_h / 2 - 14 + j * 30), ln, font=fD, fill=(225, 236, 248), anchor="lm")
    footer(d)
    return im


def paths():
    th = BLUES["ink"]
    im = img(th, "d2", "glow-bl", "circles"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 84
    block(d, "非深户的三条出路", ImageFont.truetype(FB, 54), (255, 255, 255), y, 640)
    rows = [
        ("1", "公办普高", ["靠 D类指标生", "控制线约比正取线低20分"], "9,186", "名额"),
        ("2", "民办普高", ["AC/D同分录取", "学费约3万-15万/年"], "33,195", "学位"),
        ("3", "中职 · 3+4", ["中职3年+本科4年", "毕业拿全日制本科文凭"], "300", "名额"),
    ]
    bx0, bx1 = 300, 900
    by = 260; row_h = 146; gap = 22
    fN = ImageFont.truetype(FB, 40); fT = ImageFont.truetype(FB, 34)
    fS = ImageFont.truetype(FR, 24); fStat = ImageFont.truetype(FB, 52); fLab = ImageFont.truetype(FR, 24)
    for i, (n, t, subs, stat, lab) in enumerate(rows):
        ry = by + i * (row_h + gap)
        card(im, [bx0, ry, bx1, ry + row_h], fill_alpha=16, outline=th["accent"], outline_alpha=70, radius=22)
        d.ellipse([bx0 + 26, ry + row_h / 2 - 26, bx0 + 78, ry + row_h / 2 + 26], fill=th["accent"])
        d.text((bx0 + 52, ry + row_h / 2), n, font=fN, fill=(24, 38, 66), anchor="mm")
        d.text((bx0 + 118, ry + row_h / 2 - 34), t, font=fT, fill=(255, 255, 255), anchor="lm")
        for j, s in enumerate(subs):
            d.text((bx0 + 118, ry + row_h / 2 + 4 + j * 30), s, font=fS, fill=(235, 242, 250), anchor="lm")
        d.text((bx1 - 24, ry + row_h / 2 - 20), stat, font=fStat, fill=th["accent"], anchor="rm")
        d.text((bx1 - 24, ry + row_h / 2 + 46), lab, font=fLab, fill=(235, 242, 250), anchor="rm")
    footer(d)
    return im


def three_numbers():
    th = BLUES["deep"]
    im = img(th, "v", "spot", "rings"); d = ImageDraw.Draw(im)
    y = badge(d, BANNER, th["accent"]) + 84
    block(d, "非深户中考 · 3个关键数字", ImageFont.truetype(FB, 50), (255, 255, 255), y, 680)
    cards = [
        ("54%", "D类考生占比", th["accent"]),      # 金色
        ("23%", "公办D类指标占比", (255, 255, 255)),  # 纯白
        ("146,752", "高中阶段总学位", th["sec"]),     # 亮蓝
    ]
    cx = [230, 600, 970]; cw = 336; cy = 300; ch = 400
    fN = ImageFont.truetype(FB, 80); fL = ImageFont.truetype(FR, 30)
    for (num, lab, col), xc in zip(cards, cx):
        card(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fill_alpha=20, outline=(255, 255, 255), outline_alpha=90, radius=26)
        # 数字加投影增强可读性
        d.text((xc + 2, cy + 122), num, font=fN, fill=(0, 20, 45), anchor="mm")
        d.text((xc, cy + 120), num, font=fN, fill=col, anchor="mm")
        d.line([(xc - 60, cy + 250), (xc + 60, cy + 250)], fill=(255, 255, 255, 100), width=2)
        d.text((xc, cy + 286), lab, font=fL, fill=(240, 246, 252), anchor="mm")
    footer(d)
    return im


# ---------- 公众号：首图 900×383 / 章节条 900×220 / 数据卡 900×400 ----------
def wx_base(th, w, h, direction="v", light="glow-tr", pattern="circles"):
    a = make_base(th, direction, w, h)
    a = add_light(a, light, w=w, h=h)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if pattern == "circles":
        od.ellipse([w - 320, -130, w + 90, 230], fill=th["top"] + (32,))
        od.ellipse([-130, h - 190, 170, h + 40], fill=th["top"] + (20,))
        od.ellipse([w - 210, -60, w - 30, 100], outline=th["accent"] + (90,), width=3)
    elif pattern == "slash":
        for i in range(4):
            x0 = 120 + i * 220
            od.line([(x0, -40), (x0 + 120, h)], fill=th["top"] + (34,), width=50)
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def wx_cover():
    w, h = 900, 383
    th = BLUES["navy"]
    im, d = wx_base(th, w, h, "v", "glow-tr", "circles")
    fb = ImageFont.truetype(FB, 20); txt = BANNER
    bb = d.textbbox((0, 0), txt, font=fb); pad = 22
    x0 = (w - (bb[2] + pad * 2)) / 2; y0 = 34; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=30, outline=th["accent"], width=2)
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), txt, font=fb, fill=th["accent"], anchor="mm")
    d.text((w / 2, 152), "非深户能在深圳", font=ImageFont.truetype(FB, 46), fill=(255, 255, 255), anchor="mm")
    d.text((w / 2, 208), "中考、读高中吗？", font=ImageFont.truetype(FB, 46), fill=(255, 255, 255), anchor="mm")
    d.text((w / 2, 272), "答案：可以 · 但要分清两条路", font=ImageFont.truetype(FB, 26), fill=th["accent"], anchor="mm")
    fp = ImageFont.truetype(FB, 20); t2 = "5项条件 · 3条出路 一次讲清"
    bb2 = d.textbbox((0, 0), t2, font=fp); pd = 22
    px0 = (w - (bb2[2] + pd * 2)) / 2; py0 = 316; px1 = px0 + bb2[2] + pd * 2; py1 = py0 + bb2[3] + pd
    d.rounded_rectangle([px0, py0, px1, py1], radius=30, outline=th["accent"], width=2)
    d.text(((px0 + px1) / 2, (py0 + py1) / 2), t2, font=fp, fill=th["accent"], anchor="mm")
    return im


def wx_section(num, title, sub, th, direction, light, pattern):
    w, h = 900, 220
    im, d = wx_base(th, w, h, direction, light, pattern)
    cx, cy = 96, h / 2
    d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=th["accent"])
    d.text((cx, cy), num, font=ImageFont.truetype(FB, 40), fill=(18, 30, 55), anchor="mm")
    d.text((158, cy - 26), title, font=ImageFont.truetype(FB, 44), fill=(255, 255, 255), anchor="lm")
    d.text((158, cy + 28), sub, font=ImageFont.truetype(FR, 24), fill=(232, 240, 250), anchor="lm")
    return im


def wx_card_conditions():
    w, h = 900, 400
    th = BLUES["cobalt"]
    im, d = wx_base(th, w, h, "v", "center", "grid")
    block(d, "非深户报考公办高中的5项条件", ImageFont.truetype(FB, 40), (255, 255, 255), 52, 700, x=450)
    rows = [
        ("1", "合法稳定职业：父母一方在深有稳定职业"),
        ("2", "合法稳定住所：父母一方在深有稳定住所"),
        ("3", "持有有效居住证：父母一方持有"),
        ("4", "社保累计满3年：两险都缴，一个险种满3年"),
        ("5", "3年完整初中学籍：在深读完3年初中"),
    ]
    fy0 = 122; row_h = 52
    fN = ImageFont.truetype(FB, 28); fT = ImageFont.truetype(FR, 27)
    for i, (n, txt) in enumerate(rows):
        ry = fy0 + i * row_h
        d.ellipse([74, ry + row_h / 2 - 17, 108, ry + row_h / 2 + 17], fill=th["accent"])
        d.text((91, ry + row_h / 2), n, font=fN, fill=(14, 36, 66), anchor="mm")
        d.text((130, ry + row_h / 2), txt, font=fT, fill=(235, 243, 252), anchor="lm")
    return im


def wx_card_paths():
    w, h = 900, 400
    th = BLUES["deep"]
    im, d = wx_base(th, w, h, "v", "spot", "circles")
    block(d, "非深户的三条出路", ImageFont.truetype(FB, 40), (255, 255, 255), 50, 640, x=450)
    rows = [
        ("1", "公办普高 · D类指标生", "9,186个名额 · 控制线约低20分"),
        ("2", "民办普高 · AC/D同分", "33,195个学位 · 学费3万-15万/年"),
        ("3", "中职 · 3+4中本贯通", "300个名额 · 可拿本科文凭"),
    ]
    fy0 = 118; row_h = 82
    fN = ImageFont.truetype(FB, 34); fT = ImageFont.truetype(FB, 30); fS = ImageFont.truetype(FR, 24)
    for i, (n, t, sub) in enumerate(rows):
        ry = fy0 + i * (row_h + 6)
        card(im, [70, ry, 830, ry + row_h], fill_alpha=14, outline=th["accent"], outline_alpha=60, radius=18)
        d.ellipse([92, ry + row_h / 2 - 20, 132, ry + row_h / 2 + 20], fill=th["accent"])
        d.text((112, ry + row_h / 2), n, font=fN, fill=(12, 44, 68), anchor="mm")
        d.text((160, ry + row_h / 2), t, font=fT, fill=(255, 255, 255), anchor="lm")
        d.text((800, ry + row_h / 2), sub, font=fS, fill=(235, 243, 252), anchor="rm")
    return im


def wx_card_numbers():
    w, h = 900, 400
    th = BLUES["navy"]
    im, d = wx_base(th, w, h, "radial", "glow-tr", "rings")
    block(d, "非深户中考 · 3个关键数字", ImageFont.truetype(FB, 40), (255, 255, 255), 50, 680, x=450)
    cards = [
        ("54%", "D类考生占比", th["accent"]),
        ("23%", "公办D类指标占比", (255, 255, 255)),
        ("146,752", "高中阶段总学位", th["sec"]),
    ]
    cx = [170, 450, 730]; cw = 258; cy = 132; ch = 232
    fN = ImageFont.truetype(FB, 58); fL = ImageFont.truetype(FR, 26)
    for (num, lab, col), xc in zip(cards, cx):
        card(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fill_alpha=18, outline=(255, 255, 255), outline_alpha=80, radius=20)
        d.text((xc + 2, cy + 86), num, font=fN, fill=(0, 18, 40), anchor="mm")
        d.text((xc, cy + 84), num, font=fN, fill=col, anchor="mm")
        d.line([(xc - 52, cy + 168), (xc + 52, cy + 168)], fill=(255, 255, 255, 100), width=2)
        d.text((xc, cy + 196), lab, font=fL, fill=(240, 246, 252), anchor="mm")
    return im


# ---------- 主流程 ----------
def main():
    jobs = [
        ("封面1-主标题", cover_title),
        ("封面2-数据对撞", cover_data),
        ("封面3-答案大字", cover_answer),
        ("正文图-5项条件表", table_conditions),
        ("正文图-三条出路", paths),
        ("微头条配图-3关键数字", three_numbers),
    ]
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    for name, fn in jobs:
        im = fn()
        path = os.path.join(out, f"{name}-1200x900.png")
        im.save(path)
        print("OK", path)
    wx_jobs = [
        ("公众号首图", wx_cover),
        ("公众号章节条1-资格", lambda: wx_section("一", "资格 · 两条路", "满足5项条件 → 公办/民办/中职都能报", BLUES["royal"], "v", "spot", "circles")),
        ("公众号章节条2-竞争", lambda: wx_section("二", "竞争 · 54% vs 23%", "D类考生占比 vs 公办D类指标占比", BLUES["steel"], "d1", "beam", "slash")),
        ("公众号章节条3-出路", lambda: wx_section("三", "出路 · 三条路", "公办指标生 · 民办同分 · 中职3+4", BLUES["ink"], "d2", "glow-bl", "circles")),
        ("公众号数据卡1-5项条件", wx_card_conditions),
        ("公众号数据卡2-三条出路", wx_card_paths),
        ("公众号数据卡3-3关键数字", wx_card_numbers),
    ]
    for name, fn in wx_jobs:
        im = fn()
        path = os.path.join(out, f"{name}-{im.size[0]}x{im.size[1]}.png")
        im.save(path)
        print("OK", path)


if __name__ == "__main__":
    main()
