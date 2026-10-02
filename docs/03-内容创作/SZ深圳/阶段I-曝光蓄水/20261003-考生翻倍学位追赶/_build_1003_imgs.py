# -*- coding: utf-8 -*-
"""20261003 · 考生翻倍学位追赶 · 配图生成器（v2）

- 蓝系家族：沿用 09-26~10-02 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据（全部有官方出处，见 03-合规检查清单.md §一）：**
    中考考生   2022 = 11.20 万 → 2026 = 15.30 万   （深圳市招考办公布数据）
    公办普高招生 2022 = 约 5.9 万 → 2026 = 约 8 万（101 所）  （同源；2026 年 8 万/101 所经深圳特区报原文确认）
    公办普高录取率 2024 超 52% / 2025 超 52% / 2026 约 52%
    「十五五」（2026—2030）再增公办高中学位 10 万个以上（市教育局 2026-02 市人大记者会口径）
- **两个涨幅由脚本实算**，不手抄；脚本内含**双断言**：
    ① 两涨幅必须都落在 35%~38%；
    ② 两者之差必须 ≤1.5 个百分点（这正是本条论点：学位"刚好追上"）。
- **⚠️ 防同质化**：S1-4 已于 08-23 在头条发过长期数据。**配图首屏刻意不出现
  「7.21万→15.30万」的翻倍句式**，只放本条独有的**同窗口对比**。
- 产出（命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261003-1900-今日头条-微头条配图-考生翻倍学位追赶.png   1200x900
    20261003-2030-小红书-封面-考生翻倍学位追赶.png          1080x1440
    20261003-2030-小红书-正文图1-考生翻倍学位追赶.png       1080x1440
"""
import os, time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

TOP, BOT = (18, 52, 104), (6, 14, 34)
CARD, EDGE = (12, 34, 74), (96, 148, 216)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
RED = (255, 168, 152)

PFX = "20261003"
TTL = "考生翻倍学位追赶"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261003-考生翻倍学位追赶")
SRC = "数据来源：深圳市招考办公布的历年中考考生人数与公办普高招生计划"

# ---- 原始值（万人）。涨幅一律由 delta 实算，绝不手抄 ----
K22, K26 = 11.20, 15.30      # 中考考生
S22, S26 = 5.90, 8.00        # 公办普高招生
GK = (K26 / K22 - 1) * 100   # 考生涨幅
GS = (S26 / S22 - 1) * 100   # 学位涨幅
assert 35 <= GK <= 38 and 35 <= GS <= 38, (GK, GS)          # 断言①
assert abs(GK - GS) <= 1.5, (GK, GS)                        # 断言② 刚好追上
GK_S, GS_S = f"+{GK:.1f}%", f"+{GS:.1f}%"

BADS = []


def font(fp, s):
    return ImageFont.truetype(fp, s)


def save_img(im, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for _ in range(6):
        try:
            im.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)


def base(w, h):
    yv = np.linspace(0, 1, h)[:, None, None]
    grad = (np.array(TOP, float)[None, None, :] * (1 - yv) + np.array(BOT, float)[None, None, :] * yv)
    grad = np.repeat(grad, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    gx, gy = w * 0.24, h * 0.10
    radial = np.exp(-(((xx - gx) / (w * 0.60)) ** 2 + ((yy - gy) / (h * 0.34)) ** 2))
    img = grad + np.array([255, 255, 255], float)[None, None, :] * 0.28 * radial[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def fit(d, text, fp, size, maxw, mini):
    while size > mini:
        if d.textlength(text, font=font(fp, size)) <= maxw:
            return font(fp, size)
        size -= 2
    return font(fp, mini)


def txt(d, text, xy, size, fill, fp=FB, maxw=840, mini=24, anchor="mm", tag=""):
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    BADS.append((tag or text[:8], d.textbbox(xy, text, font=f, anchor=anchor)))
    return f


def rcard(d, x0, y0, x1, y1, rad=24, outline=None, fill=CARD):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=fill,
                        outline=outline or EDGE, width=3)


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    W, H, HM = 1200, 900, 60
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 考生与学位", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "四年里，考生跑多快，学位就跑多快", (W / 2, 164), 48, WHITE,
        maxw=W - 2 * HM, mini=32, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 258, 618
    tiles = [(GK_S, "2022→2026 中考考生涨幅", GOLD),
             (GS_S, "同期公办普高学位涨幅", GOLD),
             ("52%", "公办普高录取率·连续三年", RED)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), 66, col, maxw=bw - 26,
            mini=38, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=14, tag="tl")
    txt(d, "学位追上了考生，但只是刚好追上——所以稳得住，升不了", (W / 2, 690), 30, LIGHT,
        fp=FR, maxw=W - 2 * HM, mini=21, tag="tm")
    txt(d, "「十五五」（2026—2030）公办高中再增 10 万个学位", (W / 2, 746), 25, SUB, fp=FR,
        maxw=W - 2 * HM, mini=16, tag="tm2")
    txt(d, SRC, (W / 2, 848), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="tf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 考生与学位", (W / 2, 150), 44, GOLD, maxw=1000, mini=32, tag="ct")
    txt(d, "考生和学位", (W / 2, 330), 84, WHITE, maxw=1010, mini=58, tag="ct2")
    txt(d, "谁追上谁", (W / 2, 440), 84, WHITE, maxw=1010, mini=58, tag="ct3")
    d.line([W / 2 - 300, 556, W / 2 + 300, 556], fill=GOLD, width=8)
    txt(d, "同一个四年（2022→2026）", (W / 2, 660), 38, SUB, maxw=1000, mini=26, tag="ck0")
    txt(d, f"考生 {GK_S}", (W / 2, 762), 60, GOLD, maxw=1010, mini=42, tag="ck1")
    txt(d, f"公办学位 {GS_S}", (W / 2, 866), 60, GOLD, maxw=1010, mini=42, tag="ck2")
    txt(d, "所以录取率", (W / 2, 1020), 40, SUB, maxw=1000, mini=28, tag="ck3")
    txt(d, "只能稳，不能升", (W / 2, 1102), 60, RED, maxw=1010, mini=42, tag="ck4")
    txt(d, "52%", (W / 2, 1204), 52, WHITE, maxw=1010, mini=36, tag="ck5")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（同期对比表卡） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 56
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "同一个四年：考生 vs 公办学位", (W / 2, 68), 42, WHITE,
        maxw=W - 2 * HM, mini=28, tag="h1")
    txt(d, "2022 → 2026 · 深圳市招考办公布数据", (W / 2, 116), 24, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="h2")

    X_LBL, X_22, X_26, X_D = 82, 458, 686, 1014

    # 表头
    y = 168
    RH_H = 74
    rcard(d, HM, y, W - HM, y + RH_H - 8, rad=10, fill=(20, 46, 92), outline=EDGE)
    yy = y + (RH_H - 8) / 2
    txt(d, "项目", (X_LBL, yy), 26, GOLD, fp=FR, maxw=200, mini=17, anchor="lm", tag="th0")
    txt(d, "2022", (X_22, yy), 26, GOLD, fp=FR, maxw=180, mini=17, anchor="mm", tag="th1")
    txt(d, "2026", (X_26, yy), 26, GOLD, fp=FR, maxw=180, mini=17, anchor="mm", tag="th2")
    txt(d, "四年涨幅", (X_D, yy), 26, GOLD, fp=FR, maxw=210, mini=17, anchor="rm", tag="th3")
    y += RH_H

    rows = [("中考考生", "11.20万", "15.30万", GK_S, False),
            ("公办普高招生", "约5.9万", "约8万（101所）", GS_S, True)]
    for i, (lbl, a, b, dl, hl) in enumerate(rows):
        hh = 130
        rcard(d, HM, y, W - HM, y + hh, rad=10,
              fill=(44, 34, 20) if hl else CARD, outline=EDGE)
        txt(d, lbl, (X_LBL, y + hh / 2), 26, LIGHT, fp=FR, maxw=210, mini=17,
            anchor="lm", tag=f"r{i}l")
        txt(d, a, (X_22, y + hh / 2), 32, WHITE, fp=FR, maxw=200, mini=20,
            anchor="mm", tag=f"r{i}a")
        txt(d, b, (X_26, y + hh / 2), 32, WHITE, fp=FR, maxw=200, mini=19,
            anchor="mm", tag=f"r{i}b")
        txt(d, dl, (X_D, y + hh / 2), 38, GOLD, maxw=220, mini=24,
            anchor="rm", tag=f"r{i}d")
        y += hh

    y += 34
    rcard(d, HM, y, W - HM, y + 248, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, f"两边几乎一样快：{GK_S} vs {GS_S}", (HM + 30, y + 40), 28, GOLD, fp=FR,
        maxw=W - 2 * HM - 60, mini=19, anchor="lm", tag="p0")
    txt(d, "公办普高录取率：2024 超52% · 2025 超52% · 2026 约52%", (HM + 30, y + 88), 23,
        SUB, fp=FR, maxw=W - 2 * HM - 60, mini=15, anchor="lm", tag="p1")
    txt(d, "连续三年，纹丝不动——没崩，但也没有升", (HM + 30, y + 124), 23, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=15, anchor="lm", tag="p2")
    txt(d, "学位追上了考生，但只是刚好追上", (HM + 30, y + 168), 25, LIGHT, fp=FR,
        maxw=W - 2 * HM - 60, mini=17, anchor="lm", tag="p3")
    y += 248 + 34

    rcard(d, HM, y, W - HM, y + 248, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "「十五五」（2026—2030）", (HM + 30, y + 40), 26, GOLD, fp=FR,
        maxw=W - 2 * HM - 60, mini=18, anchor="lm", tag="q0")
    txt(d, "公办高中再增 10 万个学位", (HM + 30, y + 84), 32, WHITE, fp=FR,
        maxw=W - 2 * HM - 60, mini=21, anchor="lm", tag="q1")
    txt(d, "三个限定词：五年累计 · 公办高中 · 规划目标", (HM + 30, y + 132), 22, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=15, anchor="lm", tag="q2")
    txt(d, "不是每年 2 万，也不是某一年的数", (HM + 30, y + 170), 22, SUB, fp=FR,
        maxw=W - 2 * HM - 60, mini=15, anchor="lm", tag="q3")
    y += 248 + 34

    rcard(d, HM, y, W - HM, y + 156, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 30, y + 36), 23, LIGHT, fp=FR,
        maxw=W - 2 * HM - 60, mini=16, anchor="lm", tag="ny0")
    txt(d, "· 两个涨幅为同期（2022→2026）对比，由本表实算", (HM + 30, y + 70), 20, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=14, anchor="lm", tag="ny1")
    txt(d, "· 2027 年及以后数据以官方正式发布为准", (HM + 30, y + 102), 20, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=14, anchor="lm", tag="ny2")
    txt(d, "· 长期数据（2018 年 7.21 万→2026 年 15.30 万）仅作背景，非本条主数据", (HM + 30, y + 132), 20, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=14, anchor="lm", tag="ny3")
    y += 156

    txt(d, SRC, (W / 2, y + 46), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 46)} / 底部留白 {int(H - y - 64)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print(f"实算：考生 {GK_S} / 学位 {GS_S} / 差 {abs(GK-GS):.1f}pp")
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
