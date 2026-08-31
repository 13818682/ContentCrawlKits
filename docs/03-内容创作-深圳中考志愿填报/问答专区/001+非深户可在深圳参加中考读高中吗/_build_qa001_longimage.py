# -*- coding: utf-8 -*-
"""QA-001 公众号长图极简版（900×~3200，风格同 S1-7 长图：金竖条章节头/行盒/页脚）
开头钩子区（首屏）：答案大字「能读！」+ 数据对撞「54% vs 23%」→ 抓眼球、提关注度与点击率。
内容：直接答案3条 → 5项条件表 → 竞争54%vs23% → 三条出路 → 给非深户家长的三句话 → 关注CTA页脚。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 3220
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
SHADOW = (0, 20, 45)

FD = "C:/Windows/Fonts/"
def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 1.35))
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)

# ---------- 背景：竖直渐变 + 顶部中心光晕（让钩子区更醒目） ----------
t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
arr = arr.repeat(W, axis=1)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.sqrt(((x - W / 2) / (W * 0.45)) ** 2 + ((y - H * 0.09) / (H * 0.16)) ** 2)
g = np.exp(-d * d) * 0.22
arr += np.array((150, 200, 240), np.float32)[None, None, :] * g[:, :, None]
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
d = ImageDraw.Draw(img)

checks = []
def put(text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
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
    checks.append((text, fnt, xy, anchor, color, maxw))
    return fnt

def box(x, y, w, h, fill=CARD, outline=EDGE, r=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def pill(cx, cy, text, fnt, color, pad=30, ypad=12):
    bb = d.textbbox((0, 0), text, font=fnt)
    x0 = cx - (bb[2] + pad * 2) / 2; y0 = cy - (bb[3] + ypad * 2) / 2
    x1 = x0 + bb[2] + pad * 2; y1 = y0 + bb[3] + ypad * 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, outline=color, width=2)
    put(text, fnt, (cx, cy), color=color)

def chapter(ty, txt):
    d.rectangle([50, ty - 27, 58, ty + 27], fill=GOLD)
    put(txt, font(36, True), (78, ty), anchor="lm", color=WHITE)
    d.line([50, ty + 45, 140, ty + 45], fill=GOLD, width=3)

def row(ry, tag, detail, tagcolor=GOLD):
    box(40, ry, W - 80, 90)
    put(tag, font(17, True), (76, ry + 28), anchor="lm", color=tagcolor)
    put(detail, font(14), (76, ry + 62), anchor="lm", color=WHITE, maxw=700)

def takeaway(ty, txt):
    put(txt, font(15, True), (W / 2, ty), color=GOLD, maxw=W - 80)

# ================= 开头钩子区（首屏，非常醒目） =================
pill(W / 2, 54, "深圳中考 · 问答系列 · 001", font(22, True), GOLD)
# 大问题两行放大（72px），突出视觉效果
put("非深户能在深圳", font(72, True), (W / 2 + 3, 153), color=SHADOW)
put("非深户能在深圳", font(72, True), (W / 2, 150), color=WHITE, maxw=820)
put("读高中吗？", font(72, True), (W / 2 + 3, 243), color=SHADOW)
put("读高中吗？", font(72, True), (W / 2, 240), color=WHITE, maxw=820)
# 金色巨型答案（120px）
put("能读！", font(120, True), (W / 2 + 3, 379), color=SHADOW)      # 阴影
put("能读！", font(120, True), (W / 2, 376), color=GOLD)            # 金色巨型答案

# 数据对撞带：54% vs 23%
box(70, 458, 760, 132, fill=CARD, outline=GOLD, r=18)
d.line([450, 476, 450, 572], fill=GOLD, width=2)
put("54%", font(60, True), (280, 506), color=GOLD)
put("非深户考生占比", font(25), (280, 562), color=LIGHT)
put("23%", font(60, True), (640, 506), color=WHITE)
put("公办D类指标占比", font(25), (640, 562), color=LIGHT)

pill(W / 2, 646, "5项条件 · 3条出路 · 一次讲清", font(26, True), GOLD)
d.line([60, 698, 240, 698], fill=GOLD, width=3)

# ================= 01 直接答案：可以读 =================
chapter(758, "01 · 直接答案：可以读")
rows_01 = [
    ("资格", "满足5项条件 → 公办 / 民办 / 中职都能报", GOLD),
    ("竞争", "54%考生 · 抢23%公办指标 · 路更窄，但能走", LIGHT),
    ("出路", "公办指标生 · 民办同分 · 中职3+4，三层都能走", LIGHT),
]
ry = 820
for tag, dt, tc in rows_01:
    row(ry, tag, dt, tc)
    ry += 102

# ================= 02 资格：5项条件表 =================
chapter(1138, "02 · 资格：5项条件，对号入座")
put("条件", font(15, True), (120, 1204), color=LIGHT)
put("关键要点", font(15, True), (360, 1204), color=LIGHT)
d.line([80, 1222, 820, 1222], fill=GOLD, width=2)
conds = [
    ("①", "合法稳定职业", "父母一方在深有合法稳定职业"),
    ("②", "合法稳定住所", "父母一方在深有合法稳定住所"),
    ("③", "有效居住证", "父母一方持有，注意有效期"),
    ("④", "社保累计满3年", "两险都缴，至少一个险种满3年（补缴不计）"),
    ("⑤", "3年完整初中学籍", "在深完成3年完整初中"),
]
ry = 1252
for n, c, desc in conds:
    box(60, ry, W - 120, 68, r=12)
    d.ellipse([84, ry + 17, 116, ry + 49], fill=GOLD)
    put(n, font(24, True), (100, ry + 33), color=SHADOW)
    put(c, font(16, True), (150, ry + 34), anchor="lm", color=WHITE)
    put(desc, font(14), (620, ry + 34), anchor="mm", color=WHITE, maxw=430)
    ry += 78
takeaway(1668, "条件不全 ≠ 没书读：仍可参加民办普高补录 / 中职注册入学")

# ================= 03 竞争：54% vs 23% =================
chapter(1728, "03 · 竞争：54%考生，抢23%公办指标")
box(60, 1795, 380, 168, r=18)
put("约8.3万", font(56, True), (250, 1855), color=GOLD)
put("D类考生（2026年）", font(24), (250, 1928), color=WHITE)
box(460, 1795, 380, 168, r=18)
put("18,506", font(56, True), (650, 1855), color=WHITE)
put("公办D类指标名额", font(24), (650, 1928), color=WHITE)
put("四大AC类与D类分数线基本持平（差0-5分）；普通校、新校D线通常高出AC线13-31分。",
    font(15), (W / 2, 2016), color=LIGHT, maxw=760)
takeaway(2070, "这意味着什么：分数越高，户籍差距越小；越往下，选校策略越关键。")

# ================= 04 出路：三层 =================
chapter(2130, "04 · 出路：公办之外，还有两层")
rows_04 = [
    ("公办普高", "D类指标生 9,186个 · 96/97所高中覆盖 · 控制线约低20分", GOLD),
    ("民办普高", "49所 · 33,195个学位 · AC/D同分录取 · 学费约3万-15万/年", LIGHT),
    ("中职 · 3+4", "300个名额 · 中职3年+本科4年 · 毕业拿全日制本科文凭", LIGHT),
]
ry = 2195
for tag, dt, tc in rows_04:
    row(ry, tag, dt, tc)
    ry += 102
takeaway(2510, "全市普高（含民办）录取率超过73%")

# ================= 05 给非深户家长的三句话 =================
chapter(2570, "05 · 给非深户家长的三句话")
rows_05 = [
    ("①", "先过资格关", "材料现在核对 · 报名在3月下旬（网上）", GOLD),
    ("②", "用D线定位", "别用AC线", LIGHT),
    ("③", "三条腿走路", "公办 + 民办 + 中职，别只盯公办一条路", LIGHT),
]
ry = 2635
for n, tag, dt, tc in rows_05:
    box(60, ry, W - 120, 86, r=14)
    d.ellipse([84, ry + 24, 112, ry + 52], fill=GOLD)
    put(n, font(22, True), (98, ry + 38), color=SHADOW)
    put(tag, font(16, True), (140, ry + 30), anchor="lm", color=WHITE)
    put(dt, font(13), (140, ry + 66), anchor="lm", color=LIGHT, maxw=620)
    ry += 100

# ================= 页脚 =================
divy = 2960
d.line([50, divy, 850, divy], fill=EDGE, width=2)
put("关注我 · 问答系列连载更新中", font(34, True), (W / 2, divy + 40), color=GOLD)
put("你家孩子是深户还是非深户？评论区聊聊", font(15), (W / 2, divy + 88), color=LIGHT)
put("下一篇按大家最关心的问题来写 · 深圳中考系列连载", font(14), (W / 2, divy + 126), color=SUB)
put("（数据来自深圳市教育局官方公开信息，逐条人工核对后整理、编辑审核后发布）",
    font(11), (W / 2, divy + 168), color=LIGHT, maxw=W - 80)

out = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/001+非深户可在深圳参加中考读高中吗/公众号长图-极简版-900x{}.png".format(H)
img.save(out)
print("saved", out, img.size)

# ---------- 校验：越界 + 重叠 ----------
bad = 0; bxs = []
for (text, fnt, (cx, cy), anchor, color, maxw) in checks:
    bbox = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
    x0, y0 = bbox[0] + cx, bbox[1] + cy
    x1, y1 = bbox[2] + cx, bbox[3] + cy
    w = x1 - x0
    bxs.append(((x0, y0, x1, y1), text, (cx, cy)))
    ok = (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1)
    if maxw and w > maxw + 2:
        ok = False
    if not ok:
        bad += 1
        print(f"OVERFLOW [{text[:20]}] x=({x0:.0f},{x1:.0f}) y=({y0:.0f},{y1:.0f}) maxw={maxw}")
print("OVERFLOW:", "PASS" if bad == 0 else f"FAIL {bad}")
ov = 0
for i in range(len(bxs)):
    for j in range(i + 1, len(bxs)):
        (ax0, ay0, ax1, ay1), at, ac = bxs[i]
        (bx0, by0, bx1, by1), bt, bc = bxs[j]
        if ac == bc or at == bt:
            continue
        ox = max(0, min(ax1, bx1) - max(ax0, bx0))
        oy = max(0, min(ay1, by1) - max(ay0, by0))
        if ox > 4 and oy > 4:
            ov += 1
            print(f"OVERLAP: [{at[:14]}] x [{bt[:14]}]")
print("OVERLAP:", "PASS" if ov == 0 else f"FAIL {ov}")

# ---------- 采样：钩子区大字 + 渐变 ----------
arr2 = np.array(img)
for (py, lbl, expect) in [(150, "大问题行1白字", "white"), (240, "大问题行2白字", "white"), (376, "能读！金字", "gold"), (506, "数据带金/白", "gold")]:
    px = arr2[py, W // 2, :]
    print(f"钩子区 {lbl} @(450,{py}):", px.tolist())
print("GRADIENT top@(5,0):", arr2[0, 5, :].tolist(), "bottom@(5,H-1):", arr2[H - 1, 5, :].tolist())
