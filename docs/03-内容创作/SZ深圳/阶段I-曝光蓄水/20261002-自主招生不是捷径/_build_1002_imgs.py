# -*- coding: utf-8 -*-
"""20261002 · 自主招生不是捷径 · 配图生成器

- 蓝系家族：沿用 09-26~10-01 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据来源：本地官方原件，逐页核对**——
    E:/1.HSEE/1.HSEE-Prj/0GD.深圳资料/3.政策文件资料/
      · 2026年深圳市高中阶段学校考生报考指导手册.pdf
          PDF p4（页脚 3）  Q6 五个批次与顺序 / Q8 省一级须「达标」/ Q15 一类二类 / Q16 普高自招在中考后
          PDF p5（页脚 4）  Q20 已录取不得退档或转录 / 流程图注1「也须填报中考志愿，并参加中考」
      · 2026年深圳市教育局关于深化高中阶段学校考试招生制度改革的实施意见2026.05.25发布.md
          §五（三）  普高自主招生计划总比例 ≤ 学校年度招生计划的 10%
- **本脚本不含任何未经原件的数字**：报名具体日期、考核日期、成绩权重
  （60/40）等**一律未写入**，理由见 `03-合规检查清单.md` §二。
- 产出（配图命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261002-1900-今日头条-微头条配图-自主招生不是捷径.png   1200x900
    20261002-2030-小红书-封面-自主招生不是捷径.png          1080x1440
    20261002-2030-小红书-正文图1-自主招生不是捷径.png       1080x1440
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

PFX = "20261002"
TTL = "自主招生不是捷径"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261002-自主招生不是捷径")
SRC = "数据来源：深圳市教育局《2026年深圳市高中阶段学校考生报考指导手册》与《…考试招生制度改革的实施意见》"

# 手册 Q6 原文的五个批次（顺序照录）
BATCHES = ["自主招生批", "名额分配批", "统一招生（第一批）",
           "统一招生（第二批）", "统一招生（第三批）"]

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
    BADS.append((tag or text[:8], d.textbbox(xy, text, font=f, anchor=anchor)))
    return f


def rcard(d, x0, y0, x1, y1, rad=24, outline=None, fill=CARD):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=fill,
                        outline=outline or EDGE, width=3)


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    W, H, HM = 1200, 900, 60
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 自主招生", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "它排第 1 批，但不是捷径", (W / 2, 168), 52, WHITE,
        maxw=W - 2 * HM, mini=34, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [("第 1 批", "在 5 个录取批次里的位置", GOLD),
             ("10%", "普高自招计划比例上限", GOLD),
             ("0", "被录取后还能参加的后续批次", RED)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        sz = 72 if num == "第 1 批" else 84
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), sz, col, maxw=bw - 30,
            mini=44, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=15, tag="tl")
    txt(d, "它在中考之后——报了也照样要填志愿、要中考", (W / 2, 692), 32, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, "依据：2026 年报考指导手册 Q6 / Q16 / 流程图注 1；实施意见 §五（三）", (W / 2, 748),
        23, SUB, fp=FR, maxw=W - 2 * HM, mini=16, tag="tm2")
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
    txt(d, "深圳中考 · 自主招生", (W / 2, 150), 44, GOLD, maxw=1000, mini=32, tag="ct")
    txt(d, "自主招生", (W / 2, 320), 88, WHITE, maxw=1010, mini=62, tag="ct2")
    txt(d, "不是「多一条命」", (W / 2, 446), 72, WHITE, maxw=1010, mini=52, tag="ct3")
    d.line([W / 2 - 300, 546, W / 2 + 300, 546], fill=GOLD, width=8)
    txt(d, "它排在第 1 批", (W / 2, 668), 56, SUB, maxw=1000, mini=38, tag="ct4")
    txt(d, "但你必须先中考、先填志愿", (W / 2, 762), 44, WHITE, maxw=1010, mini=30, tag="ct5")
    txt(d, "被它录取后", (W / 2, 930), 40, SUB, maxw=1000, mini=28, tag="ck1")
    txt(d, "后面还有 0 个批次", (W / 2, 1010), 56, RED, maxw=1010, mini=38, tag="ck2")
    txt(d, "计划上限 10%", (W / 2, 1136), 40, GOLD, maxw=1000, mini=28, tag="ck3")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（批次顺序图 + 四条硬规则） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 56
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "深圳高中录取：五个批次", (W / 2, 70), 44, WHITE, maxw=W - 2 * HM, mini=30, tag="h1")
    txt(d, "手册原文顺序 · 自主招生排第 1", (W / 2, 120), 24, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="h2")

    y = 172
    RH = 74
    for i, name in enumerate(BATCHES):
        hh = RH - 8
        first = (i == 0)
        rcard(d, HM, y, W - HM, y + hh, rad=12,
              fill=(20, 46, 92) if first else CARD,
              outline=RED if first else EDGE)
        txt(d, f"{'①②③④⑤'[i]}", (HM + 40, y + hh / 2), 30, GOLD if first else SUB,
            fp=FR, maxw=60, mini=20, anchor="lm", tag=f"bn{i}")
        txt(d, name, (HM + 100, y + hh / 2), 29, WHITE if first else LIGHT, fp=FR,
            maxw=W - 2 * HM - 160, mini=18, anchor="lm", tag=f"bt{i}")
        if first:
            txt(d, "你在这里", (W - HM - 26, y + hh / 2), 22, RED, fp=FR,
                maxw=150, mini=15, anchor="rm", tag="bf0")
        y += RH
    y += 12

    # 硬规则条
    rcard(d, HM, y, W - HM, y + 84, rad=12, outline=RED, fill=(38, 16, 20))
    txt(d, "已被上一批次录取 → 不再参加下一批次录取", (W / 2, y + 30), 28, RED,
        fp=FR, maxw=W - 2 * HM - 40, mini=19, tag="r1")
    txt(d, "且：已被录取的考生，不得退档或转录其他学校", (W / 2, y + 62), 24, SUB,
        fp=FR, maxw=W - 2 * HM - 40, mini=16, tag="r2")
    y += 84 + 30

    d.line([W / 2 - 340, y, W / 2 + 340, y], fill=EDGE, width=2)
    y += 32

    txt(d, "自主招生四条硬规则", (W / 2, y), 32, GOLD, maxw=W - 2 * HM, mini=22, tag="r0")
    y += 52
    rules = [("① 考核在中考之后", "报名时间和具体办法另行通知"),
             ("② 报了也要填志愿、也要中考", "流程图注 1 原文如此"),
             ("③ 录取后不得退档或转录", "选择了就得认"),
             ("④ 计划上限 ≤ 学校年度招生计划的 10%", "实施意见 §五（三）")]
    for i, (a, b) in enumerate(rules):
        rcard(d, HM, y, W - HM, y + 68, rad=10)
        txt(d, a, (HM + 28, y + 22), 25, WHITE, fp=FR, maxw=W - 2 * HM - 56,
            mini=17, anchor="lm", tag=f"q{i}a")
        txt(d, b, (HM + 28, y + 50), 21, SUB, fp=FR, maxw=W - 2 * HM - 56,
            mini=15, anchor="lm", tag=f"q{i}b")
        y += 74

    y += 10
    rcard(d, HM, y, W - HM, y + 108, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 30, y + 30), 23, LIGHT, fp=FR,
        maxw=W - 2 * HM - 60, mini=16, anchor="lm", tag="ny0")
    txt(d, "· 只引用本地官方原件（报考指导手册 / 实施意见）", (HM + 30, y + 60), 20, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=14, anchor="lm", tag="ny1")
    txt(d, "· 报名与考核的具体日期、成绩权重未列（无原件依据）", (HM + 30, y + 86), 20, SUB,
        fp=FR, maxw=W - 2 * HM - 60, mini=14, anchor="lm", tag="ny2")
    y += 108

    txt(d, SRC, (W / 2, y + 40), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 40)} / 底部留白 {int(H - y - 58)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
