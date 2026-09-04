# -*- coding: utf-8 -*-
"""
P1-2 子任务03 · 单科等级制卡（900×600）
========================================
630背后隐藏规则②：单科等级制——A+永远是前5%，等级比分数更准。
版式对齐 P1-1/02卡：标题 + 等级比例表 + 门槛强调 + 底部金句
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
WARN = (245, 156, 96)

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
    bt = "深圳中考 · P1系列 · 630背后的隐藏规则②"
    bb = d.textbbox((0, 0), bt, font=f_badge); pd = 16
    bx0 = (W - (bb[2] + pd * 2)) / 2; by0 = 30; bx1 = bx0 + bb[2] + pd * 2; by1 = by0 + bb[3] + pd
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=24, outline=GOLD, width=2)
    T(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), bt, f_badge, GOLD, "mm", "badge")

    # 主标题
    T(d, (W / 2, 100), "单科等级 · 比分数更准的定位", ImageFont.truetype(FB, 38), WHITE, "mm", "title")
    # 副题
    T(d, (W / 2, 142), "试卷难度每年不同 · 等级按全市固定比例", ImageFont.truetype(FR, 21), LIGHT, "mm", "subtitle")

    # 等级比例表（6 行）
    grades = [
        ("A+", "前5%", "全市顶尖 · 这门是你的王牌", GOLD),
        ("A", "前5%-25%", "单科优秀 · 稳定输出", WHITE),
        ("B+", "前25%-50%", "中等偏上 · 不拖后腿", WHITE),
        ("B", "前50%-75%", "中等 · 有提升空间", WHITE),
        ("C+", "前75%-95%", "偏下 · 需要重点关注", WHITE),
        ("C", "后5%", "较弱 · 必须补短板", WARN),
    ]
    f_grade = ImageFont.truetype(FB, 24)
    f_pct = ImageFont.truetype(FB, 20)
    f_desc = ImageFont.truetype(FR, 17)
    y0 = 208
    row_h = 46
    for i, (g, pct, desc, col) in enumerate(grades):
        cy = y0 + i * row_h
        if i % 2 == 0:
            card(d, [56, cy - 20, 844, cy + 20], fill_alpha=8, radius=10)
        T(d, (170, cy), g, f_grade, col, "mm", f"g{i}-grade")
        T(d, (340, cy), pct, f_pct, WHITE, "mm", f"g{i}-pct")
        T(d, (460, cy), desc, f_desc, LIGHT, "lm", f"g{i}-desc")

    # 门槛强调条（6行末行卡底458 → 门槛条 486起，高90）
    card(d, [56, 486, 844, 576], fill_alpha=18, outline=WARN, outline_alpha=180, radius=14)
    T(d, (450, 512), "省一级学校门槛：所有科目 C+ 及以上（体育C）", ImageFont.truetype(FB, 22), WARN, "mm", "gate1")
    T(d, (450, 552), "· 不能有任何一科掉到 C", ImageFont.truetype(FB, 22), WHITE, "mm", "gate2")

    path = os.path.join(out, "P1-2-子任务03-单科等级制-900x600.png")
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
