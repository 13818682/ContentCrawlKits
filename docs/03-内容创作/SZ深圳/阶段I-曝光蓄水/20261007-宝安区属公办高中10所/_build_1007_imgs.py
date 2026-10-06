# -*- coding: utf-8 -*-
"""20261007 · 宝安区属公办高中 10 所 · 配图生成器（官方区域口径）

- 蓝系家族：沿用 09-26~10-05 档调色与「左上主光」（`blue-family-visual-rule`）
- **数据（全部回两个官方原件，见 03-合规检查清单.md §一）**：
    源 A＝《2026年公办普通高中学校招生计划表》「区域」列 → 「宝安区」**10** 所；
           全市分到各区的公办普高合计 = **53** 所（「市直属」不划入任何区）。
    源 B＝《2026年高中阶段学校第一批录取标准》→ 宝安区属 10 所的 AC/D 类 **住宿线 · 走读线**。
- **⚠️ 故意不使用「公办普高总数」和「市直属所数」这两个数**：
  10-06 复检时把官方表重数了一遍，**同一张表的两套去重口径差 1**——官方**序号 1–100**（＝100 所）；
  按**校名**去重＝101 个名字。差的这一个，是**序号 23 的深圳市第三高级中学**（国内高考班 ／ 国家留学基金委
  自费出国留学班，共用一个序号、两个名字）。故总数 100 或 101、市直属 47 或 48，取决于口径。
  **但「区属合计」和「宝安区」在两套口径下完全一致（53 / 10）** → 本包只用这两个数。
  完整处置与挂账见 03-合规检查清单.md §二。
- **脚本内含 6 条断言**，任一不成立即报错：
    ① 恰好 10 所；② AC 住宿线严格降序；③ 区间＝509~583（跨度 74）；
    ④ D 住宿 > AC 住宿 的恰好 7 所；⑤ 全市区属分项求和 = 53 = 脚本内 BY_AREA 之和
       （且与该列在两套去重口径下的实算值一致）；
    ⑥ 10 所全部有住宿线，且走读线一律低于住宿线。
- **⚠️ 零评价性表述**：只出现校名与分数线，不出现「四大/八大/梯队/名校/天花板/最好」。
- 产出（命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261007-1900-今日头条-微头条配图-宝安区属公办高中10所.png   1200x900
    20261007-2030-小红书-封面-宝安区属公办高中10所.png          1080x1440
    20261007-2030-小红书-正文图1-宝安区属公办高中10所.png       1080x1440
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

PFX = "20261007"
TTL = "宝安区属公办高中10所"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261007-宝安区属公办高中10所")
SRC = "数据来源：深圳市教育局《2026年公办普通高中学校招生计划表》《2026年高中阶段学校第一批录取标准》"
SCOPE = "口径：官方《招生计划表》「区域」列 —— 市直属不划入任何区"

# ---- 原始值：(校名, AC住宿, AC走读, D住宿, D走读) ----
BA = [
    ("宝安中学（集团）高中部",   583, 581, 581, 575),
    ("新安中学（集团）高中部",   570, 566, 570, 561),
    ("松岗中学",              557, 554, 561, 559),
    ("宝安第一外国语学校",      553, 544, 554, 544),
    ("深圳市龙津中学",         552, 535, 553, 542),
    ("深圳市燕川中学",         546, 519, 550, 534),
    ("西乡中学",              538, 532, 538, 535),
    ("深圳市福海中学",         535, 518, 544, 535),
    ("石岩外国语学校",         522, 503, 531, 524),
    ("沙井中学",              509, 503, 526, 523),
]

TOT_SCHOOLS = None  # ⚠️ 总数 100 或 101 取决于去重口径，本期**不对外使用**，见文件头说明
CITY_DIRECT = None  # ⚠️ 同上（47 或 48）
BA_N = len(BA)

# 《招生计划表》「区域」列的全区分项（两套去重口径下一致，见 03-合规检查清单 §二）
BY_AREA = {"宝安区": 10, "龙华区": 9, "龙岗区": 8, "罗湖区": 6, "南山区": 6,
           "福田区": 5, "光明区": 3, "盐田区": 2, "坪山区": 2, "大鹏新区": 2}
QU_SHU = sum(BY_AREA.values())            # 全市分到各区的公办普高合计

ACS = [r[1] for r in BA]
HI, LO = max(ACS), min(ACS)
DUP = sum(1 for _, a, _, d, _ in BA if d > a)          # D 住宿 > AC 住宿
FLAT = sum(1 for _, a, _, d, _ in BA if d == a)        # 持平
LOWER = sum(1 for _, a, _, d, _ in BA if d < a)        # D 更低
BELOW = sum(1 for a in ACS if a < 550)

assert BA_N == 10, BA_N                                                  # ①
assert ACS == sorted(ACS, reverse=True), ACS                             # ②
assert (HI, LO) == (583, 509) and HI - LO == 74, (HI, LO)                # ③
assert DUP == 7, DUP                                                     # ④
assert QU_SHU == 53 and BY_AREA["宝安区"] == BA_N == 10, (QU_SHU, BA_N)  # ⑤
assert FLAT == 2 and LOWER == 1 and DUP + FLAT + LOWER == BA_N
assert all(a is not None and d2 < a for _, a, d2, _, _ in BA), "有校走读线不低于住宿线"  # ⑥
assert all(v2 < v1 for _, v1, v2, _, _ in BA), BA

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
    txt(d, "深圳中考 · 宝安区", (W / 2, 72), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "宝安的公办高中，按官方口径有 10 所", (W / 2, 152), 44, WHITE,
        maxw=W - 2 * HM, mini=28, tag="tt")

    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 234, 566
    tiles = [(f"{BA_N} 所", "宝安区属公办高中\n（官方「区域」列）", GOLD),
             (f"{QU_SHU} 所", "全市分到各区的公办普高\n（其余标「市直属」·不划区）", RED),
             (f"{LO}–{HI}", f"区属 AC 类住宿线区间\n{BA_N} 所全部可住宿 · 跨度 {HI - LO} 分", GOLD)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + 92), 62, col, maxw=bw - 26, mini=36, tag="tn")
        for j, ln in enumerate(lab.split("\n")):
            txt(d, ln, (x + bw / 2, y0 + 190 + j * 40), 20, SUB, fp=FR,
                maxw=bw - 22, mini=13, tag="tl")

    bx0, bx1, by = HM + 20, W - HM - 20, 664
    d.line([bx0, by, bx1, by], fill=EDGE, width=5)
    mid = bx0 + (bx1 - bx0) * (550 - LO) / (HI - LO)
    d.line([mid, by - 22, mid, by + 22], fill=GOLD, width=7)
    txt(d, f"{BELOW} 所在 550 分以下", (bx0 + (mid - bx0) / 2, by - 50), 25, LIGHT,
        fp=FR, maxw=mid - bx0 - 10, mini=15, tag="b1")
    txt(d, f"{BA_N - BELOW} 所在 550 分以上", (mid + (bx1 - mid) / 2, by - 50), 25, GOLD,
        fp=FR, maxw=bx1 - mid - 10, mini=15, tag="b2")
    txt(d, f"最低 {LO} · 沙井中学", (bx0, by + 40), 21, SUB, fp=FR,
        maxw=440, mini=13, anchor="lm", tag="b3")
    txt(d, f"最高 {HI} · 宝安中学（集团）高中部", (bx1, by + 40), 21, SUB, fp=FR,
        maxw=520, mini=13, anchor="rm", tag="b4")

    txt(d, f"D 类住宿线 {DUP} 所更高、{FLAT} 所持平，宝安中学低 2 分", (W / 2, 756), 27,
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
    txt(d, "深圳中考 · 宝安区", (W / 2, 150), 44, GOLD, maxw=1000, mini=30, tag="ct")
    txt(d, "按官方口径", (W / 2, 330), 52, SUB, maxw=1000, mini=34, tag="ca")
    txt(d, "宝安区公办高中", (W / 2, 458), 80, WHITE, maxw=1010, mini=52, tag="ct2")
    txt(d, "只有 10 所？", (W / 2, 586), 80, WHITE, maxw=1010, mini=52, tag="ct3")
    d.line([W / 2 - 300, 716, W / 2 + 300, 716], fill=GOLD, width=8)
    txt(d, f"全市分到各区的只有 {QU_SHU} 所", (W / 2, 940), 50, RED, maxw=1010, mini=34, tag="ck1")
    txt(d, "其余都标「市直属」·不划进任何区", (W / 2, 1050), 38, SUB, maxw=1000, mini=28, tag="ck2")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（10 所对照表） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 50
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "宝安区属公办高中（10 所）", (W / 2, 54), 40, WHITE,
        maxw=W - 2 * HM, mini=27, tag="h1")
    txt(d, "2026 年第一批录取标准 · 住宿线 / 走读线", (W / 2, 94), 22, SUB, fp=FR,
        maxw=W - 2 * HM, mini=16, tag="h2")

    XV = [56, 566, 694, 822, 950]

    y = 130
    RH_H = 58
    rcard(d, HM, y, W - HM, y + RH_H - 8, rad=10, fill=(20, 46, 92), outline=EDGE)
    yy = y + (RH_H - 8) / 2
    txt(d, "学校", (XV[0], yy), 24, GOLD, fp=FR, maxw=430, mini=16, anchor="lm", tag="th0")
    for k, lab in enumerate(["AC住宿", "AC走读", "D住宿", "D走读"]):
        txt(d, lab, (XV[k + 1], yy), 22, GOLD, fp=FR, maxw=126, mini=15, anchor="mm", tag=f"th{k + 1}")
    y += RH_H

    RH = 74
    for i, (nm, a1, a2, d1, d2) in enumerate(BA):
        hi = d1 > a1                       # D 更高 → 浅暖底
        lo = d1 < a1                       # D 更低 → 金框（唯一一所）
        rcard(d, HM, y, W - HM, y + RH - 6, rad=8,
              fill=(44, 34, 20) if hi else CARD,
              outline=GOLD if lo else EDGE)
        m = y + (RH - 6) / 2
        txt(d, nm, (XV[0], m), 24, WHITE if (hi or lo) else LIGHT, fp=FR,
            maxw=448, mini=14, anchor="lm", tag=f"n{i}")
        for k, v in enumerate([a1, a2, d1, d2]):
            txt(d, str(v), (XV[k + 1], m), 27, WHITE if (hi or lo) else LIGHT, fp=FR,
                maxw=126, mini=17, anchor="mm", tag=f"c{i}{k}")
        y += RH

    y += 18
    rcard(d, HM, y, W - HM, y + 128, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "为什么「只有」10 所？", (HM + 26, y + 34), 25, GOLD, fp=FR,
        maxw=W - 2 * HM - 52, mini=17, anchor="lm", tag="p0")
    txt(d, f"官方《招生计划表》的「区域」列里，全市只有 {QU_SHU} 所分到了各区；"
           f"其余都标着「市直属」——", (HM + 26, y + 72), 19, SUB, fp=FR,
        maxw=W - 2 * HM - 52, mini=13, anchor="lm", tag="p1")
    txt(d, f"面向全市招生，官方不划进任何一个区。所以按区数，宝安区是 {BA_N} 所。",
        (HM + 26, y + 102), 19, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="p2")
    y += 128 + 18

    rcard(d, HM, y, W - HM, y + 118, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, f"{BA_N} 所全部可住宿：AC 住宿线 {LO}–{HI} 分　|　{BA_N - BELOW} 所高于 550",
        (HM + 26, y + 32), 23, GOLD, fp=FR, maxw=W - 2 * HM - 52, mini=16,
        anchor="lm", tag="q0")
    txt(d, f"D 类住宿线高于 AC 类：{DUP} 所　|　持平：{FLAT} 所",
        (HM + 26, y + 66), 21, RED, fp=FR, maxw=W - 2 * HM - 52, mini=14,
        anchor="lm", tag="q1")
    txt(d, "唯一更低的一所：宝安中学（集团）高中部 581 / 583（低 2 分）",
        (HM + 26, y + 96), 19, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="q2")
    y += 118 + 18

    rcard(d, HM, y, W - HM, y + 92, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 26, y + 28), 21, LIGHT, fp=FR,
        maxw=W - 2 * HM - 52, mini=15, anchor="lm", tag="ny0")
    txt(d, "· 「区」取自官方《招生计划表》「区域」列，非第三方表格的分区",
        (HM + 26, y + 56), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny1")
    txt(d, "· 录取线由招生计划、报考人数等共同决定，不代表对学校的评价",
        (HM + 26, y + 78), 18, SUB, fp=FR, maxw=W - 2 * HM - 52, mini=13,
        anchor="lm", tag="ny2")
    y += 92

    txt(d, SRC, (W / 2, y + 34), 17, SUB, fp=FR, maxw=W - 2 * HM, mini=11, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 16]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(y + 34)} / 底部留白 {int(H - y - 34 - 12)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print("实算：全市分到各区的公办普高 %d 所 / 宝安区 %d 所"
          "（总数与市直属所数因去重口径有二义，本包不使用）" % (QU_SHU, BA_N))
    print(f"      AC 住宿 {LO}~{HI}（跨度 {HI - LO}）；低于 550 共 {BELOW} 所；"
          f"D 类更高 {DUP} / 持平 {FLAT} / 更低 {LOWER}")
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
