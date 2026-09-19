# -*- coding: utf-8 -*-
"""
P1-2 子任务02 · 科目性价比卡（900×600）
========================================
630背后规则①：科目性价比——同样的复习时间，投入产出比不同。
版式对齐 P1-1 子任务卡：标题 + 分组条 + 性价比明细 + 底部金句
配色沿用系列统一：深蓝渐变 + 金色数据 + 浅蓝次级
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
    bt = "深圳中考 · P1系列 · 630背后的隐藏规则①"
    bb = d.textbbox((0, 0), bt, font=f_badge); pd = 16
    bx0 = (W - (bb[2] + pd * 2)) / 2; by0 = 30; bx1 = bx0 + bb[2] + pd * 2; by1 = by0 + bb[3] + pd
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=24, outline=GOLD, width=2)
    T(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), bt, f_badge, GOLD, "mm", "badge")

    # 主标题（下移避开徽章，徽章底≈62 → 标题中心 y=105）
    T(d, (W / 2, 105), "630分 · 每1分的性价比不一样", ImageFont.truetype(FB, 38), WHITE, "mm", "title")
    # 副题
    T(d, (W / 2, 148), "同样的复习时间，投到回报最高的科目", ImageFont.truetype(FR, 22), LIGHT, "mm", "subtitle")

    # 逐科性价比（等级用自绘金星 + 文字，不用 emoji）
    def draw_star(draw, cx, cy, r, n=5, color=GOLD):
        import math
        pts = []
        for i in range(n * 2):
            ang = -math.pi / 2 + i * math.pi / n
            rad = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=color)

    subjects = [
        ("语数英物化", 5, "440分主战场 · 决定公办民办", GOLD),
        ("理化实验", 5, "2026涨到20分 · 8分增量性价比之王", GOLD),
        ("英语听说", 4, "25分可提前锁定 · 5月单独考", WHITE),
        ("体育", 4, "50分 · 过程14分初一已累积", WHITE),
        ("历史", 3, "记背为主 · 区分度低", LIGHT),
        ("道法", 3, "2026开卷 · 考理解不考记忆", LIGHT),
    ]
    f_sub = ImageFont.truetype(FB, 22)
    f_note = ImageFont.truetype(FR, 17)
    y0 = 200
    row_h = 56
    for i, (sub, starcount, note, col) in enumerate(subjects):
        cy = y0 + i * row_h
        card(d, [56, cy - 23, 844, cy + 23], fill_alpha=10, outline=None, radius=10)
        T(d, (205, cy), sub, f_sub, WHITE, "mm", f"s{i}-sub")
        # 自绘金星（最多5颗，每颗间隔 26px，从 x=410 起）
        for s in range(starcount):
            draw_star(d, 410 + s * 28, cy, 10)
        T(d, (585, cy), note, f_note, LIGHT, "lm", f"s{i}-note")
    # 分隔线
    d.line([56, 530, 844, 530], fill=EDGE, width=2)

    # 底部金句
    T(d, (W / 2, 562), "精力是有限的 · 花在刀刃上", ImageFont.truetype(FB, 22), WHITE, "mm", "bottom")

    path = os.path.join(out, "P1-2-子任务02-科目性价比-900x600.png")
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
