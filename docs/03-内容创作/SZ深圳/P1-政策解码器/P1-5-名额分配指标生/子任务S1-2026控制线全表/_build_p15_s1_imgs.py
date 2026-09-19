# -*- coding: utf-8 -*-
"""
P1-5 · S1《2026 控制线全表》四平台配图 · 共 15 张
公众号封面1 + 头条封面3 + 抖音分镜6 + 小红书封面1+正文图4

视觉档：**S1 档 = 深蓝 + 右下「标尺刻度」装饰**（与主线「深靛蓝 + 同心分配环」区分）
主色永远深蓝系不换色相；差异靠深浅 × 光影 × 装饰 × 版式。
安全区：抖音内容右缘≤950、底≤1590。
"""
import time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

# ---- S1 档（深蓝，比主线更深更冷）----
TOP, BOT = (14, 44, 92), (4, 10, 28)
CARD, EDGE = (10, 30, 68), (84, 136, 206)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
RED = (255, 138, 128)

BADS = []
PFX = "P1-5-S1-96所控制线全表"
ROOT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/P1-政策解码器/P1-5-名额分配指标生/子任务S1-2026控制线全表"


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
    gx, gy = w * 0.5, h * 0.06
    radial = np.exp(-(((xx - gx) / (w * 0.58)) ** 2 + ((yy - gy) / (h * 0.30)) ** 2))
    glow = np.array([255, 255, 255], float)[None, None, :]
    img = grad + glow * 0.30 * radial[..., None]
    # 右下「标尺刻度」：一组水平短线，长短交替
    x0, x1 = int(w * 0.62), int(w * 0.99)
    y0, gap, n = int(h * 0.80), max(6, int(h * 0.019)), 9
    for i in range(n):
        yy2 = y0 + i * gap
        if yy2 >= h - 4:
            break
        ln = (x1 - x0) if i % 3 == 0 else ((x1 - x0) * 0.52 if i % 3 == 1 else (x1 - x0) * 0.30)
        band = np.zeros((h, w), float)
        band[max(0, yy2 - 2):yy2 + 2, x0:x0 + int(ln)] = 1.0
        img += glow * 0.16 * band[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def fit(d, text, fp, size, maxw, mini):
    f = font(fp, size)
    while f.size > mini:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1: break
        f = font(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "too long: %s" % text
    return f


def txt(d, text, xy, size, fill, fp=FB, maxw=840, mini=24, anchor="mm", tag=""):
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor=anchor)))


def rcard(d, x0, y0, x1, y1, rad=24):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=CARD, outline=EDGE, width=3)


# ---------- 1. 公众号封面 900×383 ----------
def gzh_cover():
    W, H = 900, 383
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 名额分配控制线", (60, 40), 26, SUB, fp=FR, maxw=780, mini=20, anchor="la", tag="k")
    txt(d, "同一所高中，两条线", (60, 140), 66, WHITE, maxw=800, mini=44, anchor="la", tag="t1")
    txt(d, "D类门槛最高高出43分", (60, 230), 52, WHITE, maxw=800, mini=34, anchor="la", tag="t2")
    txt(d, "96 所公办普高里，79 所 D 类高于 AC 类", (60, 312), 25, GOLD, fp=FR, maxw=800, mini=18, anchor="la", tag="h")
    for t, bb in BADS:
        assert bb[0] >= 30 and bb[2] <= W - 30 and bb[1] >= 24 and bb[3] <= H - 20, (t, bb)
    print("OK 公众号封面"); BADS.clear()
    save_img(im, f"{ROOT}/01.公众号/{PFX}-公众号-封面-精炼版-900x383.png")


# ---------- 2. 头条封面 1200×900 ----------
def tt_cover(fn, badge, title, hook):
    W, H, X0, CAPW = 1200, 900, 80, 1040
    im = base(W, H); d = ImageDraw.Draw(im)
    f = font(FB, 30); tw = d.textlength(badge, font=f)
    d.rounded_rectangle([X0 - 10, 56, X0 + tw + 16, 100], radius=12, fill=(6, 18, 44), outline=(130, 175, 235), width=3)
    d.text((X0, 60), badge, font=f, fill=(210, 232, 255))
    fs, ff = None, None
    for s in range(122, 47, -2):
        c = font(FB, s)
        if max(d.textlength(l, font=c) for l in title) <= CAPW: fs, ff = s, c; break
    assert fs
    hk, hf = None, None
    for s in range(46, 19, -2):
        c = font(FB, s)
        if d.textlength(hook, font=c) <= CAPW: hk, hf = s, c; break
    assert hk
    lh = int(fs * 1.34)
    est = lh * len(title) + 56 + int(hk * 1.6)
    y0 = max((H - est) // 2 - int(fs * 0.25), 130)
    ys = [y0 + i * lh for i in range(len(title))]
    for l, y in zip(title, ys): d.text((X0, y), l, font=ff, fill=WHITE, anchor="la")
    tb = max(d.textbbox((X0, ys[i]), title[i], font=ff, anchor="la")[3] for i in range(len(title)))
    yh = tb + 56
    d.text((X0, yh), hook, font=hf, fill=GOLD, anchor="la")
    hb = d.textbbox((X0, yh), hook, font=hf, anchor="la")
    for i, l in enumerate(title):
        b = d.textbbox((X0, ys[i]), l, font=ff, anchor="la"); assert b[2] <= W - 20 and b[3] <= H - 30, (l, b)
    assert hb[2] <= W - 20 and hb[3] <= H - 30, hb
    print(f"OK 头条 {fn[-28:]} 标题{fs}px 钩子{hk}px")
    save_img(im, f"{ROOT}/02.今日头条/{fn}")


# ---------- 3. 抖音 1080×1920 ----------
WY, HY = 1080, 1920


def dy_header(d, tag):
    f = fit(d, "深圳中考", FB, 92, 820, 72)
    d.text((WY / 2, 130), "深圳中考", font=f, fill=GOLD, anchor="mm")
    bb = d.textbbox((WY / 2, 130), "深圳中考", font=f, anchor="mm"); h = (bb[2] - bb[0]) / 2 + 6
    d.line([WY / 2 - h, 214, WY / 2 + h, 214], fill=GOLD, width=6)
    f2 = font(FB, 40); b2 = d.textbbox((0, 0), tag, font=f2); tw = b2[2] - b2[0]
    d.rounded_rectangle([WY / 2 - tw / 2 - 40, 250, WY / 2 + tw / 2 + 40, 350], radius=50, outline=GOLD, width=3)
    d.text((WY / 2, 300), tag, font=f2, fill=(200, 222, 252), anchor="mm")


def dy_card(i, tag, big, gold, rows, bottom, bigsize=96, bigmini=74):
    im = base(WY, HY); d = ImageDraw.Draw(im)
    dy_header(d, tag)
    txt(d, big, (WY / 2, 640), bigsize, WHITE, maxw=820, mini=bigmini, tag="g")
    if gold:
        txt(d, gold, (WY / 2, 830), 52, GOLD, maxw=820, mini=38, tag="gold")
    y = 968
    for rt, g in rows:
        y1 = y + 150
        rcard(d, 80, y, WY - 80, y1)
        txt(d, rt, (WY / 2, (y + y1) / 2), 46, GOLD if g else WHITE, maxw=800, mini=32, tag="r")
        y = y1 + 24
    if bottom:
        txt(d, bottom, (WY / 2, 1436), 48, WHITE, maxw=820, mini=36, tag="b")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[2] > 952 or bb[1] < 55 or bb[3] > 1592]
    print(("OK  " if not bad else "!!  ") + f"抖音镜头{i:02d}", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03.抖音/{PFX}-抖音-镜头{i:02d}-1080x1920.png")


# ---------- 4. 小红书 1080×1440 ----------
WX, HX, HM = 1080, 1440, 80


def xhs_cover(title, kick, foot):
    im = base(WX, HX); d = ImageDraw.Draw(im)
    f = fit(d, "深圳中考", FB, 96, 1000, 80)
    d.text((WX / 2, 180), "深圳中考", font=f, fill=GOLD, anchor="mm")
    f = fit(d, title, FB, 118, 1000, 82)
    d.text((WX / 2, 560), title, font=f, fill=WHITE, anchor="mm")
    bb = d.textbbox((WX / 2, 560), title, font=f, anchor="mm"); h = (bb[2] - bb[0]) / 2 + 8
    d.line([WX / 2 - h, 704, WX / 2 + h, 704], fill=GOLD, width=8)
    txt(d, kick, (WX / 2, 976), 58, GOLD, maxw=1000, mini=44, tag="kc")
    txt(d, foot, (WX / 2, 1366), 28, SUB, fp=FR, maxw=1000, mini=22, tag="kf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= WX - 20 and bb[3] <= HX - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{PFX}-小红书-封面-1080x1440.png")


def xhs_card(fn, kick, title, sub, tiles, rows, concl, gap=22, minh=104, rowfont=None, rowsgold=None):
    im = base(WX, HX); d = ImageDraw.Draw(im)
    txt(d, kick, (WX / 2, 84), 34, GOLD, maxw=980, mini=26, tag="xk")
    txt(d, title, (WX / 2, 205), 60, WHITE, maxw=1000, mini=42, tag="xt")
    if sub:
        txt(d, sub, (WX / 2, 292), 30, LIGHT, fp=FR, maxw=1000, mini=22, tag="xs")
    MT, MB = 316, 1092
    th = 250 if tiles else 0
    n = len(rows)
    room = (MB - MT) - th - (26 if tiles else 0)
    rh = minh
    if n: rh = max(minh, min((room - (n - 1) * gap) / n, 320))
    y = MT
    if tiles:
        tw, g = 280, 24
        x0 = (WX - (tw * 3 + g * 2)) / 2
        for i, (num, lab) in enumerate(tiles[:3]):
            x = x0 + i * (tw + g)
            rcard(d, x, y, x + tw, y + th, rad=20)
            txt(d, num, (x + tw / 2, y + th * 0.32), 58, GOLD, maxw=tw - 26, mini=34, tag="tile")
            txt(d, lab, (x + tw / 2, y + th * 0.74), 26, SUB, fp=FR, maxw=tw - 24, mini=18, tag="tile")
        y += th + 26
    for i, rt in enumerate(rows):
        y1 = y + rh
        rcard(d, HM, y, WX - HM, y1, rad=22)
        col = WHITE
        if rowsgold and i in rowsgold: col = GOLD
        txt(d, rt, (WX / 2, (y + y1) / 2), rowfont or (38 if rh < 190 else 46), col, maxw=920, mini=24, tag="row")
        y = y1 + (gap if i < n - 1 else 0)
    b0 = 1176
    d.rounded_rectangle([HM - 6, b0, WX - HM + 6, b0 + 118], radius=26, fill=CARD, outline=GOLD, width=4)
    if concl:
        f0 = concl[0]
        txt(d, f0[0], (WX / 2, b0 + 54), 42, GOLD if f0[1] else WHITE, maxw=960, mini=28, tag="band")
    txt(d, "数据来源：深圳市教育局2026年报考指导手册附件2 · 逐行转录", (WX / 2, 1392), 21, SUB, fp=FR, maxw=1000, mini=15, tag="foot")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 18 or bb[1] < 8 or bb[2] > WX - 18 or bb[3] > HX - 8]
    print(("OK  " if not bad else "!!  ") + "小红书 " + fn[-34:], bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{fn}")


if __name__ == "__main__":
    gzh_cover()

    tt_cover(f"{PFX}-头条-封面1-主标题-1200x900.png", "深圳中考 · 名额分配控制线 S1",
             ["同一所高中", "D类门槛高43分"], "96 所里 79 所如此 · 最多 +43 分")
    tt_cover(f"{PFX}-头条-封面2-D比AC高43分-1200x900.png", "深圳中考 · 名额分配控制线 S1",
             ["79 / 96 所", "D类控制线更高"], "深汕实验 454→497 · 布吉中学 449→492")
    tt_cover(f"{PFX}-头条-封面3-全表区间-1200x900.png", "深圳中考 · 名额分配控制线 S1",
             ["AC 447 ~ 570", "D 类 482 ~ 571"], "96 所全表 · 79 所 D 类高于 AC 类")

    dy_card(1, "控制线 · S1", "同一所高中", "D类门槛高43分",
            [("名额分配控制线，不是一条", 0), ("AC 类一条、D 类一条", 1)], "96 所公办普高全表", bigsize=104, bigmini=84)
    dy_card(2, "把它当两条线看", "AC 一条", "D 类一条",
            [("两条线都由官方每年随手册公布", 0), ("D 类考生多、计划少，线本来就更高", 0)], "别拿 AC 的线，去对 D 类的孩子", bigsize=112, bigmini=88)
    dy_card(3, "96 所全表统计", "79 / 96", "所 D 类控制线更高",
            [("持平 13 所", 0), ("D 类更低，只有 4 所", 0)], "不是个例，是普遍规律", bigsize=120, bigmini=96)
    dy_card(4, "差得最狠的", "454 → 497", "深汕实验学校：高 43 分",
            [("布吉中学 449 → 492（+43）", 0), ("深中 570 → 571（只 +1）", 1)], "越往中后段，D 类门槛拉得越开", bigsize=96, bigmini=76)
    dy_card(5, "全表区间", "AC 447 ~ 570", "D 类 482 ~ 571",
            [("AC 类最高：深圳中学 570", 0), ("AC 类最低：8 所并列 447", 0)], "线不用自己算，官方每年随手册公布", bigsize=100, bigmini=80)
    dy_card(6, "查线三步", "先确认类别", "再查对应那一列",
            [("AC 类全表：447 ~ 570", 0), ("控制线与第一批录取线无关", 1)], "关注我 · 下条：深中给哪些初中分了名额", bigsize=104, bigmini=84)

    xhs_cover("同一所高中", "D类门槛高43分 · 不是一条，是两条",
              "深圳中考 · 名额分配控制线 · 收藏不迷路 · 数据2026官方")
    xhs_card(f"{PFX}-小红书-正文图1-两条线-1080x1440.png", "S1 · 核心认知",
             "控制线不是一条，是两条", "同一所高中，AC 类一条、D 类一条",
             None,
             ["AC 类控制线：该校 AC 类考生的资格门槛",
              "D 类控制线：该校 D 类考生的资格门槛",
              "两条线都由官方每年随手册公布，逐年重算"],
             [("96 所公办普高里，79 所的 D 类控制线更高", 1)])
    xhs_card(f"{PFX}-小红书-正文图2-79所更高-1080x1440.png", "S1 · 全表统计",
             "79 / 96 所：D类更高", "把 96 所全拉出来看，差距很集中",
             [("79", "D类更高"), ("13", "持平"), ("4", "D类更低")],
             ["深汕实验学校 454 → 497（+43）",
              "布吉中学 449 → 492（+43）",
              "龙华中学 459 → 501（+42）",
              "深圳中学 570 → 571（+1）"],
             [("越往中后段学校，D 类门槛拉得越开", 1)], gap=14, minh=100, rowfont=36)
    xhs_card(f"{PFX}-小红书-正文图3-全表区间-1080x1440.png", "S1 · 全表区间",
             "AC 447~570 ／ D 482~571", "2026 年 96 所公办普高控制线分布",
             [("570", "AC 最高"), ("447", "AC 最低"), ("96", "所普高")],
             ["AC 类最高：深圳中学 570",
              "AC 类最低：8 所并列 447",
              "D 类最高：深圳中学 571"],
             [("线不用自己算，官方每年随手册公布", 1)])
    xhs_card(f"{PFX}-小红书-正文图4-头部学校控制线-1080x1440.png", "S1 · 收藏资产",
             "头部学校控制线（AC类）", "2026 年官方公布值 · 全表 447~570",
             None,
             ["深圳中学 570", "深圳实验学校（高中部） 568", "深圳市高级中学中心校区 567",
              "深圳外国语学校 566", "红岭中学 563", "宝安中学（集团）高中部 562",
              "育才中学 561", "深圳大学附属中学中心校区 560",
              "全表最低 447（8 所并列）"],
             [("查线看对应那一列：AC 的线不对 D 类的孩子", 1)], gap=8, minh=76, rowfont=32)
    print("ALL DONE")
