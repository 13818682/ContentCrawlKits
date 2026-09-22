# -*- coding: utf-8 -*-
"""
QA-006《2026深圳初二生地会考·成绩》· 小红书 清单体版（2026-09-23 发）
================================================================================
产出 6 张，写入本目录下 04.小红书/（均 1080×1440）：
  封面                      —— 9月23日 10:00 开查
  正文卡1-查分三样东西       （清单体）
  正文卡2-这100分的4个作用   （清单体）
  正文卡3-两个最容易误读     （对比体）
  正文卡4-开查当天做3件事    （行动清单）
  尾卡-关注与主页合集        （承接 CTA）

视觉档：**QA-006 档 = 深钢蓝 + 右上主光 + 斜向刻度带**（与公众号/头条同档，
        全平台同任务共用同档，任务间才换档 —— 见 blue-family-visual-rule）

口径：2026-09-22 官方已公布查询日期 = 9月23日上午10:00（成绩查询页温馨提醒原文）
     见 ../00-QA-006-官方口径与历年查分时间核验.md
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "04.小红书")
PFX = "QA-006-生地会考成绩"

WX, HX = 1080, 1440
HM = 80                      # 左右版心边距
FD = "C:/Windows/Fonts/"
FB = FD + "msyhbd.ttc"
FR = FD + "msyh.ttc"

# ---- QA-006 档 ----
TOP, BOT = (20, 46, 96), (6, 16, 36)
CARD, EDGE = (12, 32, 68), (92, 140, 208)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
SRC = "数据来源：深圳市教育局 / 深圳市招生考试办公室 官方公开信息"

CHECKS = []


def font(s, bold=True):
    return ImageFont.truetype(FB if bold else FR, s)


def base(w=WX, h=HX):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    arr = np.repeat(np.array(TOP, np.float32)[None, None, :] * (1 - t)
                    + np.array(BOT, np.float32)[None, None, :] * t, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    gx, gy = w * 0.80, h * 0.12
    dd = np.sqrt(((xx - gx) / (w * 0.58)) ** 2 + ((yy - gy) / (h * 0.36)) ** 2)
    arr = arr + np.array((255, 255, 255), np.float32)[None, None, :] * (np.exp(-dd * dd) * 0.26)[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    # 左下「斜向刻度带」
    n, step_x, step_y = 10, int(w * 0.050), int(h * 0.036)
    L = int(min(w, h) * 0.070)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for i in range(n):
        x0, y0 = int(w * 0.030) + i * step_x, int(h * 0.72) + i * step_y
        if x0 + L > w - 4 or y0 + L > h - 4:
            break
        od.line([(x0, y0), (x0 + L, y0 + L)],
                fill=(GOLD + (44,)) if i % 3 == 1 else (255, 255, 255, 20), width=4)
    im.paste(ov, (0, 0), ov)
    return im


def rcard(im, box, fa=0, outline=None, oa=255, radius=22, width=2):
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if fa:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fa))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (oa,), width=width)
    im.paste(ov, (0, 0), ov)


def put(d, text, xy, size, fill, bold=True, anchor="mm", maxw=None, tag=""):
    f = font(size, bold)
    if maxw:
        while f.size > 12:
            bb = d.textbbox((0, 0), text, font=f)
            if bb[2] - bb[0] <= maxw + 1:
                break
            f = font(f.size - 1, bold)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox((0, 0), text, font=f)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    cx, cy = xy
    if anchor == "mm":
        x0, y0 = cx - bw / 2, cy - bh / 2
    elif anchor == "la":
        x0, y0 = cx, cy
    else:
        x0, y0 = cx - bw / 2, cy
    CHECKS.append((tag or text[:12], (x0, y0, x0 + bw, y0 + bh)))


def gate(name):
    bad = [(t, tuple(round(v) for v in b)) for t, b in CHECKS
           if b[0] < 20 or b[2] > WX - 20 or b[1] < 12 or b[3] > HX - 12]
    print(("OK   " if not bad else "!!   ") + name, bad if bad else "")
    CHECKS.clear()


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, name))
    print("     saved", name, im.size)


# ==================== 封面 ====================
def cover():
    im = base(); d = ImageDraw.Draw(im)
    put(d, "深圳中考", (WX / 2, 176), 96, GOLD, maxw=1000, tag="brand")
    put(d, "生地会考成绩", (WX / 2, 470), 104, WHITE, maxw=1000, tag="t1")
    put(d, "9月23日 10:00 开查", (WX / 2, 626), 88, WHITE, maxw=1000, tag="t2")
    d.line([WX / 2 - 300, 730, WX / 2 + 300, 730], fill=GOLD, width=8)
    put(d, "查分入口 · 3 样东西 · 这 100 分的 4 个作用", (WX / 2, 856), 50, GOLD,
        maxw=980, tag="kick")
    put(d, "不是看分数，是看它怎么被用", (WX / 2, 946), 40, LIGHT, bold=False,
        maxw=980, tag="kick2")
    put(d, "官方已公布 · 详情见图", (WX / 2, 1130), 34, SUB, bold=False, maxw=980, tag="note")
    put(d, "深圳中考 · 问答系列 006 · 关注不迷路", (WX / 2, 1366), 28, SUB, bold=False,
        maxw=1000, tag="foot")
    gate("小红书 封面")
    save(im, f"{PFX}-小红书-封面-1080x1440.png")


# ==================== 正文卡 ====================
def card(fn, kick, title, sub, rows, concl, tiles=None, gap=20, minh=104, rowfont=40,
         rowmark=None):
    im = base(); d = ImageDraw.Draw(im)
    put(d, kick, (WX / 2, 84), 34, GOLD, maxw=980, tag="kick")
    put(d, title, (WX / 2, 202), 58, WHITE, maxw=1000, tag="title")
    if sub:
        put(d, sub, (WX / 2, 286), 30, LIGHT, bold=False, maxw=1000, tag="sub")
    MT, MB = 322, 1086
    th = 244 if tiles else 0
    n = len(rows)
    room = (MB - MT) - th - (24 if tiles else 0)
    rh = max(minh, min((room - (n - 1) * gap) / n, 330)) if n else minh
    y = MT
    if tiles:
        tw, g = 280, 24
        x0 = (WX - (tw * 3 + g * 2)) / 2
        for i, (num, lab) in enumerate(tiles[:3]):
            x = x0 + i * (tw + g)
            rcard(im, [x, y, x + tw, y + th], fa=16, outline=(255, 255, 255), oa=70, radius=20)
            put(d, num, (x + tw / 2, y + th * 0.30), 56, GOLD, maxw=tw - 26, tag="tile-n")
            put(d, lab, (x + tw / 2, y + th * 0.72), 25, SUB, bold=False, maxw=tw - 22, tag="tile-l")
        y += th + 24
    for i, rt in enumerate(rows):
        y1 = y + rh
        mk = (rowmark or {}).get(i)
        rcard(im, [HM, y, WX - HM, y1], fa=16, outline=(255, 255, 255), oa=64, radius=22,
              width=3)
        put(d, rt, (WX / 2, (y + y1) / 2), rowfont, WHITE, maxw=880, tag="row")
        if mk:
            bs = 44
            bx, by = WX - HM - bs - 26, (y + y1) / 2 - bs / 2
            d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=10,
                                outline=None, fill=(66, 26, 26))
            d.line([bx + 11, by + 11, bx + 33, by + 33], fill=(255, 138, 128), width=6)
            d.line([bx + 33, by + 11, bx + 11, by + 33], fill=(255, 138, 128), width=6)
        y = y1 + (gap if i < n - 1 else 0)
    rcard(im, [HM - 6, 1152, WX - HM + 6, 1270], fa=16, outline=GOLD, radius=26, width=4)
    put(d, concl, (WX / 2, 1211), 40, GOLD, maxw=920, tag="band")
    put(d, SRC, (WX / 2, 1348), 21, SUB, bold=False, maxw=1000, tag="foot")
    gate("小红书 " + fn[-30:])
    save(im, fn)


# ==================== 尾卡（承接 CTA） ====================
def tail():
    im = base(); d = ImageDraw.Draw(im)
    put(d, "深圳中考", (WX / 2, 176), 96, GOLD, maxw=1000, tag="brand")
    put(d, "分数查到了，", (WX / 2, 470), 76, WHITE, maxw=1000, tag="t1")
    put(d, "接下来怎么用？", (WX / 2, 574), 76, WHITE, maxw=1000, tag="t2")
    d.line([WX / 2 - 260, 668, WX / 2 + 260, 668], fill=GOLD, width=8)
    rcard(im, [HM, 736, WX - HM, 1004], fa=16, outline=GOLD, radius=26, width=4)
    put(d, "这 100 分的 4 个作用", (WX / 2, 800), 42, GOLD, maxw=880, tag="b1")
    put(d, "① 没它不能投档　② 同分先比它", (WX / 2, 872), 36, WHITE, maxw=880, tag="b2")
    put(d, "③ 指标生批同样适用　④ 缺考可补考", (WX / 2, 932), 36, WHITE, maxw=880, tag="b3")
    put(d, "（详见主页合集「志愿规则」）", (WX / 2, 1180), 34, SUB, bold=False, maxw=920, tag="n1")
    put(d, "关注我，下一条讲：生地分数怎么和选校挂钩", (WX / 2, 1258), 36, GOLD,
        maxw=960, tag="cta")
    put(d, "深圳中考 · 问答系列 006", (WX / 2, 1366), 28, SUB, bold=False, maxw=1000, tag="foot")
    gate("小红书 尾卡")
    save(im, f"{PFX}-小红书-尾卡-关注与合集-1080x1440.png")


if __name__ == "__main__":
    cover()
    card(f"{PFX}-小红书-正文图1-查分三样东西-1080x1440.png",
         "006 · 查分",
         "怎么查？1 个入口 + 3 样东西",
         "9月23日 10:00 一到就填，别临到点才翻",
         ["① 11 位考生号（报名时分配的）",
          "② 身份证件号后 6 位（有字母填大写）",
          "③ 验证码（页面会显示）"],
         "入口：深圳招考网 → 招考服务 → 初二学考成绩查询",
         gap=22, minh=132, rowfont=40)
    card(f"{PFX}-小红书-正文图2-四个作用-1080x1440.png",
         "006 · 核心",
         "这 100 分的 4 个作用",
         "不计入中考总分，却是门槛 + 决胜分",
         ["① 有成绩才能投档",
          "② 同分比较第一层，比语数英优先",
          "③ 名额分配批（指标生）同样适用",
          "④ 缺考可补考，但缺考当年不能投档"],
         "「不计分」≠「可以不考」",
         gap=18, minh=112, rowfont=38)
    card(f"{PFX}-小红书-正文图3-两个误读-1080x1440.png",
         "006 · 别踩坑",
         "两个最容易误读的说法",
         "家长群里传得最多，也错得最多",
         ["「不计分，所以不用管」",
          "「考完就彻底定格了，没救」"],
         "没有成绩 = 当年不能投档",
         gap=26, minh=180, rowfont=42, rowmark={0: "cross", 1: "cross"})
    card(f"{PFX}-小红书-正文图4-当天做三件事-1080x1440.png",
         "006 · 行动",
         "开查当天做这 3 件事",
         "9月23日 10:00 开查",
         ["① 今晚就把考生号和身份证后 6 位备好",
          "② 查到分数立刻记下，并截图核对",
          "③ 关注我：分数怎么用，我接着讲"],
         "官方已公布 · 以招考办公告为准",
         tiles=[("23", "9月开查日"), ("100", "满分"), ("3", "样东西")],
         gap=20, minh=110, rowfont=36)
    tail()
    print("ALL DONE (小红书)")
