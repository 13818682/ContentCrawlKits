# -*- coding: utf-8 -*-
"""
P1-8《中考术语速查手册 A–Z》· 小红书 1080×1440 配图 · 共 9 张
封面1 + 正文卡7 + 尾卡1

视觉档：**P1-8 档 = 蓝系家族第四档**
  主线 = 深靛蓝 TOP(22,56,110) → 右下「同心分配环」· 中上光
  S1   = 深蓝   TOP(14,44,92)  → 右下「标尺刻度」  · 中上光
  S2   = 中深蓝 TOP(18,52,104) → 右下「勾选框列」  · 左上光
  P1-8 = 深钴蓝 TOP(28,66,122) → 左上「字母索引条」· 右上光   ← 本档

铁律：主色永远深蓝系不换色相；任务间只靠 深浅 × 光影 × 光线角度 × 装饰 × 版式 差异化。
版式：沿用 P1-4 家族坐标（cover-layout-spec §四），P1-8 在「版式」一维上做区分
      （正文卡由 S2 的「居中单行」改为「左对齐 术语+释义 两段式」）。
数据：术语释义口径见 P1-8/04-数据核验清单；控制线/等级/志愿数出报考指导手册。
"""
import time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"

# ---- P1-8 档（深钴蓝）----
TOP, BOT = (28, 66, 122), (8, 18, 44)
CARD, EDGE = (14, 42, 86), (104, 158, 226)
GOLD, WHITE = (255, 210, 120), (255, 255, 255)
LIGHT, SUB = (176, 208, 246), (214, 230, 252)

BADS = []
PFX = "P1-8-术语速查手册"
ROOT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/"
        "P1-政策解码器/P1-8-术语速查手册")
SRC = "数据来源：深圳市教育局公开发布文件（2026 年报考指导手册 / 招生计划）"

WX, HX, HM = 1080, 1440, 80


def font(fp, s):
    return ImageFont.truetype(fp, s)


def save_img(im, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for _ in range(6):
        try:
            im.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)


def base(w, h):
    """蓝系渐变 + 右上主光（P1-8 的光线角度）+ 左上「字母索引条」。"""
    yv = np.linspace(0, 1, h)[:, None, None]
    grad = (np.array(TOP, float)[None, None, :] * (1 - yv) + np.array(BOT, float)[None, None, :] * yv)
    grad = np.repeat(grad, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    # 主光：右上（区别于主线的中上、S2 的左上）
    gx, gy = w * 0.78, h * 0.09
    radial = np.exp(-(((xx - gx) / (w * 0.58)) ** 2 + ((yy - gy) / (h * 0.32)) ** 2))
    glow = np.array([255, 255, 255], float)[None, None, :]
    img = grad + glow * 0.26 * radial[..., None]
    # 左上角「字母索引条」：一排高低不齐的竖直短条，模拟词典/索引页边标
    #   · 形状 = 高低不齐（vs S2 右下「等高方框列」）
    #   · 位置 = 左上（与右上主光成对角，沿家族规律"光在一角、装饰在对角"）
    #   · 落点避开所有内容：各页品牌行居中（x≥390）、正文块均 y≥300
    bw = max(14, int(w * 0.022))
    gapb = int(bw * 0.62)
    x0 = int(w * 0.045)
    ytop = int(h * 0.052)
    n = 7
    for i in range(n if h >= 600 else 0):
        hh = int(h * (0.030 + 0.007 * (i % 4)))
        xa = x0 + i * (bw + gapb)
        bar = np.zeros((h, w), float)
        bar[ytop:ytop + hh, xa:xa + bw] = 1.0
        bar[ytop:ytop + max(2, int(h * 0.006)), xa:xa + bw] = 2.0
        img += glow * 0.15 * bar[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

def fit(d, text, fp, size, maxw, mini):
    f = font(fp, size)
    while f.size > mini:
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw + 1:
            break
        f = font(fp, f.size - 1)
    bb = d.textbbox((0, 0), text, font=f)
    assert bb[2] - bb[0] <= maxw + 1, "too long: %s" % text
    return f


def txt(d, text, xy, size, fill, fp=FB, maxw=840, mini=24, anchor="mm", tag=""):
    f = fit(d, text, fp, size, maxw, mini)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)
    BADS.append((tag or text[:10], d.textbbox(xy, text, font=f, anchor=anchor)))


def rcard(d, x0, y0, x1, y1, rad=24, outline=None, fill=None):
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad,
                        fill=fill or CARD, outline=outline or EDGE, width=3)


def audit(im, name, right_pad=18, botskip=8):
    bad = [(t, tuple(int(v) for v in bb)) for t, bb in BADS
           if bb[0] < right_pad or bb[1] < botskip
           or bb[2] > im.size[0] - right_pad or bb[3] > im.size[1] - botskip]
    print(("OK  " if not bad else "!!  ") + name + ("  " + str(bad) if bad else ""))
    BADS.clear()
    return not bad


# ---------- 1. 封面 ----------
def xhs_cover():
    im = base(WX, HX); d = ImageDraw.Draw(im)
    txt(d, "深圳中考", (WX / 2, 180), 104, GOLD, maxw=1000, mini=80, tag="brand")

    txt(d, "黑话 A–Z", (WX / 2, 520), 132, WHITE, maxw=1000, mini=96, tag="title")
    tw = d.textlength("黑话 A–Z", font=font(FB, 132))
    d.line([WX / 2 - (tw + 24) / 2, 646, WX / 2 + (tw + 24) / 2, 646], fill=GOLD, width=8)

    txt(d, "24 个词 · 7 类 · 一次讲清", (WX / 2, 748), 58, WHITE, maxw=1000, mini=40, tag="sub")
    txt(d, "家长群天天说，一半人没真懂", (WX / 2, 930), 54, GOLD, maxw=1000, mini=38, tag="kick")
    txt(d, "遇到不懂的，翻回来对一下", (WX / 2, 1160), 36, SUB, fp=FR, maxw=1000, mini=26, tag="note")
    txt(d, "深圳中考 · 术语速查 · 关注不迷路", (WX / 2, 1366), 27, SUB, fp=FR, maxw=1000, mini=20, tag="foot")

    ok = audit(im, "封面")
    save_img(im, f"{ROOT}/04.小红书/{PFX}-小红书-封面-1080x1440.png")
    return ok


# ---------- 2. 正文卡（术语 + 释义，两段式左对齐）----------
MT, MB = 330, 1112          # 行区
BAND0, BANDH = 1150, 118    # 结论横幅


def xhs_term_card(fn, idx, cat, lead, rows, band):
    im = base(WX, HX); d = ImageDraw.Draw(im)

    txt(d, f"黑话 A–Z · {idx}/07", (WX / 2, 84), 32, GOLD, maxw=980, mini=24, tag="kick")
    txt(d, cat, (WX / 2, 186), 60, WHITE, maxw=1000, mini=42, tag="cat")
    txt(d, lead, (WX / 2, 272), 30, LIGHT, fp=FR, maxw=1000, mini=22, tag="lead")

    n = len(rows)
    gap = 22
    rh = max(150, min((MB - MT - (n - 1) * gap) / n, 360))
    y = MT
    for i, (term, defs) in enumerate(rows):
        y1 = y + rh
        rcard(d, HM, y, WX - HM, y1, rad=22)
        lh, th = 30, 46
        block = th + 12 + len(defs) * lh
        top = y + max(26, (rh - block) / 2)
        txt(d, term, (HM + 36, top), 42, WHITE,
            fp=FB, maxw=WX - 2 * HM - 72, mini=28, anchor="lt", tag="term")
        yy = top + th + 12
        for ln in defs:
            txt(d, ln, (HM + 36, yy), 27, LIGHT,
                fp=FR, maxw=WX - 2 * HM - 72, mini=19, anchor="lt", tag="def")
            yy += lh
        y = y1 + (gap if i < n - 1 else 0)

    d.rounded_rectangle([HM - 6, BAND0, WX - HM + 6, BAND0 + BANDH], radius=26,
                        fill=CARD, outline=GOLD, width=4)
    txt(d, band, (WX / 2, BAND0 + BANDH / 2), 34, GOLD, maxw=940, mini=24, tag="band")
    txt(d, SRC, (WX / 2, 1382), 20, SUB, fp=FR, maxw=1010, mini=14, tag="foot")

    ok = audit(im, f"正文卡{idx} {cat}")
    save_img(im, f"{ROOT}/04.小红书/{fn}-1080x1440.png")
    return ok


# ---------- 3. 尾卡（关注 + 合集）----------
def xhs_tail():
    im = base(WX, HX); d = ImageDraw.Draw(im)
    txt(d, "深圳中考", (WX / 2, 172), 90, GOLD, maxw=1000, mini=76, tag="brand")

    txt(d, "24 个词，我拆成 7 张卡", (WX / 2, 430), 88, WHITE, maxw=930, mini=64, tag="tail1")
    tw = d.textlength("24 个词，我拆成 7 张卡", font=font(FB, 88))
    d.line([WX / 2 - (tw + 24) / 2, 534, WX / 2 + (tw + 24) / 2, 534], fill=GOLD, width=8)

    txt(d, "主页合集里，按顺序看", (WX / 2, 632), 56, GOLD, maxw=1000, mini=40, tag="tail2")

    HMG = 64
    bands = [("中考规则，一篇讲透", True),
             ("查分数线 · 选学校", False),
             ("填志愿，不踩坑", False)]
    y = 764
    for label, hot in bands:
        rcard(d, HMG, y, WX - HMG, y + 112, rad=22,
              outline=GOLD if hot else EDGE, fill=(30, 60, 108) if hot else CARD)
        txt(d, label, (WX / 2, y + 56), 46, GOLD if hot else LIGHT,
            maxw=WX - 2 * HMG - 40, mini=30, tag="band")
        y += 112 + 26

    txt(d, "关注 · 深圳中考黑话", (WX / 2, 1300), 48, WHITE, maxw=1000, mini=34, tag="cta")
    txt(d, SRC, (WX / 2, 1386), 20, SUB, fp=FR, maxw=1010, mini=14, tag="foot")

    ok = audit(im, "尾卡")
    save_img(im, f"{ROOT}/04.小红书/{PFX}-小红书-尾卡-关注合集-1080x1440.png")
    return ok


# ---------- 内容字典（改内容只改这里，不动版式）----------
CARDS = [
 ("P1-8-术语速查手册-小红书-正文图1-身份类", "01", "身份类",
  "先分清你孩子站在哪条赛道",
  [("ACD 类", ["A / C 类深户、D 类非深户；两者报公办", "走的是不同名额，赛道本身就不一样"]),
   ("应届 / 往届", ["往届生不能走名额分配，也不能报自主招生"]),
   ("学籍（三年不转）", ["名额分配要求初中三年在同一所学校；", "初一转进、初三转出，都不算"]),
   ("省一级公办普高", ["它录取的「名额分配生」有单科等级门槛：", "语数英物化史道法 C+ 以上、体育 C 以上"])],
  "D 类家长：名额分配对你全覆盖，别以为与自己无关"),

 ("P1-8-术语速查手册-小红书-正文图2-分数类", "02", "分数类",
  "分数线是结果，不是门槛",
  [("总分 630", ["由 8 个科目构成，每科分数与等级各有规则"]),
   ("原始分", ["你考多少就是多少，不做换算"]),
   ("单科等级", ["按全市排位给等级，不是按绝对分数给"]),
   ("录取分数线", ["不是学校「设」的，是该校最后一名", "被录取考生的分数——所以每年都在动"])],
  "相比分数，全市位次才是更稳的参照"),

 ("P1-8-术语速查手册-小红书-正文图3-线类", "03", "线类",
  "三种线，管的事完全不同",
  [("名额分配录取控制线", ["官方按「该校前三年录取线均分降 20 分」", "划定；每所高中一条，与该校当年第一批", "分数线无关。达不到 → 该志愿直接作废"]),
   ("一分一段表", ["全市排位定位器，填志愿前先定位次"]),
   ("走读线", ["同一所学校，走读录取线通常低于住宿线"])],
  "控制线只决定「有没有资格投档」，不决定录取"),

 ("P1-8-术语速查手册-小红书-正文图4-批次类", "04", "批次类",
  "顺序不可逆，前面录了后面全作废",
  [("五个批次", ["自主招生 → 名额分配 → 第一批 →", "第二批 → 第三批，依次进行"]),
   ("第一批 16 个志愿", ["最多 12 个普高 + 4 个中职"]),
   ("同分比较", ["总分相同时逐项比较，决定谁先被投档"]),
   ("不退档、不转录", ["一旦被录取（含走读调剂），没有「再看看」"])],
  "批次顺序不可逆——前面填高一点，后面才是安全网"),

 ("P1-8-术语速查手册-小红书-正文图5-通道类", "05", "通道类",
  "只盯一条路，最容易落空",
  [("正取生", ["第一批按分数录取，最常规的那条路"]),
   ("名额分配生（指标生）", ["高中 50% 名额分到初中，", "在你孩子本校 / 本区里竞争"]),
   ("自主招生", ["一类看数理 / 科创，二类看艺术 / 体育"])],
  "通道要组合着用，别把宝全压在一条上"),

 ("P1-8-术语速查手册-小红书-正文图6-路径类", "06", "路径类",
  "普高不是唯一出口",
  [("3+4 中本贯通", ["中职 3 年 + 本科 4 年 → 全日制本科", "（2026 年 300 个名额）"]),
   ("3+2 中高贯通", ["中职 3 年 + 高职 2 年 → 全日制大专", "（2026 年 63 个专业、2,853 个名额）"]),
   ("民办普高", ["学费高于公办，但 A / C / D 类同分录取"]),
   ("中职技工", ["与普高并列的另一条赛道，不等于没出路"])],
  "这几条路不走第一批，别和普通高中志愿混着看"),

 ("P1-8-术语速查手册-小红书-正文图7-操作类", "07", "操作类",
  "每年都有人栽在这两步上",
  [("保存 ≠ 确认", ["点「保存」只是暂存，必须再点「确认」", "并输入验证码才算提交；截止日 18:00 前", "没确认的，志愿全部作废"]),
   ("走读调剂", ["勾了被录取后不能转住宿、不能退档——", "勾之前先算清通勤时间"])],
  "填完当晚再进系统确认一次，那是最后一次后悔的机会"),
]


if __name__ == "__main__":
    results = [xhs_cover()]
    for fn, idx, cat, lead, rows, band in CARDS:
        results.append(xhs_term_card(fn, idx, cat, lead, rows, band))
    results.append(xhs_tail())
    print("\n共 %d 张；四道闸口全过：%s" % (len(results), all(results)))
