# -*- coding: utf-8 -*-
"""
P1-4 S4 走读调剂/保存确认 全套配图（深青蓝档：22,62,122 / 底 6,15,36；左主光+勾选清单装饰）
蓝系家族。公众号900x383 + 头条1200x900×3 + 抖音1080x1920×6 + 小红书1080x1440×5
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解/子任务S4-走读调剂与保存确认"

def font(sz):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def base(w, h):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array([22,62,122], np.float32)*(1-y) + np.array([6,15,36], np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.18, h*0.12
    radial = np.exp(-(((xx-gx)/(w*0.5))**2 + ((yy-gy)/(h*0.3))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.30*radial[..., None]
    for k in (0.3, 0.85):
        img += glow*0.09*np.exp(-(((xx-k*yy)/w)-0.08)**2/(2*0.05**2))[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def checkboxes(d, w, h, n=3):
    x0, y0 = int(w*0.06), int(h*0.92)
    for i in range(n):
        x = x0 + i*70
        d.rounded_rectangle([x, y0, x+44, y0+44], radius=8, outline=(130,175,235), width=3)
        d.line([x+10, y0+23, x+18, y0+32], fill=(130,210,160), width=4)
        d.line([x+18, y0+32, x+36, y0+10], fill=(130,210,160), width=4)

def badge(d, x, y, text, fs):
    f = font(fs); tw = d.textlength(text, font=f)
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, fill=(6,18,44))
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, outline=(120,165,225), width=2)
    d.text((x, y), text, font=f, fill=(205,228,255))

def mt(d, xy, lines, fs, fill=(255,255,255), lh=1.25):
    f = font(fs)
    d.multiline_text(xy, "\n".join(lines), font=f, fill=fill, anchor="la", spacing=int(fs*lh-fs))

def check(path, w, h):
    im = Image.open(path).convert("RGB")
    assert im.size == (w, h), path
    px = im.load(); blue = 0
    for cx, cy in [(3,3),(w-4,3),(3,h-4),(w-4,h-4)]:
        r, g, b = px[cx, cy]; blue += int(b > r+8 and b > g+6)
    assert blue >= 3, path+" "+str(blue)
    print("OK", path.split('/')[-1])

def newimg(w, h):
    im = Image.fromarray(base(w, h)); d = ImageDraw.Draw(im); checkboxes(d, w, h)
    return im, d

if __name__ == "__main__":
    im, d = newimg(900,383)
    badge(d, 56, 40, "深圳中考 · 操作提醒 P1-4 S4", 20)
    mt(d, (56, 150), ["走读该不该勾？", "保存≠确认"], 50)
    d.text((60, 305), "单程45分钟内才勾 · 填完记得点确认", font=font(27), fill=(255,210,120))
    p = f"{BASE}/P1-4-S4-走读调剂保存-公众号-封面-精炼版-900x383.png"; im.save(p); check(p,900,383)

    def ttc(i, title, sub1, sub2):
        im, d = newimg(1200,900)
        badge(d, 72, 60, "深圳中考 · 操作提醒", 28)
        mt(d, (72, 250), title, 58, lh=1.16)
        d.text((76, 720), sub1, font=font(46), fill=(255,210,120))
        d.text((76, 800), sub2, font=font(33), fill=(150,185,235))
        p = f"{BASE}/P1-4-S4-走读调剂保存-头条-封面{i}-1200x900.png"; im.save(p); check(p,1200,900)
    ttc("1-主标题", ["走读调剂该不该勾？", "先看三年通勤"], "2026新增 · 最多对4校勾", "被走读录了：不能转住宿·不能退档")
    ttc("2-决策表", ["一张表决定", "勾 or 不勾"], "≤30✅ 30-45⚠️ >45❌ 必须住宿绝不勾", "走读是锦上添花，不是雪中送炭")
    ttc("3-保存确认", ["保存 ≠ 确认", "别白填"], "2026最多3次确认 · 6月1日18:00截止", "填完当晚 再确认一次 打印回执")

    def dy(n, big, card):
        im, d = newimg(1080,1920)
        badge(d, 60, 84, "深圳中考 · 操作提醒", 28)
        mt(d, (60, 330), big, 60, lh=1.16)
        d.line([62,820,1018,820], fill=(120,165,225), width=2)
        mt(d, (60, 860), card, 44, lh=1.3, fill=(205,228,255))
        d.text((60, 1500), f"{n:02d} / 06", font=font(40), fill=(120,160,215))
        p = f"{BASE}/P1-4-S4-走读调剂保存-抖音-镜头{n:02d}-1080x1920.png"; im.save(p); check(p,1080,1920)
    dy(1, ["勾了走读", "= 三年通勤"], ["2026新增 · 最多对4校勾", "还反悔不了"])
    dy(2, ["被走读录了", "不能转住宿"], ["不能转住宿", "不能退档"])
    dy(3, ["三句话记住"], ["单程45分钟内才勾", "必须住宿绝不勾 · 锦上添花不是雪中送炭"])
    dy(4, ["保存 ≠ 确认"], ["填写→保存→确认(验证码)→打印回执", "2026最多3次确认"])
    dy(5, ["只保存没确认", "= 志愿作废"], ["截止6月1日18:00", "每年都有人白填"])
    dy(6, ["填完当晚", "再确认一次"], ["P1-4投档讲完", "下条：名额分配50%指标到校"])

    im, d = newimg(1080,1440)
    badge(d, 60, 84, "深圳中考 · 操作提醒", 30)
    mt(d, (60, 440), ["走读", "只在45分钟内勾"], 84, lh=1.12)
    d.line([62,940,1018,940], fill=(120,165,225), width=2)
    mt(d, (60, 990), ["被走读录了：不能转住宿·不能退档", "保存≠确认 · 别白填"], 42, fill=(255,210,120), lh=1.3)
    p = f"{BASE}/P1-4-S4-走读调剂保存-小红书-封面-1080x1440.png"; im.save(p); check(p,1080,1440)

    def xc(i, title, body, extra=None):
        im, d = newimg(1080,1440)
        badge(d, 60, 84, "深圳中考 · 操作提醒", 28)
        mt(d, (60, 250), title, 58, lh=1.18)
        d.line([62,620,1018,620], fill=(120,165,225), width=2)
        mt(d, (60, 680), body, 42, lh=1.45, fill=(205,228,255))
        if extra: d.text((60, 1330), extra, font=font(32), fill=(255,210,120))
        p = f"{BASE}/P1-4-S4-走读调剂保存-小红书-正文图{i}-1080x1440.png"; im.save(p); check(p,1080,1440)
    xc("1-走读风险", ["走读调剂是什么"], ["2026新增 · 第一批普高最多对4校勾", "勾了：住宿满、走读有余 → 录走读", "被走读录：不能转住宿 · 不能退档"])
    xc("2-决策表", ["一张表：勾 or 不勾"], ["≤30分钟 → ✅ 勾", "30-45分钟能接受 → ⚠️ 谨慎", ">45分钟/换乘 → ❌ 不勾", "必须住宿 → ❌ 绝不勾"], extra="走读是锦上添花，不是雪中送炭")
    xc("3-保存确认", ["保存 ≠ 确认"], ["填写→保存→确认(短信验证码)→打印回执", "2026最多3次确认 · 第3次后不能改", "截止6月1日18:00", "只保存没确认 = 志愿作废"], extra="每年都有人白填")
    xc("4-收口", ["P1-4 投档讲完了"], ["五批次 / 志愿顺序 / 同分 / 梯度 / 走读 / 保存", "", "下一步：打开HSEE模拟志愿填报", "亲手排一次 · 查目标校历年AC/D线", "下篇P1-5：名额分配50%指标到校"])
