# -*- coding: utf-8 -*-
"""
深圳中考 · 问答系列 · 004 公众号配图生成脚本（900 系列）
风格：P1-2「主线精简版」极简排版风（2026-09-05 用户指定）
  - 深蓝渐变 TOP(27,58,92)→BOT(13,30,48) + 顶部柔光 + 两处柔和椭圆
  - 白/金/浅蓝三色排版，无徽章胶囊、无装饰纹理；金线/细线分隔
产出 7 张：公众号配图-首图/章节条1-3/数据卡1-3
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
DIM = (96, 122, 158)


def base(w, h, gx=0.5, gy=0.18):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    g = np.exp(-(((x - w * gx) / (w * 0.32)) ** 2 + ((y - h * gy) / (h * 0.34)) ** 2))
    a = a + np.array((185, 208, 235), float)[None, None, :] * (g * 0.11)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-w * .18, -h * .08, w * .24, h * .16], fill=TOP + (34,))
    od.ellipse([w * .80, h * .82, w * 1.1, h * 1.04], fill=TOP + (20,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, size, fill, w, bold=True, maxw=None):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else w - 120
    while f.size > 14:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


def vline(d, y, x0=120, x1=780, color=DIM, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def seqline(d, parts, cy, size, w=900, maxw=None):
    """一行内分段着色居中排版：parts=[(text, fill, bold), ...]"""
    mw = maxw if maxw else w - 100
    s = size
    while s > 14:
        total = 0
        fonts = []
        for txt, _fill, bold in parts:
            f = ImageFont.truetype(FB if bold else FR, s)
            fonts.append(f)
            total += d.textlength(txt, font=f)
        if total <= mw + 1:
            break
        s -= 1
    x = (w - total) / 2
    for (txt, fill, bold), f in zip(parts, fonts):
        d.text((x, cy), txt, font=f, fill=fill, anchor="lm")
        x += d.textlength(txt, font=f)
    return s


# 首图 900×383 —— 以完整问题为主文案，简化风格、突出点击钩子
def wx_cover():
    w, h = 900, 383
    im, d = base(w, h, 0.5, 0.18)
    put(d, "深圳中考 · 问答004", (450, 40), 28, GOLD, w)
    put(d, "非深户想让孩子以深户身份中考", (450, 150), 46, WHITE, w)
    seqline(d, [("最迟几年级", GOLD, True), ("开始办户口？", WHITE, True)], 226, 46)
    d.line([(450 - 120, 270), (450 + 120, 270)], fill=GOLD, width=3)
    put(d, "决定赛道的是户口 · 越早规划越主动", (450, 308), 24, LIGHT, w, False)
    return im


def wx_section(tag, title, sub):
    w, h = 900, 220
    im, d = base(w, h, 0.5, 0.16)
    put(d, tag, (450, 58), 26, GOLD, w)
    put(d, title, (450, 130), 44, WHITE, w)
    put(d, sub, (450, 186), 22, LIGHT, w, False)
    return im


def cell(d, text, xc, y, size, fill, maxw, w=900, bold=True):
    put(d, text, (xc, y), size, fill, w, bold, maxw)


# 数据卡1：赛道账
def wx_card_track():
    w, h = 900, 400
    im, d = base(w, h, 0.5, 0.20)
    put(d, "AC vs D · 赛道差异在哪", (450, 50), 32, WHITE, w)
    hd = [("对比项", 200), ("AC类 · 深户", 500), ("D类 · 非深户", 730)]
    for t, x in hd:
        cell(d, t, x, 122, 22, SUB, 300)
    vline(d, 152)
    rows = [
        ("考生占比", "约46%", "约54%", WHITE, GOLD),
        ("公办普高名额", "约77%", "约23%", WHITE, GOLD),
        ("中下游录取线", "AC类基准", "高13-31分", WHITE, GOLD),
    ]
    ys = [210, 272, 334]
    for (lab, ac, dc, ca, cd), y in zip(rows, ys):
        cell(d, lab, 200, y, 24, WHITE, 240)
        cell(d, ac, 500, y, 26, ca, 300)
        cell(d, dc, 730, y, 26, cd, 300)
    put(d, "※ D类=非深户：四大名校AC/D持平 · 越往下差距越明显", (450, 376), 18, SUB, w, False)
    return im


# 数据卡2：截止对号
def wx_card_deadline():
    w, h = 900, 400
    im, d = base(w, h, 0.5, 0.20)
    put(d, "户口最迟要什么时候办好", (450, 56), 34, WHITE, w)
    put(d, "3月报名前，落到孩子头上", (450, 164), 48, GOLD, w)
    put(d, "考生类别按当年户口簿核验 · 报名在初三下3月下旬", (450, 236), 24, LIGHT, w, False)
    vline(d, 286, x0=200, x1=700)
    put(d, "现在读初三 → 最迟2027年3月 · 现在读初二 → 最迟2028年3月", (450, 326), 23, WHITE, w)
    put(d, "现在读小学 → 按那届中考年份，往前数到3月", (450, 368), 20, SUB, w, False)
    return im


# 数据卡3：三条路
def wx_card_routes():
    w, h = 900, 400
    im, d = base(w, h, 0.5, 0.20)
    put(d, "想拿深户 · 三条路快慢差很多", (450, 50), 32, WHITE, w)
    cols = [
        ("① 子女随迁", "最快", "一方已是深户", 150, GOLD),
        ("② 人才核准", "数月", "学历技能符合", 450, WHITE),
        ("③ 纯积分入户", "5年+", "住所+社保各满5年", 750, GOLD),
    ]
    for tag, speed, expl, xc, scol in cols:
        cell(d, tag, xc, 148, 24, LIGHT, 280)
        cell(d, speed, xc, 222, 44, scol, 260)
        cell(d, expl, xc, 280, 20, SUB, 280)
    d.line([(300, 96), (300, 320)], fill=DIM, width=2)
    d.line([(600, 96), (600, 320)], fill=DIM, width=2)
    put(d, "纯积分够格看'稳定住所(自有或租赁)满5年' · 住房每满1月积1分=租房的5倍", (450, 356), 19, LIGHT, w, False)
    return im


def main():
    out = os.path.dirname(os.path.abspath(__file__)) + "/"
    jobs = [
        ("公众号配图-首图-900x383.png", wx_cover),
        ("公众号配图-章节条1-赛道差异-900x220.png", lambda: wx_section("01 · 赛道差异", "AC 和 D 类，差的是赛道", "非深户占54% · 公办指标仅23%")),
        ("公众号配图-章节条2-截止时间-900x220.png", lambda: wx_section("02 · 截止时间", "户口最迟要什么时候办好", "中考那年3月 · 报名前落到孩子头上")),
        ("公众号配图-章节条3-对号入座-900x220.png", lambda: wx_section("03 · 对号入座", "按孩子年级，各就各位", "从幼儿园到初三 · 每档最迟行动点")),
        ("公众号配图-数据卡1-赛道账-900x400.png", wx_card_track),
        ("公众号配图-数据卡2-截止对号-900x400.png", wx_card_deadline),
        ("公众号配图-数据卡3-三条路-900x400.png", wx_card_routes),
    ]
    for name, fn in jobs:
        fn().save(out + name)
        print("OK", name)


if __name__ == "__main__":
    main()
