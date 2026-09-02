# -*- coding: utf-8 -*-
"""P1-2 小红书 8张配图（1080×1440 · 3:4）
产出：
  01.视频/ 首图(大字"藏着3个规则")
  02.图文/ 首图 + 正文图1性价比/2等级制/3隐形战场/4三件事
  03.长文/ 长文1-三规则速览(同首图) + 长文2-把规则落地(同三件事)
沿用 P1-1 _build_images_p1_1_xhs.py 版式：title/卡/行标签+说明lm分栏、verify越界。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
BAND = (17, 38, 66); NAVY = (18, 30, 55)
GRAY = (196, 205, 216)
FD = "C:/Windows/Fonts/"

D = {
    "video": "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/04.小红书/01.视频/",
    "tu": "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/04.小红书/02.图文/",
    "long": "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-2-计分规则拆解/04.小红书/03.长文/",
}
N = "01-P1-2-630背后的3个隐藏规则-小红书"
BASE_OUT = D["tu"]


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 18:
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


def box(d, x, y, w, h, fill=CARD, outline=EDGE, r=24, width=2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)


def new_canvas(variant=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    c_top = np.array((38, 82, 126), np.float32)
    c_mid = np.array((22, 48, 82), np.float32)
    c_bot = np.array((10, 22, 40), np.float32)
    for y in range(H):
        p = y / (H - 1)
        if p < 0.5:
            k = p / 0.5; col = c_top * (1 - k) + c_mid * k
        else:
            k = (p - 0.5) / 0.5; col = c_mid * (1 - k) + c_bot * k
        base[y, :, :] = col
    diag = np.clip((xx / W * 0.35 + yy / H * 0.65), 0, 1)[:, :, None]
    base *= (0.62 + 0.38 * diag)
    spots = [
        ((0.80, 0.14), (150, 200, 240)), ((0.20, 0.20), (120, 180, 235)),
        ((0.74, 0.74), (95, 160, 225)), ((0.28, 0.86), (105, 172, 230)),
    ]
    sx, sy = spots[variant % 4][0]; col = np.array(spots[variant % 4][1], np.float32)
    dist = np.sqrt(((xx - sx * W) / (W * 0.45)) ** 2 + ((yy - sy * H) / (H * 0.45)) ** 2)
    base += col[None, None, :] * (np.exp(-dist * dist) * 0.30)[:, :, None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


def save(img, rel, fn):
    import shutil
    img.save(D[rel] + fn)
    print("已保存:", rel, fn)


ALL = []

# ================= 首图 · 藏着3个规则（视频大字版） =================
def cover(mainsize):
    img, d = new_canvas(0); ck = []
    put(d, ck, "深圳中考 · 政策解码器 · 第2篇", font(28, True), (540, 100), color=GOLD)
    put(d, ck, "630分背后", font(62, True), (540, 242), color=WHITE, maxw=1000)
    put(d, ck, "藏着3个规则", font(mainsize, True), (540, 470), color=GOLD, maxw=1000)
    put(d, ck, "分数会骗人 · 规则不会", font(40, True), (540, 655), color=WHITE, maxw=1000)
    # 3 规则 pill
    labs = ["性价比", "等级制", "隐形战场"]
    pw, pg, ph = 210, 35, 80
    px0 = (W - (3 * pw + 2 * pg)) // 2
    py0 = 830
    for i, lab in enumerate(labs):
        px = px0 + i * (pw + pg)
        box(d, px, py0, pw, ph, fill=BAND, outline=GOLD, r=40, width=2)
        put(d, ck, lab, font(36, True), (px + pw // 2, py0 + ph // 2), color=GOLD, maxw=pw - 10)
    put(d, ck, "不是分不够 · 是不会用分", font(34), (540, 1020), color=LIGHT, maxw=1000)
    d.rounded_rectangle([220, 1130, 860, 1260], radius=60, fill=GOLD)
    put(d, ck, "收藏这张 · 备考慢慢对照", font(40, True), (540, 1195), color=NAVY)
    put(d, ck, "同分PK · 决胜生地 · 等级门槛别踩", font(30, True), (540, 1385), color=GOLD, maxw=1000)
    ALL.append(verify(d, ck, "首图"))
    return img


img = cover(112)
save(img, "video", N + "-首图-1080x1440.png")
img2 = cover(96)
save(img2, "tu", N + "-首图-1080x1440.png")

# ================= 正文图1 · 性价比 =================
img, d = new_canvas(1); ck = []
put(d, ck, "规则一 · 性价比", font(34, True), (540, 100), color=GOLD)
put(d, ck, "同样的时间 · 花在哪最划算", font(50, True), (540, 215), color=WHITE, maxw=1020)
rows1 = [
    ("440分", "语数英物化 · 主战场 · 全力投入", GOLD),
    ("20分", "理化实验涨到20 · 8分增量=性价比王", GOLD),
    ("170分", "历史道法体育 · 稳定发挥即可", WHITE),
]
y0, rh, rg = 330, 180, 30
for i, (t, s, tc) in enumerate(rows1):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=24)
    cy = y + rh // 2
    put(d, ck, t, font(56, True), (230, cy), color=tc, maxw=300)
    put(d, ck, s, font(35), (470, cy), anchor="lm", color=WHITE, maxw=520)
put(d, ck, "实验那8分 = 性价比之王 · 认真练就白送，刷题拿不到", font(32, True), (540, 1240), color=GOLD, maxw=1020)
put(d, ck, "别在副科题海苦熬 · 主科和实验涨分更快", font(30), (540, 1340), color=WHITE, maxw=1020)
ALL.append(verify(d, ck, "正文图1性价比"))
save(img, "tu", N + "-正文图1-性价比-1080x1440.png")

# ================= 正文图2 · 等级制 =================
img, d = new_canvas(2); ck = []
put(d, ck, "规则二 · 等级制", font(34, True), (540, 100), color=GOLD)
put(d, ck, "看等级 · 别只看分数", font(50, True), (540, 215), color=WHITE, maxw=1020)
rows2 = [
    ("A+", "前 5% · 单科顶尖", False),
    ("A", "前 5%-25% · 录取线稳定盘", False),
    ("B+", "前 25%-50% · 中等竞争区", False),
    ("B", "前 50%-75%", False),
    ("C+", "前 75%-95% · 省一级报考门槛！", True),
]
y0, rh, rg = 320, 132, 22
for i, (t, s, hot) in enumerate(rows2):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=22, outline=(255, 255, 255) if hot else EDGE, width=3 if hot else 2)
    cy = y + rh // 2
    col = GOLD if hot else WHITE
    put(d, ck, t, font(46, True), (240, cy), color=col, maxw=200)
    put(d, ck, s, font(33), (430, cy), anchor="lm", color=GOLD if hot else WHITE, maxw=600)
box(d, 60, 1100, 960, 150, r=24)
put(d, ck, "报省一级：全科 C+ 及以上 · 体育 C 即可", font(34, True), (540, 1150), color=GOLD, maxw=920)
put(d, ck, "任何一科掉到 C · 报名资格都没有", font(30), (540, 1215), color=LIGHT, maxw=920)
put(d, ck, "早发现 · 早补 · 别拖到初三", font(32, True), (540, 1340), color=WHITE, maxw=1020)
ALL.append(verify(d, ck, "正文图2等级制"))
save(img, "tu", N + "-正文图2-等级制-1080x1440.png")

# ================= 正文图3 · 隐形战场 552 PK =================
img, d = new_canvas(3); ck = []
put(d, ck, "规则三 · 隐形战场", font(34, True), (540, 100), color=GOLD)
put(d, ck, "同分PK · 生地定胜负", font(50, True), (540, 215), color=WHITE, maxw=1020)
box(d, 60, 340, 460, 340, r=26)
put(d, ck, "考生A", font(32, True), (290, 425), color=WHITE, maxw=400)
put(d, ck, "96", font(92, True), (290, 550), color=GOLD, maxw=420)
put(d, ck, "生地 · 总分552 → 被录取", font(28), (290, 660), color=WHITE, maxw=430)
box(d, 560, 340, 460, 340, r=26, outline=(90, 110, 140))
put(d, ck, "考生B", font(32, True), (790, 425), color=GRAY, maxw=400)
put(d, ck, "82", font(92, True), (790, 550), color=GRAY, maxw=420)
put(d, ck, "生地 · 总分552 → 落选", font(28), (790, 660), color=GRAY, maxw=430)
box(d, 60, 760, 960, 140, r=24)
put(d, ck, "同分先比生地 → 96 > 82", font(38, True), (540, 830), color=GOLD, maxw=920)
box(d, 60, 930, 960, 140, r=24)
put(d, ck, "信息科技 · 艺术须合格 → 才能报省一级", font(33, True), (540, 1000), color=WHITE, maxw=920)
d.rounded_rectangle([60, 1100, 1020, 1240], radius=60, fill=GOLD)
put(d, ck, "14分 = 一个高中学位", font(46, True), (540, 1170), color=NAVY)
put(d, ck, "生地是底牌 · 别让小科翻车", font(30, True), (540, 1370), color=GOLD, maxw=1020)
ALL.append(verify(d, ck, "正文图3隐形战场"))
save(img, "tu", N + "-正文图3-隐形战场-1080x1440.png")

# ================= 正文图4 · 三件事 =================
img, d = new_canvas(0); ck = []
put(d, ck, "现在能做的三件事", font(44, True), (540, 100), color=GOLD)
put(d, ck, "出分前就能做 · 做了改变结果", font(40, True), (540, 215), color=WHITE, maxw=1020)
acts = [
    ("① 看性价比分配精力", "主战场优先 · 别让副科挤占主科时间"),
    ("② 用等级定位孩子", "哪科在 C 边缘 · 就是门槛隐患"),
    ("③ 确认两个隐形门槛", "生地分数有数 · 信技艺术确认合格"),
]
y0, rh, rg = 350, 210, 55
for i, (t, s) in enumerate(acts):
    y = y0 + i * (rh + rg)
    box(d, 60, y, 960, rh, r=26)
    put(d, ck, t, font(40, True), (170, y + 70), anchor="lm", color=WHITE, maxw=820)
    put(d, ck, s, font(33), (170, y + 150), anchor="lm", color=GOLD, maxw=820)
put(d, ck, "3条落地 · 630分才没白考", font(34, True), (540, 1370), color=GOLD, maxw=1020)
ALL.append(verify(d, ck, "正文图4三件事"))
save(img, "tu", N + "-正文图4-三件事-1080x1440.png")

# ================= 长文图 =================
import shutil
long_names = {
    N + "-长文1-三规则速览-1080x1440.png": N + "-首图-1080x1440.png",   # 复用图文首图
    N + "-长文2-把规则落地-1080x1440.png": N + "-正文图4-三件事-1080x1440.png",  # 复用三件事
}
for dst, src in long_names.items():
    shutil.copyfile(D["tu"] + src, D["long"] + dst)
    print("长文图:", dst, "(复制自", src + ")")

print()
print("全部 OK =", all(ALL))
