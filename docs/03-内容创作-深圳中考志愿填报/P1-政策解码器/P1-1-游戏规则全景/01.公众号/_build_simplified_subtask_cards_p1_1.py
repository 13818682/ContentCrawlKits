# -*- coding: utf-8 -*-
"""P1-1 公众号子任务 5 卡「化繁为简」重制（内容卡 900×600 / 900×700）
规则：去顶部徽章胶囊、去装饰性底部金句；标题加大上移、数据主体下移留白更透气；
一卡一主题，只留功能性信息。输出文件名带「化繁为简-」，与原图并存。
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)

G = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/01.公众号/"


def base(w, h):
    T = np.array(TOP, float); B = np.array(BOT, float)
    t = np.linspace(0, 1, h)[:, None, None]
    a = T[None, None, :] * (1 - t) + B[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - w * 0.15) / (w * 0.5)) ** 2 + ((y - h * 0.15) / (h * 0.5)) ** 2)
    a = a * (1 - 0.22 * np.clip(d - 0.6, 0, None)[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([w - 300, -120, w + 100, 220], fill=TOP + (30,))
    od.ellipse([-140, h - 180, 150, h + 40], fill=TOP + (18,))
    im.paste(ov, (0, 0), ov)
    return im, ImageDraw.Draw(im)


def T(d, xy, text, font, fill, anchor="mm", name="", W=900, H=600, pad=4):
    bb = d.textbbox((0, 0), text, font=font)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    cx, cy = xy
    if anchor == "mm":
        x0, y0 = cx - bw / 2, cy - bh / 2
    elif anchor == "lm":
        x0, y0 = cx, cy - bh / 2
    else:
        x0, y0 = cx, cy
    if x0 < pad or x0 + bw > W - pad or y0 < pad or y0 + bh > H - pad:
        print(f"[溢出] {name}: '{text}' x0={x0:.0f}->{x0+bw:.0f} y0={y0:.0f}->{y0+bh:.0f}")
    d.text(xy, text, font=font, fill=fill, anchor=anchor)
    return (x0, y0, x0 + bw, y0 + bh)


def card(d, box, fill_alpha=0, outline=None, outline_alpha=255, radius=16, width=2):
    im = d._image
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    if fill_alpha:
        od.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, fill_alpha))
    if outline:
        od.rounded_rectangle(box, radius=radius, outline=outline + (outline_alpha,), width=width)
    im.paste(ov, (0, 0), ov)


# ================= 卡02 · 630构成（900×600） =================
img, d = base(900, 600)
T(d, (450, 84), "深圳中考 630 分，怎么构成的？", ImageFont.truetype(FB, 44), WHITE, "mm", "title", 900, 600)
card(d, [56, 150, 844, 256], fill_alpha=20, outline=EDGE, outline_alpha=120, radius=16)
f_num = ImageFont.truetype(FB, 30); f_grp = ImageFont.truetype(FR, 20)
T(d, (262, 178), "主战场 440 分 · 占 70%", f_num, GOLD, "mm", "ov-440", 900, 600)
T(d, (262, 228), "语数英物化 · 五科定胜负", f_grp, LIGHT, "mm", "ov-440-sub", 900, 600)
T(d, (638, 178), "170 分 · 另三科", f_num, WHITE, "mm", "ov-170", 900, 600)
T(d, (638, 228), "史道体 · 中等分段定公办民办", f_grp, LIGHT, "mm", "ov-170-sub", 900, 600)
d.line([(470, 160), (470, 246)], fill=EDGE, width=2)
subjects = [
    ("语文", "120", "单科最高·作文为主"), ("数学", "100", "区分度最大"),
    ("英语", "100", "笔试75+听说25"), ("物理+化学", "140", "2026实验20"),
    ("历史", "70", "记背为主"), ("道德与法治", "50", "2026起开卷"),
    ("体育", "50", "过程14+现场36"),
]
f_sub = ImageFont.truetype(FB, 22); f_score = ImageFont.truetype(FB, 26); f_note = ImageFont.truetype(FR, 16)
col_cx = [260, 640]; cw, ch, row_h = 340, 44, 58
y0 = 330
for i, (name, score, note) in enumerate(subjects):
    col = i // 4; row = i % 4
    x = col_cx[col]; cy = y0 + row * row_h
    card(d, [x - cw / 2, cy - ch / 2, x + cw / 2, cy + ch / 2], fill_alpha=10, outline=EDGE, outline_alpha=70, radius=10)
    T(d, (x - cw / 2 + 24, cy), name, f_sub, WHITE, "lm", f"row{i}", 900, 600)
    name_w = d.textlength(name, font=f_sub)
    T(d, (x - cw / 2 + 24 + name_w + 20, cy), note, f_note, SUB, "lm", f"row{i}n", 900, 600)
    T(d, (x + cw / 2 - 26, cy), score, f_score, GOLD, "rm", f"row{i}s", 900, 600)
cy4 = y0 + 3 * row_h; x4 = col_cx[1]
card(d, [x4 - cw / 2, cy4 - ch / 2, x4 + cw / 2, cy4 + ch / 2], fill_alpha=28, outline=GOLD, outline_alpha=150, radius=10)
f4 = ImageFont.truetype(FB, 26); f4n = ImageFont.truetype(FR, 18)
T(d, (x4 - cw / 2 + 24, cy4), "五科合计 440", f4, GOLD, "lm", "row7-h", 900, 600)
T(d, (x4 + cw / 2 - 24, cy4), "占70%", f4n, LIGHT, "rm", "row7-n", 900, 600)
img.save(G + "02.子任务-630构成卡/化繁为简-P1-1-子任务02-630构成卡-900x600.png")
print("OK 630构成卡")

# ================= 卡03 · ACD对比（900×600） =================
img, d = base(900, 600)
T(d, (450, 84), "考生分 ACD 三类，站哪条赛道？", ImageFont.truetype(FB, 44), WHITE, "mm", "title", 900, 600)
cats = [
    ("A类", "深户+学籍同区", "所有学校都能报", GOLD),
    ("C类", "深户+学籍跨区", "部分学校有限制", WHITE),
    ("D类", "非深户", "公办指标仅约23%", LIGHT),
]
f_cat = ImageFont.truetype(FB, 34); f_cond = ImageFont.truetype(FR, 20); f_key = ImageFont.truetype(FB, 21)
cw, ch3 = 246, 128
y3 = 168
x0s = [68, 336, 604]
for i, (cat, cond, key, col) in enumerate(cats):
    x = x0s[i] + cw / 2
    card(d, [x - cw / 2, y3, x + cw / 2, y3 + ch3], fill_alpha=16, outline=EDGE, outline_alpha=90, radius=14)
    T(d, (x, y3 + 36), cat, f_cat, col, "mm", f"cat{i}", 900, 600)
    T(d, (x, y3 + 68), cond, f_cond, WHITE, "mm", f"cat{i}c", 900, 600)
    d.line([(x - 60, y3 + 84), (x + 60, y3 + 84)], fill=(255, 255, 255, 90), width=1)
    T(d, (x, y3 + 102), key, f_key, col, "mm", f"cat{i}k", 900, 600)
T(d, (450, 358), "D 类家长 · 先记住这三条", ImageFont.truetype(FB, 26), GOLD, "mm", "d-title", 900, 600)
d_lines = [
    ("① 占比", "非深户考生过半，公办普高指标 D 类仅约 23%"),
    ("② 差距", "四大名校 ACD 持平，中下层次 D 类高 5-15 分"),
    ("③ 通道", "指标生已覆盖 D 类 —— 最重要的降分通道"),
]
f_k = ImageFont.truetype(FB, 20); f_v = ImageFont.truetype(FR, 18)
yD = 394
for i, (k, v) in enumerate(d_lines):
    ry = yD + i * 58
    card(d, [70, ry, 830, ry + 44], fill_alpha=10, outline=EDGE, outline_alpha=70, radius=10)
    T(d, (100, ry + 22), k, f_k, GOLD, "lm", f"d{i}k", 900, 600)
    T(d, (210, ry + 22), v, f_v, WHITE, "lm", f"d{i}v", 900, 600)
img.save(G + "03.子任务-ACD对比卡/化繁为简-P1-1-子任务03-ACD对比卡-900x600.png")
print("OK ACD对比卡")

# ================= 卡04 · 批次顺序（900×600） =================
img, d = base(900, 600)
T(d, (450, 84), "录取分五个批次 · 前一批录了全作废", ImageFont.truetype(FB, 40), WHITE, "mm", "title", 900, 600)
batches = [
    ("第1批", "自主招生批", "1个志愿", "自招资格高中/中职", WHITE),
    ("第2批", "名额分配批", "1个志愿", "1所公办普高（指标生）", WHITE),
    ("第3批", "统一招生第一批", "16个志愿", "普高≤12 + 中职≤4", GOLD),
    ("第4批", "统一招生第二批", "18个志愿", "本市中职、技校专业", WHITE),
    ("第5批", "统一招生第三批", "6个志愿", "外省市中职学校", WHITE),
]
f_no = ImageFont.truetype(FB, 20); f_name = ImageFont.truetype(FB, 22)
f_cnt = ImageFont.truetype(FB, 20); f_desc = ImageFont.truetype(FR, 16)
ch, row_h = 52, 66
y0 = 176
for i, (no, name, cnt, desc, col) in enumerate(batches):
    cy = y0 + i * row_h
    d.ellipse([78, cy - 18, 118, cy + 18], fill=GOLD if col == GOLD else EDGE)
    T(d, (98, cy), str(i + 1), f_no, (13, 30, 48) if col == GOLD else WHITE, "mm", f"b{i}n", 900, 600)
    T(d, (150, cy), name, f_name, col, "lm", f"b{i}m", 900, 600)
    cb = d.textbbox((0, 0), cnt, font=f_cnt); cpad = 12
    ccx = 570; cx0 = ccx - (cb[2] + cpad * 2) / 2; cx1 = ccx + (cb[2] + cpad * 2) / 2
    d.rounded_rectangle([cx0, cy - 15, cx1, cy + 15], radius=15, outline=col, width=2)
    T(d, (ccx, cy), cnt, f_cnt, col, "mm", f"b{i}c", 900, 600)
    T(d, (660, cy), desc, f_desc, SUB, "lm", f"b{i}d", 900, 600)
card(d, [70, 522, 830, 566], fill_alpha=18, outline=GOLD, outline_alpha=140, radius=12)
T(d, (450, 544), "别填「录了也不想去」的学校", ImageFont.truetype(FB, 22), GOLD, "mm", "warn", 900, 600)
img.save(G + "04.子任务-批次顺序卡/化繁为简-P1-1-子任务04-批次顺序卡-900x600.png")
print("OK 批次顺序卡")

# ================= 卡05 · 时间线（900×700） =================
img, d = base(900, 700)
T(d, (450, 86), "从报名到录取：整整 6 个月", ImageFont.truetype(FB, 42), WHITE, "mm", "title", 900, 700)
nodes = [
    ("3月", "中考报名", "D类5项材料提前备齐", False),
    ("4月", "体育中考", "36分现场 · 选考三项", False),
    ("5月", "实验+听说", "理化实验20分 · 英语听说25分", False),
    ("5月下旬", "志愿填报", "全年最重要10天！", True),
    ("6月中旬", "自主招生报名", "一类/二类只能选1所", False),
    ("6月26-28", "文化课考试", "语数英物化史道 · 2.5天", False),
    ("7月16日", "成绩公布", "含单科等级 A+/A/B+...", False),
    ("7-8月", "分批录取", "自招→指标→第1/2/3批", False),
    ("8月", "录取结束", "准备高中入学", False),
]
f_time = ImageFont.truetype(FB, 20); f_ev = ImageFont.truetype(FB, 22); f_rm = ImageFont.truetype(FR, 18)
ch, row_h = 44, 58
y0 = 140
d.line([(150, y0 - 10), (150, y0 + 8 * row_h + 12)], fill=EDGE, width=3)
for i, (tm, ev, rm, hot) in enumerate(nodes):
    cy = y0 + i * row_h
    col = GOLD if hot else EDGE
    d.ellipse([142, cy - 8, 158, cy + 8], fill=col)
    col_t = GOLD if hot else LIGHT
    T(d, (98, cy), tm, f_time, col_t, "rm", f"t{i}tm", 900, 700)
    col_e = GOLD if hot else WHITE
    T(d, (182, cy), ev, f_ev, col_e, "lm", f"t{i}ev", 900, 700)
    ev_w = d.textlength(ev, font=f_ev)
    T(d, (182 + ev_w + 18, cy), rm, f_rm, SUB, "lm", f"t{i}rm", 900, 700)
card(d, [180, 648, 720, 684], fill_alpha=16, outline=GOLD, outline_alpha=120, radius=14)
T(d, (450, 666), "志愿填报那10天 · 全年最重要决策窗口", ImageFont.truetype(FB, 22), GOLD, "mm", "warn", 900, 700)
img.save(G + "05.子任务-时间线卡/化繁为简-P1-1-子任务05-时间线卡-900x700.png")
print("OK 时间线卡")

# ================= 卡06 · 排队比喻（900×600） =================
img, d = base(900, 600)
T(d, (450, 84), "16个志愿怎么录 · 排队录取", ImageFont.truetype(FB, 42), WHITE, "mm", "title", 900, 600)
T(d, (450, 142), "分数优先 · 依照志愿顺序", ImageFont.truetype(FB, 26), GOLD, "mm", "metaphor", 900, 600)
steps = [
    ("第一步", "分高排前", "全市按分数从高到低排队，轮到谁处理谁"),
    ("第二步", "纸条按序", "按你写的志愿顺序，逐个检索有名额的学校"),
    ("第三步", "按号安排", "第一个有名额的学校录取，不能跳号去后面窗口"),
]
f_sno = ImageFont.truetype(FB, 20); f_stitle = ImageFont.truetype(FB, 26); f_sdesc = ImageFont.truetype(FR, 16)
scw, sch, sgap = 252, 156, 24
sy = 224
sx0s = [60, 324, 588]
for i, (sno, stitle, sdesc) in enumerate(steps):
    sx = sx0s[i] + scw / 2
    card(d, [sx - scw / 2, sy, sx + scw / 2, sy + sch], fill_alpha=14, outline=EDGE, outline_alpha=90, radius=14)
    T(d, (sx, sy + 30), sno, f_sno, SUB, "mm", f"s{i}n", 900, 600)
    T(d, (sx, sy + 64), stitle, f_stitle, GOLD, "mm", f"s{i}t", 900, 600)
    d.line([(sx - 70, sy + 86), (sx + 70, sy + 86)], fill=(255, 255, 255, 90), width=1)
    f_l = ImageFont.truetype(FR, 16)
    mid = len(sdesc) // 2
    cut = mid
    for probe in range(mid, -1, -1):
        if sdesc[probe] in " ，。、；":
            cut = probe + 1; break
    if cut <= 2 or cut >= len(sdesc) - 2:
        cut = mid
    T(d, (sx, sy + 108), sdesc[:cut], f_l, SUB, "mm", f"s{i}d1", 900, 600)
    T(d, (sx, sy + 134), sdesc[cut:], f_l, SUB, "mm", f"s{i}d2", 900, 600)
card(d, [80, 424, 820, 472], fill_alpha=18, outline=GOLD, outline_alpha=150, radius=12)
T(d, (450, 448), "最想去的放前面 · 按喜欢程度从高到低排", ImageFont.truetype(FB, 24), GOLD, "mm", "do", 900, 600)
T(d, (450, 520), "同分怎么办：先比生地合卷分，再比语数英三科总分", ImageFont.truetype(FR, 20), LIGHT, "mm", "tie", 900, 600)
img.save(G + "06.子任务-排队比喻卡/化繁为简-P1-1-子任务06-排队比喻卡-900x600.png")
print("OK 排队比喻卡")
print("全部生成")
