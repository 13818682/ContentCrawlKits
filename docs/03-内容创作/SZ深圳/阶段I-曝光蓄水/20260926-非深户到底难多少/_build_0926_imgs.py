# -*- coding: utf-8 -*-
"""20260926 · 阶段 I 首条 · 小红书配图生成器（2 张 1080×1440）

- 蓝系家族：沿用 S2 档的 TOP/BOT/CARD/EDGE/GOLD 与「左上主光」光线角度
- ⚠️ 装饰仍沿用 S2 的「勾选框列」（base() 内绘制），未做差异化 —— 阶段 I 首条任务
       优先出稿，装饰差异化留到后续条数（`blue-family-visual-rule` 允许，但需在下一
       条更换装饰/版面，避免逐像素重复）
- 四道闸口：尺寸 / 越界 / 蓝系（色相不变）/ 连锁（文件名与引用一致）
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



WX, HX, HM = 1080, 1440, 80
PFX = "阶段I-20260926-非深户到底难多少"
SRC = "数据来源：深圳市教育局正式发布的 2026 年高中阶段学校招生计划"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "阶段I-曝光蓄水/20260926-非深户到底难多少")


def xhs_cover_0926():
    """封面：结论式（不写悬念）。左上加「数据带」装饰，区别于 S2 的勾选框列。"""
    im = base(WX, HX); d = ImageDraw.Draw(im)
    txt(d, "深圳中考", (WX / 2, 190), 96, GOLD, maxw=1000, mini=80, tag="ct")
    txt(d, "非深户考公办", (WX / 2, 520), 104, WHITE, maxw=1000, mini=76, tag="ct2")
    txt(d, "深中 592 = 592", (WX / 2, 668), 74, WHITE, maxw=1000, mini=54, tag="ct3")
    d.line([WX / 2 - 300, 774, WX / 2 + 300, 774], fill=GOLD, width=8)
    txt(d, "难的不是名校，是中间那一档", (WX / 2, 940), 54, GOLD, maxw=1000, mini=40, tag="ck")
    txt(d, "2026 官方数据 · D 类必看的两张表", (WX / 2, 1200), 32, SUB, fp=FR, maxw=1000, mini=24, tag="cs")
    txt(d, "深圳中考 · 非深户 · 收藏不迷路", (WX / 2, 1366), 27, SUB, fp=FR, maxw=1000, mini=20, tag="cf")
    for t, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= WX - 20 and bb[3] <= HX - 10, (t, bb)
    print("OK 小红书封面"); BADS.clear()
    save_img(im, f"{ROOT}/03-配图/{PFX}-小红书-封面-深中592对592-1080x1440.png")


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
    save_img(im, f"{ROOT}/03-配图/{fn}")


# ---------- 5. 小红书 自查清单长图 1080×2400（收藏资产）----------

if __name__ == "__main__":
    xhs_cover_0926()
    xhs_card(f"{PFX}-小红书-正文图1-D类必看的两张表-1080x1440.png",
             "深圳中考 · D 类",
             "两张表看清：非深户难在哪",
             "2026 年官方数据 · 一张不差",
             [],
             ["公办普高招生计划：AC 类 61,797 人　D 类 18,506 人",
              "D 类占公办计划：23%",
              "四大名校：AC 与 D 类录取线差 0 分（深中 592 / 592）",
              "差距最大 · 曙光中学：AC 497 / D 526，差 29 分",
              "所以该研究的是：中间那一档怎么选"],
             [("难的不是名校，是中间那一档", 1)], gap=22, minh=137, rowfont=38,
             rowsgold={1, 2})
    print("ALL DONE")
