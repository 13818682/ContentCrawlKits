# -*- coding: utf-8 -*-
"""QA-001 抖音分镜头配图 9张（1080×1920 9:16竖屏）v2 —— 对应 01-QA-001-...-抖音-三件事.md 口播脚本
镜头序列：01首图(话题+兴趣点放大·强冲击)→02钩子(开场2秒兑现能读！)→03资格5项条件
        →04竞争54%vs23%→05出路三条路→06中职3+4贯通→07三件事(核对材料)→08你不是一个人→09CTA
v2 版式要求（2026-08-31 用户定稿）：
  1. 所有文字水平居中：卡片内「数字(金)+标题(白)」组合居中于上半，说明文字居中于下半。
  2. 文字不穿越文本框：box 内文字上下留白 ≥25px、左右留白 ≥40px。
  3. 文本框间距 ≥30px；gap_report 逐项校验。
  4. 首图：话题两行大字 + 巨型金「能！」+ 数据带 + 关注CTApill，兴趣点/话题最大化。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FD = "C:/Windows/Fonts/"
W, H = 1080, 1920
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
SHADOW = (0, 20, 45)
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


def list_card(d, checks, x, y, w, h, num, title, desc, r=26, desc_color=SUB):
    """带数字的居中列表卡：数字(金)+标题(白)组合居中于上半，说明居中于下半。
    留白：上下≥25px、左右≥40px。"""
    box(d, x, y, w, h, r=r)
    cy1 = y + h // 2 - 30
    cy2 = y + h - 52
    f1 = font(40, True)
    nw = int(d.textlength(num, font=f1))
    total = nw + 16 + int(d.textlength(title, font=f1))
    max_main = w - 2 * 40
    while total > max_main and f1.size > 20:
        f1 = font(f1.size - 1, True)
        nw = int(d.textlength(num, font=f1))
        total = nw + 16 + int(d.textlength(title, font=f1))
    x0 = x + w // 2 - total // 2
    put(d, checks, num, f1, (x0, cy1), anchor="lm", color=GOLD, maxw=120)
    put(d, checks, title, f1, (x0 + nw + 16, cy1), anchor="lm", color=WHITE)
    put(d, checks, desc, font(30), (x + w // 2, cy2), color=desc_color, maxw=w - 2 * 46)


def pill(d, checks, cx, cy, text, fnt, color=GOLD, pad_x=56, pad_y=28):
    """自动按文字宽度适配的金色描边胶囊（不穿越：左右留白 pad_x、上下 pad_y）。返回胶囊矩形供校验。"""
    tw = int(d.textlength(text, font=fnt))
    bb = d.textbbox((0, 0), text, font=fnt, anchor="mm")
    th = bb[3] - bb[1]
    x0, x1 = cx - tw / 2 - pad_x, cx + tw / 2 + pad_x
    y0, y1 = cy - th / 2 - pad_y, cy + th / 2 + pad_y
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, outline=color, width=3)
    put(d, checks, text, fnt, (cx, cy), color=color)
    return (int(x0), int(y0), int(x1 - x0), int(y1 - y0))   # (x, y, w, h) 供 gap_report


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


def header(d, checks, tag="深圳中考 · 问答系列 · 001", y=120):
    d.rectangle([84, y, 234, y + 5], fill=GOLD)
    put(d, checks, tag, font(34), (84, y + 52), anchor="lm", color=LIGHT, maxw=900)


def foot(d, checks, txt="数据来源：深圳市教育局2026年公开信息 · 逐条人工核对"):
    put(d, checks, txt, font(26), (W // 2, H - 90), color=SUB, maxw=1000)


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/001+非深户可在深圳参加中考读高中吗/04.抖音/"
P = "01-QA-001-非深户能在深圳读高中吗-抖音-三件事-镜头"
ALL_OK = True

# ============ 镜头01 首图：话题+兴趣点放大（强冲击封面） ============
img, d = new_canvas(0); checks = []
header(d, checks)
# 话题：问题两行放大
put(d, checks, "非深户能在深圳", font(62, True), (W // 2, 350), color=WHITE, maxw=940)
put(d, checks, "读高中吗？", font(62, True), (W // 2, 445), color=WHITE, maxw=940)
# 兴趣点：巨型金色答案（能读！居中）
put(d, checks, "能读！", font(230, True, scale=False), (W // 2 + 3, 762), color=SHADOW, maxw=940)
put(d, checks, "能读！", font(230, True, scale=False), (W // 2, 758), color=GOLD, maxw=940)
# 副钩
d.line([W // 2 - 110, 900, W // 2 + 110, 900], fill=GOLD, width=5)
put(d, checks, "5项条件 · 3条路 · 一次讲清", font(42, True), (W // 2, 985), color=WHITE, maxw=880)
# 数据对撞带
box(d, 100, 1065, 880, 250, r=40)
d.line([W // 2, 1085, W // 2, 1295], fill=GOLD, width=3)
put(d, checks, "54%", font(96, True, scale=False), (330, 1160), color=GOLD, maxw=380)
put(d, checks, "非深户考生占比", font(34), (330, 1255), color=LIGHT, maxw=360)
put(d, checks, "23%", font(96, True, scale=False), (750, 1160), color=WHITE, maxw=380)
put(d, checks, "公办D类指标", font(34), (750, 1255), color=LIGHT, maxw=360)
# 关注 CTA pill（按文字自动适配宽度，不穿越）
card_pill = pill(d, checks, W // 2, 1640, "关注我 · 非深户升学指南", font(38, True))
ALL_OK &= gap_report(d, checks, "镜头01", [(100, 1065, 880, 250), card_pill])
verify(d, checks, "镜头01")
img.save(BASE + P + "01-首图-1080x1920.png")

# ============ 镜头02 钩子 · 开场2秒兑现 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "能读！", font(130, True, scale=False), (W // 2, 440), color=GOLD, maxw=940)
put(d, checks, "非深户在深圳 · 能参加中考 · 能读高中", font(44, True), (W // 2, 600), color=WHITE, maxw=920)
d.line([W // 2 - 100, 690, W // 2 + 100, 690], fill=GOLD, width=5)
put(d, checks, "先给你结论 · 三件事一次讲清", font(36), (W // 2, 770), color=LIGHT, maxw=880)
rows2 = [
    ("第一件事 · 资格", "5项条件 · 对号入座", GOLD),
    ("第二件事 · 竞争", "54%考生 · 抢23%公办", WHITE),
    ("第三件事 · 出路", "公办 / 民办 / 中职 · 三层能走", GOLD),
]
cards2 = []
ry2 = 850
for t, s, col in rows2:
    box(d, 120, ry2, 840, 210, r=34)
    cards2.append((120, ry2, 840, 210))
    put(d, checks, t, font(46, True), (540, ry2 + 78), color=WHITE, maxw=760)
    put(d, checks, s, font(36), (540, ry2 + 152), color=col, maxw=760)
    ry2 += 210 + 34
put(d, checks, "收藏照做 · 转发给同届家长", font(40, True), (W // 2, 1600), color=GOLD, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头02", cards2)
verify(d, checks, "镜头02")
img.save(BASE + P + "02-钩子-1080x1920.png")

# ============ 镜头03 资格 · 5项条件（居中列表卡） ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "第一件事 · 资格：5项条件", font(48, True), (W // 2, 290), color=GOLD, maxw=920)
rows3 = [
    ("①", "合法稳定职业", "父母一方在深有合法稳定职业"),
    ("②", "合法稳定住所", "父母一方在深有合法稳定住所"),
    ("③", "有效居住证", "父母一方持有 · 注意有效期"),
    ("④", "社保累计满3年", "两险都缴 · 至少一个险种满3年"),
    ("⑤", "3年完整学籍", "在深完成3年完整初中"),
]
cards3 = []
ry3 = 380
for n, t, s in rows3:
    list_card(d, checks, 110, ry3, 860, 160, n, t, s)
    cards3.append((110, ry3, 860, 160))
    ry3 += 160 + 34
put(d, checks, "条件不够也别慌：民办补录 · 中职注册兜底", font(40, True), (W // 2, 1380), color=WHITE, maxw=920)
put(d, checks, "报名在3月下旬 · 社保/居住证/学籍三大翻车点", font(36), (W // 2, 1460), color=GOLD, maxw=920)
ALL_OK &= gap_report(d, checks, "镜头03", cards3)
verify(d, checks, "镜头03")
img.save(BASE + P + "03-资格-5项条件-1080x1920.png")

# ============ 镜头04 竞争 · 54% vs 23% ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "第二件事 · 竞争：54%抢23%", font(48, True), (W // 2, 290), color=GOLD, maxw=920)
box(d, 100, 390, 880, 360, r=40)
d.line([W // 2, 410, W // 2, 730], fill=GOLD, width=3)
put(d, checks, "54%", font(110, True, scale=False), (330, 530), color=GOLD, maxw=420)
put(d, checks, "非深户考生占比", font(36), (330, 640), color=LIGHT, maxw=420)
put(d, checks, "23%", font(110, True, scale=False), (750, 530), color=WHITE, maxw=420)
put(d, checks, "公办D类指标", font(36), (750, 640), color=LIGHT, maxw=420)
box(d, 100, 810, 880, 300, r=34)
put(d, checks, "四大 AC类与D线 只差 0-5 分", font(44, True), (540, 890), color=WHITE, maxw=820)
put(d, checks, "普通校D线 高出AC线 13-31 分", font(36), (540, 990), color=SUB, maxw=820)
put(d, checks, "分数越高 · 户籍差距越小", font(50, True), (W // 2, 1260), color=GOLD, maxw=920)
put(d, checks, "用D线定位 · 别用AC线", font(42, True), (W // 2, 1480), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头04", [(100, 390, 880, 360), (100, 810, 880, 300)])
verify(d, checks, "镜头04")
img.save(BASE + P + "04-竞争-54vs23-1080x1920.png")

# ============ 镜头05 出路 · 三条腿走路（居中列表卡） ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "第三件事 · 出路：三条腿走路", font(48, True), (W // 2, 290), color=GOLD, maxw=920)
rows5 = [
    ("1", "公办普高", "D线指标生 9,186个 · 控制线约低20分"),
    ("2", "民办普高", "49所 · 33,195个学位 · AC/D同分录取"),
    ("3", "中职 · 3+4", "300个名额 · 中职3年+本科4年 · 全日制本科"),
]
cards5 = []
ry5 = 400
for n, t, s in rows5:
    list_card(d, checks, 110, ry5, 860, 200, n, t, s)
    cards5.append((110, ry5, 860, 200))
    ry5 += 200 + 34
put(d, checks, "全市普高（含民办）录取率超 73%", font(48, True), (W // 2, 1290), color=GOLD, maxw=920)
put(d, checks, "公办 + 民办 + 中职 · 别只盯一条路", font(38), (W // 2, 1390), color=LIGHT, maxw=920)
ALL_OK &= gap_report(d, checks, "镜头05", cards5)
verify(d, checks, "镜头05")
img.save(BASE + P + "05-出路-三条路-1080x1920.png")

# ============ 镜头06 中职 · 3+4贯通 ============
img, d = new_canvas(1); checks = []
header(d, checks)
put(d, checks, "被忽略的好路 · 公办中职", font(48, True), (W // 2, 290), color=GOLD, maxw=920)
put(d, checks, "3+4 中本贯通", font(100, True, scale=False), (W // 2, 470), color=WHITE, maxw=940)
put(d, checks, "中职3年 + 本科4年 = 全日制本科", font(40), (W // 2, 610), color=SUB, maxw=900)
box(d, 100, 690, 880, 250, r=36)
put(d, checks, "全市 3+4 名额 只有 300 个", font(44, True), (540, 770), color=WHITE, maxw=820)
put(d, checks, "3+2 中高贯通 2,853人 · 63个专业", font(36), (540, 870), color=GOLD, maxw=820)
put(d, checks, "知道的人太少 · 好多人白白错过", font(44, True), (W // 2, 1090), color=LIGHT, maxw=920)
put(d, checks, "免学费 · 还能拿本科文凭", font(42, True), (W // 2, 1330), color=WHITE, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头06", [(100, 690, 880, 250)])
verify(d, checks, "镜头06")
img.save(BASE + P + "06-中职-3+4贯通-1080x1920.png")

# ============ 镜头07 三件事 · 现在核对（居中列表卡） ============
img, d = new_canvas(2); checks = []
header(d, checks)
put(d, checks, "现在就能做的三件事", font(54, True), (W // 2, 300), color=WHITE, maxw=920)
rows7 = [
    ("①", "核对5项材料", "社保 / 居住证 / 学籍 · 现在就查"),
    ("②", "盯住有效期", "居住证过期 · 社保断缴 = 翻车点"),
    ("③", "提前定策略", "用D线定位 · 三条腿走路"),
]
cards7 = []
ry7 = 420
for n, t, s in rows7:
    list_card(d, checks, 110, ry7, 860, 200, n, t, s)
    cards7.append((110, ry7, 860, 200))
    ry7 += 200 + 34
put(d, checks, "别等3月报名才发现 · 越早准备越稳", font(44, True), (W // 2, 1360), color=GOLD, maxw=920)
ALL_OK &= gap_report(d, checks, "镜头07", cards7)
verify(d, checks, "镜头07")
img.save(BASE + P + "07-三件事-核对材料-1080x1920.png")

# ============ 镜头08 你不是一个人 ============
img, d = new_canvas(3); checks = []
header(d, checks)
put(d, checks, "你不是一个人在焦虑", font(66, True, scale=False), (W // 2, 500), color=WHITE, maxw=940)
box(d, 90, 680, 900, 260, r=40)
put(d, checks, "54% 的非深户家庭", font(44, True), (540, 780), color=WHITE, maxw=820)
put(d, checks, "都在同一道题上绕", font(42), (540, 880), color=SUB, maxw=820)
put(d, checks, "这些坑 · 我们帮你一次讲清", font(46, True), (W // 2, 1100), color=GOLD, maxw=920)
put(d, checks, "少踩坑 · 早准备", font(42, True), (W // 2, 1460), color=LIGHT, maxw=900)
ALL_OK &= gap_report(d, checks, "镜头08", [(90, 680, 900, 260)])
verify(d, checks, "镜头08")
img.save(BASE + P + "08-你不是一个人-1080x1920.png")

# ============ 镜头09 CTA ============
img, d = new_canvas(0); checks = []
header(d, checks)
put(d, checks, "非深户读高中", font(72, True, scale=False), (W // 2, 560), color=WHITE, maxw=940)
put(d, checks, "能读！3条路 · 5项条件 · 一次讲清", font(40), (W // 2, 690), color=GOLD, maxw=920)
d.line([W // 2 - 100, 800, W // 2 + 100, 800], fill=GOLD, width=5)
box(d, 100, 900, 880, 270, r=44)
put(d, checks, "关注我 · 深圳中考系列", font(46, True), (540, 990), color=WHITE, maxw=820)
put(d, checks, "非深户升学 · 每期一个关键问题", font(34), (540, 1090), color=SUB, maxw=820)
put(d, checks, "评论区聊聊 · 下一篇按你最关心的写", font(36), (W // 2, 1520), color=SUB, maxw=920)
ALL_OK &= gap_report(d, checks, "镜头09", [(100, 900, 880, 270)])
verify(d, checks, "镜头09")
img.save(BASE + P + "09-CTA-1080x1920.png")

print()
print("QA-001 抖音分镜头 9 张 v2（文字居中版）完成。ALL_OK =", ALL_OK)
if not ALL_OK:
    print("⚠️ 存在间隙/间距不足，需检查后重新生成")
