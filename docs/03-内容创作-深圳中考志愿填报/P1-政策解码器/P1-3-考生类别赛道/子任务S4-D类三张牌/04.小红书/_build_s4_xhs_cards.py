# -*- coding: utf-8 -*-
"""P1-3 S4 D类三张牌 小红书正文图卡 ×4（1080×1440，封面另有精炼版）
正文图1-三张牌总览(收藏) / 图2-牌①指标生 / 图3-牌②民办 / 图4-牌③3+4贯通。
口径：民办49所/33,195学位/ACD同线、3+4共300名额/D类可报、指标生全覆盖——官方结论；不给民办335细档、不给3+4各专业线。
模板：S3 _build_s3_xhs_cards.py（family navy；版式换"三张牌"大卡以避免与S3五层表列表自我重复）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (31, 76, 150); BOT = (13, 29, 72)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (162, 192, 238); SUB = (214, 227, 248)
CARD = (20, 46, 100); EDGE = (70, 118, 196)
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1080, 1440
HM = 80
BOXES = []


def base():
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, H)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, W, axis=1)
    y, x = np.mgrid[0:H, 0:W]
    # 主光：左上 radial（光线角度=左上方，与封面/抖音分镜同档）
    g = np.exp(-(((x - W * 0.24) / (W * 0.40)) ** 2 + ((y - H * 0.13) / (H * 0.32)) ** 2))
    a = a + np.array((196, 214, 250), float)[None, None, :] * (g * 0.13)[..., None]
    # 左上→右下斜射光束（同抖音分镜光线角度）
    for k, amp, wid in [(0.32, 0.09, 320), (0.95, 0.06, 260)]:
        u = x - k * y
        g2 = np.exp(-((u / wid) ** 2))
        a = a + np.array((205, 222, 252), float)[None, None, :] * (g2 * amp)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-W * .18, -H * .08, W * .24, H * .16], fill=(44, 74, 140, 46))
    od.ellipse([W * .80, H * .84, W * 1.1, H * 1.05], fill=(12, 26, 64, 40))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def center(d, text, xy, size, fill, bold=True, maxw=None, min_size=22):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    mw = maxw if maxw else W - 2 * HM
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= mw + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= mw + 1, "center too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="mm")
    BOXES.append(("C:" + text[:12], d.textbbox(xy, text, font=f, anchor="mm")))
    return f


def left(d, text, xy, size, fill, right=None, bold=False, min_size=20):
    fp = FB if bold else FR
    f = ImageFont.truetype(fp, size)
    r = right if right else W - HM - 10
    while f.size > min_size:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= (r - xy[0]) + 1:
            break
        f = ImageFont.truetype(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= (r - xy[0]) + 1, "left too long: %s" % text
    d.text(xy, text, font=f, fill=fill, anchor="lm")
    BOXES.append(("L:" + text[:14], d.textbbox(xy, text, font=f, anchor="lm")))
    return f


def rcard(d, x0, y0, x1, y1, wfill=CARD, wout=EDGE, rad=22):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=wfill, outline=wout, width=2)


def footer(d):
    center(d, "数据来源：深圳市教育局2026高中招生计划与第一批录取标准（人工核对）", (W / 2, 1390), 21, SUB, bold=False, min_size=16)


def check(name):
    bad = []
    for tag, bb in BOXES:
        if bb[0] < 20 or bb[1] < 6 or bb[2] > W - 20 or bb[3] > H - 6:
            bad.append((tag, tuple(int(v) for v in bb)))
    print(("OK  " if not bad else "!!  ") + name, "| boxes:", len(BOXES), bad if bad else "")
    BOXES.clear()


# ========== 正文图1：三张牌总览（收藏） ==========
im, d = base()
center(d, "S4 · D 类出路总览", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "D类不是死胡同 · 三张牌", (W / 2, 214), 52, WHITE, min_size=44)
center(d, "2026 官方口径 · 非深户 D 类", (W / 2, 296), 28, LIGHT, bold=False, min_size=22)
rows = [
    ("①", "指标生", "全市混战 → 同校比", "名额到校 · D 类单列 · 拼校内位次"),
    ("②", "民办高中", "一条 ACD 线 · 不分 AC/D", "49 所 · 33,195 学位 · 学费 3 万-15 万/年"),
    ("③", "3+4 中本贯通", "职校3年 + 本科4年", "300 名额试点 · D 类可报 · 全日制本科"),
]
y = 356
for lab, title, big, small in rows:
    y1 = y + 288
    rcard(d, HM, y, W - HM, y1)
    center(d, lab, (HM + 92, (y + y1) / 2), 66, GOLD, maxw=140, min_size=52)
    x0 = HM + 190
    left(d, title, (x0, y + 88), 44, WHITE, bold=True, min_size=36)
    left(d, big, (x0, y + 166), 34, GOLD, min_size=28)
    left(d, small, (x0, y + 242), 27, SUB, min_size=22)
    y = y1 + 18
center(d, "三张牌 = 把竞争池变小 · 把录取线拉平 · 换一条赛道", (W / 2, 1344), 30, WHITE, min_size=24)
footer(d)
check("正文图1")
im.save(HERE + "P1-3-S4-D类三张牌-小红书-正文图1-三张牌总览-1080x1440.png")

# ========== 正文图2：牌① 指标生 ==========
im, d = base()
center(d, "牌① · 指标生（公办里）", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "全市比 → 同校比", (W / 2, 214), 58, WHITE, min_size=48)
center(d, "报同一所学校指标生 · 只和本校 D 类比", (W / 2, 300), 30, LIGHT, bold=False, min_size=24)
# 左右对比块 + 箭头
rcard(d, HM, 380, W / 2 - 40, 560)
center(d, "全市 D 类混战", (290, 440), 40, WHITE, maxw=380, min_size=32)
center(d, "和 8 万多非深户抢", (290, 520), 28, LIGHT, bold=False, min_size=22)
center(d, "→", (W / 2, 470), 64, GOLD, min_size=52)
rcard(d, W / 2 + 40, 380, W - HM, 560)
center(d, "本校 D 类位次", (790, 440), 40, GOLD, maxw=380, min_size=32)
center(d, "同校几个孩子比排名", (790, 520), 28, WHITE, bold=False, min_size=22)
mech = [
    "① 名额分配到各初中（名额到校）· D 类单列",
    "② 想用指标生 → 拼本校 D 类里的位次",
    "③ 在全校 D 类考生里排名越靠前，这张牌越硬",
]
y = 612
for t in mech:
    y1 = y + 108
    rcard(d, HM, y, W - HM, y1)
    left(d, t, (HM + 56, (y + y1) / 2), 31, WHITE, min_size=26)
    y = y1 + 16
center(d, "现在做：问学校本校 D 类指标名额 + 孩子位次", (W / 2, 1038), 32, WHITE, min_size=26)
center(d, "各初中名额怎么到校 · 另文单讲", (W / 2, 1100), 26, LIGHT, bold=False, min_size=22)
center(d, "池子变小 · 比“全市厮杀”现实得多", (W / 2, 1246), 36, GOLD, min_size=30)
footer(d)
check("正文图2")
im.save(HERE + "P1-3-S4-D类三张牌-小红书-正文图2-指标生-1080x1440.png")

# ========== 正文图3：牌② 民办 ==========
im, d = base()
center(d, "牌② · 民办普高", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "一条 ACD 线 · 不分 AC/D", (W / 2, 214), 56, WHITE, min_size=46)
center(d, "录取“面向全市 ACD 类” · 不存在“非深户要多考”", (W / 2, 300), 30, LIGHT, bold=False, min_size=24)
# 三个 stat tile
tiles = [
    ("49 所", "民办普高（2026）"),
    ("33,195", "学位（2026）"),
    ("3万-15万", "学费 / 年（区间）"),
]
tw, th, gap = 280, 216, 24
x0 = (W - (tw * 3 + gap * 2)) / 2
for i, (big, lab) in enumerate(tiles):
    x = x0 + i * (tw + gap)
    rcard(d, x, 370, x + tw, 370 + th)
    center(d, big, (x + tw / 2, 444), 50, GOLD, maxw=tw - 30, min_size=38)
    center(d, lab, (x + tw / 2, 534), 26, LIGHT, bold=False, min_size=21)
lines = [
    "D 类和深户 · 走同一条民办线报名录取",
    "公办 D 线够不着的分数段 · 这里也能上普高",
    "但：线低换的是学费高 · 办学口碑要挑",
]
y = 640
for t in lines:
    rcard(d, HM, y, W - HM, y + 108)
    left(d, t, (HM + 56, y + 54), 30, WHITE, min_size=25)
    y += 124
center(d, "定位：兜底不是首选 · 家里扛得起学费再谈", (W / 2, 1082), 34, WHITE, min_size=28)
center(d, "学费细账：见《普高和中职每年学费差多少》", (W / 2, 1150), 27, LIGHT, bold=False, min_size=22)
center(d, "分数够不到公办 D 线？这张同线的牌接得住", (W / 2, 1296), 34, GOLD, min_size=28)
footer(d)
check("正文图3")
im.save(HERE + "P1-3-S4-D类三张牌-小红书-正文图3-民办-1080x1440.png")

# ========== 正文图4：牌③ 3+4 贯通 ==========
im, d = base()
center(d, "牌③ · 3+4 中本贯通", (W / 2, 84), 32, GOLD, min_size=26)
center(d, "职校3年 + 本科4年", (W / 2, 214), 58, WHITE, min_size=48)
center(d, "毕业拿全日制本科文凭（应用型为主）", (W / 2, 300), 30, LIGHT, bold=False, min_size=24)
tiles = [
    ("300", "首批名额（2026）"),
    ("6 校 · 8 专业", "公办中职试点"),
    ("ACD 同线", "D 类可报"),
]
tw, th, gap = 280, 216, 24
x0 = (W - (tw * 3 + gap * 2)) / 2
for i, (big, lab) in enumerate(tiles):
    x = x0 + i * (tw + gap)
    rcard(d, x, 370, x + tw, 370 + th)
    center(d, big, (x + tw / 2, 446), 46, GOLD, maxw=tw - 24, min_size=34)
    center(d, lab, (x + tw / 2, 538), 25, LIGHT, bold=False, min_size=20)
lines = [
    "录取走中职批次 · 不进公办 D 类那 23% 名额池",
    "对口本科：深技大 / 深职大(深汕) / 深信职大 / 韩山师院",
    "第一批试点 · 知道的人还不多 · 信息差就是机会",
]
y = 640
for t in lines:
    rcard(d, HM, y, W - HM, y + 108)
    left(d, t, (HM + 56, y + 54), 29, WHITE, min_size=24)
    y += 124
center(d, "三句实话：读的是3年职校 · 专业只有8个 · 是另一条本科路", (W / 2, 1076), 30, WHITE, min_size=25)
center(d, "选专业 / 报名路径 · 之后单篇深挖（先关注）", (W / 2, 1144), 26, LIGHT, bold=False, min_size=21)
center(d, "挤不进的公办 D 线 · 换条路拿本科", (W / 2, 1290), 36, GOLD, min_size=30)
footer(d)
check("正文图4")
im.save(HERE + "P1-3-S4-D类三张牌-小红书-正文图4-3+4贯通-1080x1440.png")
print("done")
