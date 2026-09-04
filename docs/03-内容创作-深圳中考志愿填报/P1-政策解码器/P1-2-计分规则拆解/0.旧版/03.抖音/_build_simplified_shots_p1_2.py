# -*- coding: utf-8 -*-
"""P1-2 抖音分镜 7 张「化繁为简」重制（1080×1920）
底部 1/7（y≥1646，约274px）为字幕+图标安全区，全部留空；
内容规划在 y 0–1600 安全区，主体大字居中偏上聚焦。verify 含安全线检查。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1080, 1920
SAFE_B = 1590         # 内容最底：底部留 1/6（1600 起字幕区），缓冲 10px
SAFE_R = 950          # 内容最右：右侧留 1/10（972 起图标区），缓冲 22px
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
GRAY = (196, 205, 216)
OUT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/03.抖音/"
P = "化繁为简-P1-2-630背后的3个隐藏规则-抖音-镜头"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=940):
    f = fnt
    size = fnt.size
    path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
    while size > 14:
        bb = d.textbbox((0, 0), text, font=f, anchor=anchor)
        x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
        x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
        if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= SAFE_R + 1 and y0 >= -1 and y1 <= SAFE_B + 1:
            break
        size -= 1
        f = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=f, fill=color, anchor=anchor)
    ck.append((text, f, xy, anchor))


def verify(d, ck, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy})")
        if y1 > SAFE_B:
            bad += 1
            print(f"  [入侵字幕区] {text!r} 底y={y1:.0f} > {SAFE_B}")
        if x1 > SAFE_R:
            bad += 1
            print(f"  [入侵图标区] {text!r} 右x={x1:.0f} > {SAFE_R}")
    print(f"{name}: {bad}处越界/入侵")
    return bad == 0


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=30, width=2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)


def canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    t = np.linspace(0, 1, H)[:, None, None]
    base = np.where(t < 0.55,
                    c_top[None, None, :] * (1 - t / 0.55) + c_mid[None, None, :] * (t / 0.55),
                    c_mid[None, None, :] * (1 - (t - 0.55) / 0.45) + c_bot[None, None, :] * ((t - 0.55) / 0.45))
    base = np.repeat(base, W, axis=1).astype(np.float32)
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.62 + 0.38 * diag)
    spots = [
        ((0.80, 0.14), (150, 200, 240)), ((0.20, 0.20), (120, 180, 235)),
        ((0.72, 0.72), (95, 160, 225)), ((0.30, 0.85), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]; col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    base += col[None, None, :] * (np.exp(-dist * dist) * 0.30)[:, :, None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


ALL = []

# ============ 镜头01 钩子 ============
img, d = canvas(0); ck = []
put(d, ck, "分数会骗人", font(80, True), (W // 2, 320), color=WHITE)
put(d, ck, "规则不会", font(150, True), (W // 2, 620), color=GOLD)
put(d, ck, "630分背后 · 藏着3个隐藏规则", font(46, True), (W // 2, 1060), color=WHITE)
put(d, ck, "性价比 · 等级制 · 隐形战场", font(38), (W // 2, 1230), color=LIGHT)
ALL.append(verify(d, ck, "镜头01钩子"))
img.save(OUT + P + "01-钩子-分数会骗人-1080x1920.png")

# ============ 镜头02 总览 ============
img, d = canvas(1); ck = []
put(d, ck, "知道630 ≠ 会用630", font(74, True), (W // 2, 310), color=GOLD)
rows2 = [
    ("① 性价比", "同样的时间 · 花在哪涨分快"),
    ("② 等级制", "A+ 永远前5% · 别掉到C"),
    ("③ 隐形战场", "生地同分PK · 信技须合格"),
]
y = 560
for t, s in rows2:
    box(d, 110, y, 840, 190, r=28)
    put(d, ck, t, font(48, True), (300, y + 95), color=WHITE, maxw=320)
    put(d, ck, s, font(34), (660, y + 95), color=GOLD if t.startswith("①") else WHITE, maxw=430)
    y += 230
put(d, ck, "决定录取的 · 往往不在分数上", font(42, True), (W // 2, 1430), color=LIGHT)
ALL.append(verify(d, ck, "镜头02总览"))
img.save(OUT + P + "02-总览-3个规则-1080x1920.png")

# ============ 镜头03 性价比 ============
img, d = canvas(2); ck = []
put(d, ck, "规则一 · 性价比", font(44, True), (W // 2, 260), color=GOLD)
put(d, ck, "同样的时间 · 花在哪最划算", font(76, True), (W // 2, 480), color=WHITE)
rows3 = [
    ("440分", "语数英物化 · 主战场 · 全力投入", GOLD),
    ("20分", "理化实验涨到20 · 8分=性价比王", GOLD),
    ("170分", "历史道法体育 · 稳定发挥即可", WHITE),
]
y = 780
for t, s, col in rows3:
    box(d, 110, y, 840, 175, r=26)
    put(d, ck, t, font(60, True), (300, y + 88), color=col, maxw=320)
    put(d, ck, s, font(36), (660, y + 88), color=WHITE, maxw=430)
    y += 215
put(d, ck, "实验那8分 · 认真练就白送", font(40, True), (W // 2, 1500), color=LIGHT)
ALL.append(verify(d, ck, "镜头03性价比"))
img.save(OUT + P + "03-性价比-花在哪最划算-1080x1920.png")

# ============ 镜头04 等级制 ============
img, d = canvas(3); ck = []
put(d, ck, "规则二 · 等级制", font(44, True), (W // 2, 260), color=GOLD)
put(d, ck, "A+ 永远是前5%", font(80, True), (W // 2, 470), color=WHITE)
box(d, 110, 680, 840, 320, r=34)
put(d, ck, "等级按全市固定比例划", font(40, True), (W // 2, 780), color=LIGHT)
put(d, ck, "试卷难易 · 不影响等级", font(40, True), (W // 2, 900), color=LIGHT)
rows4 = [
    ("省一级门槛", "全科 C+ 及以上 · 体育 C 即可", GOLD),
    ("任一科掉到 C", "报省一级 · 资格都没有", WHITE),
]
y = 1080
for t, s, col in rows4:
    box(d, 110, y, 840, 175, r=28)
    put(d, ck, t, font(44, True), (320, y + 88), color=col, maxw=380)
    put(d, ck, s, font(36), (700, y + 88), color=WHITE, maxw=380)
    y += 210
ALL.append(verify(d, ck, "镜头04等级制"))
img.save(OUT + P + "04-等级制-A加永远前5-1080x1920.png")

# ============ 镜头05 隐形战场 ============
img, d = canvas(0); ck = []
put(d, ck, "规则三 · 隐形战场", font(44, True), (W // 2, 260), color=GOLD)
put(d, ck, "同分PK · 生地定胜负", font(76, True), (W // 2, 470), color=WHITE)
box(d, 110, 650, 400, 300, r=30)
put(d, ck, "考生A", font(34, True), (310, 720), color=WHITE)
put(d, ck, "96", font(100, True), (310, 870), color=GOLD)
put(d, ck, "生地 · 被录取", font(32), (310, 985), color=WHITE)
box(d, 550, 650, 400, 300, r=30, outline=(90, 110, 140))
put(d, ck, "考生B", font(34, True), (750, 720), color=GRAY)
put(d, ck, "82", font(100, True), (750, 870), color=GRAY)
put(d, ck, "生地 · 落选", font(32), (750, 985), color=GRAY)
d.rounded_rectangle([110, 1030, 940, 1170], radius=40, fill=GOLD)
put(d, ck, "14分 = 一个高中学位", font(48, True), (525, 1100), color=(18, 30, 55))
put(d, ck, "信技 · 艺术须合格 → 才能报省一级", font(38, True), (W // 2, 1350), color=WHITE)
ALL.append(verify(d, ck, "镜头05隐形"))
img.save(OUT + P + "05-隐形战场-生地PK-1080x1920.png")

# ============ 镜头06 三件事 ============
img, d = canvas(1); ck = []
put(d, ck, "现在能做的三件事", font(76, True), (W // 2, 330), color=WHITE)
acts = [
    ("① 看性价比分配精力", "主战场优先 · 别让副科挤占"),
    ("② 用等级定位孩子", "哪科在 C 边缘 · 门槛隐患"),
    ("③ 确认两个隐形门槛", "生地有数 · 信技艺术确认合格"),
]
y = 620
for t, s in acts:
    box(d, 110, y, 840, 210, r=28)
    put(d, ck, t, font(46, True), (200, y + 72), anchor="lm", color=WHITE, maxw=760)
    put(d, ck, s, font(38), (200, y + 152), anchor="lm", color=GOLD, maxw=760)
    y += 260
put(d, ck, "出分前就能做 · 做了改变结果", font(40, True), (W // 2, 1470), color=LIGHT)
ALL.append(verify(d, ck, "镜头06三件事"))
img.save(OUT + P + "06-三件事-1080x1920.png")

# ============ 镜头07 CTA ============
img, d = canvas(3); ck = []
put(d, ck, "孩子负责考试", font(64, True), (W // 2, 330), color=WHITE)
put(d, ck, "家长负责懂规则", font(112, True), (W // 2, 590), color=GOLD)
put(d, ck, "关注我 · 下期：AC类还是D类", font(50, True), (W // 2, 1000), color=WHITE)
put(d, ck, "630背后的规则 · 一篇一篇讲", font(40), (W // 2, 1200), color=LIGHT)
put(d, ck, "评论区聊聊：孩子生地考了多少分？", font(40), (W // 2, 1400), color=LIGHT)
ALL.append(verify(d, ck, "镜头07CTA"))
img.save(OUT + P + "07-CTA-1080x1920.png")

print()
print("全部 OK =", all(ALL))
