"""设计 token 集中定义（见 10-发布素材自动化方案 第六章）。

所有数据图脚本从这里读取配色/字体/水印参数，
改一处，全系列同步换肤。
"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------- 品牌色板 ----------
COLORS = {
    "brand_blue": "#1F5FA8",      # 主色：理性、专业、可信
    "accent_orange": "#F5A623",   # 强调色：CTA、关键数字、重点高亮
    "up_red": "#D64541",          # 涨（分数线上升=竞争加剧）
    "down_green": "#2E9E6B",      # 跌（分数线下降）
    "text_main": "#1A1A1A",       # 标题、正文
    "text_secondary": "#6B7280",  # 说明、注释
    "bg_white": "#FFFFFF",        # 图卡底
    "bg_light": "#F8FAFC",        # 浅底
}

# ---------- 字体 ----------
FONT_FAMILY = "SimHei"                 # 黑体：无衬线、数字清晰
FONT_PATH = "C:/Windows/Fonts/simhei.ttf"

# ---------- 水印参数（见方案第七章） ----------
WATERMARK = {
    "logo_text": "HSEE",               # 角标 logo
    "source_text": "数据来源：HSEE · 深圳教育局",  # 数据来源声明
    "diagonal_text": "HSEE",           # 半透明斜纹文字
    "diagonal_alpha": 0.07,            # 斜纹透明度（6-10%，防截但不毁观感）
    "logo_alpha": 0.9,
}

# ---------- 满分（用于跨年份归一化） ----------
SCORE_SCALE = {2025: 610, 2026: 630}   # 2025满分610 → 2026满分630

# ---------- 输出规格 ----------
FIGURE_DPI = 150
BODY_SIZE = (9, 5)                     # 正文配图 1200×900 比例


def normalize(score: float, from_year: int, to_year: int) -> float:
    """把 from_year 年份的分数，按满分比例换算到 to_year 分制。"""
    return score * (SCORE_SCALE[to_year] / SCORE_SCALE[from_year])


def setup_style():
    """全局样式初始化：注册中文字体 + 统一默认样式。"""
    if FONT_PATH:
        try:
            fm.fontManager.addfont(FONT_PATH)
        except Exception:
            pass
    plt.rcParams["font.sans-serif"] = [FONT_FAMILY]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = FIGURE_DPI
    plt.rcParams["axes.edgecolor"] = COLORS["text_secondary"]
    plt.rcParams["axes.labelcolor"] = COLORS["text_main"]
    plt.rcParams["text.color"] = COLORS["text_main"]
    plt.rcParams["xtick.color"] = COLORS["text_main"]
    plt.rcParams["ytick.color"] = COLORS["text_main"]
