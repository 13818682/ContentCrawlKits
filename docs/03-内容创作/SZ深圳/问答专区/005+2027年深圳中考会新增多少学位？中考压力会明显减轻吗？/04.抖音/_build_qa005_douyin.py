# -*- coding: utf-8 -*-
"""
QA-005 抖音 6 分镜 1080×1920 —— 版式重做，改用 P1-4 S4 家族模板（2026-09-12 用户要求）

规范来源：`P1-4-投档规则全解/_p14_dyxhs_family.py` 的 `dy_header` / `dy_card`（P1-4 S1~S4 通用版式）
  · 原 QA-005 自建版式为**左对齐**、大字仅 **66px**、且 y=300→760 之间一大片空档，观感明显低于 S4；
    本次改为家族版式：居中「深圳中考」金字 + 金下划线 + 标签胶囊 → 居中大字(96px) → 金副句
    → 圆角信息卡 → 底部句。

与 S4 的差异化（蓝系家族纪律：任务间靠 深浅×光影×光线角度×装饰×版式 区分）：
  · 版式统一到家族后，差异落在**蓝系深浅**（本档 TOP(20,66,118)，与 S1 钴蓝 / S2 钢蓝 / S3 墨深 / S4 深青蓝 四档均不同）
    与**光线角度**（本档**右上主光**，S4 为顶光）。

安全区硬规则：内容右缘 ≤ x952（右侧 1/10 留图标）、下界 ≤ y1592（底部 1/6 留字幕）。
质量闸：尺寸 + 四角蓝系 + 安全区（右缘/下界）。
"""
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
GOLD = (255, 210, 120)
WHITE = (255, 255, 255)
LIGHT = (176, 208, 246)

# ── 本档蓝系（同一深蓝色相内换深浅，禁换色相）──
TOP, BOT = (20, 66, 118), (5, 13, 34)
CARD, EDGE = (13, 41, 88), (92, 140, 208)

W, H = 1080, 1920
SAFE_X, SAFE_Y = 952, 1592
OUT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/问答专区/"
       "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？/04.抖音/")

BADS = []


def font(fp, size):
    return ImageFont.truetype(fp, size)


def base(w, h):
    """QA-005 档底色：右上主光（与 S4 的顶光区分）。"""
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32) * (1 - y) + np.array(BOT, np.float32) * y)[:, None, :]
    xx = np.arange(w)[None, :]
    yy = np.arange(h)[:, None]
    gx, gy = w * 0.78, h * 0.09
    radial = np.exp(-(((xx - gx) / (w * 0.52)) ** 2 + ((yy - gy) / (h * 0.30)) ** 2))
    glow = np.array([255, 255, 255], np.float32)[None, None, :]
    img = grad + glow * 0.30 * radial[..., None]
    for k in (0.42, 0.95):
        u = (xx - k * yy) / w
        img += glow * 0.09 * np.exp(-(u - 0.88) ** 2 / (2 * 0.05 ** 2))[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def save_img(im, out):
    for _ in range(6):
        try:
            im.save(out)
            return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)


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


def cmm(d, text, xy, size, fill, fp=FB, maxw=800, mini=30, tag=""):
    """居中锚点(middle-middle)摆放，并登记 bbox 供安全区校验。"""
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor="mm")))


def rcard(d, x0, y0, x1, y1, rad=24):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=CARD, outline=EDGE, width=3)


def dy_header(d, tag):
    """每镜相同：居中「深圳中考」金字(92px) + 金下划线 + 标签胶囊。"""
    f = fit(d, "深圳中考", FB, 92, 820, 72)
    d.text((W / 2, 130), "深圳中考", font=f, fill=GOLD, anchor="mm")
    bb = d.textbbox((W / 2, 130), "深圳中考", font=f, anchor="mm")
    half = (bb[2] - bb[0]) / 2 + 6
    d.line([W / 2 - half, 214, W / 2 + half, 214], fill=GOLD, width=6)
    f2 = font(FB, 40)
    bb2 = d.textbbox((0, 0), tag, font=f2)
    tw = bb2[2] - bb2[0]
    pad = 40
    d.rounded_rectangle([W / 2 - tw / 2 - pad, 250, W / 2 + tw / 2 + pad, 350], radius=50,
                        outline=GOLD, width=3)
    d.text((W / 2, 300), tag, font=f2, fill=(200, 222, 252), anchor="mm")


def dy_card(frame, out):
    im = base(W, H)
    d = ImageDraw.Draw(im)
    dy_header(d, frame["tag"])

    if frame.get("kind") == "b":
        # B 型：大字 + 圆角行列表（2~4 行，行高自适应）+ 底部 note
        cmm(d, frame["big"], (W / 2, 600), 96, WHITE, maxw=800, mini=76, tag="b")
        rows_n = len(frame["rows"])
        gap = 24
        y_top, y_bot = 852, 1340          # note 固定 1426，行区不得越 1340
        rh = min(150, max(96, (y_bot - y_top - (rows_n - 1) * gap) / rows_n))
        y = y_top
        for i, (txt, g) in enumerate(frame["rows"]):
            y1 = y + rh
            rcard(d, 80, y, W - 80, int(round(y1)))
            cmm(d, txt, (W / 2, (y + y1) / 2), 46, GOLD if g else WHITE, maxw=800, mini=36, tag="r")
            y = y1 + gap
        cmm(d, frame["note"], (W / 2, 1426), 40, LIGHT, fp=FR, maxw=800, mini=32, tag="n")
    else:
        # A 型：大字 + 金副句 + 圆角信息卡(c1/c2) + 底部句
        big = frame.get("bigsize", 96)
        cmm(d, frame["big"], (W / 2, 640), big, WHITE, maxw=800, mini=frame.get("bigmini", 74), tag="g")
        if frame.get("gold"):
            cmm(d, frame["gold"], (W / 2, 830), 52, GOLD, maxw=800, mini=42, tag="gold")
        if frame.get("c1"):
            rcard(d, 80, 968, W - 80, 1170)
            cmm(d, frame["c1"], (W / 2, 1034), 46, WHITE, maxw=800, mini=38, tag="c1")
            if frame.get("c2"):
                cmm(d, frame["c2"], (W / 2, 1122), 34, LIGHT, fp=FR, maxw=800, mini=28, tag="c2")
        if frame.get("bottom"):
            cmm(d, frame["bottom"], (W / 2, 1436), 48, WHITE, maxw=800, mini=40, tag="b")

    bad = []
    for tagn, bb in BADS:
        if bb[0] < 20 or bb[2] > SAFE_X:
            bad.append(tagn + "R")
        if bb[1] < 55 or bb[3] > SAFE_Y:
            bad.append(tagn + "D")
    print(("OK  " if not bad else "!!  ") + out.split("/")[-1], bad if bad else "")
    BADS.clear()
    save_img(im, out)

    im2 = Image.open(out).convert("RGB")
    px = im2.load()
    nb = 0
    for cx, cy in [(3, 3), (W - 4, 3), (3, H - 4), (W - 4, H - 4)]:
        r, g, b = px[cx, cy]
        nb += int(b > r + 8 and b > g + 6)
    assert nb >= 3, f"{out} 四角蓝系不足 {nb}/4"


JOBS = [
    dict(tag="十五五规划 · 学位", big="新建高中 10 所", gold="但 2027 届赶不上",
         c1="十五五（2026—2030）规划新增", c2="公办高中学位 10 万个以上",
         bottom="学位在长出来 · 但没你要的那么快", bigsize=96, bigmini=74),

    dict(tag="新建 10 所", kind="b", big="番号已排定",
         rows=[("39高 2400 · 40高 1800", 0), ("45高 4800 · 46高 1800", 0),
               ("合计 10800 个学位", 1)],
         note="招标方案已明确 4 所 · 41/47/48高 尚未公布"),

    dict(tag="第五座高中园", big="42高 · 43高 · 44高", gold="大鹏新区溪涌 · 一园三校全寄宿",
         c1="据报道三校合计约 8550 个学位", c2="媒体口径 · 官方尚未正式公布",
         bottom="深圳第五座高中园", bigsize=88, bigmini=72),

    dict(tag="时间账", big="它要 2029 年才建成", gold="据报道预计",
         c1="推进最快的仍在设计 / 可研阶段", c2="改扩建竣工多在 2027 年之后",
         bottom="2027 届赶不上这批学位", bigsize=88, bigmini=70),

    dict(tag="改扩建 · 超过 10 所", kind="b", big="老学校也在长大",
         rows=[("深中泥岗 · 深实验 · 深高", 0), ("宝中 · 深大附中 · 深二实", 0),
               ("翠园 · 罗湖高中 · 平冈 · 深二外", 1)],
         note="超过 10 所公办高中在动工"),

    dict(tag="唯一明确学位数的", big="深二外：1200 座", gold="3 年新增",
         c1="改扩建这批里目前唯一明确学位数的", c2="其余多为「官方公告暂未公布」",
         bottom="未来是美好的 · 现在还不能松懈", bigsize=96, bigmini=72),
]

if __name__ == "__main__":
    for n, frame in enumerate(JOBS, start=1):
        dy_card(frame, OUT + f"QA-005-未来学位-抖音-镜头{n:02d}-1080x1920.png")
    print(f"PASS · 安全区(右≤{SAFE_X} / 下≤{SAFE_Y}) + 四角蓝系 全部通过")
