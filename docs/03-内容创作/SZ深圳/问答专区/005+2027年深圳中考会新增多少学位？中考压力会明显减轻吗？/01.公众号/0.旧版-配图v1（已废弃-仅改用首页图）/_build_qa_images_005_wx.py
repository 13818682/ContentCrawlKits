# -*- coding: utf-8 -*-
"""
深圳中考 · 问答系列 · 005 公众号配图生成脚本（900 系列 · 精简版）
风格：沿用 QA-004（P1-2「主线精简版」极简排版风）
  - 深蓝渐变 TOP(27,58,92)→BOT(13,30,48) + 顶部柔光 + 两处柔和椭圆
  - 白/金/浅蓝三色排版，无徽章胶囊、无装饰纹理；金线/细线分隔
产出 7 张：首图 / 章节条1-3 / 数据卡1-3
校验：textbbox 逐元素越界检查（Read 无法预览图片，不依赖目检）
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
DIM = (96, 122, 158)

ISSUES = []
CUR = {"w": 0, "h": 0}


def base(w, h, gx=0.5, gy=0.18):
    CUR["w"], CUR["h"] = w, h
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


def put(d, text, xy, size, fill, w, bold=True, maxw=None, tag=""):
    """居中绘制（anchor=mm）；自动缩字号以适配 maxw；记录越界问题"""
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else w - 120
    while f.size > 14:
        bb = d.textbbox((0, 0), text, font=f, anchor="mm")
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox(xy, text, font=f, anchor="mm")
    if bb[0] < 0 or bb[2] > CUR["w"]:
        ISSUES.append(f"越界(横向) {tag or text[:14]} bbox={bb} w={CUR['w']}")
    if bb[1] < 0 or bb[3] > CUR["h"]:
        ISSUES.append(f"越界(纵向) {tag or text[:14]} bbox={bb} h={CUR['h']}")
    if xy[1] + (bb[3] - bb[1]) / 2 > CUR["h"] - 12:
        ISSUES.append(f"底部留白不足 {tag or text[:14]} bottom={bb[3]} h={CUR['h']}")
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    return f


def vline(d, y, x0=120, x1=780, color=DIM, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def seqline(d, parts, cy, size, w=900, maxw=None, tag=""):
    """一行内分段着色居中排版：parts=[(text, fill, bold), ...]"""
    mw = maxw if maxw else w - 100
    s = size
    while s > 14:
        total = 0; fonts = []
        for txt, _fill, bold in parts:
            f = ImageFont.truetype(FB if bold else FR, s)
            fonts.append(f); total += d.textlength(txt, font=f)
        if total <= mw + 1:
            break
        s -= 1
    x = (w - total) / 2
    if x < 0 or x + total > CUR["w"]:
        ISSUES.append(f"越界(横排) {tag or parts[0][0][:12]} x={x:.1f} total={total:.1f} w={CUR['w']}")
    if cy + s / 2 > CUR["h"] - 12:
        ISSUES.append(f"底部留白不足(横排) {tag or parts[0][0][:12]} bottom={cy + s / 2:.0f} h={CUR['h']}")
    for (txt, fill, bold), f in zip(parts, fonts):
        d.text((x, cy), txt, font=f, fill=fill, anchor="lm")
        x += d.textlength(txt, font=f)
    return s


def cell(d, text, xc, y, size, fill, maxw, w=900, bold=True, tag=""):
    put(d, text, (xc, y), size, fill, w, bold, maxw, tag)


# ── 首图 900×383：完整主题为主文案，突出"多盖一批高中"的鼓舞感 ──
def wx_cover():
    w, h = 900, 383
    im, d = base(w, h, 0.5, 0.18)
    put(d, "深圳中考 · 问答005", (450, 40), 28, GOLD, w, tag="cover-badge")
    put(d, "未来五年，深圳要为孩子", (450, 150), 46, WHITE, w, tag="cover-l1")
    seqline(d, [("多盖一批", GOLD, True), ("高中", WHITE, True)], 226, 46, tag="cover-l2")
    d.line([(450 - 120, 270), (450 + 120, 270)], fill=GOLD, width=3)
    put(d, "新建10所 · 改扩建10余所 · 规划新增学位10万个以上", (450, 308), 23, LIGHT, w, False, tag="cover-sub")
    return im


def wx_section(tag, title, sub):
    w, h = 900, 220
    im, d = base(w, h, 0.5, 0.16)
    put(d, tag, (450, 58), 26, GOLD, w, tag="sec-tag")
    put(d, title, (450, 130), 44, WHITE, w, tag="sec-title")
    put(d, sub, (450, 186), 22, LIGHT, w, False, tag="sec-sub")
    return im


# ── 数据卡1：新建10所序列（39—48高）──
def wx_card_new10():
    w, h = 900, 400
    im, d = base(w, h, 0.5, 0.20)
    put(d, "新建10所公办高中 · 三十九高—四十八高", (450, 44), 30, WHITE, w, tag="c1-title")
    hd = [("项目", 150), ("选址", 430), ("规划规模", 720)]
    for t, x in hd:
        cell(d, t, x, 100, 21, SUB, 260, tag="c1-hd")
    vline(d, 126)
    rows = [
        ("39高", "南山", "48班 / 2400学位", WHITE, GOLD),
        ("40高", "坪山", "36班 / 1800学位", WHITE, GOLD),
        ("45高", "宝安", "4800学位", WHITE, GOLD),
        ("46高", "光明", "1800学位", WHITE, GOLD),
        ("41/42/43/44/47/48高", "未公开", "未公开", LIGHT, SUB),
    ]
    ys = [166, 208, 250, 292, 334]
    for (a, b, c, ca, cc), y in zip(rows, ys):
        cell(d, a, 150, y, 22, ca, 250, tag="c1-a")
        cell(d, b, 430, y, 21, ca, 300, tag="c1-b")
        cell(d, c, 720, y, 21, cc, 330, tag="c1-c")
    put(d, "※ 41高及42/43/44/47/48高的选址与规模，官方尚未公布", (450, 372), 18, SUB, w, False, tag="c1-note")
    return im


# ── 数据卡2：两个五年 · 连续投入 ──
def wx_card_plan():
    w, h = 900, 400
    im, d = base(w, h, 0.5, 0.20)
    put(d, "两个五年规划 · 连续投入", (450, 52), 33, WHITE, w, tag="c2-title")
    put(d, "不是应急补位，是提前铺路", (450, 100), 22, LIGHT, w, False, tag="c2-sub")
    cols = [
        ("十四五", "2020—2025", "约50所", "新改扩建公办高中", "新增11万个以上学位", 240),
        ("十五五", "2026—2030", "10万个以上", "规划新增公办高中", "五年全口径目标", 660),
    ]
    for tag, span, big, blab, slb, xc in cols:
        cell(d, tag, xc, 175, 30, LIGHT, 380, tag="c2-tag")
        cell(d, span, xc, 212, 19, SUB, 380, 900, False, tag="c2-span")
        cell(d, big, xc, 282, 46, GOLD, 380, tag="c2-big")
        cell(d, blab, xc, 332, 21, WHITE, 380, tag="c2-blab")
        cell(d, slb, xc, 366, 19, SUB, 380, 900, False, tag="c2-slhb")
    d.line([(450, 165), (450, 366)], fill=DIM, width=2)
    return im


# ── 数据卡3：什么时候轮到？（冷静提醒）──
def wx_card_when():
    w, h = 900, 400
    im, d = base(w, h, 0.5, 0.20)
    put(d, "这些新学位，什么时候轮到你家孩子？", (450, 52), 31, WHITE, w, tag="c3-title")
    vline(d, 112)
    # 上块：2027届
    put(d, "2027 届中考生", (450, 156), 30, LIGHT, w, tag="c3-a1")
    put(d, "赶上的，是「扩容进行时」", (450, 208), 40, GOLD, w, tag="c3-a2")
    put(d, "新校在建、在可研、在设计——还轮不到", (450, 252), 21, SUB, w, False, tag="c3-a3")
    d.line([(230, 292), (670, 292)], fill=DIM, width=2)
    # 下块：2029-2031届
    put(d, "2029—2031 届中考生", (450, 330), 26, LIGHT, w, tag="c3-b1")
    put(d, "才真正等到「扩容完成时」", (450, 372), 30, WHITE, w, tag="c3-b2")
    return im


def main():
    out = os.path.dirname(os.path.abspath(__file__)) + "/"
    jobs = [
        ("公众号配图-首图-900x383.png", wx_cover),
        ("公众号配图-章节条1-建设节奏-900x220.png",
         lambda: wx_section("01 · 建设节奏", "这不是新闻，是节奏", "3月社稳 · 7月设计 · 9月可研，一路排下来")),
        ("公众号配图-章节条2-新建与扩建-900x220.png",
         lambda: wx_section("02 · 新建与扩建", "10所新建 + 10余所改扩建", "从三十九高到四十八高，老校也在长大")),
        ("公众号配图-章节条3-冷静提醒-900x220.png",
         lambda: wx_section("03 · 冷静提醒", "2027届赶上的，是进行时", "这些新学位服务的是2029年之后的孩子")),
        ("公众号配图-数据卡1-新建10所-900x400.png", wx_card_new10),
        ("公众号配图-数据卡2-两个五年-900x400.png", wx_card_plan),
        ("公众号配图-数据卡3-什么时候轮到-900x400.png", wx_card_when),
    ]
    for name, fn in jobs:
        im = fn()
        im.save(out + name)
        print("OK", name, im.size)
    print("\n=== 校验 ===")
    if ISSUES:
        for s in ISSUES:
            print("!!", s)
        raise SystemExit(f"校验未通过：{len(ISSUES)} 处问题")
    print("PASS · 无横向越界")


if __name__ == "__main__":
    main()
