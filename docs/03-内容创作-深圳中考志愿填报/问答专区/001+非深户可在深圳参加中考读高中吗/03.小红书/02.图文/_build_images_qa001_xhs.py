# -*- coding: utf-8 -*-
"""QA-001 小红书图文笔记配图（6张：首图 + 5张正文卡，全部 1080×1440 · 3:4）
规范（13-3 小红书模板）：首图大字版 92-104px 冲击钩子；正文图一卡一个信息点；深蓝渐变+金色+微软雅黑。
对应 01-QA-001-...-小红书-图文笔记.md 的配图说明。
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

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/001+非深户可在深圳参加中考读高中吗/03.小红书/02.图文/"
N = "01-QA-001-非深户能在深圳读高中吗-小红书"


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
    return img, ImageDraw.Draw(img), []


def save(img, fn):
    out = BASE + fn
    img.save(out)
    print("已保存:", fn)


results = {}

# ================= 1. 首图（封面） =================
img, d, ck = new_canvas(0)
put(d, ck, "深圳中考 · 问答专区 · 非深户", font(28, True), (540, 96), color=GOLD)
put(d, ck, "非深户能读高中吗？", font(92, True), (540, 268), color=WHITE, maxw=960)
put(d, ck, "能！", font(220, True), (540, 540), color=GOLD, maxw=940)
d.line([540 - 120, 668, 540 + 120, 668], fill=GOLD, width=4)
put(d, ck, "只要满足", font(34), (540, 772), color=LIGHT)
chip_w, chip_h, chip_gap = 300, 96, 40
cx0 = (W - (2 * chip_w + chip_gap)) // 2
cy0 = 836
for i, (num, lab) in enumerate([("5项", "条件"), ("3条", "出路")]):
    cx = cx0 + i * (chip_w + chip_gap)
    box(d, cx, cy0, chip_w, chip_h, r=22)
    put(d, ck, num, font(44, True), (cx + 96, cy0 + chip_h // 2), color=GOLD)
    put(d, ck, lab, font(34), (cx + 96 + 74, cy0 + chip_h // 2), color=WHITE)
put(d, ck, "收藏这张图 · 逐条核对材料", font(30), (540, 1040), color=LIGHT)
d.rounded_rectangle([250, 1120, 830, 1240], radius=60, fill=GOLD)
put(d, ck, "关注 · 深圳中考系列连载", font(40, True), (540, 1180), color=NAVY)
put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(22), (540, 1340), color=SUB)
results["cover"] = verify(d, ck, "1 首图")
save(img, N + "-首图-1080x1440.png")

# ================= 2. 正文图 · 资格5项条件 =================
img, d, ck = new_canvas(1)
put(d, ck, "非深户 · 中考资格", font(28, True), (540, 92), color=GOLD)
put(d, ck, "满足5项条件，才能报公办", font(52, True), (540, 210), color=WHITE, maxw=960)
rows = [
    ("1", "合法稳定职业", "父母一方在深有稳定职业"),
    ("2", "合法稳定住所", "父母一方在深有稳定住所"),
    ("3", "有效居住证", "注意有效期，别过期"),
    ("4", "社保累计满3年", "养老+医疗，补缴不计"),
    ("5", "3年完整初中学籍", "在深完成3年初中"),
]
y0, rh, rg = 330, 172, 22
for i, (num, t, s) in enumerate(rows):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=20)
    put(d, ck, num, font(46, True), (118, y + rh // 2), color=GOLD)
    put(d, ck, t, font(33, True), (218, y + 62), color=WHITE, maxw=740)
    put(d, ck, s, font(26), (218, y + 124), color=LIGHT, maxw=740)
put(d, ck, "条件不全也有路走 → 看下一张", font(26), (540, 1352), color=SUB)
results["qual"] = verify(d, ck, "2 资格5项条件")
save(img, N + "-正文图-资格5项条件-1080x1440.png")

# ================= 3. 正文图 · 条件不全兜底 =================
img, d, ck = new_canvas(2)
put(d, ck, "非深户 · 资格补充", font(28, True), (540, 92), color=GOLD)
put(d, ck, "条件不全 ≠ 没书读", font(58, True), (540, 210), color=WHITE, maxw=960)
put(d, ck, "仍能参加中考，但只能走这两条路", font(30), (540, 296), color=LIGHT)
paths = [
    ("①", "民办普高补录", "AC/D同分录取 · 可作保底"),
    ("②", "中职注册入学", "一样有学上 · 升学路不窄"),
]
y0, ph = 380, 240
for i, (num, t, s) in enumerate(paths):
    y = y0 + i * (ph + 30)
    box(d, 60, y, 960, ph, r=24)
    put(d, ck, num, font(52, True), (150, y + 92), color=GOLD)
    put(d, ck, t, font(40, True), (280, y + 74), color=WHITE, maxw=680)
    put(d, ck, s, font(28), (280, y + 160), color=LIGHT, maxw=680)
box(d, 60, 940, 960, 210, fill=BAND, outline=WARN, r=24, width=3)
put(d, ck, "关键", font(34, True), (150, 1000), color=WARN)
put(d, ck, "条件不全不能报公办普高划线录取", font(30, True), (540, 1000), color=WHITE, maxw=800)
put(d, ck, "只走民办补录 / 中职注册，两条路都通", font(26), (540, 1096), color=LIGHT, maxw=800)
put(d, ck, "报名时间：3月20-27日 · 网上报名", font(28, True), (540, 1268), color=GOLD)
put(d, ck, "5项条件看上一张 →", font(26), (540, 1352), color=SUB)
results["fallback"] = verify(d, ck, "3 条件不全兜底")
save(img, N + "-正文图-条件不全兜底-1080x1440.png")

# ================= 4. 正文图 · 竞争54vs23 =================
img, d, ck = new_canvas(3)
put(d, ck, "非深户 · 竞争", font(28, True), (540, 92), color=GOLD)
put(d, ck, "54%的考生，竞争23%的公办指标", font(48, True), (540, 210), color=WHITE, maxw=980)
bw, bh, bgap = 430, 330, 40
bx0 = (W - (2 * bw + bgap)) // 2
by0 = 340
for i, (num, lab) in enumerate([("54%", "D类考生占比"), ("23%", "公办普高D类指标")]):
    bx = bx0 + i * (bw + bgap)
    box(d, bx, by0, bw, bh, r=26)
    put(d, ck, num, font(108, True), (bx + bw // 2, by0 + 120), color=GOLD)
    put(d, ck, lab, font(30), (bx + bw // 2, by0 + 250), color=WHITE)
put(d, ck, "四大名校 AC线 vs D线 只差 0-5分", font(34, True), (540, 780), color=WHITE, maxw=980)
put(d, ck, "普通校/新校 D线通常高 13-31分", font(28), (540, 872), color=LIGHT)
d.line([540 - 110, 950, 540 + 110, 950], fill=GOLD, width=4)
put(d, ck, "分数越高，户籍差距越小", font(36, True), (540, 1020), color=GOLD)
put(d, ck, "越往下，选校策略越关键", font(28), (540, 1100), color=LIGHT)
put(d, ck, "数据来源：深圳市教育局2026年招生计划", font(22), (540, 1280), color=SUB)
put(d, ck, "出路看下一张 →", font(26), (540, 1352), color=SUB)
results["compete"] = verify(d, ck, "4 竞争54vs23")
save(img, N + "-正文图-竞争54vs23-1080x1440.png")

# ================= 5. 正文图 · 出路三条路 =================
img, d, ck = new_canvas(0)
put(d, ck, "非深户 · 出路", font(28, True), (540, 92), color=GOLD)
put(d, ck, "公办之外，还有两条路", font(52, True), (540, 210), color=WHITE, maxw=960)
ways = [
    ("公办", "D类指标生", "9,186个名额 · 96/97所高中 · 低约20分", GOLD),
    ("民办", "49所 · 同分录取", "AC/D同分 · 学费约3万-15万/年 · 可保底", WHITE),
    ("中职", "3+4中本贯通", "中职3年+本科4年 · 拿全日制本科文凭", WHITE),
]
y0, wh, wg = 330, 250, 26
for i, (t, mid, s, tc) in enumerate(ways):
    y = y0 + i * (wh + wg)
    box(d, 60, y, 960, wh, r=24)
    put(d, ck, t, font(40, True), (180, y + wh // 2), color=tc)
    d.line([280, y + 60, 280, y + wh - 60], fill=EDGE, width=2)
    put(d, ck, mid, font(34, True), (340, y + 84), color=WHITE, maxw=680)
    put(d, ck, s, font(27), (340, y + 168), color=LIGHT, maxw=680)
put(d, ck, "全市普高录取率 超73%", font(44, True), (540, 1300), color=GOLD)
results["ways"] = verify(d, ck, "5 出路三条路")
save(img, N + "-正文图-出路三条路-1080x1440.png")

# ================= 6. 正文图 · 行动核对5项 =================
img, d, ck = new_canvas(1)
put(d, ck, "非深户 · 现在行动", font(28, True), (540, 92), color=GOLD)
put(d, ck, "现在就能做 · 核对5项材料", font(52, True), (540, 210), color=WHITE, maxw=980)
checks = [
    ("☐", "社保断没断", "养老+医疗累计满3年"),
    ("☐", "居住证过没过期", "持有效居住证"),
    ("☐", "学籍连不连贯", "在深3年完整学籍"),
    ("☐", "职业住所材料", "父母一方在深稳定"),
    ("☐", "报名时间", "3月20-27日 · 网上报名"),
]
y0, rh, rg = 320, 166, 20
for i, (mk, t, s) in enumerate(checks):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=20)
    put(d, ck, mk, font(40), (130, y + rh // 2), color=GOLD)
    put(d, ck, t, font(32, True), (218, y + 58), color=WHITE, maxw=720)
    put(d, ck, s, font(25), (218, y + 118), color=LIGHT, maxw=720)
put(d, ck, "别等3月报名才发现 · 收藏这张清单", font(34, True), (540, 1340), color=GOLD)
results["action"] = verify(d, ck, "6 行动核对5项")
save(img, N + "-正文图-行动核对5项-1080x1440.png")

print()
print("全部 OK =", all(results.values()))
