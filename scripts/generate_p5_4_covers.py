"""试点脚本：为 P5-4《分数线复盘》生成封面/首图。

跑通"封面生成"环节，产出 3 个平台的封面（标题区+数据区+品牌区三段式）：
  1. 公众号封面 900×383（2.35:1）
  2. 小红书首图 1080×1440（3:4）
  3. 今日头条封面 1200×900

用法：python generate_p5_4_covers.py
"""
import os

from hsee_charts import cover

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    # 1. 公众号封面（横版）
    cover.render_cover(
        os.path.join(OUT_DIR, "p5-4-封面-公众号.png"),
        tag="P5 · 录取后行动指南",
        title="深圳中考分数线复盘：满分610变630，涨跌背后的真相",
        data_text="四大名校归一化后几乎没变",
        data_num="±1分",
        width=900, height=383,
    )

    # 2. 小红书首图（竖版）
    cover.render_cover(
        os.path.join(OUT_DIR, "p5-4-首图-小红书.png"),
        tag="2026深圳中考",
        title="分数线“全线大涨”？真相是满分变了",
        data_text="归一化后四大名校基本没变",
        data_num="±1分",
        width=1080, height=1440,
    )

    # 3. 今日头条封面（横版三图之一）
    cover.render_cover(
        os.path.join(OUT_DIR, "p5-4-封面-今日头条.png"),
        tag="深圳中考 · 数据复盘",
        title="2026分数线“暴涨”的真相：满分变了，涨跌怎么算",
        data_text="四大名校归一化后真实涨跌",
        data_num="±1分",
        width=1200, height=900,
    )

    print("封面生成完成，输出目录：", os.path.abspath(OUT_DIR))


if __name__ == "__main__":
    main()
