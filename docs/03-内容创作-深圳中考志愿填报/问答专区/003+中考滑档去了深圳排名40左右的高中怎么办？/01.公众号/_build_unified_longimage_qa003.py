# -*- coding: utf-8 -*-
"""QA-003 公众号极简版 · 统一长图 · 大字版（13-1 规范：900宽连续渐变）
大字版说明：正文 ×2.4（渲染38px，手机显示≈16px），章节/数字大字手动放大。
内容镜像 003-…-公众号-终版-极简.md：滑档定义 → 排名40区间 → 两条路 → 分工论 → 转给孩子 → 系列第3篇。
自上而下累加 y 布局，避免坐标漂移。越界+重叠校验 + 自动裁剪尾部。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 7000
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 2.4))   # 正文 ×2.4
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

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

def box(x, y, w, h, fill=CARD, outline=EDGE, r=18):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=3)

def chapter(ty, txt, l1="", l2=""):
    d.rectangle([50, ty - 36, 60, ty + 36], fill=GOLD)
    if l1:
        put(l1, font(52, True), (80, ty - 28), anchor="lm", color=WHITE)
        put(l2, font(30, True), (80, ty + 28), anchor="lm", color=LIGHT)
    else:
        put(txt, font(52, True), (80, ty), anchor="lm", color=WHITE)
    d.line([50, ty + 58, 160, ty + 58], fill=GOLD, width=3)

def row(ry, tag, detail, tagcolor=GOLD):
    box(40, ry, W - 80, 130)
    put(tag, font(32, True), (76, ry + 40), anchor="lm", color=tagcolor)
    put(detail, font(16), (76, ry + 88), anchor="lm", color=WHITE, maxw=720)
    return ry + 145

def band(ry, h, lines, lh=72):
    box(40, ry, W - 80, h, r=18)
    sy = ry + lh
    for txt, fnt, color in lines:
        put(txt, fnt, (W / 2, sy), color=color, maxw=W - 180)
        sy += lh
    return ry + h

y = 0
# ---------- 页眉 ----------
y += 42
put("深圳中考 · 问答系列 · 第3篇", font(18, True), (50, y), anchor="lm", color=GOLD)
y += 54
put("滑档去了排名40的高中？先别慌，这不是终点", font(38, True), (50, y), anchor="lm", color=WHITE)
y += 60
put("排名40=录取线557分 · 第35-45名553-561 · 孩子学习好 · 家长决策优", font(16), (50, y), anchor="lm", color=LIGHT, maxw=800)
y += 48
d.line([50, y, 160, y], fill=GOLD, width=3)

# ---------- 01 你其实不算滑档 ----------
y += 82
chapter(y, "01 · 你其实不算「滑档」")
y += 100
for tag, detail, tc in [
    ("冲档落空", "冲的志愿没录上，落到稳/保 → 正常结果，好好规划高中", LIGHT),
    ("稳保落空", "稳和保也没接住 → 已录公办，接受并规划", LIGHT),
    ("全线滑档", "第一批全落空 → 才涉及补录（和本文读者无关）", GOLD),
]:
    y = row(y, tag, detail, tc)
y += 36
put("这意味着什么：多数「滑档去排名40」是冲档落空——冲太高、稳太少、保没垫底。问题不在孩子考砸，在志愿梯度没拉开。", font(17, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 02 排名40什么水平 ----------
chapter(y, "02 · 排名40，到底什么水平")
y += 100
box(40, y, W - 80, 420, r=18)
yy = y + 80
put("第40名 · 深高创新高中", font(24, True), (W / 2, yy), color=WHITE)
yy += 130
put("557分", font(96, True), (W / 2, yy), color=GOLD)
yy += 130
put("第35-45名区间 553-561分 · 第一批中后段公办普高", font(17), (W / 2, yy), color=LIGHT, maxw=W - 160)
y += 420
y += 40
put("这意味着什么：你录到的是公办、有稳定师资、有正常高考通道，部分还有特色班/重点班。滑档≠人生完蛋，以为滑档=完蛋的恐慌，才是最大的损失。", font(17, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 03 两条路 ----------
chapter(y, "03 · 你面前只有两条路")
y += 100
box(40, y, W - 80, 320, r=18)
d.line([W / 2, y + 30, W / 2, y + 290], fill=EDGE, width=3)
put("接受并规划", font(28, True), (265, y + 96), color=GOLD)
put("主路 · 想通排名40不差", font(18), (265, y + 190), color=WHITE)
put("复读", font(28, True), (635, y + 96), color=LIGHT)
put("慎选 · 不能报指标生/自主招生", font(18), (635, y + 190), color=WHITE)
y += 320
y += 40
put("这意味着什么：补录/征求志愿跟你没关系——那是给全线滑档没学上家长的方向，能回的是民办普高/中职（公办无补录窗口）。对已录排名40公办的你，补录是降级，不是补救。", font(17, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 04 分工论 ----------
chapter(y, "", l1="04 · 孩子负责学习好", l2="家长负责决策优")
y += 100
for tag, detail in [
    ("① 没想到政策", "公办第一批录取即锁定 · 补录只对民办 · 复读不能报指标生"),
    ("② 没想到策略", "冲稳保没拉开 · 没留保底志愿 · 指标生不会用"),
    ("③ 没想到数据", "各校历年录取线 · AC/D类分差 · 自己分数段的位置"),
]:
    y = row(y, tag, detail, LIGHT)
y += 36
put("这三件事，都是出分前就能做、且做了真能改变结果的事。这一仗，孩子负责冲锋，家长负责掌舵。", font(17, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 05 转给孩子 ----------
chapter(y, "05 · 把这句话，转给孩子")
y += 100
box(40, y, W - 80, 360, r=18)
put("别让孩子觉得自己「输在了中考」", font(28, True), (W / 2, y + 80), color=WHITE)
put("中考只是定了起点，定不了终点", font(18), (W / 2, y + 150), color=LIGHT)
put("排名40的学校，同样有人考进重点大学", font(28, True), (W / 2, y + 230), color=GOLD)
y += 360
y += 40
put("现在就能做三件事：①对号入座（冲档落空就接受）②接受并规划（查出口数据/特色班/升学路径）③想复读先过清单（失常？自愿？抗压？缺一项都慎重）", font(17, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 06 系列第3篇 · 问答系列 ----------
chapter(y, "06 · 给更多家长的一句话")
y += 100
box(40, y, W - 80, 320, r=18)
put("那位家长的今天，可能就是你家的明天", font(28, True), (W / 2, y + 70), color=GOLD)
put("如果你们也把志愿当「到时候再说」的话", font(17), (W / 2, y + 140), color=SUB)
put("你现在看到这一篇，就是提前做功课的开始", font(24, True), (W / 2, y + 230), color=WHITE)
y += 320
y += 40
box(40, y, W - 80, 760, r=18)
put("你现在读的是《问答系列》第3篇", font(28, True), (W / 2, y + 60), color=GOLD)
put("每个家长高频提问 · 一题一答 · 按顺序读更系统", font(17), (W / 2, y + 116), color=SUB)
# 四条问答，每条两行（标题行+细节行），统一字号 font(17)
f17 = font(17)
qa_rows = [
    ("① 非深户能参加中考读高中吗？", "5项条件 · 3条路"),
    ("② 普高和中职学费差多少？", "公办约1万 · 民办21万-36万"),
    ("③ 滑档去排名40的高中怎么办？", "两条路：接受 or 复读"),
    ("④ 志愿怎么填才不滑档？", "冲稳保梯度怎么排"),
]
sy = y + 210
for title, desc in qa_rows:
    put(title, f17, (76, sy), anchor="lm", color=GOLD, maxw=W - 170)
    sy += 60
    put(desc, f17, (76, sy), anchor="lm", color=WHITE, maxw=W - 170)
    sy += 76
put("更多家长高频提问陆续回答 · 关注不迷路", font(20, True), (W / 2, sy + 10), color=GOLD, maxw=W - 160)
y += 760

# ---------- 页脚 ----------
y += 60
d.line([50, y, 850, y], fill=EDGE, width=3)
y += 60
put("滑档≠人生完蛋，恐慌才是损失。", font(36, True), (W / 2, y), color=WHITE)
y += 66
put("数据，是焦虑最好的解药。", font(18), (W / 2, y), color=LIGHT)
y += 60
put("关注 · 深圳中考系列持续更新 · 把志愿的账提前算清", font(17), (W / 2, y), color=SUB, maxw=W - 80)
y += 52
for s in [
    "数据来源：深圳市教育局《2026年高中阶段学校考试招生工作的通知》《2026年中考报名工作的通知》",
    "深圳市2026年高中阶段学校第一批录取标准（按2026录取线AC类住宿排序）· 名额分配招生计划",
    "录取线、补录、复读的具体规则以当年市招考办公告为准",
]:
    put(s, font(14), (W / 2, y), color=LIGHT, maxw=W - 110)
    y += 50

# ---------- 裁剪到内容实际长度（消除尾部空白） ----------
content_end = y
print("内容底部≈", content_end, "| 画布H=", H, "| 余量=", H - content_end)
final_h = content_end + 60
img2 = img.crop((0, 0, W, final_h))
out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/003+中考滑档去了深圳排名40左右的高中怎么办？/01.公众号/003+中考滑档去了深圳排名40左右的高中怎么办？-公众号-长图-极简版.png"
img2.save(out)
print("saved", img2.size)

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
