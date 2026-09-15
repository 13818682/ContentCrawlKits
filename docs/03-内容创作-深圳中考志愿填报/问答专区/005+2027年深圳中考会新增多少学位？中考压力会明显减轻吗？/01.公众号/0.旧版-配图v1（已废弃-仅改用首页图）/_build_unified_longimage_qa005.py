# -*- coding: utf-8 -*-
"""QA-005 公众号极简版 · 大字封面 + 统一长图（13-1 规范：900宽连续渐变）
- 极简封面：关键数字为视觉主角（88px 金色）+ CTA胶囊自底部定位（底边 = H-24，留白≥20px）
- 长图：正文 ≤17px（渲染 ×2.4），自上而下累加 y 布局；越界+重叠+渐变单调三检 + 自动裁剪尾部
内容镜像《005+...-公众号-终版-精简.md》：三件事 → 节奏 → 新建 → 扩建 → 两个五年 → 何时轮到 → 三句话
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = 900
TOP = (27, 58, 92); BOT = (13, 30, 48)
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
CARD = (31, 66, 106); EDGE = (58, 100, 148)
FD = "C:/Windows/Fonts/"

OUT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/"
       "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？/01.公众号/")


def font(size, bold=False):
    if size <= 17:
        size = int(round(size * 2.4))   # 正文 ×2.4
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def grad(w, h):
    """单条连续渐变（禁止拼接）；返回 (img, draw)"""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c1 = np.array(TOP, dtype=np.float32); c2 = np.array(BOT, dtype=np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    arr = arr.repeat(w, axis=1)
    y, x = np.mgrid[0:h, 0:w]
    g = np.exp(-(((x - w * 0.5) / (w * 0.32)) ** 2 + ((y - h * 0.14) / (h * 0.34)) ** 2))
    arr = arr + np.array((185, 208, 235), dtype=np.float32)[None, None, :] * (g * 0.11)[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([-w * .18, -h * .08, w * .24, h * .16], fill=TOP + (34,))
    od.ellipse([w * .80, h * .82, w * 1.1, h * 1.04], fill=TOP + (20,))
    img.paste(ov, (0, 0), ov)
    return img, ImageDraw.Draw(img)


# ═══════════════ 极简大字封面 900×383 ═══════════════
def build_cover():
    w, h = 900, 383
    img, d = grad(w, h)

    def ctext(text, size, xy, color, bold=True, maxw=820):
        f = ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)
        while size > 12:
            bb = d.textbbox((0, 0), text, font=f, anchor="mm")
            if bb[2] - bb[0] <= maxw + 1:
                break
            size -= 1
            f = ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)
        d.text(xy, text, font=f, fill=color, anchor="mm")
        bb = d.textbbox(xy, text, font=f, anchor="mm")
        assert bb[0] >= 0 and bb[2] <= w and bb[1] >= 0 and bb[3] <= h, f"cover越界 {text} {bb}"
        return bb

    ctext("深圳中考 · 问答005", 24, (450, 44), GOLD)
    ctext("未来五年，深圳要为孩子多盖一批高中", 26, (450, 94), WHITE, maxw=800)
    ctext("10万个以上", 88, (450, 202), GOLD, maxw=820)
    ctext("规划新增公办高中学位 · 2026—2030", 20, (450, 272), LIGHT, False, maxw=820)

    # CTA 胶囊：自底部定位，底边 = H-24（底部留白 24px ≥ 20px）
    ch = 46
    cy1 = h - 24
    cy0 = cy1 - ch
    d.rounded_rectangle([450 - 235, cy0, 450 + 235, cy1], radius=ch // 2,
                        outline=GOLD, width=3, fill=(31, 66, 106))
    ctext("关注 · 深圳中考系列持续更新", 20, (450, (cy0 + cy1) // 2), GOLD)
    assert cy1 <= h - 20, "封面底部留白不足"

    out = OUT + "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？-公众号-封面-极简版.png"
    img.save(out)
    print("saved", out.split("/")[-1], img.size)
    return img


# ═══════════════ 统一长图 ═══════════════
H = 9000
img, d = grad(W, H)
checks = []


def put(text, fnt, xy, anchor="mm", color=WHITE, maxw=None):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 8:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            bw = bb[2] - bb[0]
            x0, x1 = bb[0] + xy[0], bb[2] + xy[0]
            if bw <= maxw + 1 and x0 >= -1 and x1 <= W + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    checks.append((text, fnt, xy, anchor, color, maxw))


def box(x, y, w, h, fill=CARD, outline=EDGE, r=18):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=3)


def chapter(ty, txt, l1="", l2=""):
    d.rectangle([50, ty - 36, 60, ty + 36], fill=GOLD)
    if l1:
        put(l1, font(52, True), (80, ty - 28), anchor="lm", color=WHITE)
        put(l2, font(30, True), (80, ty + 28), anchor="lm", color=LIGHT)
    else:
        put(txt, font(52, True), (80, ty), anchor="lm", color=WHITE, maxw=W - 100)
    d.line([50, ty + 58, 160, ty + 58], fill=GOLD, width=3)


def row(ry, tag, detail, tagcolor=GOLD, hbox=130):
    box(40, ry, W - 80, hbox)
    put(tag, font(32, True), (76, ry + 40), anchor="lm", color=tagcolor)
    put(detail, font(16), (76, ry + 88), anchor="lm", color=WHITE, maxw=720)
    return ry + hbox + 15


def mea(ry, txt):
    """『这意味着什么』金色横贯段"""
    put(txt, font(17, True), (W / 2, ry), color=GOLD, maxw=W - 110)
    return ry + 82


y = 0
# ---------- 页眉 ----------
y += 42
put("深圳中考 · 问答系列 · 第5篇", font(18, True), (50, y), anchor="lm", color=GOLD)
y += 56
put("未来五年，深圳要为孩子多盖一批高中", font(38, True), (50, y), anchor="lm", color=WHITE, maxw=800)
y += 60
put("新建10所 · 改扩建10余所 · 规划新增学位10万个以上", font(16), (50, y), anchor="lm", color=LIGHT, maxw=800)
y += 48
d.line([50, y, 160, y], fill=GOLD, width=3)

# ---------- 01 三件事 ----------
y += 82
chapter(y, "01 · 未来五年，深圳要做三件事")
y += 100
y = row(y, "① 新建一批高中", "第三十九高级中学至第四十八高级中学 · 10所新建公办高中的番号已排定", GOLD)
y = row(y, "② 让老学校长大", "超过10所公办高中正在改扩建 · 三大高中园首次进入改扩建程序", GOLD)
y = row(y, "③ 学位总量再抬一台阶", "“十五五”（2026—2030）规划新增公办高中学位10万个以上", GOLD)
y += 36
y = mea(y, "口径提醒：「10万个以上」是十五五五年的全口径规划目标，涵盖所有新改扩建项目——它不是上面这10所新校的学位数。项目数量 ≠ 学位总量。")

# ---------- 02 节奏 ----------
chapter(y, "02 · 这不是新闻，是节奏")
y += 100
for tag, detail in [
    ("3 月", "第三十九、第四十高级中学启动社会稳定风险评估——“十五五”第一批新改扩建公办高中项目"),
    ("7 月", "第四十一高级中学项目设计招标启动（计划总投资63,609万元）"),
    ("9 月 1 日", "坪山、光明、深汕三大高中园改扩建进入可研招标——三大高中园首次进入改扩建程序"),
    ("9 月 8 日", "第四十二至第四十八高级中学 + 深大附中高中部扩建，8个项目前期合同一起公示"),
]:
    y = row(y, tag, detail, LIGHT)
y += 36
y = mea(y, "单看每一条，都是普通政务公告。连起来看，它是一条节奏——关于深圳未来要给孩子们准备多少高中学位的节奏。")

# ---------- 03 新建 ----------
chapter(y, "03 · 新建：10所，正从图纸上站起来")
y += 100
box(40, y, W - 80, 470, r=18)
yy = y + 72
put("新建10所公办高中 · 三十九高—四十八高", font(26, True), (W / 2, yy), color=GOLD)
yy += 96
for nm, loc, scale in [
    ("39高", "南山", "48班 / 2400学位（含50%走读）"),
    ("40高", "坪山", "36班 / 1800学位（含30%走读）"),
    ("45高", "宝安", "4800学位"),
    ("46高", "光明", "1800学位"),
]:
    put(f"{nm} · {loc}", font(24, True), (76, yy), anchor="lm", color=WHITE)
    put(scale, font(22, True), (830, yy), anchor="rm", color=GOLD, maxw=430)
    yy += 62
put("41/42/43/44/47/48高 · 选址与规模官方尚未公布", font(17), (76, yy + 12), anchor="lm", color=LIGHT, maxw=740)
y += 470
y += 40
y = mea(y, "走读名额是这次的一个信号：一所学校不再只有“住校”一种可能——对家门口就有高中的家庭，是实实在在的便利。")

# ---------- 04 扩建 ----------
chapter(y, "04 · 扩建：老学校也在悄悄长大")
y += 100
box(40, y, W - 80, 360, r=18)
put("深中泥岗 · 深实验 · 深高中心校区（南） · 宝中集团", font(22, True), (W / 2, y + 66), color=WHITE, maxw=780)
put("深大附中 · 深二实 · 翠园本部 · 罗湖高中 · 平冈 · 深二外", font(22, True), (W / 2, y + 122), color=WHITE, maxw=780)
put("超过 10 所公办高中，正在改扩建", font(30, True), (W / 2, y + 204), color=GOLD, maxw=780)
put("多分布在罗湖、福田、宝安、龙华、龙岗等成熟片区", font(17), (W / 2, y + 268), color=LIGHT, maxw=780)
put("※ 目前唯一官方公布新增学位数的是深二外：3年新增1200座", font(16), (W / 2, y + 316), color=SUB, maxw=780)
y += 360
y += 40
y = mea(y, "扩容不只是新区的事。住在老城区的家庭，同样可能等来家门口那所学校的“长大”。深二外改扩建后年招生从990人增至近1400人，增幅超40%。")

# ---------- 05 两个五年 ----------
chapter(y, "05 · 两个五年，连续投入")
y += 100
box(40, y, W - 80, 380, r=18)
d.line([W / 2, y + 40, W / 2, y + 340], fill=EDGE, width=3)
put("十四五", font(30, True), (265, y + 76), color=LIGHT)
put("2020—2025", font(17), (265, y + 116), color=SUB)
put("约50所", font(46, True), (265, y + 196), color=GOLD)
put("新改扩建公办高中", font(21, True), (265, y + 258), color=WHITE)
put("新增11万个以上学位", font(17), (265, y + 312), color=SUB)
put("十五五", font(30, True), (635, y + 76), color=LIGHT)
put("2026—2030", font(17), (635, y + 116), color=SUB)
put("10万个以上", font(46, True), (635, y + 196), color=GOLD)
put("规划新增公办高中", font(21, True), (635, y + 258), color=WHITE)
put("五年全口径目标", font(17), (635, y + 312), color=SUB)
y += 380
y += 40
y = mea(y, "如果只是某一年紧张、临时应付一阵，做不出这种跨越两个五年规划的连续投入。这是“提前铺路”，不是“事后补课”。")

# ---------- 06 什么时候轮到 ----------
chapter(y, "06 · 这些学位，什么时候轮到你家孩子")
y += 100
box(40, y, W - 80, 400, r=18)
put("2027 届中考生", font(28, True), (W / 2, y + 72), color=LIGHT)
put("赶上的，是「扩容进行时」", font(38, True), (W / 2, y + 148), color=GOLD, maxw=760)
put("新校在建、在可研、在设计 —— 还轮不到", font(17), (W / 2, y + 216), color=SUB, maxw=760)
d.line([230, y + 262, 670, y + 262], fill=EDGE, width=3)
put("2029—2031 届中考生", font(26, True), (W / 2, y + 308), color=LIGHT)
put("才真正等到「扩容完成时」", font(30, True), (W / 2, y + 356), color=WHITE, maxw=760)
y += 400
y += 40
y = mea(y, "新学位在长出来，但长得没有你希望得那么快；而考生人数这几年一直在涨。公办普高录取率稳在约52%——“稳”意味着没恶化，但它不是“升”。")

# ---------- 07 三句话 ----------
chapter(y, "07 · 给2027届家长的三句话")
y += 100
for tag, detail, tc in [
    ("① 为城市鼓掌", "但为孩子做准备——城市的学位是十年的事，孩子的初三是一年的事", LIGHT),
    ("② 看长远", "但做在当下——未来的好消息，改变不了明年的竞争", LIGHT),
    ("③ 乐观", "但别盲目乐观——看好深圳的长期，做足孩子的当下", GOLD),
]:
    y = row(y, tag, detail, tc)
y += 36
box(40, y, W - 80, 300, r=18)
put("▍现在就能做的三件事", font(26, True), (W / 2, y + 62), color=GOLD)
put("① 守住校内排名 —— 名额分配占公办普高计划的50%，校内位次比全市分数更管用", font(17), (76, y + 136), anchor="lm", color=WHITE, maxw=740)
put("② 盯紧名额分配 —— 政策细节每年都要重新核一遍，别拿去年口径套今年", font(17), (76, y + 198), anchor="lm", color=WHITE, maxw=740)
put("③ 把志愿梯度想清楚 —— 新校越多，越要“对标位次”而不是“对标去年分数”", font(17), (76, y + 260), anchor="lm", color=WHITE, maxw=740)
y += 300

# ---------- 页脚 ----------
y += 60
d.line([50, y, 850, y], fill=EDGE, width=3)
y += 60
put("看好深圳的长期，做足孩子的当下。", font(34, True), (W / 2, y), color=WHITE, maxw=800)
y += 64
put("深圳不是在“补学位”，是在为孩子的未来提前铺路。", font(18), (W / 2, y), color=LIGHT, maxw=800)
y += 60
put("关注 · 深圳中考系列持续更新 · 把学位的账提前算清", font(17), (W / 2, y), color=SUB, maxw=W - 80)
y += 52
for s in [
    "数据来源：深圳市政府采购网合同公示 · 深圳市教育局历年高中阶段学校招生计划与招标公告",
    "深圳市建筑工务署招标公告 · 深圳市人民政府门户网站 · 深圳特区报",
    "各项目进展、学位数与“十五五”规划目标以官方最终发布为准",
]:
    put(s, font(14), (W / 2, y), color=LIGHT, maxw=W - 110)
    y += 50

# ---------- 裁剪 ----------
content_end = y
print("内容底部≈", content_end, "| 画布H=", H, "| 余量=", H - content_end)
final_h = content_end + 60
img2 = img.crop((0, 0, W, final_h))
out2 = OUT + "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？-公众号-长图-极简版.png"
img2.save(out2)
print("saved", out2.split("/")[-1], img2.size)

# ---------- 校验 ----------
bad = 0; bxs = []
for (text, fnt, (cx, cy), anchor, color, maxw) in checks:
    bbox = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
    x0, y0 = bbox[0] + cx, bbox[1] + cy
    x1, y1 = bbox[2] + cx, bbox[3] + cy
    bw = x1 - x0
    bxs.append(((x0, y0, x1, y1), text, (cx, cy)))
    ok = (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1)
    if maxw and bw > maxw + 2: ok = False
    if not ok:
        bad += 1
        print(f"OVERFLOW [{text[:20]}] x=({x0:.0f},{x1:.0f}) y=({y0:.0f},{y1:.0f}) maxw={maxw}")
print("OVERFLOW:", "PASS" if bad == 0 else f"FAIL {bad}")
ov = 0
for i in range(len(bxs)):
    for j in range(i + 1, len(bxs)):
        (ax0, ay0, ax1, ay1), at, ac = bxs[i]
        (bx0, by0, bx1, by1), bt, bc = bxs[j]
        if ac == bc:
            continue
        ox = max(0, min(ax1, bx1) - max(ax0, bx0))
        oy = max(0, min(ay1, by1) - max(ay0, by0))
        if ox > 4 and oy > 4:
            ov += 1
            print(f"OVERLAP: [{at[:14]}] x [{bt[:14]}]")
print("OVERLAP:", "PASS" if ov == 0 else f"FAIL {ov}")

# ---------- 渐变单调性检查 ----------
arrck = np.asarray(img2.convert("RGB"))
lum = arrck.mean(axis=(1, 2))
mono = np.all(np.diff(lum[::40]) <= 1e-6) or np.all(np.diff(lum[::40]) >= -1e-6)
print("渐变单调:", "PASS" if mono else "WARN(存在非单调段，多为柔光叠加，人工确认)")
print("底部留白:", final_h - content_end, "px")

build_cover()
