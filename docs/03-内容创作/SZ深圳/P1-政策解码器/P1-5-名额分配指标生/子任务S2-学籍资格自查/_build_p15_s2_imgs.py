# -*- coding: utf-8 -*-
"""
P1-5 · S2《学籍资格自查》四平台配图 · 共 15 张
公众号封面1 + 头条封面3 + 抖音分镜6 + 小红书封面1+正文图4 + 自查清单长图1 = 16（含长图）

视觉档：**S2 档 = 蓝系家族第三档**
  主线 = 深靛蓝 TOP(22,56,110) → 右下「同心分配环」
  S1   = 深蓝   TOP(14,44,92)  → 右下「标尺刻度」
  S2   = 中深蓝 TOP(18,52,104) → 右下「勾选框列」(自查感)，光线角度改为**左上方**（主线/S1 均为中上方）

铁律：主色永远深蓝系不换色相；任务间只靠 深浅 × 光影 × 光线角度 × 装饰 × 版式 差异化。
安全区：抖音内容右缘≤950、底≤1590。
"""
import time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

# ---- S2 档 ----
TOP, BOT = (18, 52, 104), (6, 14, 34)
CARD, EDGE = (12, 34, 74), (96, 148, 216)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
TICK = (120, 196, 150)          # 「过」的勾
CROSS = (255, 138, 128)         # 「不过」的叉

BADS = []
PFX = "P1-5-S2-学籍资格自查"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "P1-政策解码器/P1-5-名额分配指标生/子任务S2-学籍资格自查")
SRC = "数据来源：深圳市教育局2026年报考指导手册 · 二、名额分配政策 Q3/Q9"


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
    """蓝系渐变 + 左上主光（S2 的光线角度）+ 右下「勾选框列」装饰。"""
    yv = np.linspace(0, 1, h)[:, None, None]
    grad = (np.array(TOP, float)[None, None, :] * (1 - yv) + np.array(BOT, float)[None, None, :] * yv)
    grad = np.repeat(grad, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    # 主光：左上（区别于主线/S1 的中上方）
    gx, gy = w * 0.24, h * 0.10
    radial = np.exp(-(((xx - gx) / (w * 0.60)) ** 2 + ((yy - gy) / (h * 0.34)) ** 2))
    glow = np.array([255, 255, 255], float)[None, None, :]
    img = grad + glow * 0.28 * radial[..., None]
    # 右下「勾选框列」：一列空心圆角方框，长短边交替，模拟 checklist
    # ⚠️ 安全区双闸：右缘收在 w*0.86（1080 宽 → 929px，避开右侧 1/10 图标区）
    #                下缘收在 min(h-4, h*0.82)（1920 高 → 1574px，避开底部 1/6 字幕区）
    # ⚠️ 矮画布（h<600，如公众号封面 900×383）不出装饰——一列框在矮画布上只落单 1 个，像瑕疵
    bw = max(16, int(w * 0.030))
    x1 = int(w * 0.86)
    x0 = x1 - bw
    ymax = min(h - 4, int(h * (0.82 if h >= 1200 else 0.94)))
    y0, gap, n = int(h * 0.735), int(bw * 1.85), 6
    for i in range(n if h >= 600 else 0):
        yy2 = y0 + i * gap
        if yy2 + bw >= ymax:
            break
        top_ = np.zeros((h, w), float); top_[max(0, yy2 - 2):yy2 + 2, x0:x1] = 1.0
        bot_ = np.zeros((h, w), float); bot_[yy2 + bw - 2:yy2 + bw + 2, x0:x1] = 1.0
        lft = np.zeros((h, w), float); lft[yy2:yy2 + bw, max(0, x0 - 2):x0 + 2] = 1.0
        rgt = np.zeros((h, w), float); rgt[yy2:yy2 + bw, x1 - 2:x1 + 2] = 1.0
        # 每 3 个里有 1 个带"勾"的对角暗示（更亮）
        boost = 0.26 if i % 3 == 1 else 0.13
        img += glow * boost * (top_ + bot_ + lft + rgt)[..., None]
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


def rcard(d, x0, y0, x1, y1, rad=24, outline=None):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=CARD, outline=outline or EDGE, width=3)


# ---------- 1. 公众号封面 900×383 ----------
def gzh_cover():
    W, H = 900, 383
    im = base(W, H); d = ImageDraw.Draw(im)
    # 用户 2026-09-18 改进：主题文字前必须带「指标生资格：」前缀，否则「初中三年不能转学」会被误读为普遍校规
    txt(d, "深圳中考", (60, 44), 26, SUB, fp=FR, maxw=780, mini=20, anchor="la", tag="k")
    txt(d, "指标生资格：", (60, 122), 52, GOLD, maxw=800, mini=36, anchor="la", tag="t0")
    txt(d, "初中三年不能转学", (60, 212), 60, WHITE, maxw=800, mini=40, anchor="la", tag="t1")
    txt(d, "4 条自查，错 1 条就没了", (60, 312), 36, GOLD, maxw=800, mini=24, anchor="la", tag="t2")
    for t, bb in BADS:
        assert bb[0] >= 30 and bb[2] <= W - 30 and bb[1] >= 24 and bb[3] <= H - 20, (t, bb)
    print("OK 公众号封面（含「指标生资格：」前缀）"); BADS.clear()
    save_img(im, f"{ROOT}/01.公众号/{PFX}-公众号-封面-精炼版-900x383.png")


# ---------- 2. 头条封面 1200×900 ----------
def tt_cover(fn, badge, title, hook):
    W, H, X0, CAPW = 1200, 900, 80, 1040
    im = base(W, H); d = ImageDraw.Draw(im)
    f = font(FB, 30); tw = d.textlength(badge, font=f)
    d.rounded_rectangle([X0 - 10, 56, X0 + tw + 16, 100], radius=12, fill=(8, 22, 50), outline=(130, 175, 235), width=3)
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
    print(f"OK 头条 {fn[-30:]} 标题{fs}px 钩子{hk}px")
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


def dy_card(i, tag, big, gold, rows, bottom, bigsize=96, bigmini=74, pre=None):
    """pre: 主题文字前的「定性前缀」行（如「指标生资格：」），用户 2026-09-18 要求首帧必带。"""
    im = base(WY, HY); d = ImageDraw.Draw(im)
    dy_header(d, tag)
    if pre:
        txt(d, pre, (WY / 2, 530), 62, GOLD, maxw=820, mini=46, tag="pre")
        txt(d, big, (WY / 2, 672), bigsize, WHITE, maxw=820, mini=bigmini, tag="g")
    else:
        txt(d, big, (WY / 2, 640), bigsize, WHITE, maxw=820, mini=bigmini, tag="g")
    if gold:
        txt(d, gold, (WY / 2, 846 if pre else 830), 52, GOLD, maxw=820, mini=38, tag="gold")
    y = 968
    for rt, g in rows:
        y1 = y + 150
        # ⚠️ 卡片右缘 944（含 3px 描边后 ≈946 < 950 安全线），不用 WY-80（会伸到 1000 压住图标区）
        rcard(d, 136, y, 944, y1)
        txt(d, rt, (WY / 2, (y + y1) / 2), 44, GOLD if g else WHITE, maxw=720, mini=30, tag="r")
        y = y1 + 24
    if bottom:
        txt(d, bottom, (WY / 2, 1440), 46, WHITE, maxw=820, mini=34, tag="b")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 20 or bb[2] > 952 or bb[1] < 55 or bb[3] > 1592]
    print(("OK  " if not bad else "!!  ") + f"抖音镜头{i:02d}", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/03.抖音/{PFX}-抖音-镜头{i:02d}-1080x1920.png")


# ---------- 4. 小红书 1080×1440 ----------
WX, HX, HM = 1080, 1440, 80


def xhs_cover():
    im = base(WX, HX); d = ImageDraw.Draw(im)
    f = fit(d, "深圳中考", FB, 96, 1000, 80)
    d.text((WX / 2, 190), "深圳中考", font=f, fill=GOLD, anchor="mm")
    txt(d, "指标生资格", (WX / 2, 520), 104, WHITE, maxw=1000, mini=76, tag="ct")
    txt(d, "4 条错 1 条就没了", (WX / 2, 668), 78, WHITE, maxw=1000, mini=56, tag="ct2")
    d.line([WX / 2 - 300, 774, WX / 2 + 300, 774], fill=GOLD, width=8)
    txt(d, "不是看分数，是看学籍", (WX / 2, 940), 58, GOLD, maxw=1000, mini=44, tag="ck")
    txt(d, "初中三年不能转学 · 含完整自查清单", (WX / 2, 1200), 32, SUB, fp=FR, maxw=1000, mini=24, tag="cs")
    txt(d, "深圳中考 · 指标生资格自查 · 收藏不迷路", (WX / 2, 1366), 27, SUB, fp=FR, maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= WX - 20 and bb[3] <= HX - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{PFX}-小红书-封面-1080x1440.png")


def xhs_card(fn, kick, title, sub, tiles, rows, concl, gap=22, minh=104, rowfont=None,
             rowsgold=None, rowmark=None):
    """rowmark: dict{idx: 'tick'|'cross'} → 行首绘制勾／叉标记"""
    im = base(WX, HX); d = ImageDraw.Draw(im)
    txt(d, kick, (WX / 2, 84), 34, GOLD, maxw=980, mini=26, tag="xk")
    txt(d, title, (WX / 2, 205), 58, WHITE, maxw=1000, mini=40, tag="xt")
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
        mk = (rowmark or {}).get(i)
        rcard(d, HM, y, WX - HM, y1, rad=22,
              outline=TICK if mk == "tick" else (CROSS if mk == "cross" else EDGE))
        col = WHITE
        if rowsgold and i in rowsgold: col = GOLD
        cx = WX / 2
        if mk:
            # 行首勾／叉方框
            bs = 46
            bx = HM + 30
            by = (y + y1) / 2 - bs / 2
            d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=10, outline=None,
                                fill=(18, 58, 44) if mk == "tick" else (66, 26, 26))
            if mk == "tick":
                d.line([bx + 11, by + 25, bx + 19, by + 34], fill=TICK, width=6)
                d.line([bx + 19, by + 34, bx + 35, by + 13], fill=TICK, width=6)
            else:
                d.line([bx + 12, by + 12, bx + 34, by + 34], fill=CROSS, width=6)
                d.line([bx + 34, by + 12, bx + 12, by + 34], fill=CROSS, width=6)
            cx = WX / 2 + bs / 2 + 6
        txt(d, rt, (cx, (y + y1) / 2), rowfont or (36 if rh < 190 else 44), col, maxw=880, mini=24, tag="row")
        y = y1 + (gap if i < n - 1 else 0)
    b0 = 1176
    d.rounded_rectangle([HM - 6, b0, WX - HM + 6, b0 + 118], radius=26, fill=CARD, outline=GOLD, width=4)
    if concl:
        f0 = concl[0]
        txt(d, f0[0], (WX / 2, b0 + 54), 40, GOLD if f0[1] else WHITE, maxw=940, mini=26, tag="band")
    txt(d, SRC, (WX / 2, 1392), 21, SUB, fp=FR, maxw=1000, mini=15, tag="foot")
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 18 or bb[1] < 8 or bb[2] > WX - 18 or bb[3] > HX - 8]
    print(("OK  " if not bad else "!!  ") + "小红书 " + fn[-36:], bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{fn}")


# ---------- 5. 小红书 自查清单长图 1080×2400（收藏资产）----------
def xhs_checklist(fn):
    W, H = 1080, 2720
    im = base(W, H); d = ImageDraw.Draw(im)
    txt(d, "深圳中考 · 指标生资格", (W / 2, 110), 38, GOLD, maxw=960, mini=28, tag="lk")
    txt(d, "学籍资格自查清单", (W / 2, 216), 76, WHITE, maxw=1000, mini=56, tag="lt")
    txt(d, "4 条全对才有资格 · 错 1 条就没了", (W / 2, 312), 34, LIGHT, fp=FR, maxw=1000, mini=24, tag="ls")
    d.line([W / 2 - 340, 372, W / 2 + 340, 372], fill=GOLD, width=6)

    # 四条自查（带空勾选框 + 说明）
    items = [
        ("1", "孩子是应届初中毕业生吗？", "往届生不得填报名额分配志愿"),
        ("2", "初中三年是在深圳的初中读的吗？", "在市外初中就读的深圳户籍考生不得填报"),
        ("3", "初一第一学期就在现在这所初中吗？", "初一才转进来的，「一直在」不成立"),
        ("4", "初中三年中间，转过学吗？", "转过一次，三年学籍中断，不成立"),
    ]
    y = 430
    for num, q, note in items:
        h = 250
        rcard(d, 80, y, W - 80, y + h, rad=24)
        # 空勾选框（供家长手勾）
        d.rounded_rectangle([112, y + 86, 182, y + 156], radius=12, outline=GOLD, width=5)
        txt(d, num, (147, y + 121), 40, GOLD, maxw=60, mini=28, tag="n")
        txt(d, q, (610, y + 74), 40, WHITE, maxw=760, mini=26, tag="q")
        txt(d, note, (610, y + 152), 28, SUB, fp=FR, maxw=760, mini=20, tag="note")
        y += h + 24

    # 四种不成立
    y += 26
    txt(d, "另外，这 4 种情况也都不成立", (W / 2, y + 30), 40, GOLD, maxw=900, mini=28, tag="cx")
    y += 92
    for t in ["初一才转进来", "初三转出去", "初二因为搬家转过一次", "在市内跨校转学（不论哪个学期）"]:
        d.rounded_rectangle([80, y, W - 80, y + 104], radius=20, fill=CARD, outline=CROSS, width=3)
        d.line([122, y + 34, 122 + 36, y + 70], fill=CROSS, width=7)
        d.line([122 + 36, y + 34, 122, y + 70], fill=CROSS, width=7)
        txt(d, t, (620, y + 52), 38, WHITE, maxw=740, mini=24, tag="cx2")
        y += 104 + 18

    # 现在做两件事
    y += 30
    txt(d, "现在做 2 件事", (W / 2, y + 34), 44, GOLD, maxw=900, mini=30, tag="ac")
    y += 100
    for t in ["① 向初中学校核对：入学时间 + 有无转学记录",
              "② 留意学校资格公示，名单里没孩子就立刻去问"]:
        d.rounded_rectangle([80, y, W - 80, y + 116], radius=20, fill=CARD, outline=GOLD, width=4)
        txt(d, t, (W / 2, y + 58), 35, WHITE, maxw=880, mini=22, tag="ac2")
        y += 116 + 20

    txt(d, "资格是三年攒出来的 · 初三补不回来", (W / 2, y + 60), 36, GOLD, maxw=940, mini=24, tag="ft")
    txt(d, SRC, (W / 2, H - 66), 22, SUB, fp=FR, maxw=1000, mini=15, tag="foot")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < 18 or bb[1] < 8 or bb[2] > W - 18 or bb[3] > H - 8]
    print(("OK  " if not bad else "!!  ") + "小红书 自查清单长图", bad if bad else "")
    BADS.clear()
    save_img(im, f"{ROOT}/04.小红书/{fn}")


if __name__ == "__main__":
    gzh_cover()

    tt_cover(f"{PFX}-头条-封面1-主标题-1200x900.png", "深圳中考 · 指标生资格 S2",
             ["指标生资格", "4条错1条就没了"], "不是看分数，是看学籍")
    tt_cover(f"{PFX}-头条-封面2-四条自查-1200x900.png", "深圳中考 · 指标生资格 S2",
             ["四条自查", "全对才有资格"], "应届 · 在深圳读 · 初一就在 · 三年没转学")
    tt_cover(f"{PFX}-头条-封面3-四种不成立-1200x900.png", "深圳中考 · 指标生资格 S2",
             ["这 4 种", "都不成立"], "初一转进 · 初三转出 · 初二转学 · 市内跨校")

    dy_card(1, "S2 · 学籍自查", "初中三年 6 个学期", "中间转过一次就没了",
            [("不是看分数", 0), ("是看学籍", 1)], "指标生资格，初中三年不能转学",
            bigsize=88, bigmini=70, pre="指标生资格：")
    dy_card(2, "资格是 3 条", "必须同时满足", "前两条大多天然满足",
            [("① 应届 ② 参加本市中考", 0), ("③ 初一第一学期起连续三年学籍", 1)], "卡人的永远是第 ③ 条", bigsize=96, bigmini=76)
    dy_card(3, "四条自查", "全对才有资格", None,
            [("初一第一学期就在这所初中吗", 0), ("初中三年中间转过学吗", 0)], "错 1 条，志愿填了也无效", bigsize=104, bigmini=84)
    dy_card(4, "这 4 种都不算", "转过一次", "资格就断",
            [("初一转进 · 初三转出", 0), ("初二转学 · 市内跨校", 0)], "不管发生在哪个学期", bigsize=104, bigmini=84)
    dy_card(5, "为什么卡这么严", "防两种现象", "投机性转学 · 挂读",
            [("学籍在一所学校", 0), ("人却在另一所读", 0)], "手册：维护招生公平公正", bigsize=100, bigmini=80)
    dy_card(6, "现在做 2 件事", "今天就查", None,
            [("① 核对入学时间 + 转学记录", 0), ("② 留意学校资格公示", 0)], "转给初一初二家长，还来得及", bigsize=104, bigmini=84)

    xhs_cover()
    xhs_card(f"{PFX}-小红书-正文图1-资格三条-1080x1440.png", "S2 · 核心认知",
             "资格是 3 条，必须同时满足", "手册原文：须同时具备以下条件",
             None,
             ["① 符合当年中考划线录取条件的应届毕业生",
              "② 参加我市当年中考",
              "③ 从初一年级第一学期起一直在报名校就读，且取得该校三年学籍"],
             [("前两条大多天然满足，卡人的是第 ③ 条", 1)])
    xhs_card(f"{PFX}-小红书-正文图2-四条自查-1080x1440.png", "S2 · 逐条自查",
             "对号入座：4 条自查", "空框留给自家孩子，逐条勾",
             None,
             ["1  孩子是应届初中毕业生吗？",
              "2  初中三年是在深圳的初中读的吗？",
              "3  初一第一学期就在现在这所初中吗？",
              "4  初中三年中间，转过学吗？"],
             [("四条全对才有资格，错 1 条就没了", 1)], gap=16, minh=104, rowfont=36)
    xhs_card(f"{PFX}-小红书-正文图3-四种不成立-1080x1440.png", "S2 · 反例",
             "这 4 种，都不成立", "「三年学籍」要的是同一所学校、连续三年",
             None,
             ["初一才转进来", "初三转出去",
              "初二因为搬家转过一次", "在市内跨校转学（不论哪个学期）"],
             [("还有一种更隐蔽的：学籍在一校、人在另一校读（挂读）", 1)],
             gap=16, minh=100, rowfont=38, rowmark={0: "cross", 1: "cross", 2: "cross", 3: "cross"})
    xhs_card(f"{PFX}-小红书-正文图4-现在做两件事-1080x1440.png", "S2 · 行动",
             "现在做 2 件事", "别等初三 —— 资格补不回来",
             [("2", "件事"), ("3", "年积累"), ("0", "次转学")],
             ["① 向初中学校核对：入学时间 + 有无转学记录",
              "② 留意学校资格公示，名单里没孩子就立刻去问",
              "③ 转给身边初一、初二的家长"],
             [("初一初二看到还来得及，初三看到只能后悔", 1)], gap=18, minh=110, rowfont=34)
    xhs_checklist(f"{PFX}-小红书-学籍自查清单长图-1080x2720.png")
    print("ALL DONE")
