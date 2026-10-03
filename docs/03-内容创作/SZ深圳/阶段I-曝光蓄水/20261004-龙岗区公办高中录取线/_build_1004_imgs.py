# -*- coding: utf-8 -*-
"""20261004 · 龙岗区公办高中录取线 · 配图生成器

- 蓝系家族：沿用 09-26~10-03 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据（深圳市教育局 2026 年高中阶段学校第一批录取标准）**：
    龙岗区 13 所公办高中的 AC 类 / D 类住宿线。
    数据源＝`20261001-录取线与招生计划可比表/_rows_1001.json`（81 所 JOIN 口径）
    交叉校验＝`P3-3 公办高中梯队`（区域与 AC/D 一致）、`P2-4 走读分差排行`（住宿线一致）
- **脚本内含 5 条断言**，任一不成立即报错，防止手抄漂移：
    ① 恰好 13 所；② AC 线严格降序；③ AC 区间＝504~579；
    ④ 560 分以下 9 所 / 以上 4 所；⑤ D 类线高于 AC 类的恰好 8 所。
- **⚠️ 零评价性表述**：配图只出现校名与分数线，**不出现「四大/八大/梯队/名校/天花板/最好」**
  （`00-阶段I主题计划与排期` §二 边界 2：不做学校排名/梯队式表述）。
- 产出（命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261004-1900-今日头条-微头条配图-龙岗区公办高中录取线.png   1200x900
    20261004-2030-小红书-封面-龙岗区公办高中录取线.png          1080x1440
    20261004-2030-小红书-正文图1-龙岗区公办高中录取线.png       1080x1440
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

PFX = "20261004"
TTL = "龙岗区公办高中录取线"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261004-龙岗区公办高中录取线")
SRC = "数据来源：深圳市教育局《2026年高中阶段学校第一批录取标准》"
SCOPE = "口径：2026 年已公布录取线的公办普高 81 所中的龙岗区 13 所"

# ---- 原始值：(校名, AC 类住宿线, D 类住宿线)。已按 AC 线降序 ----
LG = [
    ("深圳科学高中", 579, 579),
    ("龙城高级中学", 576, 576),
    ("深圳科学高中龙岗分校", 567, 567),
    ("广东实验中学深圳学校", 565, 570),
    ("龙岗区实验高级中学", 559, 560),
    ("深圳市第三高级中学", 544, 540),
    ("平冈中学", 540, 546),
    ("深圳市高级中学文博高中", 537, 539),
    ("深圳实验学校至臻高中", 526, 524),
    ("横岗高级中学", 510, 525),
    ("深圳启元中学", 510, 529),
    ("平湖外国语学校", 506, 524),
    ("深圳市龙岗区第二高级中学", 504, 522),
]

N = len(LG)
ACS = [r[1] for r in LG]
HI, LO = max(ACS), min(ACS)
SPAN = HI - LO
BELOW = sum(1 for a in ACS if a < 560)      # 560 分以下
ABOVE = sum(1 for a in ACS if a >= 560)     # 560 分及以上
DUP = sum(1 for _, a, d in LG if d > a)     # D 类线高于 AC 类
SAME = sum(1 for _, a, d in LG if d == a)
DLO = sum(1 for _, a, d in LG if d < a)

assert N == 13, N                                                  # ①
assert ACS == sorted(ACS, reverse=True), ACS                       # ②
assert (HI, LO) == (579, 504), (HI, LO)                            # ③
assert (BELOW, ABOVE) == (9, 4), (BELOW, ABOVE)                    # ④
assert DUP == 8, DUP                                               # ⑤
assert DUP + SAME + DLO == N

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
    txt(d, "深圳中考 · 龙岗区", (W / 2, 72), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "龙岗区公办高中，录取线差多少", (W / 2, 152), 46, WHITE,
        maxw=W - 2 * HM, mini=30, tag="tt")

    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 236, 570
    tiles = [(f"{N} 所", "龙岗区公办高中\n（已公布录取线口径）", GOLD),
             (f"{LO}–{HI}", f"AC 类住宿线区间\n跨度 {SPAN} 分", GOLD),
             (f"{DUP} 所", "D 类住宿线\n高于 AC 类住宿线", RED)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + 96), 62, col, maxw=bw - 26, mini=36, tag="tn")
        for j, ln in enumerate(lab.split("\n")):
            txt(d, ln, (x + bw / 2, y0 + 194 + j * 40), 21, SUB, fp=FR,
                maxw=bw - 22, mini=14, tag="tl")

    # 560 分界条
    bx0, bx1, by = HM + 20, W - HM - 20, 668
    d.line([bx0, by, bx1, by], fill=EDGE, width=5)
    mid = bx0 + (bx1 - bx0) * (560 - LO) / SPAN
    d.line([mid, by - 22, mid, by + 22], fill=GOLD, width=7)
    txt(d, f"{BELOW} 所在 560 分以下", (bx0 + (mid - bx0) / 2, by - 52), 26, LIGHT,
        fp=FR, maxw=mid - bx0 - 10, mini=16, tag="b1")
    txt(d, f"{ABOVE} 所在 560 分以上", (mid + (bx1 - mid) / 2, by - 52), 26, GOLD,
        fp=FR, maxw=bx1 - mid - 10, mini=16, tag="b2")
    txt(d, f"最低 {LO}（龙岗区第二高级中学）", (bx0, by + 40), 21, SUB, fp=FR,
        maxw=420, mini=14, anchor="lm", tag="b3")
    txt(d, f"最高 {HI}（深圳科学高中）", (bx1, by + 40), 21, SUB, fp=FR,
        maxw=420, mini=14, anchor="rm", tag="b4")

    txt(d, "看龙岗的学校，先看它在区内这一段的位置，再看它一所的线", (W / 2, 762), 27,
        LIGHT, fp=FR, maxw=W - 2 * HM, mini=19, tag="tm")
    txt(d, SCOPE, (W / 2, 806), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ts")
    txt(d, SRC, (W / 2, 846), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=12, tag="tf")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 龙岗区", (W / 2, 150), 44, GOLD, maxw=1000, mini=30, tag="ct")
    txt(d, "龙岗区公办高中", (W / 2, 330), 78, WHITE, maxw=1010, mini=52, tag="ct2")
    txt(d, "录取线差多少？", (W / 2, 442), 78, WHITE, maxw=1010, mini=52, tag="ct3")
    d.line([W / 2 - 300, 556, W / 2 + 300, 556], fill=GOLD, width=8)
    txt(d, "AC 类住宿线", (W / 2, 664), 38, SUB, maxw=1000, mini=26, tag="ck0")
    txt(d, f"{LO} → {HI}", (W / 2, 776), 76, GOLD, maxw=1010, mini=52, tag="ck1")
    txt(d, f"跨度 {SPAN} 分 · {N} 所", (W / 2, 866), 36, SUB, maxw=1000, mini=24, tag="ck2")
    txt(d, "13 所里", (W / 2, 1010), 40, SUB, maxw=1000, mini=28, tag="ck3")
    txt(d, f"{BELOW} 所在 560 分以下", (W / 2, 1096), 58, WHITE, maxw=1010, mini=40, tag="ck4")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（13 所对照表） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 50
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "龙岗区公办高中录取线（13 所）", (W / 2, 58), 40, WHITE,
        maxw=W - 2 * HM, mini=27, tag="h1")
    txt(d, "2026 年第一批录取标准 · 住宿线", (W / 2, 100), 23, SUB, fp=FR,
        maxw=W - 2 * HM, mini=17, tag="h2")

    X_NAME, X_AC, X_D, X_DIF = 70, 640, 800, 1005

    y = 142
    RH_H = 62
    rcard(d, HM, y, W - HM, y + RH_H - 8, rad=10, fill=(20, 46, 92), outline=EDGE)
    yy = y + (RH_H - 8) / 2
    txt(d, "学校", (X_NAME, yy), 25, GOLD, fp=FR, maxw=400, mini=16, anchor="lm", tag="th0")
    txt(d, "AC 类", (X_AC, yy), 25, GOLD, fp=FR, maxw=150, mini=16, anchor="mm", tag="th1")
    txt(d, "D 类", (X_D, yy), 25, GOLD, fp=FR, maxw=150, mini=16, anchor="mm", tag="th2")
    txt(d, "D−AC", (X_DIF, yy), 25, GOLD, fp=FR, maxw=170, mini=16, anchor="rm", tag="th3")
    y += RH_H

    RH = 56
    for i, (nm, a, dd) in enumerate(LG):
        hh = RH
        dif = dd - a
        hi = dif > 0
        rcard(d, HM, y, W - HM, y + hh - 4, rad=8,
              fill=(44, 34, 20) if hi else CARD, outline=EDGE)
        m = y + (hh - 4) / 2
        txt(d, nm, (X_NAME, m), 25, LIGHT if not hi else WHITE, fp=FR,
            maxw=430, mini=15, anchor="lm", tag=f"n{i}")
        txt(d, str(a), (X_AC, m), 29, WHITE, fp=FR, maxw=150, mini=18, anchor="mm", tag=f"a{i}")
        txt(d, str(dd), (X_D, m), 29, WHITE, fp=FR, maxw=150, mini=18, anchor="mm", tag=f"d{i}")
        txt(d, f"{dif:+d}" if dif else "0", (X_DIF, m), 27,
            RED if hi else (SUB if dif == 0 else LIGHT),
            fp=FR, maxw=170, mini=17, anchor="rm", tag=f"f{i}")
        y += hh

    y += 26
    rcard(d, HM, y, W - HM, y + 104, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, f"{BELOW} 所在 560 分以下 · {ABOVE} 所在 560 分以上", (HM + 26, y + 34), 24,
        GOLD, fp=FR, maxw=W - 2 * HM - 52, mini=17, anchor="lm", tag="p0")
    txt(d, f"最低 {LO} · 深圳市龙岗区第二高级中学　|　最高 {HI} · 深圳科学高中",
        (HM + 26, y + 74), 22, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=15,
        anchor="lm", tag="p1")
    y += 104 + 24

    rcard(d, HM, y, W - HM, y + 104, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, f"D 类线高于 AC 类：{DUP} 所　|　持平：{SAME} 所　|　更低：{DLO} 所",
        (HM + 26, y + 34), 24, RED, fp=FR, maxw=W - 2 * HM - 52, mini=17,
        anchor="lm", tag="q0")
    txt(d, "规律：分数越低的学校，D 类要多考的越多", (HM + 26, y + 74), 22, SUB,
        fp=FR, maxw=W - 2 * HM - 52, mini=15, anchor="lm", tag="q1")
    y += 104 + 24

    rcard(d, HM, y, W - HM, y + 96, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 26, y + 30), 22, LIGHT, fp=FR,
        maxw=W - 2 * HM - 52, mini=16, anchor="lm", tag="ny0")
    txt(d, "· 上表为 2026 年已公布录取线的公办普高 81 所中的龙岗区 13 所，非龙岗全部公办高中",
        (HM + 26, y + 60), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny1")
    txt(d, "· 录取线由招生计划、报考人数等共同决定，不代表对学校的评价",
        (HM + 26, y + 84), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny2")
    y += 96

    txt(d, SRC, (W / 2, y + 34), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 16]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 34)} / 底部留白 {int(H - y - 52)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print(f"实算：{N} 所 / AC {LO}~{HI}（跨度 {SPAN}）/ 560 以下 {BELOW} 所 / D 类更高 {DUP} 所")
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
