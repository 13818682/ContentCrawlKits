# -*- coding: utf-8 -*-
"""
P1-1 子任务05 · 时间线卡（900×600）
========================================
深圳中考 3月报名 → 8月录取，6个月关键节点
版式：标题 + 左侧时间轴竖线 + 9个节点（时间徽标+事项+关键提醒）+ 底部金句
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

W, H = 900, 700
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
    T(d, (W / 2, 100), "从报名到录取：整整 6 个月", ImageFont.truetype(FB, 38), WHITE, "mm", "title")

    # 时间线节点（9个）：时间徽标 + 事项+提醒 同行
    nodes = [
        ("3月", "中考报名", "D类5项材料提前备齐", False),
        ("4月", "体育中考", "36分现场 · 选考三项", False),
        ("5月", "实验+听说", "理化实验20分 · 英语听说25分", False),
        ("5月下旬", "志愿填报", "全年最重要10天！", True),
        ("6月中旬", "自主招生报名", "一类/二类只能选1所", False),
        ("6月26-28", "文化课考试", "语数英物化史道 · 2.5天", False),
        ("7月16日", "成绩公布", "含单科等级 A+/A/B+...", False),
        ("7-8月", "分批录取", "自招→指标→第1/2/3批", False),
        ("8月", "录取结束", "准备高中入学", False),
    ]
    f_time = ImageFont.truetype(FB, 20)
    f_ev = ImageFont.truetype(FB, 22)
    f_rm = ImageFont.truetype(FR, 18)

    # 9个节点：每卡高44，行距58（卡间隙14），起点 150（标题下方留足）
    ch, row_h = 44, 58
    y0 = 150
    # 时间轴竖线
    d.line([(150, y0 - 10), (150, y0 + 8 * row_h + 10)], fill=EDGE, width=3)
    for i, (tm, ev, rm, hot) in enumerate(nodes):
        cy = y0 + i * row_h
        # 时间轴圆点
        col = GOLD if hot else EDGE
        d.ellipse([142, cy - 8, 158, cy + 8], fill=col)
        # 时间徽标（左）
        col_t = GOLD if hot else LIGHT
        T(d, (98, cy), tm, f_time, col_t, "rm", f"t{i}-time")
        # 事项+提醒 同一行（事项前，提醒紧跟，都用 lm）
        col_e = GOLD if hot else WHITE
        T(d, (180, cy), ev, f_ev, col_e, "lm", f"t{i}-ev")
        ev_w = d.textlength(ev, font=f_ev)
        T(d, (180 + ev_w + 18, cy), rm, f_rm, SUB, "lm", f"t{i}-rm")

    # 底部金句（最后节点卡底=150+8*58+22=636，金句 y=676，底部留白≥20）
    T(d, (W / 2, 676), "志愿填报那 10 天 · 是全年最重要的决策窗口", ImageFont.truetype(FB, 24), GOLD, "mm", "bottom")

    path = os.path.join(out, "P1-1-子任务05-时间线卡-900x700.png")
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
