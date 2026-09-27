# -*- coding: utf-8 -*-
"""20260928 · 深圳中考「A线」到底是什么 · 配图生成器

- 蓝系家族：沿用 09-26 / 09-27 档调色与「左上主光」（`blue-family-visual-rule`）
- 数据**直接解析 P3-1 终稿**（单一数据源，不手抄）
- 产出（配图命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20260928-1900-今日头条-微头条配图-A线到底是什么.png   1200x900
    20260928-2030-小红书-封面-A线到底是什么.png          1080x1440
    20260928-2030-小红书-正文图1-A线到底是什么.png       1080x1440
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
PFX = "20260928"                 # 发布日期
TTL = "A线到底是什么"             # 标题（与文稿文件名末段一致）
HH_TT, HH_XHS = "1900", "2030"   # 发布时间（与文稿文件名 HHMM 一致）

ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20260928-A线到底是什么")
SRC_LEVELS = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
              "P3-数据择校地图/P3-1-一分一段表/"
              "01-P3-1-深圳中考成绩定位：分数-等级-排名-对标学校速查（2026数据2027参考）-公众号-终稿.md")
SRC = "数据来源：深圳市教育局 2026 年中考成绩公告"


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


# ---------------- 解析 P3-1 终稿（单一数据源） ----------------
LEVEL_ORDER = ["A+", "A", "B+", "B", "C+", "C"]


def load_levels():
    """返回 [(等级, 占比, 累计排名比例, 15.3万对应排名), ...] —— 直接解析 P3-1 表格。"""
    s = open(SRC_LEVELS, encoding="utf-8").read()
    out = []
    for line in s.split("\n"):
        if not line.startswith("|"):
            continue
        c = [x.strip().replace("**", "") for x in line.strip("|").split("|")]
        if len(c) < 4 or c[0] not in LEVEL_ORDER:
            continue
        out.append((c[0], c[1], c[2], c[3]))
    return out


def load_facts():
    """从 P3-1 抽出 考生总数 / A+线 两个关键数（不手抄）。"""
    s = open(SRC_LEVELS, encoding="utf-8").read()
    total = re.search(r"考生总数\s*\|\s*\*\*([\d.]+万)人\*\*", s)
    aplus = re.search(r"A\+线（总分）\s*\|\s*\*\*(\d+)分\*\*", s)
    over = re.search(r"600\s*分以上\s*\|\s*\*\*([\d+]+)人\*\*", s)
    # 兜底：报错好过编造
    assert total and aplus, "P3-1 关键数解析失败——不要手抄，去查源文件"
    return (total.group(1), aplus.group(1), over.group(1) if over else None)


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    total, aplus, _ = load_facts()
    W, H, HM = 1200, 900, 60
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 成绩定位", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "「A 线」不是录取线，是排名线", (W / 2, 168), 50, WHITE,
        maxw=W - 2 * HM, mini=34, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [(aplus, "2026 年 A+ 线（全市前 5%）"),
             ("前 25%", "A 线 = 单科进全市前 25%"),
             (f"{total}", "2026 考生总数（等级按此池划）")]
    for i, (num, lab) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.33), 76, GOLD, maxw=bw - 30, mini=44, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=15, tag="tl")
    txt(d, "等级比例固定不变，分数线年年都变", (W / 2, 692), 30, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, SRC, (W / 2, 848), 20, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="tf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    lv = load_levels()
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考", (W / 2, 170), 92, GOLD, maxw=1000, mini=76, tag="ct")
    txt(d, "「A 线」到底是什么？", (W / 2, 400), 84, WHITE, maxw=1000, mini=60, tag="ct2")
    d.line([W / 2 - 300, 500, W / 2 + 300, 500], fill=GOLD, width=8)
    txt(d, "不是录取线", (W / 2, 640), 88, RED, maxw=1000, mini=64, tag="ct3")
    txt(d, "是排名线", (W / 2, 780), 88, GOLD, maxw=1000, mini=64, tag="ct4")
    txt(d, "等级比例固定　分数线年年变", (W / 2, 940), 38, WHITE, maxw=1000, mini=28, tag="ck")
    # 六档比例一行
    for i, (g, pct, cum, _r) in enumerate(lv):
        x = W / 2 + (i - 2.5) * 168
        txt(d, g, (x, 1090), 36, GOLD if i < 2 else LIGHT, maxw=150, mini=26, tag=f"lg{i}")
        txt(d, pct, (x, 1140), 26, SUB, fp=FR, maxw=150, mini=18, tag=f"lp{i}")
    txt(d, "A 线 = 全市前 5% – 25%", (W / 2, 1250), 34, GOLD, maxw=1000, mini=24, tag="cs")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= W - 20 and bb[3] <= H - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（等级比例资产卡） ----------------
def xhs_card():
    lv = load_levels()
    total, aplus, _ = load_facts()
    W, H, HM = 1080, 1440, 60
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "深圳中考 6 个等级 · 官方比例", (W / 2, 76), 42, WHITE,
        maxw=W - 2 * HM, mini=30, tag="h1")
    txt(d, "按全市排名切分，比例固定不变", (W / 2, 130), 25, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="h2")

    # 表头
    y = 196
    HH_ = 50
    rcard(d, HM, y, W - HM, y + HH_, rad=12, outline=GOLD)
    txt(d, "等级", (HM + 70, y + HH_ / 2), 25, GOLD, anchor="mm", maxw=110, mini=18, tag="th1")
    txt(d, "占比", (HM + 260, y + HH_ / 2), 25, GOLD, anchor="mm", maxw=110, mini=18, tag="th2")
    txt(d, "累计排名", (HM + 470, y + HH_ / 2), 25, GOLD, anchor="mm", maxw=200, mini=18, tag="th3")
    txt(d, f"{total}考生对应", (W - HM - 190, y + HH_ / 2), 25, GOLD, anchor="mm",
        maxw=300, mini=18, tag="th4")
    y += HH_ + 8

    RH = 92
    for i, (g, pct, cum, rng) in enumerate(lv):
        top = (i < 2)                                     # A+/A 高亮
        rcard(d, HM, y, W - HM, y + RH - 8, rad=10,
              outline=GOLD if top else EDGE, fill=(24, 46, 92) if top else CARD)
        col = GOLD if top else WHITE
        txt(d, g, (HM + 70, y + (RH - 8) / 2), 42, col, anchor="mm", maxw=110, mini=26, tag="lv")
        txt(d, pct, (HM + 260, y + (RH - 8) / 2), 34, col, fp=FR, anchor="mm",
            maxw=110, mini=22, tag="pc")
        txt(d, cum, (HM + 470, y + (RH - 8) / 2), 30, LIGHT, fp=FR, anchor="mm",
            maxw=200, mini=20, tag="cm")
        r = rng.replace("约", "").replace("名", "")
        txt(d, r, (W - HM - 190, y + (RH - 8) / 2), 26, LIGHT, fp=FR, anchor="mm",
            maxw=300, mini=17, tag="rg")
        y += RH

    y += 10
    d.line([W / 2 - 340, y, W / 2 + 340, y], fill=EDGE, width=2)
    txt(d, f"2026 年 A+ 线：{aplus} 分（全市前 5%）", (W / 2, y + 60), 34, GOLD,
        maxw=W - 2 * HM, mini=24, tag="ap")
    txt(d, "等级线是「定位线」，不是「录取线」", (W / 2, y + 118), 32, WHITE,
        maxw=W - 2 * HM, mini=22, tag="key")

    # 「怎么用」提示框 —— 填实底部，且是真正可操作的一步
    by0, by1 = y + 156, y + 400
    rcard(d, HM, by0, W - HM, by1, rad=14, outline=GOLD, fill=(26, 44, 84))
    txt(d, "怎么用这张表", (W / 2, by0 + 40), 30, GOLD, maxw=W - 2 * HM - 30, mini=22, tag="hw")
    txt(d, "① 先看孩子的单科等级（不是分数）", (HM + 34, by0 + 100), 25, WHITE,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="u1")
    txt(d, "② 用等级查上表的排名区间，定位全市位置", (HM + 34, by0 + 146), 25, WHITE,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="u2")
    txt(d, "③ 比例永不变、分数年年变 —— 盯等级，别盯分数", (HM + 34, by0 + 192), 25, GOLD,
        fp=FR, maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag="u3")

    txt(d, SRC, (W / 2, by1 + 52), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=14, tag="ft")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") + f"小红书正文图 (末行 y={int(by1 + 52)} / 底部留白 {int(H - by1 - 70)}px)", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    print("解析到等级档:", [r[0] for r in load_levels()], "| 关键数:", load_facts())
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
