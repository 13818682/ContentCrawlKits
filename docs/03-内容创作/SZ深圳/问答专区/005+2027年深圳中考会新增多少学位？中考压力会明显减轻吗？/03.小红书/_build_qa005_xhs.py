# -*- coding: utf-8 -*-
"""
QA-005 小红书 图文（封面 + 正文图3）1080×1440
规范来源：P1-4 S1《_build_p14_s1_all.py》小红书段（2026-09-09 定）
- cobalt 档 TOP(18,74,128) → BOT(6,16,42)；左上主光 + 两道斜光束（蓝系家族，禁换色相）
- 版式：左上徽章胶囊 → 大字标题 → 分隔线 → 正文块 → 底部金色/浅蓝条
内容：十五五新建/扩建学校数 + 各校学位数 + 总数（可截图收藏）
质量闸：尺寸断言 + 四角蓝系断言 + 文本越界断言 + 元素重叠/空档断言
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
OUT = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/问答专区/"
       "005+2027年深圳中考会新增多少学位？中考压力会明显减轻吗？/03.小红书/")

ISSUES = []


def font(sz, bold=True):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc",
              r"C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def base(w, h, TOP=(18, 74, 128), BOT=(6, 16, 42)):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32) * (1 - y) + np.array(BOT, np.float32) * y)[:, None, :]
    xx = np.arange(w)[None, :]
    yy = np.arange(h)[:, None]
    gx, gy = w * 0.22, h * 0.12
    radial = np.exp(-(((xx - gx) / (w * 0.5)) ** 2 + ((yy - gy) / (h * 0.3)) ** 2))
    glow = np.array([255, 255, 255], np.float32)[None, None, :]
    img = grad + glow * 0.30 * radial[..., None]
    for k in (0.35, 0.9):
        u = (xx - k * yy) / w
        beam = np.exp(-(u - 0.10) ** 2 / (2 * 0.05 ** 2))
        img += glow * 0.10 * beam[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)


GOLD_BRAND = (255, 210, 120)


def brand(d, y, fs, topic="未来学位", topic_fs=None):
    """品牌行（2026-09-12 用户规则）：「深圳中考」用大字金字，手机缩略图上一眼可辨；
    主题标签退到右侧小字。原实现是 32px 小胶囊（占画布 3%，手机上约 11px，不可读）。"""
    f = font(fs)
    d.text((60, y), "深圳中考", font=f, fill=GOLD_BRAND, anchor="la")
    bb = d.textbbox((60, y), "深圳中考", font=f, anchor="la")
    tf = font(topic_fs or int(fs * 0.55))
    d.text((W - 60, bb[3] - int(fs * 0.28)), topic, font=tf, fill=(196, 220, 250), anchor="rs")
    if bb[2] > W - 20:
        ISSUES.append(f"品牌字越界 right={bb[2]:.0f}")


def mt(d, xy, lines, fs, fill=(255, 255, 255), lh=1.25, tag=""):
    f = font(fs)
    d.multiline_text(xy, "\n".join(lines), font=f, fill=fill, anchor="la",
                     spacing=int(fs * lh - fs), align="left")
    for ln in lines:
        bb = d.textbbox(xy, ln, font=f)
        if bb[2] > W - 40:
            ISSUES.append(f"越界 [{tag}] right={bb[2]:.0f} 「{ln[:18]}」")
    # 按字体行高推算文本块真实上下界（textbbox 返回的是绝对坐标，不可再加 xy[1]）
    asc, desc = f.getmetrics()
    lh_px = asc + desc + int(fs * lh - fs)
    top = xy[1]
    bot = xy[1] + (len(lines) - 1) * lh_px + asc + desc
    if bot > H - 20:
        ISSUES.append(f"越界(下) [{tag}] block bottom={bot:.0f}")
    return (top, bot)


def hline(d, x0, x1, y, color=(120, 165, 225), wdt=2):
    d.line([x0, y, x1, y], fill=color, width=wdt)


def one(d, xy, text, fs, fill=(255, 255, 255), bold=True, tag=""):
    f = font(fs, bold) if bold else ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", fs)
    d.text(xy, text, font=f, fill=fill, anchor="la")
    bb = d.textbbox(xy, text, font=f)
    if bb[2] > W - 40:
        ISSUES.append(f"越界 [{tag}] right={bb[2]:.0f} 「{text[:18]}」")
    if bb[3] > H - 20:
        ISSUES.append(f"越界(下) [{tag}] bottom={bb[3]:.0f}")
    return bb


def check(path):
    im = Image.open(path).convert("RGB")
    assert im.size == (W, H), f"{path} {im.size} != {W}x{H}"
    px = im.load()
    blue = 0
    for cx, cy in [(3, 3), (W - 4, 3), (3, H - 4), (W - 4, H - 4)]:
        r, g, b = px[cx, cy]
        blue += int(b > r + 8 and b > g + 6)
    assert blue >= 3, f"{path} 四角蓝系不足 {blue}/4"
    print("OK", path.split("/")[-1], f"corner-blue {blue}/4")


# ── 封面 ──
def xhs_cover():
    img = Image.fromarray(base(W, H), "RGB")
    d = ImageDraw.Draw(img)
    brand(d, 74, 64)
    bb1 = mt(d, (60, 400), ["未来五年，深圳", "要建多少所高中？"], 96, fill=(255, 255, 255), lh=1.16, tag="cv-title")
    hline(d, 62, 1018, 940)
    bb2 = mt(d, (60, 990), ["新建 10 所 · 改扩建超 10 所", "规划新增学位 10 万个以上"], 42,
             fill=(255, 210, 120), lh=1.35, tag="cv-sub")
    d.text((60, 1330), "收藏这份学位清单 · 数据持续更新",
           font=font(32), fill=(150, 185, 235))
    # 间距断言
    if bb1[1] < 330:
        ISSUES.append("封面标题过高（可能压到品牌行）")
    if bb2[0] < 950 - 40:
        ISSUES.append(f"封面副题与分隔线间距不足 ({950 - bb2[0]:.0f}px)")
    p = OUT + "QA-005-未来学位-小红书-封面-1080x1440.png"
    img.save(p)
    check(p)


# ── 正文图 ──
def xhs_card(n, fname, title, body, extra=None, body_fs=42, body_lh=1.45, y_body=700):
    img = Image.fromarray(base(W, H), "RGB")
    d = ImageDraw.Draw(img)
    brand(d, 92, 38)
    bb = mt(d, (60, 250), title, 62, fill=(255, 255, 255), lh=1.2, tag=f"c{n}-title")
    hline(d, 62, 1018, 630)
    tb = mt(d, (60, y_body), body, body_fs, fill=(205, 228, 255), lh=body_lh, tag=f"c{n}-body")
    if extra:
        d.text((60, 1330), extra, font=font(32), fill=(255, 210, 120))
    if y_body < 690:
        ISSUES.append(f"c{n} 正文起始过高")
    if tb[1] > 1300:
        ISSUES.append(f"c{n} 正文底部 {tb[1]:.0f} 压到底部条 (1300)")
    if bb[1] < 230:
        ISSUES.append(f"c{n} 标题压到品牌行")
    p = OUT + fname
    img.save(p)
    check(p)


if __name__ == "__main__":
    xhs_cover()

    xhs_card(1, "QA-005-未来学位-小红书-正文图1-新建10所-1080x1440.png",
             ["新建 10 所公办高中", "学位数清单"],
             ["招标方案 4 所 · 合计 10800",
              "39高南山2400 ｜ 40高坪山1800",
              "45高宝安4800 ｜ 46高光明1800",
              "",
              "第五座高中园 · 大鹏溪涌",
              "42高2550 ｜ 43高3000 ｜ 44高3000",
              "三校合计 8550（媒体披露）",
              "",
              "41高 · 47高 · 48高 尚未公布"],
             body_fs=36, body_lh=1.40,
             extra="招标方案 10800 + 媒体披露 8550")

    xhs_card(2, "QA-005-未来学位-小红书-正文图2-改扩建超10所-1080x1440.png",
             ["改扩建 超过 10 所", "老学校也在长大"],
             ["深中泥岗 · 深实验 · 深高中心校区",
              "宝中集团 · 深大附中 · 深二实",
              "翠园本部 · 罗湖高中 · 平冈 · 深二外",
              "",
              "目前唯一公布学位数的：",
              "深二外 —— 3年新增 1200 座"],
             extra="三大高中园首次进入改扩建程序")

    xhs_card(3, "QA-005-未来学位-小红书-正文图3-总数10万个以上-1080x1440.png",
             ["总数：10 万个以上", "五年全口径规划目标"],
             ["十五五（2026—2030）",
              "规划新增公办高中学位",
              "10 万个以上",
              "",
              "注意：这是五年全口径总数",
              "不等于「10 所新校」的学位数"],
             extra="别把「10 万」和「10 所」混着算")

    xhs_card(4, "QA-005-未来学位-小红书-正文图4-但2027届赶不上-1080x1440.png",
             ["但 2027 届", "赶不上这批学位"],
             ["推进最快的仍在设计 / 可研阶段",
              "改扩建竣工多在 2027 年之后",
              "",
              "新建校从可研到开学，一般还要几年",
              "2027 届该盯的，仍是现有学校分数线"],
             extra="未来是美好的，现在还不能松懈")

    if ISSUES:
        for s in ISSUES:
            print("!!", s)
        raise SystemExit(f"校验未通过：{len(ISSUES)} 处")
    print("PASS · 越界/重叠/空档 全部通过")
