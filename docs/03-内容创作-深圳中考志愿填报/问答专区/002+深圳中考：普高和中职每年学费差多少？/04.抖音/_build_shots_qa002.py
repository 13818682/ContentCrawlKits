# -*- coding: utf-8 -*-
"""QA-002 抖音分镜头配图 9张（1080×1920 9:16竖屏）v2 —— 按公众号精简版V3「三笔账」重排
对应 01-QA-002-...-抖音-学费账.md 口播脚本 v2。
镜头序列：01核心观点→02钩子(三笔账预览)→03第一笔(三年总账)→04第二笔(工资负担/同分对比)
        →05第三笔(志愿失误)→06公办中职(贯通机会)→07你不是一个人→08三件事→09CTA
复用 S1-6 _build_shots_s1_6.py 规范：蓝色基准+光影层次、文字放大1/3、
数字居中上(金)+标签居中下(浅灰)垂直对称（防水平重叠）、gap_report 检测
文字-边框间隙≥15px、卡间距≥30px、verify 0 越界。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1080, 1920
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
SC = 4 / 3


def font(size, bold=False, scale=True):
    if scale:
        size = int(round(size * SC))
    if size <= 17:
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def new_canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.55:
            k = p / 0.55
            col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.55) / 0.45
            col = c_mid * (1 - k) + c_bot * k
        base[y, :, :] = col
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.60 + 0.40 * diag)
    spots = [
        ((0.78, 0.15), (150, 200, 240)),
        ((0.22, 0.20), (120, 180, 235)),
        ((0.72, 0.72), (95, 160, 225)),
        ((0.30, 0.85), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]
    col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    g = np.exp(-dist * dist) * 0.30
    base += col[None, None, :] * g[:, :, None]
    dist2 = np.sqrt(((xx - 0.12 * W) / (W * 0.35)) ** 2 + ((yy - 0.86 * H) / (H * 0.30)) ** 2)
    g2 = np.exp(-dist2 * dist2) * 0.16
    base += np.array((70, 140, 210), np.float32)[None, None, :] * g2[:, :, None]
    dist3 = np.sqrt(((xx - 0.90 * W) / (W * 0.40)) ** 2 + ((yy - 0.92 * H) / (H * 0.25)) ** 2)
    g3 = np.exp(-dist3 * dist3) * 0.12
    base += np.array((150, 110, 60), np.float32)[None, None, :] * g3[:, :, None]
    base = np.clip(base, 0, 255)
    img = Image.fromarray(base.astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


def put(d, checks, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
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
    checks.append((text, fnt, xy, anchor))


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=30):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=3)


def verify(d, checks, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in checks:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy})")
    print(f"{name}: 共{len(checks)}处文字，{bad}处越界")


def gap_report(d, checks, name, cards):
    print(f"--- {name} 间隙检测 ---")
    ok = True
    for ci, (x, y, w, h) in enumerate(cards):
        mt = mb = ml = mr = 10 ** 9
        for (text, fnt, (cx, cy), anchor) in checks:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + cx, bb[1] + cy
            x1, y1 = bb[2] + cx, bb[3] + cy
            if x < cx < x + w and y < cy < y + h:
                mt = min(mt, y0 - y); mb = min(mb, y + h - y1)
                ml = min(ml, x0 - x); mr = min(mr, x + w - x1)
        flag = "OK" if (mt >= 15 and mb >= 15 and ml >= 15 and mr >= 15) else "⚠️ 间隙不足"
        if flag != "OK":
            ok = False
        print(f"  卡{ci+1} ({x},{y} {w}x{h}): 上{mt} 下{mb} 左{ml} 右{mr}  {flag}")
    if len(cards) > 1:
        for i in range(len(cards) - 1):
            gap = cards[i + 1][1] - (cards[i][1] + cards[i][3])
            flag = "OK" if gap >= 30 else "⚠️ 过窄"
            if flag != "OK":
                ok = False
            print(f"  卡间距{i+1}-{i+2}: {gap}px  {flag}")
    return ok


def header(d, checks, tag="深圳中考 · 问答系列 · 002", y=130):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=900)


def foot(d, checks, txt="数据来源：深圳市教育局2026年招生计划 · 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/002+深圳中考：普高和中职每年学费差多少？/04.抖音/"
P = "01-QA-002-普高和中职学费差多少-抖音-学费账-镜头"
ALL_OK = True

# ============ 镜头01 核心观点 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "深圳中考 · 学费账", font(56, True), (W // 2, 330), color=GOLD, maxw=900)
put(d, checks, "普高和中职 · 三年学费差多少", font(38), (W // 2, 430), color=WHITE, maxw=900)
d.line([W // 2 - 100, 600, W // 2 + 100, 600], fill=GOLD, width=5)
put(d, checks, "公办 1 万", font(100, True, scale=False), (W // 2, 790), color=WHITE, maxw=940)
put(d, checks, "民办 30 万", font(100, True, scale=False), (W // 2, 940), color=GOLD, maxw=940)
put(d, checks, "同样读三年书 · 差距 25-40 倍", font(48, True), (W // 2, 1130), color=LIGHT, maxw=900)
box(d, 110, 1320, 860, 200, r=100)
put(d, checks, "先算三笔账", font(40, True), (W // 2, 1420), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头01", [(110, 1320, 860, 200)])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-核心观点-1080x1920.png")

# ============ 镜头02 钩子 · 三笔账预览 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "先算三笔账", font(72, True, scale=False), (W // 2, 420), color=WHITE, maxw=940)
put(d, checks, "深圳中考学费 · 差得多离谱", font(38), (W // 2, 545), color=GOLD, maxw=900)
rows2 = [
    ("第一笔 · 学费差距", "公办三年约1万 vs 民办21万-36万", GOLD),
    ("第二笔 · 工资负担", "一年 7万-12万 ≈ 打工人全年工资", WHITE),
    ("第三笔 · 志愿失误", "白花钱 · 还错过孩子的好路径", GOLD),
]
cards2 = []
ry2 = 640
for t, s, col in rows2:
    box(d, 120, ry2, 840, 180, r=34)
    cards2.append((120, ry2, 840, 180))
    cy2 = ry2 + 90
    put(d, checks, t, font(44, True), (540, cy2 - 40), color=WHITE, maxw=780)
    put(d, checks, s, font(32), (540, cy2 + 48), color=col, maxw=780)
    ry2 += 180 + 34
ALL_OK &= gap_report(d, checks, "镜头02", cards2)
verify(d, checks, "镜头02")
img.save(BASE + P + "02-钩子-1080x1920.png")

# ============ 镜头03 第一笔 · 三年总账 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "第一笔 · 三年总账", font(48, True), (W // 2, 290), color=GOLD, maxw=900)
rows = [("约 1 万", "公办普高 · 三年", GOLD), ("21万-36万", "民办普高 · 三年", GOLD),
        ("约 3 千", "公办中职 · 三年(免学费)", GOLD), ("5万-10万", "民办中职 · 三年", GOLD)]
cards = []
ry = 410
for num, lab, col in rows:
    box(d, 120, ry, 840, 200, r=30)
    cards.append((120, ry, 840, 200))
    cy = ry + 100
    put(d, checks, num, font(56, True), (540, cy - 38), color=col, maxw=760)
    put(d, checks, lab, font(34), (540, cy + 52), color=SUB, maxw=760)
    ry += 200 + 30
put(d, checks, "公办三年1万 · 民办三年25万起，差 25-40 倍", font(40, True), (W // 2, ry + 18), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头03", cards)
verify(d, checks, "镜头03")
img.save(BASE + P + "03-第一笔-三年总账-1080x1920.png")

# ============ 镜头04 第二笔 · 工资负担 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "第二笔 · 更扎心", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
put(d, checks, "一年 7万-12万", font(84, True, scale=False), (W // 2, 470), color=WHITE, maxw=900)
put(d, checks, "≈ 一个打工人全年工资", font(40), (W // 2, 600), color=SUB, maxw=900)
box(d, 90, 700, 900, 240, r=36)
put(d, checks, "分数差不多的孩子", font(38), (540, 760), color=SUB, maxw=820)
put(d, checks, "公办 3千/年", font(48, True), (300, 855), color=WHITE, maxw=380)
put(d, checks, "民办 7万/年", font(48, True), (780, 855), color=GOLD, maxw=380)
put(d, checks, "这钱，花得冤不冤？", font(46, True), (W // 2, 1080), color=LIGHT, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头04", [(90, 700, 900, 240)])
verify(d, checks, "镜头04")
img.save(BASE + P + "04-第二笔-工资负担-1080x1920.png")

# ============ 镜头05 第三笔 · 志愿失误 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "第三笔 · 最怕填错志愿", font(48, True), (W // 2, 300), color=GOLD, maxw=920)
box(d, 90, 420, 900, 230, r=34)
put(d, checks, "很多孩子进民办是被动的", font(44, True), (540, 500), color=WHITE, maxw=820)
put(d, checks, "分数够不上公办线 · 没得选", font(34), (540, 585), color=SUB, maxw=820)
d.line([W // 2 - 100, 730, W // 2 + 100, 730], fill=GOLD, width=5)
put(d, checks, "填错一步", font(56, True), (W // 2, 840), color=WHITE, maxw=900)
put(d, checks, "多掏几十万 · 还错过好路径", font(44, True), (W // 2, 950), color=GOLD, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头05", [(90, 420, 900, 230)])
verify(d, checks, "镜头05")
img.save(BASE + P + "05-第三笔-志愿失误-1080x1920.png")

# ============ 镜头06 公办中职 · 贯通机会 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "公办中职 · 被忽略的好路", font(48, True), (W // 2, 300), color=GOLD, maxw=920)
put(d, checks, "免学费", font(96, True, scale=False), (W // 2, 470), color=WHITE, maxw=900)
put(d, checks, "还有 3+4 贯通本科", font(40), (W // 2, 600), color=SUB, maxw=900)
box(d, 90, 700, 900, 240, r=36)
put(d, checks, "全市贯通名额 约 3,000 多个", font(44, True), (540, 770), color=WHITE, maxw=820)
put(d, checks, "3+4 中本贯通 只有 300 个", font(40), (540, 870), color=GOLD, maxw=820)
put(d, checks, "知道的人太少 · 好多人白白错过", font(44, True), (W // 2, 1080), color=LIGHT, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头06", [(90, 700, 900, 240)])
verify(d, checks, "镜头06")
img.save(BASE + P + "06-公办中职-贯通机会-1080x1920.png")

# ============ 镜头07 你不是一个人 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "你不是一个人在焦虑", font(62, True, scale=False), (W // 2, 500), color=WHITE, maxw=940)
box(d, 90, 680, 900, 260, r=40)
put(d, checks, "这些数字、这些坑", font(42, True), (540, 780), color=WHITE, maxw=820)
put(d, checks, "我们帮你提前看清", font(48, True), (540, 880), color=GOLD, maxw=820)
put(d, checks, "少踩坑 · 做当下最好的选择", font(44, True), (W // 2, 1100), color=LIGHT, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头07", [(90, 680, 900, 260)])
verify(d, checks, "镜头07")
img.save(BASE + P + "07-你不是一个人-1080x1920.png")

# ============ 镜头08 三件事 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "现在就能做的三件事", font(54, True), (W // 2, 300), color=WHITE, maxw=900)
rows = [("1", "现在就开始看数据", "公办录取线 / 民办学费 / 贯通专业"),
        ("2", "先定预算，再谈志愿", "别等录取了才发现上不起"),
        ("3", "公办优先 · 民办比价", "中职要看贯通通道")]
cards = []
ry = 420
for n, t, s in rows:
    box(d, 90, ry, 900, 230, r=34)
    cards.append((90, ry, 900, 230))
    d.ellipse([150, ry + 85, 230, ry + 165], fill=GOLD)
    put(d, checks, n, font(52, True), (190, ry + 125), color=(18, 30, 55), maxw=80)
    put(d, checks, t, font(46, True), (280, ry + 75), anchor="lm", color=WHITE, maxw=650)
    put(d, checks, s, font(34), (280, ry + 160), anchor="lm", color=SUB, maxw=650)
    ry += 230 + 50
put(d, checks, "学费这件事，越早知道越好", font(46, True), (W // 2, ry + 30), color=GOLD, maxw=940)
ALL_OK &= gap_report(d, checks, "镜头08", cards)
verify(d, checks, "镜头08")
img.save(BASE + P + "08-三件事-1080x1920.png")

# ============ 镜头09 CTA ============
img, d = new_canvas(0); checks = []
header(d, checks)
d.line([W // 2 - 100, 720, W // 2 + 100, 720], fill=GOLD, width=5)
put(d, checks, "学费这件事", font(72, True, scale=False), (W // 2, 890), color=WHITE, maxw=900)
put(d, checks, "越早知道越好", font(72, True, scale=False), (W // 2, 1030), color=GOLD, maxw=900)
box(d, 100, 1220, 880, 210, r=42)
put(d, checks, "关注我 · 深圳中考系列", font(46, True), (540, 1325), color=WHITE, maxw=840)
put(d, checks, "少踩坑 · 做当下最好的选择", font(40), (W // 2, 1560), color=SUB, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头09", [(100, 1220, 880, 210)])
verify(d, checks, "镜头09")
img.save(BASE + P + "09-CTA-1080x1920.png")

print()
print("QA-002 抖音分镜头 9 张 v2（三笔账重排）完成。ALL_OK =", ALL_OK)
if not ALL_OK:
    print("⚠️ 存在间隙/间距不足，需检查后重新生成")
