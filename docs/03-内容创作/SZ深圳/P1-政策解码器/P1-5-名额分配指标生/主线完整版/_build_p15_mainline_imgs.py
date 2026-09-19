# -*- coding: utf-8 -*-
"""
P1-5《名额分配：50%指标到校，校内竞争怎么玩》主线完整版 · 四平台配图生成
共 15 张：公众号封面1 + 头条封面3 + 抖音分镜6 + 小红书封面1+正文图4

视觉档：**深靛蓝**（与 P1-4 主线 navy(27,58,92) 区分）
  TOP(22,56,110) → BOT(6,14,38)，顶光 + 右下角同心「分配环」装饰（象征名额下到各初中）
蓝系家族铁律：只换深浅/光影/装饰/版式，不换色相。
安全区：抖音内容右缘≤950、底≤1590；所有文字带越界断言。
"""
import time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

# ---- P1-5 深靛蓝档（主线专用，勿与其他任务复用同档）----
TOP   = (22, 56, 110)
BOT   = (6, 14, 38)
CARD  = (12, 34, 76)
EDGE  = (92, 144, 214)
GOLD  = (255, 210, 120)
WHITE = (255, 255, 255)
LIGHT = (176, 208, 246)
SUB   = (214, 230, 252)

BADS = []


def font(fp, size):
    return ImageFont.truetype(fp, size)


def save_img(im, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for _ in range(6):
        try:
            im.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)


def base(w, h):
    """深靛蓝底：顶光垂直渐变 + 右下角同心分配环。"""
    yv = np.linspace(0, 1, h)[:, None, None]
    grad = (np.array(TOP, float)[None, None, :] * (1 - yv) + np.array(BOT, float)[None, None, :] * yv)
    grad = np.repeat(grad, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    gx, gy = w * 0.5, h * 0.06
    radial = np.exp(-(((xx - gx) / (w * 0.58)) ** 2 + ((yy - gy) / (h * 0.30)) ** 2))
    glow = np.array([255, 255, 255], float)[None, None, :]
    img = grad + glow * 0.30 * radial[..., None]
    # 右下同心分配环
    cx, cy = w * 0.94, h * 0.98
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    for k in (0.30, 0.46, 0.62, 0.78):
        ring = np.exp(-((r - k * max(w, h) * 0.30) ** 2) / (2 * (w * 0.006) ** 2))
        img += glow * 0.10 * ring[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def fit(d, text, fp, size, maxw, mini):
    f = font(fp, size)
    while f.size > mini:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = font(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "too long: %s" % text
    return f


def txt(d, text, xy, size, fill, fp=FB, maxw=840, mini=24, anchor="mm", tag=""):
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor=anchor)))


def rcard(d, x0, y0, x1, y1, rad=24, fill=None, edge=None, width=3):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad,
                        fill=fill if fill is not None else CARD,
                        outline=edge if edge is not None else EDGE, width=width)


ROOT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/P1-政策解码器/P1-5-名额分配指标生/主线完整版"
PFX = "P1-5-名额分配：50%指标到校，校内竞争怎么玩"


# ============ 1. 公众号封面 900×383（精简版：小标 → 单行大标题 → 金句）============
def gzh_cover():
    W, H = 900, 383
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 名额分配", (60, 40), 26, SUB, fp=FR, maxw=780, mini=20,
        anchor="la", tag="kick")
    txt(d, "深中1002个学位", (60, 140), 74, WHITE, maxw=800, mini=46, anchor="la", tag="t1")
    txt(d, "不在全市抢，在初中里抢", (60, 230), 44, WHITE, maxw=800, mini=32, anchor="la", tag="t2")
    txt(d, "1002 ÷ 1980 ≈ 50.6% · 控制线 570 比正取线低 22 分", (60, 312), 25, GOLD,
        fp=FR, maxw=800, mini=18, anchor="la", tag="hook")
    for t, bb in BADS:
        assert bb[0] >= 30 and bb[2] <= W - 30 and bb[1] >= 24 and bb[3] <= H - 20, (t, bb)
    print("OK 公众号封面", BADS and ""); BADS.clear()
    save_img(im, f"{ROOT}/01.公众号/{PFX}-公众号-封面-精炼版-900x383.png")


# ============ 2. 头条封面 1200×900 ×3（角标 → 白大字(≤2行) → 黄钩）============
def tt_cover(fn, badge, title, hook):
    W, H, X0, CAPW = 1200, 900, 80, 1040
    im = base(W, H); d = ImageDraw.Draw(im)
    f = font(FB, 30); tw = d.textlength(badge, font=f)
    d.rounded_rectangle([X0 - 10, 56, X0 + tw + 16, 100], radius=12,
                        fill=(6, 18, 44), outline=(130, 175, 235), width=3)
    d.text((X0, 60), badge, font=f, fill=(210, 232, 255))
    fs, ff = None, None
    for s in range(122, 47, -2):
        cand = font(FB, s)
        if max(d.textlength(ln, font=cand) for ln in title) <= CAPW:
            fs, ff = s, cand; break
    assert fs, "大标题无可行字号"
    hk, hf = None, None
    for s in range(46, 19, -2):
        cand = font(FB, s)
        if d.textlength(hook, font=cand) <= CAPW:
            hk, hf = s, cand; break
    assert hk
    lh = int(fs * 1.34)
    est = lh * len(title) + 56 + int(hk * 1.6)
    y0 = max((H - est) // 2 - int(fs * 0.25), 130)
    ys = [y0 + i * lh for i in range(len(title))]
    for ln, yy in zip(title, ys):
        d.text((X0, yy), ln, font=ff, fill=WHITE, anchor="la")
    tb = max(d.textbbox((X0, ys[i]), title[i], font=ff, anchor="la")[3] for i in range(len(title)))
    yh = tb + 56
    d.text((X0, yh), hook, font=hf, fill=GOLD, anchor="la")
    hb = d.textbbox((X0, yh), hook, font=hf, anchor="la")
    for i, ln in enumerate(title):
        b = d.textbbox((X0, ys[i]), ln, font=ff, anchor="la")
        assert b[2] <= W - 20 and b[3] <= H - 30, (ln, b)
    assert hb[2] <= W - 20 and hb[3] <= H - 30, hb
    print(f"OK 头条 {fn} 标题{fs}px 钩子{hk}px")
    save_img(im, f"{ROOT}/02.今日头条/{fn}")


# ============ 3. 抖音分镜 1080×1920 ×6（顶「深圳中考」金字 + 信息卡）============
WY, HY = 1080, 1920


def dy_header(d, tag):
    f = fit(d, "深圳中考", FB, 92, 820, 72)
    d.text((WY / 2, 130), "深圳中考", font=f, fill=GOLD, anchor="mm")
    bb = d.textbbox((WY / 2, 130), "深圳中考", font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 6
    d.line([WY / 2 - half, 214, WY / 2 + half, 214], fill=GOLD, width=6)
    f2 = font(FB, 40); bb2 = d.textbbox((0, 0), tag, font=f2); tw = bb2[2] - bb2[0]
    d.rounded_rectangle([WY / 2 - tw / 2 - 40, 250, WY / 2 + tw / 2 + 40, 350],
                        radius=50, outline=GOLD, width=3)
    d.text((WY / 2, 300), tag, font=f2, fill=(200, 222, 252), anchor="mm")


def dy_card(i, tag, big, gold, rows, bottom, bigsize=96, bigmini=74):
    im = base(WY, HY); d = ImageDraw.Draw(im)
    dy_header(d, tag)
    txt(d, big, (WY / 2, 640), bigsize, WHITE, maxw=820, mini=bigmini, tag="g")
    if gold:
        txt(d, gold, (WY / 2, 830), 52, GOLD, maxw=820, mini=40, tag="gold")
    y = 968
    for rtxt, g in rows:
        y1 = y + 150
        rcard(d, 80, y, WY - 80, y1)
        txt(d, rtxt, (WY / 2, (y + y1) / 2), 46, GOLD if g else WHITE, maxw=800, mini=34, tag="r")
        y = y1 + 24
    if bottom:
        txt(d, bottom, (WY / 2, 1436), 48, WHITE, maxw=820, mini=38, tag="b")
    bad = []
    for t, bb in BADS:
        if bb[0] < 20 or bb[2] > 952 or bb[1] < 55 or bb[3] > 1592:
            bad.append((t, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + f"抖音镜头{i:02d}", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03.抖音/{PFX}-抖音-镜头{i:02d}-1080x1920.png")


# ============ 4. 小红书 1080×1440（封面 + 正文卡）============
WX, HX, HM = 1080, 1440, 80


def xhs_cover(title, kick, foot):
    im = base(WX, HX); d = ImageDraw.Draw(im)
    f = fit(d, "深圳中考", FB, 96, 1000, 80)
    d.text((WX / 2, 180), "深圳中考", font=f, fill=GOLD, anchor="mm")
    f = fit(d, title, FB, 118, 1000, 90)
    d.text((WX / 2, 560), title, font=f, fill=WHITE, anchor="mm")
    bb = d.textbbox((WX / 2, 560), title, font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 8
    d.line([WX / 2 - half, 704, WX / 2 + half, 704], fill=GOLD, width=8)
    txt(d, kick, (WX / 2, 976), 62, GOLD, maxw=1000, mini=46, tag="kc")
    txt(d, foot, (WX / 2, 1366), 28, SUB, fp=FR, maxw=1000, mini=22, tag="kf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= WX - 20 and bb[3] <= HX - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{PFX}-小红书-封面-1080x1440.png")


def xhs_card(fn, kick, title, sub, tiles, rows, concl, gap=22, minh=104, rowfont=None):
    im = base(WX, HX); d = ImageDraw.Draw(im)
    txt(d, kick, (WX / 2, 84), 34, GOLD, maxw=980, mini=26, tag="xk")
    txt(d, title, (WX / 2, 205), 62, WHITE, maxw=1000, mini=44, tag="xt")
    if sub:
        txt(d, sub, (WX / 2, 292), 30, LIGHT, fp=FR, maxw=1000, mini=22, tag="xs")
    MT, MB = 316, 1092
    tiles_h = 250 if tiles else 0
    n = len(rows)
    room = (MB - MT) - tiles_h - (26 if tiles else 0)
    rh = minh
    if n:
        rh = max(minh, min((room - (n - 1) * gap) / n, 320))
    y = MT
    if tiles:
        tw, g = 280, 24
        x0 = (WX - (tw * 3 + g * 2)) / 2
        for i, (num, lab) in enumerate(tiles[:3]):
            x = x0 + i * (tw + g)
            rcard(d, x, y, x + tw, y + tiles_h, rad=20)
            txt(d, num, (x + tw / 2, y + tiles_h * 0.32), 60, GOLD, maxw=tw - 26, mini=40, tag="tile")
            txt(d, lab, (x + tw / 2, y + tiles_h * 0.74), 26, SUB, fp=FR, maxw=tw - 24, mini=18, tag="tile")
        y += tiles_h + 26
    for i, rtxt in enumerate(rows):
        y1 = y + rh
        rcard(d, HM, y, WX - HM, y1, rad=22)
        fs_row = rowfont or (38 if rh < 190 else 46)
        txt(d, rtxt, (WX / 2, (y + y1) / 2), fs_row, WHITE, maxw=920, mini=24, tag="row")
        y = y1 + (gap if i < n - 1 else 0)
    b0 = 1176
    d.rounded_rectangle([HM - 6, b0, WX - HM + 6, b0 + 118], radius=26, fill=CARD, outline=GOLD, width=4)
    if concl:
        first = concl[0]
        txt(d, first[0], (WX / 2, b0 + 54), 44, GOLD if first[1] else WHITE, maxw=960, mini=30, tag="band")
    txt(d, "数据来源：深圳市教育局2026年报考指导手册附件2 · 人工核对", (WX / 2, 1392), 21, SUB,
        fp=FR, maxw=1000, mini=15, tag="foot")
    bad = []
    for t, bb in BADS:
        if bb[0] < 18 or bb[1] < 8 or bb[2] > WX - 18 or bb[3] > HX - 8:
            bad.append((t, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + "小红书 " + fn, bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{fn}")


if __name__ == "__main__":
    # ---- 1. 公众号封面 ----
    gzh_cover()

    # ---- 2. 头条封面 3 张 ----
    tt_cover(f"{PFX}-头条-封面1-主标题-1200x900.png",
             "深圳中考 · 名额分配 P1-5",
             ["深中1002个学位", "不在全市抢"],
             "1002 ÷ 1980 ≈ 50.6%，一半名额下到各初中")
    tt_cover(f"{PFX}-头条-封面2-控制线对比表-1200x900.png",
             "深圳中考 · 名额分配 P1-5",
             ["同一所学校", "两条线差22分"],
             "深中 正取线592 · 指标生控制线570")
    tt_cover(f"{PFX}-头条-封面3-案例-1200x900.png",
             "深圳中考 · 名额分配 P1-5",
             ["571分，达线却落选"],
             "布吉中学3个名额，5个人抢")

    # ---- 3. 抖音分镜 6 张 ----
    dy_card(1, "名额分配 · P1-5", "深中一半学位", "不在全市抢",
            [("1002个名额  ÷  1980个计划", 0), ("≈ 50.6% 分到各初中", 1)],
            "只和你孩子同校的同学抢", bigsize=110, bigmini=86)
    dy_card(2, "它叫什么", "名额分配", "家长叫它：指标生",
            [("公办普高拿出 50% 招生计划", 0), ("按考生人数比例下到每所初中", 0)],
            "深中：1002人走这条路，不走全市统招", bigsize=112, bigmini=88)
    dy_card(3, "在哪竞争", "不在全市", "在你孩子那所初中",
            [("全市竞争 ❌", 0), ("校内竞争 ✅", 1)],
            "同一所高中，不同初中的难度完全不同", bigsize=112, bigmini=88)
    dy_card(4, "门槛① 学籍", "初中三年", "必须同一所学校",
            [("初一转进 → 不算", 0), ("初三转出 → 不算", 0)],
            "从市外转入：须初三第一学期起已在该校", bigsize=110, bigmini=86)
    dy_card(5, "门槛② 分数", "深中控制线 570", "正取线 592，差 22 分",
            [("控制线由官方每年公布，不用自己算", 0), ("深中：AC 类 570 ／ D 类 571", 1)],
            "AC 类 447~570 ／ D 类 482~571（96所）", bigsize=96, bigmini=76)
    dy_card(6, "真实案例", "571分，也落选", "布吉中学 3 个名额，5 人抢",
            [("588 / 579 / 573 → 录取", 0), ("571 达线但名额满 → 落选", 1)],
            "关注我 · 下条：指标生怎么填才不浪费", bigsize=104, bigmini=84)

    # ---- 4. 小红书 封面 + 4 正文卡 ----
    xhs_cover("深中1002个学位", "不在全市抢 · 在你孩子初中里抢",
              "深圳中考 · 名额分配 · 收藏不迷路 · 数据2026官方")
    xhs_card(f"{PFX}-小红书-正文图1-1002除以1980-1080x1440.png",
             "P1-5 · 核心数字",
             "1002 ÷ 1980 ≈ 50.6%", "深中一半学位不走全市统招",
             [("1002", "名额分配人数"), ("1980", "招生计划总数"), ("50.6%", "下到各初中")],
             ["公办普高拿出 50% 招生计划，按考生人数比例分到每一所初中"],
             [("这半数学位，竞争范围是校内，不是全市", 1)])
    xhs_card(f"{PFX}-小红书-正文图2-2026控制线区间-1080x1440.png",
             "P1-5 · 控制线",
             "2026 年控制线区间", "官方每年随手册公布，不用自己算",
             [("570", "AC最高·深中"), ("516", "AC中位数"), ("447", "AC最低")],
             ["深中 AC 类 570 ／ D 类 571（仅差 1 分）",
              "AC 类区间 447 ~ 570，中位 516",
              "D 类区间 482 ~ 571，中位 524"],
             [("96 所全表见 S1《名额分配控制线全表》", 1)])
    xhs_card(f"{PFX}-小红书-正文图3-8校控制线对比表-1080x1440.png",
             "P1-5 · 收藏资产",
             "8 所头部学校：差多少", "正取线 vs 名额分配控制线（2026·AC类）",
             None,
             ["深圳中学 592 / 570 → 差 22",
              "深实验高中部 590 / 568 → 差 22",
              "深圳外国语 587 / 566 → 差 21",
              "深高中心校区 587 / 567 → 差 20",
              "红岭中学 584 / 563 → 差 21",
              "宝安中学 583 / 562 → 差 21",
              "深圳科学高中 579 / 558 → 差 21",
              "南山外国语 579 / 555 → 差 24"],
             [("头部学校差距全在 20~24 分，不跟题目难易走", 1)],
             gap=10, minh=86, rowfont=36)
    xhs_card(f"{PFX}-小红书-正文图4-布吉中学3名额5人争-1080x1440.png",
             "P1-5 · 真实场景",
             "571分，达线也落选", "布吉中学 3 个名额，5 人填报",
             None,
             ["小张 588 → 录取",
              "小王 579 → 录取",
              "小李 573 → 录取",
              "小陈 571 → 达线，但名额已满，落选",
              "小赵 566 → 未达控制线"],
             [("571分在别的初中也许稳进，这里就是第4名", 1)])
    print("ALL DONE")
