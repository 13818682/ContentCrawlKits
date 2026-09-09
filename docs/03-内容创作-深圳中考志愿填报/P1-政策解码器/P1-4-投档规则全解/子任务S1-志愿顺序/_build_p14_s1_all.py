# -*- coding: utf-8 -*-
"""
P1-4 S1 志愿顺序 全套配图（cobalt 档：18,74,128 / 底 6,16,42；左上主光+斜光束）
- 公众号封面 900x383(1) + 头条 3 封面 1200x900
- 抖音 6 分镜 1080x1920（安全区：内容右缘≤950 / 下界≤1590）
- 小红书 封面+正文图4 1080x1440
蓝系家族，主色深蓝禁换色相。质量闸：尺寸 + 四角蓝系。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解/子任务S1-志愿顺序"

def font(sz, bold=True):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

def base(w, h, TOP=(18,74,128), BOT=(6,16,42)):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32)*(1-y) + np.array(BOT, np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.22, h*0.12
    radial = np.exp(-(((xx-gx)/(w*0.5))**2 + ((yy-gy)/(h*0.3))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.30*radial[..., None]
    for k in (0.35, 0.9):
        u = (xx - k*yy)/w
        beam = np.exp(-(u-0.10)**2/(2*0.05**2))
        img += glow*0.10*beam[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def open_(w, h):
    return ImageDraw.Draw(Image.fromarray(base(w, h), "RGB"))

def badge(d, x, y, text, fs):
    f = font(fs)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, fill=(8,30,64))
    d.rounded_rectangle([x-8, y-3, x+tw+10, y+int(fs*1.5)], radius=9, outline=(120,165,225), width=2)
    d.text((x, y), text, font=f, fill=(205,228,255))

def mt(d, xy, lines, fs, fill=(255,255,255), lh=1.25, anchor="la", align="left"):
    f = font(fs)
    d.multiline_text(xy, "\n".join(lines), font=f, fill=fill, anchor=anchor, spacing=int(fs*lh-fs), align=align)

def hline(d, x0, x1, y, color=(120,165,225), wdt=2):
    d.line([x0, y, x1, y], fill=color, width=wdt)

def check(path, w, h):
    im = Image.open(path).convert("RGB")
    assert im.size == (w, h), f"{path} {im.size}!={w}x{h}"
    px = im.load(); blue = 0
    for cx, cy in [(3,3),(w-4,3),(3,h-4),(w-4,h-4)]:
        r, g, b = px[cx, cy]
        blue += int(b > r+8 and b > g+6)
    assert blue >= 3, f"{path} blue {blue}/4"
    print("OK", path.split('/')[-1])

# ---------- 横向封面 ----------
def cover_gzh():
    img = Image.fromarray(base(900,383)); d = ImageDraw.Draw(img)
    badge(d, 56, 46, "深圳中考 · 志愿顺序 P1-4 S1", 22)
    mt(d, (56, 150), ["志愿顺序填错，", "分高也白搭"], 52, fill=(255,255,255))
    d.text((60, 296), "想去的学校 · 放第1志愿", font=font(30), fill=(255,210,120))
    p = f"{BASE}/P1-4-S1-志愿顺序-公众号-封面-精炼版-900x383.png"; img.save(p); check(p,900,383)

def cover_tt(i, title, sub1, sub2):
    img = Image.fromarray(base(1200,900)); d = ImageDraw.Draw(img)
    badge(d, 72, 68, "深圳中考 · 志愿顺序", 30)
    mt(d, (72, 260), title, 62, fill=(255,255,255), lh=1.18)
    d.text((76, 700), sub1, font=font(48), fill=(255,210,120))
    d.text((76, 780), sub2, font=font(34), fill=(150,185,235))
    d.text((76, 870), "HSEE · 模拟志愿填报  亲手排一次", font=font(26), fill=(120,155,210))
    p = f"{BASE}/P1-4-S1-志愿顺序-头条-封面{i}-1200x900.png"; img.save(p); check(p,1200,900)

# ---------- 抖音分镜（竖） ----------
def dy_shot(n, big, card, safe=(950,1590)):
    img = Image.fromarray(base(1080,1920)); d = ImageDraw.Draw(img)
    badge(d, 60, 90, "深圳中考 · 志愿顺序", 30)
    mt(d, (60, 300), big, 66, fill=(255,255,255), lh=1.18)
    hline(d, 62, 1018, 760)
    mt(d, (60, 810), card, 44, fill=(205,228,255), lh=1.3)
    d.text((60, 1500), f"{n:02d} / 06", font=font(40), fill=(120,160,215))
    p = f"{BASE}/P1-4-S1-志愿顺序-抖音-镜头{n:02d}-1080x1920.png"; img.save(p); check(p,1080,1920)

# ---------- 小红书（竖 1080x1440） ----------
def xhs_cover():
    img = Image.fromarray(base(1080,1440)); d = ImageDraw.Draw(img)
    badge(d, 60, 90, "深圳中考 · 志愿顺序", 32)
    mt(d, (60, 420), ["想去的学校", "放第1志愿"], 88, fill=(255,255,255), lh=1.16)
    hline(d, 62, 1018, 950)
    mt(d, (60, 1000), ["600分也可能败给599分", "——不是分数，是顺序"], 40, fill=(255,210,120), lh=1.35)
    d.text((60, 1330), "收藏这张顺序表 · 填志愿前看一遍", font=font(32), fill=(150,185,235))
    p = f"{BASE}/P1-4-S1-志愿顺序-小红书-封面-1080x1440.png"; img.save(p); check(p,1080,1440)

def xhs_card(i, title, body, extra=None):
    img = Image.fromarray(base(1080,1440)); d = ImageDraw.Draw(img)
    badge(d, 60, 90, "深圳中考 · 志愿顺序", 30)
    mt(d, (60, 260), title, 62, fill=(255,255,255), lh=1.2)
    hline(d, 62, 1018, 640)
    mt(d, (60, 700), body, 42, fill=(205,228,255), lh=1.45)
    if extra:
        d.text((60, 1330), extra, font=font(32), fill=(255,210,120))
    p = f"{BASE}/P1-4-S1-志愿顺序-小红书-正文图{i}-1080x1440.png"; img.save(p); check(p,1080,1440)

if __name__ == "__main__":
    cover_gzh()
    cover_tt(1, ["600 分，", "败给 599 分？"], "深圳投档8字：分数优先·志愿顺序", "志愿是排序表，不是省分表")
    cover_tt(2, ["超常发挥够名校，", "却被保底校录走"], "2025 真实：第1志愿填保底 → 后面全作废", "每年都有 · 顺序检索即录")
    cover_tt(3, ["最想去的学校，", "放第 1 志愿"], "按喜欢程度，从高到低排", "冲·稳·保·底 拉开梯度 · 保底放最后")
    dy_shot(1, ["600分，败给了", "599分"], ["不是分数", "是志愿顺序填反了"])
    dy_shot(2, ["深圳投档", "就8个字"], ["分数优先", "依照志愿顺序"])
    dy_shot(3, ["不是第1志愿", "有加分"], ["系统从上到下检索", "第1个有空位就录你"])
    dy_shot(4, ["想去的放第2", "= 白搭"], ["第1检索到保底校", "直接录取你"])
    dy_shot(5, ["每年都有人", "吃这个亏"], ["超常发挥够名校", "却被保底校录走"])
    dy_shot(6, ["把最想去的", "放最前"], ["志愿是排序表", "不是省分表"])
    xhs_cover()
    xhs_card(1, ["600 去 B · 599 进 A", "分数更高反而吃亏"], ["小刚600：第1志愿B校 → 录B", "小芳599：第1志愿A校 → 录A", "", "原因：系统先按你第1志愿检索", "第1个有空位的学校就录取你"])
    xhs_card(2, ["不是第1志愿有加分", "是顺序检索"], ["你填的第1志愿，第一个被检索", "它有空位，你直接进；没空位才", "看第2、第3…", "", "想去的学校不放前面", "分再高也轮不到它"])
    xhs_card(3, ["第1志愿别填保底"], ["孩子超常发挥、够上更好的学校", "却因第1志愿填了保底", "被直接录走 → 后面全作废", "", "保底校只放最后1-2个"], extra="每年都有人吃这个亏")
    xhs_card(4, ["正确排法", "一张图记住"], ["① 最想去的学校放第1志愿", "② 按喜欢程度从高到低排", "③ 梯度：冲→稳→保→底 拉开", "", "一句话：志愿是排序表，不是省分表"], extra="收藏这篇 · 填志愿前看一遍")
