# -*- coding: utf-8 -*-
"""
统一紧凑重渲 P1-4 S1~S4 的 抖音6分镜(1080x1920) + 小红书封面/正文图4(1080x1440)。
排版（参考今日头条封面风格）：
  角标 → 白色大标题(自动放大) → 金色句紧贴其下(小间距) → 浅色要点行 → 顺排紧凑
垂直居中于内容区，行间/块间小间隙；断言：不越右界、文字块紧凑不重叠、下界安全。
抖音安全区：文字右缘≤960、内容底≤1570（底部留字幕）。
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
def tlen(t, f): return MEAS.textlength(t, font=f)
def mbox(t, f, y, x=70): return MEAS.textbbox((x, y), t, font=f, anchor="la")

WHITE = (255,255,255); GOLD = (255,210,120); LIGHT = (205,228,255)

def base(w, h, TOP, BOT):
    y = np.linspace(0, 1, h)[:, None]
    grad = (np.array(TOP, np.float32)*(1-y) + np.array(BOT, np.float32)*y)[:, None, :]
    xx = np.arange(w)[None, :]; yy = np.arange(h)[:, None]
    gx, gy = w*0.5, h*0.10
    radial = np.exp(-(((xx-gx)/(w*0.6))**2 + ((yy-gy)/(h*0.30))**2))
    glow = np.array([255,255,255], np.float32)[None, None, :]
    img = grad + glow*0.30*radial[..., None]
    for k in (0.4, 1.0):
        img += glow*0.08*np.exp(-(((xx-k*yy)/w)-0.12)**2/(2*0.06**2))[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def save_img(img, out):
    for i in range(6):
        try:
            img.save(out); return
        except OSError:
            time.sleep(0.6)
    raise OSError(out)

def fit_auto(text, start, mini, cap):
    s = start
    while s >= mini:
        f = font(s)
        if tlen(text, f) <= cap:
            return s, f
        s -= 2
    return mini, font(mini)

def stack_render(img, blocks, region_top, region_bottom, badge_txt, badge_x=70,
                 title_max=118, gold_max=56, body_max=50, X0=70, right_cap=960):
    """blocks = [(kind, text)] kind in title/gold/body。返回布局，内部自选字号避免超高。"""
    d = ImageDraw.Draw(img)
    bf = font(28 if badge_txt and False else 30)
    tw = d.textlength(badge_txt, font=font(30))
    d.rounded_rectangle([X0-10, 80, X0+tw+18, 126], radius=12, fill=(6,18,44),
                        outline=(130,175,235), width=3)
    d.text((X0, 84), badge_txt, font=font(30), fill=(210,232,255))
    avail = region_bottom - region_top

    def layout(title_fs):
        sizes = []
        for kind, text in blocks:
            if kind == "title":
                fs = title_fs
                while fs >= 54 and tlen(text, font(fs)) > right_cap - X0 - 6:
                    fs -= 2
            elif kind == "gold":
                fs, _ = fit_auto(text, gold_max, 26, right_cap - X0 - 6)
            else:
                fs, _ = fit_auto(text, body_max, 24, right_cap - X0 - 6)
            sizes.append((kind, fs, text))
        rows = []
        y = 0
        for i, (kind, fs, text) in enumerate(sizes):
            if i > 0:
                prev = sizes[i-1][0]
                y += 34 if kind != prev else 12
            rows.append((kind, fs, text, y))
            y += int(fs*1.32)
        return rows, y

    title_fs = title_max
    while title_fs >= 60:
        rows, bottom = layout(title_fs)
        if bottom <= avail:
            break
        title_fs -= 4
    y0 = region_top + (avail - bottom)//2
    if y0 < 150:
        y0 = 150
    total_b = None
    for kind, fs, text, ry in rows:
        f = font(fs)
        col = WHITE if kind == "title" else (GOLD if kind == "gold" else LIGHT)
        d.text((X0, y0+ry), text, font=f, fill=col, anchor="la")
        b = mbox(text, f, y0+ry, X0)
        assert b[2] <= right_cap, f"{badge_txt} 越右界 {b} {text}"
        total_b = b[3]
    assert total_b <= region_bottom + 10, f"{badge_txt} 超下界 {total_b}"
    return d

# ---------------- 数据 ----------------
ROOT = "E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作-深圳中考志愿填报/P1-政策解码器/P1-4-投档规则全解"
PAL = {
  "S1": (18,74,128,6,16,42), "S2": (46,78,132,10,20,44),
  "S3": (14,32,66,5,10,24), "S4": (22,62,122,6,15,36),
}
BADGE = {"S1":"深圳中考 · 志愿顺序 S1","S2":"深圳中考 · 同分规则 S2","S3":"深圳中考 · 志愿自查 S3","S4":"深圳中考 · 操作提醒 S4"}
# dy 分镜：每镜头 = 标题行(白) + gold句(金) + 要点(浅)（可为空）
DY = {
 "S1": [
   (["600分，败给了599分"], "不是分数，是志愿顺序填反了", []),
   (["深圳投档就 8 个字"], "分数优先 · 依照志愿顺序", []),
   (["不是第1志愿有加分"], "系统从上到下检索，第1个有空位就录你", []),
   (["想去的放第2 = 白搭"], "第1志愿检索到保底校，直接录取你", []),
   (["每年都有人吃这个亏"], "超常发挥够名校，却被保底校录走", []),
   (["把最想去的放最前"], "志愿是排序表，不是省分表", []),
 ],
 "S2": [
   (["同分先比初二那科？"], "不是语数英，是生地合卷", []),
   (["生地98 vs 生地90"], "580 同分争最后名额 → 98 先录", []),
   (["语数英高10分也没用"], "第1层比生地 · 第2层才比语数英", []),
   (["生地初二就考完了"], "分数早定，填志愿前改变不了", []),
   (["别过度焦虑"], "同分PK只发生在极端情况", ["同分 + 争同一校最后名额"]),
   (["生地是隐形分"], "没考别裸考 · 考完心里有数", []),
 ],
 "S3": [
   (["12个志愿全填一个分段？"], "听起来稳，其实是最贵的错", []),
   (["超常考560 · 更好的没报"], "全填530-540，分浪费了", []),
   (["失误考520 = 直接全灭"], "2025真实：12志愿全落 · 补录民办", []),
   (["拉开梯度：冲稳保底"], "冲高5-15 · 稳±5 · 保低10-20 · 底低30+", []),
   (["宁可冲不到，不能保不住"], "真实发挥有浮动，梯度就是缓冲", []),
   (["4问自查，任一'是'都要改"], "占坑? 扎堆? 保底第1? 走读看通勤?", []),
 ],
 "S4": [
   (["勾了走读 = 三年通勤"], "2026新增 · 最多对4校勾 · 还反悔不了", []),
   (["被走读录了不能转住宿"], "不能转住宿 · 不能退档", []),
   (["三句话记住"], "单程45分钟内才勾", ["必须住宿绝不勾 · 走读只是锦上添花"]),
   (["保存 ≠ 确认"], "填写→保存→确认(短信验证码)→打印回执", []),
   (["只保存没确认 = 志愿作废"], "2026最多3次确认 · 截止6月1日18:00", []),
   (["填完当晚再确认一次"], "P1-4投档讲完 · 下条：名额分配", []),
 ],
}
# 小红书：封面(title,gold,bottom) + 4 正文卡(title, gold, body)
XHS = {
 "S1": (
   (["想去的学校，放第1志愿"], "600分也可能败给599分", "不是分数，是志愿顺序"),
   (["600去B · 599进A"], "分数更高反而吃亏", ["小刚600：第1志愿B校 → 录B", "小芳599：第1志愿A校 → 录A", "系统按你志愿顺序检索 · 第一个有空位就录"]),
   (["不是第1志愿有加分"], "是顺序检索", ["第1志愿最先被检索，有空位就进", "没空位才看第2、第3…", "想去的学校不放前面 = 轮不到它"]),
   (["第1志愿别填保底"], "超常发挥也白搭", ["2025真实：保底占第1 → 被直接录走", "后面11个更好志愿全作废", "保底只放最后1-2个"]),
   (["正确排法"], "最想去的放第1志愿", ["按喜欢程度从高到低排", "冲→稳→保→底 拉开梯度", "志愿是排序表，不是省分表"]),
 ),
 "S2": (
   (["同分先比初二那科"], "生地合卷 ＞ 语数英", "多数家长想反了"),
   (["同分PK层级表"], "先比生地，再比语数英", ["第1层：生物与地理(合卷) 高者优先", "第2层：语数英三科总分 高者优先"]),
   (["生地98 vs 生地90"], "同分先录98", ["小陈580(生地98) 先录", "小李580(生地90/语数英310) 高10分也没用"]),
   (["生地初二就考完了"], "分数早定 · 别裸考", ["填志愿、出总分时都改不了", "没考的别裸考，能提前锁定", "考完的查一下心里有数"]),
   (["不用为同分焦虑"], "极端情况才触发", ["只在：总分相同 + 争同一校最后名额", "大多数人总分这层就录完了", "它是一道保险，不是决定一切"]),
 ),
 "S3": (
   (["冲稳保底 · 拉开梯度"], "志愿是区间，不是点", "别全押一个分段"),
   (["最贵的错：全扎一段"], "超常浪费 · 失误全灭", ["超常考560 → 更好的没报", "失误考520 → 12个全够不着", "2025真实：12志愿全落·补录民办"]),
   (["冲·稳·保·底 四档"], "给孩子留容错", ["冲：高5-15分 放2-3个", "稳：平时±5分 放多数", "保：低10-20 · 底：低30+ 一定留足"]),
   (["4问自查清单"], "任一'是'都要改", ["Q1 填了'录了也不想去'的? 会作废后批", "Q2 12志愿全扎一个分段?", "Q3 第1志愿填了保底?", "Q4 勾走读前看过通勤?"]),
   (["一句话记住"], "志愿是区间不是点", ["别估一个分填一堆分", "覆盖一段可能区间", "发挥好坏都有学上"]),
 ),
 "S4": (
   (["走读只在45分钟内勾"], "被走读录了不能转住宿", "2026新增 · 最多对4校勾"),
   (["走读调剂是什么"], "勾了可能被录成走读", ["2026新增 · 第一批普高最多对4校勾", "住宿满、走读有余 → 录走读生", "被走读录取：不能转住宿 · 不能退档"]),
   (["一张表：勾 or 不勾"], "走读是锦上添花", ["≤30分钟 → 勾", "30-45分钟能接受 → 谨慎", ">45分钟/换乘 → 不勾", "身体必须住宿 → 绝不勾"]),
   (["保存 ≠ 确认"], "只保存没确认 = 作废", ["填写→保存→确认(验证码)→打印回执", "2026最多3次确认 · 第3次后不能改", "截止6月1日18:00"]),
   (["P1-4 投档讲完了"], "下一步：亲手排一次", ["五批次/顺序/同分/梯度/走读/保存 都讲了", "打开 HSEE 模拟志愿填报 试一次", "下篇 P1-5：名额分配50%指标到校"]),
 ),
}
if __name__ == "__main__":
    for unit in ["S1","S2","S3","S4"]:
        TOP = PAL[unit]
        BADGE_TXT = BADGE[unit]
        # 抖音 6 分镜
        for i, (title, gold, body) in enumerate(DY[unit], start=1):
            blocks = [("title", t) for t in title] + [("gold", gold)] + [("body", t) for t in body]
            img = Image.fromarray(base(1080, 1920, TOP[:3], TOP[3:]))
            stack_render(img, blocks, 170, 1560, BADGE_TXT, right_cap=960)
            d = ImageDraw.Draw(img)
            d.text((70, 148), f"{i:02d}/06", font=font(34), fill=(120,160,215))
            out = f"{ROOT}/子任务S{unit[1]}-" + ("志愿顺序" if unit=="S1" else "同分PK" if unit=="S2" else "四个投档错误自查" if unit=="S3" else "走读调剂与保存确认")
            fn_map = {"S1":"P1-4-S1-志愿顺序","S2":"P1-4-S2-同分PK","S3":"P1-4-S3-四错自查","S4":"P1-4-S4-走读调剂保存"}
            fp = f"{out}/03.抖音/{fn_map[unit]}-抖音-镜头{i:02d}-1080x1920.png"
            save_img(img, fp)
            print("OK dy", fp.split('/')[-1])
        # 小红书 封面 + 4 卡
        xc = XHS[unit]
        # 封面
        title, gold, bot = xc[0]
        img = Image.fromarray(base(1080, 1440, TOP[:3], TOP[3:]))
        stack_render(img, [("title", t) for t in title] + [("gold", gold)] + [("body", bot)],
                     170, 1370, BADGE_TXT, right_cap=1000)
        folder = f"{ROOT}/子任务S{unit[1]}-" + ("志愿顺序" if unit=="S1" else "同分PK" if unit=="S2" else "四个投档错误自查" if unit=="S3" else "走读调剂与保存确认")
        save_img(img, f"{folder}/04.小红书/{fn_map[unit]}-小红书-封面-1080x1440.png")
        print("OK xhs cover", unit)
        for idx, (title, gold, body) in enumerate(xc[1:], start=1):
            blocks = [("title", t) for t in title] + [("gold", gold)] + [("body", t) for t in body]
            img = Image.fromarray(base(1080, 1440, TOP[:3], TOP[3:]))
            stack_render(img, blocks, 160, 1370, BADGE_TXT, right_cap=1000)
            desc = ["1-反直觉结果","2-顺序检索原理","3-保底坑","4-正确排法"] if unit=="S1" else \
                   ["1-层级表","2-案例","3-生地初二已定","4-别焦虑"] if unit=="S2" else \
                   ["1-最贵的错","2-四档梯度","3-4问自查","4-一句话"] if unit=="S3" else \
                   ["1-走读风险","2-决策表","3-保存确认","4-收口"]
            save_img(img, f"{folder}/04.小红书/{fn_map[unit]}-小红书-正文图{desc[idx-1]}-1080x1440.png")
            print("OK xhs card", unit, desc[idx-1])
