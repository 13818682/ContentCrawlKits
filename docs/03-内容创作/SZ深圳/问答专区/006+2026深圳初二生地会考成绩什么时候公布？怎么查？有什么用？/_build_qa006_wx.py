# -*- coding: utf-8 -*-
"""
QA-006《2026深圳初二生地会考成绩即将公布：怎么查？这100分有什么用？》· 公众号配图
================================================================================
产出 9 张，全部写入本目录下的 01.公众号/ ：
  封面-精炼版 900x383        （四行左对齐，同 P1-5 起用的精简版封面模板）
  封面-极简版 900x383        （关键数字「100分」为视觉主角，落实"精简+极简"双方向铁律）
  章节条 1/2/3  900x220
  数据卡 1/2/3  900x400
  长图-极简版   900xH       （收藏型资产，单条渐变不拼接）

视觉档：**QA-006 档 = 蓝系家族（深钢蓝档）**
  主色永远深蓝系不换色相；与既有各档靠 深浅 × 光影 × 光线角度 × 装饰 × 版式 区分：
    主线 = 深靛蓝 (22,56,110) 中上方主光 · 同心分配环
    S1   = 深蓝   (14,44,92)  中上方主光 · 标尺刻度
    S2   = 中深蓝 (18,52,104) 左上主光   · 勾选框列
    QA-006 = 深钢蓝 (20,46,96) 右上主光  · 斜向刻度带（时间/分数刻度意象）

口径：见 ../00-QA-006-官方口径与历年查分时间核验.md
     成绩不计入中考总分 · 没有此成绩不能投档 · 同分比较第一层（生地先于语数英）
     2026 具体公布日期官方未发布 —— 图文一律不写死日期
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "01.公众号")
PFX = "QA-006-生地会考成绩"

FD = "C:/Windows/Fonts/"
FB = FD + "msyhbd.ttc"
FR = FD + "msyh.ttc"

# ---------------- QA-006 视觉档 ----------------
TOP, BOT = (20, 46, 96), (6, 16, 36)
CARD, EDGE = (12, 32, 68), (92, 140, 208)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)
SRC = "数据来源：深圳市教育局 / 深圳市招生考试办公室 官方公开信息"


def font(s, bold=False):
    return ImageFont.truetype(FB if bold else FR, s)


def base(w, h):
    """深钢蓝竖直渐变 + **右上主光**（区别于主线/S1/S2）+ 左下「斜向刻度带」装饰。"""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    c1 = np.array(TOP, np.float32)[None, None, :]
    c2 = np.array(BOT, np.float32)[None, None, :]
    arr = c1 * (1 - t) + c2 * t
    arr = np.repeat(arr, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # 主光：右上（0.80w, 0.12h）
    gx, gy = w * 0.80, h * 0.12
    d = np.sqrt(((xx - gx) / (w * 0.58)) ** 2 + ((yy - gy) / (h * 0.36)) ** 2)
    arr = arr + np.array((255, 255, 255), np.float32)[None, None, :] * (np.exp(-d * d) * 0.26)[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def decor_ticks(im):
    """左下「斜向刻度带」：一组 45° 短刻度，低透明度，只在装饰层，不遮文字。"""
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    n = 9 if h >= 600 else 6
    step_x = max(6, int(w * 0.052))
    step_y = max(4, int(h * 0.038))
    L = max(10, int(min(w, h) * 0.072))
    for i in range(n):
        x0 = int(w * 0.035) + i * step_x
        y0 = int(h * 0.70) + i * step_y
        if x0 + L > w - 4 or y0 + L > h - 4:
            break
        col = GOLD + (46,) if i % 3 == 1 else (255, 255, 255, 22)
        od.line([(x0, y0), (x0 + L, y0 + L)], fill=col, width=4)
    od.line([(int(w * 0.035), int(h * 0.70) - 10), (int(w * 0.035), int(h * 0.70) + n * step_y + L)],
            fill=(255, 255, 255, 30), width=2)
    im.paste(ov, (0, 0), ov)


def rcard(im, box, fill_alpha=0, outline=None, outline_alpha=255, radius=22, width=2):
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fill_alpha))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


CHECKS = []


def put(d, text, xy, size, fill, bold=True, anchor="mm", maxw=None, W=900, H=400, tag=""):
    """带宽度自适应与越界记录的文字绘制。"""
    f = font(size, bold)
    if maxw:
        while f.size > 10:
            bb = d.textbbox((0, 0), text, font=f)
            if bb[2] - bb[0] <= maxw + 1:
                break
            f = font(f.size - 1, bold)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox((0, 0), text, font=f)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    cx, cy = xy
    if anchor == "mm":
        x0, y0 = cx - bw / 2, cy - bh / 2
    elif anchor == "la":
        x0, y0 = cx, cy
    elif anchor == "lm":
        x0, y0 = cx, cy - bh / 2
    else:
        x0, y0 = cx - bw / 2, cy
    CHECKS.append((tag or text[:12], (x0, y0, x0 + bw, y0 + bh), W, H, maxw))
    return f


def gate(name, W, H, bottom_pad=20, side_pad=20):
    bad = []
    for tag, bb, w, h, maxw in CHECKS:
        if bb[0] < side_pad - 12 or bb[2] > w - side_pad + 12 or bb[1] < 8 or bb[3] > h - bottom_pad + 8:
            bad.append((tag, tuple(round(v) for v in bb)))
        elif maxw and (bb[2] - bb[0]) > maxw + 2:
            bad.append((tag, "maxw", round(bb[2] - bb[0]), maxw))
    print(("OK   " if not bad else "!!   ") + name, bad if bad else "")
    CHECKS.clear()
    return not bad


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    im.save(p)
    print("     saved", name, im.size)


# ==================== 1. 封面 · 精炼版 900x383 ====================
def cover_jinglian():
    """精炼版封面 = 时效/查分方向（担当紧迫感）：「随时可能公布」+「入口先存好」。"""
    W, H = 900, 383
    im = base(W, H)
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    put(d, "深圳中考", (60, 44), 26, SUB, bold=False, anchor="la", maxw=780, W=W, H=H, tag="k")
    # 定性前缀：把范围钉死在「初二 · 生地会考」，避免被读成其他学段/其他考试
    put(d, "初二生地会考：", (60, 120), 52, GOLD, anchor="la", maxw=800, W=W, H=H, tag="t0")
    put(d, "成绩随时可能公布", (60, 206), 58, WHITE, anchor="la", maxw=800, W=W, H=H, tag="t1")
    put(d, "入口先存好 · 出分当天不慌", (60, 310), 32, GOLD, bold=False, anchor="la",
        maxw=800, W=W, H=H, tag="t2")
    gate("公众号封面-精炼版", W, H)
    save(im, f"{PFX}-公众号-封面-精炼版-900x383.png")


# ==================== 2. 封面 · 极简版 900x383 ====================
def cover_jijian():
    """极简方向：关键数字「100」为视觉主角 + 金白对撞（不计入总分 vs 不能投档）。"""
    W, H = 900, 383
    im = base(W, H)
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    put(d, "深圳中考 · 初二生地会考", (W / 2, 46), 26, SUB, bold=False, W=W, H=H, tag="k")
    put(d, "100分", (W / 2 + 3, 180), 116, (0, 16, 36), W=W, H=H, tag="sh")
    put(d, "100分", (W / 2, 176), 116, GOLD, W=W, H=H, tag="n")
    d.line([W / 2 - 250, 250, W / 2 + 250, 250], fill=(255, 255, 255, 90), width=2)
    put(d, "不计入中考总分", (W / 2, 292), 44, WHITE, W=W, H=H, tag="a")
    put(d, "但没有它，录取时不能投档", (W / 2, 348), 30, GOLD, bold=False, W=W, H=H, tag="b")
    gate("公众号封面-极简版", W, H)
    save(im, f"{PFX}-公众号-封面-极简版-900x383.png")


# ==================== 3. 章节条 900x220 ×3 ====================
def section(idx, num, title, sub, name, light="glow-tr"):
    W, H = 900, 220
    im = base(W, H)
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    cx, cy = 96, H / 2
    d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=GOLD)
    put(d, num, (cx, cy), 40, (18, 30, 55), W=W, H=H, tag="num")
    put(d, title, (158, cy - 26), 44, WHITE, anchor="lm", maxw=680, W=W, H=H, tag="title")
    put(d, sub, (158, cy + 30), 24, LIGHT, bold=False, anchor="lm", maxw=700, W=W, H=H, tag="sub")
    gate(f"公众号章节条-{name}", W, H)
    save(im, f"{PFX}-公众号-章节条{idx}-{name}-900x220.png")


# ==================== 4. 数据卡 900x400 ×3 ====================
def card_times():
    """历年查分时间表。"""
    W, H = 900, 400
    im = base(W, H)
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    put(d, "历年查分时间 · 都在 9 月，上午 10 点", (450, 40), 34, WHITE, maxw=760, W=W, H=H, tag="t")
    put(d, "2026 年具体日期以市招考办公告为准", (450, 76), 19, LIGHT, bold=False, W=W, H=H, tag="sub")
    tx0, tx1 = 60, 840
    rcard(im, [tx0, 100, tx1, 140], fill_alpha=26, radius=16)
    put(d, "年份", (190, 120), 24, WHITE, W=W, H=H, tag="h1")
    put(d, "成绩查询时间", (560, 120), 24, WHITE, W=W, H=H, tag="h2")
    rows = [
        ("2025年", "9月18日 10:00", WHITE),
        ("2024年", "9月19日 10:00", WHITE),
        ("2023年", "9月22日 10:00", WHITE),
        ("2022年", "10月10日 10:00", LIGHT),
        ("2026年", "官方未发布 · 近期留意", GOLD),
    ]
    ry0 = 146
    row_h = 44
    for i, (y, v, col) in enumerate(rows):
        ry = ry0 + i * row_h
        if i % 2 == 0:
            rcard(im, [tx0, ry, tx1, ry + row_h], fill_alpha=12, radius=12)
        put(d, y, (190, ry + row_h / 2), 25, (235, 243, 252), W=W, H=H, tag="y")
        put(d, v, (560, ry + row_h / 2), 25 if i == 4 else 26, col, W=W, H=H, tag="v")
    gate("公众号数据卡1", W, H)
    save(im, f"{PFX}-公众号-数据卡1-历年查分时间-900x400.png")


def card_score():
    """成绩怎么构成 + 等级怎么划。"""
    W, H = 900, 400
    im = base(W, H)
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    put(d, "这 100 分怎么来的", (450, 40), 34, WHITE, maxw=760, W=W, H=H, tag="t")
    # 上排：100 = 95 + 5
    rcard(im, [60, 82, 840, 186], fill_alpha=16, radius=18)
    put(d, "满分 100 分", (170, 116), 28, WHITE, W=W, H=H, tag="a1")
    put(d, "＝", (280, 112), 32, GOLD, W=W, H=H, tag="eq")
    put(d, "笔试卷面 95 分", (420, 116), 28, LIGHT, W=W, H=H, tag="a2")
    put(d, "＋", (545, 112), 32, GOLD, W=W, H=H, tag="plus")
    put(d, "实验操作 5 分", (665, 116), 28, GOLD, W=W, H=H, tag="a3")
    put(d, "笔试 95 = 生物学 45 ＋ 地理 50", (450, 162), 22, SUB, bold=False, W=W, H=H, tag="a4")
    # 下排：等级比例
    put(d, "单科等级按成绩划定 · 比例固定", (450, 214), 26, WHITE, maxw=760, W=W, H=H, tag="b0")
    grades = [("A+", "5%", GOLD), ("A", "20%", WHITE), ("B+", "25%", WHITE),
              ("B", "25%", WHITE), ("C+", "20%", LIGHT), ("C", "5%", LIGHT)]
    cw, gap = 118, 14
    x0 = (W - (cw * 6 + gap * 5)) / 2
    for i, (g, p, col) in enumerate(grades):
        x = x0 + i * (cw + gap)
        rcard(im, [x, 242, x + cw, 320], fill_alpha=16, outline=(255, 255, 255),
              outline_alpha=70, radius=16)
        put(d, g, (x + cw / 2, 268), 32, col, W=W, H=H, tag="g")
        put(d, p, (x + cw / 2, 300), 24, LIGHT, bold=False, W=W, H=H, tag="p")
    put(d, "满分人数超 5% 时，满分者均为 A+", (450, 352), 20, LIGHT, bold=False, W=W, H=H, tag="c")
    gate("公众号数据卡2", W, H)
    save(im, f"{PFX}-公众号-数据卡2-成绩构成与等级-900x400.png")


def card_roles():
    """这 100 分的 4 个作用。"""
    W, H = 900, 400
    im = base(W, H)
    decor_ticks(im)
    d = ImageDraw.Draw(im)
    put(d, "这 100 分的 4 个作用", (450, 38), 34, WHITE, maxw=760, W=W, H=H, tag="t")
    put(d, "不计入中考总分 · 却是录取门槛 + 同分决胜分", (450, 72), 19, GOLD,
        bold=False, W=W, H=H, tag="sub")
    rows = [
        ("①", "有成绩才能投档", "没有这项成绩的，高中录取时不能投档", GOLD),
        ("②", "同分比较第一层", "总分相同先比生地，比语数英更优先", GOLD),
        ("③", "名额分配批同样适用", "指标生批次遇同分，也走同一条规则", LIGHT),
        ("④", "缺考可补考", "缺考者可申请参加下一年度考试", LIGHT),
    ]
    ry = 94
    for n, tag, note, col in rows:
        rcard(im, [60, ry, 840, ry + 64], fill_alpha=16, outline=(255, 255, 255),
              outline_alpha=60, radius=16)
        d.ellipse([82, ry + 19, 108, ry + 45], fill=GOLD)
        put(d, n, (95, ry + 32), 19, (18, 30, 55), W=W, H=H, tag="n")
        put(d, tag, (130, ry + 21), 26, col, anchor="lm", maxw=420, W=W, H=H, tag="r1")
        put(d, note, (130, ry + 50), 20, SUB, bold=False, anchor="lm", maxw=690, W=W, H=H, tag="r2")
        ry += 70
    gate("公众号数据卡3", W, H)
    save(im, f"{PFX}-公众号-数据卡3-四个作用-900x400.png")


# ==================== 5. 长图 · 极简版 900xH ====================
LH = 3360


def longimage():
    W, H = 900, LH
    # 长图用稍浅的头、稍深尾，与短图同档同色相
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    c1 = np.array((24, 54, 108), np.float32)[None, None, :]
    c2 = np.array((6, 16, 36), np.float32)[None, None, :]
    arr = np.repeat(c1 * (1 - t) + c2 * t, W, axis=1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dtop = np.sqrt(((xx - W * 0.5) / (W * 0.46)) ** 2 + ((yy - H * 0.055) / (H * 0.10)) ** 2)
    arr = arr + np.array((160, 205, 245), np.float32)[None, None, :] * (np.exp(-dtop * dtop) * 0.20)[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(im)

    def P(text, size, xy, color=WHITE, bold=True, anchor="mm", maxw=None, tag=""):
        return put(d, text, xy, size, color, bold=bold, anchor=anchor, maxw=maxw, W=W, H=H, tag=tag)

    def box(x, y, w, h, r=16, fa=0, outline=EDGE, oa=255):
        rcard(im, [x, y, x + w, y + h], fill_alpha=fa, outline=outline, outline_alpha=oa,
              radius=r, width=2)

    def pill(cx, cy, text, size, color):
        f = font(size, True)
        bb = d.textbbox((0, 0), text, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x0, y0 = cx - tw / 2 - 30, cy - th / 2 - 14
        x1, y1 = cx + tw / 2 + 30, cy + th / 2 + 14
        d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, outline=color, width=2)
        P(text, size, (cx, cy), color, tag="pill")

    def chapter(y, text):
        d.rectangle([50, y - 27, 58, y + 27], fill=GOLD)
        P(text, 36, (78, y), WHITE, anchor="lm", tag="ch")
        d.line([50, y + 45, 145, y + 45], fill=GOLD, width=3)

    def row(y, tag, detail, tagcolor=GOLD, h=90):
        box(40, y, W - 80, h, r=16, fa=14)
        P(tag, 25, (76, y + 30), tagcolor, anchor="lm", maxw=380, tag="rt")
        P(detail, 20, (76, y + 64), WHITE, bold=False, anchor="lm", maxw=720, tag="rd")

    def take(y, text, color=GOLD):
        P(text, 21, (W / 2, y), color, maxw=W - 80, tag="take")

    # ---- 钩子区 ----
    pill(W / 2, 56, "深圳中考 · 初二生地会考", 22, GOLD)
    P("生地会考成绩", 68, (W / 2, 158), WHITE, maxw=800, tag="h1")
    P("什么时候出？", 68, (W / 2, 244), WHITE, maxw=800, tag="h2")
    P("就在这几天", 108, (W / 2 + 3, 396), (0, 16, 36), tag="h3s")
    P("就在这几天", 108, (W / 2, 392), GOLD, tag="h3")
    # 数据对撞：100 分 vs 计入总分 0 分
    box(70, 476, 760, 140, r=18, fa=16, outline=GOLD)
    d.line([450, 496, 450, 596], fill=GOLD, width=2)
    P("100分", 58, (285, 528), GOLD, tag="v1")
    P("生地会考满分", 24, (285, 584), LIGHT, bold=False, tag="v1l")
    P("0分", 58, (640, 528), WHITE, tag="v2")
    P("计入中考总分", 24, (640, 584), LIGHT, bold=False, tag="v2l")
    pill(W / 2, 668, "怎么查 · 历年时间 · 这 100 分的用处", 25, GOLD)
    d.line([60, 718, 250, 718], fill=GOLD, width=3)

    # ---- 01 什么时候出 ----
    chapter(778, "01 · 什么时候出？")
    P("历年都在 9 月中下旬的上午 10:00 开放查询：", 21, (W / 2, 852), LIGHT, bold=False,
      maxw=760, tag="p1")
    times = [("2025年", "9月18日 10:00", GOLD), ("2024年", "9月19日 10:00", GOLD),
             ("2023年", "9月22日 10:00", GOLD), ("2022年", "10月10日 10:00", LIGHT)]
    ry = 890
    for y, v, col in times:
        box(60, ry, W - 120, 62, r=12, fa=14)
        P(y, 24, (200, ry + 31), WHITE, tag="ty")
        P(v, 26, (600, ry + 31), col, tag="tv")
        ry += 72
    take(ry + 26, "2026 年官方尚未发布确切日期 · 以市招考办公告为准")

    # ---- 02 怎么查 ----
    chapter(1280, "02 · 怎么查？")
    P("入口：深圳招考网 → 招考服务栏目 → 初二学业水平考试成绩查询", 21, (W / 2, 1354),
      LIGHT, bold=False, maxw=800, tag="p2")
    steps = [
        ("①", "11 位考生号", "报名时分配的考生号，别填成学籍号"),
        ("②", "身份证件号后 6 位", "有字母须大写，如 Y023456(A) 填 23456A"),
        ("③", "验证码", "查分页面会显示，照填即可"),
    ]
    ry = 1400
    for n, tag, note in steps:
        box(60, ry, W - 120, 84, r=16, fa=14)
        d.ellipse([84, ry + 26, 112, ry + 54], fill=GOLD)
        P(n, 20, (98, ry + 40), (18, 30, 55), tag="sn")
        P(tag, 25, (140, ry + 30), WHITE, anchor="lm", maxw=420, tag="st")
        P(note, 20, (140, ry + 64), LIGHT, bold=False, anchor="lm", maxw=700, tag="sn2")
        ry += 94
    take(ry + 22, "成绩公布当天，查询页面的年份会更新为「2026」")
    take(ry + 58, "最终成绩以市招考办下发的成绩单为准", WHITE)

    # ---- 03 这 100 分有什么用 ----
    chapter(1810, "03 · 这 100 分，有什么用？")
    roles = [
        ("有成绩才能投档", "没有这项成绩的，高中阶段学校录取时不能投档", GOLD),
        ("同分比较第一层", "总分相同时先比生地，比语数英更优先", GOLD),
        ("名额分配批同样适用", "指标生批次遇同分，也走同一条规则", LIGHT),
        ("缺考可补考", "缺考者可申请参加下一年度考试，但缺考当年不能投档", LIGHT),
    ]
    ry = 1883
    for tag, note, col in roles:
        row(ry, tag, note, col)
        ry += 102
    take(ry + 20, "不计入中考总分，却同时是「门槛」和「决胜分」")

    # ---- 04 两个别误读 ----
    chapter(2380, "04 · 两个最容易误读的说法")
    ry = 2452
    for t, n in [("「不计分，所以不用管」",
                  "它是投档门槛：没有成绩，当年直接不能投档"),
                 ("「考完就彻底定格了」",
                  "已考完的分数确实改不了；缺考的可以申请下一年补考")]:
        box(50, ry, W - 100, 108, r=18, fa=16, outline=GOLD)
        P(t, 25, (78, ry + 34), GOLD, anchor="lm", maxw=760, tag="mt")
        P(n, 20, (78, ry + 74), WHITE, bold=False, anchor="lm", maxw=760, tag="mn")
        ry += 124

    # ---- 05 给家长 ----
    chapter(2760, "05 · 现在做这 3 件事")
    ry = 2830
    for n, t in [("①", "关注我：出分当天第一时间贴入口与注意事项"),
                 ("②", "把查分入口存进收藏夹，别等出分才翻"),
                 ("③", "查分当天记下分数并截图核对，别等填志愿才找")]:
        box(60, ry, W - 120, 74, r=14, fa=14)
        P(n, 24, (96, ry + 37), GOLD, tag="fn")
        P(t, 22, (140, ry + 37), WHITE, bold=False, anchor="lm", maxw=700, tag="ft")
        ry += 86

    # ---- 页脚 ----
    divy = ry + 40
    d.line([50, divy, W - 50, divy], fill=EDGE, width=2)
    P("关注我 · 深圳中考问答系列连载中", 32, (W / 2, divy + 46), GOLD, tag="cta")
    P("成绩公布当天，我会同步更新查分入口与注意事项", 20, (W / 2, divy + 96), LIGHT,
      bold=False, tag="cta2")
    P(SRC, 18, (W / 2, divy + 140), SUB, bold=False, maxw=W - 80, tag="src")
    P("本文为政策信息整理，具体以深圳市教育局、市招考办正式公告为准", 17,
      (W / 2, divy + 176), LIGHT, bold=False, maxw=W - 80, tag="dis")

    assert divy + 176 < H - 18, (divy, H)
    gate("公众号长图-极简版", W, H, bottom_pad=10, side_pad=18)
    save(im, f"{PFX}-公众号-长图-极简版-900x{H}.png")


if __name__ == "__main__":
    cover_jinglian()
    cover_jijian()
    section(1, "一", "什么时候出", "历年都在 9 月中下旬 · 上午 10 点开放", "历年时间")
    section(2, "二", "怎么查", "深圳招考网 · 考生号 ＋ 身份证后 6 位", "怎么查")
    section(3, "三", "有什么用", "不计入总分 · 但没它不能投档", "有什么用")
    card_times()
    card_score()
    card_roles()
    longimage()
    print("ALL DONE (公众号)")
