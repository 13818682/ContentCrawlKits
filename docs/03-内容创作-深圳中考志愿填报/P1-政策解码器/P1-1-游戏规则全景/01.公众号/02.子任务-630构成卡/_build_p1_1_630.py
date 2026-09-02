# -*- coding: utf-8 -*-
"""
P1-1 子任务02 · 630构成卡（900×400）
========================================
深圳中考总分630构成：8科 → 主战场440(五科) + 170(三科)
版式：标题 + 分组总览条 + 8科两列分组明细
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

BBOXES = []  # 校验收集


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
    # ===== 区块纵向坐标（H=620，各区块之间留足间隙）=====
    # 徽章：胶囊 30~56
    f_badge = ImageFont.truetype(FB, 18)
    bt = "深圳中考 · P1系列 · 游戏规则全景"
    bb = d.textbbox((0, 0), bt, font=f_badge); pd = 16
    bx0 = (W - (bb[2] + pd * 2)) / 2; by0 = 30; bx1 = bx0 + bb[2] + pd * 2; by1 = by0 + bb[3] + pd
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=24, outline=GOLD, width=2)
    T(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), bt, f_badge, GOLD, "mm", "badge")
    # 主标题：y=106（徽章底56 → 标题顶~82，留≥26）
    T(d, (W / 2, 106), "深圳中考 630 分，怎么构成的？", ImageFont.truetype(FB, 40), WHITE, "mm", "title")
    # 分组总览条：y 144~244（高100），上下两行 y=170/220
    card(d, [56, 144, 844, 244], fill_alpha=20, outline=EDGE, outline_alpha=120, radius=16)
    f_num = ImageFont.truetype(FB, 30)
    f_grp = ImageFont.truetype(FR, 20)
    T(d, (262, 170), "主战场 440 分 · 占 70%", f_num, GOLD, "mm", "ov-440")
    T(d, (262, 220), "语数英物化 · 五科定胜负", f_grp, LIGHT, "mm", "ov-440-sub")
    T(d, (638, 170), "170 分 · 另三科", f_num, WHITE, "mm", "ov-170")
    T(d, (638, 220), "史道体 · 中等分段定公办民办", f_grp, LIGHT, "mm", "ov-170-sub")
    d.line([(470, 152), (470, 236)], fill=EDGE, width=2)
    # 明细区两列：卡高44，行距58（卡间隙14），首卡 y0=292（分组条底244 → 卡顶270，留26）
    # 每行卡片内单行排布：科目名(lm) + 说明(lm) + 分数(rm)，说明紧跟科目同行
    subjects = [
        ("语文", "120", "单科最高·作文为主"),
        ("数学", "100", "区分度最大"),
        ("英语", "100", "笔试75+听说25"),
        ("物理+化学", "140", "2026实验20"),
        ("历史", "70", "记背为主"),
        ("道德与法治", "50", "2026起开卷"),
        ("体育", "50", "过程14+现场36"),
    ]
    f_sub = ImageFont.truetype(FB, 22)
    f_score = ImageFont.truetype(FB, 26)
    f_note = ImageFont.truetype(FR, 16)
    col_cx = [260, 640]
    cw, ch, row_h = 340, 44, 58
    y0 = 292
    for i, (name, score, note) in enumerate(subjects):
        col = i // 4
        row = i % 4
        x = col_cx[col]
        cy = y0 + row * row_h
        card(d, [x - cw / 2, cy - ch / 2, x + cw / 2, cy + ch / 2],
             fill_alpha=10, outline=EDGE, outline_alpha=70, radius=10)
        T(d, (x - cw / 2 + 24, cy), name, f_sub, WHITE, "lm", f"row{i}-name")
        # 说明紧跟科目名，中间隔 20px
        name_w = d.textlength(name, font=f_sub)
        T(d, (x - cw / 2 + 24 + name_w + 20, cy), note, f_note, SUB, "lm", f"row{i}-note")
        T(d, (x + cw / 2 - 26, cy), score, f_score, GOLD, "rm", f"row{i}-score")
    # 右列第4格：强调卡（五科合计）——第4行 cy = 292+3*58 = 466
    cy4 = y0 + 3 * row_h
    x4 = col_cx[1]
    card(d, [x4 - cw / 2, cy4 - ch / 2, x4 + cw / 2, cy4 + ch / 2],
         fill_alpha=28, outline=GOLD, outline_alpha=150, radius=10)
    f4 = ImageFont.truetype(FB, 26); f4n = ImageFont.truetype(FR, 18)
    T(d, (x4 - cw / 2 + 24, cy4), "五科合计 440", f4, GOLD, "lm", "row7-high")
    T(d, (x4 + cw / 2 - 24, cy4), "占70%", f4n, LIGHT, "rm", "row7-note")
    # 底部一句话：y=566（第4行卡底488 → 金句，底部留白≥20）
    T(d, (W / 2, 566), "每1分都有它的位置 · 每1分都算数", ImageFont.truetype(FB, 24), GOLD, "mm", "bottom")
    path = os.path.join(out, "P1-1-子任务02-630构成卡-900x600.png")
    im.save(path)
    print("OK", path)

    # ---- 校验：越界 + 重叠 ----
    print("=== 越界检测 ===")
    bad = False
    for name, (x0, y0, x1, y1) in BBOXES:
        if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
            print(f"[FAIL] {name}: {x0:.0f},{y0:.0f}->{x1:.0f},{y1:.0f}")
            bad = True
    print("OVERFLOW: PASS" if not bad else "OVERFLOW: FAIL")

    print("=== 重叠检测（区域不相交的块不判）===")
    n_ov = 0
    for i in range(len(BBOXES)):
        for j in range(i + 1, len(BBOXES)):
            n1, r1 = BBOXES[i]; n2, r2 = BBOXES[j]
            # 徽章与标题 y 区间不同，明细行与分组条 y 区间不同——仅当中心距小于两半径和才判
            c1 = ((r1[0] + r1[2]) / 2, (r1[1] + r1[3]) / 2)
            c2 = ((r2[0] + r2[2]) / 2, (r2[1] + r2[3]) / 2)
            ox = min(r1[2], r2[2]) - max(r1[0], r2[0])
            oy = min(r1[3], r2[3]) - max(r1[1], r2[1])
            if ox > 4 and oy > 4:
                print(f"[重叠?] {n1} <-> {n2} ox={ox:.0f} oy={oy:.0f}")
                n_ov += 1
    print("OVERLAP: PASS" if n_ov == 0 else f"OVERLAP: {n_ov} 对重叠")


if __name__ == "__main__":
    main()
