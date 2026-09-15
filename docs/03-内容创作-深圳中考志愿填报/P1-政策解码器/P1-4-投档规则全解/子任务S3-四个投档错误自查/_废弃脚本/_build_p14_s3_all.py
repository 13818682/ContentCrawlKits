# -*- coding: utf-8 -*-
"""
P1-4 S3 四错自查/志愿梯度 全套配图（ink 深档：14,32,66 / 底 5,10,24；顶光+细网格自查感）
蓝系家族。公众号900x383 + 头条1200x900×3 + 抖音1080x1920×6 + 小红书1080x1440×5
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解/子任务S3-四个投档错误自查"

def font(sz):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def base(w, h):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array([14,32,66], np.float32)*(1-y) + np.array([5,10,24], np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.5, h*0.10
    radial = np.exp(-(((xx-gx)/(w*0.55))**2 + ((yy-gy)/(h*0.30))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.30*radial[..., None]
    for k in (0.4, 1.0):
        img += glow*0.08*np.exp(-(((xx-k*yy)/w)-0.12)**2/(2*0.05**2))[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def D(w, h):
    d = ImageDraw.Draw(Image.fromarray(base(w, h), "RGB"))
    # 细网格（自查感）
    for x in range(0, w, 90):
        d.line([x, 0, x, h], fill=(90,130,190), width=1)
    for y in range(0, h, 90):
        d.line([0, y, w, y], fill=(60,90,140), width=1)
    return d

def badge(d, x, y, text, fs):
    f = font(fs); tw = d.textlength(text, font=f)
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, fill=(6,16,38))
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, outline=(120,160,220), width=2)
    d.text((x, y), text, font=f, fill=(205,228,255))

def mt(d, xy, lines, fs, fill=(255,255,255), lh=1.25):
    f = font(fs)
    d.multiline_text(xy, "\n".join(lines), font=f, fill=fill, anchor="la", spacing=int(fs*lh-fs))

def check(path, w, h):
    im = Image.open(path).convert("RGB")
    assert im.size == (w, h), path
    px = im.load(); blue = 0
    for cx, cy in [(3,3),(w-4,3),(3,h-4),(w-4,h-4)]:
        r, g, b = px[cx, cy]; blue += int(b > r+4 and b > g+4)
    assert blue >= 3, path+" "+str(blue)
    print("OK", path.split('/')[-1])

if __name__ == "__main__":
    im2 = Image.fromarray(base(900,383)); d2 = ImageDraw.Draw(im2)
    for x in range(0,900,90): d2.line([x,0,x,383],fill=(80,120,180),width=1)
    for y in range(0,383,90): d2.line([0,y,900,y],fill=(55,85,135),width=1)
    badge(d2, 56, 40, "深圳中考 · 志愿自查 P1-4 S3", 20)
    mt(d2, (56, 150), ["12个志愿全填", "一个分段？"], 52); d2.text((60, 300), "冲稳保底 · 拉开梯度", font=font(30), fill=(255,210,120))
    p = f"{BASE}/P1-4-S3-四错自查-公众号-封面-精炼版-900x383.png"
    im2.save(p); check(p,900,383)

    def ttc(i, title, sub1, sub2):
        im = Image.fromarray(base(1200,900)); d = ImageDraw.Draw(im)
        badge(d, 72, 62, "深圳中考 · 志愿自查", 28)
        mt(d, (72, 250), title, 58, lh=1.16)
        d.text((76, 720), sub1, font=font(46), fill=(255,210,120))
        d.text((76, 800), sub2, font=font(33), fill=(150,185,235))
        p = f"{BASE}/P1-4-S3-四错自查-头条-封面{i}-1200x900.png"; im.save(p); check(p,1200,900)
    ttc("1-主标题", ["12个志愿全填", "一个分段？"], "超常→一所更好没报 · 失误→12个全灭", "冲稳保底 · 拉开梯度")
    ttc("2-案例", ["考560浪费分", "考520直接全灭"], "2025真实：12志愿全落 · 补录民办", "志愿没有容错 = 最贵的错")
    ttc("3-自查4问", ["4问自查", "填之前过一遍"], "占坑? 扎堆? 保底占第1? 走读看通勤?", "任一'是'，都要改")

    def dy(n, big, card):
        im = Image.fromarray(base(1080,1920)); d = ImageDraw.Draw(im)
        badge(d, 60, 84, "深圳中考 · 志愿自查", 28)
        mt(d, (60, 340), big, 60, lh=1.16)
        d.line([62,820,1018,820], fill=(120,160,220), width=2)
        mt(d, (60, 860), card, 44, lh=1.3, fill=(205,228,255))
        d.text((60, 1500), f"{n:02d} / 06", font=font(40), fill=(120,160,215))
        p = f"{BASE}/P1-4-S3-四错自查-抖音-镜头{n:02d}-1080x1920.png"; im.save(p); check(p,1080,1920)
    dy(1, ["12个志愿全填", "一个分段？"], ["听起来稳", "其实是最贵的错"])
    dy(2, ["超常发挥考560", "一所更好的没报"], ["全填530-540", "分浪费了"])
    dy(3, ["失误考520", "= 直接全灭"], ["2025真实：12志愿全落", "最后补录民办"])
    dy(4, ["拉开梯度", "冲·稳·保·底"], ["冲高5-15放2-3个", "稳±5放多数 · 保低10-20 · 底低30+"])
    dy(5, ["宁可冲不到", "不能保不住"], ["真实发挥有浮动", "梯度就是缓冲"])
    dy(6, ["4问自查", "任一'是'都要改"], ["占坑? 扎堆? 保底第1? 走读看通勤?", "志愿是区间不是点"])

    im = Image.fromarray(base(1080,1440)); d = ImageDraw.Draw(im)
    badge(d, 60, 84, "深圳中考 · 志愿自查", 30)
    mt(d, (60, 440), ["冲稳保底", "拉开梯度"], 86, lh=1.12)
    d.line([62,940,1018,940], fill=(120,160,220), width=2)
    mt(d, (60, 990), ["志愿是区间，不是点", "别全押一个分段"], 42, fill=(255,210,120), lh=1.3)
    p = f"{BASE}/P1-4-S3-四错自查-小红书-封面-1080x1440.png"; im.save(p); check(p,1080,1440)

    def xc(i, title, body, extra=None):
        im = Image.fromarray(base(1080,1440)); d = ImageDraw.Draw(im)
        badge(d, 60, 84, "深圳中考 · 志愿自查", 28)
        mt(d, (60, 260), title, 58, lh=1.18)
        d.line([62,620,1018,620], fill=(120,160,220), width=2)
        mt(d, (60, 680), body, 42, lh=1.45, fill=(205,228,255))
        if extra: d.text((60, 1330), extra, font=font(32), fill=(255,210,120))
        p = f"{BASE}/P1-4-S3-四错自查-小红书-正文图{i}-1080x1440.png"; im.save(p); check(p,1080,1440)
    xc("1-最贵的错", ["最贵的错：全扎一段"], ["超常考560 → 更好的没报", "失误考520 → 12个全够不着", "2025真实：12志愿全落·补录民办", "", "志愿没有容错 = 最贵"])
    xc("2-四档梯度", ["冲·稳·保·底 四档"], ["冲：高5-15分 放2-3个", "稳：平时±5分 放多数", "保：低10-20分", "底：低30分以上 一定留足", "", "宁可冲不到，不能保不住"])
    xc("3-4问自查", ["4问自查清单"], ["Q1 填了'录了也不想去'的? → 前批一录后批作废", "Q2 全扎一个分段? → 按梯度重排", "Q3 第1志愿填保底? → 保底放最后", "Q4 勾走读前看通勤? → 单程45分钟内"], extra="任一'是'都要改")
    xc("4-一句话", ["志愿是区间不是点"], ["别估一个分、填一堆分", "而是覆盖一段可能区间", "", "给孩子发挥好坏都留退路", "都尽量上更好的那所"])
