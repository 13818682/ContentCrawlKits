# -*- coding: utf-8 -*-
"""20260929 · 深圳体育中考 球类六选一怎么选 · 配图生成器

- 蓝系家族：沿用 09-26~09-28 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据来源：官方 PDF 原件，逐格核对**——
    E:/1.HSEE/1.HSEE-Prj/0GD.深圳资料/3.政策文件资料/
    附件2：2026年深圳市初中学业水平考试体育与健康科目考试项目规则和评分标准.pdf
      · p34         三类球类评分表（满分速/次数）
      · p20-21      排球规则（失误重做、计时不停、两次考试机会）
      · p23-24      乒乓球规则（2 分钟内 6 发球 + 30 次组合）
      · p27-29      羽毛球规则（3 分钟内发球10 + 击球20）
      · p30         网球规则（5 分钟内发球10 + 击球20）
      · p36         备注（分段分值，实际按每一分值算到百分之一）
  该 PDF 非文本可解析，故本表**人工逐格抄录并复核**，不解析。
- 产出（配图命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20260929-1900-今日头条-微头条配图-体育三类项目怎么选.png   1200x900
    20260929-2030-小红书-封面-体育三类项目怎么选.png          1080x1440
    20260929-2030-小红书-正文图1-体育三类项目怎么选.png       1080x1440
"""
import time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

TOP, BOT = (18, 52, 104), (6, 14, 34)
CARD, EDGE = (12, 34, 74), (96, 148, 216)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
RED = (255, 168, 152)

BADS = []
# 配图命名（经营者 2026-09-26 定）：发布日期-时间-平台-文稿类型-标题
# 与「PNG 实体 / md frontmatter images / 本脚本 save_img()」三处同步，勿只改一处
PFX = "20260929"                 # 发布日期
TTL = "体育三类项目怎么选"        # 标题（与文稿文件名末段一致）
HH_TT, HH_XHS = "1900", "2030"   # 发布时间（与文稿文件名 HHMM 一致）

ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20260929-体育三类项目怎么选")
SRC = "数据来源：深圳市教育局《2026年深圳市初中学业水平考试体育与健康科目考试项目规则和评分标准》"

# 三类球类六选一：满分（100 分）标准 —— 抄自官方 PDF p34
BALLS = [
    ("足球",   "男 44.5 秒 / 女 46.5 秒", "计时"),
    ("篮球",   "男 38.5 秒 / 女 40.5 秒", "计时"),
    ("排球",   "男 22.9 秒 / 女 24.9 秒", "计时"),
    ("乒乓球", "28 次",                    "计数"),
    ("羽毛球", "21 次",                    "计数"),
    ("网球",   "21 次",                    "计数"),
]


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
    glow = np.array([255, 255, 255], float)[None, None, :]
    img = grad + glow * 0.28 * radial[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def fit(d, text, fp, size, maxw, mini):
    while size > mini:
        if d.textlength(text, font=font(fp, size)) <= maxw:
            return font(fp, size)
        size -= 2
    return font(fp, mini)


def txt(d, text, xy, size, fill, fp=FB, maxw=840, mini=24, anchor="mm", tag=""):
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    BADS.append((tag or text[:8], bb))
    return f


def rcard(d, x0, y0, x1, y1, rad=24, outline=None, fill=CARD):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=fill, outline=outline or EDGE, width=3)


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    W, H, HM = 1200, 900, 60
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳体育中考 · 2026 新规", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "球类六选一，别只看秒数", (W / 2, 168), 52, WHITE,
        maxw=W - 2 * HM, mini=36, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [("12 分", "每类实际占分（36÷3）", GOLD),
             ("2 种", "玩法：计时 vs 计数", GOLD),
             ("2 次", "排球考试机会（多数项目仅 1 次）", RED)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), 76, col, maxw=bw - 30, mini=46, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=15, tag="tl")
    txt(d, "计时项目失误＝重做，计时不停", (W / 2, 692), 30, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, "计数项目失误＝当次不计，考试继续", (W / 2, 742), 30, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm2")
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
    txt(d, "深圳体育中考", (W / 2, 170), 88, GOLD, maxw=1000, mini=72, tag="ct")
    txt(d, "球类六选一", (W / 2, 380), 96, WHITE, maxw=1010, mini=70, tag="ct2")
    txt(d, "到底怎么选？", (W / 2, 500), 96, WHITE, maxw=1010, mini=70, tag="ct3")
    d.line([W / 2 - 300, 600, W / 2 + 300, 600], fill=GOLD, width=8)

    # 两类玩法
    for i, (lab, items, col) in enumerate([
            ("计时", "足球 · 篮球 · 排球", GOLD),
            ("计数", "乒乓球 · 羽毛球 · 网球", LIGHT)]):
        y = 700 + i * 150
        txt(d, lab, (W / 2 - 330, y), 52, col, maxw=200, mini=36, tag=f"pl{i}")
        txt(d, items, (W / 2 + 100, y), 36, WHITE, maxw=560, mini=26, tag=f"pi{i}")

    txt(d, "不是哪个简单", (W / 2, 1030), 56, SUB, maxw=1000, mini=40, tag="cq")
    txt(d, "是失误后「重做」还是「少一次」", (W / 2, 1130), 48, GOLD,
        maxw=1010, mini=34, tag="ca")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= W - 20 and bb[3] <= H - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（六选一资产卡） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 60
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "球类六选一 · 满分标准", (W / 2, 74), 42, WHITE, maxw=W - 2 * HM, mini=30, tag="h1")
    txt(d, "三类项目（六选一）· 2026 官方评分标准", (W / 2, 126), 24, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="h2")

    # 表头
    y = 186
    HH_ = 48
    rcard(d, HM, y, W - HM, y + HH_, rad=12, outline=GOLD)
    txt(d, "项目", (HM + 80, y + HH_ / 2), 25, GOLD, anchor="mm", maxw=130, mini=18, tag="th1")
    txt(d, "满分（100 分）标准", (HM + 470, y + HH_ / 2), 25, GOLD, anchor="mm",
        maxw=520, mini=18, tag="th2")
    txt(d, "玩法", (W - HM - 90, y + HH_ / 2), 25, GOLD, anchor="mm", maxw=150, mini=18, tag="th3")
    y += HH_ + 8

    RH = 68
    for name, std, kind in BALLS:
        timed = (kind == "计时")
        rcard(d, HM, y, W - HM, y + RH - 8, rad=10,
              outline=GOLD if timed else EDGE, fill=(30, 40, 62) if timed else CARD)
        txt(d, name, (HM + 80, y + (RH - 8) / 2), 30, WHITE, anchor="mm", maxw=130, mini=20, tag="nm")
        txt(d, std, (HM + 470, y + (RH - 8) / 2), 27, LIGHT, fp=FR, anchor="mm",
            maxw=520, mini=18, tag="std")
        txt(d, kind, (W - HM - 90, y + (RH - 8) / 2), 27, GOLD if timed else SUB,
            fp=FR, anchor="mm", maxw=150, mini=19, tag="kd")
        y += RH

    y += 8
    d.line([W / 2 - 340, y, W / 2 + 340, y], fill=EDGE, width=2)

    # 两种失败模式对比 —— 本条的核心
    by0, by1 = y + 26, y + 300
    rcard(d, HM, by0, W - HM, by1, rad=14, outline=GOLD, fill=(26, 44, 84))
    txt(d, "两种玩法，失误代价完全不同", (W / 2, by0 + 40), 31, GOLD,
        maxw=W - 2 * HM - 30, mini=22, tag="hw")
    txt(d, "计时：失误要重做，计时不停 → 直接吃时间", (HM + 34, by0 + 104), 26, RED,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="m1")
    txt(d, "排球垫、传、扣任一环失误，整套重来", (HM + 34, by0 + 146), 23, SUB,
        fp=FR, maxw=W - 2 * HM - 68, mini=15, anchor="lm", tag="m2")
    txt(d, "计数：失误当次不计，考试继续 → 只少一次", (HM + 34, by0 + 198), 26, LIGHT,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="m3")
    txt(d, "乒乓球 2 分钟、羽毛球 3 分钟、网球 5 分钟", (HM + 34, by0 + 240), 23, SUB,
        fp=FR, maxw=W - 2 * HM - 68, mini=15, anchor="lm", tag="m4")

    y = by1 + 30
    txt(d, "每类满分 100，三类取平均 ×0.36＝36 分", (W / 2, y + 30), 29, GOLD,
        maxw=W - 2 * HM, mini=20, tag="eq")
    txt(d, "→ 每类实际占 12 分，没有可以放弃的凑数项", (W / 2, y + 80), 27, WHITE,
        maxw=W - 2 * HM, mini=19, tag="eq2")
    txt(d, SRC, (W / 2, y + 140), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") + f"小红书正文图 (末行 y={int(y + 140)} / 底部留白 {int(H - y - 158)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
