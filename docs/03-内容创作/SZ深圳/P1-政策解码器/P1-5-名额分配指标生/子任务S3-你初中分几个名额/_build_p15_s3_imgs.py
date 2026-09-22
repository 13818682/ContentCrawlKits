# -*- coding: utf-8 -*-
"""
P1-5 · S3《你初中分几个名额》（并入 S4 收口）· 配图生成器
================================================================================
本批产出 15 张（头条长文 3 封面 + 2 正文图属**存稿**，待通道恢复再补）：
  01.公众号/  封面-精炼版 900x383 ／ 章节条1-3 900x220 ／ 数据卡1-3 900x400 ／ 长图 900xH
  04.小红书/  封面 ／ 正文图1-4 ／ 尾卡-关注与合集      （均 1080x1440）
  02.今日头条/ 微头条配图 1200x900

视觉档：**P1-5-S3 档 = 蓝系家族（中钢蓝档）**
  主色永远深蓝系不换色相；与同系列各档靠 深浅 × 光影 × 光线角度 × 装饰 × 版式 区分：
    主线 = 深靛蓝 (22,56,110) 中上方主光 · 同心分配环
    S1   = 深蓝   (14,44,92)  中上方主光 · 标尺刻度
    S2   = 中深蓝 (18,52,104) 左上主光   · 勾选框列
    S3   = 中钢蓝 (22,50,100) **右下主光** · **分布点阵**（"名额分配到校"的意象）
  结构规划 §107 原建议即为「分布点阵装饰」，本脚本据此落地。

口径：见同目录 00-S3-官方口径与名额分配数据核验记录.md
  ⚠️ 铁律：凡出现「163 所」处必须同框给出 Q8「区共享名额」的出路，不得只讲绝望。
"""
import os, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PFX = "P1-5-S3-你初中分几个名额"
FD = "C:/Windows/Fonts/"
FB, FR = FD + "msyhbd.ttc", FD + "msyh.ttc"

TOP, BOT = (22, 50, 100), (7, 18, 40)
CARD, EDGE = (13, 34, 72), (96, 148, 216)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
SRC = "数据来源：2026年深圳市高中阶段学校考生报考指导手册（附件2/3）"

CHECKS = []


def font(s, bold=True):
    return ImageFont.truetype(FB if bold else FR, s)


def save_img(im, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for _ in range(6):
        try:
            im.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)


def base(w, h):
    """中钢蓝竖直渐变 + **右下主光**（区别于主线/S1/S2）+ **分布点阵**装饰。"""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    arr = np.repeat(np.array(TOP, np.float32)[None, None, :] * (1 - t)
                    + np.array(BOT, np.float32)[None, None, :] * t, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    gx, gy = w * 0.84, h * 0.88          # 右下主光（新角度）
    dd = np.sqrt(((xx - gx) / (w * 0.62)) ** 2 + ((yy - gy) / (h * 0.42)) ** 2)
    arr = arr + np.array((255, 255, 255), np.float32)[None, None, :] * (np.exp(-dd * dd) * 0.24)[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    # 分布点阵：均匀网格上亮度不等的点，模拟「名额被分配到不同学校」的疏密
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    step = max(46, int(min(w, h) * 0.072))
    r0 = max(2, int(min(w, h) * 0.0035))
    n = 0
    for gyy in range(int(h * 0.10), h, step):
        for gxx in range(int(w * 0.06), w, step):
            k = (gxx // step + gyy // step) % 5
            a = 46 if k == 0 else (26 if k == 1 else 13)
            r = r0 + (2 if k == 0 else 0)
            od.ellipse([gxx - r, gyy - r, gxx + r, gyy + r],
                       fill=(GOLD + (a,)) if k == 0 else (255, 255, 255, a))
            n += 1
    im.paste(ov, (0, 0), ov)
    return im


def rcard(im, box, fa=0, outline=None, oa=255, radius=22, width=2):
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if fa:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fa))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (oa,), width=width)
    im.paste(ov, (0, 0), ov)


def put(d, text, xy, size, fill, bold=True, anchor="mm", maxw=None, W=900, H=400, tag=""):
    f = font(size, bold)
    if maxw:
        while f.size > 11:
            bb = d.textbbox((0, 0), text, font=f)
            if bb[2] - bb[0] <= maxw + 1:
                break
            f = font(f.size - 1, bold)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox((0, 0), text, font=f)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    cx, cy = xy
    if anchor == "mm":
        x0, y0 = cx - bw / 2, cy - bh / 2
    elif anchor == "la":
        x0, y0 = cx, cy
    elif anchor == "lm":
        x0, y0 = cx, cy - bh / 2
    elif anchor == "rm":
        x0, y0 = cx - bw, cy - bh / 2
    elif anchor == "ra":
        x0, y0 = cx - bw, cy
    else:
        x0, y0 = cx, cy - bh / 2
    CHECKS.append((tag or text[:12], (x0, y0, x0 + bw, y0 + bh), W, H))
    return f


def gate(name, W, H, side=20, bottom=16):
    bad = [(t, tuple(round(v) for v in b)) for t, b, w, h in CHECKS
           if b[0] < side - 12 or b[2] > w - side + 12 or b[1] < 8 or b[3] > h - bottom + 8]
    print(("OK   " if not bad else "!!   ") + name, bad if bad else "")
    CHECKS.clear()


# ==================== 公众号 ====================
def gzh_cover():
    W, H = 900, 383
    im = base(W, H); d = ImageDraw.Draw(im)
    put(d, "深圳中考", (60, 44), 26, SUB, bold=False, anchor="la", maxw=780, W=W, H=H, tag="k")
    # 定性前缀：钉死范围（名额分配 / AC 类），避免被读成普遍规则
    put(d, "名额分配（指标生）：", (60, 118), 46, GOLD, anchor="la", maxw=800, W=W, H=H, tag="t0")
    put(d, "你孩子初中分到几个？", (60, 204), 56, WHITE, anchor="la", maxw=800, W=W, H=H, tag="t1")
    put(d, "488 所里 163 所是 0 个 · 但还有一条路", (60, 308), 30, GOLD, bold=False,
        anchor="la", maxw=810, W=W, H=H, tag="t2")
    gate("公众号封面-精炼版", W, H)
    save_img(im, f"{HERE}/01.公众号/{PFX}-公众号-封面-精炼版-900x383.png")


def gzh_section(idx, num, title, sub, name):
    W, H = 900, 220
    im = base(W, H); d = ImageDraw.Draw(im)
    cx, cy = 96, H / 2
    d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=GOLD)
    put(d, num, (cx, cy), 40, (18, 30, 55), W=W, H=H, tag="num")
    put(d, title, (158, cy - 26), 42, WHITE, anchor="lm", maxw=680, W=W, H=H, tag="title")
    put(d, sub, (158, cy + 30), 23, LIGHT, bold=False, anchor="lm", maxw=700, W=W, H=H, tag="sub")
    gate(f"公众号章节条{idx}-{name}", W, H)
    save_img(im, f"{HERE}/01.公众号/{PFX}-公众号-章节条{idx}-{name}-900x220.png")


def gzh_card1():
    """名额怎么分：比例原则 + 实测盘子。"""
    W, H = 900, 400
    im = base(W, H); d = ImageDraw.Draw(im)
    put(d, "名额怎么分到学校？按报名人数比例", (450, 42), 32, WHITE, maxw=780, W=W, H=H, tag="t")
    rcard(im, [60, 84, 840, 146], fa=16, outline=GOLD, radius=16)
    put(d, "各初中该类别报名人数 ÷ 全市该类别报名人数", (450, 115), 26, GOLD,
        maxw=760, W=W, H=H, tag="f")
    put(d, "→ 学校越大、同类别考生越多，名额越多", (450, 178), 24, LIGHT, bold=False,
        maxw=780, W=W, H=H, tag="f2")
    subs = [("32,710", "AC类名额总数"), ("488", "参与初中"), ("45", "每校中位数")]
    cx = [200, 450, 700]; cw = 226; cy, ch = 214, 140
    for (num, lab), xc in zip(subs, cx):
        rcard(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fa=16,
              outline=(255, 255, 255), oa=70, radius=18)
        put(d, num, (xc, cy + 52), 46, GOLD, W=W, H=H, tag="n")
        put(d, lab, (xc, cy + 104), 22, SUB, bold=False, W=W, H=H, tag="l")
    put(d, "2026 年 AC 类 · 最多的一所 888 个", (450, 382), 20, LIGHT, bold=False,
        W=W, H=H, tag="n2")
    gate("公众号数据卡1", W, H)
    save_img(im, f"{HERE}/01.公众号/{PFX}-公众号-数据卡1-名额怎么分-900x400.png")


def gzh_card2():
    """⭐ 163 所 0 个 → 区共享名额（必须同框）。"""
    W, H = 900, 400
    im = base(W, H); d = ImageDraw.Draw(im)
    put(d, "163 所初中，AC 类名额是 0 个", (450, 40), 32, WHITE, maxw=780, W=W, H=H, tag="t")
    put(d, "占 488 所的 33.4%", (450, 76), 22, LIGHT, bold=False, W=W, H=H, tag="sub")
    rcard(im, [60, 104, 840, 196], fa=18, outline=GOLD, radius=18, width=3)
    put(d, "但 0 个 ≠ 没机会", (450, 133), 32, GOLD, W=W, H=H, tag="a")
    put(d, "手册第 8 问：以区为单位整体重算 → 可报「区共享名额」", (450, 172), 23,
        WHITE, bold=False, maxw=770, W=W, H=H, tag="b")
    put(d, "范围变化：本校 → 全区这一组学校", (450, 226), 24, LIGHT, bold=False,
        maxw=780, W=W, H=H, tag="c")
    rows = [("龙华区新华中学教育集团", "11 个"), ("深圳中学初中部", "10 个"),
            ("拿到 0 个深中名额的初中", "163 所")]
    ry = 262
    for i, (a, b) in enumerate(rows):
        rcard(im, [60, ry, 840, ry + 40], fa=12 if i % 2 == 0 else 0, radius=10)
        put(d, a, (80, ry + 20), 22, WHITE, anchor="lm", maxw=520, W=W, H=H, tag="r1")
        put(d, b, (820, ry + 20), 24, GOLD if i == 2 else LIGHT, anchor="rm",
            maxw=280, W=W, H=H, tag="r2")
        ry += 42
    gate("公众号数据卡2", W, H)
    save_img(im, f"{HERE}/01.公众号/{PFX}-公众号-数据卡2-区共享名额-900x400.png")


def gzh_card3():
    """收口：两条回收规则（必须分开写）。"""
    W, H = 900, 400
    im = base(W, H); d = ImageDraw.Draw(im)
    put(d, "名额没用完，分两种，后果不同", (450, 40), 32, WHITE, maxw=780, W=W, H=H, tag="t")
    rows = [("各初中学校未完成", "自动失效", "名额作废，不给别人也不给本校"),
            ("各公办普高未完成", "转普通生计划", "自动回到第一批次录取")]
    ry = 88
    for tag, res, note in rows:
        rcard(im, [60, ry, 840, ry + 118], fa=16,
              outline=GOLD if "转" in res else (255, 255, 255), oa=90, radius=18)
        put(d, tag, (84, ry + 34), 26, WHITE, anchor="lm", maxw=420, W=W, H=H, tag="r1")
        put(d, res, (84, ry + 80), 30, GOLD, anchor="lm", maxw=420, W=W, H=H, tag="r2")
        put(d, note, (826, ry + 58), 21, SUB, bold=False, anchor="rm", maxw=340, W=W, H=H, tag="r3")
        ry += 130
    rcard(im, [60, 352, 840, 392], fa=16, outline=(255, 255, 255), oa=70, radius=14)
    put(d, "另：名额分配志愿只填 1 所，且与第一批次相互独立", (450, 372), 21, LIGHT,
        bold=False, maxw=770, W=W, H=H, tag="n")
    gate("公众号数据卡3", W, H)
    save_img(im, f"{HERE}/01.公众号/{PFX}-公众号-数据卡3-两条回收规则-900x400.png")


LH = 3260


def gzh_longimage():
    W, H = 900, LH
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    arr = np.repeat(np.array((26, 58, 112), np.float32)[None, None, :] * (1 - t)
                    + np.array(BOT, np.float32)[None, None, :] * t, W, axis=1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dd = np.sqrt(((xx - W * 0.5) / (W * 0.46)) ** 2 + ((yy - H * 0.045) / (H * 0.09)) ** 2)
    arr = arr + np.array((160, 205, 245), np.float32)[None, None, :] * (np.exp(-dd * dd) * 0.20)[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(im)

    def P(text, size, xy, color=WHITE, bold=True, anchor="mm", maxw=None, tag=""):
        return put(d, text, xy, size, color, bold=bold, anchor=anchor, maxw=maxw,
                   W=W, H=H, tag=tag)

    def box(x, y, w, h, r=16, fa=0, outline=EDGE, oa=255):
        rcard(im, [x, y, x + w, y + h], fa=fa, outline=outline, oa=oa,
              radius=r, width=2)

    def pill(cx, cy, text, size, color):
        f = font(size, True)
        bb = d.textbbox((0, 0), text, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.rounded_rectangle([cx - tw / 2 - 28, cy - th / 2 - 13,
                             cx + tw / 2 + 28, cy + th / 2 + 13], radius=40, outline=color, width=2)
        P(text, size, (cx, cy), color, tag="pill")

    def chapter(y, text):
        d.rectangle([50, y - 26, 58, y + 26], fill=GOLD)
        P(text, 34, (78, y), WHITE, anchor="lm", tag="ch")
        d.line([50, y + 44, 145, y + 44], fill=GOLD, width=3)

    # 钩子区
    pill(W / 2, 54, "深圳中考 · 名额分配（指标生）", 21, GOLD)
    P("你孩子初中", 62, (W / 2, 150), WHITE, maxw=800, tag="h1")
    P("分到几个名额？", 62, (W / 2, 228), WHITE, maxw=800, tag="h2")
    P("163 所是 0 个", 84, (W / 2 + 3, 372), (0, 16, 36), maxw=820, tag="h3s")
    P("163 所是 0 个", 84, (W / 2, 368), GOLD, maxw=820, tag="h3")
    box(70, 448, 760, 132, r=18, fa=16, outline=GOLD)
    P("488", 54, (185, 496), GOLD, tag="v1")
    P("所初中", 22, (185, 544), LIGHT, bold=False, tag="v1l")
    P("163", 54, (450, 496), WHITE, tag="v2")
    P("所是 0 个", 22, (450, 544), LIGHT, bold=False, tag="v2l")
    P("33.4%", 54, (715, 496), GOLD, tag="v3")
    P("占比", 22, (715, 544), LIGHT, bold=False, tag="v3l")
    pill(W / 2, 634, "但还有一条路 · 往下看第 3 节", 23, GOLD)
    d.line([60, 682, 250, 682], fill=GOLD, width=3)

    # 01
    chapter(742, "01 · 名额怎么分到学校？")
    P("分配原则（手册原文）：各初中学校相应考生类别报名中考的考生数，", 20,
      (W / 2, 812), LIGHT, bold=False, maxw=780, tag="p1")
    P("占全市该类别报名中考的考生数的比例。", 20, (W / 2, 844), LIGHT, bold=False,
      maxw=780, tag="p2")
    P("→ 学校越大、同类别考生越多，名额越多", 24, (W / 2, 898), GOLD, maxw=800, tag="p3")
    stats = [("32,710", "AC类名额总数", GOLD), ("488", "参与初中", WHITE),
             ("45", "每校中位数", WHITE)]
    cx = [215, 450, 685]; cw, cy, ch = 240, 936, 128
    for (n, l, col), xc in zip(stats, cx):
        box(xc - cw / 2, cy, cw, ch, r=16, fa=14)
        P(n, 40, (xc, cy + 46), col, tag="sn")
        P(l, 20, (xc, cy + 94), SUB, bold=False, tag="sl")
    P("最多的一所 888 个（相差约 19 倍）", 22, (W / 2, 1104), LIGHT, bold=False, maxw=800, tag="s4")

    # 02
    chapter(1170, "02 · 163 所初中是 0 个")
    rows = [("龙华区新华中学教育集团", "深中名额 11 个"), ("深圳中学初中部", "10 个"),
            ("拿到 0 个深中名额的初中", "163 所")]
    ry = 1226
    for i, (a, b) in enumerate(rows):
        box(60, ry, W - 120, 56, r=12, fa=14)
        P(a, 22, (84, ry + 28), WHITE, anchor="lm", maxw=520, tag="r1")
        P(b, 22, (816, ry + 28), GOLD if i == 2 else LIGHT, anchor="rm", maxw=280, tag="r2")
        ry += 62
    P("拿到 10 个以上的，全深圳只有 2 所", 21, (W / 2, ry + 20), LIGHT, bold=False,
      maxw=800, tag="r3")

    # 03 —— ⭐ 必须与"163"同框
    chapter(1530, "03 · 拿到 0 个，还有这条路")
    box(60, 1590, W - 120, 100, r=18, fa=18, outline=GOLD)
    P("0 个 ≠ 没机会", 34, (W / 2, 1622), GOLD, tag="a1")
    P("手册第 8 问原文见下", 20, (W / 2, 1664), LIGHT, bold=False, tag="a2")
    box(60, 1706, W - 120, 128, r=16, fa=12)
    P("「对于按公式计算后分得名额为 0 的初中学校，", 20, (W / 2, 1746), WHITE,
      bold=False, maxw=760, tag="q1")
    P("以区为单位作为一个整体，重新按公式进行计算，", 20, (W / 2, 1780), WHITE,
      bold=False, maxw=760, tag="q2")
    P("这些学校的考生具备报考区共享名额的机会。」", 20, (W / 2, 1814), WHITE,
      bold=False, maxw=760, tag="q3")
    P("范围变化：本校 → 全区这一组学校", 24, (W / 2, 1868), GOLD, maxw=800, tag="a3")

    # 04
    chapter(1930, "04 · 怎么查你孩子学校？")
    ry = 1986
    for a, b in [("名额分到各初中的具体数量", "手册附件 3"),
                 ("各高中的计划数与录取控制线", "手册附件 2")]:
        box(60, ry, W - 120, 60, r=12, fa=14)
        P(a, 22, (84, ry + 30), WHITE, anchor="lm", maxw=520, tag="e1")
        P(b, 22, (816, ry + 30), GOLD, anchor="rm", maxw=300, tag="e2")
        ry += 66
    P("控制线 = 前三年同类别线（630制）均值降 20 分", 21, (W / 2, ry + 18), LIGHT,
      bold=False, maxw=800, tag="e3")
    P("⚠ 控制线与当年第一批线无关，不能作第一批志愿参考", 20, (W / 2, ry + 52), GOLD,
      bold=False, maxw=800, tag="e4")

    # 05 收口
    chapter(2266, "05 · 收口：两个最容易搞混的机制")
    box(60, 2326, W - 120, 96, r=16, fa=16, outline=GOLD)
    P("名额分配志愿只填 1 所", 26, (W / 2, 2356), WHITE, tag="c1")
    P("且与第一批次相互独立 —— 想读该校普通生，第一批再填一次", 20, (W / 2, 2396),
      GOLD, bold=False, maxw=770, tag="c2")
    ry = 2442
    for tag, res, note in [("各初中学校未完成", "自动失效", "名额作废"),
                           ("各公办普高未完成", "转普通生计划", "回到第一批次")]:
        box(60, ry, W - 120, 78, r=14, fa=14)
        P(tag, 22, (84, ry + 28), WHITE, anchor="lm", maxw=400, tag="d1")
        P(res, 24, (84, ry + 58), GOLD, anchor="lm", maxw=400, tag="d2")
        P(note, 20, (816, ry + 40), SUB, bold=False, anchor="rm", tag="d3")
        ry += 86

    # 06 行动
    chapter(ry + 46, "06 · 现在做这 3 件事")
    ry2 = ry + 106
    for n, t2 in [("①", "去附件 3 查你孩子学校的名额数"),
                  ("②", "如果是 0 个，找区共享名额，别放弃"),
                  ("③", "想读某校，第一批次记得再填一次")]:
        box(60, ry2, W - 120, 66, r=14, fa=14)
        P(n, 22, (96, ry2 + 33), GOLD, tag="f1")
        P(t2, 22, (140, ry2 + 33), WHITE, bold=False, anchor="lm", maxw=700, tag="f2")
        ry2 += 76

    divy = ry2 + 34
    d.line([50, divy, W - 50, divy], fill=EDGE, width=2)
    P("关注我 · 深圳中考政策解码系列", 30, (W / 2, divy + 44), GOLD, tag="cta")
    P("名额分配讲完了，下一期讲怎么把它填对", 20, (W / 2, divy + 90), LIGHT,
      bold=False, tag="cta2")
    P(SRC, 18, (W / 2, divy + 132), SUB, bold=False, maxw=W - 80, tag="src")
    P("本文为政策信息整理，以深圳市教育局、市招考办正式公告及报考指导手册为准", 17,
      (W / 2, divy + 166), LIGHT, bold=False, maxw=W - 80, tag="dis")
    assert divy + 166 < H - 16, (divy, H)
    gate("公众号长图-极简版", W, H, side=18, bottom=10)
    save_img(im, f"{HERE}/01.公众号/{PFX}-公众号-长图-极简版-900x{H}.png")


# ==================== 小红书 ====================
WX, HX, HM = 1080, 1440, 80


def xhs_cover():
    im = base(WX, HX); d = ImageDraw.Draw(im)
    put(d, "深圳中考", (WX / 2, 176), 96, GOLD, maxw=1000, W=WX, H=HX, tag="brand")
    put(d, "名额分配（指标生）", (WX / 2, 452), 56, LIGHT, bold=False, maxw=1000, W=WX, H=HX, tag="k")
    put(d, "你孩子初中", (WX / 2, 574), 92, WHITE, maxw=1000, W=WX, H=HX, tag="t1")
    put(d, "分到几个名额？", (WX / 2, 676), 92, WHITE, maxw=1000, W=WX, H=HX, tag="t2")
    d.line([WX / 2 - 300, 772, WX / 2 + 300, 772], fill=GOLD, width=8)
    put(d, "488 所里 163 所是 0 个", (WX / 2, 892), 52, GOLD, maxw=980, W=WX, H=HX, tag="kick")
    put(d, "但 0 个 ≠ 没机会", (WX / 2, 976), 46, WHITE, maxw=980, W=WX, H=HX, tag="kick2")
    put(d, "第 3 张图有手册原文", (WX / 2, 1148), 34, SUB, bold=False, maxw=980, W=WX, H=HX, tag="note")
    put(d, "深圳中考 · 政策解码 · 关注不迷路", (WX / 2, 1366), 28, SUB, bold=False,
        maxw=1000, W=WX, H=HX, tag="foot")
    gate("小红书 封面", WX, HX)
    save_img(im, f"{HERE}/04.小红书/{PFX}-小红书-封面-1080x1440.png")


def xhs_card(fn, kick, title, sub, rows, concl, tiles=None, gap=20, minh=104, rowfont=38,
             rowgold=None, tilesize=56):
    im = base(WX, HX); d = ImageDraw.Draw(im)
    put(d, kick, (WX / 2, 84), 34, GOLD, maxw=980, W=WX, H=HX, tag="kick")
    put(d, title, (WX / 2, 202), 56, WHITE, maxw=1000, W=WX, H=HX, tag="title")
    if sub:
        put(d, sub, (WX / 2, 286), 29, LIGHT, bold=False, maxw=1000, W=WX, H=HX, tag="sub")
    MT, MB = 322, 1086
    th = 244 if tiles else 0
    n = len(rows)
    room = (MB - MT) - th - (24 if tiles else 0)
    rh = max(minh, min((room - (n - 1) * gap) / n, 340)) if n else minh
    y = MT
    if tiles:
        tw, g = 280, 24
        x0 = (WX - (tw * 3 + g * 2)) / 2
        for i, (num, lab) in enumerate(tiles[:3]):
            x = x0 + i * (tw + g)
            rcard(im, [x, y, x + tw, y + th], fa=16, outline=(255, 255, 255), oa=70, radius=20)
            put(d, num, (x + tw / 2, y + th * 0.30), tilesize, GOLD, maxw=tw - 24,
                W=WX, H=HX, tag="tn")
            put(d, lab, (x + tw / 2, y + th * 0.72), 23, SUB, bold=False, maxw=tw - 22,
                W=WX, H=HX, tag="tl")
        y += th + 24
    for i, rt in enumerate(rows):
        y1 = y + rh
        rcard(im, [HM, y, WX - HM, y1], fa=16, outline=(255, 255, 255), oa=64, radius=22, width=3)
        put(d, rt, (WX / 2, (y + y1) / 2), rowfont,
            GOLD if (rowgold and i in rowgold) else WHITE, maxw=880, W=WX, H=HX, tag="row")
        y = y1 + (gap if i < n - 1 else 0)
    rcard(im, [HM - 6, 1152, WX - HM + 6, 1270], fa=16, outline=GOLD, radius=26, width=4)
    put(d, concl, (WX / 2, 1211), 38, GOLD, maxw=920, W=WX, H=HX, tag="band")
    put(d, SRC, (WX / 2, 1348), 21, SUB, bold=False, maxw=1000, W=WX, H=HX, tag="foot")
    gate("小红书 " + fn[-28:], WX, HX, side=18, bottom=10)
    save_img(im, f"{HERE}/04.小红书/{fn}")


def xhs_tail():
    im = base(WX, HX); d = ImageDraw.Draw(im)
    put(d, "深圳中考", (WX / 2, 176), 96, GOLD, maxw=1000, W=WX, H=HX, tag="brand")
    put(d, "名额分配 ·", (WX / 2, 470), 72, WHITE, maxw=1000, W=WX, H=HX, tag="t1")
    put(d, "讲完了，怎么填？", (WX / 2, 566), 72, WHITE, maxw=1000, W=WX, H=HX, tag="t2")
    d.line([WX / 2 - 250, 656, WX / 2 + 250, 656], fill=GOLD, width=8)
    rcard(im, [HM, 724, WX - HM, 1012], fa=16, outline=GOLD, radius=26, width=4)
    put(d, "填之前记住这两条", (WX / 2, 788), 42, GOLD, maxw=880, W=WX, H=HX, tag="b1")
    put(d, "① 只能填 1 所公办普高", (WX / 2, 866), 36, WHITE, maxw=880, W=WX, H=HX, tag="b2")
    put(d, "② 与第一批次独立，普通生要再填一次", (WX / 2, 930), 34, WHITE, maxw=880,
        W=WX, H=HX, tag="b3")
    put(d, "（完整拆解见主页合集「志愿规则」）", (WX / 2, 1160), 34, SUB, bold=False,
        maxw=920, W=WX, H=HX, tag="n1")
    put(d, "关注我，下一条讲：名额分配志愿怎么填不浪费", (WX / 2, 1244), 34, GOLD,
        maxw=960, W=WX, H=HX, tag="cta")
    put(d, "深圳中考 · 政策解码", (WX / 2, 1366), 28, SUB, bold=False, maxw=1000,
        W=WX, H=HX, tag="foot")
    gate("小红书 尾卡", WX, HX)
    save_img(im, f"{HERE}/04.小红书/{PFX}-小红书-尾卡-关注与合集-1080x1440.png")


# ==================== 头条微头条配图 ====================
def tt_wt():
    W, H = 1200, 900
    im = base(W, H); d = ImageDraw.Draw(im)
    f = font(30)
    badge = "深圳中考 · 政策解码 S3"
    tw = d.textlength(badge, font=f)
    d.rounded_rectangle([70, 56, 80 + tw + 18, 100], radius=12, fill=(8, 22, 50),
                        outline=(130, 175, 235), width=3)
    put(d, badge, (80, 60), 30, (210, 232, 255), anchor="la", W=W, H=H, tag="badge")
    put(d, "你孩子初中分到几个名额？", (W / 2, 186), 52, WHITE, maxw=1040, W=W, H=H, tag="t")
    cards = [("32,710", "AC类名额总数", GOLD), ("163", "所初中是 0 个", GOLD),
             ("45", "每校中位数", WHITE)]
    cx = [230, 600, 970]; cw, cy, ch = 340, 268, 372
    for (num, lab, col), xc in zip(cards, cx):
        rcard(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fa=18,
              outline=(255, 255, 255), oa=80, radius=26)
        put(d, num, (xc + 3, cy + 126), 66, (0, 18, 40), W=W, H=H, tag="sh")
        put(d, num, (xc, cy + 122), 66, col, W=W, H=H, tag="n")
        d.line([xc - 66, cy + 236, xc + 66, cy + 236], fill=(255, 255, 255), width=2)
        put(d, lab, (xc, cy + 288), 28, (240, 246, 252), bold=False, maxw=cw - 26,
            W=W, H=H, tag="l")
    put(d, "0 个 ≠ 没机会 · 手册第 8 问：可报区共享名额", (W / 2, 760), 32, GOLD,
        maxw=1060, W=W, H=H, tag="c")
    put(d, SRC, (W / 2, 858), 21, (188, 200, 214), bold=False, maxw=1100, W=W, H=H, tag="foot")
    gate("头条 微头条配图", W, H)
    save_img(im, f"{HERE}/02.今日头条/{PFX}-头条-微头条配图-1200x900.png")


if __name__ == "__main__":
    gzh_cover()
    gzh_section(1, "一", "名额怎么分", "按报名人数比例 · 大校多小校少", "怎么分")
    gzh_section(2, "二", "0 个的出路", "163 所 → 区共享名额", "零名的出路")
    gzh_section(3, "三", "收口", "批次独立 + 两条回收规则", "收口")
    gzh_card1(); gzh_card2(); gzh_card3()
    gzh_longimage()
    xhs_cover()
    xhs_card(f"{PFX}-小红书-正文图1-名额怎么分-1080x1440.png", "S3 · 怎么分",
             "名额按比例分，不是平均分",
             "各初中该类别报名人数 ÷ 全市该类别报名人数",
             ["学校越大、同类别考生越多，名额越多",
              "AC 类名额总数 32,710 个",
              "分到 488 所初中，每校中位 45 个",
              "最多的一所 888 个"],
             "中位 45 与 888 差约 19 倍",
             gap=18, minh=110, rowfont=36, rowgold={0})
    xhs_card(f"{PFX}-小红书-正文图2-163所是0个-1080x1440.png", "S3 · 反差点",
             "488 所里，163 所是 0 个",
             "占 33.4% · 数据口径：2026 年 AC 类",
             ["163 所初中 AC 类名额 = 0",
              "深中一列：最多 11 个（龙华新华）",
              "拿到 10 个以上的，全深圳只有 2 所",
              "拿到 0 个深中名额的：163 所"],
             "先记住这个数，再看下一条",
             gap=18, minh=110, rowfont=36, rowgold={0})
    xhs_card(f"{PFX}-小红书-正文图3-区共享名额-1080x1440.png", "S3 · 出路",
             "0 个 ≠ 没机会",
             "手册第 8 问原文",
             ["「分得名额为 0 的初中学校，",
              "以区为单位作为一个整体，",
              "重新按公式进行计算，",
              "这些学校的考生具备报考区共享名额的机会。」"],
             "范围变化：本校 → 全区这一组学校",
             gap=16, minh=104, rowfont=36)
    xhs_card(f"{PFX}-小红书-正文图4-填之前记住两件事-1080x1440.png", "S3 · 收口",
             "填之前记住这两件事",
             "名额分配的收口机制",
             ["① 名额分配志愿只能填 1 所公办普高",
              "② 它与第一批次相互独立",
              "→ 想读该校普通生，第一批再填一次",
              "③ 初中校未完成 = 失效；高中校未完成 = 转普通生计划"],
             "两个批次各填一次，才叫双保险",
             tiles=[("488", "所初中"), ("163", "所是 0 个"), ("1", "所志愿上限")],
             gap=18, minh=104, rowfont=34)
    xhs_tail()
    tt_wt()
    print("ALL DONE (S3)")
