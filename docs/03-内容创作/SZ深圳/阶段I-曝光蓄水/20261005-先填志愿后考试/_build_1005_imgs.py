# -*- coding: utf-8 -*-
"""20261005 · 先填志愿后考试 · 配图生成器

- 蓝系家族：沿用 09-26~10-04 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据（`P1-7` 数据核验清单 11/11：源《2026年深圳市高中阶段学校考生报考指导手册》§1）**：
    2026 年 志愿填报 5/23–6/1；文化课中考 6/26–6/28；中间间隔 = **实算**（脚本用 datetime 算，不手抄）。
    全年节奏：3 月报名 / 4 月体育 / 5 月实验+听说+志愿 / 6 月中考 / 7 月出分录取 / 8 月补录。
- **⚠️ 日期纪律（`08-阶段I` §4.6 三分法 ②）**：**2027 年日程官方尚未发布**——
  配图**主视觉只到「月」，不出现任何具体日期**；具体日期一律在正文里标「2026 年」。
- 产出（命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261005-1900-今日头条-微头条配图-先填志愿后考试.png           1200x900
    20261005-2030-小红书-封面-先填志愿后考试.png                  1080x1440
    20261005-2030-小红书-正文图1-先填志愿后考试.png               1080x1440
"""
import os, time
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

TOP, BOT = (18, 52, 104), (6, 14, 34)
CARD, EDGE = (12, 34, 74), (96, 148, 216)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
RED = (255, 168, 152)

PFX = "20261005"
TTL = "先填志愿后考试"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261005-先填志愿后考试")
SRC = "数据来源：深圳市教育局《2026年深圳市高中阶段学校考生报考指导手册》"
SCOPE = "月份为固定节奏；具体日期以 2026 年为参考，2027 年以官方发布为准"

# ---- 原始值：2026 年官方节点。间隔一律由 datetime 实算 ----
VOL_END = date(2026, 6, 1)    # 志愿确认截止
EXAM_START = date(2026, 6, 26)  # 文化课中考首日
GAP = (EXAM_START - VOL_END).days
assert GAP == 25, GAP                       # ① 实算：确认截止 → 开考 = 25 天
VOL_WINDOW = (date(2026, 6, 1) - date(2026, 5, 23)).days + 1
assert VOL_WINDOW == 10, VOL_WINDOW         # ② 志愿窗口 10 天

STAGES = [
    ("3 月", "中考报名", "错过就没有考试资格，不设补报", False),
    ("4 月", "体育中考", "36 分计入总分，选哪三项初三上就要定", False),
    ("5 月", "实验操作 + 英语听说 + 志愿填报", f"全年最挤的一个月，志愿窗口只有 {VOL_WINDOW} 天", True),
    ("6 月", "文化课考试", "2.5 天，7 科", False),
    ("7 月", "成绩公布 + 分批录取", "自招批 → 名额分配批 → 第一批 → 第二批", False),
    ("8 月", "补录 + 准备入学", "补录通常没有公办普高", False),
]
assert len(STAGES) == 6, len(STAGES)        # ③ 六个阶段

NODES = [
    "3 月 报名：没有报名等于没有考试资格，没有补报",
    "5 月 志愿填报：窗口只有 10 天，过期不补",
    '志愿的"确认"：保存不等于提交，要收到短信验证码',
]
assert len(NODES) == 3, len(NODES)          # ④ 三个致命节点

TILES = [(f"{GAP} 天", "志愿确认完 → 中考开考\n中间还有 25 天", GOLD),
         ("5 月", "填志愿的月份\n6 月才中考", RED),
         ("3 个", "错过就回不了头\n的节点", GOLD)]

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
    txt(d, "深圳中考 · 2027 届", (W / 2, 70), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "志愿，是在考试之前填的", (W / 2, 152), 50, WHITE,
        maxw=W - 2 * HM, mini=32, tag="tt")

    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 234, 566
    for i, (num, lab, col) in enumerate(TILES):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + 92), 66, col, maxw=bw - 26, mini=38, tag="tn")
        for j, ln in enumerate(lab.split("\n")):
            txt(d, ln, (x + bw / 2, y0 + 190 + j * 40), 21, SUB, fp=FR,
                maxw=bw - 22, mini=14, tag="tl")

    txt(d, "填志愿的时候，孩子还没考——确认完到开考，中间还有 25 天", (W / 2, 636), 28,
        LIGHT, fp=FR, maxw=W - 2 * HM, mini=19, tag="tm")

    rcard(d, HM, 690, W - HM, 782, rad=16, outline=EDGE, fill=(10, 28, 62))
    txt(d, "全年节奏", (HM + 28, 736), 22, GOLD, fp=FR, maxw=180, mini=15,
        anchor="lm", tag="s0")
    txt(d, "3月报名 · 4月体育 · 5月填志愿 · 6月中考 · 7月出分录取 · 8月补录",
        (W - HM - 28, 736), 22, SUB, fp=FR, maxw=W - 2 * HM - 230, mini=15,
        anchor="rm", tag="s1")

    txt(d, SCOPE, (W / 2, 816), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ts")
    txt(d, SRC, (W / 2, 854), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=12, tag="tf")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 2027 届", (W / 2, 150), 44, GOLD, maxw=1000, mini=30, tag="ct")
    txt(d, "深圳中考的志愿", (W / 2, 336), 76, WHITE, maxw=1010, mini=50, tag="ct2")
    txt(d, "是在考试之前填的", (W / 2, 448), 76, WHITE, maxw=1010, mini=50, tag="ct3")
    d.line([W / 2 - 300, 564, W / 2 + 300, 564], fill=GOLD, width=8)
    txt(d, "5 月填志愿", (W / 2, 686), 72, RED, maxw=1010, mini=48, tag="ck1")
    txt(d, "6 月才中考", (W / 2, 796), 72, GOLD, maxw=1010, mini=48, tag="ck2")
    d.line([W / 2 - 220, 890, W / 2 + 220, 890], fill=EDGE, width=3)
    txt(d, "填的时候", (W / 2, 1000), 40, SUB, maxw=1000, mini=28, tag="ck3")
    txt(d, "孩子还没考", (W / 2, 1086), 58, WHITE, maxw=1010, mini=40, tag="ck4")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（全年节奏表） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 50
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "2027 届中考 · 全年节奏", (W / 2, 58), 40, WHITE,
        maxw=W - 2 * HM, mini=27, tag="h1")
    txt(d, "月份为固定节奏，具体日期以官方发布为准", (W / 2, 100), 22, SUB, fp=FR,
        maxw=W - 2 * HM, mini=16, tag="h2")

    X_M, X_T = 92, 196
    y = 142
    RH = 140
    for i, (mo, item, note, hi) in enumerate(STAGES):
        rcard(d, HM, y, W - HM, y + RH - 8, rad=12,
              fill=(48, 32, 20) if hi else CARD,
              outline=GOLD if hi else EDGE)
        m = y + (RH - 8) / 2
        txt(d, mo, (X_M, m), 34, RED if hi else GOLD, fp=FR, maxw=110, mini=22, tag=f"m{i}")
        txt(d, item, (X_T, y + 46), 28, WHITE, maxw=W - HM - X_T - 24, mini=18,
            anchor="lm", tag=f"t{i}")
        txt(d, note, (X_T, y + 92), 21, SUB, fp=FR, maxw=W - HM - X_T - 24, mini=14,
            anchor="lm", tag=f"n{i}")
        y += RH

    y += 22
    rcard(d, HM, y, W - HM, y + 168, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "三个回不了头的节点", (HM + 26, y + 34), 25, GOLD, fp=FR,
        maxw=W - 2 * HM - 52, mini=17, anchor="lm", tag="q0")
    for j, ln in enumerate(NODES):
        txt(d, f"{j + 1}. {ln}", (HM + 26, y + 76 + j * 34), 20, SUB, fp=FR,
            maxw=W - 2 * HM - 52, mini=14, anchor="lm", tag=f"q{j + 1}")
    y += 168 + 22

    rcard(d, HM, y, W - HM, y + 118, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 26, y + 30), 22, LIGHT, fp=FR,
        maxw=W - 2 * HM - 52, mini=16, anchor="lm", tag="ny0")
    txt(d, "· 节点月份为每年固定节奏；文中具体日期为 2026 年官方值，2027 年以官方发布为准",
        (HM + 26, y + 62), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny1")
    txt(d, "· 志愿窗口 10 天、确认截止到开考 25 天，均由官方日期实算",
        (HM + 26, y + 88), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny2")
    y += 118

    txt(d, SRC, (W / 2, y + 34), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 16]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 34)} / 底部留白 {int(H - y - 52)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print(f"实算：志愿窗口 {VOL_WINDOW} 天 / 确认截止→开考 {GAP} 天 / 阶段 {len(STAGES)} 个")
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
