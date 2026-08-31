# -*- coding: utf-8 -*-
"""S1-7 小红书配图 2 张补充（延续 13-3 规范：深蓝渐变+金色数据+微软雅黑）：
  A. 07 首图（大字版）→ 「07-1 首图」：在原图上叠加醒目大字标题，主标题 104px，
     首页缩略图一眼可读；保留下方数据卡与阶段列表。
  B. 首页广告 → 「09-1 首页广告」：独立获客广告图（大钩子 + 4 阶段时间线 + 关注 CTA）。
  数字编号规则：{小红书笔记序号}-{笔记内图片顺序}-…，首图=1，正文图=2，上传按序。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66)          # 大字标题条底色
NAVY = (18, 30, 55)          # 金色按钮文字
FD = "C:/Windows/Fonts/"


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    """写文字，可选最大宽度自动缩字号（下限 22），并记录坐标供越界校验。"""
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
    return fnt


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
    return bad == 0


def new_canvas(variant=0):
    """与 _build_xhs_s1_7.py 相同的深蓝渐变画布。"""
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


BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/S1-基本态势/S1-7-备考时间线/03-小红书/"
N = "S1-7-2027年中考家长备考时间线：从今天起每个月要做什么-小红书"

# ================= A. 07-1 首图（大字版，主标题 104px） =================
# 源：原 07 首图（已另存为 07-0 旧版），在其上覆盖大字标题横幅
src = BASE + "07-0-" + N + "-备考时间线-首图-旧版-1080x1440.png"
img = Image.open(src).convert("RGB")
d = ImageDraw.Draw(img)
ck = []

bx, by, bw, bh = 40, 40, 1000, 380
d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26, fill=BAND, outline=GOLD, width=3)

# 金色小标签（带主题定位）
put(d, ck, "深圳中考 · 备考时间线", font(28, True), (540, by + 54), color=GOLD)
# 冲击力大字主标题（104px）：2027中考 / 仅剩300天（300天 金色高亮）
put(d, ck, "2027中考", font(104, True), (540, by + 164), color=WHITE, maxw=940)
f_big = font(104, True)
w_pre = int(d.textlength("仅剩", font=f_big))
w_gold = int(d.textlength("300天", font=f_big))
tot = w_pre + w_gold
x1 = 540 - tot / 2 + w_pre / 2
x2 = 540 - tot / 2 + w_pre + w_gold / 2
put(d, ck, "仅剩", f_big, (x1, by + 288), color=WHITE)
put(d, ck, "300天", f_big, (x2, by + 288), color=GOLD)
# 金色点缀线
d.line([540 - 90, by + 352, 540 + 90, by + 352], fill=GOLD, width=4)

ok_a = verify(d, ck, "A 07-1 首图")
out_a = BASE + "07-1-" + N + "-备考时间线-首图-1080x1440.png"
img.save(out_a)
print("A 已保存:", out_a.split("/")[-1])

# ================= B. 09-1 首页广告 =================
img, d, ck = new_canvas(0)
put(d, ck, "深圳中考 · 备考指南", font(30, True), (540, 116), color=GOLD)
put(d, ck, "距2027年中考", font(104, True), (540, 262), color=WHITE, maxw=1000)

f100 = font(104, True)
w_left = int(d.textlength("还剩", font=f100))
w_gold = int(d.textlength("300天", font=f100))
tot = w_left + w_gold
x1 = 540 - tot / 2 + w_left / 2
x2 = 540 - tot / 2 + w_left + w_gold / 2
put(d, ck, "还剩", f100, (x1, 390), color=WHITE)
put(d, ck, "300天", f100, (x2, 390), color=GOLD)
d.line([540 - 110, 500, 540 + 110, 500], fill=GOLD, width=4)

put(d, ck, "从现在起，每个月该做什么？", font(40), (540, 585), color=LIGHT)

stages = [("① 现在", "2026.8"), ("② 1-3月", "一模定位"), ("③ 4-5月", "志愿填报"), ("④ 6-7月", "中考录取")]
cw, ch, cgap = 215, 112, 26
cx0 = (W - (4 * cw + 3 * cgap)) // 2
cy0 = 680
for i, (t, s) in enumerate(stages):
    cx = cx0 + i * (cw + cgap)
    d.rounded_rectangle([cx, cy0, cx + cw, cy0 + ch], radius=20, fill=CARD, outline=EDGE, width=2)
    put(d, ck, t, font(32, True), (cx + cw // 2, cy0 + 38), color=WHITE)
    put(d, ck, s, font(26), (cx + cw // 2, cy0 + 82), color=GOLD)

d.rounded_rectangle([60, 850, 1020, 1010], radius=22, fill=CARD, outline=EDGE, width=2)
put(d, ck, "收藏这份时间线 · 每月对照执行", font(36, True), (540, 904), color=WHITE)
put(d, ck, "4个阶段 · 10天志愿填报窗口 · 先填志愿后考试", font(28), (540, 958), color=LIGHT)

d.rounded_rectangle([260, 1070, 820, 1190], radius=60, fill=GOLD)
put(d, ck, "关注我们 · 每月同步更新", font(40, True), (540, 1130), color=NAVY)

put(d, ck, "数据来源：深圳市教育局公开信息 · 逐条人工核对", font(24), (540, 1280), color=SUB)

ok_b = verify(d, ck, "B 09-1 首页广告")
out_b = BASE + "09-1-" + N + "-首页广告-1080x1440.png"
img.save(out_b)
print("B 已保存:", out_b.split("/")[-1])

print()
print("A OK =", ok_a, "| B OK =", ok_b)
