# -*- coding: utf-8 -*-
"""
统一重渲 P1-4 全部 今日头条 封面 1200x900 ×15（主线+S1~S4 各3）
版式：角标 → 白色大标题(≤2行·按宽度自适放大·统一字号) → 黄色钩子(紧贴其下 56px)
整块垂直居中；断言：各行不越右界、标题↔钩子间距、钩子不触底。
各单元沿用蓝系档位。无网格。
"""
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def font(sz):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

MEAS = ImageDraw.Draw(Image.new("RGB", (6, 6)))

def base(w, h, TOP, BOT):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32)*(1-y) + np.array(BOT, np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.5, h*0.10
    radial = np.exp(-(((xx-gx)/(w*0.6))**2 + ((yy-gy)/(h*0.32))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.30*radial[..., None]
    for k in (0.4, 1.0):
        img += glow*0.08*np.exp(-(((xx-k*yy)/w)-0.12)**2/(2*0.06**2))[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def tlen(text, f):
    return MEAS.textlength(text, font=f)

def mbox(text, f, y):
    return MEAS.textbbox((X0, y), text, font=f, anchor="la")

W, H = 1200, 900
X0 = 80
CAPW = 1040

def badge(d, text):
    f = font(30)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([X0-10, 56, X0+tw+16, 100], radius=12, fill=(6,18,44),
                        outline=(130,175,235), width=3)
    d.text((X0, 60), text, font=f, fill=(210,232,255))

def save_img(img, out, tries=5):
    for i in range(tries):
        try:
            img.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)

def render(out, TOP, BOT, badge_txt, title, hook):
    """title: 白字行列表(≤2)；hook: 黄色一行。动态：先按宽定字号，再垂直居中试排。"""
    img = Image.fromarray(base(W, H, TOP, BOT)); d = ImageDraw.Draw(img)
    badge(d, badge_txt)
    # 1) 大标题字号：各行宽度都 ≤ CAPW，取最大可行（≥48）
    fs = None; f = None
    for s in range(122, 47, -2):
        ff = font(s)
        if max(tlen(ln, ff) for ln in title) <= CAPW:
            fs, f = s, ff
            break
    assert fs, "大标题无可行字号"
    # 2) 黄钩字号（≤46 且宽度 ≤ CAPW）
    hk = None; hf = None
    for s in range(46, 19, -2):
        ff = font(s)
        if tlen(hook, ff) <= CAPW:
            hk, hf = s, ff
            break
    assert hk
    # 3) 垂直试排：块高度估算→居中；校验钩子底 ≤ H-36
    line_h = int(fs*1.34)
    block_est = line_h*len(title) + 56 + int(hk*1.6)
    y0 = (H - block_est)//2 - int(fs*0.25)
    if y0 < 130:
        y0 = 130
    ys = [y0 + i*line_h for i in range(len(title))]
    tb = max(mbox(ln, f, ys[i])[3] for i, ln in enumerate(title))
    yh = tb + 56
    hb = mbox(hook, hf, yh)
    assert hb[3] <= H-30, f"钩子触底 {hb}"
    # 4) 落笔
    for ln, yy in zip(title, ys):
        d.text((X0, yy), ln, font=f, fill=(255,255,255), anchor="la")
    d.text((X0, yh), hook, font=hf, fill=(255,210,120), anchor="la")
    # 5) 断言
    for ln, yy in zip(title, ys):
        bb = mbox(ln, f, yy)
        assert bb[2] <= W-20, f"标题越界 {bb} {ln}"
    assert mbox(hook, hf, yh)[2] <= W-20
    assert mbox(hook, hf, yh)[1] - tb >= 40, "黄钩离标题过近"
    save_img(img, out)
    im = Image.open(out).convert("RGB"); px = im.load(); nb = 0
    for cx, cy in [(3,3),(W-4,3),(3,H-4),(W-4,H-4)]:
        r, g, b = px[cx, cy]; nb += int(b > r+8 and b > g+6)
    assert nb >= 3
    print("OK", out.split('/')[-1], f"标题字号 {fs}px · 钩子 {hk}px")

ROOT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解"
PAL = {
  "主线完整版": dict(TOP=(27,58,92), BOT=(8,18,40), badge="深圳中考 · 投档规则 P1-4"),
  "子任务S1-志愿顺序": dict(TOP=(18,74,128), BOT=(6,16,42), badge="深圳中考 · 志愿顺序 S1"),
  "子任务S2-同分PK": dict(TOP=(46,78,132), BOT=(10,20,44), badge="深圳中考 · 同分规则 S2"),
  "子任务S3-四个投档错误自查": dict(TOP=(14,32,66), BOT=(5,10,24), badge="深圳中考 · 志愿自查 S3"),
  "子任务S4-走读调剂与保存确认": dict(TOP=(22,62,122), BOT=(6,15,36), badge="深圳中考 · 操作提醒 S4"),
}
COVERS = {
  "主线完整版": [
    ("P1-4-主线完整版-头条-封面1-主标题-1200x900.png",
     ["2026 深圳中考", "录取批次与投档规则全解"], "前批一录 · 后批全作废（不退档不转录）"),
    ("P1-4-主线完整版-头条-封面2-数据对撞-1200x900.png",
     ["600 分，败给 599 分？", "不是分数，是顺序"], "深圳投档8字：分数优先 · 志愿顺序"),
    ("P1-4-主线完整版-头条-封面3-答案行动-1200x900.png",
     ["想去的学校，放最前面", "志愿填完记得点确认"], "保存≠确认 · 截止 6月1日 18:00"),
  ],
  "子任务S1-志愿顺序": [
    ("P1-4-S1-志愿顺序-头条-封面1-主标题-1200x900.png",
     ["600 分，败给 599 分？"], "不是分数，是志愿顺序填反了"),
    ("P1-4-S1-志愿顺序-头条-封面2-真实案例-1200x900.png",
     ["超常发挥够名校，", "却被保底校录走"], "2025 真实：第1志愿填保底 → 后面全作废"),
    ("P1-4-S1-志愿顺序-头条-封面3-正确排法-1200x900.png",
     ["最想去的学校，", "放第 1 志愿"], "按喜欢程度从高到低排 · 保底放最后"),
  ],
  "子任务S2-同分PK": [
    ("P1-4-S2-同分PK-头条-封面1-主标题-1200x900.png",
     ["中考同分怎么比？", "先比生地，不是语数英"], "第1层生地合卷 · 第2层才比语数英"),
    ("P1-4-S2-同分PK-头条-封面2-案例-1200x900.png",
     ["生地98 vs 生地90", "同分先录98"], "580同分 · 语数英高10分也没用"),
    ("P1-4-S2-同分PK-头条-封面3-行动-1200x900.png",
     ["没考初二生地？", "别裸考"], "这是唯一初二就能锁定的分数"),
  ],
  "子任务S3-四个投档错误自查": [
    ("P1-4-S3-四错自查-头条-封面1-主标题-1200x900.png",
     ["12个志愿全填", "一个分段？"], "超常→更好的没报 · 失误→12个全灭"),
    ("P1-4-S3-四错自查-头条-封面2-案例-1200x900.png",
     ["考560浪费分", "考520直接全灭"], "2025真实：12志愿全落 · 补录民办"),
    ("P1-4-S3-四错自查-头条-封面3-自查4问-1200x900.png",
     ["4问自查", "填之前过一遍"], "占坑? 扎堆? 保底第1? 走读看通勤?"),
  ],
  "子任务S4-走读调剂与保存确认": [
    ("P1-4-S4-走读调剂保存-头条-封面1-主标题-1200x900.png",
     ["走读调剂该不该勾？", "先看三年通勤"], "2026新增 · 最多对4校勾"),
    ("P1-4-S4-走读调剂保存-头条-封面2-决策表-1200x900.png",
     ["一张表决定", "勾 or 不勾"], "≤30✅  30-45⚠️  >45❌  必须住宿绝不勾"),
    ("P1-4-S4-走读调剂保存-头条-封面3-保存确认-1200x900.png",
     ["保存 ≠ 确认", "别白填"], "2026最多3次确认 · 6月1日18:00截止"),
  ],
}
if __name__ == "__main__":
    for u, covers in COVERS.items():
        pal = PAL[u]
        for fn, title, hook in covers:
            out = f"{ROOT}/{u}/02.今日头条/{fn}"
            render(out, pal["TOP"], pal["BOT"], pal["badge"], title, hook)
