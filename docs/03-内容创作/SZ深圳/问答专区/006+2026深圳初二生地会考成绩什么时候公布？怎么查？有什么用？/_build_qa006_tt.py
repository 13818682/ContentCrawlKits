# -*- coding: utf-8 -*-
"""
QA-006《2026深圳初二生地会考成绩即将公布：怎么查？这100分有什么用？》· 今日头条配图
================================================================================
产出 7 张，全部写入本目录下的 02.今日头条/ （均 1200×900）：
  封面1-主标题     封面2-数据对撞     封面3-答案大字      （三张不同构图，不重复）
  正文图1-历年查分时间    正文图2-怎么查    正文图3-四个作用
  微头条配图-关键数字

视觉档：**QA-006 档 = 蓝系家族（深钢蓝档）**
  主色永远深蓝系不换色相；与既有多档靠 深浅 × 光影 × 光线角度 × 装饰 × 版式 区分：
    QA-006 = 深钢蓝 (20,46,96) · 右上主光 · 斜向刻度带（时间/分数刻度意象）
  （主线 深靛蓝中上方光/同心环、S1 深蓝中上方光/标尺、S2 中深蓝左上光/勾选框列）

口径：见 ../00-QA-006-官方口径与历年查分时间核验.md —— **2026 具体公布日期官方未发布，图文一律不写死日期。**
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "02.今日头条")
PFX = "QA-006-生地会考成绩"
W, H = 1200, 900
X0, CAPW = 80, 1040

FD = "C:/Windows/Fonts/"
FB = FD + "msyhbd.ttc"
FR = FD + "msyh.ttc"

# ---------------- QA-006 视觉档 ----------------
TOP, BOT = (20, 46, 96), (6, 16, 36)
CARD, EDGE = (12, 32, 68), (92, 140, 208)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
BADGE = "深圳中考 · 问答系列 006"
SRC = "数据来源：深圳市教育局 / 深圳市招生考试办公室 官方公开信息"

CHECKS = []


def font(s, bold=True):
    return ImageFont.truetype(FB if bold else FR, s)


def base(w=W, h=H):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    c1 = np.array(TOP, np.float32)[None, None, :]
    c2 = np.array(BOT, np.float32)[None, None, :]
    arr = np.repeat(c1 * (1 - t) + c2 * t, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    gx, gy = w * 0.80, h * 0.12
    d = np.sqrt(((xx - gx) / (w * 0.58)) ** 2 + ((yy - gy) / (h * 0.36)) ** 2)
    arr = arr + np.array((255, 255, 255), np.float32)[None, None, :] * (np.exp(-d * d) * 0.26)[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def decor_ticks(im):
    """左下「斜向刻度带」（本档专属装饰）。"""
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    n = 10
    step_x = int(w * 0.050)
    step_y = int(h * 0.036)
    L = int(min(w, h) * 0.070)
    for i in range(n):
        x0 = int(w * 0.030) + i * step_x
        y0 = int(h * 0.72) + i * step_y
        if x0 + L > w - 4 or y0 + L > h - 4:
            break
        col = GOLD + (44,) if i % 3 == 1 else (255, 255, 255, 20)
        od.line([(x0, y0), (x0 + L, y0 + L)], fill=col, width=4)
    od.line([(int(w * 0.030) - 8, int(h * 0.72) - 12),
             (int(w * 0.030) - 8, int(h * 0.72) + n * step_y + L)],
            fill=(255, 255, 255, 26), width=2)
    im.paste(ov, (0, 0), ov)


def rcard(im, box, fa=0, outline=None, oa=255, radius=22, width=2):
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fa:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fa))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (oa,), width=width)
    im.paste(ov, (0, 0), ov)


def put(d, text, xy, size, fill, bold=True, anchor="mm", maxw=None, tag=""):
    f = font(size, bold)
    if maxw:
        while f.size > 10:
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
    else:
        x0, y0 = cx - bw / 2, cy
    CHECKS.append((tag or text[:12], (x0, y0, x0 + bw, y0 + bh), maxw))
    return f


def gate(name):
    bad = []
    for tag, bb, maxw in CHECKS:
        if bb[0] < 20 or bb[2] > W - 20 or bb[1] < 8 or bb[3] > H - 20:
            bad.append((tag, tuple(round(v) for v in bb)))
        elif maxw and (bb[2] - bb[0]) > maxw + 2:
            bad.append((tag, "maxw"))
    print(("OK   " if not bad else "!!   ") + name, bad if bad else "")
    CHECKS.clear()
    return not bad


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    im.save(p)
    print("     saved", name, im.size)


def badge(d):
    f = font(30)
    tw = d.textlength(BADGE, font=f)
    d.rounded_rectangle([X0 - 10, 56, X0 + tw + 18, 100], radius=12,
                        fill=(8, 22, 50), outline=(130, 175, 235), width=3)
    put(d, BADGE, (X0, 60), 30, (210, 232, 255), anchor="la", tag="badge")


def footer(d, text=SRC):
    put(d, text, (W / 2, H - 42), 21, (188, 200, 214), bold=False, tag="footer")


def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if d.textlength(cur + ch, font=f) <= maxw:
                cur += ch
            else:
                out.append(cur)
                cur = ch
        if cur:
            out.append(cur)
    return out


def block(d, text, size, fill, y, maxw=CAPW, lh=1.26, x=W / 2, anchor="mm", tag=""):
    f = font(size)
    for ln in wrap(d, text, f, maxw):
        put(d, ln, (x, y + size * 0.62), size, fill, anchor=anchor, tag=tag)
        y += size * lh
    return y


# ==================== 封面 ×3 ====================
def tt_cover(fn, title, hook):
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    fs, ff = None, None
    for s in range(122, 47, -2):
        c = font(s)
        if max(d.textlength(l, font=c) for l in title) <= CAPW:
            fs, ff = s, c
            break
    assert fs, title
    hk, hf = None, None
    for s in range(46, 19, -2):
        c = font(s)
        if d.textlength(hook, font=c) <= CAPW:
            hk, hf = s, c
            break
    assert hk, hook
    lh = int(fs * 1.34)
    est = lh * len(title) + 56 + int(hk * 1.6)
    y0 = max((H - est) // 2 - int(fs * 0.25), 140)
    ys = [y0 + i * lh for i in range(len(title))]
    for l, y in zip(title, ys):
        d.text((X0, y), l, font=ff, fill=WHITE, anchor="la")
        bb = d.textbbox((X0, y), l, font=ff, anchor="la")
        CHECKS.append((l[:10], bb, CAPW))
    tb = max(d.textbbox((X0, ys[i]), title[i], font=ff, anchor="la")[3] for i in range(len(title)))
    yh = tb + 56
    d.text((X0, yh), hook, font=hf, fill=GOLD, anchor="la")
    bb = d.textbbox((X0, yh), hook, font=hf, anchor="la")
    CHECKS.append((hook[:10], bb, CAPW))
    footer(d)
    gate(f"头条 {fn[8:26]} 标题{fs}px 钩子{hk}px")
    save(im, fn)


def cover_data():
    """封面2-数据对撞：100 分 vs 计入总分 0 分。"""
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    rcard(im, [X0, 250, W - X0, 570], fa=16, outline=GOLD, radius=24)
    d.line([W / 2, 280, W / 2, 540], fill=GOLD, width=3)
    put(d, "100分", (W * 0.28, 348), 100, GOLD, tag="n1")
    put(d, "生地会考满分", (W * 0.28, 442), 32, LIGHT, bold=False, tag="l1")
    put(d, "0分", (W * 0.72, 348), 100, WHITE, tag="n2")
    put(d, "计入中考总分", (W * 0.72, 442), 32, LIGHT, bold=False, tag="l2")
    block(d, "不算分，却是录取的硬门槛", 40, WHITE, 610, tag="c")
    footer(d)
    gate("头条 封面2-数据对撞")
    save(im, f"{PFX}-头条-封面2-数据对撞-1200x900.png")


def cover_answer():
    """封面3-答案大字。"""
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    put(d, "没成绩", (W / 2 + 3, 330), 132, (0, 16, 36), tag="s1")
    put(d, "没成绩", (W / 2, 326), 132, WHITE, tag="a1")
    put(d, "不能投档", (W / 2 + 3, 470), 132, (0, 16, 36), tag="s2")
    put(d, "不能投档", (W / 2, 466), 132, GOLD, tag="a2")
    block(d, "官方原文：没有生物与地理（合卷）成绩的，录取时不能投档", 32,
          LIGHT, 596, tag="n")
    footer(d)
    gate("头条 封面3-答案大字")
    save(im, f"{PFX}-头条-封面3-答案大字-1200x900.png")


# ==================== 正文图 ×3 ====================
def art_times():
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    block(d, "历年查分时间 · 都在 9 月，上午 10 点", 46, WHITE, 150, tag="t")
    put(d, "官方已公布：2026年 9月23日 10:00", (W / 2, 262), 28, GOLD, tag="sub")
    tx0, tx1 = 90, 1110
    rcard(im, [tx0, 306, tx1, 362], fa=26, radius=16)
    put(d, "年份", (330, 334), 30, WHITE, tag="h1")
    put(d, "成绩查询时间", (820, 334), 30, WHITE, tag="h2")
    rows = [
        ("2026年", "9月23日 10:00", GOLD),
        ("2025年", "9月18日 10:00", WHITE),
        ("2024年", "9月19日 10:00", WHITE),
        ("2023年", "9月22日 10:00", WHITE),
        ("2022年", "10月10日 10:00", LIGHT),
    ]
    ry0, row_h = 372, 82
    for i, (y, v, col) in enumerate(rows):
        ry = ry0 + i * row_h
        if i % 2 == 0:
            rcard(im, [tx0, ry, tx1, ry + row_h - 8], fa=12, radius=14)
        put(d, y, (330, ry + (row_h - 8) / 2), 36, (235, 243, 252), tag="y")
        put(d, v, (820, ry + (row_h - 8) / 2), 36, col, tag="v")
    footer(d)
    gate("头条 正文图1-历年查分时间")
    save(im, f"{PFX}-头条-正文图1-历年查分时间-1200x900.png")


def art_howto():
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    block(d, "怎么查：1 个入口 + 3 样东西", 46, WHITE, 150, tag="t")
    rcard(im, [90, 250, 1110, 330], fa=18, outline=GOLD, radius=18)
    put(d, "深圳招考网 → 招考服务栏目 → 初二学业水平考试成绩查询", (W / 2, 290), 30,
        GOLD, tag="entry")
    steps = [("①", "11 位考生号", "报名时分配的考生号"),
             ("②", "身份证件号后 6 位", "有字母须大写，如 Y023456(A) 填 23456A"),
             ("③", "验证码", "查分页面会显示，照填即可")]
    ry = 370
    for n, tag, note in steps:
        rcard(im, [90, ry, 1110, ry + 122], fa=16, outline=(255, 255, 255), oa=70, radius=20)
        d.ellipse([124, ry + 39, 168, ry + 83], fill=GOLD)
        put(d, n, (146, ry + 61), 30, (18, 30, 55), tag="sn")
        put(d, tag, (210, ry + 46), 34, WHITE, anchor="lm", maxw=420, tag="st")
        put(d, note, (210, ry + 92), 26, LIGHT, bold=False, anchor="lm", maxw=840, tag="sn2")
        ry += 140
    put(d, "成绩公布当天，查询页面年份会更新为「2026」", (W / 2, 812), 28, GOLD, tag="n1")
    put(d, "最终成绩以市招考办下发的成绩单为准", (W / 2, 852), 24, LIGHT, bold=False, tag="n2")
    gate("头条 正文图2-怎么查")
    save(im, f"{PFX}-头条-正文图2-怎么查-1200x900.png")


def art_roles():
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    block(d, "这 100 分的 4 个作用", 46, WHITE, 138, tag="t")
    rows = [
        ("①", "有成绩才能投档", "没有这项成绩的，高中阶段学校录取时不能投档", GOLD),
        ("②", "同分比较第一层", "中考总分相同先比生地，比语数英更优先", GOLD),
        ("③", "名额分配批同样适用", "指标生批次遇同分，也走同一条规则", LIGHT),
        ("④", "缺考可补考", "缺考者可申请参加下一年度考试，但缺考当年不能投档", LIGHT),
    ]
    ry = 246
    for n, tag, note, col in rows:
        rcard(im, [80, ry, 1120, ry + 128], fa=16, outline=(255, 255, 255), oa=64, radius=20)
        d.ellipse([112, ry + 42, 156, ry + 86], fill=GOLD)
        put(d, n, (134, ry + 64), 30, (18, 30, 55), tag="n")
        put(d, tag, (196, ry + 48), 36, col, anchor="lm", maxw=520, tag="r1")
        put(d, note, (196, ry + 96), 26, SUB, bold=False, anchor="lm", maxw=880, tag="r2")
        ry += 148
    put(d, "不计入中考总分 · 却是录取门槛 + 同分决胜分", (W / 2, 858), 30, GOLD, tag="f")
    gate("头条 正文图3-四个作用")
    save(im, f"{PFX}-头条-正文图3-四个作用-1200x900.png")


# ==================== 微头条配图 ====================
def wt_numbers():
    im = base()
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    badge(d)
    block(d, "关于生地会考，记住 3 个数字", 46, WHITE, 150, tag="t")
    cards = [("100分", "生地会考满分", GOLD),
             ("0分", "计入中考总分", WHITE),
             ("第1层", "同分优先比它", GOLD)]
    cx = [230, 600, 970]
    cw, cy, ch = 340, 320, 400
    for (num, lab, col), xc in zip(cards, cx):
        rcard(im, [xc - cw / 2, cy, xc + cw / 2, cy + ch], fa=18,
              outline=(255, 255, 255), oa=80, radius=26)
        put(d, num, (xc + 3, cy + 132), 72, (0, 18, 40), tag="sh")
        put(d, num, (xc, cy + 128), 72, col, tag="n")
        d.line([xc - 66, cy + 250, xc + 66, cy + 250], fill=(255, 255, 255), width=2)
        put(d, lab, (xc, cy + 300), 30, (240, 246, 252), bold=False, tag="l")
    put(d, "没有成绩 = 不能投档 · 同分先比它", (W / 2, 790), 34, GOLD, tag="c")
    footer(d)
    gate("头条 微头条配图-关键数字")
    save(im, f"{PFX}-头条-微头条配图-关键数字-1200x900.png")


if __name__ == "__main__":
    tt_cover(f"{PFX}-头条-封面1-主标题-1200x900.png",
             ["生地会考成绩", "9月23日 10:00 开查"],
             "查分入口 · 三样东西 · 这 100 分的 4 个作用")
    cover_data()
    cover_answer()
    art_times()
    art_howto()
    art_roles()
    wt_numbers()
    print("ALL DONE (今日头条)")
