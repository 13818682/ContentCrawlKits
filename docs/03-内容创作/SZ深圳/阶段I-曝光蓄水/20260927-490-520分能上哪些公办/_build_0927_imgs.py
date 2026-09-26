# -*- coding: utf-8 -*-
"""20260927 · 490~520 分能上哪些公办 · 配图生成器

- 蓝系家族：沿用 09-26 档调色与「左上主光」（`blue-family-visual-rule`）
- 数据**直接解析 P3-2 终稿**（单一数据源，与 09-26 主题 B 同源，避免手抄）
- 产出（配图命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20260927-1900-今日头条-微头条配图-490-520分能上哪些公办.png   1200x900
    20260927-2030-小红书-封面-490-520分能上哪些公办.png          1080x1440
    20260927-2030-小红书-正文图1-490-520分能上哪些公办.png       1080x1440
"""
import time, os, re
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
PFX = "20260927"                      # 发布日期
TTL = "490-520分能上哪些公办"           # 标题（与文稿文件名末段一致）
HH_TT, HH_XHS = "1900", "2030"        # 发布时间（与文稿文件名 HHMM 一致）

ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20260927-490-520分能上哪些公办")
SRC_SCHOOL = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
              "P3-数据择校地图/P3-2-AC-D分差排行/"
              "01-P3-2-AC类vsD类分差排行榜：哪些学校对D类最友好-公众号-终稿.md")
SRC = "数据来源：深圳市教育局正式发布的 2026 年高中阶段学校招生录取标准"


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


# ---------------- 解析 P3-2 终稿（与 09-26 主题 B 同源） ----------------
def load_schools():
    s = open(SRC_SCHOOL, encoding="utf-8").read()
    out = {}
    for line in s.split("\n"):
        if not line.startswith("|"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 6 or not re.fullmatch(r"\d+", c[3] or ""):
            continue
        name = c[0].replace("**", "")
        if name in ("学校", "") or set(name) <= set("-: "):
            continue
        out[name] = (int(c[3]), int(c[4]))       # (AC住宿线, D住宿线)
    return out


# 48 字上限的分档（与 P3-9 的三段一致，但数值以 P3-2 实算为准）
BANDS = [("487 – 499 分", 487, 499), ("503 – 510 分", 503, 510), ("516 – 520 分", 516, 520)]


def facts():
    sch = load_schools()
    ac520 = {n: v for n, v in sch.items() if v[0] <= 520}          # 深户够得到
    d520 = {n: v for n, v in sch.items() if v[1] <= 520}           # 非深户够得到
    ac500 = [n for n, v in sch.items() if v[0] <= 500]
    d500 = [n for n, v in sch.items() if v[1] <= 500]
    bands = []
    for lab, lo, hi in BANDS:
        rs = sorted([(n, v[0], v[1]) for n, v in sch.items() if lo <= v[0] <= hi],
                    key=lambda r: r[1])
        bands.append((lab, rs))
    return sch, ac520, d520, ac500, d500, bands


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    sch, ac520, d520, ac500, d500, _ = facts()
    W, H, HM = 1200, 900, 60
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 2026 公办高中", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "520 分以内的公办，深户和非深户差多少", (W / 2, 168), 46, WHITE,
        maxw=W - 2 * HM, mini=32, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [(str(len(ac520)), "深户可报（AC 线 ≤ 520）", GOLD),
             (str(len(d520)), "非深户可报（D 线 ≤ 520）", RED),
             (str(len(d500)), "非深户 500 分以下可报", RED)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), 84, col, maxw=bw - 30, mini=48, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=15, tag="tl")
    txt(d, "最低 AC 线 487 分　·　最低 D 线 504 分", (W / 2, 692), 30, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, "单位：AC 类 / D 类住宿生录取线", (W / 2, 742), 22, SUB, fp=FR,
        maxw=W - 2 * HM, mini=16, tag="tm2")
    txt(d, SRC, (W / 2, 848), 20, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="tf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    sch, ac520, d520, ac500, d500, _ = facts()
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考", (W / 2, 180), 92, GOLD, maxw=1000, mini=76, tag="ct")
    txt(d, "520 分以内的公办", (W / 2, 430), 90, WHITE, maxw=1010, mini=66, tag="ct2")
    txt(d, "能报哪些", (W / 2, 556), 90, WHITE, maxw=1010, mini=66, tag="ct3")
    d.line([W / 2 - 300, 660, W / 2 + 300, 660], fill=GOLD, width=8)
    # 双行对比：深户 vs 非深户
    for i, (num, lab, col) in enumerate([(str(len(ac520)), "所", GOLD), (str(len(d520)), "所", RED)]):
        y = 830 + i * 190
        txt(d, num, (W / 2 - 90, y), 110, col, maxw=320, mini=78, tag=f"cv{i}")
        txt(d, lab, (W / 2 + 60, y + 22), 46, col, maxw=200, mini=32, tag=f"cv{i}b")
        txt(d, "深户可报" if i == 0 else "非深户可报", (W / 2, y + 92), 34, SUB, fp=FR,
            maxw=900, mini=24, tag=f"cl{i}")
    txt(d, "2026 官方录取线 · 按 AC 线分 3 档", (W / 2, 1270), 32, SUB, fp=FR,
        maxw=1000, mini=24, tag="cs")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= W - 20 and bb[3] <= H - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（24 所资产卡） ----------------
def xhs_card():
    sch, ac520, d520, ac500, d500, bands = facts()
    W, H, HM = 1080, 1440, 60
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "520 分以内的 24 所公办高中", (W / 2, 70), 40, WHITE, maxw=W - 2 * HM, mini=28, tag="h1")
    txt(d, f"深户 AC 线 ≤ 520 共 {len(ac520)} 所，按分数分 3 档", (W / 2, 122), 24, SUB,
        fp=FR, maxw=W - 2 * HM, mini=18, tag="h2")

    y = 168
    BH, RH = 48, 46
    for lab, rs in bands:
        rcard(d, HM, y, W - HM, y + BH, rad=12, outline=GOLD)
        txt(d, f"{lab}　·　{len(rs)} 所", (W / 2, y + BH / 2), 29, GOLD,
            maxw=W - 2 * HM - 24, mini=20, tag="band")
        y += BH + 8
        # 校名两列排布
        colw = (W - 2 * HM - 24) / 2
        for i, (name, ac, dc) in enumerate(rs):
            cx = HM + 12 + (i % 2) * colw
            cy = y + (i // 2) * RH
            nm = name if len(name) <= 16 else name[:16] + "…"
            txt(d, nm, (cx, cy + RH / 2 - 2), 22, WHITE, fp=FR, maxw=colw - 96,
                mini=15, anchor="lm", tag="nm")
            txt(d, f"{ac}", (cx + colw - 76, cy + RH / 2 - 2), 23, GOLD, fp=FR,
                maxw=68, mini=16, anchor="rm", tag="ac")
            txt(d, f"{dc}", (cx + colw - 16, cy + RH / 2 - 2), 23, LIGHT, fp=FR,
                maxw=68, mini=16, anchor="rm", tag="dc")
        y += ((len(rs) + 1) // 2) * RH + 16

    # 非深户专区
    rcard(d, HM, y, W - HM, y + 64, rad=14, outline=RED, fill=(38, 16, 20))
    txt(d, f"非深户（D 线 ≤ 520）只剩 {len(d520)} 所", (W / 2, y + 32), 31, RED,
        maxw=W - 2 * HM - 24, mini=22, tag="dt")
    y += 76
    for name, (ac, dc) in sorted(d520.items(), key=lambda x: x[1][1]):
        nm = name if len(name) <= 18 else name[:18] + "…"
        txt(d, nm, (HM + 14, y), 23, WHITE, fp=FR, maxw=560, mini=16, anchor="lm", tag="dn")
        txt(d, f"AC {ac}　D {dc}", (W - HM - 14, y), 23, RED, fp=FR,
            maxw=300, mini=16, anchor="rm", tag="dd")
        y += 42
    y += 16
    d.line([W / 2 - 340, y, W / 2 + 340, y], fill=EDGE, width=2)
    txt(d, "左列为深户 AC 线，右列为非深户 D 线", (W / 2, y + 34), 22, SUB, fp=FR,
        maxw=W - 2 * HM, mini=16, tag="lg")
    txt(d, "D 类家庭看 D 线那一列，别对着 AC 线看", (W / 2, y + 84), 27, GOLD,
        maxw=W - 2 * HM, mini=19, tag="cta")
    txt(d, SRC, (W / 2, y + 142), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=14, tag="ft")
    # 末尾一句：留白 ≥20px
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") + "小红书正文图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
