# -*- coding: utf-8 -*-
"""
P1-5 · S1《2026 控制线全表》补充配图 · 96 所全表长图（2 张）

用途：兑现标题「96 所公办普高全表」的承诺，做成读者可收藏的对表资产。
版式：3 列（学校 / AC类 / D类），按 **AC 类控制线由高到低** 排列；
      上半 = 1–48 所、下半 = 49–96 所。
视觉档：**复用 `_build_p15_s1_imgs.py` 的 S1 档**（深蓝 + 右下标尺刻度），保证同套一致。
输出：公众号 / 今日头条 / 小红书 三个平台目录各 2 张（抖音 1080×1920 单帧放不下 48 行，不出）。

数据源：`00-S1-名额分配录取控制线全表（96所·AC类+D类·官方附件2转录）.md`（唯一真源，勿手抄）
"""
import os
import re
import sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _build_p15_s1_imgs as S  # base / txt / save_img / 配色 / ROOT / PFX

SRC = os.path.join(S.ROOT, "00-S1-名额分配录取控制线全表（96所·AC类+D类·官方附件2转录）.md")

W = 1080
PAD = 54
ROW_H = 46
X_NAME, X_AC, X_D = 54, 790, 965      # 学校左对齐锚点 / AC、D 居中锚点


def load():
    """从官方转录表读 96 校 AC、D 控制线；返回 [(学校, AC, D), ...]。"""
    raw = open(SRC, encoding="utf-8").read()
    ac_part, d_part = re.split(r"## D 类", raw)
    pat = re.compile(r"^\|\s*\d+\s*\|\s*(.+?)\s*\|\s*\d+\s*\|\s*\*\*(\d+)\*\*\s*\|$", re.M)
    ac = {m.group(1).strip(): int(m.group(2)) for m in pat.finditer(ac_part)}
    dd = {m.group(1).strip(): int(m.group(2)) for m in pat.finditer(d_part)}
    assert len(ac) == len(dd) == 96, (len(ac), len(dd))
    rows = [(k, ac[k], dd[k]) for k in ac]
    # AC 降序（稳定：AC 相同者保持官方附件2 原序）
    rows.sort(key=lambda r: -r[1])
    return rows


def fmt(name):
    """长校名做温和缩写，保住可识别性（不改官方全称的语义）。"""
    name = name.replace("（深大附中中心校区）", "（深大附中）")
    name = name.replace("（深大附中盐田校区）", "（盐田校区）")
    name = name.replace("（中科附高）", "")
    name = name.replace("深圳市第二高级中学深汕实验学校", "二高深汕实验学校")
    name = name.replace("深圳市第二高级中学宝安高中部", "二高宝安高中部")
    name = name.replace("中国科学院深圳理工大学附属实验高级中学", "中科院深理工附高")
    name = name.replace("香港中文大学（深圳）附属明德高级中学", "港中深附属明德高中")
    name = name.replace("西交利物浦大学基础教育集团外国语高级中学", "西交利物浦附外高中")
    name = name.replace("北京师范大学南山附属学校", "北师大南山附校")
    name = name.replace("北京大学附属中学深圳学校", "北大附中深圳学校")
    name = name.replace("东北师范大学附属中学深圳学校", "东北师大附中深圳学校")
    name = name.replace("深圳北理莫斯科大学附属实验中学", "深北莫附中")
    name = name.replace("广东实验中学深圳学校", "广东实验中学深圳校")
    name = name.replace("深圳大学附属实验中学", "深大附属实验中学")
    name = name.replace("华中师范大学龙岗附属中学", "华中师大龙岗附中")
    name = name.replace("南方科技大学附属中学", "南科大附中")
    name = name.replace("深圳市龙华科技实验高级中学", "龙华科技实验高中")
    name = name.replace("深圳市龙华外国语高级中学", "龙华外国语高中")
    name = name.replace("红岭教育集团大鹏华侨中学", "红岭大鹏华侨中学")
    name = name.replace("深圳市龙岗区第二高级中学", "龙岗区第二高级中学")
    name = name.replace("（综合高中）", "")
    return name


def sheet(rows, part, total_parts, out_paths):
    """rows: 该半区数据；part: 1/2；total_parts: 2"""
    n = len(rows)
    head_h = 340
    th_h = 66
    foot_h = 190
    H = head_h + th_h + n * ROW_H + foot_h

    im = S.base(W, H)
    d = ImageDraw.Draw(im)

    # ---- 页眉 ----
    badge = "深圳中考 · 名额分配控制线 · S1"
    f = S.font(S.FB, 26)
    tw = d.textlength(badge, font=f)
    d.rounded_rectangle([PAD - 8, 54, PAD + tw + 18, 100], radius=12,
                        fill=(6, 18, 44), outline=(130, 175, 235), width=3)
    d.text((PAD, 58), badge, font=f, fill=(210, 232, 255))

    S.txt(d, "2026 名额分配录取控制线", (PAD, 170), 62, S.WHITE, maxw=980, mini=40, anchor="la", tag="ft-t1")
    S.txt(d, "96 所公办普高全表 · D 类 vs AC 类", (PAD, 252), 38, S.GOLD, maxw=980, mini=26, anchor="la", tag="ft-t2")
    S.txt(d, f"按 AC 类控制线由高到低 ｜ 第 {part}/{total_parts} 张"
             f"（第 {'1–48' if part == 1 else '49–96'} 所）",
           (PAD, 306), 25, S.SUB, fp=S.FR, maxw=980, mini=18, anchor="la", tag="ft-t3")

    # ---- 表头 ----
    ty = head_h
    d.rounded_rectangle([PAD - 12, ty, W - PAD + 12, ty + th_h - 6], radius=14, fill=(8, 24, 56), outline=S.EDGE, width=3)
    S.txt(d, "学校", (X_NAME, ty + th_h / 2 - 3), 30, S.GOLD, maxw=640, mini=20, anchor="lm", tag="ft-h1")
    S.txt(d, "AC类", (X_AC, ty + th_h / 2 - 3), 30, S.GOLD, maxw=200, mini=20, anchor="mm", tag="ft-h2")
    S.txt(d, "D类", (X_D, ty + th_h / 2 - 3), 30, S.GOLD, maxw=200, mini=20, anchor="mm", tag="ft-h3")

    # ---- 数据行 ----
    y = ty + th_h
    for i, (name, a, dd_) in enumerate(rows):
        yy = y + i * ROW_H
        if i % 2 == 0:
            d.rectangle([PAD - 12, yy, W - PAD + 12, yy + ROW_H - 4], fill=(8, 22, 52))
        if dd_ > a:
            dcol = S.GOLD
        elif dd_ == a:
            dcol = S.WHITE
        else:
            dcol = S.LIGHT
        cy = yy + ROW_H / 2 - 2
        S.txt(d, fmt(name), (X_NAME, cy), 23, S.SUB, fp=S.FR, maxw=666, mini=16, anchor="lm", tag=f"n{i}")
        S.txt(d, str(a), (X_AC, cy), 27, S.WHITE, maxw=180, mini=18, anchor="mm", tag=f"a{i}")
        S.txt(d, str(dd_), (X_D, cy), 27, dcol, maxw=180, mini=18, anchor="mm", tag=f"d{i}")

    # ---- 页脚 ----
    fy = y + n * ROW_H + 26
    d.line([PAD - 12, fy - 8, W - PAD + 12, fy - 8], fill=(70, 118, 182), width=2)
    S.txt(d, "D 类高于 AC 类 79 所 ｜ 持平 13 所 ｜ D 类更低 4 所",
          (W / 2, fy + 40), 32, S.GOLD, maxw=960, mini=20, anchor="mm", tag="ft-f1")
    S.txt(d, "金色 = 该校 D 类控制线高于 AC 类　白色 = 持平　浅蓝 = D 类更低",
          (W / 2, fy + 84), 22, S.LIGHT, fp=S.FR, maxw=960, mini=15, anchor="mm", tag="ft-f2")
    S.txt(d, "数据来源：深圳市教育局2026年报考指导手册附件2 · 逐行转录",
          (W / 2, fy + 130), 22, S.SUB, fp=S.FR, maxw=960, mini=15, anchor="mm", tag="ft-f3")

    bad = [(t, tuple(int(v) for v in bb)) for t, bb in S.BADS
           if bb[0] < 12 or bb[2] > W - 8 or bb[1] < 20 or bb[3] > H - 6]
    print(("OK  " if not bad else "!!  ") + f"全表 第{part}张 {W}x{H}", bad if bad else "")
    S.BADS.clear()
    for p in out_paths:
        S.save_img(im, p)


if __name__ == "__main__":
    all_rows = load()
    halves = [all_rows[:48], all_rows[48:]]
    tags = ["全表1-1到48所", "全表2-49到96所"]
    for idx, (rows_h, tag) in enumerate(zip(halves, tags), start=1):
        outs = [
            f"{S.ROOT}/01.公众号/{S.PFX}-公众号-{tag}-1080x{340 + 66 + len(rows_h) * ROW_H + 190}.png",
            f"{S.ROOT}/02.今日头条/{S.PFX}-头条-{tag}-1080x{340 + 66 + len(rows_h) * ROW_H + 190}.png",
            f"{S.ROOT}/04.小红书/{S.PFX}-小红书-{tag}-1080x{340 + 66 + len(rows_h) * ROW_H + 190}.png",
        ]
        sheet(rows_h, idx, 2, outs)
    print("FULLTABLE DONE")
