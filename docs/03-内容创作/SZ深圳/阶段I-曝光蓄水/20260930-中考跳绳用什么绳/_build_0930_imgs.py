# -*- coding: utf-8 -*-
"""20260930 · 中考跳绳到底用什么绳 · 配图生成器

- 蓝系家族：沿用 09-26~09-29 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据来源：官方 PDF 原件，逐页核对**——
    E:/1.HSEE/1.HSEE-Prj/0GD.深圳资料/3.政策文件资料/
    附件2：2026年深圳市初中学业水平考试体育与健康科目考试项目规则和评分标准.pdf
      · p3   三类之一「4 分钟跳绳」规则（1 次机会、跳绳测试仪、场地器材无「绳」条款）
      · p7   二类之一「1 分钟跳绳」规则（2 次机会取最好、同上器材条款）
      · p35  跳绳评分表（4 分钟：男592/女584；1 分钟：男164/女164）
      · p22/p29/p30  球类器材条款（对照用：考场统一提供用球、考生不能自带球）
  该 PDF 非文本可解析，故本表**人工逐页抄录并复核**，不解析。
- 产出（配图命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20260930-1900-今日头条-微头条配图-中考跳绳用什么绳.png   1200x900
    20260930-2030-小红书-封面-中考跳绳用什么绳.png          1080x1440
    20260930-2030-小红书-正文图1-中考跳绳用什么绳.png       1080x1440
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
PFX = "20260930"                 # 发布日期
TTL = "中考跳绳用什么绳"          # 标题（与文稿文件名末段一致）
HH_TT, HH_XHS = "1900", "2030"   # 发布时间（与文稿文件名 HHMM 一致）

ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20260930-中考跳绳用什么绳")
SRC = "数据来源：深圳市教育局《2026年深圳市初中学业水平考试体育与健康科目考试项目规则和评分标准》"

# 官方两份跳绳规则的「场地器材」条款 —— 抄自 p3 / p7（两条一字不差）
GEAR_ROPE = ["平整适宜地面",
             "符合国家计量标准的跳绳测试仪",
             "倒计时电动计时器"]
# 球类器材条款（对照）—— 抄自 p22 / p29 / p30
GEAR_BALL = ["考场统一提供符合国家标准的用球",
             "考生不能自带球"]


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
    txt(d, "深圳体育中考 · 跳绳", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "官方规则里，一个字没提「绳」", (W / 2, 168), 50, WHITE,
        maxw=W - 2 * HM, mini=34, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [("592", "4 分钟跳绳满分（男·次）", GOLD),
             ("164", "1 分钟跳绳满分（男·次）", GOLD),
             ("0", "官方器材条款提到「绳」的次数", RED)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), 84, col, maxw=bw - 30, mini=48, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=15, tag="tl")
    txt(d, "成绩由「跳绳测试仪」计入，不是靠你那根绳", (W / 2, 692), 30, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, "4 分钟跳绳 1 次机会　·　1 分钟跳绳 2 次机会", (W / 2, 742), 26, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="tm2")
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
    txt(d, "跳绳，到底用什么绳？", (W / 2, 400), 84, WHITE, maxw=1010, mini=60, tag="ct2")
    d.line([W / 2 - 300, 500, W / 2 + 300, 500], fill=GOLD, width=8)
    txt(d, "官方规则翻遍了", (W / 2, 640), 60, SUB, maxw=1000, mini=42, tag="ct3")
    txt(d, "一个字没提「绳」", (W / 2, 780), 86, RED, maxw=1010, mini=62, tag="ct4")
    txt(d, "因为成绩是「跳绳测试仪」记的", (W / 2, 950), 38, WHITE, maxw=1000, mini=27, tag="ck")
    txt(d, "4 分钟跳绳 592 次满分 · 1 分钟跳绳 164 次满分", (W / 2, 1090), 32, GOLD,
        maxw=1010, mini=22, tag="cn")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= W - 20 and bb[3] <= H - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440 ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 60
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "官方「场地器材」条款对比", (W / 2, 72), 42, WHITE, maxw=W - 2 * HM, mini=30, tag="h1")
    txt(d, "两份跳绳规则 vs 球类规则", (W / 2, 122), 24, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="h2")

    y = 178
    # 球类（写明绳/球归属）
    bh = 152
    rcard(d, HM, y, W - HM, y + bh, rad=14, outline=EDGE)
    txt(d, "球类项目（排球 / 羽毛球 / 网球）", (HM + 30, y + 40), 29, LIGHT,
        fp=FR, maxw=W - 2 * HM - 60, mini=20, anchor="lm", tag="gb")
    for i, t in enumerate(GEAR_BALL):
        txt(d, "· " + t, (HM + 40, y + 88 + i * 40), 25, WHITE, fp=FR,
            maxw=W - 2 * HM - 80, mini=17, anchor="lm", tag=f"gbi{i}")
    y += bh + 20

    # 跳绳（无「绳」条款）
    rh = 236
    rcard(d, HM, y, W - HM, y + rh, rad=14, outline=RED, fill=(38, 16, 20))
    txt(d, "跳绳（4 分钟 / 1 分钟）", (HM + 30, y + 40), 29, RED,
        fp=FR, maxw=W - 2 * HM - 60, mini=20, anchor="lm", tag="gr")
    for i, t in enumerate(GEAR_ROPE):
        txt(d, "· " + t, (HM + 40, y + 88 + i * 40), 25, WHITE, fp=FR,
            maxw=W - 2 * HM - 80, mini=17, anchor="lm", tag=f"gri{i}")
    txt(d, "→ 一条也没提到「绳」", (HM + 40, y + rh - 26), 27, RED, fp=FR,
        maxw=W - 2 * HM - 80, mini=18, anchor="lm", tag="grz")
    y += rh + 26

    d.line([W / 2 - 340, y, W / 2 + 340, y], fill=EDGE, width=2)
    y += 30

    # 两种跳绳对比
    txt(d, "两种跳绳，差别在这", (W / 2, y), 32, GOLD, maxw=W - 2 * HM, mini=22, tag="cmp")
    y += 56
    rows = [("考试机会", "1 次", "2 次（取最好）"),
            ("满分（男）", "592 次", "164 次"),
            ("满分（女）", "584 次", "164 次"),
            ("失误", "不计次数，考试继续", "同")]
    RH = 68
    # 表头
    txt(d, "", (HM + 150, y), 1, WHITE, tag="sp")
    txt(d, "4 分钟跳绳（一类）", (HM + 470, y), 25, GOLD, maxw=380, mini=18, anchor="mm", tag="ch1")
    txt(d, "1 分钟跳绳（二类）", (W - HM - 200, y), 25, GOLD, maxw=380, mini=18, anchor="mm", tag="ch2")
    y += 40
    for lab, a, b in rows:
        rcard(d, HM, y, W - HM, y + RH - 8, rad=10)
        txt(d, lab, (HM + 24, y + (RH - 8) / 2), 24, LIGHT, fp=FR,
            maxw=250, mini=17, anchor="lm", tag="rl")
        txt(d, a, (HM + 470, y + (RH - 8) / 2), 25, WHITE, fp=FR,
            maxw=380, mini=17, anchor="mm", tag="ra")
        txt(d, b, (W - HM - 200, y + (RH - 8) / 2), 25, WHITE, fp=FR,
            maxw=380, mini=17, anchor="mm", tag="rb")
        y += RH
    y += 30
    # 「所以别把时间花在挑绳上」—— 填实底部，且是真正可操作的下一步
    by0, by1 = y, y + 226
    rcard(d, HM, by0, W - HM, by1, rad=14, outline=GOLD, fill=(26, 44, 84))
    txt(d, "所以别把时间花在挑绳上", (W / 2, by0 + 42), 31, GOLD,
        maxw=W - 2 * HM - 30, mini=22, tag="hw")
    txt(d, "① 先定项目：一类 4 分钟跳绳只有 1 次机会，", (HM + 34, by0 + 104), 25, WHITE,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="u1")
    txt(d, "　　二类 1 分钟跳绳有 2 次（取最好）", (HM + 34, by0 + 144), 25, WHITE,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="u2")
    txt(d, "② 练「失误后立刻重启」——失误不计次数，但时间在走", (HM + 34, by0 + 194), 25, GOLD,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="u3")

    txt(d, SRC, (W / 2, by1 + 46), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") + f"小红书正文图 (末行 y={int(by1 + 46)} / 底部留白 {int(H - by1 - 64)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
