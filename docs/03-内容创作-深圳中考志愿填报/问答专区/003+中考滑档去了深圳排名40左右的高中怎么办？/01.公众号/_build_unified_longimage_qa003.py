# -*- coding: utf-8 -*-
"""QA-003 公众号极简版 · 统一长图（13-1 规范：900宽连续渐变，金竖条章节头/数字卡/行盒/系列钩子卡）
内容镜像 003-…-公众号-终版-极简.md：滑档定义 → 排名40区间 → 两条路 → 分工论 → 转给孩子 → 系列第3篇。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 2900
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)
FBD = font(34, True)

t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
img = Image.fromarray(arr.repeat(W, axis=1).astype(np.uint8), "RGB")
d = ImageDraw.Draw(img)

checks = []
def put(text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 8:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            w = bb[2] - bb[0]
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if w <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    checks.append((text, fnt, xy, anchor, color, maxw))

def box(x, y, w, h, fill=CARD, outline=EDGE, r=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def chapter(ty, txt):
    d.rectangle([50, ty - 27, 58, ty + 27], fill=GOLD)
    put(txt, font(36, True), (78, ty), anchor="lm", color=WHITE)
    d.line([50, ty + 45, 140, ty + 45], fill=GOLD, width=3)

def row(ry, tag, detail, tagcolor=GOLD):
    box(40, ry, W - 80, 80)
    put(tag, font(19, True), (76, ry + 26), anchor="lm", color=tagcolor)
    put(detail, font(16), (76, ry + 56), anchor="lm", color=WHITE, maxw=740)

# ---------- 页眉 ----------
put("深圳中考 · 问答系列 · 第3篇", font(15, True), (50, 36), anchor="lm", color=GOLD)
put("滑档去了排名40的高中？先别慌，这不是终点", FBD, (50, 74), anchor="lm", color=WHITE)
put("排名40=录取线557分 · 第35-45名553-561 · 孩子学习好 · 家长决策优", font(16), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 你其实不算滑档 ----------
chapter(208, "01 · 你其实不算「滑档」")
rows_dui = [
    ("冲档落空", "冲的志愿没录上，落到稳/保 → 正常结果，好好规划高中", LIGHT),
    ("稳保落空", "稳和保也没接住 → 已录公办，接受并规划", LIGHT),
    ("全线滑档", "第一批全落空 → 才涉及补录（和本文读者无关）", GOLD),
]
ry1 = 270
for tag, detail, tc in rows_dui:
    row(ry1, tag, detail, tc)
    ry1 += 90
put("这意味着什么：多数「滑档去排名40」是冲档落空——冲太高、稳太少、保没垫底。问题不在孩子考砸，在志愿梯度没拉开。",
    font(17, True), (W / 2, ry1 + 2), color=GOLD, maxw=W - 80)

# ---------- 02 排名40什么水平 ----------
chapter(ry1 + 52, "02 · 排名40，到底什么水平")
box(40, ry1 + 120, W - 80, 178, r=18)
ry_t = ry1 + 120
put("第40名 · 深高创新高中", font(17, True), (W / 2, ry_t + 28), color=WHITE)
put("557分", font(54, True), (W / 2, ry_t + 86), color=GOLD)
put("第35-45名区间 553-561分 · 第一批中后段公办普高", font(15), (W / 2, ry_t + 148), color=LIGHT, maxw=W - 120)
ry2 = ry_t + 178
put("这意味着什么：你录到的是公办、有稳定师资、有正常高考通道，部分还有特色班/重点班。滑档≠人生完蛋，以为滑档=完蛋的恐慌，才是最大的损失。",
    font(17, True), (W / 2, ry2 + 28), color=GOLD, maxw=W - 80)

# ---------- 03 两条路 ----------
chapter(ry2 + 88, "03 · 你面前只有两条路")
box(40, ry2 + 150, W - 80, 150, r=18)
d.line([W / 2, ry2 + 166, W / 2, ry2 + 284], fill=EDGE, width=2)
put("接受并规划", font(18, True), (265, ry2 + 184), color=GOLD)
put("主路 · 想通排名40不差", font(16), (265, ry2 + 226), color=WHITE)
put("复读", font(18, True), (635, ry2 + 184), color=LIGHT)
put("慎选 · 不能报指标生/自主招生", font(16), (635, ry2 + 226), color=WHITE)
ry3 = ry2 + 300
put("这意味着什么：补录/征求志愿跟你没关系——那是给全线滑档没学上家长的方向，能回的是民办普高/中职（公办无补录窗口）。对已录排名40公办的你，补录是降级，不是补救。",
    font(17, True), (W / 2, ry3 + 28), color=GOLD, maxw=W - 80)

# ---------- 04 分工论 ----------
chapter(ry3 + 88, "04 · 孩子负责学习好，家长负责决策优")
rows_dg = [
    ("① 没想到政策", "公办第一批录取即锁定 · 补录只对民办 · 复读不能报指标生"),
    ("② 没想到策略", "冲稳保没拉开 · 没留保底志愿 · 指标生不会用"),
    ("③ 没想到数据", "各校历年录取线 · AC/D类分差 · 自己分数段的位置"),
]
ry4 = ry3 + 156
for tag, detail in rows_dg:
    row(ry4, tag, detail, LIGHT)
    ry4 += 90
put("这三件事，都是出分前就能做、且做了真能改变结果的事。这一仗，孩子负责冲锋，家长负责掌舵。",
    font(17, True), (W / 2, ry4 + 2), color=GOLD, maxw=W - 80)

# ---------- 05 转给孩子 ----------
chapter(ry4 + 52, "05 · 把这句话，转给孩子")
box(40, ry4 + 118, W - 80, 190, r=18)
put("别让孩子觉得自己「输在了中考」", font(19, True), (W / 2, ry4 + 160), color=WHITE)
put("中考只是定了起点，定不了终点", font(16), (W / 2, ry4 + 222), color=LIGHT)
put("排名40的学校，同样有人考进重点大学", font(17, True), (W / 2, ry4 + 280), color=GOLD)
ry5 = ry4 + 308
put("现在就能做三件事：①对号入座（冲档落空就接受）②接受并规划（查出口数据/特色班/升学路径）③想复读先过清单（失常？自愿？抗压？缺一项都慎重）",
    font(17, True), (W / 2, ry5 + 34), color=GOLD, maxw=W - 80)

# ---------- 06 系列第3篇 · 问答系列 ----------
chapter(ry5 + 84, "06 · 给更多家长的一句话")
band_y = ry5 + 144
box(40, band_y, W - 80, 190, r=18)
put("那位家长的今天，可能就是你家的明天", font(17, True), (W / 2, band_y + 40), color=GOLD)
put("如果你们也把志愿当「到时候再说」的话", font(15), (W / 2, band_y + 74), color=SUB)
put("你现在看到这一篇，就是提前做功课的开始", font(16, True), (W / 2, band_y + 124), color=WHITE)

band_y2 = band_y + 226
box(40, band_y2, W - 80, 350, r=18)
put("你现在读的是《问答系列》第3篇", font(17, True), (W / 2, band_y2 + 38), color=GOLD)
put("每个家长高频提问，一题一答，按顺序读更系统", font(14), (W / 2, band_y2 + 70), color=SUB)
qa_list = [
    "① 非深户能在深圳参加中考读高中吗？5项条件 · 3条路",
    "② 普高和中职学费差多少？公办约1万 · 民办21万-36万",
    "③ 滑档去了排名40的高中怎么办？（本篇）",
    "④ 深圳中考志愿到底怎么填才不滑档？（下篇）",
]
sy = band_y2 + 106
for s in qa_list:
    put(s, font(15), (76, sy), anchor="lm", color=WHITE, maxw=W - 140)
    sy += 42
put("更多家长高频提问陆续回答 · 关注不迷路", font(15, True), (W / 2, sy + 6), color=GOLD, maxw=W - 120)

# ---------- 页脚 ----------
divy = band_y2 + 386
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("滑档≠人生完蛋，恐慌才是损失。", font(26, True), (W / 2, divy + 38), color=WHITE)
put("数据，是焦虑最好的解药。", font(17), (W / 2, divy + 82), color=LIGHT)
put("关注 · 深圳中考系列持续更新 · 把志愿的账提前算清", font(15), (W / 2, divy + 122), color=SUB)
put("数据来源：深圳市教育局《2026年高中阶段学校考试招生工作的通知》《2026年中考报名工作的通知》",
    font(13), (W / 2, divy + 156), color=LIGHT, maxw=W - 80)
put("深圳市2026年高中阶段学校第一批录取标准（按2026录取线AC类住宿排序）· 名额分配招生计划",
    font(13), (W / 2, divy + 184), color=LIGHT, maxw=W - 80)
put("录取线、补录、复读的具体规则以当年市招考办公告为准",
    font(13), (W / 2, divy + 212), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/003+中考滑档去了深圳排名40左右的高中怎么办？/01.公众号/003+中考滑档去了深圳排名40左右的高中怎么办？-公众号-长图-极简版.png"
img.save(out)
print("saved", img.size, "| 内容底部≈", divy + 230, "| 画布余量=", H - (divy + 230))

# ---------- 校验 ----------
bad = 0; bxs = []
for (text, fnt, (cx, cy), anchor, color, maxw) in checks:
    bbox = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
    x0, y0 = bbox[0] + cx, bbox[1] + cy
    x1, y1 = bbox[2] + cx, bbox[3] + cy
    w = x1 - x0
    bxs.append(((x0, y0, x1, y1), text, (cx, cy)))
    ok = (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1)
    if maxw and w > maxw + 2: ok = False
    if not ok:
        bad += 1
        print(f"OVERFLOW [{text[:20]}] x=({x0:.0f},{x1:.0f}) y=({y0:.0f},{y1:.0f}) maxw={maxw}")
print("OVERFLOW:", "PASS" if bad == 0 else f"FAIL {bad}")
ov = 0
for i in range(len(bxs)):
    for j in range(i + 1, len(bxs)):
        (ax0, ay0, ax1, ay1), at, ac = bxs[i]
        (bx0, by0, bx1, by1), bt, bc = bxs[j]
        if ac == bc:
            continue
        ox = max(0, min(ax1, bx1) - max(ax0, bx0))
        oy = max(0, min(ay1, by1) - max(ay0, by0))
        if ox > 4 and oy > 4:
            ov += 1
            print(f"OVERLAP: [{at[:14]}] x [{bt[:14]}]")
print("OVERLAP:", "PASS" if ov == 0 else f"FAIL {ov}")
