# -*- coding: utf-8 -*-
"""
P1-1 子任务04 · 批次顺序卡（900×600）
========================================
深圳中考录取分五个批次，前一批录了后面全作废
版式：标题 + 5批次纵向阶梯卡（序号+批次名+志愿数+一句说明）+ 关键提醒 + 底部金句
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
    T(d, (W / 2, 96), "录取分五个批次，前一批录了", ImageFont.truetype(FB, 36), WHITE, "mm", "title1")
    T(d, (W / 2, 142), "后面全部作废", ImageFont.truetype(FB, 36), GOLD, "mm", "title2")

    # 5批次纵向阶梯卡：每卡高52，行距64（卡间隙12）
    batches = [
        ("第1批", "自主招生批", "1个志愿", "自招资格高中/中职", WHITE),
        ("第2批", "名额分配批", "1个志愿", "1所公办普高（指标生）", WHITE),
        ("第3批", "统一招生第一批", "16个志愿", "普高≤12 + 中职≤4", GOLD),
        ("第4批", "统一招生第二批", "18个志愿", "本市中职、技校专业", WHITE),
        ("第5批", "统一招生第三批", "6个志愿", "外省市中职学校", WHITE),
    ]
    f_no = ImageFont.truetype(FB, 20)
    f_name = ImageFont.truetype(FB, 22)
    f_cnt = ImageFont.truetype(FB, 20)
    f_desc = ImageFont.truetype(FR, 16)
    f_left = ImageFont.truetype(FB, 18)
    ch, row_h = 52, 64
    y0 = 212
    for i, (no, name, cnt, desc, col) in enumerate(batches):
        cy = y0 + i * row_h
        # 序号圆
        d.ellipse([78, cy - 18, 118, cy + 18], fill=GOLD if col == GOLD else EDGE)
        T(d, (98, cy), str(i + 1), f_no, (13, 30, 48) if col == GOLD else WHITE, "mm", f"b{i}-no")
        # 批次名（左侧）
        T(d, (140, cy), name, f_name, col, "lm", f"b{i}-name")
        # 志愿数胶囊（中部）
        cb = d.textbbox((0, 0), cnt, font=f_cnt); cpad = 12
        ccx = 560
        cx0 = ccx - (cb[2] + cpad * 2) / 2; cx1 = ccx + (cb[2] + cpad * 2) / 2
        d.rounded_rectangle([cx0, cy - 15, cx1, cy + 15], radius=15, outline=col, width=2)
        T(d, (ccx, cy), cnt, f_cnt, col, "mm", f"b{i}-cnt")
        # 说明（右侧）
        T(d, (640, cy), desc, f_desc, SUB, "lm", f"b{i}-desc")

    # 关键提醒条（批次卡最后一行 cy=212+4*64=468 卡底494 → 提醒条524，留30px）
    card(d, [70, 524, 830, 568], fill_alpha=18, outline=GOLD, outline_alpha=140, radius=12)
    T(d, (450, 546), "被前一批录取，后面志愿全部作废——每个批次都别填不想去的学校", ImageFont.truetype(FB, 20), GOLD, "mm", "warn")

    path = os.path.join(out, "P1-1-子任务04-批次顺序卡-900x600.png")
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
