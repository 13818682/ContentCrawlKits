# -*- coding: utf-8 -*-
"""
深圳中考 · 问答系列 · 002 公众号配图生成脚本
============================================
文章：普高和中职每年学费差多少？
产出：公众号配图 7 张（文件名统一以「公众号配图」开头）
  - 公众号配图-首图-900x383.png
  - 公众号配图-章节条1/2/3-900x220.png
  - 公众号配图-数据卡1/2/3-900x400.png
设计：统一蓝色系家族(6档) + 金色强调 + 顶部胶囊徽章「深圳中考·问答系列·002」
      + 微软雅黑 + 版心安全区；变化靠蓝系深浅×渐变方向×光影×纹理。
复用自 001 的 _build_qa_images.py（wx_* 公众号函数段）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"   # 微软雅黑粗体
FR = "C:/Windows/Fonts/msyh.ttc"     # 微软雅黑

BLUES = {
    "navy":   dict(top=(20, 59, 115),  bot=(10, 32, 60),  accent=(242, 184, 75),  sec=(150, 205, 255)),
    "royal":  dict(top=(22, 70, 130),  bot=(10, 32, 64),  accent=(242, 184, 75),  sec=(140, 200, 255)),
    "steel":  dict(top=(42, 66, 106),  bot=(18, 30, 52),  accent=(242, 184, 75),  sec=(168, 202, 244)),
    "cobalt": dict(top=(16, 58, 120),  bot=(7, 26, 60),   accent=(242, 184, 75),  sec=(126, 188, 255)),
    "ink":    dict(top=(30, 48, 86),   bot=(12, 20, 40),  accent=(242, 184, 75),  sec=(150, 180, 232)),
    "deep":   dict(top=(14, 84, 140),  bot=(8, 36, 70),   accent=(242, 184, 75),  sec=(182, 220, 255)),
}

BANNER = "深圳中考 · 问答系列 · 002"


def make_base(theme, direction="v", w=900, h=400):
    T = np.array(theme["top"], float); B = np.array(theme["bot"], float)
    if direction == "v":
        t = np.linspace(0, 1, h)[:, None, None]
        a = T[None, None, :] * (1 - t) + B[None, None, :] * t
        a = np.repeat(a, w, axis=1)
    elif direction == "d1":
        x = np.linspace(0, 1, w)[None, :, None]; y = np.linspace(0, 1, h)[:, None, None]
        t = (x + y) / 2; a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    elif direction == "d2":
        x = np.linspace(0, 1, w)[None, :, None]; y = np.linspace(0, 1, h)[:, None, None]
        t = (1 - x + y) / 2; a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    else:
        t = np.linspace(0, 1, h)[:, None, None]
        a = T[None, None, :] * (1 - t) + B[None, None, :] * t
        a = np.repeat(a, w, axis=1)
        y, x = np.mgrid[0:h, 0:w]
        d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
        a = a * (1 - 0.36 * np.clip(d - 0.55, 0, None)[..., None])
    return a


def add_light(a, kind, w=900, h=400, color=(255, 255, 255)):
    y, x = np.mgrid[0:h, 0:w]; c = np.array(color, float)
    if kind == "glow-tr":
        d = np.sqrt((x - w * 0.86) ** 2 + (y - h * 0.10) ** 2); g = np.exp(-d ** 2 / (2 * 300 ** 2)) * 0.30
    elif kind == "glow-bl":
        d = np.sqrt((x - w * 0.14) ** 2 + (y - h * 0.88) ** 2); g = np.exp(-d ** 2 / (2 * 320 ** 2)) * 0.28
    elif kind == "beam":
        d = np.abs(1.8 * x - y - 120) / np.sqrt(1.8 ** 2 + 1); g = np.exp(-d ** 2 / (2 * 260 ** 2)) * 0.22
    elif kind == "spot":
        d = np.sqrt((x - w / 2) ** 2 + (y - h * 0.18) ** 2); g = np.exp(-d ** 2 / (2 * 320 ** 2)) * 0.30
    else:
        d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
        g = np.clip(0.28 * (1 - d), 0, None) * 0.9
    return np.clip(a + c * g[..., None], 0, 255)


def wx_base(th, w, h, direction="v", light="glow-tr", pattern="circles"):
    a = make_base(th, direction, w, h)
    a = add_light(a, light, w, h)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    top = th["top"]; accent = th["accent"]
    if pattern == "circles":
        od.ellipse([w - 320, -130, w + 90, 230], fill=top + (32,))
        od.ellipse([-130, h - 190, 170, h + 40], fill=top + (20,))
        od.ellipse([w - 210, -60, w - 30, 100], outline=accent + (90,), width=3)
    elif pattern == "rings":
        cx, cy = w - 120, h - 120
        for r in (90, 140, 190):
            od.ellipse([cx - r, cy - r, cx + r, cy + r], outline=top + (50,), width=2)
    elif pattern == "slash":
        for i in range(4):
            x0 = 120 + i * 220
            od.line([(x0, -40), (x0 + 120, h)], fill=top + (34,), width=50)
        od.line([(w - 100, -60), (w + 60, h)], fill=accent + (55,), width=22)
    elif pattern == "grid":
        for x in range(60, w, 84):
            for y in range(60, h, 84):
                od.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 20))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def T(d, xy, text, font, fill, anchor="mm", w=900, h=400, name="", pad=6):
    """带越界校验的文本绘制：超出画布即打印警告（不中断），返回实际bbox。"""
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
    if x0 < pad or x0 + bw > w - pad or y0 < pad or y0 + bh > h - pad:
        print(f"[溢出警告] {name}: '{text}' 宽{bw} 位置x0={x0:.0f}->{x0+bw:.0f} y0={y0:.0f}->{y0+bh:.0f} (画布{w}x{h})")
    d.text(xy, text, font=font, fill=fill, anchor=anchor)
    return (x0, y0, x0 + bw, y0 + bh)


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


def block(d, text, font, fill, y, maxw, lh=1.22, x=450, w=900, h=400, name=""):
    for ln in wrap(text, font, maxw, d):
        T(d, (x, y), ln, font, fill, "mm", w, h, name)
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


def badge_capsule(d, text, accent, w, y0=34, name=""):
    f = ImageFont.truetype(FB, 20)
    bb = d.textbbox((0, 0), text, font=f); pad = 22
    x0 = (w - (bb[2] + pad * 2)) / 2; y0 = y0; x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + pad
    d.rounded_rectangle([x0, y0, x1, y1], radius=30, outline=accent, width=2)
    T(d, ((x0 + x1) / 2, (y0 + y1) / 2), text, f, accent, "mm", w, y1 + 30, name)
    return y1


# ---------- 首图 900×383 ----------
def wx_cover():
    w, h = 900, 383
    th = BLUES["navy"]
    im, d = wx_base(th, w, h, "v", "glow-tr", "circles")
    badge_capsule(d, BANNER, th["accent"], w, name="首图-badge")
    T(d, (w / 2, 152), "同样读三年书", ImageFont.truetype(FB, 46), (255, 255, 255), "mm", w, h, "首图-标题1")
    T(d, (w / 2, 206), "有人花1万 · 有人花30万", ImageFont.truetype(FB, 46), (255, 255, 255), "mm", w, h, "首图-标题2")
    T(d, (w / 2, 272), "普高和中职的学费差 · 家长现在就得看清", ImageFont.truetype(FB, 25), th["accent"], "mm", w, h, "首图-副题")
    fp = ImageFont.truetype(FB, 20); t2 = "三年总账 · 三个数字 · 三件事"
    bb2 = d.textbbox((0, 0), t2, font=fp); pd = 22
    px0 = (w - (bb2[2] + pd * 2)) / 2; py0 = 318; px1 = px0 + bb2[2] + pd * 2; py1 = py0 + bb2[3] + pd
    d.rounded_rectangle([px0, py0, px1, py1], radius=30, outline=th["accent"], width=2)
    T(d, ((px0 + px1) / 2, (py0 + py1) / 2), t2, fp, th["accent"], "mm", w, h, "首图-胶囊")
    return im


# ---------- 章节条 900×220 ----------
def wx_section(num, title, sub, th, direction, light, pattern, name):
    w, h = 900, 220
    im, d = wx_base(th, w, h, direction, light, pattern)
    cx, cy = 96, h / 2
    d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=th["accent"])
    T(d, (cx, cy), num, ImageFont.truetype(FB, 40), (18, 30, 55), "mm", w, h, name + "-num")
    T(d, (158, cy - 26), title, ImageFont.truetype(FB, 44), (255, 255, 255), "lm", w, h, name + "-title")
    T(d, (158, cy + 28), sub, ImageFont.truetype(FR, 24), (232, 240, 250), "lm", w, h, name + "-sub")
    return im


# ---------- 数据卡 900×400 ----------
def wx_card_table():
    w, h = 900, 400
    th = BLUES["cobalt"]
    im, d = wx_base(th, w, h, "v", "center", "grid")
    block(d, "同样读三年书 · 四类学校总账", ImageFont.truetype(FB, 38), (255, 255, 255), 46, 640, x=450, w=w, h=h, name="卡1-标题")
    # 表头行
    tx0, tx1 = 60, 840
    fH = ImageFont.truetype(FB, 24)
    card(im, [tx0, 102, tx1, 148], fill_alpha=26, radius=16)
    T(d, (190, 125), "学校类型", fH, (255, 255, 255), "mm", w, h, "卡1-表头-类型")
    T(d, (505, 125), "三年总花费（约）", fH, (255, 255, 255), "mm", w, h, "卡1-表头-花费")
    T(d, (770, 125), "与公办比", fH, (255, 255, 255), "mm", w, h, "卡1-表头-对比")
    # 数据行（每行单行文字，行距充足，不重叠）
    rows = [
        ("公办普高", "约1万", "基准", (255, 255, 255)),
        ("民办普高", "21万-36万", "贵约25-40倍", th["accent"]),
        ("公办中职", "约3千", "免学费", (255, 255, 255)),
        ("民办中职", "5万-10万", "贵约20-35倍", th["accent"]),
    ]
    fT = ImageFont.truetype(FB, 28); fN = ImageFont.truetype(FB, 30); fS = ImageFont.truetype(FR, 22)
    ry0 = 156; row_h = 58
    for i, (label, num, note, col) in enumerate(rows):
        ry = ry0 + i * row_h
        if i % 2 == 0:
            card(im, [tx0, ry, tx1, ry + row_h], fill_alpha=12, radius=14)
        T(d, (190, ry + row_h / 2), label, fT, (235, 243, 252), "mm", w, h, f"卡1-{label}")
        T(d, (505, ry + row_h / 2), num, fN, col, "mm", w, h, f"卡1-{label}-花费")
        T(d, (770, ry + row_h / 2), note, fS, (225, 236, 248), "mm", w, h, f"卡1-{label}-对比")
    return im


def wx_card_numbers():
    w, h = 900, 400
    th = BLUES["deep"]
    im, d = wx_base(th, w, h, "v", "spot", "rings")
    block(d, "三个让你清醒的数字", ImageFont.truetype(FB, 40), (255, 255, 255), 50, 640, x=450, w=w, h=h, name="卡2-标题")
    cards = [
        ("33%", "考生家庭读民办", th["accent"]),
        ("25-40倍", "民办比公办贵", (255, 255, 255)),
        ("9.9万/年", "深圳私营平均工资", th["sec"]),
    ]
    cx = [150, 450, 750]; cw = 280; cy = 130; ch = 236
    fN = ImageFont.truetype(FB, 42); fL = ImageFont.truetype(FR, 25)
    for (num, lab, col), xc in zip(cards, cx):
        card(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fill_alpha=18, outline=(255, 255, 255), outline_alpha=80, radius=20)
        T(d, (xc + 2, cy + 88), num, fN, (0, 18, 40), "mm", w, h, "卡2-投影")
        T(d, (xc, cy + 86), num, fN, col, "mm", w, h, "卡2-数字")
        d.line([(xc - 56, cy + 168), (xc + 56, cy + 168)], fill=(255, 255, 255, 100), width=2)
        T(d, (xc, cy + 198), lab, fL, (240, 246, 252), "mm", w, h, "卡2-标签")
    return im


def wx_card_guantong():
    w, h = 900, 400
    th = BLUES["navy"]
    im, d = wx_base(th, w, h, "radial", "glow-tr", "rings")
    block(d, "公办中职 · 便宜但名额少", ImageFont.truetype(FB, 40), (255, 255, 255), 46, 640, x=450, w=w, h=h, name="卡3-标题")
    T(d, (w / 2, 170), "约2,300个", ImageFont.truetype(FB, 70), th["accent"], "mm", w, h, "卡3-大数字")
    T(d, (w / 2, 248), "公办中职贯通本科名额", ImageFont.truetype(FB, 28), (255, 255, 255), "mm", w, h, "卡3-标签")
    fS = ImageFont.truetype(FR, 23)
    T(d, (w / 2, 302), "3+4中本贯通仅300个 · 3+2公办约1,960个", fS, (225, 236, 248), "mm", w, h, "卡3-明细1")
    T(d, (w / 2, 342), "15.3万考生竞争 · 名额少得可怜", fS, th["accent"], "mm", w, h, "卡3-明细2")
    return im


# ---------- 主流程 ----------
def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    jobs = [
        ("公众号配图-首图-900x383.png", wx_cover),
        ("公众号配图-章节条1-三年总账-900x220.png", lambda: wx_section("一", "三年总账", "公办普高1万 vs 民办普高21-36万", BLUES["royal"], "v", "spot", "circles", "章节1")),
        ("公众号配图-章节条2-三个数字-900x220.png", lambda: wx_section("二", "三个清醒的数字", "每3个考生1个进民办 · 民办贵25-40倍", BLUES["steel"], "d1", "beam", "slash", "章节2")),
        ("公众号配图-章节条3-三件事-900x220.png", lambda: wx_section("三", "现在就该做的三件事", "看数据 · 定预算 · 比通道", BLUES["ink"], "d2", "glow-bl", "circles", "章节3")),
        ("公众号配图-数据卡1-三年总账-900x400.png", wx_card_table),
        ("公众号配图-数据卡2-三个数字-900x400.png", wx_card_numbers),
        ("公众号配图-数据卡3-贯通名额-900x400.png", wx_card_guantong),
    ]
    for name, fn in jobs:
        im = fn()
        path = os.path.join(out, name)
        im.save(path)
        print("OK", path)


if __name__ == "__main__":
    main()
