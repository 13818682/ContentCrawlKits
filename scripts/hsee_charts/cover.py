"""封面/首图生成（HTML 模板 + Edge headless 截图）。

见 10-发布素材自动化方案 第五章：模板化（标题区 + 数据区 + 品牌区三段式），
复用 config 设计 token，保证与数据图同源配色、同源品牌。
"""
import os
import subprocess
import tempfile

from . import config

EDGE_PATH = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

# 字体栈（微软雅黑渲染最佳，黑体兜底）
FONT_STACK = '"Microsoft YaHei", "PingFang SC", "SimHei", sans-serif'


def _css():
    c = config.COLORS
    return f"""
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: {_css_body_width}px; height: {_css_body_height}px;
      font-family: {FONT_STACK};
      background: linear-gradient(135deg, {c['brand_blue']} 0%, #174A82 100%);
      color: #ffffff;
      overflow: hidden;
    }}
    .wrap {{ width: 100%; height: 100%; padding: {_css_pad}px; display: flex; flex-direction: column; }}
    .tag {{
      font-size: {_css_tag}px; color: {c['accent_orange']}; font-weight: bold;
      letter-spacing: 2px; border-left: 4px solid {c['accent_orange']}; padding-left: 10px;
    }}
    .title {{ font-size: {_css_title}px; font-weight: bold; line-height: 1.28; margin-top: {_css_gap}px; }}
    .data {{
      margin-top: {_css_gap2}px; display: inline-block; align-self: flex-start;
      background: rgba(255,255,255,0.12); border-radius: 12px; padding: 14px 20px;
      font-size: {_css_data}px; font-weight: bold;
    }}
    .data .num {{ color: {c['accent_orange']}; }}
    .footer {{
      margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end;
      font-size: 12px; color: rgba(255,255,255,0.75);
    }}
    .footer .brand {{ font-size: 14px; font-weight: bold; color: #ffffff; letter-spacing: 1px; }}
    """


# 布局参数按横版/竖版区分（模块级变量，_css() 读取）
_css_body_width = 900
_css_body_height = 383
_css_pad = 36
_css_tag = 15
_css_title = 36
_css_data = 22
_css_gap = 22
_css_gap2 = 24


def _set_layout(width, height):
    global _css_body_width, _css_body_height, _css_pad, _css_tag, _css_title, _css_data, _css_gap, _css_gap2
    _css_body_width, _css_body_height = width, height
    portrait = height > width
    if portrait:
        _css_pad, _css_tag = 56, 22
        _css_title = 64
        _css_data = 40
        _css_gap, _css_gap2 = 40, 44
    else:
        _css_pad, _css_tag = 36, 15
        _css_title = 36
        _css_data = 22
        _css_gap, _css_gap2 = 22, 24


def _build_html(tag, title, data_text, data_num):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{_css()}</style></head>
<body><div class="wrap">
  <div class="tag">{tag}</div>
  <div class="title">{title}</div>
  <div class="data">{data_text} <span class="num">{data_num}</span></div>
  <div class="footer">
    <div>{config.WATERMARK['source_text']}</div>
    <div class="brand">{config.WATERMARK['logo_text']}</div>
  </div>
</div></body></html>"""


def render_cover(out_path, tag, title, data_text, data_num, width, height):
    """生成一张封面图：写 HTML → Edge headless 截图。

    - tag: 系列/品类标签（如 "P5 · 录取后行动指南"）
    - title: 主标题
    - data_text: 数据说明（如 "四大名校归一化后"）
    - data_num: 核心数据（如 "±1分"）
    - width/height: 输出尺寸（如公众号 900×383，小红书 1080×1440）
    """
    _set_layout(width, height)
    html = _build_html(tag, title, data_text, data_num)

    tmp_html = os.path.join(tempfile.gettempdir(), "hsee_cover_tmp.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    out_abs = os.path.abspath(out_path)
    cmd = [
        EDGE_PATH, "--headless=new", "--disable-gpu",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        f"--screenshot={out_abs}",
        "file:///" + tmp_html.replace("\\", "/"),
    ]
    subprocess.run(cmd, capture_output=True, timeout=60)
    return out_abs
