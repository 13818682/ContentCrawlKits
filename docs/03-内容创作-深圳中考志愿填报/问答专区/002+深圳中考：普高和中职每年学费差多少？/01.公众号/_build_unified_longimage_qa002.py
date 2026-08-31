# -*- coding: utf-8 -*-
"""QA-002 公众号极简版 · 统一长图（13-1 规范：900宽连续渐变，金竖条章节头/数字卡/对比块/行盒/系列钩子卡）
内容镜像 002-…-公众号-终版-极简.md：三组数字 → 一年贵25-40倍 → 填错志愿代价 → 对号入座 → 系列第2篇。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 2700
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
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
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
    box(40, ry, W - 80, 95)
    put(tag, font(17, True), (76, ry + 30), anchor="lm", color=tagcolor)
    put(detail, font(14), (76, ry + 64), anchor="lm", color=WHITE, maxw=720)

# ---------- 页眉 ----------
put("深圳中考 · 问答系列 · 第2篇", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("同样读三年书，有人花1万，有人花30万", FBD, (50, 74), anchor="lm", color=WHITE)
put("公办三年约1万 · 民办21万-36万 · 公办中职免学费", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 三年学费四个档 ----------
chapter(208, "01 · 三年学费，四个档")
box_data = [
    ("约1万", "公办普高三年", "80,303人"),
    ("21万-36万", "民办普高三年", "33,195人"),
    ("约3千", "公办中职三年", "免学费 · 15,924人"),
]
for i, (num, lab, note) in enumerate(box_data):
    x = 40 + i * 280
    box(x, 283, 260, 220)
    put(num, font(42, True), (x + 130, 283 + 66), color=GOLD)
    put(lab, font(17, True), (x + 130, 283 + 124), color=WHITE)
    put(note, font(13), (x + 130, 283 + 162), color=SUB)
put("另有民办中职技工：17,330人 · 三年5万-10万", font(13), (W / 2, 534), color=SUB)
put("这意味着什么：同样读三年书，公办约1万，民办21万-36万——差的二十几万，可能是你家几年省吃俭用都攒不下的积蓄。",
    font(15, True), (W / 2, 580), color=GOLD, maxw=W - 80)

# ---------- 02 一年贵25-40倍 ----------
chapter(640, "02 · 一年贵25-40倍")
box(40, 715, W - 80, 180, r=18)
d.line([W / 2, 735, W / 2, 875], fill=EDGE, width=2)
put("民办普高 一年学费", font(17, True), (265, 745), color=WHITE)
put("7万-12万", font(42, True), (265, 815), color=GOLD)
put("= 公办普高的", font(17, True), (635, 745), color=WHITE)
put("25-40倍", font(42, True), (635, 815), color=GOLD)
put("≈ 一个打工人全年工资 · 三年 ≈ 不吃不喝干2-3年", font(15), (W / 2, 930), color=LIGHT)
put("这意味着什么：分数差不多的孩子，一个进公办一年3千，一个滑到民办一年7万——差的是家长有没有提前看清。",
    font(15, True), (W / 2, 982), color=GOLD, maxw=W - 80)

# ---------- 03 填错志愿的代价 ----------
chapter(1042, "03 · 填错志愿，白花钱还错过一条路")
rows_cost = [
    ("① 志愿被动", "分数够不上公办线，只能去民办——不是'不挑'，是被动局面"),
    ("② 信息盲区", "不知道公办中职免学费，里面还有3+4中本贯通（中职3年+本科4年，拿全日制本科文凭）"),
    ("③ 名额太少", "全市3+4仅约300个，15.3万考生抢，知道的人却太少"),
]
ry3 = 1117
for tag, detail in rows_cost:
    row(ry3, tag, detail, LIGHT)
    ry3 += 95 + 15
put("这意味着什么：志愿填错一步，多掏几十万，还可能错过孩子最好的一条路。",
    font(15, True), (W / 2, ry3 + 4), color=GOLD, maxw=W - 80)

# ---------- 04 对号入座 ----------
chapter(ry3 + 60, "04 · 对号入座")
rows_dui = [
    ("成绩稳上公办线", "盯紧公办普高线，志愿别大意", GOLD),
    ("临界生家庭", "先定预算再谈志愿，家里三年能扛多少，决定志愿表下限", GOLD),
    ("考虑中职的家庭", "优先公办中职+贯通通道，别错过免学费的本科路", GOLD),
]
ry4 = ry3 + 135
for tag, detail, tc in rows_dui:
    row(ry4, tag, detail, tc)
    ry4 += 95 + 15
put("现在就能做三件事：①现在开始看数据 ②先定预算再谈志愿 ③公办优先、民办比价、中职看通道",
    font(15, True), (W / 2, ry4 + 4), color=GOLD, maxw=W - 80)

# ---------- 05 系列第2篇 · 问答系列 ----------
chapter(ry4 + 60, "05 · 这只是问答系列第2篇")
band_y = ry4 + 135
box(40, band_y, W - 80, 356, r=18)
put("你现在读的是《问答系列》第2篇", font(16, True), (W / 2, band_y + 40), color=GOLD)
put("每个家长高频提问，一题一答，按顺序读更系统", font(13), (W / 2, band_y + 72), color=SUB)
qa_list = [
    "① 非深户能在深圳参加中考读高中吗？5项条件 · 3条路",
    "② 普高和中职每年学费差多少？公办约1万 · 民办21万-36万（本篇）",
    "③ 民办普高一年到底收多少、值不值？（下篇）",
]
sy = band_y + 112
for s in qa_list:
    put(s, font(14), (76, sy), anchor="lm", color=WHITE, maxw=W - 140)
    sy += 40
put("更多家长高频提问陆续回答 · 关注不迷路", font(14, True), (W / 2, sy + 8), color=GOLD, maxw=W - 120)

# ---------- 页脚 ----------
divy = band_y + 392
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("学费这件事，永远是越早知道越好。", font(26, True), (W / 2, divy + 40), color=WHITE)
put("数据，是焦虑最好的解药。", font(16), (W / 2, divy + 84), color=LIGHT)
put("打开HSEE小程序 · 查学费 / 录取数据 / 贯通名额", font(14), (W / 2, divy + 126), color=SUB)
put("（数据来源：深圳市发改委教育收费标准、深圳市教育局2026年招生计划、中职免学费政策、深圳市统计局2025年平均工资、各校收费公示。逐条人工核对后发布）",
    font(11), (W / 2, divy + 172), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/002+深圳中考：普高和中职每年学费差多少？/01.公众号/002+深圳中考：普高和中职每年学费差多少？-公众号-长图-极简版.png"
img.save(out)
print("saved", img.size)

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
