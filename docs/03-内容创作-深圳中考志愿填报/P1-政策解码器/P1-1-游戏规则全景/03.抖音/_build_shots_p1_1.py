# -*- coding: utf-8 -*-
"""P1-1 抖音分镜头配图 9张（1080×1920 9:16竖屏）
对应 01-P1-1-...-抖音-四句话看懂.md 口播脚本。
镜头序列：01钩子(四句话就讲完)→02第一句(630总分)→03第二句(ACD三类)→04第三句(五批次)
        →05第四句(16志愿排队)→06时间线→07三件事→08系列预告→09CTA
复用 QA-003 _build_shots_qa003.py 规范：蓝色基准+光影层次、文字放大4/3、
数字居中上(金)+标签居中下(浅灰)垂直对称、gap_report 检测文字-边框间隙≥15px、卡间距≥30px、verify 0越界。"""
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
    return bad == 0


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


def header(d, checks, tag="深圳中考 · 政策解码器 · 第1篇", y=130):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=900)


def foot(d, checks, txt="数据来源：《2026年深圳市高中阶段学校考生报考指导手册》· 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/03.抖音/"
P = "01-P1-1-深圳中考游戏规则-抖音-四句话看懂-镜头"
ALL_OK = True

# ============ 镜头01 钩子 · 四句话就讲完 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "深圳中考", font(64, True), (W // 2, 350), color=WHITE, maxw=940)
put(d, checks, "四句话就讲完了", font(100, True, scale=False), (W // 2, 540), color=GOLD, maxw=940)
d.line([W // 2 - 120, 700, W // 2 + 120, 700], fill=GOLD, width=5)
put(d, checks, "不是考试 · 是一套游戏规则", font(40, True), (W // 2, 850), color=WHITE, maxw=900)
put(d, checks, "搞懂规则 · 填志愿不踩坑", font(40, True), (W // 2, 940), color=WHITE, maxw=900)
box(d, 110, 1160, 860, 220, r=100)
put(d, checks, "先别慌 · 四句话就够", font(40, True), (W // 2, 1270), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头01", [(110, 1160, 860, 220)])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-钩子-四句话就讲完-1080x1920.png")

# ============ 镜头02 第一句 · 总分630 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "第一句 · 总分630", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
box(d, 110, 480, 860, 440, r=40)
put(d, checks, "总分", font(36), (W // 2, 580), color=WHITE, maxw=820)
put(d, checks, "630", font(130, True, scale=False), (W // 2, 740), color=GOLD, maxw=940)
put(d, checks, "考8科 · 语数英物化史道体", font(34, True), (W // 2, 850), color=WHITE, maxw=820)
rows2 = [
    ("440分", "语数英物化 · 主战场", GOLD),
    ("170分", "史道体 · 定公办民办", WHITE),
]
cy = 1000
for t, s, col in rows2:
    box(d, 110, cy, 860, 180, r=30)
    put(d, checks, t, font(44, True), (300, cy + 90), color=col, maxw=300)
    put(d, checks, s, font(32), (640, cy + 90), color=WHITE, maxw=460)
    cy += 230
put(d, checks, "每1分都有它的位置", font(38, True), (W // 2, 1490), color=WHITE, maxw=900)
box(d, 110, 1580, 860, 200, r=100)
put(d, checks, "偏科要不得", font(40, True), (W // 2, 1680), color=GOLD, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头02", [(110, 480, 860, 440), (110, 1000, 860, 180), (110, 1230, 860, 180), (110, 1580, 860, 200)])
verify(d, checks, "镜头02")
img.save(BASE + P + "02-第一句-630总分-1080x1920.png")

# ============ 镜头03 第二句 · ACD三类 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "第二句 · 考生分ACD三类", font(48, True), (W // 2, 340), color=GOLD, maxw=900)
rows3 = [
    ("A类", "深户+学籍同区 · 都能报", LIGHT),
    ("C类", "深户+学籍跨区 · 部分受限", LIGHT),
    ("D类", "非深户 · 占一半以上 · 公办指标23%", GOLD),
]
cy3 = 540
for t, s, col in rows3:
    box(d, 110, cy3, 860, 180, r=30)
    put(d, checks, t, font(44, True), (300, cy3 + 90), color=col, maxw=300)
    put(d, checks, s, font(32), (640, cy3 + 90), color=WHITE, maxw=460)
    cy3 += 230
put(d, checks, "D类家长 · 信息准备比什么都重要", font(36, True), (W // 2, 1310), color=GOLD, maxw=920)
box(d, 110, 1420, 860, 200, r=100)
put(d, checks, "别用分数硬扛信息差", font(38, True), (W // 2, 1520), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头03", [(110, 540, 860, 180), (110, 770, 860, 180), (110, 1000, 860, 180), (110, 1420, 860, 200)])
verify(d, checks, "镜头03")
img.save(BASE + P + "03-第二句-ACD三类-1080x1920.png")

# ============ 镜头04 第三句 · 五批次 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "第三句 · 录取分五批次", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
rows4 = [
    ("① 自招批", "1个志愿", LIGHT),
    ("② 名额分配", "1个志愿 · 指标生", LIGHT),
    ("③ 第一批", "16个志愿 · 核心", GOLD),
    ("④ 第二批", "18个志愿", LIGHT),
    ("⑤ 第三批", "6个志愿", LIGHT),
]
cy4 = 500
for t, s, col in rows4:
    box(d, 110, cy4, 860, 150, r=30)
    put(d, checks, t, font(38, True), (320, cy4 + 75), color=col, maxw=340)
    put(d, checks, s, font(30), (660, cy4 + 75), color=WHITE, maxw=420)
    cy4 += 180
put(d, checks, "前一批录了 · 后面全部作废", font(36, True), (W // 2, 1450), color=GOLD, maxw=920)
box(d, 110, 1560, 860, 200, r=100)
put(d, checks, "别填不想去的学校", font(38, True), (W // 2, 1660), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头04", [(110, 500, 860, 150), (110, 680, 860, 150), (110, 860, 860, 150), (110, 1040, 860, 150), (110, 1220, 860, 150), (110, 1560, 860, 200)])
verify(d, checks, "镜头04")
img.save(BASE + P + "04-第三句-五批次-1080x1920.png")

# ============ 镜头05 第四句 · 16志愿排队 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "第四句 · 16个志愿", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
box(d, 110, 460, 860, 620, r=40)
put(d, checks, "分数优先 · 依照志愿顺序", font(34, True), (W // 2, 560), color=WHITE, maxw=820)
put(d, checks, "排队录取", font(56, True), (W // 2, 700), color=GOLD, maxw=820)
put(d, checks, "分高排前", font(30), (W // 2, 800), color=LIGHT, maxw=820)
put(d, checks, "你手里有张纸条写志愿顺序", font(30), (W // 2, 860), color=LIGHT, maxw=820)
put(d, checks, "打饭阿姨按纸条找", font(30), (W // 2, 930), color=LIGHT, maxw=820)
put(d, checks, "哪个窗口有饭就安排你", font(30), (W // 2, 990), color=LIGHT, maxw=820)
put(d, checks, "最想去的放前面 · 从高到低排", font(40, True), (W // 2, 1330), color=WHITE, maxw=920)
put(d, checks, "同分先比生地合卷 · 再比语数英", font(32), (W // 2, 1450), color=LIGHT, maxw=920)
box(d, 110, 1580, 860, 200, r=100)
put(d, checks, "顺序自己定 · 主动权在你", font(38, True), (W // 2, 1680), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头05", [(110, 460, 860, 620), (110, 1580, 860, 200)])
verify(d, checks, "镜头05")
img.save(BASE + P + "05-第四句-16志愿排队-1080x1920.png")

# ============ 镜头06 时间线 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "从报名到录取 · 整整6个月", font(48, True), (W // 2, 340), color=GOLD, maxw=900)
rows6 = [
    "3月 报名 → 4月 体育中考",
    "5月 实验+听说 → 5月下旬 ⚠️志愿填报",
    "6月 自招+文化课 → 7月16日出分",
    "7-8月 分批录取 → 8月录取结束",
]
cy6 = 500
for s in rows6:
    box(d, 110, cy6, 860, 150, r=30)
    put(d, checks, s, font(34, True), (W // 2, cy6 + 75), color=WHITE, maxw=780)
    cy6 += 180
put(d, checks, "志愿填报那10天 · 全年最重要", font(36, True), (W // 2, 1330), color=GOLD, maxw=920)
box(d, 110, 1440, 860, 200, r=100)
put(d, checks, "错过不能回头 · 现在就能准备", font(34, True), (W // 2, 1540), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头06", [(110, 500, 860, 150), (110, 680, 860, 150), (110, 860, 860, 150), (110, 1040, 860, 150), (110, 1440, 860, 200)])
verify(d, checks, "镜头06")
img.save(BASE + P + "06-时间线-1080x1920.png")

# ============ 镜头07 三件事 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "现在该做的三件事", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
rows7 = [
    ("① 记住四句话", "630 · 三类 · 五批 · 16志愿"),
    ("② 确认类别", "AC还是D · 定备考基调"),
    ("③ 了解指标生", "50%公办学位 · 降分通道"),
]
cy7 = 480
for t, s in rows7:
    box(d, 110, cy7, 860, 250, r=30)
    put(d, checks, t, font(38, True), (170, cy7 + 80), anchor="lm", color=WHITE, maxw=760)
    put(d, checks, s, font(32), (170, cy7 + 170), anchor="lm", color=GOLD, maxw=760)
    cy7 += 300
box(d, 110, 1480, 860, 200, r=100)
put(d, checks, "出分前就能做 · 做了改变结果", font(34, True), (W // 2, 1580), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头07", [(110, 480, 860, 250), (110, 780, 860, 250), (110, 1080, 860, 250), (110, 1480, 860, 200)])
verify(d, checks, "镜头07")
img.save(BASE + P + "07-三件事-1080x1920.png")

# ============ 镜头08 系列预告 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "这只是系列第1篇", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
put(d, checks, "政策解码器 · 共8篇", font(36), (W // 2, 450), color=WHITE, maxw=900)
rows8 = [
    "P1-2 630分怎么来的",
    "P1-3 AC类还是D类",
    "P1-4 招生批次与投档",
    "P1-5 名额分配 · 指标生",
    "P1-6 自主招生 · P1-7 时间线",
    "P1-8 术语速查手册",
]
cy8 = 560
for s in rows8:
    box(d, 110, cy8, 860, 120, r=30)
    put(d, checks, s, font(30, True), (W // 2, cy8 + 60), color=WHITE, maxw=780)
    cy8 += 150
put(d, checks, "下一篇 · 630分怎么来的", font(36, True), (W // 2, 1530), color=GOLD, maxw=920)
box(d, 110, 1650, 860, 160, r=80)
put(d, checks, "按顺序读更系统 · 关注不迷路", font(32, True), (W // 2, 1730), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头08", [(110, 560, 860, 120), (110, 710, 860, 120), (110, 860, 860, 120), (110, 1010, 860, 120), (110, 1160, 860, 120), (110, 1310, 860, 120), (110, 1650, 860, 160)])
verify(d, checks, "镜头08")
img.save(BASE + P + "08-系列预告-1080x1920.png")

# ============ 镜头09 CTA ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "孩子负责学习好", font(52, True), (W // 2, 420), color=WHITE, maxw=900)
put(d, checks, "家长负责决策优", font(68, True, scale=False), (W // 2, 560), color=GOLD, maxw=940)
d.line([W // 2 - 100, 700, W // 2 + 100, 700], fill=GOLD, width=5)
put(d, checks, "政策 · 数据 · 志愿梯度", font(38, True), (W // 2, 830), color=WHITE, maxw=900)
put(d, checks, "出分前就该做功课", font(38, True), (W // 2, 920), color=WHITE, maxw=900)
box(d, 110, 1080, 860, 240, r=60)
put(d, checks, "关注我", font(44, True), (W // 2, 1160), color=WHITE, maxw=820)
put(d, checks, "下一篇讲630分怎么来的", font(34), (W // 2, 1240), color=GOLD, maxw=820)
put(d, checks, "四句话记住 · 填志愿不慌", font(32), (W // 2, 1420), color=LIGHT, maxw=900)
box(d, 110, 1520, 860, 160, r=80)
put(d, checks, "评论区聊聊：你家孩子升初几？", font(34, True), (W // 2, 1600), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头09", [(110, 1080, 860, 240), (110, 1520, 860, 160)])
verify(d, checks, "镜头09")
img.save(BASE + P + "09-CTA-1080x1920.png")

print()
print("全部 OK =", ALL_OK)
