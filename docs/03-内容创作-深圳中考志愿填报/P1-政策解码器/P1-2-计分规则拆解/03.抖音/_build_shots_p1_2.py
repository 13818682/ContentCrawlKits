# -*- coding: utf-8 -*-
"""P1-2 抖音分镜头配图 7张（1080×1920 9:16竖屏）
对应 01-P1-2-...-抖音口播脚本.md。
镜头：01钩子(分数会骗人)→02总览(3规则)→03性价比→04等级制→05隐形战场→06三件事→07CTA
沿用 P1-1 _build_shots_p1_1.py 规范：SC=4/3 文字放大、蓝色渐变光影、gap_report 间隙检测、verify 越界。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1080, 1920
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
GRAY = (196, 205, 216)
SC = 4 / 3


def font(size, bold=False, scale=True):
    if scale:
        size = int(round(size * SC))
    if size <= 17:
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def new_canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.55:
            k = p / 0.55; col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.55) / 0.45; col = c_mid * (1 - k) + c_bot * k
        base_row = col
    base = np.tile(np.linspace(0, 1, H)[:, None, None] * 0 + 1, (1, 1, 3)) * 0  # placeholder
    # 渐变列
    t = np.linspace(0, 1, H)[:, None, None]
    colgrad = np.where(t < 0.55, c_top[None, None, :] * (1 - t / 0.55) + c_mid[None, None, :] * (t / 0.55),
                       c_mid[None, None, :] * (1 - (t - 0.55) / 0.45) + c_bot[None, None, :] * ((t - 0.55) / 0.45))
    base = np.repeat(colgrad, W, axis=1).astype(np.float32)
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.60 + 0.40 * diag)
    spots = [
        ((0.78, 0.15), (150, 200, 240)), ((0.22, 0.20), (120, 180, 235)),
        ((0.72, 0.72), (95, 160, 225)), ((0.30, 0.85), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]; col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    base += col[None, None, :] * (np.exp(-dist * dist) * 0.30)[:, :, None]
    dist2 = np.sqrt(((xx - 0.12 * W) / (W * 0.35)) ** 2 + ((yy - 0.86 * H) / (H * 0.30)) ** 2)
    base += np.array((70, 140, 210), np.float32)[None, None, :] * (np.exp(-dist2 * dist2) * 0.16)[:, :, None]
    dist3 = np.sqrt(((xx - 0.90 * W) / (W * 0.40)) ** 2 + ((yy - 0.92 * H) / (H * 0.25)) ** 2)
    base += np.array((150, 110, 60), np.float32)[None, None, :] * (np.exp(-dist3 * dist3) * 0.12)[:, :, None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
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


def header(d, checks, tag="深圳中考 · 政策解码器 · 第2篇", y=130):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=900)


def foot(d, checks, txt="数据来源：《2026年深圳市高中阶段学校考生报考指导手册》· 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/03.抖音/"
P = "01-P1-2-630背后的3个隐藏规则-抖音-3个规则-镜头"
ALL_OK = True

# ============ 镜头01 钩子 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "分数会骗人", font(62, True), (W // 2, 360), color=WHITE, maxw=940)
put(d, checks, "规则不会", font(108, True, scale=False), (W // 2, 570), color=GOLD, maxw=940)
d.line([W // 2 - 120, 730, W // 2 + 120, 730], fill=GOLD, width=5)
put(d, checks, "630分背后 · 藏着3个隐藏规则", font(42, True), (W // 2, 880), color=WHITE, maxw=940)
put(d, checks, "决定录取的 · 往往不在分数上", font(40, True), (W // 2, 970), color=WHITE, maxw=940)
box(d, 110, 1200, 860, 220, r=100)
put(d, checks, "性价比 · 等级制 · 隐形战场", font(40, True), (W // 2, 1310), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头01", [(110, 1200, 860, 220)])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-钩子-分数会骗人-1080x1920.png")

# ============ 镜头02 总览 · 3个规则 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "知道630 ≠ 会用630", font(58, True, scale=False), (W // 2, 340), color=GOLD, maxw=940)
rows2 = [
    ("① 性价比", "同样的时间 · 花在哪最划算", GOLD),
    ("② 等级制", "A+永远前5% · 别掉到C", WHITE),
    ("③ 隐形战场", "生地同分PK · 信技须合格", WHITE),
]
cy2 = 540
for t, s, col in rows2:
    box(d, 110, cy2, 860, 180, r=30)
    put(d, checks, t, font(42, True), (300, cy2 + 90), color=col, maxw=320)
    put(d, checks, s, font(30), (660, cy2 + 90), color=WHITE, maxw=430)
    cy2 += 230
put(d, checks, "分数之外 · 才见高下", font(42, True), (W // 2, 1390), color=GOLD, maxw=940)
box(d, 110, 1500, 860, 200, r=100)
put(d, checks, "三条规则 · 一条条拆开讲", font(40, True), (W // 2, 1600), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头02", [(110, 540, 860, 180), (110, 770, 860, 180), (110, 1000, 860, 180), (110, 1500, 860, 200)])
verify(d, checks, "镜头02")
img.save(BASE + P + "02-总览-3个规则-1080x1920.png")

# ============ 镜头03 规则一 性价比 ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "规则一 · 性价比", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
put(d, checks, "同样的复习时间 · 花在哪最划算", font(34, True), (W // 2, 440), color=WHITE, maxw=920)
rows3 = [
    ("440分", "语数英物化 · 主战场 · 全力投入", GOLD),
    ("20分", "理化实验涨到20 · 8分增量=性价比王", GOLD),
    ("170分", "历史道法体育 · 稳定发挥即可", WHITE),
]
cy3 = 600
for t, s, col in rows3:
    box(d, 110, cy3, 860, 190, r=30)
    put(d, checks, t, font(46, True), (300, cy3 + 95), color=col, maxw=300)
    put(d, checks, s, font(29), (640, cy3 + 95), color=WHITE, maxw=440)
    cy3 += 235
put(d, checks, "实验那8分 · 认真练就白送", font(38, True), (W // 2, 1370), color=GOLD, maxw=920)
box(d, 110, 1460, 860, 200, r=100)
put(d, checks, "刷题拿不到 · 别在副科题海苦熬", font(36, True), (W // 2, 1560), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头03", [(110, 600, 860, 190), (110, 835, 860, 190), (110, 1070, 860, 190), (110, 1460, 860, 200)])
verify(d, checks, "镜头03")
img.save(BASE + P + "03-性价比-花在哪最划算-1080x1920.png")

# ============ 镜头04 规则二 等级制 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "规则二 · 等级比分数更准", font(52, True), (W // 2, 340), color=GOLD, maxw=900)
put(d, checks, "分数会变 · 等级不变", font(34, True), (W // 2, 440), color=WHITE, maxw=920)
box(d, 110, 570, 860, 290, r=40)
put(d, checks, "A+ = 全市前5%", font(54, True), (W // 2, 690), color=GOLD, maxw=820)
put(d, checks, "试卷再难 · 也是单科顶尖", font(34), (W // 2, 800), color=WHITE, maxw=820)
rows4 = [
    ("省一级学校门槛", "全科 C+ 及以上 · 体育 C 即可", GOLD),
    ("任何一科掉到 C", "报省一级 · 资格都没有", WHITE),
]
cy4 = 940
for t, s, col in rows4:
    box(d, 110, cy4, 860, 190, r=30)
    put(d, checks, t, font(36, True), (320, cy4 + 95), color=col, maxw=360)
    put(d, checks, s, font(30), (700, cy4 + 95), color=WHITE, maxw=380)
    cy4 += 225
put(d, checks, "看等级 · 才知道孩子的真实位置", font(38, True), (W // 2, 1490), color=GOLD, maxw=920)
box(d, 110, 1580, 860, 200, r=100)
put(d, checks, "早发现 · 早补 · 别拖到初三", font(38, True), (W // 2, 1680), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头04", [(110, 570, 860, 290), (110, 940, 860, 190), (110, 1165, 860, 190), (110, 1580, 860, 200)])
verify(d, checks, "镜头04")
img.save(BASE + P + "04-等级制-A加永远前5-1080x1920.png")

# ============ 镜头05 规则三 隐形战场 ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "规则三 · 不计分的隐形战场", font(50, True), (W // 2, 340), color=GOLD, maxw=920)
put(d, checks, "生地 · 信技 · 艺术", font(34, True), (W // 2, 440), color=WHITE, maxw=920)
# 双卡 552
box(d, 110, 570, 420, 320, r=34)
put(d, checks, "考生A", font(32, True), (320, 630), color=WHITE, maxw=360)
put(d, checks, "生地 96", font(60, True, scale=False), (320, 750), color=GOLD, maxw=400)
put(d, checks, "总分552 · 被录取", font(28), (320, 850), color=WHITE, maxw=380)
box(d, 550, 570, 420, 320, r=34, outline=(90, 110, 140))
put(d, checks, "考生B", font(32, True), (760, 630), color=GRAY, maxw=360)
put(d, checks, "生地 82", font(60, True, scale=False), (760, 750), color=GRAY, maxw=400)
put(d, checks, "总分552 · 落选", font(28), (760, 850), color=GRAY, maxw=380)
box(d, 110, 950, 860, 160, r=30)
put(d, checks, "同分PK · 先比生地 → 96 > 82", font(36, True), (W // 2, 1030), color=GOLD, maxw=800)
box(d, 110, 1150, 860, 160, r=30)
put(d, checks, "信技 · 艺术须合格 → 才能报省一级", font(34, True), (W // 2, 1230), color=WHITE, maxw=820)
box(d, 110, 1350, 860, 150, r=30)
put(d, checks, "14分 = 一个高中学位", font(40, True), (W // 2, 1425), color=GOLD, maxw=820)
box(d, 110, 1560, 860, 190, r=100)
put(d, checks, "生地是底牌 · 别让小科翻车", font(38, True), (W // 2, 1655), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头05", [(110, 570, 420, 320), (550, 570, 420, 320), (110, 950, 860, 160), (110, 1150, 860, 160), (110, 1350, 860, 150), (110, 1560, 860, 190)])
verify(d, checks, "镜头05")
img.save(BASE + P + "05-隐形战场-生地PK-1080x1920.png")

# ============ 镜头06 三件事 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "现在能做的三件事", font(56, True), (W // 2, 340), color=GOLD, maxw=900)
rows6 = [
    ("① 看性价比分配精力", "主战场优先 · 别让副科挤占主科时间"),
    ("② 用等级定位孩子", "哪科在C边缘 · 就是门槛隐患"),
    ("③ 确认两个隐形门槛", "生地分数有数 · 信技艺术确认合格"),
]
cy6 = 520
for t, s in rows6:
    box(d, 110, cy6, 860, 240, r=30)
    put(d, checks, t, font(38, True), (170, cy6 + 75), anchor="lm", color=WHITE, maxw=760)
    put(d, checks, s, font(31), (170, cy6 + 165), anchor="lm", color=GOLD, maxw=760)
    cy6 += 300
box(d, 110, 1470, 860, 200, r=100)
put(d, checks, "出分前就能做 · 做了改变结果", font(36, True), (W // 2, 1570), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头06", [(110, 520, 860, 240), (110, 820, 860, 240), (110, 1120, 860, 240), (110, 1470, 860, 200)])
verify(d, checks, "镜头06")
img.save(BASE + P + "06-三件事-1080x1920.png")

# ============ 镜头07 CTA ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "孩子负责考试", font(52, True), (W // 2, 400), color=WHITE, maxw=900)
put(d, checks, "家长负责懂规则", font(68, True, scale=False), (W // 2, 550), color=GOLD, maxw=940)
d.line([W // 2 - 100, 700, W // 2 + 100, 700], fill=GOLD, width=5)
put(d, checks, "政策 · 数据 · 志愿梯度", font(38, True), (W // 2, 840), color=WHITE, maxw=900)
put(d, checks, "630背后的规则 · 一篇一篇讲", font(38, True), (W // 2, 930), color=WHITE, maxw=900)
box(d, 110, 1090, 860, 250, r=60)
put(d, checks, "关注我", font(46, True), (W // 2, 1175), color=WHITE, maxw=820)
put(d, checks, "下期：AC类还是D类 · 户籍影响什么", font(33), (W // 2, 1285), color=GOLD, maxw=820)
put(d, checks, "3个隐藏规则 · 帮你把630分用明白", font(32), (W // 2, 1450), color=LIGHT, maxw=940)
box(d, 110, 1540, 860, 170, r=80)
put(d, checks, "评论区聊聊：孩子生地考了多少分？", font(33, True), (W // 2, 1625), color=WHITE, maxw=820)
ALL_OK &= gap_report(d, checks, "镜头07", [(110, 1090, 860, 250), (110, 1540, 860, 170)])
verify(d, checks, "镜头07")
img.save(BASE + P + "07-CTA-1080x1920.png")

print()
print("全部 OK =", ALL_OK)
