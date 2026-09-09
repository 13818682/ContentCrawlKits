# -*- coding: utf-8 -*-
"""
P1-4 S2 同分PK 全套配图（steel 档：46,78,132 / 底 10,20,44；右上主光+同心圆+斜光束）
- 公众号封面 900x383 + 头条3封面 1200x900 + 抖音6分镜 1080x1920 + 小红书封面+正文4 1080x1440
蓝系家族，主色深蓝禁换色相。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解/子任务S2-同分PK"

def font(sz, bold=True):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def base(w, h, TOP=(46,78,132), BOT=(10,20,44)):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32)*(1-y) + np.array(BOT, np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.80, h*0.12
    radial = np.exp(-(((xx-gx)/(w*0.5))**2 + ((yy-gy)/(h*0.3))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.30*radial[..., None]
    # 斜光束（右上→左下方向镜像）
    for k in (0.35, 0.9):
        u = ((w-xx) - k*yy)/w
        img += glow*0.10*np.exp(-(u-0.08)**2/(2*0.05**2))[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def D(w, h):
    return ImageDraw.Draw(Image.fromarray(base(w, h), "RGB"))

def rings(d, w, h):
    cx, cy = int(w*0.86), int(h*0.16)
    for rad, col in [(110,(90,140,200)), (170,(70,115,175)), (235,(55,95,155))]:
        d.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], outline=col, width=2)

def badge(d, x, y, text, fs):
    f = font(fs); tw = d.textlength(text, font=f)
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, fill=(12,34,72))
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, outline=(120,160,220), width=2)
    d.text((x, y), text, font=f, fill=(205,228,255))

def mt(d, xy, lines, fs, fill=(255,255,255), lh=1.25, spacing=None):
    f = font(fs)
    d.multiline_text(xy, "\n".join(lines), font=f, fill=fill, anchor="la",
                     spacing=int((spacing or (fs*lh-fs))))

def hline(d, x0, x1, y, color=(120,160,220), wdt=2):
    d.line([x0, y, x1, y], fill=color, width=wdt)

def check(path, w, h):
    im = Image.open(path).convert("RGB")
    assert im.size == (w, h), path
    px = im.load(); blue = 0
    for cx, cy in [(3,3),(w-4,3),(3,h-4),(w-4,h-4)]:
        r, g, b = px[cx, cy]; blue += int(b > r+8 and b > g+6)
    assert blue >= 3, path+" blue "+str(blue)
    print("OK", path.split('/')[-1])

if __name__ == "__main__":
    # 公众号封面 900x383
    img = Image.fromarray(base(900,383)); d = ImageDraw.Draw(img)
    rings(d, 900, 383)
    badge(d, 56, 42, "深圳中考 · 同分规则 P1-4 S2", 20)
    mt(d, (56, 150), ["中考同分怎么比？", "先比生地，不是语数英"], 46)
    d.text((60, 300), "生地：初二就定下的隐形分", font=font(28), fill=(255,210,120))
    p = f"{BASE}/P1-4-S2-同分PK-公众号-封面-精炼版-900x383.png"; img.save(p); check(p,900,383)
    # 头条 3 封面 1200x900
    def ttc(i, title, sub1, sub2):
        img = Image.fromarray(base(1200,900)); d = ImageDraw.Draw(img)
        rings(d, 1200, 900)
        badge(d, 72, 62, "深圳中考 · 同分PK", 28)
        mt(d, (72, 240), title, 58, lh=1.16)
        d.text((76, 700), sub1, font=font(46), fill=(255,210,120))
        d.text((76, 780), sub2, font=font(33), fill=(150,185,235))
        d.text((76, 868), "HSEE · 模拟志愿填报", font=font(26), fill=(120,155,210))
        p = f"{BASE}/P1-4-S2-同分PK-头条-封面{i}-1200x900.png"; img.save(p); check(p,1200,900)
    ttc("1-主标题", ["中考同分怎么比？", "先比生地，不是语数英"], "第1层比生地合卷 · 第2层才比语数英", "生地是初二就定的隐形分")
    ttc("2-案例", ["生地98 vs 生地90", "同分先录98"], "580同分 · 语数英高10分也没用", "第1层生地就分出胜负")
    ttc("3-行动", ["没考初二生地？", "别裸考"], "这是唯一能提前锁定的分数", "已考完 · 查一下心里有数")
    # 抖音 6 分镜 1080x1920
    def dy(n, big, card):
        img = Image.fromarray(base(1080,1920)); d = ImageDraw.Draw(img)
        rings(d, 1080, 1920)
        badge(d, 60, 84, "深圳中考 · 同分PK", 28)
        mt(d, (60, 320), big, 62, lh=1.16)
        hline(d, 62, 1018, 780)
        mt(d, (60, 830), card, 44, lh=1.3, fill=(205,228,255))
        d.text((60, 1500), f"{n:02d} / 06", font=font(40), fill=(120,160,215))
        p = f"{BASE}/P1-4-S2-同分PK-抖音-镜头{n:02d}-1080x1920.png"; img.save(p); check(p,1080,1920)
    dy(1, ["同分先比", "初二那科？"], ["不是语数英", "是生地合卷"])
    dy(2, ["生地98", "vs 生地90"], ["580 同分 · 争最后1个名额", "比生地：98＞90 → 先录98"])
    dy(3, ["语数英高10分", "也没用"], ["第1层比生地", "第2层才比语数英"])
    dy(4, ["生地初二", "就考完了"], ["分数早定", "填志愿前改变不了"])
    dy(5, ["别过度焦虑"], ["同分PK只在", "'同分+争最后名额'极端情况触发"])
    dy(6, ["生地是隐形分"], ["没考别裸考", "考完心里有数"])
    # 小红书
    img = Image.fromarray(base(1080,1440)); d = ImageDraw.Draw(img)
    rings(d, 1080, 1440)
    badge(d, 60, 84, "深圳中考 · 同分PK", 30)
    mt(d, (60, 430), ["同分先比", "初二那科"], 84, lh=1.15)
    hline(d, 62, 1018, 940)
    mt(d, (60, 990), ["生地合卷 ＞ 语数英", "——多数家长想反了"], 42, fill=(255,210,120), lh=1.35)
    d.text((60, 1330), "生地：唯一初二就定下的隐形分", font=font(30), fill=(150,185,235))
    p = f"{BASE}/P1-4-S2-同分PK-小红书-封面-1080x1440.png"; img.save(p); check(p,1080,1440)
    def xc(i, title, body, extra=None):
        img = Image.fromarray(base(1080,1440)); d = ImageDraw.Draw(img)
        rings(d, 1080, 1440)
        badge(d, 60, 84, "深圳中考 · 同分PK", 28)
        mt(d, (60, 250), title, 58, lh=1.18)
        hline(d, 62, 1018, 620)
        mt(d, (60, 680), body, 42, lh=1.45, fill=(205,228,255))
        if extra: d.text((60, 1330), extra, font=font(32), fill=(255,210,120))
        p = f"{BASE}/P1-4-S2-同分PK-小红书-正文图{i}-1080x1440.png"; img.save(p); check(p,1080,1440)
    xc("1-层级表", ["同分PK层级表"], ["第1层：生物与地理(合卷) 高者优先", "第2层：语数英三科总分 高者优先", "", "先比生地，不是先比语数英"])
    xc("2-案例", ["生地98 vs 生地90"], ["小陈580 生地98 语数英300", "小李580 生地90 语数英310", "", "比生地：98＞90 → 小陈先录", "小李语数英高10分也没用"])
    xc("3-生地初二已定", ["生地初二就考完了"], ["分数早已躺在系统里", "填志愿、出总分时都改不了", "", "没考的：别裸考，能提前锁定", "考完的：查一下心里有数"], extra="别到最后一格才想起它")
    xc("4-别焦虑", ["不用为同分过度焦虑"], ["只在极端情况触发：", "总分相同 + 争同一校最后名额", "", "大多数人总分这层就录完了", "它是一道保险，不是决定一切"])
