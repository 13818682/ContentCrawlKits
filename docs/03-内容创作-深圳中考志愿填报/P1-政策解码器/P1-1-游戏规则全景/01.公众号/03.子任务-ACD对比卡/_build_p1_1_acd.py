# -*- coding: utf-8 -*-
"""
P1-1 子任务03 · ACD对比卡（900×600）
========================================
深圳中考考生分ACD三类：A最宽赛道 / C跨区 / D非深户窄赛道但有弯道
版式：标题 + 三类对比横卡 + D类关键数据行 + 底部金句
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

TOP = (27, 58, 92)
BOT = (13, 30, 48)
WHITE = (255, 255, 255)
GOLD = (245, 198, 107)
LIGHT = (157, 184, 212)
SUB = (201, 217, 232)
CARD = (31, 66, 106)
EDGE = (58, 100, 148)

W, H = 900, 600
BBOXES = []


def base(w=W, h=H):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - w * 0.15) / (w * 0.5)) ** 2 + ((y - h * 0.15) / (h * 0.5)) ** 2)
    a = a * (1 - 0.22 * np.clip(d - 0.6, 0, None)[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([w - 300, -120, w + 100, 220], fill=TOP + (30,))
    od.ellipse([-140, h - 180, 150, h + 40], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def T(d, xy, text, font, fill, anchor="mm", name="", pad=4):
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
        print(f"[溢出] {name}: '{text}' x0={x0:.0f}->{x0+bw:.0f} y0={y0:.0f}->{y0+bh:.0f}")
    d.text(xy, text, font=font, fill=fill, anchor=anchor)
    BBOXES.append((name, (x0, y0, x0 + bw, y0 + bh)))
    return (x0, y0, x0 + bw, y0 + bh)


def card(d, box, fill_alpha=0, outline=None, outline_alpha=255, radius=16, width=2):
    im = d._image
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fill_alpha))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    im, d = base()

    # 徽章
    f_badge = ImageFont.truetype(FB, 18)
    bt = "深圳中考 · P1系列 · 游戏规则全景"
    bb = d.textbbox((0, 0), bt, font=f_badge); pd = 16
    bx0 = (W - (bb[2] + pd * 2)) / 2; by0 = 30; bx1 = bx0 + bb[2] + pd * 2; by1 = by0 + bb[3] + pd
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=24, outline=GOLD, width=2)
    T(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), bt, f_badge, GOLD, "mm", "badge")

    # 主标题
    T(d, (W / 2, 106), "考生分 ACD 三类，站哪条赛道？", ImageFont.truetype(FB, 40), WHITE, "mm", "title")

    # 三类对比横卡（并列 3 张，卡高 120，间距 25）
    cats = [
        ("A类", "深户+学籍同区", "所有学校都能报", GOLD),
        ("C类", "深户+学籍跨区", "部分学校有限制", WHITE),
        ("D类", "非深户", "公办指标仅占约23%", LIGHT),
    ]
    f_cat = ImageFont.truetype(FB, 34)
    f_cond = ImageFont.truetype(FR, 20)
    f_key = ImageFont.truetype(FB, 21)
    cw, ch3 = 246, 120
    y3 = 160
    x0s = [68, 336, 604]
    for i, (cat, cond, key, col) in enumerate(cats):
        x = x0s[i] + cw / 2
        card(d, [x - cw / 2, y3, x + cw / 2, y3 + ch3], fill_alpha=16, outline=EDGE, outline_alpha=90, radius=14)
        T(d, (x, y3 + 34), cat, f_cat, col, "mm", f"cat{i}-tag")
        T(d, (x, y3 + 68), cond, f_cond, WHITE, "mm", f"cat{i}-cond")
        d.line([(x - 60, y3 + 86), (x + 60, y3 + 86)], fill=(255, 255, 255, 90), width=1)
        T(d, (x, y3 + 102), key, f_key, col, "mm", f"cat{i}-key")
    # 三类卡底部一句话
    T(d, (W / 2, 316), "一句话：深户看 A/C 区别，非深户看 D 类三条", ImageFont.truetype(FR, 20), SUB, "mm", "cat-sum")

    # D类三条关键数据（横条）
    T(d, (W / 2, 350), "D 类家长 · 先记住这三条", ImageFont.truetype(FB, 26), GOLD, "mm", "d-title")
    d_lines = [
        ("① 占比", "非深户考生过半，公办普高指标 D 类仅约 23%"),
        ("② 差距", "四大名校 ACD 持平，中下层次 D 类高 5-15 分"),
        ("③ 通道", "指标生已覆盖 D 类 —— 最重要的降分通道"),
    ]
    f_k = ImageFont.truetype(FB, 20)
    f_v = ImageFont.truetype(FR, 18)
    yD = 386
    for i, (k, v) in enumerate(d_lines):
        ry = yD + i * 56
        card(d, [70, ry, 830, ry + 44], fill_alpha=10, outline=EDGE, outline_alpha=70, radius=10)
        T(d, (100, ry + 22), k, f_k, GOLD, "lm", f"d{i}-k")
        T(d, (210, ry + 22), v, f_v, WHITE, "lm", f"d{i}-v")

    # 底部金句
    T(d, (W / 2, 566), "不是要制造焦虑 · 而是信息准备对 D 类更重要", ImageFont.truetype(FB, 24), GOLD, "mm", "bottom")

    path = os.path.join(out, "P1-1-子任务03-ACD对比卡-900x600.png")
    im.save(path)
    print("OK", path)

    # ---- 校验 ----
    print("=== 越界检测 ===")
    bad = False
    for name, (x0, y0, x1, y1) in BBOXES:
        if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
            print(f"[FAIL] {name}: {x0:.0f},{y0:.0f}->{x1:.0f},{y1:.0f}")
            bad = True
    print("OVERFLOW: PASS" if not bad else "OVERFLOW: FAIL")
    print("=== 重叠检测 ===")
    n_ov = 0
    for i in range(len(BBOXES)):
        for j in range(i + 1, len(BBOXES)):
            n1, r1 = BBOXES[i]; n2, r2 = BBOXES[j]
            ox = min(r1[2], r2[2]) - max(r1[0], r2[0])
            oy = min(r1[3], r2[3]) - max(r1[1], r2[1])
            if ox > 4 and oy > 4:
                print(f"[重叠?] {n1} <-> {n2} ox={ox:.0f} oy={oy:.0f}")
                n_ov += 1
    print("OVERLAP: PASS" if n_ov == 0 else f"OVERLAP: {n_ov} 对重叠")


if __name__ == "__main__":
    main()
