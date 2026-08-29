"""为 P3-8《D类分数线地图》生成数据图：各梯队 D类-AC 平均分差。

用法：python generate_p3_8.py
"""
import os
import matplotlib.pyplot as plt

from hsee_charts import config, watermark

config.setup_style()

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 2026 真实数据（来自 gen_d_class_data.py 查询 sz_v_school_scores_timeline）
TIER_LABELS = ["四大", "八大/十大", "二十大\n/三十强", "五十强", "百强/新校"]
TIER_DIFF = [0.0, 0.1, 0.8, 10.4, 23.1]
TIER_COLORS = ["#1F5FA8", "#4A86C8", "#7FA8D9", "#A8C6E8", "#D3E3F3"]


def chart_tier_diff():
    fig, ax = plt.subplots(figsize=config.BODY_SIZE)
    bars = ax.bar(TIER_LABELS, TIER_DIFF, color=TIER_COLORS, width=0.55)
    for b, v in zip(bars, TIER_DIFF):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.6,
                f"{v:.1f}分", ha="center", fontsize=10.5, fontweight="bold")
    ax.set_title("学校越顶尖，D类越不吃亏（各梯队 D类线 - AC线 平均分差）",
                 fontsize=13, fontweight="bold")
    ax.set_ylabel("D类线 - AC线（分）")
    ax.set_ylim(0, 28)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)

    out = os.path.join(OUT_DIR, "p3-8-梯队分差.png")
    watermark.save_with_watermark(fig, out)
    print("生成完成：", os.path.abspath(out))


if __name__ == "__main__":
    chart_tier_diff()
