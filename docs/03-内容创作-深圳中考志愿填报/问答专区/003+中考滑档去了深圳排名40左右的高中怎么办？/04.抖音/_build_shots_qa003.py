# -*- coding: utf-8 -*-
"""QA-003 抖音分镜头配图 9张（1080×1920 9:16竖屏）
对应 01-QA-003-...-抖音-滑档真相.md 口播脚本。
镜头序列：01钩子(不叫滑档)→02真滑档vs冲档落空→03排名40区间(557)→04志愿梯度问题
        →05两条路(接受/复读)→06复读限制→07分工论(孩子学习好家长决策优)→08别慌翻盘→09CTA
复用 QA-002 _build_shots_qa002.py 规范：蓝色基准+光影层次、文字放大4/3、
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


def header(d, checks, tag="深圳中考 · 问答系列 · 003", y=130):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=900)


def foot(d, checks, txt="数据来源：深圳市2026年第一批录取标准 · 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/003+中考滑档去了深圳排名40左右的高中怎么办？/04.抖音/"
P = "01-QA-003-中考滑档去了深圳排名40左右的高中怎么办-抖音-滑档真相-镜头"
ALL_OK = True

# ============ 镜头01 钩子 · 不叫滑档 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "滑档去排名40？", font(64, True), (W // 2, 380), color=WHITE, maxw=940)
put(d, checks, "其实不叫滑档", font(88, True, scale=False), (W // 2, 560), color=GOLD, maxw=940)
d.line([W // 2 - 120, 720, W // 2 + 120, 720], fill=GOLD, width=5)
put(d, checks, "孩子多半不是考砸了", font(40, True), (W // 2, 860), color=WHITE, maxw=900)
put(d, checks, "是志愿没填好", font(40, True), (W // 2, 940), color=WHITE, maxw=900)
box(d, 110, 1160, 860, 220, r=100)
put(d, checks, "先别慌 · 看数据再说", font(40, True), (W // 2, 1270), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头01", [(110, 1160, 860, 220)])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-钩子-不叫滑档-1080x1920.png")

# ============ 镜头02 真滑档 vs 冲档落空 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "先分清两种情况", font(56, True), (W // 2, 360), color=GOLD, maxw=900)
rows2 = [
    ("真滑档", "第一批志愿全没接住", SUB),
    ("冲档落空", "冲太高 · 落到了稳/保", GOLD),
]
cy = 560
for t, s, col in rows2:
    box(d, 110, cy, 860, 200, r=30)
    put(d, checks, t, font(44, True), (280, cy + 100), color=col, maxw=280)
    put(d, checks, s, font(32), (620, cy + 100), color=WHITE, maxw=480)
    cy += 260
put(d, checks, "「去排名40」大概率是第二种", font(36, True), (W // 2, 1210), color=GOLD, maxw=920)
put(d, checks, "问题不在分数 · 在志愿梯度", font(34), (W // 2, 1300), color=WHITE, maxw=920)
box(d, 110, 1420, 860, 200, r=100)
put(d, checks, "别把冲档落空当滑档", font(38, True), (W // 2, 1520), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头02", [(110, 560, 860, 200), (110, 820, 860, 200), (110, 1420, 860, 200)])
verify(d, checks, "镜头02")
img.save(BASE + P + "02-真滑档vs冲档落空-1080x1920.png")

# ============ 镜头03 排名40区间 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "排名40 · 到底啥水平？", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
box(d, 110, 500, 860, 340, r=40)
put(d, checks, "第40名录取线", font(36), (W // 2, 600), color=WHITE, maxw=820)
put(d, checks, "557分", font(130, True, scale=False), (W // 2, 750), color=GOLD, maxw=940)
put(d, checks, "第35-45名区间 553-561分", font(34, True), (W // 2, 920), color=WHITE, maxw=820)
put(d, checks, "第一批中后段公办普高", font(40, True), (W // 2, 1180), color=WHITE, maxw=900)
put(d, checks, "师资不差 · 高考出口正常", font(32), (W // 2, 1340), color=LIGHT, maxw=900)
box(d, 110, 1460, 860, 200, r=100)
put(d, checks, "滑档 ≠ 人生完蛋", font(42, True), (W // 2, 1560), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头03", [(110, 500, 860, 340), (110, 1460, 860, 200)])
verify(d, checks, "镜头03")
img.save(BASE + P + "03-排名40区间-1080x1920.png")

# ============ 镜头04 志愿梯度问题 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "为什么会这样？", font(56, True), (W // 2, 360), color=GOLD, maxw=900)
rows4 = [
    ("冲太高", "志愿全填了够不着的学校", LIGHT),
    ("稳太少", "没留够稳妥的梯度", LIGHT),
    ("保没垫底", "没有能兜住的保底志愿", LIGHT),
]
cy4 = 540
for t, s, col in rows4:
    box(d, 110, cy4, 860, 180, r=30)
    put(d, checks, t, font(44, True), (300, cy4 + 90), color=GOLD, maxw=300)
    put(d, checks, s, font(32), (640, cy4 + 90), color=WHITE, maxw=460)
    cy4 += 230
put(d, checks, "志愿梯度没拉开 · 录到了低一档的学校", font(34, True), (W // 2, 1290), color=WHITE, maxw=920)
box(d, 110, 1400, 860, 200, r=100)
put(d, checks, "出分前就该填对", font(40, True), (W // 2, 1500), color=GOLD, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头04", [(110, 540, 860, 180), (110, 770, 860, 180), (110, 1000, 860, 180), (110, 1400, 860, 200)])
verify(d, checks, "镜头04")
img.save(BASE + P + "04-志愿梯度问题-1080x1920.png")

# ============ 镜头05 两条路 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "你只有两条路", font(56, True), (W // 2, 350), color=GOLD, maxw=900)
box(d, 110, 520, 860, 280, r=30)
put(d, checks, "接受并规划", font(46, True), (W // 2, 620), color=WHITE, maxw=820)
put(d, checks, "主路 · 排名40不差，把高中读好", font(32), (W // 2, 720), color=LIGHT, maxw=820)
box(d, 110, 860, 860, 280, r=30)
put(d, checks, "复读", font(46, True), (W // 2, 960), color=GOLD, maxw=820)
put(d, checks, "慎选 · 条件苛刻", font(32), (W // 2, 1060), color=LIGHT, maxw=820)
put(d, checks, "补录/征求志愿跟你无关", font(36, True), (W // 2, 1260), color=WHITE, maxw=920)
put(d, checks, "那是给没学上的家长的 · 回的是民办普高", font(30), (W // 2, 1350), color=LIGHT, maxw=920)
box(d, 110, 1450, 860, 200, r=100)
put(d, checks, "补录是降级 · 不是补救", font(38, True), (W // 2, 1550), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头05", [(110, 520, 860, 280), (110, 860, 860, 280), (110, 1450, 860, 200)])
verify(d, checks, "镜头05")
img.save(BASE + P + "05-两条路-1080x1920.png")

# ============ 镜头06 复读限制 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "复读 · 三个关键限制", font(52, True), (W // 2, 360), color=GOLD, maxw=900)
rows6 = [
    "不能报指标生（名额分配）",
    "不能参加自主招生",
    "等于丢掉两个重要通道",
]
cy6 = 540
for s in rows6:
    box(d, 110, cy6, 860, 160, r=30)
    put(d, checks, s, font(38, True), (W // 2, cy6 + 80), color=WHITE, maxw=780)
    cy6 += 210
put(d, checks, "不是「不甘心」就该复读", font(36, True), (W // 2, 1280), color=GOLD, maxw=920)
put(d, checks, "先过三关：失常？自愿？抗压？", font(32), (W // 2, 1370), color=WHITE, maxw=920)
box(d, 110, 1460, 860, 200, r=100)
put(d, checks, "复读 · 慎选", font(40, True), (W // 2, 1560), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头06", [(110, 540, 860, 160), (110, 750, 860, 160), (110, 960, 860, 160), (110, 1460, 860, 200)])
verify(d, checks, "镜头06")
img.save(BASE + P + "06-复读限制-1080x1920.png")

# ============ 镜头07 分工论 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "中考 · 家长和孩子拼的不一样", font(44, True), (W // 2, 340), color=WHITE, maxw=920)
d.line([W // 2 - 100, 460, W // 2 + 100, 460], fill=GOLD, width=5)
box(d, 110, 560, 860, 240, r=30)
put(d, checks, "孩子", font(40, True), (300, 680), color=WHITE, maxw=260)
put(d, checks, "负责学习好", font(40, True), (640, 680), color=GOLD, maxw=440)
box(d, 110, 860, 860, 240, r=30)
put(d, checks, "家长", font(40, True), (300, 980), color=WHITE, maxw=260)
put(d, checks, "负责决策优", font(40, True), (640, 980), color=GOLD, maxw=440)
put(d, checks, "理解政策 · 研究数据 · 排好志愿梯度", font(32), (W // 2, 1220), color=LIGHT, maxw=920)
box(d, 110, 1340, 860, 200, r=100)
put(d, checks, "孩子冲锋 · 家长掌舵", font(40, True), (W // 2, 1440), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头07", [(110, 560, 860, 240), (110, 860, 860, 240), (110, 1340, 860, 200)])
verify(d, checks, "镜头07")
img.save(BASE + P + "07-分工论-1080x1920.png")

# ============ 镜头08 别慌翻盘 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "别让孩子觉得输了", font(52, True), (W // 2, 360), color=GOLD, maxw=900)
put(d, checks, "中考只是定了起点 · 定不了终点", font(36), (W // 2, 480), color=WHITE, maxw=920)
box(d, 110, 600, 860, 260, r=30)
put(d, checks, "排名40的学校", font(36), (300, 730), color=WHITE, maxw=300)
put(d, checks, "同样有人考进重点大学", font(36, True), (650, 730), color=GOLD, maxw=420)
box(d, 110, 920, 860, 260, r=30)
put(d, checks, "最怕的不是进普通校", font(36), (W // 2, 1000), color=WHITE, maxw=780)
put(d, checks, "是孩子带着「我不行」读三年", font(36, True), (W // 2, 1090), color=GOLD, maxw=780)
put(d, checks, "你镇定 · 孩子才有底气", font(36, True), (W // 2, 1300), color=WHITE, maxw=920)
box(d, 110, 1440, 860, 200, r=100)
put(d, checks, "加油 · 路还长 · 稳稳走", font(42, True), (W // 2, 1540), color=GOLD, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头08", [(110, 600, 860, 260), (110, 920, 860, 260), (110, 1440, 860, 200)])
verify(d, checks, "镜头08")
img.save(BASE + P + "08-别慌翻盘-1080x1920.png")

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
put(d, checks, "下次教你怎么填志愿不滑档", font(34), (W // 2, 1240), color=GOLD, maxw=820)
put(d, checks, "下一期：冲稳保梯度怎么排", font(32), (W // 2, 1420), color=LIGHT, maxw=900)
box(d, 110, 1520, 860, 160, r=80)
put(d, checks, "评论区聊聊：你家孩子什么分段？", font(34, True), (W // 2, 1600), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头09", [(110, 1080, 860, 240), (110, 1520, 860, 160)])
verify(d, checks, "镜头09")
img.save(BASE + P + "09-CTA-1080x1920.png")

print()
print("全部 OK =", ALL_OK)
