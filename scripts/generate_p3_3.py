"""试点脚本：为 P3-3《深圳公办高中梯队全盘点》生成数据图 + 封面。

复用共享库，仅新增本文特有的梯队图表逻辑。
产出：
  1. 五梯队分布图（每梯队学校数 + 分数段）
  2. 公众号封面

用法：python generate_p3_3.py
"""
import os
import matplotlib.pyplot as plt

from hsee_charts import config, db, watermark, cover

config.setup_style()

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)


# 梯队划分（基于 AC 住宿线，边界对齐文章）
TIERS = [
    ("第一梯队\n四大", 587, 999),
    ("第二梯队\n八大/十大", 570, 586),
    ("第三梯队\n二十大/三十强", 540, 569),
    ("第四梯队\n五十强", 500, 539),
    ("第五梯队\n百强/新校", 0, 499),
]
# 蓝色渐变：越顶尖越深
TIER_COLORS = ["#1F5FA8", "#4A86C8", "#7FA8D9", "#A8C6E8", "#D3E3F3"]


def chart_tier_distribution():
    rows = db.query_all_ac_lines(year="2026")
    labels = [t[0] for t in TIERS]
    counts = [sum(1 for r in rows if t[1] <= r[1] <= t[2]) for t in TIERS]

    fig, ax = plt.subplots(figsize=config.BODY_SIZE)
    bars = ax.bar(labels, counts, color=TIER_COLORS, width=0.55)
    for b, c, t in zip(bars, counts, TIERS):
        rng = f"{t[1]}分" if t[1] == 587 else (f"{t[1]}-{t[2]}分" if t[2] != 999 else f"≥{t[1]}分")
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5,
                f"{c}所\n{rng}", ha="center", fontsize=9.5)
    ax.set_title("101 所公办普高分成 5 个梯队（按 2026 AC 住宿线）", fontsize=13, fontweight="bold")
    ax.set_ylabel("学校数（所）")
    ax.set_ylim(0, max(counts) + 12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)

    watermark.save_with_watermark(fig, os.path.join(OUT_DIR, "p3-3-梯队分布.png"))


def cover_p3_3():
    cover.render_cover(
        os.path.join(OUT_DIR, "p3-3-封面-公众号.png"),
        tag="P3 · 数据择校地图",
        title="深圳公办高中梯队全盘点：四大/八大/二十大/新校",
        data_text="101 所公办普高，按分数线分成",
        data_num="5个梯队",
        width=900, height=383,
    )


if __name__ == "__main__":
    chart_tier_distribution()
    cover_p3_3()
    print("P3-3 生成完成：", os.path.abspath(OUT_DIR))
