"""为 P2-6《D类指标生机会》生成数据图：D类指标生名额 Top15（横向柱）。

用法：python generate_p2_6.py
"""
import os
import matplotlib.pyplot as plt

from hsee_charts import config, watermark

config.setup_style()

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 2026 真实数据（来自 gen_d_quota_summary.py）
SCHOOLS = ["光明区高级中学", "致理中学", "龙华科技实验", "燕川中学", "龙岗区二高",
           "龙津中学", "聚龙科学中学", "深外弘知高中", "华中师大龙岗", "第七高级中学",
           "观澜中学", "深中数理高中", "深中科技高中", "深中实验高中", "红岭中学"]
D_QUOTA = [203, 194, 162, 161, 159, 155, 153, 149, 146, 146, 145, 145, 145, 145, 139]


def chart_d_quota():
    fig, ax = plt.subplots(figsize=(8, 7))
    y = list(range(len(SCHOOLS)))
    bars = ax.barh(y, D_QUOTA, color="#4A86C8", height=0.6)
    for yi, v in zip(y, D_QUOTA):
        ax.text(v + 2, yi, str(v), va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(SCHOOLS, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("D类指标生名额（人）")
    ax.set_title("D类指标生名额 Top15：普通校/新校是主战场", fontsize=13, fontweight="bold")
    ax.set_xlim(0, 235)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)

    out = os.path.join(OUT_DIR, "p2-6-D类指标生名额.png")
    watermark.save_with_watermark(fig, out)
    print("生成完成：", os.path.abspath(out))


if __name__ == "__main__":
    chart_d_quota()
