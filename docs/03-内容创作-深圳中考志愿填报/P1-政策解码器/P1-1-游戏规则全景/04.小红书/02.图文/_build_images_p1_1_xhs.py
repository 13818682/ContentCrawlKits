# -*- coding: utf-8 -*-
"""P1-1 小红书图文配图（6张：首图 + 正文图1-5，全部 1080×1440 · 3:4）
一卡一个信息点；序号与文字块共中线（block2_lm）；正文文字≥1.5倍；框内留白/框间距达标。
内容：首图(四句话) → 图1(第一句630) → 图2(第二句ACD) → 图3(第三句五批次) → 图4(第四句16志愿) → 图5(时间线+三件事)
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
WARN = (245, 156, 96)
FD = "C:/Windows/Fonts/"

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/04.小红书/02.图文/"
N = "01-P1-1-深圳中考游戏规则-四句话看懂-小红书"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 20:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    ck.append((text, fnt, xy, anchor))
    return fnt


def verify(d, ck, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} @({cx},{cy})")
    print(f"{name}: 共{len(ck)}处文字，{bad}处越界")
    return bad == 0


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=24, width=2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)


def block2_lm(d, ck, x, cy, title, sub, tf, sf, maxw=760, tc=WHITE, sc=LIGHT):
    tb = d.textbbox((0, 0), title, font=tf, anchor="lm")
    sb = d.textbbox((0, 0), sub, font=sf, anchor="lm")
    th, sh = tb[3] - tb[1], sb[3] - sb[1]
    gap = 10
    total = th + gap + sh
    ty = cy - total / 2 + th / 2
    sy = cy + total / 2 - sh / 2
    put(d, ck, title, tf, (x, ty), anchor="lm", color=tc, maxw=maxw)
    put(d, ck, sub, sf, (x, sy), anchor="lm", color=sc, maxw=maxw)


def new_canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.5:
            k = p / 0.5
            col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.5) / 0.5
            col = c_mid * (1 - k) + c_bot * k
        base[y, :, :] = col
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.62 + 0.38 * diag)
    spots = [
        ((0.80, 0.14), (150, 200, 240)),
        ((0.20, 0.20), (120, 180, 235)),
        ((0.74, 0.74), (95, 160, 225)),
        ((0.28, 0.86), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]
    col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    g = np.exp(-dist * dist) * 0.30
    base += col[None, None, :] * g[:, :, None]
    base = np.clip(base, 0, 255)
    img = Image.fromarray(base.astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


def save(img, fn):
    img.save(BASE + fn)
    print("已保存:", fn)


results = {}

# ================= 1. 首图 =================
img, d = new_canvas(0); ck = []
put(d, ck, "深圳中考 · 政策解码器 · 第1篇", font(28, True), (540, 100), color=GOLD)
put(d, ck, "深圳中考游戏规则", font(62, True), (540, 250), color=WHITE, maxw=1000)
put(d, ck, "四句话就讲完", font(110, True), (540, 510), color=GOLD, maxw=980)
put(d, ck, "不是考试 · 是一套游戏规则", font(38), (540, 650), color=LIGHT, maxw=1000)
chip_w, chip_h, chip_gap = 460, 160, 36
cx0 = (W - (2 * chip_w + chip_gap)) // 2
cy0 = 770
for i, (lab, num) in enumerate([("总分", "630分"), ("第一批志愿", "16个")]):
    cx = cx0 + i * (chip_w + chip_gap)
    box(d, cx, cy0, chip_w, chip_h, r=22)
    put(d, ck, lab, font(30), (cx + chip_w // 2, cy0 + 48), color=WHITE, maxw=chip_w - 20)
    put(d, ck, num, font(52, True), (cx + chip_w // 2, cy0 + 118), color=GOLD, maxw=chip_w - 20)
put(d, ck, "ACD三类 · 五批次 · 排队录取", font(30), (540, 1080), color=LIGHT, maxw=1000)
d.rounded_rectangle([220, 1160, 860, 1290], radius=60, fill=GOLD)
put(d, ck, "收藏这张 · 慢慢对照", font(40, True), (540, 1225), color=NAVY)
put(d, ck, "搞懂规则 · 填志愿不踩坑", font(28, True), (540, 1380), color=GOLD, maxw=1000)
results["cover"] = verify(d, ck, "1 首图")
save(img, N + "-首图-1080x1440.png")

# ================= 2. 正文图1 · 第一句630 =================
img, d = new_canvas(1); ck = []
put(d, ck, "第一句 · 总分630", font(34, True), (540, 100), color=GOLD)
put(d, ck, "每1分的来源都不一样", font(52, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 320, 960, 290, r=24)
put(d, ck, "总分", font(36), (540, 410), color=WHITE, maxw=920)
put(d, ck, "630", font(110, True), (540, 530), color=GOLD, maxw=900)
rows = [
    ("440分", "语数英物化 · 主战场", GOLD),
    ("170分", "史道体 · 定公办民办", WHITE),
]
y0, rh, rg = 660, 170, 28
for i, (t, s, tc) in enumerate(rows):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, t, font(52, True), (220, cy), color=tc, maxw=300)
    put(d, ck, s, font(34), (480, cy), color=WHITE, maxw=480)
put(d, ck, "考8科 · 2026实验操作20 · 道法开卷", font(28, True), (540, 1080), color=GOLD, maxw=1020)
put(d, ck, "每1分都有它的位置 · 偏科要不得", font(34, True), (540, 1170), color=WHITE, maxw=1020)
put(d, ck, "下一张：考生分ACD三类", font(26), (540, 1360), color=SUB)
results["s1"] = verify(d, ck, "2 第一句630")
save(img, N + "-正文图1-第一句630-1080x1440.png")

# ================= 3. 正文图2 · 第二句ACD =================
img, d = new_canvas(2); ck = []
put(d, ck, "第二句 · 考生分ACD三类", font(34, True), (540, 100), color=GOLD)
put(d, ck, "户籍决定你站哪条赛道", font(52, True), (540, 215), color=WHITE, maxw=1020)
rows2 = [
    ("A类", "深户+学籍同区 · 都能报", SUB),
    ("C类", "深户+学籍跨区 · 部分受限", SUB),
    ("D类", "非深户 · 占一半以上 · 公办指标约23%", GOLD),
]
y0, rh, rg = 320, 160, 22
for i, (t, s, tc) in enumerate(rows2):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22)
    cy = y + rh // 2
    put(d, ck, t, font(46, True), (190, cy), color=tc, maxw=240)
    # 说明左对齐，从标签右缘(≈236)后起，避免 mm 居中重叠
    put(d, ck, s, font(34), (280, cy), anchor="lm", color=WHITE, maxw=620)
box(d, 60, 880, 960, 210, r=24)
put(d, ck, "D类家长 · 信息准备比什么都重要", font(38, True), (540, 970), color=GOLD, maxw=920)
put(d, ck, "别用分数去硬扛信息差", font(32), (540, 1040), color=LIGHT, maxw=920)
put(d, ck, "下一张：录取分五个批次", font(26), (540, 1360), color=SUB)
results["s2"] = verify(d, ck, "3 第二句ACD")
save(img, N + "-正文图2-第二句ACD-1080x1440.png")

# ================= 4. 正文图3 · 第三句五批次 =================
img, d = new_canvas(3); ck = []
put(d, ck, "第三句 · 录取分五批次", font(34, True), (540, 100), color=GOLD)
put(d, ck, "前一批录了 · 后面全作废", font(52, True), (540, 215), color=WHITE, maxw=1020)
rows3 = [
    ("① 自招批", "1个志愿"),
    ("② 名额分配", "1个 · 指标生"),
    ("③ 第一批", "16个 · 普高≤12+中职≤4"),
    ("④ 第二批", "18个"),
    ("⑤ 第三批", "6个"),
]
y0, rh, rg = 320, 150, 22
for i, (t, s) in enumerate(rows3):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=20)
    cy = y + rh // 2
    put(d, ck, t, font(44, True), (300, cy), color=GOLD if i == 2 else WHITE, maxw=400)
    put(d, ck, s, font(36), (700, cy), color=LIGHT, maxw=340)
put(d, ck, "别填「录了也不想去」的学校", font(38, True), (540, 1260), color=WHITE, maxw=1020)
put(d, ck, "下一张：16个志愿怎么录", font(26), (540, 1360), color=SUB)
results["s3"] = verify(d, ck, "4 第三句五批次")
save(img, N + "-正文图3-第三句五批次-1080x1440.png")

# ================= 5. 正文图4 · 第四句16志愿 =================
img, d = new_canvas(0); ck = []
put(d, ck, "第四句 · 16个志愿", font(34, True), (540, 100), color=GOLD)
put(d, ck, "分高先挑 · 顺序你定", font(52, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 320, 960, 400, r=24)
put(d, ck, "分数优先 · 依照志愿顺序", font(34, True), (540, 420), color=WHITE, maxw=920)
put(d, ck, "排队录取", font(68, True), (540, 560), color=GOLD, maxw=900)
put(d, ck, "分高排前 · 纸条写志愿顺序 · 按顺序找", font(30), (540, 660), color=LIGHT, maxw=920)
acts = [
    ("①", "最想去的放前面", "按喜欢程度从高到低排"),
    ("②", "同分怎么办", "先比生地合卷 · 再比语数英"),
]
y0, rh, rg = 780, 190, 28
for i, (num, t, s) in enumerate(acts):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=24)
    cy = y + rh // 2
    put(d, ck, num, font(56, True), (140, cy), color=GOLD)
    block2_lm(d, ck, 230, cy, t, s, font(42, True), font(32), maxw=780)
put(d, ck, "志愿排序就是你的主动权", font(34, True), (540, 1230), color=WHITE, maxw=1020)
put(d, ck, "下一张：从报名到录取", font(26), (540, 1360), color=SUB)
results["s4"] = verify(d, ck, "5 第四句16志愿")
save(img, N + "-正文图4-第四句16志愿-1080x1440.png")

# ================= 6. 正文图5 · 时间线 + 三件事 =================
img, d = new_canvas(1); ck = []
put(d, ck, "从报名到录取 · 整整6个月", font(34, True), (540, 100), color=GOLD)
put(d, ck, "5个节点 · 错过不能回头", font(52, True), (540, 215), color=WHITE, maxw=1020)
rows5 = [
    ("3月", "报名", "D类5项材料备齐"),
    ("4月", "体育中考", "36分现场"),
    ("5月", "实验+听说", "志愿填报那10天⚠️"),
    ("6月", "自招+文化课", "6.26-28考试"),
    ("7-8月", "出分+分批录取", "7.16出分"),
]
y0, rh, rg = 320, 130, 22
for i, (tm, ev, note) in enumerate(rows5):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=20)
    cy = y + rh // 2
    hot = i == 2
    put(d, ck, tm, font(36, True), (160, cy), color=GOLD if hot else WHITE, maxw=160)
    put(d, ck, ev, font(34, True), (380, cy), color=GOLD if hot else WHITE, maxw=280)
    put(d, ck, note, font(30), (700, cy), color=LIGHT, maxw=320)
put(d, ck, "出分前就能做三件事：记四句话 · 确认类别 · 了解指标生", font(28, True), (540, 1182), color=GOLD, maxw=1020)
put(d, ck, "三件套 · 收藏这条慢慢对照", font(32, True), (540, 1380), color=GOLD, maxw=1020)
results["tl"] = verify(d, ck, "6 时间线")
save(img, N + "-正文图5-时间线三件事-1080x1440.png")

print()
print("全部 OK =", all(results.values()))
