# -*- coding: utf-8 -*-
"""
QA-005 公众号首页图（规范来源：P1-4 主线完整版《_build_p14_mainline_covers.py》，2026-09-09 定）
- navy 档：TOP(27,58,92) → BOT(8,18,40)；顶部偏中径向光 + 两道自上而下斜光
- 版式：左上徽章胶囊 + 左对齐大字主标题（第二行数字用金色强调）+ 浅蓝副题（不用居中排版、不用 CTA 胶囊）
- 蓝系家族：主色深蓝，顶部「深圳中考」徽章保留；数字 ≤2 组
质量闸：尺寸断言 + 四角蓝系占比断言 + 文本越界断言 + 元素间距断言
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 383
OUT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/问答专区/"
       "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？/01.公众号/"
       "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？-公众号-封面-900x383.png")

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
    """垂直渐变 + 顶部偏中径向光 + 两道斜光"""
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


def guard(tag, d, xy, text, fnt):
    """越界断言：文本右边界必须留在画布安全区内"""
    x0, y0, x1, y1 = d.textbbox(xy, text, font=fnt)
    if x1 > W - 30:
        ISSUES.append(f"越界 [{tag}] right={x1:.0f} > {W - 30}  「{text}」")
    if y1 > H - 10:
        ISSUES.append(f"越界(下) [{tag}] bottom={y1:.0f} > {H - 10}")


def main():
    arr = base(W, H)
    img = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(img)

    badge(d, int(W * 0.06), int(H * 0.12), "深圳中考 · 问答005", font(22))

    big = font(int(H * 0.19))            # ≈72px
    subf = font(int(H * 0.095))          # ≈36px
    X = W * 0.06

    # 版式：按实测字框排布（72px 行占 [y+16,y+88]；36px 副题占 [y+10,y+45]）
    Y1, Y2, Y3 = 112, 196, 300
    drawn = []

    def line1(txt, x, y, fnt, fill, tag):
        d.text((x, y), txt, font=fnt, fill=fill, anchor="la")
        bb = d.textbbox((x, y), txt, font=fnt)
        if bb[2] > W - 30:
            ISSUES.append(f"越界 [{tag}] right={bb[2]:.0f} > {W - 30}  「{txt}」")
        if bb[3] > H - 10:
            ISSUES.append(f"越界(下) [{tag}] bottom={bb[3]:.0f}")
        return bb

    bb1 = line1("未来五年，深圳规划新增", X, Y1, big, (255, 255, 255), "title0")
    drawn.append(("title0", bb1))

    # 第二行分两段：白「公办高中学位」+ 金「10万个以上」（数字为视觉重点）
    t2a, t2b = "公办高中学位", "10万个以上"
    d.text((X, Y2), t2a, font=big, fill=(255, 255, 255), anchor="la")
    xa = X + d.textlength(t2a, font=big)
    d.text((xa, Y2), t2b, font=big, fill=(255, 210, 120), anchor="la")
    bb2 = d.textbbox((X, Y2), t2a + t2b, font=big)
    if bb2[2] > W - 30:
        ISSUES.append(f"越界 [title1] right={bb2[2]:.0f} > {W - 30}")
    if bb2[3] > H - 10:
        ISSUES.append(f"越界(下) [title1] bottom={bb2[3]:.0f}")
    drawn.append(("title1", bb2))

    sub = "2026—2030 · 覆盖五年全部新改扩建项目"
    bb3 = line1(sub, X + 2, Y3, subf, (157, 184, 212), "sub")
    drawn.append(("sub", bb3))

    # 重叠断言（同一 x 带内的相邻元素必须留出间隙）
    for i in range(len(drawn) - 1):
        (na, ba), (nb, bb2) = drawn[i], drawn[i + 1]
        ox = min(ba[2], bb2[2]) - max(ba[0], bb2[0])
        oy = min(ba[3], bb2[3]) - max(ba[1], bb2[1])
        if ox > 2 and oy > 2:
            ISSUES.append(f"重叠 {na} × {nb} (ox={ox:.0f}, oy={oy:.0f})")
        elif oy > -8:
            ISSUES.append(f"间距过窄 {na}→{nb} (间隙={-oy:.0f}px)")

    img.save(OUT)
    print("saved", OUT.split("/")[-1], img.size)

    # ── 质量闸 ──
    im = Image.open(OUT).convert("RGB")
    assert im.size == (W, H), f"size {im.size} != {W}x{H}"
    px = im.load()
    blue = 0
    for cx, cy in [(3, 3), (W - 4, 3), (3, H - 4), (W - 4, H - 4)]:
        r, g, b = px[cx, cy]
        blue += int(b > r + 10 and b > g + 8)
    assert blue >= 3, f"四角蓝系不足 {blue}/4"
    print(f"OK {W}x{H} corner-blue {blue}/4")

    if ISSUES:
        for s in ISSUES:
            print("!!", s)
        raise SystemExit(f"校验未通过：{len(ISSUES)} 处")
    print("PASS · 无越界 / 徽章在安全区")


if __name__ == "__main__":
    main()
