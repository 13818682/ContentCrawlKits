# -*- coding: utf-8 -*-
"""20261004 · 龙岗区属公办高中 8 所 · 配图生成器（v2 · 官方区域口径）

- 蓝系家族：沿用 09-26~10-05 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据（全部回单一官方源，见 03-合规检查清单.md §一）**：
    源 A＝《2026年公办普通高中学校招生计划表》「区域」列 → 公办普高 **99** 所、其中「市直属」**47** 所、
           「龙岗区」**8** 所；区属合计 = 99 − 47 = **52**。
    源 B＝《2026年高中阶段学校第一批录取标准》→ 龙岗区属 8 所的 AC/D 类 **住宿线 · 走读线**。
- **⚠️ v1 已作废**：v1 用 `P3-10`/`P3-2` 的分区（龙岗 13 所），经两台数据源交叉后判定不可靠
  （漏 布吉中学 / 华中师范大学龙岗附属中学；误收 深高文博高中 / 深实验至臻高中）。
- **脚本内含 5 条断言**，任一不成立即报错：
    ① 恰好 8 所；② 有住宿线的 7 所 AC 住宿线严格降序；③ 该 7 所区间＝504~576；
    ④ 该 7 所中 D 住宿 > AC 住宿 的恰好 6 所；⑤ 99 − 47 = 52（区属合计自洽）。
- **⚠️ 零评价性表述**：只出现校名与分数线，不出现「四大/八大/梯队/名校/天花板/最好」。
- 产出（命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261004-1900-今日头条-微头条配图-龙岗区属公办高中8所.png   1200x900
    20261004-2030-小红书-封面-龙岗区属公办高中8所.png          1080x1440
    20261004-2030-小红书-正文图1-龙岗区属公办高中8所.png       1080x1440
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

PFX = "20261004"
TTL = "龙岗区属公办高中8所"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261004-龙岗区属公办高中8所")
SRC = "数据来源：深圳市教育局《2026年公办普通高中学校招生计划表》《2026年高中阶段学校第一批录取标准》"
SCOPE = "口径：官方《招生计划表》「区域」列 —— 市直属不划入任何区"

# ---- 原始值：(校名, AC住宿, AC走读, D住宿, D走读)；None = 该校无住宿线 ----
LG = [
    ("龙城高级中学",          576, 573, 576, 571),
    ("华中师范大学龙岗附属中学", 561, 556, 562, 552),
    ("龙岗区实验高级中学",      559, 548, 560, 550),
    ("平冈中学",              540, 534, 546, 540),
    ("横岗高级中学",          510, 503, 525, 521),
    ("平湖外国语学校",         506, 493, 524, 517),
    ("深圳市龙岗区第二高级中学", 504, 497, 522, 518),
    ("布吉中学",              None, 492, None, 515),
]

TOT_SCHOOLS = 99   # 官方《招生计划表》公办普高学校数（按校名去重）
CITY_DIRECT = 47   # 其中「市直属」
LG_N = len(LG)
QU_SHU = TOT_SCHOOLS - CITY_DIRECT   # 区属合计

BOARD = [r for r in LG if r[1] is not None]        # 有住宿线的 7 所
ACS = [r[1] for r in BOARD]
HI, LO = max(ACS), min(ACS)
BELOW = sum(1 for a in ACS if a < 560)
DUP = sum(1 for _, a, _, d, _ in BOARD if d > a)

assert LG_N == 8, LG_N                                                   # ①
assert LG_N == 0 or BOARD and all(r[1] is not None for r in BOARD)
assert ACS == sorted(ACS, reverse=True), ACS                             # ②
assert (HI, LO) == (576, 504), (HI, LO)                                  # ③
assert DUP == 6, DUP                                                     # ④
assert TOT_SCHOOLS - CITY_DIRECT == QU_SHU == 52, QU_SHU                 # ⑤
assert len(BOARD) == 7 and BELOW == 5 and len(LG) - len(BOARD) == 1

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
    txt(d, "龙岗的公办高中，按官方口径只有 8 所", (W / 2, 152), 44, WHITE,
        maxw=W - 2 * HM, mini=28, tag="tt")

    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 234, 566
    tiles = [(f"{LG_N} 所", "龙岗区属公办高中\n（官方「区域」列）", GOLD),
             (f"{CITY_DIRECT} 所", f"市直属·官方不划区\n（公办普高共 {TOT_SCHOOLS} 所）", RED),
             (f"{LO}–{HI}", f"区属 AC 类住宿线区间\n{len(BOARD)} 所有住宿 · 跨度 {HI - LO} 分", GOLD)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + 92), 62, col, maxw=bw - 26, mini=36, tag="tn")
        for j, ln in enumerate(lab.split("\n")):
            txt(d, ln, (x + bw / 2, y0 + 190 + j * 40), 20, SUB, fp=FR,
                maxw=bw - 22, mini=13, tag="tl")

    bx0, bx1, by = HM + 20, W - HM - 20, 664
    d.line([bx0, by, bx1, by], fill=EDGE, width=5)
    mid = bx0 + (bx1 - bx0) * (560 - LO) / (HI - LO)
    d.line([mid, by - 22, mid, by + 22], fill=GOLD, width=7)
    txt(d, f"{BELOW} 所在 560 分以下", (bx0 + (mid - bx0) / 2, by - 50), 25, LIGHT,
        fp=FR, maxw=mid - bx0 - 10, mini=15, tag="b1")
    txt(d, f"{len(BOARD) - BELOW} 所在 560 分以上", (mid + (bx1 - mid) / 2, by - 50), 25, GOLD,
        fp=FR, maxw=bx1 - mid - 10, mini=15, tag="b2")
    txt(d, f"最低 {LO} · 龙岗区第二高级中学", (bx0, by + 40), 21, SUB, fp=FR,
        maxw=440, mini=13, anchor="lm", tag="b3")
    txt(d, f"最高 {HI} · 龙城高级中学", (bx1, by + 40), 21, SUB, fp=FR,
        maxw=440, mini=13, anchor="rm", tag="b4")

    txt(d, "布吉中学没有住宿线，只招走读——AC 类走读线 492 分", (W / 2, 756), 27,
        LIGHT, fp=FR, maxw=W - 2 * HM, mini=18, tag="tm")
    txt(d, SCOPE, (W / 2, 804), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ts")
    txt(d, SRC, (W / 2, 846), 17, SUB, fp=FR, maxw=W - 2 * HM, mini=11, tag="tf")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 龙岗区", (W / 2, 140), 44, GOLD, maxw=1000, mini=30, tag="ct")
    txt(d, "按官方口径", (W / 2, 292), 52, SUB, maxw=1000, mini=34, tag="ca")
    txt(d, "龙岗区公办高中", (W / 2, 400), 76, WHITE, maxw=1010, mini=50, tag="ct2")
    txt(d, "只有 8 所？", (W / 2, 512), 76, WHITE, maxw=1010, mini=50, tag="ct3")
    d.line([W / 2 - 300, 626, W / 2 + 300, 626], fill=GOLD, width=8)
    txt(d, f"深圳 {TOT_SCHOOLS} 所公办普高", (W / 2, 744), 44, LIGHT, maxw=1000, mini=30, tag="ck0")
    txt(d, f"{CITY_DIRECT} 所是市直属", (W / 2, 846), 62, RED, maxw=1010, mini=42, tag="ck1")
    txt(d, "官方不划进任何区", (W / 2, 946), 44, SUB, maxw=1000, mini=30, tag="ck2")
    txt(d, f"区属合计 {QU_SHU} 所", (W / 2, 1060), 34, SUB, fp=FR, maxw=1000, mini=23, tag="ck3")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（8 所对照表） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 50
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "龙岗区属公办高中（8 所）", (W / 2, 56), 40, WHITE,
        maxw=W - 2 * HM, mini=27, tag="h1")
    txt(d, "2026 年第一批录取标准 · 住宿线 / 走读线", (W / 2, 98), 22, SUB, fp=FR,
        maxw=W - 2 * HM, mini=16, tag="h2")

    XV = [66, 560, 692, 824, 956]

    y = 138
    RH_H = 62
    rcard(d, HM, y, W - HM, y + RH_H - 8, rad=10, fill=(20, 46, 92), outline=EDGE)
    yy = y + (RH_H - 8) / 2
    txt(d, "学校", (XV[0], yy), 24, GOLD, fp=FR, maxw=390, mini=16, anchor="lm", tag="th0")
    for k, lab in enumerate(["AC住宿", "AC走读", "D住宿", "D走读"]):
        txt(d, lab, (XV[k + 1], yy), 22, GOLD, fp=FR, maxw=130, mini=15, anchor="mm", tag=f"th{k + 1}")
    y += RH_H

    RH = 88
    for i, (nm, a1, a2, d1, d2) in enumerate(LG):
        hi = a1 is not None and d1 is not None and d1 > a1
        nosleep = a1 is None
        rcard(d, HM, y, W - HM, y + RH - 6, rad=8,
              fill=(44, 34, 20) if hi else CARD,
              outline=GOLD if nosleep else EDGE)
        m = y + (RH - 6) / 2
        txt(d, nm, (XV[0], m), 24, WHITE if (hi or nosleep) else LIGHT, fp=FR,
            maxw=400, mini=14, anchor="lm", tag=f"n{i}")
        for k, v in enumerate([a1, a2, d1, d2]):
            col = DIM if v is None else WHITE
            txt(d, "无" if v is None else str(v), (XV[k + 1], m), 27, col, fp=FR,
                maxw=130, mini=17, anchor="mm", tag=f"c{i}{k}")
        y += RH

    y += 22
    rcard(d, HM, y, W - HM, y + 136, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "为什么「只有」8 所？", (HM + 26, y + 36), 25, GOLD, fp=FR,
        maxw=W - 2 * HM - 52, mini=17, anchor="lm", tag="p0")
    txt(d, f"官方《招生计划表》里，公办普高共 {TOT_SCHOOLS} 所，其中 {CITY_DIRECT} 所标「市直属」——"
           f"不划入任何区。", (HM + 26, y + 76), 19, SUB, fp=FR,
        maxw=W - 2 * HM - 52, mini=13, anchor="lm", tag="p1")
    txt(d, f"区属合计 {QU_SHU} 所，龙岗区 {LG_N} 所。市直属的那些面向全市招生，按区查不到。",
        (HM + 26, y + 106), 19, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="p2")
    y += 136 + 22

    rcard(d, HM, y, W - HM, y + 128, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, f"{len(BOARD)} 所有住宿线：{LO}–{HI} 分　|　{len(BOARD) - BELOW} 所高于 560",
        (HM + 26, y + 34), 23, GOLD, fp=FR, maxw=W - 2 * HM - 52, mini=16,
        anchor="lm", tag="q0")
    txt(d, f"D 类住宿线高于 AC 类：{DUP} 所　|　持平：1 所（龙城高级中学）",
        (HM + 26, y + 70), 21, RED, fp=FR, maxw=W - 2 * HM - 52, mini=14,
        anchor="lm", tag="q1")
    txt(d, "布吉中学无住宿线，只招走读（AC 492 / D 515）",
        (HM + 26, y + 100), 19, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="q2")
    y += 128 + 22

    rcard(d, HM, y, W - HM, y + 96, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 26, y + 30), 21, LIGHT, fp=FR,
        maxw=W - 2 * HM - 52, mini=15, anchor="lm", tag="ny0")
    txt(d, "· 「区」取自官方《招生计划表》「区域」列，非第三方表格的分区",
        (HM + 26, y + 60), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny1")
    txt(d, "· 录取线由招生计划、报考人数等共同决定，不代表对学校的评价",
        (HM + 26, y + 84), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny2")
    y += 96

    txt(d, SRC, (W / 2, y + 36), 17, SUB, fp=FR, maxw=W - 2 * HM, mini=11, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 16]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 36)} / 底部留白 {int(H - y - 54)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print(f"实算：公办普高 {TOT_SCHOOLS} 所 / 市直属 {CITY_DIRECT} 所 / 区属 {QU_SHU} 所 / 龙岗 {LG_N} 所")
    print(f"      有住宿线 {len(BOARD)} 所，AC {LO}~{HI}，低于 560 共 {BELOW} 所，D 类更高 {DUP} 所")
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
