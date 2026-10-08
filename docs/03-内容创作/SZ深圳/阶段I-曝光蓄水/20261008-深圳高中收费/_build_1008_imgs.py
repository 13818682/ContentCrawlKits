# -*- coding: utf-8 -*-
"""20261008 · 深圳高中收费 · 配图生成器（公办高中学费四档）

- 蓝系家族：沿用 09-26~10-07 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据（全部回官方源，见 01-收费核源档案.md §二/§三/§四/§五）**：
    源 A＝深价联字〔2002〕37号 → 公办普高「一费制」学杂费**按学校等级四档**
           （一般 905 / 区一级 996 / 市一级 1041 / 省一级 1131，元/生·学期），
           该费已含杂费、课本教材费、练习本费。
    源 B＝深价〔2001〕49号 → 住宿费 **450** 元/生·学期（高中）。
    源 C＝深财教〔2013〕34号 → 公办中职**符合条件者免学费**（对象含深圳市户籍）。
    源 D＝深圳市教育局「高中阶段学校信息」专栏 → 民办普高**逐校**收费，取到 4 所官方数。
- **脚本内含断言**，任一不成立即报错：
    ① 恰好四档；② 金额严格递增；③ 区间＝905~1131 且极差＝226；
    ④ 住宿费＝450；⑤ 民办 4 所金额严格递增且全部 ≥ 20000。
- **⚠️ 三条口径纪律**：
    ① **不写「借读生书杂费」**（深价联字〔2002〕37号 里的另一档，现行是否仍收未核）；
    ② 四档按**官方等级**分，**不是按好坏排**；
    ③ 民办那 4 所是**已核到的例子，不是推荐名单**（图内已注明）。
- **⚠️ 零评价性表述**：不出现「四大/八大/梯队/名校/天花板/最好」。
- 产出（命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261008-1900-今日头条-微头条配图-公办高中学费四档.png   1200x900
    20261008-2030-小红书-封面-公办高中学费四档.png          1080x1440
    20261008-2030-小红书-正文图1-公办高中学费四档.png       1080x1440
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
DIM = (120, 146, 186)

PFX = "20261008"
TTL = "公办高中学费四档"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261008-深圳高中收费")
SRC = ("数据来源：深圳市物价局、市教育局、市财政局《关于调整我市中小学收费标准全面实行"
       "「一费制」的通知》（深价联字〔2002〕37号）")
SCOPE = "口径：深价联字〔2002〕37号（2002 年秋季起执行）· 单位 元/生·学期"

# ---- 原始值 ----
TIERS = [("一般学校", 905), ("区一级学校", 996), ("市一级学校", 1041), ("省一级学校", 1131)]
DORM = 450                                   # 深价〔2001〕49号
MB = [("深圳市华侨（康桥）书院", 25800),        # 深圳市教育局「高中阶段学校信息」专栏
      ("深圳市龙岗区德琳学校", 29500),
      ("深圳市中荟高级中学", 31800),
      ("深圳市华胜实验学校", 35000)]

LO, HI = TIERS[0][1], TIERS[-1][1]
DIF = HI - LO

assert len(TIERS) == 4, TIERS                                                     # ①
assert all(TIERS[i][1] < TIERS[i + 1][1] for i in range(3)), TIERS                # ②
assert (LO, HI) == (905, 1131) and DIF == 226, (LO, HI, DIF)                      # ③
assert DORM == 450, DORM                                                          # ④
assert len(MB) == 4 and all(MB[i][1] < MB[i + 1][1] for i in range(3)), MB        # ⑤
assert all(v >= 20000 for _, v in MB), MB

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
    txt(d, "深圳中考 · 公办高中", (W / 2, 72), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "公办高中的学费，不是一个数，是四个数", (W / 2, 152), 44, WHITE,
        maxw=W - 2 * HM, mini=28, tag="tt")

    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 226, 536
    tiles = [(f"{len(TIERS)} 档", "公办高中学费按学校等级分档\n政府定价 · 非义务教育阶段", GOLD),
             (f"{LO}–{HI}", f"一学期 · 单位 元/生·学期\n最高档比最低档贵 {DIF} 元", RED),
             (f"{DORM}", "住宿费 · 元/生·学期\n住宿生另交（走读不收）", GOLD)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + 88), 58, col, maxw=bw - 26, mini=34, tag="tn")
        for j, ln in enumerate(lab.split("\n")):
            txt(d, ln, (x + bw / 2, y0 + 184 + j * 38), 19, SUB, fp=FR,
                maxw=bw - 22, mini=13, tag="tl")

    # ---- 四档明细条（等距四点，非按金额比例）----
    bx0, bx1, by = HM + 30, W - HM - 30, 664
    d.line([bx0, by, bx1, by], fill=EDGE, width=5)
    for i, (nm, v) in enumerate(TIERS):
        x = bx0 + (bx1 - bx0) * i / (len(TIERS) - 1)
        d.line([x, by - 20, x, by + 20], fill=GOLD, width=7)
        txt(d, nm, (x, 614), 19, SUB, fp=FR, maxw=230, mini=12, tag=f"t1{i}")
        txt(d, str(v), (x, 716), 30, WHITE, fp=FR, maxw=230, mini=18, tag=f"t2{i}")
    txt(d, "四档明细", (W / 2, 566), 22, GOLD, fp=FR, maxw=W - 2 * HM, mini=14, tag="bh")

    txt(d, "公办中职：符合条件的学生免学费（含深圳市户籍）", (W / 2, 788), 27,
        LIGHT, fp=FR, maxw=W - 2 * HM, mini=18, tag="tm")
    txt(d, SCOPE, (W / 2, 828), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ts")
    txt(d, SRC, (W / 2, 864), 17, SUB, fp=FR, maxw=W - 2 * HM, mini=11, tag="tf")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 公办高中", (W / 2, 150), 44, GOLD, maxw=1000, mini=30, tag="ct")
    txt(d, "按官方口径", (W / 2, 330), 52, SUB, maxw=1000, mini=34, tag="ca")
    txt(d, "公办高中的学费", (W / 2, 458), 80, WHITE, maxw=1010, mini=52, tag="ct2")
    txt(d, "有四个价？", (W / 2, 586), 80, WHITE, maxw=1010, mini=52, tag="ct3")
    d.line([W / 2 - 300, 716, W / 2 + 300, 716], fill=GOLD, width=8)
    txt(d, f"{LO} / {TIERS[1][1]} / {TIERS[2][1]} / {HI}", (W / 2, 940), 50, RED,
        maxw=1010, mini=34, tag="ck1")
    txt(d, "按学校等级 · 一学期", (W / 2, 1050), 38, SUB, maxw=1000, mini=28, tag="ck2")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（三类对照卡） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 50
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "深圳高中收费（三类对照）", (W / 2, 56), 40, WHITE,
        maxw=W - 2 * HM, mini=27, tag="h1")
    txt(d, "公办普高 / 公办中职 / 民办普高 · 口径与出处各不相同", (W / 2, 98), 21, SUB, fp=FR,
        maxw=W - 2 * HM, mini=15, tag="h2")

    y = 146
    IN = HM + 26
    MW = W - 2 * HM - 52

    # ---- A. 公办普高 ----
    rcard(d, HM, y, W - HM, y + 440, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "一、公办普高：四个价", (IN, y + 34), 26, GOLD, fp=FR,
        maxw=MW, mini=17, anchor="lm", tag="a0")
    ay = y + 66
    for i, (nm, v) in enumerate(TIERS):
        rcard(d, IN, ay, W - HM - 26, ay + 64, rad=8)
        txt(d, nm, (IN + 20, ay + 32), 23, LIGHT, fp=FR,
            maxw=430, mini=15, anchor="lm", tag=f"an{i}")
        txt(d, str(v), (W - HM - 46, ay + 32), 28, WHITE, fp=FR,
            maxw=180, mini=18, anchor="rm", tag=f"av{i}")
        ay += 70
    txt(d, f"住宿费另交 {DORM} 元/生·学期（住宿生）", (IN, ay + 22), 20, LIGHT, fp=FR,
        maxw=MW, mini=13, anchor="lm", tag="a5")
    txt(d, "这四个数已含杂费、课本教材费、练习本费；学校不得另收课本资料费、练习本费、证册费",
        (IN, ay + 56), 17, SUB, fp=FR, maxw=MW, mini=12, anchor="lm", tag="a6")
    y += 440 + 18

    # ---- B. 公办中职 ----
    rcard(d, HM, y, W - HM, y + 196, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "二、公办中职：符合条件可免学费", (IN, y + 32), 25, GOLD, fp=FR,
        maxw=MW, mini=16, anchor="lm", tag="b0")
    txt(d, "免学费对象：农村（含县镇）学生 / 城市涉农专业 / 家庭经济困难学生 /",
        (IN, y + 76), 19, SUB, fp=FR, maxw=MW, mini=13, anchor="lm", tag="b1")
    txt(d, "深圳市户籍学生 / 父母一方持有效居住证且正常缴社保的其他城市学生",
        (IN, y + 112), 19, SUB, fp=FR, maxw=MW, mini=13, anchor="lm", tag="b2")
    txt(d, "（艺术类相关表演专业除外 · 依据 深财教〔2013〕34号）",
        (IN, y + 154), 17, DIM, fp=FR, maxw=MW, mini=12, anchor="lm", tag="b3")
    y += 196 + 18

    # ---- C. 民办普高 ----
    rcard(d, HM, y, W - HM, y + 348, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "三、民办普高：市场调节价，没有统一表", (IN, y + 32), 25, GOLD, fp=FR,
        maxw=MW, mini=16, anchor="lm", tag="c0")
    cy = y + 62
    for i, (nm, v) in enumerate(MB):
        rcard(d, IN, cy, W - HM - 26, cy + 56, rad=8)
        txt(d, nm, (IN + 20, cy + 28), 22, LIGHT, fp=FR,
            maxw=560, mini=14, anchor="lm", tag=f"cn{i}")
        txt(d, f"{v:,}", (W - HM - 46, cy + 28), 25, WHITE, fp=FR,
            maxw=170, mini=16, anchor="rm", tag=f"cv{i}")
        cy += 62
    txt(d, "教育局官网逐校公示，以上是已核到的例子（元/学期·学费），不是推荐名单；以各校公示为准",
        (IN, cy + 20), 16, DIM, fp=FR, maxw=MW, mini=11, anchor="lm", tag="c5")
    y += 348 + 18

    # ---- D. 口径说明 ----
    rcard(d, HM, y, W - HM, y + 114, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (IN, y + 30), 20, LIGHT, fp=FR, maxw=MW, mini=14, anchor="lm", tag="d0")
    txt(d, "· 四档按官方《招生计划表》的学校等级分，不是按好坏排",
        (IN, y + 64), 17, SUB, fp=FR, maxw=MW, mini=12, anchor="lm", tag="d1")
    txt(d, "· 民办为市场调节价（粤发改规〔2025〕1号），故不存在统一价目表",
        (IN, y + 90), 17, SUB, fp=FR, maxw=MW, mini=12, anchor="lm", tag="d2")
    y += 114

    txt(d, SRC, (W / 2, y + 34), 16, SUB, fp=FR, maxw=W - 2 * HM, mini=11, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 16]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 34)} / 底部留白 {int(H - y - 54)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print(f"实算：公办 {len(TIERS)} 档 {LO}~{HI}（极差 {DIF}）／住宿 {DORM}／民办样例 {len(MB)} 所 "
          f"{MB[0][1]}~{MB[-1][1]}")
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
