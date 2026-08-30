# -*- coding: utf-8 -*-
"""S1-7 抖音分镜头配图 9张（1080×1920 9:16竖屏）
对应 01-S1-7-...-抖音-备考时间线.md 口播脚本。
镜头序列：01核心观点(倒计时300天)→02钩子(不是5月才开始)→03现在到9月(3件事)
→04 10-12月(信息收集)→05 1-3月(定位冲刺)→06 4-5月(决策冲刺/志愿10天)
→07 6月中考→08两条线(孩子拼分数/家长拼决策)→09CTA
复用 S1-6/QA-002 分镜头规范：蓝色基准+光影层次、文字放大1/3、
gap_report 检测文字-边框≥15px/卡间距≥30px、verify 0越界。"""
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


def header(d, checks, tag="深圳中考 · S1 基本态势 · 系列第7篇·收官", y=130):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=980)


def foot(d, checks, txt="数据来源：深圳市教育局官方公开信息 · 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


def list_card(d, checks, ry, num, title, desc, hl=False):
    """编号+标题+说明 列表卡（圆角大卡，编号金圆）"""
    box(d, 90, ry, 900, 230, r=34)
    d.ellipse([150, ry + 85, 230, ry + 165], fill=GOLD)
    put(d, checks, num, font(52, True), (190, ry + 125), color=(18, 30, 55), maxw=80)
    put(d, checks, title, font(46, True), (280, ry + 75), anchor="lm", color=(GOLD if hl else WHITE), maxw=650)
    put(d, checks, desc, font(34), (280, ry + 160), anchor="lm", color=SUB, maxw=650)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/04.抖音/"
P = "01-S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-抖音-备考时间线-镜头"
ALL_OK = True

# ============ 镜头01 核心观点 ============
img, d = new_canvas(0); checks = []
header(d, checks)
d.line([W // 2 - 100, 600, W // 2 + 100, 600], fill=GOLD, width=5)
put(d, checks, "2027 中考", font(72, True, scale=False), (W // 2, 760), color=WHITE, maxw=940)
put(d, checks, "倒计时 300 天", font(90, True, scale=False), (W // 2, 900), color=GOLD, maxw=940)
put(d, checks, "现在开始 · 刚刚好", font(44, True), (W // 2, 1060), color=LIGHT, maxw=900)
box(d, 100, 1240, 880, 220, r=44)
put(d, checks, "9个月 · 每月该做什么", font(42, True), (540, 1350), color=WHITE, maxw=840)
ALL_OK &= gap_report(d, checks, "镜头01", [(100, 1240, 880, 220)])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-核心观点-1080x1920.png")

# ============ 镜头02 钩子 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "离2027中考 还有约300天", font(60, True, scale=False), (W // 2, 560), color=WHITE, maxw=940)
box(d, 90, 700, 900, 220, r=40)
put(d, checks, "现在开始 · 刚刚好", font(48, True), (540, 810), color=GOLD, maxw=840)
d.line([W // 2 - 100, 1000, W // 2 + 100, 1000], fill=GOLD, width=5)
put(d, checks, "但中考不是5月才开始", font(56, True), (W // 2, 1150), color=WHITE, maxw=920)
put(d, checks, "从今年9月开学 就开始了", font(44, True), (W // 2, 1290), color=LIGHT, maxw=920)
ALL_OK &= gap_report(d, checks, "镜头02", [(90, 700, 900, 220)])
verify(d, checks, "镜头02")
img.save(BASE + P + "02-钩子-1080x1920.png")

# ============ 镜头03 现在到9月 · 3件事 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "现在到9月 · 先做3件事", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
cards = []
ry = 420
for n, t, s in [("1", "体育过程性评价", "14分开始累积 · 先确认前两年分数"),
                ("2", "理化实验操作", "计入中考总分"),
                ("3", "搞懂三组数字", "16万考生 · 8万学位 · 52%录取率")]:
    list_card(d, checks, ry, n, t, s)
    cards.append((90, ry, 900, 230))
    ry += 280
put(d, checks, "同时开始浏览目标学校", font(40, True), (W // 2, ry + 10), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头03", cards)
verify(d, checks, "镜头03")
img.save(BASE + P + "03-现在到9月-3件事-1080x1920.png")

# ============ 镜头04 10-12月 信息收集 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "10-12月 · 信息收集期", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
cards = []
ry = 420
for n, t, s in [("1", "研究指标生", "名额分配到校 · 校内竞争"),
                ("2", "锁定目标学校", "按梯队列好 冲·稳·保"),
                ("3", "11月期中定位", "看孩子目前的位置")]:
    list_card(d, checks, ry, n, t, s)
    cards.append((90, ry, 900, 230))
    ry += 280
put(d, checks, "目标越早锁定，方向越早明确", font(40, True), (W // 2, ry + 10), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头04", cards)
verify(d, checks, "镜头04")
img.save(BASE + P + "04-10到12月-信息收集-1080x1920.png")

# ============ 镜头05 1-3月 定位冲刺 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "明年1-3月 · 定位冲刺期", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
cards = []
ry = 420
for n, t, s in [("1", "一模定位", "全市定位 · 填志愿的重要参考"),
                ("2", "政策发布", "盯紧当年招生政策变化"),
                ("3", "3月下旬中考报名", "D类提前备好 社保+居住证")]:
    list_card(d, checks, ry, n, t, s)
    cards.append((90, ry, 900, 230))
    ry += 280
put(d, checks, "材料没备齐，到报名才慌就晚了", font(40, True), (W // 2, ry + 10), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头05", cards)
verify(d, checks, "镜头05")
img.save(BASE + P + "05-1到3月-定位冲刺-1080x1920.png")

# ============ 镜头06 4-5月 决策冲刺 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "明年4-5月 · 决策冲刺期", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
cards = []
ry = 420
for n, t, s in [("1", "二模 + 草拟志愿", "对照分数段调整方案"),
                ("2", "5月下旬志愿填报", "只有约10天窗口",),
                ("3", "先填志愿，后考试", "考完再想就来不及了")]:
    list_card(d, checks, ry, n, t, s, hl=(n == "2"))
    cards.append((90, ry, 900, 230))
    ry += 280
put(d, checks, "志愿方案，决定了孩子走哪条路", font(40, True), (W // 2, ry + 10), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头06", cards)
verify(d, checks, "镜头06")
img.save(BASE + P + "06-4到5月-决策冲刺-1080x1920.png")

# ============ 镜头07 6月中考 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "明年6月 · 中考", font(48, True), (W // 2, 320), color=GOLD, maxw=900)
put(d, checks, "6 月", font(150, True, scale=False), (W // 2, 520), color=WHITE, maxw=940)
put(d, checks, "临门一脚", font(48, True), (W // 2, 700), color=GOLD, maxw=900)
box(d, 90, 800, 900, 240, r=36)
put(d, checks, "前9个月的准备", font(44, True), (540, 900), color=WHITE, maxw=820)
put(d, checks, "都在这一刻兑现", font(42), (540, 990), color=LIGHT, maxw=820)
put(d, checks, "孩子走进考场 · 家长心里有底", font(40, True), (W // 2, 1180), color=SUB, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头07", [(90, 800, 900, 240)])
verify(d, checks, "镜头07")
img.save(BASE + P + "07-6月中考-1080x1920.png")

# ============ 镜头08 两条线 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "孩子拼分数 · 家长拼决策", font(52, True), (W // 2, 340), color=WHITE, maxw=940)
cards = []
box(d, 100, 480, 880, 320, r=36)
cards.append((100, 480, 880, 320))
put(d, checks, "孩子的试卷", font(40, True), (540, 600), color=GOLD, maxw=820)
put(d, checks, "拼的是分数", font(56, True), (540, 700), color=WHITE, maxw=820)
box(d, 100, 860, 880, 320, r=36)
cards.append((100, 860, 880, 320))
put(d, checks, "家长的志愿表", font(40, True), (540, 980), color=GOLD, maxw=820)
put(d, checks, "拼的是决策", font(56, True), (540, 1080), color=WHITE, maxw=820)
put(d, checks, "两份试卷 · 都别交白卷", font(46, True), (W // 2, 1320), color=LIGHT, maxw=940)
ALL_OK &= gap_report(d, checks, "镜头08", cards)
verify(d, checks, "镜头08")
img.save(BASE + P + "08-两条线-1080x1920.png")

# ============ 镜头09 CTA ============
img, d = new_canvas(0); checks = []
header(d, checks)
d.line([W // 2 - 100, 680, W // 2 + 100, 680], fill=GOLD, width=5)
put(d, checks, "备考不迷路", font(72, True, scale=False), (W // 2, 860), color=GOLD, maxw=940)
box(d, 100, 1080, 880, 220, r=44)
put(d, checks, "关注我 · 深圳中考系列", font(46, True), (540, 1190), color=WHITE, maxw=840)
put(d, checks, "收藏这条 · 9个月一步步带你走", font(40), (W // 2, 1450), color=SUB, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头09", [(100, 1080, 880, 220)])
verify(d, checks, "镜头09")
img.save(BASE + P + "09-CTA-1080x1920.png")

print()
print("S1-7 抖音分镜头 9 张完成。ALL_OK =", ALL_OK)
if not ALL_OK:
    print("⚠️ 存在间隙/间距不足，需检查后重新生成")
