# -*- coding: utf-8 -*-
"""S1-2 极简版 · 统一长图（风格同 S1-1/S1-3：金竖条章节头/行盒/系列钩子卡，连续渐变）
内容：5 大启示（表格+行盒）+ 对号入座 + 系列第2篇钩子 + 页脚"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 3430
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:                       # 正文文字统一放大1.35倍，展示大字不受影响
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
    if maxw is not None:                                   # 越界自适应：超出maxw/画布则缩小字号
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

def takeaway(ty, txt):
    put(txt, font(15, True), (W / 2, ty), color=GOLD, maxw=W - 80)

# ---------- 页眉 ----------
put("深圳中考 · S1 基本态势 · 系列第2篇", font(14, True), (50, 36), anchor="lm", color=GOLD)
put("2026年数据复盘：给2027届家长的5个启示", FBD, (50, 74), anchor="lm", color=WHITE)
put("15.30万考生 · 101所公办高中分数线全部出炉 · 涨没涨不重要，看对策", font(15), (50, 122), anchor="lm", color=LIGHT)
d.line([50, 156, 140, 156], fill=GOLD, width=3)

# ---------- 01 启示一：四大名校 AC/D 持平 ----------
chapter(208, "01 · 顶尖层，户籍不再是天花板")
box(40, 268, W - 80, 230)
put("学校", font(15, True), (76, 296), anchor="lm", color=LIGHT)
put("AC类住宿", font(15, True), (600, 296), anchor="mm", color=LIGHT)
put("D类住宿", font(15, True), (730, 296), anchor="mm", color=LIGHT)
d.line([76, 322, 800, 322], fill=GOLD, width=2)
tb = [
    ("深圳中学", 592, 592),
    ("深实验（高中部）", 590, 590),
    ("深圳外国语学校", 587, 587),
    ("深高级（中心校区）", 587, 587),
]
ty0 = 352
for name, ac, dc in tb:
    put(name, font(16, True), (76, ty0), anchor="lm", color=WHITE)
    put(str(ac), font(16, True), (600, ty0), anchor="mm", color=GOLD)
    put(str(dc), font(16, True), (730, ty0), anchor="mm", color=GOLD)
    ty0 += 40
takeaway(545, "这意味着什么：目标四大的D类孩子——分数面前人人平等，户籍不再是天花板。")

# ---------- 02 启示二：走读降分 ----------
chapter(600, "02 · 走读，最高能降35分")
rows_02 = [
    ("① 深实验崇文", "住宿506 → 走读471 · 低35分（最大分差案例）"),
    ("② 深理工附中", "住宿559 → 走读526 · 低33分"),
    ("③ 深圳中学", "住宿592 → 走读586 · 低6分 · 全市走读计划7,455人"),
]
ry = 665
for tag, detail in rows_02:
    row(ry, tag, detail, GOLD)
    ry += 110
takeaway(1015, "这意味着什么：代价是不能住校、录取后无法改回。通勤超45分钟，不建议为几分冒险。")

# ---------- 03 启示三：新校三档 ----------
chapter(1070, "03 · 新校首年分化，看谁在办")
rows_03 = [
    ("第一档 · 背靠名校", "深理工附中559 · 深大附中盐田553 · 二高宝安539", GOLD),
    ("第二档 · 潜力股", "益新517 · 启元510", LIGHT),
    ("第三档 · 综合高中", "曙光497 · 创新487", LIGHT),
]
ry3 = 1135
for tag, detail, tc in rows_03:
    row(ry3, tag, detail, tc)
    ry3 += 110
takeaway(1485, "这意味着什么：考虑新校先问“谁在办”——背靠名校首年更稳，独立新办要有当探路者的准备。")

# ---------- 04 启示四：指标生 ----------
chapter(1540, "04 · 指标生，中等学校才是宝藏")
rows_04 = [
    ("四大名校", "降分空间通常仅1-5分 · 名额竞争激烈", GOLD),
    ("30-50名的学校", "降5-15分 · 有的学校甚至低20分以上", LIGHT),
]
ry4 = 1605
for tag, detail, tc in rows_04:
    row(ry4, tag, detail, tc)
    ry4 += 110
takeaway(1850, "这意味着什么：中分段孩子，指标生这一个志愿（只能填1所）最值钱——去查所在初中的名额分配。")

# ---------- 05 启示五：D类 ----------
chapter(1905, "05 · D类：头可冲，底要兜")
rows_05 = [
    ("好消息", "头部D线≈AC线 · 指标生已实现D类全覆盖 · D类占比仅约23%（18,506人）", GOLD),
    ("坏消息", "480-530分段D线仍高AC线5-15分 · 稍有不慎就滑档", LIGHT),
]
ry5 = 1970
for tag, detail, tc in rows_05:
    row(ry5, tag, detail, tc)
    ry5 += 110
takeaway(2215, "这意味着什么：550+冲分数；480-530（尤其D类）从现在起就备好候选方案。")

# ---------- 06 对号入座 ----------
chapter(2270, "06 · 这些数据，对你意味着什么？")
rows_06 = [
    ("550+ · 冲分数", "户籍不构成障碍 · 把精力放在提分上", GOLD),
    ("480-530 · 两手抓", "指标生这张牌最值钱 · 早备民办低进高出 / 3+4 / 3+2候选", GOLD),
    ("考虑新校", "先问谁在办 · 背靠名校的首年风险更可控", LIGHT),
]
ry6 = 2335
for tag, detail, tc in rows_06:
    row(ry6, tag, detail, tc)
    ry6 += 110

# ---------- 07 系列第2篇 · 共7篇 ----------
chapter(2720, "07 · 这只是第2篇 · 共7篇")
band_y = 2790
box(40, band_y, W - 80, 385, r=18)
put("你现在读的是《基本态势》系列第2篇 · 共7篇", font(16, True), (W / 2, band_y + 40), color=GOLD)
put("这个系列帮你从零建立深圳中考的完整认知", font(13), (W / 2, band_y + 70), color=SUB)
series = [
    "启点：2027届家长现在该做什么？",
    "2026年数据复盘：给2027届的5个启示（本篇）",
    "一张图看懂竞争格局",
    "8年考生人数翻倍：深度拆解",
    "52%录取率背后的3个真相",
    "深圳中考全部出路可视化",
    "2027届考生备考时间线",
]
sy = band_y + 110
for i, s in enumerate(series, 1):
    put(f"0{i}  {s}", font(14), (76, sy), anchor="lm", color=WHITE)
    put(f"0{i}", font(14, True), (76, sy), anchor="lm", color=GOLD)
    sy += 34
put("建议按顺序读 · 第3篇：一张图看懂竞争格局——考生、学位、录取率，你的孩子排哪里。",
    font(14, True), (W / 2, band_y + 360), color=GOLD, maxw=W - 100)

# ---------- 页脚 ----------
divy = band_y + 430
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("数据，是焦虑最好的解药。", font(26, True), (W / 2, divy + 36), color=WHITE)
put("“涨没涨”不重要，重要的是涨在哪个层次、你的对策是什么。", font(16), (W / 2, divy + 76), color=LIGHT)
put("2027最新政策发布 · HSEE第一时间更新", font(14), (W / 2, divy + 114), color=SUB)
put("打开HSEE小程序 · 查2026录取数据 / 历年分数线 / 指标生名额", font(13), (W / 2, divy + 146), color=SUB)
put("（核心数据均来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 188), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-2-数据复盘-承前启后/01-公众号/05-S1-2-2026年深圳中考数据复盘：对2027届家长的5个启示-公众号-长图-极简版.png"
img.save(out)
print("saved", out, img.size)

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

# ---------- 采样：渐变连续性 + 关键元素落点 ----------
import numpy as _np
col = _np.array(img)[:, 899, :].astype(int)
mono = all(col[y][0] >= col[y + 1][0] and col[y][2] >= col[y + 1][2] for y in range(0, H - 1, 200))
print("GRADIENT MONOTONE (R down, B down):", "PASS" if mono else "FAIL")
# 金竖条 x50-58 @ chapter y
for cy, lbl in [(208, "ch01"), (600, "ch02"), (1070, "ch03")]:
    px = _np.array(img)[cy, 54, :]
    print(f"GOLDBAR {lbl} @({54},{cy}):", px.tolist())
