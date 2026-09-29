# -*- coding: utf-8 -*-
"""20261001 · 录取线与招生计划可比表 · 配图生成器

- 蓝系家族：沿用 09-26~09-30 档调色与「左上主光」（`blue-family-visual-rule`）
- **本脚本不手抄任何数字**：分档汇总一律由 `_extract_1001_data.py` 落盘的
  `_rows_1001.json` 现算（同一份数据 → 图、稿、合规清单三处口径不可能漂移）
- 两个官方源：
    A 招生计划  E:/1.HSEE/1.HSEE-Prj/0GD.深圳资料/3.政策文件资料/
               1.深圳市2026年公办普通高中学校招生计划表.xlsx
    B 录取线    P3-2-AC-D分差排行/01-…-公众号-终稿.md（源为官方第一批录取标准 Excel）
- 产出（配图命名 = 发布日期-时间-平台-文稿类型-标题，经营者 2026-09-26 定）：
    20261001-1900-今日头条-微头条配图-录取线与招生计划可比表.png   1200x900
    20261001-2030-小红书-封面-录取线与招生计划可比表.png          1080x1440
    20261001-2030-小红书-正文图1-录取线与招生计划可比表.png       1080x1440
"""
import io, json, os, time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

TOP, BOT = (18, 52, 104), (6, 14, 34)
CARD, EDGE = (12, 34, 74), (96, 148, 216)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
RED = (255, 168, 152)

PFX = "20261001"
TTL = "录取线与招生计划可比表"
HH_TT, HH_XHS = "1900", "2030"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20261001-录取线与招生计划可比表")
SRC = "数据来源：深圳市教育局《2026年公办普通高中学校招生计划表》与《2026年第一批录取标准》"

BADS = []
BANDS = [(580, 999, "580 分以上"), (560, 579, "560–579 分"), (540, 559, "540–559 分"),
         (520, 539, "520–539 分"), (500, 519, "500–519 分"), (0, 499, "499 分及以下")]


def load_bands():
    """六档汇总：学校数 / 招生计划合计 / D 类名额合计 —— 全部现算，不手抄。"""
    rows = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "_rows_1001.json"), encoding="utf-8"))["rows"]
    out = []
    for lo, hi, lab in BANDS:
        g = [r for r in rows if r["ac"] and lo <= r["ac"] <= hi]
        out.append({"label": lab, "n": len(g),
                    "tot": sum(r["tot"] for r in g),
                    "dq": sum(r["d_qty"] or 0 for r in g)})
    return out


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


def comma(n):
    return f"{n:,}"


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    W, H, HM = 1200, 900, 60
    b = load_bands()
    top, mid = b[0], b[1]          # 580+ / 560-579
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 2026 公办普高", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, "分数够了，不等于有位置", (W / 2, 168), 54, WHITE,
        maxw=W - 2 * HM, mini=36, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [(comma(top["tot"]), f"580 分以上 {top['n']} 所·招生计划", GOLD),
             (comma(top["dq"]), "其中 D 类名额", RED),
             (comma(mid["tot"]), f"560–579 分 {mid['n']} 所·招生计划", GOLD)]
    for i, (num, lab, col) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), 76, col, maxw=bw - 30, mini=44, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 21, SUB, fp=FR,
            maxw=bw - 26, mini=15, tag="tl")
    txt(d, "分数是门槛，位置是数量——两件事", (W / 2, 692), 32, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, "口径：AC 类住宿线分档 · 覆盖 81 所已公布录取线的公办普高", (W / 2, 748), 25, SUB,
        fp=FR, maxw=W - 2 * HM, mini=18, tag="tm2")
    txt(d, SRC, (W / 2, 848), 19, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="tf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    W, H = 1080, 1440
    b = load_bands()
    top = b[0]
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 2026 公办普高", (W / 2, 168), 44, GOLD, maxw=1000, mini=32, tag="ct")
    txt(d, "分数够了", (W / 2, 352), 92, WHITE, maxw=1010, mini=66, tag="ct2")
    txt(d, "不等于有位置", (W / 2, 480), 92, WHITE, maxw=1010, mini=66, tag="ct3")
    d.line([W / 2 - 300, 580, W / 2 + 300, 580], fill=GOLD, width=8)
    txt(d, "分数线只是门槛", (W / 2, 712), 58, SUB, maxw=1000, mini=40, tag="ct4")
    txt(d, "位置才是数量", (W / 2, 826), 58, RED, maxw=1000, mini=40, tag="ct5")
    txt(d, f"580 分以上只有 {top['n']} 所", (W / 2, 990), 42, WHITE, maxw=1000, mini=28, tag="ck1")
    txt(d, f"招生计划 {comma(top['tot'])} 人", (W / 2, 1064), 42, GOLD, maxw=1010, mini=28, tag="ck2")
    txt(d, f"其中 D 类名额只有 {comma(top['dq'])} 个", (W / 2, 1138), 38, RED,
        maxw=1010, mini=26, tag="ck3")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1352), 27, SUB, fp=FR,
        maxw=1000, mini=20, tag="cf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 10]
    print(("OK  " if not bad else "!!  ") + "小红书封面", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书正文图 1080×1440（六档可比表） ----------------
def xhs_card():
    W, H, HM = 1080, 1440, 56
    b = load_bands()
    im = base(W, H); d = ImageDraw.Draw(im)

    txt(d, "六档汇总：分数线 × 招生计划", (W / 2, 70), 44, WHITE, maxw=W - 2 * HM, mini=30, tag="h1")
    txt(d, "2026 年 81 所已公布录取线的公办普高", (W / 2, 120), 24, SUB, fp=FR,
        maxw=W - 2 * HM, mini=18, tag="h2")

    # 表头
    y = 176
    c1, c2, c3, c4 = HM + 30, HM + 330, HM + 590, W - HM - 150
    txt(d, "分数段（AC 住宿线）", (c1, y), 23, GOLD, fp=FR, maxw=300, mini=16, anchor="lm", tag="th1")
    txt(d, "学校", (c2, y), 23, GOLD, fp=FR, maxw=200, mini=16, tag="th2")
    txt(d, "招生计划", (c3, y), 23, GOLD, fp=FR, maxw=220, mini=16, tag="th3")
    txt(d, "D 类名额", (c4, y), 23, GOLD, fp=FR, maxw=200, mini=16, tag="th4")
    y += 34
    d.line([HM, y, W - HM, y], fill=EDGE, width=2)
    y += 8

    RH = 76
    for i, r in enumerate(b):
        hh = RH - 8
        rcard(d, HM, y, W - HM, y + hh, rad=10,
              fill=(20, 46, 92) if i == 0 else CARD,
              outline=RED if i == 0 else EDGE)
        lab = r["label"]
        txt(d, lab, (c1, y + hh / 2), 26, WHITE if i == 0 else LIGHT, fp=FR,
            maxw=300, mini=17, anchor="lm", tag=f"rl{i}")
        txt(d, f"{r['n']} 所", (c2, y + hh / 2), 26, WHITE, fp=FR,
            maxw=200, mini=17, tag=f"rn{i}")
        txt(d, comma(r["tot"]), (c3, y + hh / 2), 27, GOLD if i == 0 else WHITE, fp=FR,
            maxw=220, mini=17, tag=f"rt{i}")
        txt(d, comma(r["dq"]), (c4, y + hh / 2), 27, RED if i == 0 else WHITE, fp=FR,
            maxw=200, mini=17, tag=f"rd{i}")
        y += RH
    y += 14

    d.line([W / 2 - 340, y, W / 2 + 340, y], fill=EDGE, width=2)
    y += 34

    # 三步用法
    txt(d, "这张表怎么用：三步", (W / 2, y), 32, GOLD, maxw=W - 2 * HM, mini=22, tag="u0")
    y += 54
    for i, t in enumerate([
            "① 先看自己的分数落在哪一档",
            "② 数一数这一档有多少所学校、多少个位置",
            "③ 非深户再数一遍：其中 D 类名额有多少个"]):
        txt(d, t, (HM + 34, y), 26, WHITE if i < 2 else RED, fp=FR,
            maxw=W - 2 * HM - 68, mini=17, anchor="lm", tag=f"u{i+1}")
        y += 46
    y += 16

    top = b[0]
    by0, by1 = y, y + 158
    rcard(d, HM, by0, W - HM, by1, rad=14, outline=GOLD, fill=(26, 44, 84))
    txt(d, "分数是门槛，位置是数量", (W / 2, by0 + 44), 32, GOLD,
        maxw=W - 2 * HM - 30, mini=22, tag="hw")
    txt(d, f"580 分以上 {top['n']} 所，招生计划 {comma(top['tot'])} 人，",
        (HM + 34, by0 + 96), 26, WHITE, fp=FR, maxw=W - 2 * HM - 68,
        mini=17, anchor="lm", tag="hw2")
    txt(d, f"其中写明 D 类名额的只有 {comma(top['dq'])} 个",
        (HM + 34, by0 + 134), 26, RED, fp=FR, maxw=W - 2 * HM - 68,
        mini=17, anchor="lm", tag="hw3")

    txt(d, SRC, (W / 2, by1 + 46), 18, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="ft")

    # 口径说明（填实底部 + 把口径写在图上，防被读成"全部公办高中"）
    ny = by1 + 118
    rcard(d, HM, ny, W - HM, ny + 150, rad=14, outline=EDGE, fill=(10, 28, 62))
    txt(d, "口径说明", (HM + 30, ny + 36), 24, LIGHT, fp=FR,
        maxw=W - 2 * HM - 60, mini=17, anchor="lm", tag="ny0")
    for i, t in enumerate([
            "· 分数段按 AC 类住宿录取线划分，非学校综合评价",
            "· 招生计划与 D 类名额取自官方招生计划表，逐校相加",
            "· 覆盖 81 所已公布录取线的公办普高，非全部"]):
        txt(d, t, (HM + 30, ny + 74 + i * 26), 20, SUB, fp=FR,
            maxw=W - 2 * HM - 60, mini=14, anchor="lm", tag=f"ny{i+1}")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > H - 30]
    print(("OK  " if not bad else "!!  ") +
          f"小红书正文图 (末行 y={int(by1 + 46)} / 底部留白 {int(H - by1 - 64)}px)",
          bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-正文图1-{TTL}.png")


if __name__ == "__main__":
    tt_card()
    xhs_cover()
    xhs_card()
    print("ALL DONE")
