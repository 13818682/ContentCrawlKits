# -*- coding: utf-8 -*-
"""
深圳中考 · 问答系列 · 004 今日头条配图生成脚本（1200×900）
风格：P1-2「主线精简版」极简排版风（2026-09-05 用户指定）
  - 深蓝渐变 TOP(27,58,92)→BOT(13,30,48) + 顶部柔光 + 两处柔和椭圆
  - 顶部金色描边胶囊(平台) + 白/金大标题排版 + 底部浅色来源
  - 无装饰纹理；细线/金线分隔
产出 6 张：封面1-3 + 正文图×2 + 微头条配图
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
DIM = (96, 122, 158)
W, H = 1200, 900
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"


def base(w=W, h=H, gx=0.5, gy=0.18):
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


def put(d, text, xy, size, fill, w=W, bold=True, maxw=None):
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


def pill(d, text, cy, size=30, pad=30):
    f = ImageFont.truetype(FB, size)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    while tw > W - 200:
        size -= 1; f = ImageFont.truetype(FB, size)
        bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    x0, x1 = (W - tw) / 2 - pad, (W + tw) / 2 + pad; hh = size * 1.9
    d.rounded_rectangle([x0, cy - hh / 2, x1, cy + hh / 2], radius=hh / 2, outline=GOLD, width=3)
    d.text((W / 2, cy), text, font=f, fill=WHITE, anchor="mm")


def footer(d):
    put(d, "数据来源：深圳市公安局/市教育局公开文件 · 逐条人工核对", (W / 2, 850), 22, SUB, bold=False)


# 封面1-主标题
def cover_title():
    im, d = base()
    pill(d, "深圳中考 · 问答004", 118)
    put(d, "非深户想转深户", (W / 2, 330), 100, WHITE)
    put(d, "最迟几年级办户口？", (W / 2, 492), 66, GOLD)
    put(d, "AC/D差的是赛道：D类约54%考生 · 公办名额仅约23%", (W / 2, 640), 38, LIGHT, bold=False)
    d.line([(W / 2 - 220, 738), (W / 2 + 220, 738)], fill=GOLD, width=4)
    footer(d)
    return im


# 封面2-数据对撞
def cover_data():
    im, d = base()
    pill(d, "深圳中考 · 问答004", 118)
    put(d, "54%", (W * 0.33, 430), 150, GOLD)
    put(d, "非深户(D)考生占比", (W * 0.33, 585), 34, LIGHT, bold=False)
    put(d, "23%", (W * 0.67, 430), 150, WHITE)
    put(d, "公办普高给D类名额", (W * 0.67, 585), 34, LIGHT, bold=False)
    d.line([(W / 2, 300), (W / 2, 640)], fill=GOLD, width=3)
    put(d, "多数孩子落中下游 · 赛道差，是户口定的", (W / 2, 742), 46, WHITE)
    footer(d)
    return im


# 封面3-答案大字
def cover_answer():
    im, d = base()
    pill(d, "深圳中考 · 问答004", 118)
    put(d, "3月前", (W / 2, 400), 168, GOLD)
    put(d, "中考那年 · 户口落到孩子头上", (W / 2, 600), 58, WHITE)
    put(d, "现在初三 → 最迟2027年3月 · 读初二 → 2028 · 读小学 → 按届往前数", (W / 2, 700), 30, LIGHT, bold=False)
    footer(d)
    return im


# 正文图-赛道账（表格）
def table_track():
    im, d = base()
    pill(d, "深圳中考 · 问答004", 118)
    put(d, "AC vs D · 赛道差异在哪", (W / 2, 196), 48, WHITE)
    hd = [("对比项", 280), ("AC类 · 深户", 620), ("D类 · 非深户", 920)]
    for t, x in hd:
        put(d, t, (x, 300), 30, SUB, maxw=360)
    d.line([(180, 352), (1020, 352)], fill=DIM, width=2)
    rows = [
        ("考生占比", "约46%", "约54%", WHITE, GOLD),
        ("公办普高名额", "约77%", "约23%", WHITE, GOLD),
        ("中下游录取线", "AC类基准", "高13-31分", WHITE, GOLD),
    ]
    ys = [470, 600, 730]
    for (lab, ac, dc, ca, cd), y in zip(rows, ys):
        put(d, lab, (280, y), 34, WHITE, maxw=360)
        put(d, ac, (620, y), 38, ca, maxw=360)
        put(d, dc, (920, y), 38, cd, maxw=360)
    footer(d)
    return im


# 正文图-年级时间表
def grade_plan():
    im, d = base()
    pill(d, "深圳中考 · 问答004", 118)
    put(d, "按孩子年级 · 对号入座", (W / 2, 190), 48, WHITE)
    rows = [
        ("幼儿园~小学低年级", "来得及", "走纯积分 · 社保别断 攒住所年限", GOLD),
        ("小学高年级", "开始吃紧", "先评估父母能否走人才核准", WHITE),
        ("初一 / 初二", "基本无望", "转D类策略 · 打满资格志愿牌", LIGHT),
        ("已经初三", "翻篇", "只盯5项资格 + 志愿梯度", WHITE),
    ]
    y0 = 380; step = 122
    for i, (who, status, act, scol) in enumerate(rows):
        cy = y0 + i * step
        put(d, who, (300, cy), 34, WHITE, maxw=480)
        put(d, status, (700, cy), 38, scol, maxw=300)
        put(d, act, (990, cy), 28, SUB, maxw=380)
        if i < len(rows) - 1:
            d.line([(200, cy + step / 2), (1000, cy + step / 2)], fill=DIM, width=2)
    footer(d)
    return im


# 微头条配图-3关键数字
def three_numbers():
    im, d = base()
    pill(d, "深圳中考 · 问答004", 118)
    put(d, "3 个关键数字", (W / 2, 200), 48, WHITE)
    nums = [
        ("54%", "D类考生占比", 230, GOLD),
        ("23%", "公办普高D类名额", 600, WHITE),
        ("13-31分", "普通校D线比AC线高", 970, GOLD),
    ]
    for n, lab, xc, col in nums:
        put(d, n, (xc, 520), 118, col, maxw=340)
        put(d, lab, (xc, 660), 32, LIGHT, maxw=340, bold=False)
    footer(d)
    return im


def main():
    jobs = [
        ("今日头条-封面1-主标题-1200x900.png", cover_title),
        ("今日头条-封面2-数据对撞-1200x900.png", cover_data),
        ("今日头条-封面3-答案大字-1200x900.png", cover_answer),
        ("今日头条-正文图-赛道账-1200x900.png", table_track),
        ("今日头条-正文图-年级时间表-1200x900.png", grade_plan),
        ("今日头条-微头条配图-3关键数字-1200x900.png", three_numbers),
    ]
    for name, fn in jobs:
        fn().save(HERE + name)
        print("OK", name)


if __name__ == "__main__":
    main()
