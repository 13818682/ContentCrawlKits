# -*- coding: utf-8 -*-
"""
P1-2 子任务04 · 隐形战场卡（900×600）
========================================
630背后隐藏规则③：不计入总分的隐形战场——生地同分PK + 信技/艺术入场券。
版式对齐 02/03卡：标题 + 生地PK案例卡 + 同分PK两层 + 信技门槛 + 底部金句
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
    bt = "深圳中考 · P1系列 · 630背后的隐藏规则③"
    bb = d.textbbox((0, 0), bt, font=f_badge); pd = 16
    bx0 = (W - (bb[2] + pd * 2)) / 2; by0 = 30; bx1 = bx0 + bb[2] + pd * 2; by1 = by0 + bb[3] + pd
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=24, outline=GOLD, width=2)
    T(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), bt, f_badge, GOLD, "mm", "badge")

    # 主标题
    T(d, (W / 2, 100), "不计总分 · 却决定命运的两个隐形战场", ImageFont.truetype(FB, 34), WHITE, "mm", "title")

    # 一、生地同分PK案例卡（内容区整体下移，标题→①间距拉开）
    T(d, (W / 2, 172), "① 生地会考 · 同分PK的胜负手", ImageFont.truetype(FB, 24), GOLD, "mm", "sec1")
    # 案例对比卡
    case_w, case_h, case_gap = 380, 120, 40
    cx0 = (W - (2 * case_w + case_gap)) // 2
    cy0 = 206
    # 考生A（录取）
    card(d, [cx0, cy0, cx0 + case_w, cy0 + case_h], fill_alpha=14, outline=GOLD, outline_alpha=150, radius=16)
    T(d, (cx0 + 90, cy0 + 32), "考生A", ImageFont.truetype(FB, 22), WHITE, "mm", "caseA-t")
    T(d, (cx0 + 90, cy0 + 80), "总分552", ImageFont.truetype(FB, 24), GOLD, "mm", "caseA-sc")
    T(d, (cx0 + case_w - 90, cy0 + 80), "生地96", ImageFont.truetype(FB, 20), GOLD, "mm", "caseA-bio")
    # 考生B
    card(d, [cx0 + case_w + case_gap, cy0, cx0 + 2 * case_w + case_gap, cy0 + case_h], fill_alpha=10, outline=EDGE, outline_alpha=100, radius=16)
    T(d, (cx0 + case_w + case_gap + 90, cy0 + 32), "考生B", ImageFont.truetype(FB, 22), WHITE, "mm", "caseB-t")
    T(d, (cx0 + case_w + case_gap + 90, cy0 + 80), "总分552", ImageFont.truetype(FB, 24), WHITE, "mm", "caseB-sc")
    T(d, (cx0 + case_w + case_gap + case_w - 90, cy0 + 80), "生地82", ImageFont.truetype(FB, 20), SUB, "mm", "caseB-bio")
    # 说明（A录取标签用自绘对勾替代 ✓）
    def draw_check(draw, cx, cy, size, color=GOLD):
        draw.line([(cx - size, cy), (cx - size * 0.3, cy + size * 0.7)], fill=color, width=4)
        draw.line([(cx - size * 0.3, cy + size * 0.7), (cx + size, cy - size * 0.5)], fill=color, width=4)
    draw_check(d, 138 + cx0, 356, 10)
    T(d, (cx0 + case_w + 20, 356), "总分相同 → 先比生地 → 考生A录取", ImageFont.truetype(FB, 20), WHITE, "lm", "case-note")

    # 二、同分PK两层 + 信技门槛
    T(d, (W / 2, 412), "② 同分PK顺序 & 报考门槛", ImageFont.truetype(FB, 24), GOLD, "mm", "sec2")
    pk_rows = [
        ("第1层", "生物与地理（合卷）", "高者优先"),
        ("第2层", "语数英三科总分", "生地相同才比"),
    ]
    f_lv = ImageFont.truetype(FB, 20)
    f_it = ImageFont.truetype(FR, 17)
    y2 = 448
    for i, (lv, item, rule) in enumerate(pk_rows):
        cy = y2 + i * 36
        T(d, (200, cy), lv, f_lv, GOLD, "mm", f"pk{i}-lv")
        T(d, (390, cy), item, f_it, WHITE, "lm", f"pk{i}-item")
        T(d, (700, cy), rule, f_it, LIGHT, "mm", f"pk{i}-rule")

    # 底部金句
    T(d, (W / 2, 578), "生地已定别慌 · 语数英还能对冲 · 信技艺术确认合格", ImageFont.truetype(FB, 18), WHITE, "mm", "bottom")

    path = os.path.join(out, "P1-2-子任务04-隐形战场-900x600.png")
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
