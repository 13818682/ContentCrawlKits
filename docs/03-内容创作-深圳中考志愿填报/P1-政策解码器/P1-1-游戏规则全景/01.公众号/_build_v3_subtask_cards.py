# -*- coding: utf-8 -*-
"""P1-1 子任务 04批次/05时间线/06排队 内容卡 · 630 规则样板铺开（待目检，不覆盖原图）
骨架：标题 → 主结构(批次流程/三步卡/时间线) → 实心金结论；无装饰句。
数据出自 P1-1 主线 md（自招→名额分配→第一批16→二批18→三批6 等）。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
FB = "C:/Windows/Fonts/msyhbd.ttc"; FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
EDGE = (58, 100, 148); NAVY = (18, 30, 55)
G = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/01.公众号/"


def base(w, h):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    dd = np.sqrt(((x - w * 0.15) / (w * 0.5)) ** 2 + ((y - h * 0.15) / (h * 0.5)) ** 2)
    a = a * (1 - 0.22 * np.clip(dd - 0.6, 0, None)[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([w - 300, -120, w + 100, 220], fill=TOP + (30,))
    od.ellipse([-140, h - 180, 150, h + 40], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def put(d, text, xy, fnt, fill, maxw=None, name="", w=900, h=600, anchor="mm"):
    f = fnt
    while maxw and f.size > 12:
        bb = d.textbbox((0, 0), text, font=f, anchor=anchor)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = ImageFont.truetype(FB if f.path.endswith("msyhbd.ttc") else FR, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f, anchor=anchor)
    x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
    x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
    if not (x0 >= -1 and x1 <= w + 1 and y0 >= -1 and y1 <= h + 1):
        print(f"[溢出] {name}: '{text}' 字{f.size} 盒{x0:.0f},{y0:.0f}->{x1:.0f},{y1:.0f}")
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    return f


def rbox(d, im, box, radius=14, fill=None, fill_alpha=0, outline=None, outline_alpha=255, width=2):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    if fill is not None and fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=fill + (fill_alpha,))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


def gold_bar(d, im, y0, text, w=900, h=600, fnt=None, name="bar"):
    rbox(d, im, [70, y0, 830, y0 + 56], radius=16, fill=GOLD, fill_alpha=255)
    put(d, text, (450, y0 + 28), fnt or ImageFont.truetype(FB, 25), NAVY, 700, name, w, h)


# ============ 04 批次顺序卡 900×600 ============
im, d = base(900, 600)
put(d, "录取按五个批次依次进行", (450, 58), ImageFont.truetype(FB, 42), WHITE, 860, "t04", 900, 600)
batches = [
    ("自主招生批", "1 个志愿", "自招资格高中 / 中职"),
    ("名额分配批", "1 个志愿", "指标生 · 1 所公办普高"),
    ("统一招生·第一批", "16 个志愿", "主力批次：普高≤12＋中职≤4"),
    ("统一招生·第二批", "18 个志愿", "本市中职、技校专业"),
    ("统一招生·第三批", "6 个志愿", "外省市中职学校"),
]
y = 168
for i, (nm, cnt, desc) in enumerate(batches):
    cy = y + 26
    rbox(d, im, [70, y, 830, y + 52], radius=12, fill_alpha=10, outline=EDGE, outline_alpha=70, width=2)
    d.ellipse([92, cy - 17, 126, cy + 17], fill=GOLD if i == 2 else EDGE)
    put(d, str(i + 1), (109, cy), ImageFont.truetype(FB, 22), NAVY if i == 2 else WHITE, None, f"no{i}", 900, 600)
    put(d, nm, (150, cy), ImageFont.truetype(FB, 23), WHITE, 330, f"nm{i}", 900, 600, "lm")
    put(d, cnt, (560, cy), ImageFont.truetype(FB, 23), GOLD if i == 2 else LIGHT, 170, f"cnt{i}", 900, 600, "rm")
    put(d, desc, (600, cy), ImageFont.truetype(FR, 16), SUB, 210, f"ds{i}", 900, 600, "lm")
    y += 62
gold_bar(d, im, y + 4, "被前一批录取 → 后面批次全部作废（不退档 · 不转录）", 900, 600,
         ImageFont.truetype(FB, 23), "g04")
im.save(G + "04.子任务-批次顺序卡/P1-1-子任务04-批次顺序卡-规则样板-900x600.png")
print("saved 批次顺序卡")

# ============ 06 排队比喻卡 900×600 ============
im, d = base(900, 600)
put(d, "16 个志愿 · 排队录取", (450, 54), ImageFont.truetype(FB, 44), WHITE, 860, "t06", 900, 600)
put(d, "分数优先 · 依照志愿顺序（1→2→3）", (450, 108), ImageFont.truetype(FB, 26), GOLD, 780, "pr06", 900, 600)
steps = [
    ("①", "分高排前", "全市按分数\n从高到低排队"),
    ("②", "纸条按序", "按你写的志愿顺序\n逐个找有名额的学校"),
    ("③", "有空即录", "第 1 个有空位的学校\n录取，录完即止"),
]
cw, chh, y0 = 252, 178, 168
xcs = [178, 450, 722]
for i, (no, ttl, body) in enumerate(steps):
    x = xcs[i]
    rbox(d, im, [x - cw / 2, y0, x + cw / 2, y0 + chh], radius=14,
         fill_alpha=14, outline=EDGE, outline_alpha=90, width=2)
    put(d, no, (x, y0 + 30), ImageFont.truetype(FB, 22), GOLD, None, f"s{i}no", 900, 600)
    put(d, ttl, (x, y0 + 66), ImageFont.truetype(FB, 26), WHITE, cw - 30, f"s{i}t", 900, 600)
    d.line([(x - 80, y0 + 92), (x + 80, y0 + 92)], fill=(255, 255, 255, 80), width=1)
    l1, l2 = body.split("\n")
    put(d, l1, (x, y0 + 118), ImageFont.truetype(FR, 16), SUB, cw - 30, f"s{i}d1", 900, 600)
    put(d, l2, (x, y0 + 146), ImageFont.truetype(FR, 16), SUB, cw - 30, f"s{i}d2", 900, 600)
gold_bar(d, im, 392, "最优：把最想去的放前面 · 按喜欢程度从高到低排", 900, 600,
         ImageFont.truetype(FB, 25), "g06")
put(d, "同分：先比生地合卷分，再比语数英三科总分", (450, 528),
    ImageFont.truetype(FR, 20), LIGHT, 700, "tie06", 900, 600)
im.save(G + "06.子任务-排队比喻卡/P1-1-子任务06-排队比喻卡-规则样板-900x600.png")
print("saved 排队比喻卡")

# ============ 05 时间线卡 900×700 ============
im, d = base(900, 700)
put(d, "从报名到录取：整整 6 个月", (450, 58), ImageFont.truetype(FB, 42), WHITE, 860, "t05", 900, 700)
nodes = [
    ("3月", "中考报名", "", False),
    ("4月", "体育中考", "现场 36 分 · 选考三项", False),
    ("5月", "实验 + 听说", "理化实验20 · 英语听说25", False),
    ("5月下旬", "志愿填报", "全年最重要 10 天！", True),
    ("6月中旬", "自主招生报名", "一类 / 二类只能选 1 所", False),
    ("6月26-28", "文化课考试", "语数英物化史道 · 2.5 天", False),
    ("7月中旬", "成绩公布", "出分后按分排队", False),
    ("7-8月", "分批录取", "自招→指标→第1/2/3批", False),
    ("8月", "录取结束", "准备高中入学", False),
]
y0 = 124
d.line([(150, y0 - 8), (150, y0 + 8 * 58 + 8)], fill=EDGE, width=3)
for i, (tm, ev, rm, hot) in enumerate(nodes):
    cy = y0 + i * 58
    col = GOLD if hot else EDGE
    d.ellipse([142, cy - 8, 158, cy + 8], fill=col)
    put(d, tm, (96, cy), ImageFont.truetype(FB, 20), GOLD if hot else LIGHT, None, f"t{i}tm", 900, 700, "rm")
    put(d, ev, (182, cy), ImageFont.truetype(FB, 24), GOLD if hot else WHITE, None, f"t{i}ev", 900, 700, "lm")
    if rm:
        evw = ImageFont.truetype(FB, 24).getlength(ev)
        put(d, rm, (182 + evw + 16, cy), ImageFont.truetype(FR, 17), SUB, 560, f"t{i}rm", 900, 700, "lm")
rbox(d, im, [180, 630, 720, 682], radius=16, fill=GOLD, fill_alpha=255)
put(d, "志愿填报那 10 天 · 全年最重要决策窗口", (450, 656),
    ImageFont.truetype(FB, 23), NAVY, 500, "g05", 900, 700)
im.save(G + "05.子任务-时间线卡/P1-1-子任务05-时间线卡-规则样板-900x700.png")
print("saved 时间线卡")
