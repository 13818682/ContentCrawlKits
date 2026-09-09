# -*- coding: utf-8 -*-
"""
统一重渲 P1-4 五张公众号封面 900x383（主线+S1~S4）
版式（动态链式、绝无重叠）：
  角标(y24-54) → 大标题(白·单行·自适应放大，la起笔) → [可选副题] → 底部金钩子
钩子固定贴底，字块自上而下依次排列，间距用实测 bbox 保证。
各单元沿用其蓝系档位。质量闸：宽度≤右缘、字块不相交、四角蓝系。
"""
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def save_img(img, out, tries=5):
    for i in range(tries):
        try:
            img.save(out)
            return
        except OSError:
            time.sleep(0.6)
    raise OSError(f"save failed after {tries} tries: {out}")

def font(sz):
    for p in [r"C:/Windows/Fonts/msyhbd.ttc", r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def base(w, h, TOP, BOT):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32)*(1-y) + np.array(BOT, np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.5, h*0.08
    radial = np.exp(-(((xx-gx)/(w*0.55))**2 + ((yy-gy)/(h*0.34))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.32*radial[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

W, H = 900, 383
X0 = 56
MAXW = 792

def tlen(text, f):
    return ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f)

def fit(text, start=96, minimum=40, cap=MAXW):
    s = start
    while s >= minimum:
        f = font(s)
        if tlen(text, f) <= cap:
            return s, f
        s -= 2
    return minimum, font(minimum)

def badge(d, text):
    f = font(21)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([X0-8, 24, X0+tw+12, 52], radius=9, fill=(6,18,44),
                        outline=(120,165,225), width=2)
    d.text((X0, 27), text, font=f, fill=(205,228,255))

def box(text, f, y):
    return d.textbbox((X0, y), text, font=f, anchor="la")

def _box(text, f, y):
    return d.textbbox((X0, y), text, font=f, anchor="la")

def render(out, TOP, BOT, badge_txt, primary, secondary, hook):
    global d
    img = Image.fromarray(base(W, H, TOP, BOT)); d = ImageDraw.Draw(img)
    badge(d, badge_txt)
    f2 = font(32)

    def plan(ps):
        """试排：返回布局，ps=大标题字号；竖直不可行返回 None。
        钩子不贴底：紧接上一字块下方固定间距（主标题/副题之后），下方留白。"""
        pf = font(ps)
        if tlen(primary, pf) > MAXW:
            return None
        yp = 128
        pb = _box(primary, pf, yp)
        ys = sb = None
        if secondary:
            ys = pb[3] + 16
            sb = _box(secondary, f2, ys)
            if sb[3] > H - 120:      # 副题过低下压
                return None
        prev_bottom = sb[3] if secondary else pb[3]
        yh = int(prev_bottom + (30 if secondary else 52))   # 靠近白题句，留呼吸
        # 钩子字号：先满足宽度，再按竖直空间缩小，保证底缘 ≤ H-18
        hb = None
        for s in range(40, 17, -2):
            fk = font(s)
            if tlen(hook, fk) > MAXW:
                continue
            b = _box(hook, fk, yh)
            if b[3] <= H - 18:
                hb = b
                hk = fk
                break
        if hb is None:
            return None
        return dict(pf=pf, yp=yp, pb=pb, ys=ys, sb=sb, yh=yh, hk=hk, hb=hb)

    chosen = None
    for ps in range(100, 43, -2):
        chosen = plan(ps)
        if chosen:
            break
    assert chosen, f"找不到可行大标题字号: {primary} / {secondary}"
    # ---- 落笔 ----
    d.text((X0, chosen["yp"]), primary, font=chosen["pf"], fill=(255,255,255), anchor="la")
    if secondary:
        d.text((X0, chosen["ys"]), secondary, font=f2, fill=(200,222,250), anchor="la")
    d.text((X0, chosen["yh"]), hook, font=chosen["hk"], fill=(255,210,120), anchor="la")
    pb, sb, hb = chosen["pb"], chosen["sb"], chosen["hb"]
    # ---- 断言 ----
    assert pb[2] <= W-20 and hb[2] <= W-20 and hb[3] <= H-18
    if secondary:
        assert sb[1] - pb[3] >= 8 and hb[1] - sb[3] >= 24
    else:
        assert hb[1] - pb[3] >= 44   # 黄钩紧贴白题句下方（接近、不贴底）
    save_img(img, out)
    # 角蓝
    im = Image.open(out).convert("RGB"); px = im.load(); nb = 0
    for cx, cy in [(3,3),(W-4,3),(3,H-4),(W-4,H-4)]:
        r, g, b = px[cx, cy]; nb += int(b > r+8 and b > g+6)
    assert nb >= 3
    print("OK", out.split('/')[-1], f"主标题字号 {ps}px")

ROOT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解"
UNITS = {
  "主线完整版": dict(TOP=(27,58,92), BOT=(8,18,40), badge="深圳中考 · 投档规则 P1-4",
      primary="深圳中考怎么录取？", secondary="五批次 · 投档规则一次讲清",
      hook="前批一录 · 后批全作废（不退档不转录）"),
  "子任务S1-志愿顺序": dict(TOP=(18,74,128), BOT=(6,16,42), badge="深圳中考 · 志愿顺序 S1",
      primary="志愿顺序填错，分高也白搭", secondary=None,
      hook="想去的学校 · 放第 1 志愿"),
  "子任务S2-同分PK": dict(TOP=(46,78,132), BOT=(10,20,44), badge="深圳中考 · 同分规则 S2",
      primary="中考同分先比生地", secondary="不是先比语数英",
      hook="生地：初二就定下的隐形分"),
  "子任务S3-四个投档错误自查": dict(TOP=(14,32,66), BOT=(5,10,24), badge="深圳中考 · 志愿自查 S3",
      primary="12个志愿全填一个分段？", secondary=None,
      hook="冲稳保底 · 拉开梯度"),
  "子任务S4-走读调剂与保存确认": dict(TOP=(22,62,122), BOT=(6,15,36), badge="深圳中考 · 操作提醒 S4",
      primary="走读该不该勾？保存≠确认", secondary=None,
      hook="单程45分钟内才勾 · 填完记得点确认"),
}
if __name__ == "__main__":
    for u, cfg in UNITS.items():
        name = "P1-4-主线完整版-公众号-封面-精炼版-900x383.png" if u == "主线完整版" else \
               ("P1-4-S1-志愿顺序-公众号-封面-精炼版-900x383.png" if "S1" in u else
                "P1-4-S2-同分PK-公众号-封面-精炼版-900x383.png" if "S2" in u else
                "P1-4-S3-四错自查-公众号-封面-精炼版-900x383.png" if "S3" in u else
                "P1-4-S4-走读调剂保存-公众号-封面-精炼版-900x383.png")
        out = f"{ROOT}/{u}/01.公众号/{name}"
        render(out, cfg["TOP"], cfg["BOT"], cfg["badge"], cfg["primary"], cfg["secondary"], cfg["hook"])
