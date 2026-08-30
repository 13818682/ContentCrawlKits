# -*- coding: utf-8 -*-
"""S1-7 小红书配图（1080×1440 3:4）——按 13-3 小红书规范重生成
两篇笔记 × 2 张（首图+正文图）= 4 张：
  07 备考时间线：首图(300天/4段/10天) + 正文图-时间线(4阶段)
  08 志愿清单： 首图(10天/1所/35分) + 正文图-核对清单(4项)
风格：深蓝渐变 + 金色数据 + 微软雅黑；字号 主标题44 / 大数字56 / 标签34 / 正文30（下限22）
复用 S1-6/QA-002 分镜头规范：光影层次、gap_report 文字-边框≥15px/卡间距≥30px、verify 0越界。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
FD = "C:/Windows/Fonts/"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def new_canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.5:
            k = p / 0.5
            col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.5) / 0.5
            col = c_mid * (1 - k) + c_bot * k
        base[y, :, :] = col
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.62 + 0.38 * diag)
    spots = [
        ((0.80, 0.14), (150, 200, 240)),
        ((0.20, 0.20), (120, 180, 235)),
        ((0.74, 0.74), (95, 160, 225)),
        ((0.28, 0.86), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]
    col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    g = np.exp(-dist * dist) * 0.30
    base += col[None, None, :] * g[:, :, None]
    base = np.clip(base, 0, 255)
    img = Image.fromarray(base.astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img), []


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 22:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    ck.append((text, fnt, xy, anchor))


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=20):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)


def verify(d, ck, name):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} @({cx},{cy})")
    print(f"{name}: 共{len(ck)}处文字，{bad}处越界")


def gap_report(d, ck, name, cards):
    print(f"--- {name} 间隙检测 ---")
    ok = True
    for ci, (x, y, w, h) in enumerate(cards):
        mt = mb = ml = mr = 10 ** 9
        for (text, fnt, (cx, cy), anchor) in ck:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + cx, bb[1] + cy
            x1, y1 = bb[2] + cx, bb[3] + cy
            if x < cx < x + w and y < cy < y + h:
                mt = min(mt, y0 - y); mb = min(mb, y + h - y1)
                ml = min(ml, x0 - x); mr = min(mr, x + w - x1)
        flag = "OK" if (mt >= 15 and mb >= 15 and ml >= 15 and mr >= 15) else "⚠️ 不足"
        if flag != "OK":
            ok = False
        print(f"  卡{ci+1} ({x},{y} {w}x{h}): 上{mt} 下{mb} 左{ml} 右{mr}  {flag}")
    if len(cards) > 1:
        for i in range(len(cards) - 1):
            # 纵向堆叠卡：用 y 轴间距；若同行横排则用 x 轴间距
            gy = cards[i + 1][1] - (cards[i][1] + cards[i][3])
            gx = cards[i + 1][0] - (cards[i][0] + cards[i][2])
            gap = gy if abs(gy) < abs(gx) else gx
            flag = "OK" if gap >= 30 else "⚠️ 过窄"
            if flag != "OK":
                ok = False
            print(f"  卡间距{i+1}-{i+2}: {gap}px  {flag}")
    return ok


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/03-小红书/"
N = "S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-小红书"
ALL_OK = True


def data_cards(d, ck, y, cards, cards_list):
    """三张数据卡：数字(56金)上 + 标签(30白)下，卡宽280，间距30。"""
    for (xc, num, lab) in cards:
        box(d, xc - 140, y, 280, 150)
        cards_list.append((xc - 140, y, 280, 150))
        put(d, ck, num, font(56, True), (xc, y + 58), color=GOLD)
        put(d, ck, lab, font(30), (xc, y + 116), color=WHITE)


def list_row(d, ck, y, num, title, desc, cards_list=None):
    """清单行：编号金圆 + 标题白34 + 说明浅蓝30。"""
    box(d, 60, y, 960, 130, r=18)
    if cards_list is not None:
        cards_list.append((60, y, 960, 130))
    d.ellipse([100, y + 45, 160, y + 105], fill=GOLD)
    put(d, ck, num, font(34, True), (130, y + 75), color=(18, 30, 55))
    put(d, ck, title, font(34, True), (200, y + 38), anchor="lm", color=WHITE)
    put(d, ck, desc, font(30), (200, y + 90), anchor="lm", color=LIGHT)


# ========== 07 首图：备考时间线 ==========
img, d, ck = new_canvas(0)
put(d, ck, "深圳中考 · S1 · 备考时间线", font(22, True), (60, 90), anchor="lm", color=GOLD)
put(d, ck, "2027中考备考时间线", font(44, True), (60, 230), anchor="lm")
put(d, ck, "每月做什么 · 现在开始刚刚好", font(30), (60, 310), anchor="lm", color=LIGHT)
d.line([60, 360, 200, 360], fill=GOLD, width=3)
c7 = []
data_cards(d, ck, 430, [(230, "300天", "备考倒计时窗口"), (540, "4段", "备考阶段"), (850, "10天", "志愿填报窗口")], c7)
ALL_OK &= gap_report(d, ck, "07首图·数据卡", c7)
put(d, ck, "4个关键阶段", font(34, True), (60, 670), anchor="lm", color=GOLD)
stages = [("① 现在（2026.8）", "确认体育过程性评价分 · 搭认知框架"),
          ("② 2027年1-3月", "一模 · 定位基准"),
          ("③ 2027年4-5月", "指标生名额公布 · 5月下旬志愿填报约10天"),
          ("④ 2027年6-7月", "中考 → 录取")]
for i, (t, s) in enumerate(stages):
    put(d, ck, t, font(34, True), (120, 760 + i * 105), anchor="lm", color=WHITE)
    put(d, ck, s, font(30), (120, 803 + i * 105), anchor="lm", color=LIGHT)
put(d, ck, "收藏照着做 · 按月对照", font(34, True), (540, 1300), color=GOLD)
put(d, ck, "数据来源：深圳市教育局公开信息", font(22), (540, 1385), color=SUB)
verify(d, ck, "07首图")
img.save(BASE + "07-" + N + "-备考时间线-首图-1080x1440.png")

# ========== 07 正文图：时间线 ==========
img, d, ck = new_canvas(1)
put(d, ck, "深圳中考 · S1 · 备考时间线", font(22, True), (60, 90), anchor="lm", color=GOLD)
put(d, ck, "备考时间线 · 关键节点", font(44, True), (60, 200), anchor="lm")
d.line([60, 250, 200, 250], fill=GOLD, width=3)
tl = []
blocks = [("① 现在（2026.8）", "确认体育过程性评价历史分，规划初三训练。开始搭认知框架，别等明年5月才动手。"),
          ("② 2027年1-3月", "一模定位基准。各区一模时间不同，通常在初三下学期初。用一模成绩对目标学校才靠谱。"),
          ("③ 2027年4-5月", "招生计划、指标生名额陆续公布；5月下旬志愿填报，只有约10天。先填志愿、后考试。"),
          ("④ 2027年6-7月", "中考 → 录取。前面准备充分，这段就是验证。")]
by = 320
for i, (t, s) in enumerate(blocks):
    d.ellipse([108, by + 20, 140, by + 52], fill=GOLD)
    if i < 3:
        d.line([124, by + 52, 124, by + 282], fill=EDGE, width=3)
    box(d, 180, by, 840, 230, r=20)
    tl.append((180, by, 840, 230))
    put(d, ck, t, font(34, True), (220, by + 42), anchor="lm", color=GOLD)
    lines = s.split("。")
    yy = by + 96
    for ln in [x for x in lines if x.strip()]:
        put(d, ck, ln + ("。" if ln != lines[-1] else ""), font(30), (220, yy), anchor="lm", color=WHITE, maxw=760)
        yy += 48
    by += 260
ALL_OK &= gap_report(d, ck, "07正文·时间线块", tl)
put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(22), (540, 1400), color=SUB)
verify(d, ck, "07正文")
img.save(BASE + "07-" + N + "-备考时间线-正文图-时间线-1080x1440.png")

# ========== 08 首图：志愿清单 ==========
img, d, ck = new_canvas(2)
put(d, ck, "深圳中考 · S1 · 志愿填报", font(22, True), (60, 90), anchor="lm", color=GOLD)
put(d, ck, "收藏！志愿填报前要核对的清单", font(44, True), (60, 230), anchor="lm")
put(d, ck, "先填志愿后考试 · 只有约10天", font(30), (60, 310), anchor="lm", color=LIGHT)
d.line([60, 360, 200, 360], fill=GOLD, width=3)
c8 = []
data_cards(d, ck, 430, [(230, "10天", "志愿填报窗口"), (540, "1所", "指标生只能填"), (850, "35分", "走读最高降分")], c8)
ALL_OK &= gap_report(d, ck, "08首图·数据卡", c8)
put(d, ck, "4项核对清单", font(34, True), (60, 670), anchor="lm", color=GOLD)
items = [("① 指标生", "查名额分配+目标高中近2年使用"),
         ("② 走读 / 住宿", "评估通勤 · 录取后不可改回"),
         ("③ 候选方案", "民办低进高出 · 中职3+4/3+2"),
         ("④ 定位基准", "一模成绩出来再定冲稳保")]
for i, (t, s) in enumerate(items):
    put(d, ck, t, font(34, True), (120, 760 + i * 105), anchor="lm", color=WHITE)
    put(d, ck, s, font(30), (120, 803 + i * 105), anchor="lm", color=LIGHT)
put(d, ck, "填志愿前逐项过一遍", font(34, True), (540, 1300), color=GOLD)
put(d, ck, "数据来源：深圳市教育局公开信息", font(22), (540, 1385), color=SUB)
verify(d, ck, "08首图")
img.save(BASE + "08-" + N + "-志愿清单-首图-1080x1440.png")

# ========== 08 正文图：核对清单 ==========
img, d, ck = new_canvas(3)
put(d, ck, "深圳中考 · S1 · 志愿填报", font(22, True), (60, 90), anchor="lm", color=GOLD)
put(d, ck, "志愿填报核对清单 · 4项", font(44, True), (60, 200), anchor="lm")
d.line([60, 250, 200, 250], fill=GOLD, width=3)
c8b = []
list_row(d, ck, 330, "①", "指标生", "只能填1所 · 降分：四大1-5分 / 中等5-15分", c8b)
list_row(d, ck, 490, "②", "走读 / 住宿", "走读最高降35分 · 录取后无法改回住宿", c8b)
list_row(d, ck, 650, "③", "候选方案", "民办哪些低进高出 · 中职3+4/3+2怎么报名", c8b)
list_row(d, ck, 810, "④", "定位基准", "一模成绩出来再定冲稳保 · 现在先搭框架", c8b)
ALL_OK &= gap_report(d, ck, "08正文·清单行", c8b)
put(d, ck, "现在就开始核对，别到时候手忙脚乱", font(34, True), (540, 1030), color=GOLD)
put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(22), (540, 1120), color=SUB)
verify(d, ck, "08正文")
img.save(BASE + "08-" + N + "-志愿清单-正文图-核对清单-1080x1440.png")

print()
print("S1-7 小红书配图 4 张完成。ALL_OK =", ALL_OK)
if not ALL_OK:
    print("⚠️ 存在间隙/间距不足，需检查后重新生成")
