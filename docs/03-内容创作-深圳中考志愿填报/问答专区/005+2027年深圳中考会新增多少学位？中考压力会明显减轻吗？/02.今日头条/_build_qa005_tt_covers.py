# -*- coding: utf-8 -*-
"""
QA-005 今日头条 3 图封面 1200×900
规范来源：P1-4 主线完整版《_build_p14_mainline_covers.py》（2026-09-09 定）
- navy 档 TOP(27,58,92) → BOT(8,18,40)；顶部偏中径向光 + 两道自上而下斜光
- 版式：左上徽章胶囊 + 左对齐大字主标题 + 金色副题 + 浅蓝补充行 + 底部行动条
质量闸：尺寸断言 + 四角蓝系占比断言 + 文本越界断言 + 元素间距断言
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 900
OUT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/问答专区/"
       "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？/02.今日头条/")

ISSUES = []


def font(sz, bold=True):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc",
              r"C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def base(w, h, TOP=(27, 58, 92), BOT=(8, 18, 40)):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32) * (1 - y) + np.array(BOT, np.float32) * y)[:, None, :]
    xx = np.arange(w)[None, :]
    yy = np.arange(h)[:, None]
    radial = np.exp(-(((xx - w * 0.50) / (w * 0.55)) ** 2 + ((yy - h * 0.10) / (h * 0.30)) ** 2))
    glow = np.array([255, 255, 255], dtype=np.float32)[None, None, :]
    img = grad + glow * 0.28 * radial[..., None]
    for k in (0.45, 1.1):
        u = (xx - k * yy) / w
        beam = np.exp(-(u - 0.15) ** 2 / (2 * 0.05 ** 2))
        img += glow * 0.10 * beam[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)


def badge(d, x, y, text, fnt):
    tw = d.textlength(text, font=fnt)
    d.rounded_rectangle([x - 8, y - 4, x + tw + 10, y + int(fnt.size * 1.5)], radius=8, fill=(10, 30, 62))
    d.rounded_rectangle([x - 8, y - 4, x + tw + 10, y + int(fnt.size * 1.5)], radius=8,
                        outline=(110, 150, 215), width=2)
    d.text((x, y), text, font=fnt, fill=(200, 222, 255))
    if x + tw + 10 > W - 10:
        ISSUES.append(f"徽章越界 right={x + tw + 10:.0f}")


def render(path, badge_text, title_lines, sub_lines, tag=""):
    arr = base(W, H)
    img = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(img)
    drawn = []

    badge(d, int(W * 0.06), int(H * 0.075), badge_text, font(30))

    big = font(int(W * 0.075))           # 90px
    y0 = int(H * 0.24)
    XT = W * 0.06
    for i, line in enumerate(title_lines):
        yy = y0 + i * int(big.size * 1.28)
        if isinstance(line, (list, tuple)):      # 分段着色：[(文字, 颜色), ...]
            xx = XT
            for seg, col in line:
                d.text((xx, yy), seg, font=big, fill=col, anchor="la")
                xx += d.textlength(seg, font=big)
            full = "".join(t for t, _ in line)
        else:
            d.text((XT, yy), line, font=big, fill=(255, 255, 255), anchor="la")
            full = line
        bb = d.textbbox((XT, yy), full, font=big)
        if bb[2] > W - 40:
            ISSUES.append(f"越界 [{tag}] title{i} right={bb[2]:.0f} > {W - 40} 「{full}」")
        drawn.append((f"title{i}", bb))

    # 副题（金色）
    subf = font(int(W * 0.042))          # 50px
    y_sub = int(H * 0.55)
    d.text((W * 0.062, y_sub), sub_lines[0], font=subf, fill=(255, 210, 120), anchor="la")
    bb = d.textbbox((W * 0.062, y_sub), sub_lines[0], font=subf)
    if bb[2] > W - 40:
        ISSUES.append(f"越界 [{tag}] sub right={bb[2]:.0f} 「{sub_lines[0]}」")
    drawn.append(("sub", bb))

    # 补充行（浅蓝）
    sm = font(int(W * 0.033))            # 39px
    for j, s in enumerate(sub_lines[1:], start=1):
        yy = y_sub + j * int(W * 0.058)
        d.text((W * 0.062, yy), s, font=sm, fill=(150, 180, 225), anchor="la")
        bb = d.textbbox((W * 0.062, yy), s, font=sm)
        if bb[2] > W - 40:
            ISSUES.append(f"越界 [{tag}] sub{j} right={bb[2]:.0f} 「{s}」")
        drawn.append((f"sub{j}", bb))

    # 底部行动条
    d.text((W * 0.06, H * 0.925), "HSEE · 模拟志愿填报  亲手排一次",
           font=font(int(W * 0.026)), fill=(120, 150, 200), anchor="la")

    # 间距断言
    for i in range(len(drawn) - 1):
        (na, ba), (nb, bb2) = drawn[i], drawn[i + 1]
        ox = min(ba[2], bb2[2]) - max(ba[0], bb2[0])
        oy = min(ba[3], bb2[3]) - max(ba[1], bb2[1])
        if ox > 2 and oy > 2:
            ISSUES.append(f"重叠 [{tag}] {na} × {nb}")
        elif ox > 2 and -oy > int(H * 0.08):   # 空档阈值按画布高度 8% 计
            ISSUES.append(f"空档过大 [{tag}] {na}→{nb} = {-oy:.0f}px (>{int(H * 0.08)})")

    img.save(path)
    print("saved", path.split("/")[-1], img.size)


def check(path):
    im = Image.open(path).convert("RGB")
    assert im.size == (W, H), f"{path} {im.size} != {W}x{H}"
    px = im.load()
    blue = 0
    for cx, cy in [(3, 3), (W - 4, 3), (3, H - 4), (W - 4, H - 4)]:
        r, g, b = px[cx, cy]
        blue += int(b > r + 10 and b > g + 8)
    assert blue >= 3, f"{path} 四角蓝系不足 {blue}/4"
    print(f"OK {path.split('/')[-1]} corner-blue {blue}/4")


JOBS = [
    ("今日头条-封面1-主标题-1200x900.png",
     "深圳中考 · 未来学位",
     ["未来五年，深圳规划新增", [("公办高中学位", (255, 255, 255)), ("10万个以上", (255, 210, 120))]],
     ["新建10所 · 改扩建10余所"], "c1"),
    ("今日头条-封面2-数据对撞-1200x900.png",
     "深圳中考 · 未来学位",
     ["一边是10所新高中", "一边是10余所老校扩容"],
     ["新增公办高中学位10万个以上", "已公开：39高2400 · 40高1800 · 45高4800 · 46高1800"], "c2"),
    ("今日头条-封面3-答案行动-1200x900.png",
     "深圳中考 · 未来学位",
     ["但这些学位", "2027届赶不上"],
     ["推进最快的仍在设计或可研阶段", "守住校内排名 · 盯紧名额分配 · 排好志愿梯度"], "c3"),
]

if __name__ == "__main__":
    for name, bd, tl, sl, tg in JOBS:
        render(OUT + name, bd, tl, sl, tg)
    for name, *_ in JOBS:
        check(OUT + name)
    if ISSUES:
        for s in ISSUES:
            print("!!", s)
        raise SystemExit(f"校验未通过：{len(ISSUES)} 处")
    print("PASS · 越界/重叠/空档 全部通过")
