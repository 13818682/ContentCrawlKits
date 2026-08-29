"""试点脚本：为 P5-4《分数线复盘》生成核心数据图。

跑通"数据图生成"环节，产出 3 张图：
  1. 四大名校 2025归一化 vs 2026 分数线对比（分组柱状图）
  2. 八大/十大 2025→2026 真实涨跌（发散条形图，红涨绿跌）
  3. AC/D 分差：顶尖校吃平 vs 普通校溢价（条形图）

用法：python generate_p5_4.py
"""
import os
import matplotlib.pyplot as plt

from hsee_charts import config, db, watermark

config.setup_style()

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 校名简称（太长放不下坐标轴）
SHORT = {
    "深圳实验学校(高中部)": "深圳实验",
    "深圳市高级中学中心校区": "深圳高级中学",
    "深圳大学附属中学中心校区(深大附中中心校区)": "深大附中",
    "宝安中学(集团)高中部": "宝安中学",
    "翠园中学(爱国路校区)": "翠园中学",
    "南方科技大学附属中学": "南科大附中",
    "北京师范大学南山附属学校": "北师大南山",
    "南山外国语学校(集团)高级中学": "南山外国语",
    "深圳市第二实验学校": "深圳二实验",
    "华中师范大学龙岗附属中学": "华中师大龙岗",
    "广东实验中学深圳学校": "广东实验深圳",
    "深圳市格致中学": "格致中学",
    "深圳市曙光中学(综合高中)": "曙光中学",
    "深圳中学数理高中": "深中数理高中",
    "深圳实验学校崇文高中": "深实验崇文高中",
}


def short(name):
    return SHORT.get(name, name)


# ---------------------------------------------------------------------------
# 图1：四大名校 2025归一化 vs 2026
# ---------------------------------------------------------------------------
def chart_four_big():
    rows = db.query_ac_scores(years=("2025", "2026"), limit=4)
    names = [short(r[0]) for r in rows]
    ac25 = [r[1] for r in rows]
    ac26 = [r[2] for r in rows]
    ac25_norm = [round(config.normalize(s, 2025, 2026), 1) for s in ac25]

    x = range(len(names))
    w = 0.38
    fig, ax = plt.subplots(figsize=config.BODY_SIZE)
    ax.bar([i - w/2 for i in x], ac25_norm, w, label="2025（归一化到630分制）",
           color=config.COLORS["brand_blue"])
    ax.bar([i + w/2 for i in x], ac26, w, label="2026（实际）",
           color=config.COLORS["accent_orange"])

    for i in x:
        ax.text(i - w/2, ac25_norm[i] + 1, f"{ac25_norm[i]:.0f}",
                ha="center", fontsize=9, color=config.COLORS["text_secondary"])
        ax.text(i + w/2, ac26[i] + 1, f"{ac26[i]}",
                ha="center", fontsize=9, color=config.COLORS["text_main"],
                fontweight="bold")

    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.set_ylim(0, max(ac26) + 12)
    ax.set_title("四大名校分数线：满分610→630后，归一化几乎没变", fontsize=13, fontweight="bold")
    ax.set_ylabel("AC类住宿线（分）")
    ax.legend(frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)

    watermark.save_with_watermark(fig, os.path.join(OUT_DIR, "p5-4-四大名校-归一化对比.png"))


# ---------------------------------------------------------------------------
# 图2：八大/十大 归一化后真实涨跌（发散条形图）
# ---------------------------------------------------------------------------
def chart_real_change():
    rows = db.query_ac_scores(years=("2025", "2026"), limit=15)
    data = []
    for name, ac25, ac26 in rows:
        norm = config.normalize(ac25, 2025, 2026)
        data.append((name, round(ac26 - norm, 1)))
    # 取真实变化最大的 5 涨 + 5 跌（|diff| 最大的 10 个）
    data.sort(key=lambda t: t[1])
    pick = data[:5] + data[-5:]
    pick.sort(key=lambda t: t[1])

    names = [short(n) for n, _ in pick]
    diffs = [d for _, d in pick]
    colors = []
    for d in diffs:
        if d >= 2:
            colors.append(config.COLORS["up_red"])
        elif d <= -2:
            colors.append(config.COLORS["down_green"])
        else:
            colors.append(config.COLORS["text_secondary"])

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.barh(names, diffs, color=colors)
    for i, d in enumerate(diffs):
        ax.text(d + (0.15 if d >= 0 else -0.15), i, f"{d:+.0f}",
                va="center", ha="left" if d >= 0 else "right",
                fontsize=9, fontweight="bold", color=colors[i])
    ax.axvline(0, color=config.COLORS["text_main"], linewidth=0.8)
    ax.set_title("八大/十大 2025→2026 真实涨跌（归一化满分后）", fontsize=13, fontweight="bold")
    ax.set_xlabel("真实涨跌（分）：红涨 = 竞争升温，绿跌 = 热度回落")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)

    watermark.save_with_watermark(fig, os.path.join(OUT_DIR, "p5-4-真实涨跌-发散条形图.png"))


# ---------------------------------------------------------------------------
# 图3：AC/D 分差：顶尖校吃平 vs 普通校溢价
# ---------------------------------------------------------------------------
def chart_acd_gap():
    rows = db.query_acd_diff(year="2026")
    # 顶尖校：AC线最高的前 6 所；普通校：D线溢价最高的 6 所（不受AC线限制）
    top = rows[:6]
    bottom = sorted(rows, key=lambda r: r[3], reverse=True)[:6]
    picks = top + bottom

    names = [short(r[0]) for r in picks]
    diffs = [r[3] for r in picks]
    colors = [config.COLORS["brand_blue"]] * len(top) + \
             [config.COLORS["accent_orange"]] * len(bottom)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.barh(names, diffs, color=colors)
    for i, d in enumerate(diffs):
        ax.text(d + 0.3, i, f"{d:+d}", va="center", ha="left",
                fontsize=9, fontweight="bold", color=colors[i])
    ax.axvline(0, color=config.COLORS["text_main"], linewidth=0.8)
    ax.set_title("AC/D 分差：越顶尖 D 类越不吃亏，越普通溢价越高", fontsize=13, fontweight="bold")
    ax.set_xlabel("D线 - AC线（分）：0 = D类不吃亏，正数 = D类需多考的分")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)

    watermark.save_with_watermark(fig, os.path.join(OUT_DIR, "p5-4-ACD分差.png"))


if __name__ == "__main__":
    chart_four_big()
    chart_real_change()
    chart_acd_gap()
    print("生成完成，输出目录：", os.path.abspath(OUT_DIR))
