# -*- coding: utf-8 -*-
"""
P1-4 主线完整版 封面生成（navy 档：27,58,92 / 底 8,18,40；正中顶光）
- 公众号封面 900x383（精炼版）
- 头条 3 封面 1200x900（主标题 / 数据对撞 / 答案行动）
蓝系家族：主色深蓝，顶部「深圳中考」大字保留；数字≤2。
质量闸：尺寸断言 + 四角蓝系占比断言。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = None, None

def font(sz, bold=True):
    paths = [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc",
             r"C:/Windows/Fonts/simhei.ttf"]
    for p in paths:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()

def base(w, h, TOP=(27,58,92), BOT=(8,18,40)):
    """垂直渐变 + 顶部偏中径向光 + 两道斜光 + 细网点装饰。返回 RGB array。"""
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32)*(1-y) + np.array(BOT, np.float32)*y)[:, None, :]  # h,1,3
    xx = np.arange(w)[None, :]
    yy = np.arange(h)[:, None]
    gx, gy = w*0.50, h*0.10
    radial = np.exp(-(((xx-gx)/(w*0.55))**2 + ((yy-gy)/(h*0.30))**2))
    glow = np.array([255,255,255], dtype=np.float32)[None, None, :]
    img = grad + glow*0.28*radial[..., None]
    # 两道自上而下的斜光
    for k in (0.45, 1.1):
        u = (xx - k*yy)/w
        beam = np.exp(-(u-0.15)**2/(2*0.05**2))
        img += glow*0.10*beam[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def draw_text(d, xy, text, fnt, fill, anchor="la", spacing=6, align="left"):
    d.multiline_text(xy, text, font=fnt, fill=fill, anchor=anchor, spacing=spacing, align=align)

def badge(d, x, y, text, fnt):
    tw = d.textlength(text, font=fnt)
    d.rounded_rectangle([x-8, y-4, x+tw+10, y+int(fnt.size*1.5)], radius=8, fill=(10,30,62))
    d.rounded_rectangle([x-8, y-4, x+tw+10, y+int(fnt.size*1.5)], radius=8,
                        outline=(110,150,215), width=2)
    d.text((x, y), text, font=fnt, fill=(200,222,255))

def render(path, w, h, title_lines, sub_lines, accent_color=(255,210,120),
           badge_text="深圳中考 · 投档规则", top=None):
    arr = base(w, h, TOP=top or (27,58,92), BOT=(8,18,40))
    img = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(img)
    if w > h:  # 横版公众号 900x383
        badge(d, int(w*0.06), int(h*0.12), badge_text, font(22))
        big = font(int(h*0.19))
        subf = font(int(h*0.095))
        y0 = int(h*0.40)
        for i, line in enumerate(title_lines):
            draw_text(d, (w*0.06, y0+i*(int(h*0.19)*1.25)), line, big, (255,255,255), anchor="la")
        draw_text(d, (w*0.062, h*0.76), sub_lines[0], subf, accent_color, anchor="la")
    else:  # 竖版 1200x900 头条
        badge(d, int(w*0.06), int(h*0.075), badge_text, font(30))
        big = font(int(w*0.075))
        y0 = int(h*0.26)
        for i, line in enumerate(title_lines):
            draw_text(d, (w*0.06, y0+i*int(big.size*1.28)), line, big, (255,255,255), anchor="la")
        draw_text(d, (w*0.062, h*0.70), sub_lines[0], font(int(w*0.042)), accent_color, anchor="la")
        for j, s in enumerate(sub_lines[1:], start=1):
            draw_text(d, (w*0.062, h*0.70+j*int(w*0.058)), s, font(int(w*0.033)), (150,180,225), anchor="la")
        # 底部条
        draw_text(d, (w*0.06, h*0.925), "HSEE · 模拟志愿填报  亲手排一次", font(int(w*0.026)), (120,150,200), anchor="la")
    img.save(path)
    print("saved", path)

def check(path, w, h):
    im = Image.open(path).convert("RGB")
    assert im.size == (w, h), f"{path} size {im.size} != {w}x{h}"
    px = im.load()
    blue = 0
    for cx, cy in [(3,3),(w-4,3),(3,h-4),(w-4,h-4)]:
        r,g,b = px[cx,cy]
        blue += int(b > r+10 and b > g+8)
    assert blue >= 3, f"{path} 四角蓝系不足 {blue}/4"
    print(f"OK {path} {w}x{h} corner-blue {blue}/4")

if __name__ == "__main__":
    out = r"E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解/主线完整版"
    # 公众号封面 900x383
    render(f"{out}/P1-4-主线完整版-公众号-封面-精炼版-900x383.png", 900, 383,
           ["深圳中考怎么录取？", "五批次·投档规则一次讲清"],
           ["前批一录，后批全作废｜不退档不转录"])
    check(f"{out}/P1-4-主线完整版-公众号-封面-精炼版-900x383.png", 900, 383)
    # 头条 3 封面 1200x900
    render(f"{out}/P1-4-主线完整版-头条-封面1-主标题-1200x900.png", 1200, 900,
           ["2026 深圳中考", "录取批次与投档规则全解"],
           ["五批次先录谁·怎么录｜前批一录后批作废"])
    check(f"{out}/P1-4-主线完整版-头条-封面1-主标题-1200x900.png", 1200, 900)
    render(f"{out}/P1-4-主线完整版-头条-封面2-数据对撞-1200x900.png", 1200, 900,
           ["600 分 败给 599 分？", "不是分数，是顺序"],
           ["深圳投档就 8 个字：分数优先·志愿顺序", "2025 真实：565 够八大却被保底校录走"])
    check(f"{out}/P1-4-主线完整版-头条-封面2-数据对撞-1200x900.png", 1200, 900)
    render(f"{out}/P1-4-主线完整版-头条-封面3-答案行动-1200x900.png", 1200, 900,
           ["想去的学校，放最前面", "志愿填完记得点确认"],
           ["保存≠确认｜截止 6月1日 18:00", "用 HSEE 模拟志愿填报，亲手排一次"])
    check(f"{out}/P1-4-主线完整版-头条-封面3-答案行动-1200x900.png", 1200, 900)
