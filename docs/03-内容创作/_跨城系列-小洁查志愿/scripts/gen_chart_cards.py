# -*- coding: utf-8 -*-
"""
跨城系列《小洁查志愿》公众号配图 · 确定性图表卡渲染脚本
方式: Python + PIL, 微软雅黑, 深蓝系统一模板
输出: 各篇 01.公众号 目录下的 PNG (900x400)
用法: python gen_chart_cards.py            # 生成全部图表
      python gen_chart_cards.py p02 p05    # 只生成指定篇目

技能与规范来源:
- 本脚本依据《00-系列配图规格与生成脚本.md》实现（视觉系统/逐图文案/验收闸口/合规红线）
- 主技能 doubao-creative-design（公众号配图生成总控）:
  C:\Users\weiwei\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills\doubao-creative-design\
  - references\media-wechat-official.md  公众号平台视觉特征与红线（克制秩序感、品牌色、金句容器化）
  - references\clarification-and-confirmation.md  澄清门禁（用户已授权按专业判断定规格）
  - references\model-4.5.md  seedream 4.5 改写规则（AI 图部分）
- 图表卡部分由本脚本确定性渲染（PIL + 微软雅黑），文字 100% 准确，不依赖 AI 生图
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 400
BG = (15, 42, 74)          # #0F2A4A 深蓝底
BG_DEEP = (10, 30, 56)     # #0A1E38
CARD = (22, 54, 94)        # #16375E 卡片底
CARD_LINE = (46, 90, 140)  # #2E5A8C 卡片边框
GOLD = (212, 168, 67)      # #D4A843 强调
LBLUE = (143, 180, 214)    # #8FB4D6 辅助
WHITE = (244, 241, 234)    # #F4F1EA 米白
GRAY = (120, 145, 175)     # 弱化文字

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {
    "p02": os.path.join(ROOT, "第02篇-家长最常卡住的五个地方", "01.公众号"),
    "p05": os.path.join(ROOT, "第05篇-四座城市我们一座一座来", "01.公众号"),
    "p06": os.path.join(ROOT, "第06篇-为什么我们不直接抄网上的分数线", "01.公众号"),
    "p07": os.path.join(ROOT, "第07篇-初二家长现在做这三件事", "01.公众号"),
    "p08": os.path.join(ROOT, "第08篇-四座城市都齐了", "01.公众号"),
}

def font(sz, bold=True):
    p = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    return ImageFont.truetype(p, sz)

def base(draw):
    draw.rectangle([0, 0, W, H], fill=BG)
    # 顶部系列标签
    f = font(15, bold=False)
    draw.text((40, 22), "小洁查志愿 · 深莞广佛四城", font=f, fill=LBLUE)
    # 右上角装饰圆点
    draw.ellipse([858, 20, 872, 34], fill=GOLD)
    draw.ellipse([846, 28, 854, 36], fill=LBLUE)

def title(draw, text, y=48, size=28):
    f = font(size)
    draw.text((40, y), text, font=f, fill=GOLD)

def note(draw, text, y=300, size=17, color=LBLUE, center=True):
    f = font(size, bold=False)
    if center:
        tw = f.getlength(text)
        draw.text(((W - tw) / 2, y), text, font=f, fill=color)
    else:
        draw.text((40, y), text, font=f, fill=color)

def card(draw, x0, y0, x1, y1, radius=12, fill=CARD, outline=CARD_LINE, ow=2):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=ow)

def center_text(draw, text, cx, cy, f, color):
    tw = f.getlength(text)
    draw.text((cx - tw / 2, cy - f.size / 2), text, font=f, fill=color)

# ---------------- 第02篇 ----------------
def p02_chart01_batch_flow():
    """深圳录取 · 五个批次"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "深圳录取 · 五个批次")
    nodes = ["自主招生批", "名额分配批", "统招第一批", "统招第二批", "统招第三批"]
    cw, ch, gap, y0, y1 = 150, 90, 16, 120, 210
    x = (W - (cw * 5 + gap * 4)) / 2
    f_node = font(18)
    for i, n in enumerate(nodes):
        x0 = x + i * (cw + gap)
        card(d, x0, y0, x0 + cw, y1, radius=10)
        center_text(d, n, x0 + cw / 2, (y0 + y1) / 2, f_node, WHITE)
        if i < 4:
            ax = x0 + cw + gap / 2
            f_arrow = font(26)
            center_text(d, "→", ax, (y0 + y1) / 2, f_arrow, GOLD)
    note(d, "前一批被录取，后面的批次不再看", y=265)
    img.save(os.path.join(DIRS["p02"], "第02篇-家长最常卡住的五个地方-公众号-图表01-五批次流程.png"))

def p02_chart02_five_blocks():
    """家长最常卡住的五处（前两处绕，后三处散）"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "家长最常卡住的五处")
    items = [("词", "绕"), ("顺序", "绕"), ("数据", "散"), ("学校", "散"), ("说法", "散")]
    cw, ch, gap, y0, y1 = 150, 120, 16, 120, 240
    x = (W - (cw * 5 + gap * 4)) / 2
    f_tag = font(16); f_name = font(26)
    for i, (name, tag) in enumerate(items):
        x0 = x + i * (cw + gap)
        card(d, x0, y0, x0 + cw, y1)
        tag_color = GOLD if tag == "绕" else LBLUE
        center_text(d, tag, x0 + cw / 2, y0 + 30, f_tag, tag_color)
        center_text(d, name, x0 + cw / 2, (y0 + y1) / 2 + 16, f_name, WHITE)
    note(d, "前两处是绕，后三处是散", y=280, color=GOLD)
    img.save(os.path.join(DIRS["p02"], "第02篇-家长最常卡住的五个地方-公众号-图表02-五处卡点.png"))

# ---------------- 第05篇 ----------------
def p05_chart01_scores():
    """四座城市，四个满分"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "四座城市，四个满分")
    items = [("深圳", "630 分"), ("东莞", "800 分"), ("广州", "810 分"), ("佛山", "740 分")]
    cw, ch, gap, y0, y1 = 195, 130, 14, 112, 242
    x = (W - (cw * 4 + gap * 3)) / 2
    f_city = font(18); f_score = font(34)
    for i, (city, score) in enumerate(items):
        x0 = x + i * (cw + gap)
        card(d, x0, y0, x0 + cw, y1)
        center_text(d, city, x0 + cw / 2, y0 + 32, f_city, LBLUE)
        center_text(d, score, x0 + cw / 2, y0 + 82, f_score, GOLD)
    note(d, "东莞 2027 起降 680 · 佛山 2027 起调 700 · 广州 2029 前不变", y=272)
    note(d, "深圳 2026 年起由 610 分调至 630 分", y=302, color=GRAY)
    img.save(os.path.join(DIRS["p05"], "第05篇-四座城市我们一座一座来-公众号-图表01-四城总分.png"))

def p05_chart02_batch_compare():
    """批次：名字一样，装的学校不一样"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "批次：名字一样，装的学校不一样")
    col_w, col_h, y0 = 380, 245, 106
    sx = 40; dx = 480
    f_col = font(22); f_node = font(15)
    for label, nodes, x0 in [("深圳", ["自主招生批", "名额分配批", "统招第一批", "统招第二批", "统招第三批"], sx),
                             ("东莞", ["提前批", "第一批", "第二批", "第三批", "第四批"], dx)]:
        card(d, x0, y0, x0 + col_w, y0 + col_h)
        center_text(d, label, x0 + col_w / 2, y0 + 24, f_col, WHITE)
        n_h, n_gap = 30, 9
        ny = y0 + 48
        for n in nodes:
            card(d, x0 + 18, ny, x0 + col_w - 18, ny + n_h, radius=6, fill=BG_DEEP, outline=CARD_LINE, ow=1)
            center_text(d, n, x0 + col_w / 2, ny + n_h / 2, f_node, LBLUE)
            ny += n_h + n_gap
    note(d, "都是五个批次，可名字与里面装的东西，是另一套", y=372)
    img.save(os.path.join(DIRS["p05"], "第05篇-四座城市我们一座一座来-公众号-图表02-批次对比.png"))

def p05_chart03_volunteer_count():
    """能填几个"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "能填几个")
    col_w, col_h, y0 = 380, 210, 100
    sx = 40; dx = 480
    f_col = font(22); f_line = font(16)
    for label, lines, x0 in [("深圳", [("统招第一批", "16 个 · 普高最多 12 个"), ("统招第二批", "18 个")], sx),
                             ("东莞", [("第一批", "6 个"), ("第二批", "6 个")], dx)]:
        card(d, x0, y0, x0 + col_w, y0 + col_h)
        center_text(d, label, x0 + col_w / 2, y0 + 26, f_col, WHITE)
        ly = y0 + 62
        for a, b in lines:
            center_text(d, a, x0 + col_w / 2 - 70, ly, f_line, LBLUE)
            center_text(d, b, x0 + col_w / 2 + 55, ly, f_line, GOLD)
            ly += 52
    note(d, "深圳的志愿表，比东莞长得多", y=335, color=GOLD)
    img.save(os.path.join(DIRS["p05"], "第05篇-四座城市我们一座一座来-公众号-图表03-志愿数量.png"))

# ---------------- 第06篇 ----------------
def p06_chart01_line_structure():
    """同一个分数，至少有这几种"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "同一个分数，至少有这几种")
    groups = [("住宿生 / 走读生", "两个数", ""), ("A 类 / C 类 / D 类考生", "三个不同的数", ""),
              ("正取线 / 名额分配控制线", "两个数", "不能互相参考")]
    cw, ch, gap, y0, y1 = 270, 160, 15, 112, 272
    x = (W - (cw * 3 + gap * 2)) / 2
    f_tag = font(16); f_num = font(26); f_sub = font(14)
    for i, (tag, num, sub) in enumerate(groups):
        x0 = x + i * (cw + gap)
        card(d, x0, y0, x0 + cw, y1)
        center_text(d, tag, x0 + cw / 2, y0 + 36, f_tag, LBLUE)
        center_text(d, num, x0 + cw / 2, y0 + 92, f_num, GOLD)
        if sub:
            center_text(d, sub, x0 + cw / 2, y0 + 132, f_sub, GRAY)
    note(d, "一句话本身是不完整的 —— 它缺了三个定语", y=306, color=WHITE)
    img.save(os.path.join(DIRS["p06"], "第06篇-为什么我们不直接抄网上的分数线-公众号-图表01-分数线结构.png"))

def p06_chart02_three_questions():
    """看到一个分数线，问三个问题"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "看到一个分数线，问三个问题")
    qs = [("① 这是哪一年的？", "总分改过没有？改过的年份，不能直接比"),
          ("② 这是哪条线？", "住宿还是走读？A、C、D 哪一类？"),
          ("③ 这是谁说的？", "官方公布，还是别人推算的？")]
    cw, ch, gap, y0, y1 = 270, 170, 15, 108, 278
    x = (W - (cw * 3 + gap * 2)) / 2
    f_q = font(18); f_s = font(14)
    for i, (q, s) in enumerate(qs):
        x0 = x + i * (cw + gap)
        card(d, x0, y0, x0 + cw, y1)
        center_text(d, q, x0 + cw / 2, y0 + 46, f_q, WHITE)
        f_s_ = f_s
        tw = f_s_.getlength(s)
        # 自动缩小到卡片宽度
        while tw > cw - 28 and f_s_.size > 12:
            f_s_ = font(f_s_.size - 1, bold=False)
            tw = f_s_.getlength(s)
        center_text(d, s, x0 + cw / 2, y0 + 108, f_s_, LBLUE)
    note(d, "三问在深圳适用，在东莞、广州、佛山的道理也一样", y=320, color=GRAY)
    img.save(os.path.join(DIRS["p06"], "第06篇-为什么我们不直接抄网上的分数线-公众号-图表02-三问卡片.png"))

def p06_chart03_two_batches():
    """名额分配填了，第一批还要再填一次"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "名额分配填了，第一批还要再填一次")
    col_w, col_h, y0 = 380, 200, 104
    sx = 40; dx = 480
    f_col = font(20); f_line = font(15)
    for label, lines, x0 in [("名额分配志愿", ["只管“指标生”这一条路", "只在本校内部比"], sx),
                             ("第一批志愿", ["大多数孩子被录取的那一批", "没走成，就必须在第一批再填一次"], dx)]:
        card(d, x0, y0, x0 + col_w, y0 + col_h)
        center_text(d, label, x0 + col_w / 2, y0 + 30, f_col, WHITE)
        ly = y0 + 76
        for ln in lines:
            f_ = font(15, bold=False)
            while f_.getlength(ln) > col_w - 30 and f_.size > 12:
                f_ = font(f_.size - 1, bold=False)
            center_text(d, ln, x0 + col_w / 2, ly, f_, LBLUE)
            ly += 44
    note(d, "两个独立批次，互不顶替 · 少填一次，就少一条路", y=330, color=GOLD)
    img.save(os.path.join(DIRS["p06"], "第06篇-为什么我们不直接抄网上的分数线-公众号-图表03-双批次.png"))

# ---------------- 第07篇 ----------------
def p07_chart01_three_things():
    """初二这一年，做三件事就够了"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "初二这一年，做三件事就够了")
    items = [("① 知道有几条路", "不止普高一条：中职、技工、中本贯通……"),
             ("② 搞清楚分类", "孩子属于哪一类，能报的范围就不一样"),
             ("③ 开始记位次", "别只记分数，记孩子在年级里的位置")]
    cw, ch, gap, y0, y1 = 270, 175, 15, 106, 281
    x = (W - (cw * 3 + gap * 2)) / 2
    f_t = font(18); f_s = font(14)
    for i, (t, s) in enumerate(items):
        x0 = x + i * (cw + gap)
        card(d, x0, y0, x0 + cw, y1)
        center_text(d, t, x0 + cw / 2, y0 + 44, f_t, WHITE)
        f_ = font(14, bold=False)
        while f_.getlength(s) > cw - 30 and f_.size > 11:
            f_ = font(f_.size - 1, bold=False)
        center_text(d, s, x0 + cw / 2, y0 + 116, f_, LBLUE)
    note(d, "三件事都不占时间 · 一年也就记十几次，每次两分钟", y=318, color=GRAY)
    img.save(os.path.join(DIRS["p07"], "第07篇-初二家长现在做这三件事-公众号-图表01-三件事.png"))

def p07_chart02_rank_record():
    """每次大考，记一笔位次"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "每次大考，记一笔位次")
    rows = [("一次大考", "年级约 120 名", "较上次 ↑"), ("二次大考", "年级约 100 名", "较上次 ↑"),
            ("三次大考", "年级约 105 名", "较上次 ↓")]
    col_x = [40, 240, 560, 690]
    col_w = [170, 290, 100, 120]
    heads = ["考试", "位次（示例）", "对比", "备注"]
    y0, row_h, gap = 112, 52, 10
    f_h = font(16); f_r = font(15)
    for cx, cw_, htxt in zip(col_x, col_w, heads):
        center_text(d, htxt, cx + cw_ / 2, y0 + 6, f_h, GOLD)
    ry = y0 + 28
    for i, (a, b, c) in enumerate(rows):
        card(d, 40, ry, 860, ry + row_h, radius=8, fill=BG_DEEP, outline=CARD_LINE, ow=1)
        for cx, cw_, txt in zip(col_x, col_w, (a, b, c)):
            color = GOLD if i == 0 else LBLUE
            center_text(d, txt, cx + cw_ / 2, ry + row_h / 2, f_r, color)
        ry += row_h + gap
    note(d, "位次比较稳：总分一动，往年分数就没法直接比了", y=300, color=GRAY)
    img.save(os.path.join(DIRS["p07"], "第07篇-初二家长现在做这三件事-公众号-图表02-位次记录.png"))

# ---------------- 第08篇 ----------------
def p08_chart01_progress():
    """四座城市，现在到哪一步"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    base(d); title(d, "四座城市，现在到哪一步")
    rows = [("深圳", "已整理完", GOLD), ("东莞", "已整理完", GOLD),
            ("广州", "正在做", LBLUE), ("佛山", "材料已拿到 · 排在后面", LBLUE)]
    y0, row_h, gap = 108, 50, 10
    f_city = font(20); f_st = font(16)
    for i, (city, st, color) in enumerate(rows):
        ry = y0 + i * (row_h + gap)
        card(d, 40, ry, 860, ry + row_h, radius=8)
        center_text(d, city, 130, ry + row_h / 2, f_city, WHITE)
        mark = "✓" if color == GOLD else "…"
        center_text(d, mark, 300, ry + row_h / 2, font(20), color)
        center_text(d, st, 560, ry + row_h / 2, f_st, color)
    note(d, "进度一直在往前走 · 时间说早了、最后没做完，那是我的问题", y=320, color=GRAY)
    img.save(os.path.join(DIRS["p08"], "第08篇-四座城市都齐了-公众号-图表01-四城进度.png"))

JOBS = {
    "p02": [p02_chart01_batch_flow, p02_chart02_five_blocks],
    "p05": [p05_chart01_scores, p05_chart02_batch_compare, p05_chart03_volunteer_count],
    "p06": [p06_chart01_line_structure, p06_chart02_three_questions, p06_chart03_two_batches],
    "p07": [p07_chart01_three_things, p07_chart02_rank_record],
    "p08": [p08_chart01_progress],
}

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or list(JOBS.keys())
    for t in targets:
        if t in JOBS:
            for fn in JOBS[t]:
                fn()
                print("OK", fn.__name__)
        else:
            print("SKIP unknown:", t)
    print("done")
