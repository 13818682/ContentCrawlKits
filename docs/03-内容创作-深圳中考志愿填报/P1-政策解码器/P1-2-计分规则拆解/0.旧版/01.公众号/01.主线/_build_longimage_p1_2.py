# -*- coding: utf-8 -*-
"""P1-2 主线极简版 · 公众号统一长图（13-1 规范：900宽连续渐变，风格对齐 P1-1 长图）
大字版说明：正文 ≤17px ×2.4（渲染~40px，手机≈17px），章节/金句/数据大字手动放大。
自上而下累加 y 布局。越界+重叠校验。深蓝 CARD 实卡，无白色分栏。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 6600
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 2.4))   # 正文 ×2.4（手机显示 ~16.6px）
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

def box(x, y, w, h, fill=CARD, outline=EDGE, r=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def chapter(ty, txt, l1="", l2=""):
    d.rectangle([50, ty - 36, 60, ty + 36], fill=GOLD)
    if l1:
        put(l1, font(52, True), (80, ty - 28), anchor="lm", color=WHITE)
        put(l2, font(34, True), (80, ty + 28), anchor="lm", color=LIGHT)
    else:
        put(txt, font(52, True), (80, ty), anchor="lm", color=WHITE)
    d.line([50, ty + 58, 160, ty + 58], fill=GOLD, width=3)

def row(ry, tag, detail, tagcolor=GOLD):
    box(40, ry, W - 80, 148)
    put(tag, font(36, True), (76, ry + 46), anchor="lm", color=tagcolor)
    put(detail, font(16), (76, ry + 100), anchor="lm", color=WHITE, maxw=680)
    return ry + 162

def band(ry, h, lines, lh=74):
    box(40, ry, W - 80, h, r=18)
    sy = ry + lh
    for txt, fnt, color in lines:
        put(txt, fnt, (W / 2, sy), color=color, maxw=W - 180)
        sy += lh
    return ry + h

def gold_line(y, txt):
    put(txt, font(34, True), (W / 2, y), color=GOLD, maxw=W - 110)
    return y + 82

y = 0
# ---------- 页眉 ----------
y += 42
put("深圳中考 · 政策解码器 · 第2篇", font(20, True), (50, y), anchor="lm", color=GOLD)
y += 54
put("630背后的3个隐藏规则", font(44, True), (50, y), anchor="lm", color=WHITE)
y += 62
put("性价比 · 等级制 · 隐形战场 —— 分数之外的决策智慧", font(16), (50, y), anchor="lm", color=LIGHT, maxw=800)
y += 50
d.line([50, y, 160, y], fill=GOLD, width=3)

# ---------- 01 性价比 ----------
y += 82
chapter(y, "", l1="01 · 性价比", l2="同样的时间 · 花在哪最划算")
y += 106
y = band(y, 320, [
    ("语数英物化 = 440分 · 主战场 · 全力投入", font(42, True), GOLD),
    ("理化实验2026涨到20分 · 8分增量 · 刷题拿不到", font(36, True), WHITE),
    ("历史 + 道法 120分 · 稳定发挥即可 · 别挤占主科", font(17), LIGHT),
])
y += 46
y = gold_line(y, "精力有限 · 花在刀刃上：中等生别在副科题海苦熬")

# ---------- 02 单科等级制 ----------
chapter(y, "", l1="02 · 单科等级制", l2="A+ 永远是全市前5%")
y += 116
for tag, detail, tc in [
    ("A+ = 全市前5%", "固定比例划分 · 试卷再难也是单科顶尖", GOLD),
    ("省一级学校门槛", "所有科目 C+ 及以上 · 体育 C 即可", LIGHT),
    ("不能有一科掉到 C", "等级比分数稳 · 看得出真实位置", LIGHT),
]:
    y = row(y, tag, detail, tc)
y += 36
y = gold_line(y, "等级比分数更准：A+ 永远前5%，掉到C就危险")

# ---------- 03 隐形战场 ----------
chapter(y, "", l1="03 · 隐形战场", l2="不计总分 · 却决定录取")
y += 116
for tag, detail, tc in [
    ("生地 · 合卷100分", "不计入630 · 同分PK时先比生地", GOLD),
    ("552分真实案例", "生地96录取 · 生地82落选 · 差14分", GOLD),
    ("信技 · 艺术 入场券", "报省一级须合格 · 别让合格考翻车", LIGHT),
]:
    y = row(y, tag, detail, tc)
y += 36
y = gold_line(y, "14分的生地差距，就是一个高中学位")

# ---------- 04 现在该做的三件事 ----------
chapter(y, "", l1="04 · 现在该做的三件事", l2="三条马上能用的建议")
y += 116
for tag, detail in [
    ("① 看性价比分配精力", "主战场优先 · 别让副科挤占主科时间"),
    ("② 用等级定位孩子", "哪科在 C 边缘，就是省一级门槛隐患"),
    ("③ 确认两个隐形门槛", "生地心里有数 · 信技艺术确认合格"),
]:
    y = row(y, tag, detail, LIGHT)
y += 82

# ---------- 05 系列第2篇 ----------
chapter(y, "", l1="05 · 这只是政策解码器第2篇", l2="别让信息差 · 吃掉分数")
y += 116
box(40, y, W - 80, 300, r=18)
put("政策解码器共8篇 · 本篇拆解630背后的决策智慧", font(36, True), (W / 2, y + 62), color=GOLD)
put("每条规则都直接影响志愿填报 · 别让信息差吃掉分数", font(17), (W / 2, y + 116), color=SUB, maxw=W - 110)
put("下一篇 · P1-3：AC类还是D类", font(34, True), (W / 2, y + 190), color=WHITE)
put("户籍到底影响什么 · 一次讲透", font(34, True), (W / 2, y + 252), color=WHITE)
y += 300
y += 46
# 系列8篇：统一字号 36px，等距排列
fnt36 = font(30, True)   # 30px 不触发放大 → 渲染 36px（手机 15.6px）
item_rows = [
    ("① 游戏规则全景：30分钟从入门到看懂", WHITE),
    ("② 630背后的3个隐藏规则：性价比·等级·隐形战场", GOLD),
    ("③ AC类还是D类：考生类别决定赛道", WHITE),
    ("④ 招生批次与投档规则：电脑怎么录", WHITE),
    ("⑤ 名额分配：指标生到底是什么", WHITE),
    ("⑥ 报名到录取：关键时间节点全流程", WHITE),
    ("⑦ 中考术语速查手册：黑话随时查", WHITE),
]
box_h = 120 + 8 * 72
box(40, y, W - 80, box_h, r=18)
put("系列8篇 · 按顺序读更系统", font(36, True), (W / 2, y + 64), color=GOLD)
sy = y + 64 + 70
for title, color in item_rows:
    put(title, fnt36, (76, sy), anchor="lm", color=color, maxw=760)
    sy += 72
y += box_h

# ---------- 页脚 ----------
y += 70
d.line([50, y, 850, y], fill=EDGE, width=2)
y += 62
put("搞懂630背后的规则，精力才能花对地方。", font(36, True), (W / 2, y), color=WHITE)
y += 70
put("数据，是焦虑最好的解药。", font(17), (W / 2, y), color=LIGHT)
y += 62
put("关注 · 深圳中考政策解码器 · 8篇陪你搞懂每一条规则", font(17), (W / 2, y), color=SUB, maxw=W - 80)
y += 56
for s in [
    "数据来源：深圳市教育局《2026年高中阶段学校考生报考指导手册》",
    "逐条人工核对后整理 · 具体规则以当年市招考办公告为准",
]:
    put(s, font(15), (W / 2, y), color=LIGHT, maxw=W - 110)
    y += 50

# ---------- 裁剪到内容实际长度 ----------
content_end = y
print("内容底部≈", content_end, "| 余量=", H - content_end)
final_h = content_end + 60
img2 = img.crop((0, 0, W, final_h))
img2.save("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/01.公众号/01.主线/P1-2-主线-公众号-长图-极简版.png")
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
