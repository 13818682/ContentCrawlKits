"""试点脚本：为 P3-2《AC类vs D类分差排行榜》生成数据图 + 封面。

复用共享库（config/db/watermark/cover），仅新增本文特有的图表逻辑。
产出：
  1. 友好度分布图（6 档学校数量）
  2. "反向友好"学校（D线低于AC线）
  3. 公众号封面

用法：python generate_p3_2.py
"""
import os
import matplotlib.pyplot as plt

from hsee_charts import config, db, watermark, cover

config.setup_style()

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 图1：友好度分布（6 档学校数量）
# ---------------------------------------------------------------------------
def chart_friendly_distribution():
    rows = db.query_acd_diff(year="2026")
    tiers = [
        ("≤0分\nD类更低", 0, 0),
        ("1-3分", 1, 3),
        ("4-8分", 4, 8),
        ("9-15分", 9, 15),
        ("16-25分", 16, 25),
        (">25分", 26, 999),
    ]
    labels = [t[0] for t in tiers]
    counts = [sum(1 for r in rows if t[1] <= r[3] <= t[2]) for t in tiers]
    colors = ["#2E9E6B", "#7BBF7B", "#E8B84B", "#E08B4B", "#D6604D", "#D64541"]

    fig, ax = plt.subplots(figsize=config.BODY_SIZE)
    bars = ax.bar(labels, counts, color=colors, width=0.6)
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.4, str(c),
                ha="center", fontsize=11, fontweight="bold")
    ax.set_title("AC/D 分差友好度分布：越靠左 D 类越不吃亏", fontsize=13, fontweight="bold")
    ax.set_ylabel("学校数（所）")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)

    watermark.save_with_watermark(fig, os.path.join(OUT_DIR, "p3-2-友好度分布.png"))


# ---------------------------------------------------------------------------
# 图2：反向友好校（D线低于AC线）
# ---------------------------------------------------------------------------
def chart_reverse_friendly():
    rows = db.query_acd_diff(year="2026")
    neg = [r for r in rows if r[3] < 0]
    neg.sort(key=lambda r: r[3])  # 最负的排最上

    names = [r[0] for r in neg]
    diffs = [r[3] for r in neg]

    fig, ax = plt.subplots(figsize=(8, max(3, 0.5 * len(neg))))
    ax.barh(names, diffs, color=config.COLORS["down_green"])
    for i, d in enumerate(diffs):
        ax.text(d - 0.15, i, f"{d:+d}", va="center", ha="right",
                fontsize=9, fontweight="bold", color=config.COLORS["down_green"])
    ax.axvline(0, color=config.COLORS["text_main"], linewidth=0.8)
    ax.set_title("反向友好校：D 线反而低于 AC 线（罕见）", fontsize=13, fontweight="bold")
    ax.set_xlabel("D线 - AC线（分），负值 = D类更划算")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)

    watermark.save_with_watermark(fig, os.path.join(OUT_DIR, "p3-2-反向友好校.png"))


def cover_p3_2():
    cover.render_cover(
        os.path.join(OUT_DIR, "p3-2-封面-公众号.png"),
        tag="P3 · 数据择校地图",
        title="AC类vs D类分差排行榜：哪些学校对D类最友好",
        data_text="全深圳 41 所学校 D 类分差≤3分",
        data_num="五星友好",
        width=900, height=383,
    )


if __name__ == "__main__":
    chart_friendly_distribution()
    chart_reverse_friendly()
    cover_p3_2()
    print("P3-2 生成完成：", os.path.abspath(OUT_DIR))
