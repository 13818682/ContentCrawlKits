"""水印与保存（见 10-发布素材自动化方案 第七章）。

三层水印：
1. 角标 logo（右下角，清晰）——品牌标识
2. 数据来源（左下角，常规）——声明 + 防盗
3. 半透明斜纹（斜铺整图，6-10% 透明）——防直接截走
"""
import matplotlib.pyplot as plt

from . import config


def save_with_watermark(fig, path, diagonal_count=3):
    """给 fig 叠加三层水印后保存到 path。

    diagonal_count：斜纹水印的条数（3-5 条斜铺整图）。
    """
    w = config.WATERMARK
    fig_width, fig_height = fig.get_size_inches()

    # 1. 角标 logo（右下角）
    fig.text(
        0.985, 0.012, w["logo_text"],
        ha="right", va="bottom",
        fontsize=11, fontweight="bold",
        color=config.COLORS["brand_blue"], alpha=w["logo_alpha"],
    )

    # 2. 数据来源（左下角）
    fig.text(
        0.015, 0.012, w["source_text"],
        ha="left", va="bottom",
        fontsize=7.5, color=config.COLORS["text_secondary"],
    )

    # 3. 半透明斜纹（斜铺整图，防截）
    for i in range(diagonal_count):
        x = 0.15 + i * (0.7 / max(diagonal_count - 1, 1))
        fig.text(
            x, 0.55, w["diagonal_text"],
            ha="center", va="center",
            fontsize=42, rotation=30,
            color=config.COLORS["brand_blue"], alpha=w["diagonal_alpha"],
        )

    fig.savefig(path, dpi=config.FIGURE_DPI, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
