# -*- coding: utf-8 -*-
"""P1-1 封面「化繁为简」重制 12 张
规则（样板已确认）：去掉顶部徽章胶囊/系列小字、去掉装饰性底部金句，
只保留 大标题/主数字 + 单行核心信息（功能行）+ 必要 CTA；留白放大。
产出文件名统一前缀「化繁为简-」，与原图并存。
覆盖：
  公众号主线首图 ×2（900×383）
  公众号子任务封面 ×5（900×383）
  今日头条封面 ×3（1200×900）
  小红书首图 ×2（1080×1440，视频/图文各一）
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

FD = "C:/Windows/Fonts/"
WHITE = (255, 255, 255); GOLD = (245, 198, 107)
LIGHT = (157, 184, 212); SUB = (201, 217, 232)
NAVY = (18, 30, 55)


def font(size, bold=False):
    return ImageFont.truetype(FD + ("msyhbd.ttc" if bold else "msyh.ttc"), size)


def canvas(w, h):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c1 = np.array((27, 58, 92), np.float32); c2 = np.array((13, 30, 48), np.float32)
    arr = (c1[None, None, :] * (1 - t[:, :, None]) + c2[None, None, :] * t[:, :, None])
    img = Image.fromarray(arr.repeat(w, axis=1).astype(np.uint8), "RGB")
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    glow = np.exp(-(((xx - w * 0.5) / (w * 0.62)) ** 2 + ((yy - h * 0.16) / (h * 0.5)) ** 2)) * 0.15
    img = Image.fromarray(np.clip(np.array(img, float) + np.array((210, 225, 250))[None, None, :] * glow[:, :, None], 0, 255).astype(np.uint8), "RGB")
    return img, ImageDraw.Draw(img)


def put(d, ck, text, fnt, xy, anchor="mm", color=WHITE, maxw=None, W=1200, H=900):
    if maxw is not None:
        size = fnt.size
        path = "msyhbd.ttc" if fnt.path.endswith("msyhbd.ttc") else "msyh.ttc"
        while size > 12:
            bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
            x0, y0 = bb[0] + xy[0], bb[1] + xy[1]
            x1, y1 = bb[2] + xy[0], bb[3] + xy[1]
            if x1 - x0 <= maxw + 1 and x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1:
                break
            size -= 1
            fnt = ImageFont.truetype(FD + path, size)
    d.text(xy, text, font=fnt, fill=color, anchor=anchor)
    ck.append((text, fnt, xy, anchor))


def verify(d, ck, name, W, H):
    bad = 0
    for (text, fnt, (cx, cy), anchor) in ck:
        bb = d.textbbox((0, 0), text, font=fnt, anchor=anchor)
        x0, y0 = bb[0] + cx, bb[1] + cy
        x1, y1 = bb[2] + cx, bb[3] + cy
        if not (x0 >= -1 and x1 <= W + 1 and y0 >= -1 and y1 <= H + 1):
            bad += 1
            print(f"  [越界] {text!r} 字体{fnt.size} @({cx},{cy})")
    print(f"{name}: OVERFLOW {'PASS' if bad == 0 else 'FAIL ' + str(bad)}")
    return bad == 0


GZH = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/01.公众号/"
TT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/02.今日头条/"
XHS = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-1-游戏规则全景/04.小红书/"
ALL = []


# ================= 900×383 · 公众号横版封面 =================
def gzh(big, sub_top, foot, out, big_color=GOLD, big_size=112):
    """中心大数字(或文字) + 底部单行核心信息；无徽章无装饰金句。"""
    img, d = canvas(900, 383); ck = []
    if sub_top:
        put(d, ck, sub_top, font(20, True), (450, 78), color=LIGHT, maxw=860, W=900, H=383)
    put(d, ck, big, font(big_size, True), (450, 205 if not sub_top else 200), color=big_color, maxw=860, W=900, H=383)
    if foot:
        put(d, ck, foot, font(20, True), (450, 322), color=WHITE, maxw=880, W=900, H=383)
    ALL.append(verify(d, ck, os.path.basename(out), 900, 383))
    img.save(out)
    print("saved", out.split("/")[-1])


# 主线-精简版首图：两行标题（无副题胶囊）
img, d = canvas(900, 383); ck = []
put(d, ck, "深圳中考游戏规则", font(42, True), (450, 128), color=WHITE, maxw=880, W=900, H=383)
put(d, ck, "30分钟从入门到看懂", font(46, True), (450, 212), color=GOLD, maxw=880, W=900, H=383)
put(d, ck, "总分630 · ACD三类 · 五批次 · 16志愿", font(21, True), (450, 330), color=LIGHT, maxw=880, W=900, H=383)
ALL.append(verify(d, ck, "主线精简首图·化繁", 900, 383))
img.save(GZH + "01.主线/化繁为简-P1-1-主线-公众号-首图-精简版-900x383.png")
print("saved 化繁为简-主线精简首图")

# 主线-极简大字版：630 巨字为唯一主角
gzh("630", None, "语数英物化440分 · 每1分都有它的位置", GZH + "01.主线/化繁为简-P1-1-主线-公众号-首图-极简大字版-900x383.png")

# 子任务02 · 630构成
gzh("630", "总分怎么构成的", "语数英物化 440 分 · 历史道法体育 170 分",
    GZH + "02.子任务-630构成卡/化繁为简-P1-1-子任务02-公众号封面-900x383.png")
# 子任务03 · ACD三类
img, d = canvas(900, 383); ck = []
put(d, ck, "考生分 ACD 三类", font(60, True), (450, 178), color=GOLD, maxw=860, W=900, H=383)
put(d, ck, "你站哪条赛道 · 决定了能报哪些学校", font(21, True), (450, 322), color=WHITE, maxw=880, W=900, H=383)
ALL.append(verify(d, ck, "子任务ACD·化繁", 900, 383))
img.save(GZH + "03.子任务-ACD对比卡/化繁为简-P1-1-子任务03-公众号封面-900x383.png")
print("saved 化繁为简-ACD封面")
# 子任务04 · 五批次
gzh("5", "录取分几个批次", "自招→名额分配→第一批16→第二批18→第三批6",
    GZH + "04.子任务-批次顺序卡/化繁为简-P1-1-子任务04-公众号封面-900x383.png")
# 子任务05 · 时间线
gzh("6", "从报名到录取要多久", "3月报名到8月录取 · 志愿填报那10天最重要",
    GZH + "05.子任务-时间线卡/化繁为简-P1-1-子任务05-公众号封面-900x383.png")
# 子任务06 · 排队录取
gzh("16", "第一批志愿可以填几个", "分高先挑 · 最想去的放前面 · 按志愿顺序录取",
    GZH + "06.子任务-排队比喻卡/化繁为简-P1-1-子任务06-公众号封面-900x383.png")


# ================= 1200×900 · 头条封面 =================
# 封面1 · 主标题
img, d = canvas(1200, 900); ck = []
put(d, ck, "深圳中考游戏规则", font(62, True), (600, 300), color=WHITE, maxw=1100, W=1200, H=900)
put(d, ck, "30分钟从入门到看懂", font(68, True), (600, 440), color=GOLD, maxw=1100, W=1200, H=900)
put(d, ck, "总分630 · ACD三类 · 五批次 · 16志愿", font(34, True), (600, 620), color=LIGHT, maxw=1100, W=1200, H=900)
put(d, ck, "四句话 · 讲完深圳中考的游戏规则", font(34, True), (600, 805), color=WHITE, maxw=1100, W=1200, H=900)
ALL.append(verify(d, ck, "头条封面1·化繁", 1200, 900))
img.save(TT + "化繁为简-今日头条-封面1-主标题-1200x900.png")
print("saved 化繁为简-头条封面1")

# 封面2 · 数据对撞 440/170
img, d = canvas(1200, 900); ck = []
put(d, ck, "630分 · 8科 · 分两大块", font(36, True), (600, 210), color=LIGHT, maxw=1100, W=1200, H=900)
put(d, ck, "440", font(150, True), (380, 500), color=GOLD, maxw=520, W=1200, H=900)
put(d, ck, "语数英物化 · 主战场", font(34, True), (380, 660), color=WHITE, maxw=560, W=1200, H=900)
put(d, ck, "170", font(150, True), (820, 500), color=WHITE, maxw=520, W=1200, H=900)
put(d, ck, "历史道法体育 · 定公办民办", font(34, True), (820, 660), color=WHITE, maxw=560, W=1200, H=900)
put(d, ck, "每1分都有它的位置 · 备考价值不一样", font(34, True), (600, 815), color=GOLD, maxw=1100, W=1200, H=900)
ALL.append(verify(d, ck, "头条封面2·化繁", 1200, 900))
img.save(TT + "化繁为简-今日头条-封面2-数据对撞-1200x900.png")
print("saved 化繁为简-头条封面2")

# 封面3 · 答案大字
img, d = canvas(1200, 900); ck = []
put(d, ck, "搞懂规则", font(150, True), (600, 330), color=GOLD, maxw=1100, W=1200, H=900)
put(d, ck, "不犯低级错误 · 本身就是优势", font(46, True), (600, 560), color=WHITE, maxw=1100, W=1200, H=900)
put(d, ck, "四句话 · 建立深圳中考全景地图", font(34), (600, 700), color=LIGHT, maxw=1100, W=1200, H=900)
ALL.append(verify(d, ck, "头条封面3·化繁", 1200, 900))
img.save(TT + "化繁为简-今日头条-封面3-答案大字-1200x900.png")
print("saved 化繁为简-头条封面3")


# ================= 1080×1440 · 小红书首图 =================
def xhs_cover(out):
    img, d = canvas(1080, 1440); ck = []
    put(d, ck, "深圳中考游戏规则", font(58, True), (540, 300), color=WHITE, maxw=1000, W=1080, H=1440)
    put(d, ck, "四句话就讲完", font(122, True), (540, 545), color=GOLD, maxw=1000, W=1080, H=1440)
    put(d, ck, "总分630 · ACD三类 · 五批次 · 16志愿", font(36, True), (540, 840), color=LIGHT, maxw=1020, W=1080, H=1440)
    d.rounded_rectangle([280, 1150, 800, 1290], radius=70, fill=GOLD)
    put(d, ck, "收藏 · 30分钟看懂规则", font(44, True), (540, 1220), color=NAVY, maxw=480, W=1080, H=1440)
    ALL.append(verify(d, ck, "小红书首图·化繁", 1080, 1440))
    img.save(out)
    print("saved", out.split("/")[-1])


xhs_cover(XHS + "01.视频/化繁为简-P1-1-深圳中考游戏规则-四句话看懂-小红书-首图-1080x1440.png")
xhs_cover(XHS + "02.图文/化繁为简-P1-1-深圳中考游戏规则-四句话看懂-小红书-首图-1080x1440.png")

print()
print("全部 OK =", all(ALL))
