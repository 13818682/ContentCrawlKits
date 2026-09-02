# -*- coding: utf-8 -*-
"""P1-1 主线极简版 · 公众号统一长图 · 大字版（13-1 规范：900宽连续渐变）
大字版说明：正文 ×2.0（渲染32px，手机显示≈14px），章节/数字大字手动放大。
自上而下累加 y 布局，避免坐标漂移。越界+重叠校验。
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
        # 两行标题：主行 l1 在 ty-28，副行 l2 在 ty+26
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

y = 0
# ---------- 页眉 ----------
y += 42
put("深圳中考 · 政策解码器 · 第1篇", font(20, True), (50, y), anchor="lm", color=GOLD)
y += 54
put("深圳中考游戏规则：30分钟从入门到看懂", font(44, True), (50, y), anchor="lm", color=WHITE)
y += 62
put("总分630 · ACD三类 · 五批次 · 16志愿 · 四句话讲完整套规则", font(16), (50, y), anchor="lm", color=LIGHT, maxw=800)
y += 50
d.line([50, y, 160, y], fill=GOLD, width=3)

# ---------- 01 总分630 ----------
y += 82
chapter(y, "01 · 总分630，五科定胜负")
y += 106
y = band(y, 320, [
    ("语数英物化 = 440分 · 占总分70% · 主战场", font(42, True), GOLD),
    ("历史 + 道法 + 体育 = 170分", font(36, True), WHITE),
    ("中等分段 · 这170分决定公办还是民办", font(17), LIGHT),
])
y += 46
put("这意味着什么：每1分都有它的位置，偏科要不得。", font(34, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 02 ACD三类 ----------
chapter(y, "02 · 考生分ACD三类")
y += 116
for tag, detail, tc in [
    ("A类", "深户+学籍同区 · 最宽赛道 · 所有学校都能报", LIGHT),
    ("C类", "深户+学籍跨区 · 部分学校有限制", LIGHT),
    ("D类", "非深户 · 占考生一半以上 · 公办指标仅约23%", GOLD),
]:
    y = row(y, tag, detail, tc)
y += 36
put("这意味着什么：信息准备对D类家长更加重要，别用分数去硬扛信息差。", font(34, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 03 五批次 ----------
chapter(y, "03 · 录取分五个批次")
y += 116
for tag, detail, tc in [
    ("自招 → 名额分配", "前两批各1个志愿 · 录了后面全作废", LIGHT),
    ("第一批", "16个志愿 · 普高≤12 + 中职≤4 · 核心批次", GOLD),
    ("第二、三批", "18个+6个 · 本市/外省中职技校", LIGHT),
]:
    y = row(y, tag, detail, tc)
y += 36
put("这意味着什么：前一批录了后面全部作废，每个批次都别填不想去的学校。", font(34, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 04 排队比喻 ----------
chapter(y, "", l1="04 · 16个志愿", l2="分高先挑 · 顺序你定")
y += 116
box(40, y, W - 80, 520, r=18)
yy = y + 90
put("排队录取", font(36, True), (W / 2, yy), color=GOLD)
yy += 96
put("分数高的排前面，你手里有张纸条写志愿顺序", font(17), (W / 2, yy), color=WHITE)
yy += 76
put("打饭阿姨按纸条找，哪个窗口有饭", font(17), (W / 2, yy), color=WHITE)
yy += 76
put("就安排你到哪", font(17), (W / 2, yy), color=WHITE)
yy += 90
put("不能说「1号没了想去5号」 · 系统只能按顺序来", font(34, True), (W / 2, yy), color=GOLD)
y += 520
y += 46
put("最想去的放前面，从高到低排；同分先比生地合卷，再比语数英。", font(34, True), (W / 2, y), color=GOLD, maxw=W - 110)
y += 82

# ---------- 05 时间线 ----------
chapter(y, "05 · 从报名到录取 · 整整6个月")
y += 116
y = band(y, 270, [
    ("3月报名 → 8月录取结束", font(36, True), GOLD),
    ("5个节点错过不能回头 · 志愿填报那10天是全年最重要决策窗口", font(17), WHITE),
])
y += 82

# ---------- 06 三件事 ----------
chapter(y, "06 · 现在该做的三件事")
y += 116
for tag, detail in [
    ("① 记住四句话", "总分630 · 三类 · 五批 · 16志愿按分排队"),
    ("② 确认孩子类别", "AC还是D · 学籍户籍同不同区 · 定备考基调"),
    ("③ 开始了解指标生", "50%公办学位指标到校 · 校内竞争 · 降分通道"),
]:
    y = row(y, tag, detail, LIGHT)
y += 82

# ---------- 07 系列第1篇 ----------
chapter(y, "07 · 这只是系列第1篇")
y += 116
box(40, y, W - 80, 300, r=18)
put("政策解码器共8篇 · 本篇给全景地图", font(36, True), (W / 2, y + 62), color=GOLD)
put("P1-2~P1-8 逐一深入每条规则", font(17), (W / 2, y + 116), color=SUB)
put("下一篇《630分怎么来的》", font(34, True), (W / 2, y + 190), color=WHITE)
put("那440分主战场，每科怎么拿分", font(34, True), (W / 2, y + 252), color=WHITE)
y += 300
y += 46
# 系列8篇：7条单行，统一字号 36px，等距排列
fnt36 = font(30, True)   # 30px 不触发放大 → 渲染 36px（手机 15.6px）
item_rows = [
    ("① 630分怎么来的：考试科目与2026三大变化", GOLD),
    ("② AC类还是D类：考生类别决定赛道", WHITE),
    ("③ 招生批次与投档规则：电脑怎么录", WHITE),
    ("④ 名额分配：指标生到底是什么", WHITE),
    ("⑤ 自主招生：一类二类区别", WHITE),
    ("⑥ 报名到录取：关键时间节点全流程", WHITE),
    ("⑦ 中考术语速查手册：黑话随时查", GOLD),
]
# 标题区 120 + 7行×行距 72 = 504
box_h = 120 + 7 * 72
box(40, y, W - 80, box_h, r=18)
put("系列8篇 · 按顺序读更系统", font(36, True), (W / 2, y + 64), color=GOLD)
sy = y + 64 + 70
for title, color in item_rows:
    put(title, fnt36, (76, sy), anchor="lm", color=color)
    sy += 72
y += box_h

# ---------- 页脚 ----------
y += 70
d.line([50, y, 850, y], fill=EDGE, width=2)
y += 62
put("搞懂规则，不犯低级错误，本身就是优势。", font(36, True), (W / 2, y), color=WHITE)
y += 70
put("数据，是焦虑最好的解药。", font(17), (W / 2, y), color=LIGHT)
y += 62
put("关注 · 深圳中考政策解码器 · 8篇陪你搞懂每一条规则", font(17), (W / 2, y), color=SUB, maxw=W - 80)
y += 56
for s in [
    "数据来源：深圳市教育局《2026年高中阶段学校考生报考指导手册》",
    "2026年深圳市高中阶段学校第一批录取标准 · 名额分配招生计划（逐条人工核对）",
    "具体规则以当年市招考办公告为准",
]:
    put(s, font(15), (W / 2, y), color=LIGHT, maxw=W - 110)
    y += 50

# ---------- 裁剪到内容实际长度（消除尾部空白） ----------
content_end = y
print("内容底部≈", content_end, "| 画布H=", H, "| 余量=", H - content_end)
# 底部留白 60px
final_h = content_end + 60
img2 = img.crop((0, 0, W, final_h))
img2.save("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/01.公众号/01.主线/P1-1-主线-公众号-长图-极简版.png")
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
