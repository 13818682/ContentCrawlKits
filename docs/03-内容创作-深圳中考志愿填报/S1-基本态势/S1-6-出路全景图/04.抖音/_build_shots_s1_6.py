# -*- coding: utf-8 -*-
"""S1-6 抖音分镜头配图 9张（1080×1920 9:16竖屏）v5
对应 01-S1-6-...-抖音-4条出路.md 口播脚本。
v4→v5：数据卡改为「数字居中上 + 标签居中下」垂直对称布局（修复数字/标签水平重叠），
并新增边框-文字间隙检测（gap_report）与卡间距检测。"""
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
    """检测每张卡片内文字距边框的间隙（上/下/左/右最小px），以及卡间距"""
    print(f"--- {name} 间隙检测 ---")
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
        print(f"  卡{ci+1} ({x},{y} {w}x{h}): 上{mt} 下{mb} 左{ml} 右{mr}  {flag}")
    if len(cards) > 1:
        for i in range(len(cards) - 1):
            gap = cards[i + 1][1] - (cards[i][1] + cards[i][3])
            print(f"  卡间距{i+1}-{i+2}: {gap}px  {'OK' if gap >= 30 else '⚠️ 过窄'}")


def header(d, checks, tag="深圳中考 · 出路全景", y=130):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=900)


def foot(d, checks, txt="数据来源：深圳市教育局官方公开信息 · 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-6-出路全景图/04.抖音/"
P = "01-S1-6-一张图看懂深圳中考全部出路-抖音-4条出路-镜头"

# ============ 镜头01 核心观点 ============
img, d = new_canvas(0); checks = []
header(d, checks)
d.line([W // 2 - 100, 600, W // 2 + 100, 600], fill=GOLD, width=5)
put(d, checks, "中考不止", font(104, True, scale=False), (W // 2, 790), color=WHITE, maxw=940)
put(d, checks, "公办一条路", font(104, True, scale=False), (W // 2, 940), color=WHITE, maxw=940)
put(d, checks, "其实有 4 层出路", font(58, True), (W // 2, 1130), color=GOLD, maxw=900)
box(d, 110, 1300, 860, 210, r=105)
put(d, checks, "146,752 个学位 · 180 所学校", font(40, True), (W // 2, 1405), color=WHITE, maxw=820)
gap_report(d, checks, "镜头01", [(110, 1300, 860, 210)])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-核心观点-1080x1920.png")

# ============ 镜头02 钩子 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "给孩子查学校", font(84, True, scale=False), (W // 2, 620), color=WHITE, maxw=940)
box(d, 90, 780, 900, 210, r=40)
put(d, checks, "90% 的家长，只搜「公办普高」", font(46, True), (W // 2, 885), color=LIGHT, maxw=860)
d.line([W // 2 - 100, 1100, W // 2 + 100, 1100], fill=GOLD, width=5)
put(d, checks, "但你孩子的路", font(64, True), (W // 2, 1230), color=WHITE, maxw=920)
put(d, checks, "远不止这一条", font(64, True), (W // 2, 1340), color=GOLD, maxw=920)
gap_report(d, checks, "镜头02", [(90, 780, 900, 210)])
verify(d, checks, "镜头02")
img.save(BASE + P + "02-钩子-1080x1920.png")

# ============ 镜头03 第一层 公办普高 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "第一层 · 公办普高", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
# 数据卡：数字居中上(金色) + 标签居中下(浅灰)，垂直对称
rows = [("约 8 万", "招生学位"), ("101 所", "公办普高"), ("约 52%", "录取率")]
cards = []
ry = 420
for num, lab in rows:
    box(d, 120, ry, 840, 240, r=30)
    cards.append((120, ry, 840, 240))
    cy = ry + 120
    put(d, checks, num, font(84, True), (540, cy - 45), color=GOLD, maxw=760)
    put(d, checks, lab, font(50), (540, cy + 62), color=SUB, maxw=760)
    ry += 240 + 44
put(d, checks, "大多数家长的首选目标", font(40), (W // 2, ry + 28), color=LIGHT, maxw=900)
gap_report(d, checks, "镜头03", cards)
verify(d, checks, "镜头03")
img.save(BASE + P + "03-公办普高-1080x1920.png")

# ============ 镜头04 第二层 民办普高 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "第二层 · 民办普高", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
rows = [("33,195", "招生人数"), ("49 所", "民办普高")]
cards = []
ry = 430
for num, lab in rows:
    box(d, 120, ry, 840, 220, r=30)
    cards.append((120, ry, 840, 220))
    cy = ry + 110
    put(d, checks, num, font(82, True), (540, cy - 40), color=GOLD, maxw=760)
    put(d, checks, lab, font(48), (540, cy + 55), color=SUB, maxw=760)
    ry += 220 + 40
box(d, 120, ry, 840, 210, r=30)
cards.append((120, ry, 840, 210))
cy = ry + 105
put(d, checks, "AC类和D类 同分录取", font(46, True), (540, cy - 45), color=WHITE, maxw=800)
put(d, checks, "D 类家长的重要补充选项", font(34), (540, cy + 45), color=SUB, maxw=800)
ry += 210 + 40
box(d, 120, ry, 840, 170, r=30)
cards.append((120, ry, 840, 170))
put(d, checks, "学费 3万-15万 / 年", font(40), (540, ry + 85), color=LIGHT, maxw=800)
gap_report(d, checks, "镜头04", cards)
verify(d, checks, "镜头04")
img.save(BASE + P + "04-民办普高-1080x1920.png")

# ============ 镜头05 第三层 中职技工 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "第三层 · 中职技工", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
rows = [("33,254", "招生人数"), ("30 所", "中职及技工")]
cards = []
ry = 430
for num, lab in rows:
    box(d, 120, ry, 840, 220, r=30)
    cards.append((120, ry, 840, 220))
    cy = ry + 110
    put(d, checks, num, font(82, True), (540, cy - 40), color=GOLD, maxw=760)
    put(d, checks, lab, font(48), (540, cy + 55), color=SUB, maxw=760)
    ry += 220 + 40
put(d, checks, "最被低估的一条路", font(48, True), (W // 2, ry + 50), color=WHITE, maxw=900)
put(d, checks, "中职，一样有出路", font(38), (W // 2, ry + 130), color=LIGHT, maxw=900)
gap_report(d, checks, "镜头05", cards)
verify(d, checks, "镜头05")
img.save(BASE + P + "05-中职技工-1080x1920.png")

# ============ 镜头06 第四层 曲线读大学 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "第四层 · 曲线读大学", font(48, True), (W // 2, 300), color=GOLD, maxw=900)
cards = []
box(d, 90, 450, 900, 400, r=34)
cards.append((90, 450, 900, 400))
cy = 650
put(d, checks, "3+4 中本贯通", font(50, True), (540, cy - 90), color=WHITE, maxw=840)
put(d, checks, "中职 3 年 → 全日制本科 4 年", font(40), (540, cy), color=LIGHT, maxw=840)
put(d, checks, "拿全日制本科文凭，和高考一样", font(34), (540, cy + 90), color=SUB, maxw=840)
box(d, 90, 900, 900, 400, r=34)
cards.append((90, 900, 900, 400))
cy = 1100
put(d, checks, "3+2 中高贯通", font(50, True), (540, cy - 90), color=WHITE, maxw=840)
put(d, checks, "中职 3 年 → 高职 2 年", font(40), (540, cy), color=LIGHT, maxw=840)
put(d, checks, "2,853 人 · 63 个专业", font(34), (540, cy + 90), color=SUB, maxw=840)
put(d, checks, "知道的人还不多，是低分段被低估的选项", font(40, True), (W // 2, 1410), color=GOLD, maxw=900)
gap_report(d, checks, "镜头06", cards)
verify(d, checks, "镜头06")
img.save(BASE + P + "06-曲线读大学-1080x1920.png")

# ============ 镜头07 降分通道 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "还有这些工具", font(52, True), (W // 2, 330), color=WHITE, maxw=900)
put(d, checks, "都是降分通道", font(42), (W // 2, 440), color=GOLD, maxw=900)
cards = []
box(d, 90, 540, 900, 340, r=34)
cards.append((90, 540, 900, 340))
cy = 710
put(d, checks, "走 读", font(56, True), (540, cy - 55), color=WHITE, maxw=840)
put(d, checks, "调剂入学 · 最高能降 35 分", font(38), (540, cy + 65), color=LIGHT, maxw=840)
box(d, 90, 930, 900, 340, r=34)
cards.append((90, 930, 900, 340))
cy = 1100
put(d, checks, "指标生", font(56, True), (540, cy - 55), color=WHITE, maxw=840)
put(d, checks, "校内竞争 · 降分空间 5-20 分", font(38), (540, cy + 65), color=LIGHT, maxw=840)
put(d, checks, "会用工具的人，多一条路", font(42, True), (W // 2, 1420), color=GOLD, maxw=900)
gap_report(d, checks, "镜头07", cards)
verify(d, checks, "镜头07")
img.save(BASE + P + "07-降分通道-1080x1920.png")

# ============ 镜头08 全景覆盖 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "4 层出路加起来", font(60, True), (W // 2, 540), color=WHITE, maxw=900)
box(d, 100, 680, 880, 330, r=36)
cy = 845
put(d, checks, "高中阶段总学位", font(40), (540, cy - 70), color=SUB, maxw=820)
put(d, checks, "146,752 个", font(88, True), (540, cy + 60), color=GOLD, maxw=820)
put(d, checks, "基本覆盖全部 15.3 万考生", font(44, True), (W // 2, 1140), color=WHITE, maxw=900)
put(d, checks, "几乎每个孩子都有书读", font(44, True), (W // 2, 1300), color=GOLD, maxw=900)
gap_report(d, checks, "镜头08", [(100, 680, 880, 330)])
verify(d, checks, "镜头08")
img.save(BASE + P + "08-全景覆盖-1080x1920.png")

# ============ 镜头09 CTA ============
img, d = new_canvas(0); checks = []
header(d, checks)
d.line([W // 2 - 100, 720, W // 2 + 100, 720], fill=GOLD, width=5)
put(d, checks, "关键不是", font(72, True, scale=False), (W // 2, 890), color=WHITE, maxw=900)
put(d, checks, "「有没有学上」", font(72, True, scale=False), (W // 2, 1030), color=LIGHT, maxw=900)
put(d, checks, "是「选对哪条路」", font(72, True, scale=False), (W // 2, 1170), color=GOLD, maxw=900)
box(d, 100, 1330, 880, 210, r=42)
put(d, checks, "收藏这条 · 填志愿用得上", font(42, True), (540, 1435), color=WHITE, maxw=840)
put(d, checks, "点我主页，看完整出路全景图", font(36), (W // 2, 1610), color=SUB, maxw=900)
gap_report(d, checks, "镜头09", [(100, 1330, 880, 210)])
verify(d, checks, "镜头09")
img.save(BASE + P + "09-CTA-1080x1920.png")

print("S1-6 抖音分镜头 9 张 v5 全部完成")
