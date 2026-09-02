# -*- coding: utf-8 -*-
"""
P1-1 公众号子任务封面 5 张（900×383）
========================================
每个子任务一个【主导巨型数字】作视觉主角（主钩子），细分数据降为副题小字。
统一深蓝渐变+金色数据+顶部光晕。徽章+主标题+巨型数字+说明+CTA胶囊。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 383
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
FD = "C:/Windows/Fonts/"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 10:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    ck.append((text, fnt, xy, anchor))


def verify(d, ck, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} @({cx},{cy})")
    print(f"{name}: OVERFLOW {'PASS' if bad == 0 else 'FAIL ' + str(bad)}")
    return bad == 0


def new_canvas():
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    glow = np.exp(-(((x - W * 0.5) / (W * 0.6)) ** 2 + ((y - H * 0.18) / (H * 0.45)) ** 2)) * 0.16
    img2 = Image.fromarray(np.clip(np.array(img, float) + np.array((210, 225, 250))[None, None, :] * glow[:, :, None], 0, 255).astype(np.uint8), "RGB")
    return img2, ImageDraw.Draw(img2)


def build(badge, hook_label, hook_num, hook_unit, detail, cta, out_path, main_text=None):
    """主导巨型数字封面：徽章+小标+巨型数字(金色)+单位胶囊+底部说明+CTA
    main_text: 若提供，则直接渲染文字主句（不分数字+单位），用于ACD这类"考生分ACD三类"主钩子。"""
    img, d = new_canvas()
    ck = []
    # 徽章
    d.rounded_rectangle([280, 20, 620, 50], radius=15, fill=BAND, outline=GOLD, width=2)
    put(d, ck, badge, font(15, True), (450, 35), color=GOLD)
    # 钩子标签（主视觉上方的引导词）
    put(d, ck, hook_label, font(22, True), (450, 78), color=LIGHT, maxw=860)
    if main_text:
        # 文字主句作为视觉主角（居中大字，金色），适合"考生分ACD三类"这类主题句
        f_mt = font(66, True)
        put(d, ck, main_text, f_mt, (450, 205), color=GOLD, maxw=880)
    else:
        # 主导巨型数字 + 单位胶囊（居中对齐）
        f_giant = font(110, True)
        bb_num = d.textbbox((0, 0), hook_num, font=f_giant)
        num_px = bb_num[2] - bb_num[0]
        put(d, ck, hook_num, f_giant, (450, 215), color=GOLD, maxw=820)
        # 单位胶囊放在数字右侧
        if hook_unit:
            fu = font(30, True)
            bbu = d.textbbox((0, 0), hook_unit, font=fu)
            pad_u = 16
            ux0 = 450 + num_px / 2 + 14
            uy0, uy1 = 197, 233
            ux1 = ux0 + bbu[2] + pad_u * 2
            d.rounded_rectangle([ux0, uy0, ux1, uy1], radius=18, fill=GOLD)
            put(d, ck, hook_unit, fu, (ux0 + (bbu[2] + pad_u * 2) / 2, (uy0 + uy1) / 2), color=NAVY)
    # 底部说明（细分数据，小字，主钩子的补充）
    put(d, ck, detail, font(19, True), (450, 300), color=WHITE, maxw=860)
    # CTA 胶囊
    fp = font(15, True)
    bb = d.textbbox((0, 0), cta, font=fp)
    pd = 12
    py1 = H - 24
    py0 = py1 - bb[3] - pd
    px0 = (W - (bb[2] + pd * 2)) / 2
    px1 = px0 + bb[2] + pd * 2
    d.rounded_rectangle([px0, py0, px1, py1], radius=24, outline=GOLD, width=2)
    put(d, ck, cta, fp, ((px0 + px1) / 2, (py0 + py1) / 2), color=GOLD)
    ok = verify(d, ck, os.path.basename(out_path))
    if not (px0 >= 10 and px1 <= W - 10 and py0 >= 10 and py1 <= H - 20):
        print(f"  [胶囊越界] 底部留白={H - py1:.0f}px")
    img.save(out_path)
    print("saved", out_path.split("/")[-1], img.size)
    return ok


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/01.公众号/"
BADGE = "深圳中考 · P1系列 · 630背后的隐藏规则"

results = []
# 1. 科目性价比 —— 主导钩子「同样的时间 更高的分」
results.append(build(
    BADGE, "同样的复习时间 · 花在哪最划算", "5星", "全力投入",
    "语数英物化★★★★★主战场 · 理化实验2026涨20分性价比王 · 历史道法稳定即可",
    "精力有限 · 花在刀刃上 · 收藏",
    BASE + "02.子任务-科目性价比/P1-2-子任务02-公众号封面-900x383.png",
    main_text="科目性价比",
))
# 2. 单科等级制 —— 主导钩子「A+」
results.append(build(
    BADGE, "单科等级 · 比分数更准的定位", "A+", "全市前5%",
    "A+永远是前5% · 省一级门槛=不能掉C · 看等级不看单次分数",
    "对号入座 · 收藏对照",
    BASE + "03.子任务-单科等级制/P1-2-子任务03-公众号封面-900x383.png",
    main_text="A+ 永远前5%",
))
# 3. 隐形战场 —— 主导钩子「生地」
results.append(build(
    BADGE, "不计总分 · 却决定命运", "生地", "100分",
    "同分PK先比生地 · 14分差距=一个学位 · 信息科技艺术须合格",
    "隐形战场别忽视 · 收藏",
    BASE + "04.子任务-隐形战场/P1-2-子任务04-公众号封面-900x383.png",
    main_text="同分PK 决胜生地",
))

print()
print("全部 OK =", all(results))
