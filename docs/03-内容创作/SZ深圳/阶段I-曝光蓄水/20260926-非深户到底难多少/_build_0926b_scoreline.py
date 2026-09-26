# -*- coding: utf-8 -*-
"""20260926 主题B · 2026 公办高中录取线分档 · 配图生成器

- 蓝系家族：沿用 S2 档调色与「左上主光」
- 数据直接**解析 P3-2 终稿**（单一数据源，避免手抄出错）
- 产出：头条微头条配图 1200×900「3 关键数字」+ 小红书封面 1080×1440 + 小红书分档长图 1080×约4500
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

BADS = []
# 配图命名（经营者 2026-09-26 定）：发布日期-平台-文稿类型-标题
# 与「PNG 实体 / md frontmatter images / 本脚本 save_img()」三处同步，勿只改一处
PFX = "20260926"                    # 发布日期
TTL = "2026公办高中录取线分档"        # 标题（与文稿文件名末段一致）
HH_TT, HH_XHS = "1200", "1230"       # 发布时间（与文稿文件名 HHMM 一致）
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20260926-非深户到底难多少")
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


# ---------------- 解析 P3-2 终稿 ----------------
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
        out[name] = (int(c[3]), int(c[4]))       # (AC住宿, D住宿)
    return out


BANDS = [("580 分以上", 580, 999), ("560 – 579", 560, 579), ("540 – 559", 540, 559),
         ("520 – 539", 520, 539), ("500 – 519", 500, 519), ("500 分以下", 0, 499)]


def band_rows(sch):
    res = []
    for lab, lo, hi in BANDS:
        rs = [(n, v[0], v[1]) for n, v in sch.items() if lo <= v[0] <= hi]
        rs.sort(key=lambda r: -r[1])
        res.append((lab, rs))
    return res


# ---------------- 1. 头条微头条配图 1200×900 ----------------
def tt_card():
    sch = load_schools()
    acs = [v[0] for v in sch.values()]
    top, bot = max(acs), min(acs)
    mid = sorted(acs)[len(acs) // 2]
    W, H, HM = 1200, 900, 60
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 2026 录取线", (W / 2, 74), 30, GOLD, maxw=W - 2 * HM, mini=22, tag="tk")
    txt(d, f"公办高中 {len(sch)} 所，录取线差 {top - bot} 分", (W / 2, 168), 52, WHITE,
        maxw=W - 2 * HM, mini=34, tag="tt")
    n, gap = 3, 30
    bw = (W - 2 * HM - gap * (n - 1)) / n
    y0, y1 = 262, 620
    tiles = [(str(bot), f"最低的公办线（{len([a for a in acs if a < 500])} 所在 500 分以下）"),
             (str(mid), "中位：一半学校高过它"), (str(top), "最高（深圳中学）")]
    for i, (num, lab) in enumerate(tiles):
        x = HM + i * (bw + gap)
        rcard(d, x, y0, x + bw, y1, rad=24)
        txt(d, num, (x + bw / 2, y0 + (y1 - y0) * 0.32), 84, GOLD, maxw=bw - 30, mini=48, tag="tn")
        txt(d, lab, (x + bw / 2, y0 + (y1 - y0) * 0.72), 23, SUB, fp=FR,
            maxw=bw - 26, mini=16, tag="tl")
    txt(d, "表格口径：AC 类住宿生录取线", (W / 2, 692), 30, LIGHT, fp=FR,
        maxw=W - 2 * HM, mini=22, tag="tm")
    txt(d, SRC, (W / 2, 848), 20, SUB, fp=FR, maxw=W - 2 * HM, mini=13, tag="tf")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 14 or bb[1] < 6 or bb[2] > W - 14 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + "头条配图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_TT}-今日头条-微头条配图-{TTL}.png")


# ---------------- 2. 小红书封面 1080×1440 ----------------
def xhs_cover():
    sch = load_schools()
    acs = sorted(v[0] for v in sch.values())
    mid = acs[len(acs) // 2]
    W, H = 1080, 1440
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考", (W / 2, 190), 96, GOLD, maxw=1000, mini=80, tag="ct")
    txt(d, "公办高中录取线", (W / 2, 520), 92, WHITE, maxw=1000, mini=68, tag="ct2")
    txt(d, f"{min(acs)} — {max(acs)} 分", (W / 2, 668), 78, GOLD, maxw=1000, mini=56, tag="ct3")
    d.line([W / 2 - 300, 774, W / 2 + 300, 774], fill=GOLD, width=8)
    txt(d, f"{len(sch)} 所全在这，一半高过 {mid} 分", (W / 2, 940), 50, WHITE, maxw=1000, mini=36, tag="ck")
    txt(d, "2026 官方录取线 · 按分数分 6 档", (W / 2, 1200), 32, SUB, fp=FR, maxw=1000, mini=24, tag="cs")
    txt(d, "深圳中考 · 择校必备 · 收藏不迷路", (W / 2, 1366), 27, SUB, fp=FR, maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= W - 20 and bb[3] <= H - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-封面-{TTL}.png")


# ---------------- 3. 小红书分档长图 ----------------
def xhs_long():
    sch = load_schools()
    groups = band_rows(sch)
    W, HM = 1080, 70
    RH, BH, GAP = 54, 62, 16
    HEAD, FOOT = 250, 150
    h = HEAD + sum(BH + len(rs) * RH + GAP for _, rs in groups) + FOOT
    im = base(W, h); d = ImageDraw.Draw(im)
    y = 86
    txt(d, "深圳中考 · 2026", (W / 2, y), 34, GOLD, maxw=W - 2 * HM, mini=24, tag="h1"); y += 66
    txt(d, f"公办高中录取线 · 分 {len(groups)} 档", (W / 2, y), 54, WHITE, maxw=W - 2 * HM, mini=38, tag="h2"); y += 74
    txt(d, "按 AC 类住宿生录取线从高到低排列", (W / 2, y), 28, LIGHT, fp=FR, maxw=W - 2 * HM, mini=20, tag="h3")
    y += 40
    for lab, rs in groups:
        if not rs:
            continue
        rcard(d, HM, y, W - HM, y + BH, rad=14, outline=GOLD)
        txt(d, f"{lab}　·　{len(rs)} 所", (W / 2, y + BH / 2), 36, GOLD, maxw=W - 2 * HM - 30, mini=24, tag="band")
        y += BH
        for i, (name, ac, dc) in enumerate(rs):
            rcard(d, HM, y, W - HM, y + RH - 6, rad=10)
            nm = name if len(name) <= 15 else name[:15] + "…"
            txt(d, nm, (HM + 22, y + (RH - 6) / 2), 30, WHITE, fp=FR,
                maxw=470, mini=20, anchor="lm", tag="nm")
            txt(d, f"AC {ac}", (W - HM - 250, y + (RH - 6) / 2), 30, GOLD, fp=FR,
                maxw=150, mini=20, anchor="rm", tag="ac")
            txt(d, f"D {dc}", (W - HM - 22, y + (RH - 6) / 2), 30, LIGHT, fp=FR,
                maxw=150, mini=20, anchor="rm", tag="dc")
            y += RH
        y += GAP
    txt(d, f"共 {len(sch)} 所公办普通高中（本表覆盖范围以 2026 官方录取标准为准）",
        (W / 2, y + 30), 24, SUB, fp=FR, maxw=W - 2 * HM, mini=17, tag="ft1")
    txt(d, SRC, (W / 2, y + 74), 20, SUB, fp=FR, maxw=W - 2 * HM, mini=14, tag="ft2")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 16 or bb[1] < 6 or bb[2] > W - 16 or bb[3] > h - 6]
    print(("OK  " if not bad else "!!  ") + f"小红书长图 {W}x{h}", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-{HH_XHS}-小红书-长图-{TTL}.png")


if __name__ == "__main__":
    tt_card()
    xhs_cover()
    xhs_long()
    print("ALL DONE")
