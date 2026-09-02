# -*- coding: utf-8 -*-
"""
P1-1 子任务06 · 排队比喻卡（900×600）
========================================
16个志愿 "分数优先、依照志愿顺序" —— 排队录取比喻
版式：标题 + 比喻核心句 + 排队示意图（分数排队→纸条按序→按号安排）+ 操作要点 + 底部金句
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
    T(d, (W / 2, 100), "16个志愿怎么录？分高先挑，按你排的顺序", ImageFont.truetype(FB, 34), WHITE, "mm", "title")

    # 比喻核心句（金色条，缩短、下移，与标题拉开）
    card(d, [180, 148, 720, 188], fill_alpha=16, outline=GOLD, outline_alpha=130, radius=12)
    T(d, (450, 168), "分数优先 · 依照志愿顺序 = 排队录取", ImageFont.truetype(FB, 26), GOLD, "mm", "metaphor")

    # 三步示意（横排 3 卡）
    steps = [
        ("第一步", "分高排前", "全市按分数从高到低排队，轮到谁处理谁"),
        ("第二步", "纸条按序", "按你写的志愿顺序，逐个检索有名额的学校"),
        ("第三步", "按号安排", "第一个有名额的学校录取，不能跳号去后面窗口"),
    ]
    f_sno = ImageFont.truetype(FB, 20)
    f_stitle = ImageFont.truetype(FB, 26)
    f_sdesc = ImageFont.truetype(FR, 17)
    scw, sch, sgap = 252, 150, 24
    sy = 214
    sx0s = [60, 324, 588]
    for i, (sno, stitle, sdesc) in enumerate(steps):
        sx = sx0s[i] + scw / 2
        card(d, [sx - scw / 2, sy, sx + scw / 2, sy + sch], fill_alpha=14, outline=EDGE, outline_alpha=90, radius=14)
        T(d, (sx, sy + 30), sno, f_sno, SUB, "mm", f"s{i}-no")
        T(d, (sx, sy + 62), stitle, f_stitle, GOLD, "mm", f"s{i}-title")
        d.line([(sx - 70, sy + 84), (sx + 70, sy + 84)], fill=(255, 255, 255, 90), width=1)
        # 说明自动换行（两行，居中）
        f_l = ImageFont.truetype(FR, 16)
        # 按字数均分两行（每行约10字）
        mid = len(sdesc) // 2
        # 找最近的自然断点（空格/逗号/句号）
        cut = mid
        for probe in range(mid, -1, -1):
            if sdesc[probe] in " ，。、；":
                cut = probe + 1
                break
        if cut <= 2 or cut >= len(sdesc) - 2:
            cut = mid
        T(d, (sx, sy + 108), sdesc[:cut], f_l, SUB, "mm", f"s{i}-d1")
        T(d, (sx, sy + 132), sdesc[cut:], f_l, SUB, "mm", f"s{i}-d2")

    # 操作要点（黄色条，三步卡底364 → 顶部404，间隙40）
    card(d, [80, 404, 820, 452], fill_alpha=18, outline=GOLD, outline_alpha=150, radius=12)
    T(d, (450, 428), "把最想去的学校放前面，按喜欢程度从高到低排", ImageFont.truetype(FB, 24), GOLD, "mm", "do")

    # 同分提醒（操作要点底452 → y=500，间隙48）
    T(d, (450, 500), "同分怎么办：先比生物地理合卷分，再比语数英三科总分", ImageFont.truetype(FR, 20), LIGHT, "mm", "tie")

    # 底部金句（同分500 → 金句552，间隙52；底部留白600-552-13=35）
    T(d, (W / 2, 552), "分高先挑 · 顺序自己定——志愿排序就是你的主动权", ImageFont.truetype(FB, 24), GOLD, "mm", "bottom")

    path = os.path.join(out, "P1-1-子任务06-排队比喻卡-900x600.png")
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
