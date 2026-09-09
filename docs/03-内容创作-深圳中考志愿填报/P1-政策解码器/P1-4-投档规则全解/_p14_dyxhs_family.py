# -*- coding: utf-8 -*-
"""
P1-4 S1~S4 · 抖音分镜 + 小红书配图（底色与公众号封面统一：同一套 TOP/BOT 垂直渐变+顶部光）
抖音：顶部「深圳中考」金字 + 金章小标 + 白句/金副句 + 圆角信息卡 + 底部句（安全区右≤950/下≤1590）
小红书：金小标 + 大白题 + 浅副句 + 统计卡/圆角信息条 + 金结论 + 数据脚注；内容纵向填充避免底部大片留白
"""
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
BADS = []
GOLD = (255, 210, 120); WHITE = (255, 255, 255)
LIGHT = (176, 208, 246); SUB = (214, 230, 252)

def save_img(im, out):
    for _ in range(6):
        try:
            im.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)

def font(fp, size): return ImageFont.truetype(fp, size)

def base(w, h, TOP, BOT):
    """与公众号封面 _fix_gzh_covers.base 一致（顶光垂直渐变），跨载体同底色。"""
    yv = np.linspace(0, 1, h)[:, None, None]
    grad = (np.array(TOP, float)[None, None, :]*(1-yv) + np.array(BOT, float)[None, None, :]*yv)
    grad = np.repeat(grad, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    gx, gy = w*0.5, h*0.08
    radial = np.exp(-(((xx-gx)/(w*0.55))**2 + ((yy-gy)/(h*0.30))**2))
    glow = np.array([255, 255, 255], float)[None, None, :]
    img = grad + glow*0.32*radial[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB"), None

def fit(d, text, fp, size, maxw, mini):
    f = font(fp, size)
    while f.size > mini:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2]-bb[0] <= maxw+1: break
        f = font(fp, f.size-1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2]-bb[0] <= maxw+1, "too long: %s" % text
    return f

def cmm(d, text, xy, size, fill, fp=FB, maxw=840, mini=30, tag=""):
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor="mm")))

def rcard(d, x0, y0, x1, y1, CARD, EDGE, rad=24):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=CARD, outline=EDGE, width=3)

# ---------------- 抖音分镜 ----------------
W, H = 1080, 1920
def dy_header(d, tag):
    f = fit(d, "深圳中考", FB, 92, 820, 72)
    d.text((W/2, 130), "深圳中考", font=f, fill=GOLD, anchor="mm")
    bb = d.textbbox((W/2, 130), "深圳中考", font=f, anchor="mm"); half = (bb[2]-bb[0])/2 + 6
    d.line([W/2-half, 214, W/2+half, 214], fill=GOLD, width=6)
    f2 = font(FB, 40); bb2 = d.textbbox((0, 0), tag, font=f2); tw = bb2[2]-bb2[0]; pad = 40
    d.rounded_rectangle([W/2-tw/2-pad, 250, W/2+tw/2+pad, 350], radius=50, outline=GOLD, width=3)
    d.text((W/2, 300), tag, font=f2, fill=(200, 222, 252), anchor="mm")

def dy_card(frame, TOP, BOT, CARD, EDGE, out):
    im, _ = base(W, H, TOP, BOT)
    d = ImageDraw.Draw(im)
    dy_header(d, frame["tag"])
    if frame.get("kind") == "b":
        cmm(d, frame["big"], (W/2, 600), 96, WHITE, maxw=800, mini=76, tag="b")
        y = 852
        for i, (txt, g) in enumerate(frame["rows"]):
            y1 = y + 150
            rcard(d, 80, y, W-80, y1, CARD, EDGE)
            cmm(d, txt, (W/2, (y+y1)/2), 46, GOLD if g else WHITE, maxw=800, mini=36, tag="r")
            y = y1 + 24
        cmm(d, frame["note"], (W/2, 1426), 40, LIGHT, fp=FR, maxw=800, mini=32, tag="n")
    else:
        big = frame.get("bigsize", 96)
        cmm(d, frame["big"], (W/2, 640), big, WHITE, maxw=800, mini=frame.get("bigmini", 74), tag="g")
        if frame.get("gold"):
            cmm(d, frame["gold"], (W/2, 830), 52, GOLD, maxw=800, mini=42, tag="gold")
        if frame.get("c1"):
            rcard(d, 80, 968, W-80, 1170, CARD, EDGE)
            cmm(d, frame["c1"], (W/2, 1034), 46, WHITE, maxw=800, mini=38, tag="c1")
            if frame.get("c2"):
                cmm(d, frame["c2"], (W/2, 1122), 34, LIGHT, fp=FR, maxw=800, mini=28, tag="c2")
        if frame.get("bottom"):
            cmm(d, frame["bottom"], (W/2, 1436), 48, WHITE, maxw=800, mini=40, tag="b")
    bad = []
    for tagn, bb in BADS:
        if bb[0] < 20 or bb[2] > 952: bad.append(tagn+"R")
        if bb[1] < 55 or bb[3] > 1592: bad.append(tagn+"D")
    print(("OK  " if not bad else "!!  ") + out.split('/')[-1], bad if bad else "")
    BADS.clear()
    save_img(im, out)

# ---------------- 小红书 ----------------
WX, HX = 1080, 1440; HM = 80
def xhs_cover(TOP, BOT, title, kick, foot, out):
    im, _ = base(WX, HX, TOP, BOT)
    d = ImageDraw.Draw(im)
    f = fit(d, "深圳中考", FB, 96, 1000, 80); d.text((WX/2, 180), "深圳中考", font=f, fill=GOLD, anchor="mm")
    f = fit(d, title, FB, 118, 1000, 94)
    d.text((WX/2, 560), title, font=f, fill=WHITE, anchor="mm")
    bb = d.textbbox((WX/2, 560), title, font=f, anchor="mm"); half = (bb[2]-bb[0])/2 + 8
    d.line([WX/2-half, 704, WX/2+half, 704], fill=GOLD, width=8)
    cmm(d, kick, (WX/2, 976), 64, GOLD, maxw=1000, mini=50, tag="kc")
    cmm(d, foot, (WX/2, 1366), 30, SUB, fp=FR, maxw=1000, mini=24, tag="kf")
    for tagn, bb in BADS:
        assert bb[0] >= 20 and bb[2] <= WX-20 and bb[3] <= HX-10, (tagn, bb)
    print("OK xhs cover", out.split('/')[-1]); BADS.clear()
    save_img(im, out)

def xhs_card(TOP, BOT, CARD, EDGE, kick, title, sub, tiles, rows, concl, out):
    """统一底色；版式三段填满：顶部标题区 → 主体区(300~1090，行高自适应铺满)
    → 底部【金框结论横幅】(~1160-1300) → 数据脚注。底部不留大段空白。"""
    im, _ = base(WX, HX, TOP, BOT)
    d = ImageDraw.Draw(im)
    cmm(d, kick, (WX/2, 84), 34, GOLD, maxw=980, mini=28, tag="xk")
    cmm(d, title, (WX/2, 205), 62, WHITE, maxw=1000, mini=50, tag="xt")
    if sub:
        cmm(d, sub, (WX/2, 292), 30, LIGHT, fp=FR, maxw=1000, mini=24, tag="xs")
    # 主体区段
    MAIN_TOP, MAIN_BOT = 316, 1092
    tiles_h = 250 if tiles else 0
    n_rows = len(rows)
    gap_between_rows = 22
    row_room = (MAIN_BOT - MAIN_TOP) - tiles_h - (26 if tiles else 0)
    row_h = row_min = 104
    if n_rows:
        row_h = max(row_min, min((row_room - (n_rows-1)*gap_between_rows)/n_rows, 320))
    y = MAIN_TOP
    if tiles:
        th = tiles_h
        tw, gap = 280, 24
        x0 = (WX - (tw*3 + gap*2))/2
        for i, (num, lab) in enumerate(tiles[:3]):
            x = x0 + i*(tw + gap)
            rcard(d, x, y, x+tw, y+th, CARD, EDGE, rad=20)
            cmm(d, num, (x+tw/2, y+th*0.32), 62, GOLD, maxw=tw-26, mini=46, tag="tile")
            cmm(d, lab, (x+tw/2, y+th*0.74), 27, SUB, fp=FR, maxw=tw-24, mini=21, tag="tile")
        y += th + 26
    if rows:
        for i, txt in enumerate(rows):
            y1 = y + row_h
            rcard(d, HM, y, WX-HM, y1, CARD, EDGE, rad=22)
            cmm(d, txt, (WX/2, (y+y1)/2), 38 if row_h < 190 else 46, WHITE, maxw=920, mini=28, tag="row")
            y = y1 + (gap_between_rows if i < n_rows-1 else 0)
    # 底部金框结论横幅
    b0 = 1176
    d.rounded_rectangle([HM-6, b0, WX-HM+6, b0+118], radius=26, fill=CARD, outline=GOLD, width=4)
    if concl:
        first = concl[0]
        cmm(d, first[0], (WX/2, b0+54), 44, GOLD if first[1] else WHITE, maxw=960, mini=34, tag="band")
    cmm(d, "数据来源：深圳市教育局2026报考指导手册 · 人工核对", (WX/2, 1392), 21, SUB, fp=FR, maxw=1000, mini=16, tag="foot")
    bad = []
    for tagn, bb in BADS:
        if bb[0] < 18 or bb[1] < 8 or bb[2] > WX-18 or bb[3] > HX-8:
            bad.append((tagn, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + out.split('/')[-1], bad if bad else "")
    BADS.clear()
    save_img(im, out)
