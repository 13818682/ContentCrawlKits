"""给内容终稿文章 frontmatter 回填分人群标签（audience/quadrant/region）。

对齐 docs/12-细分市场内容专区规划.md §1.2 标签规范。
仅处理 `-公众号-终稿.md` 文件；幂等（已有 audience/region 字段则跳过）。

用法：python tag_articles.py
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.abspath(os.path.join(BASE, "..", "docs", "03-内容创作-深圳中考志愿填报"))

# article_id -> 标签。P3-5 四个子文件分别用 P3-5 / P3-5-02 / -03 / -04。
TAGS = {
    "P1-3":    {"audience": ["D类", "AC类"], "quadrant": "焦虑求助型"},
    "P1-6":    {"audience": ["AC类"], "quadrant": "自信DIY型"},
    "P2-1":    {"audience": ["AC类", "D类"]},
    "P2-2":    {"audience": ["AC类", "D类"]},
    "P3-2":    {"audience": ["D类"]},
    "P3-3":    {"audience": ["全部"]},
    "P3-4":    {"audience": ["D类", "临界生"]},
    "P3-5":    {"audience": ["临界生"]},
    "P3-5-02": {"audience": ["临界生"]},
    "P3-5-03": {"audience": ["临界生"]},
    "P3-5-04": {"audience": ["临界生"]},
    "P3-6-1":  {"audience": ["AC类"], "quadrant": "自信DIY型"},
    "P3-6-2":  {"audience": ["临界生"]},
    "P3-6-3":  {"audience": ["D类"]},
    "P3-6-6":  {"region": ["全市"]},
    "P4-2":    {"audience": ["全部"]},
    "P4-3":    {"audience": ["D类"], "quadrant": "焦虑求助型"},
    "P4-5":    {"audience": ["临界生"], "quadrant": "临界求生型"},
    "P4-9":    {"audience": ["临界生"], "quadrant": "临界求生型"},
    "P4-10":   {"audience": ["临界生"], "quadrant": "临界求生型"},
    "P5-2":    {"audience": ["临界生", "D类"], "quadrant": "临界求生型"},
    "P5-3":    {"audience": ["临界生"], "quadrant": "临界求生型"},
}


def iter_final_files():
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith("-公众号-终稿.md"):
                yield os.path.join(root, f)


def extract_article_id(text):
    m = re.search(r'^article:\s*"([^"]+)"', text, re.MULTILINE)
    return m.group(1) if m else None


def build_tag_lines(tags):
    lines = []
    if "audience" in tags:
        lines.append('audience: [' + ", ".join(f'"{v}"' for v in tags["audience"]) + "]")
    if "quadrant" in tags:
        lines.append(f'quadrant: "{tags["quadrant"]}"')
    if "region" in tags:
        lines.append('region: [' + ", ".join(f'"{v}"' for v in tags["region"]) + "]")
    return lines


def insert_tags(text, tag_lines):
    """在 frontmatter 的 article: 行之后插入标签行，保留原换行符。"""
    m = re.search(r'^article:\s*"[^"]*"[ \t]*(\r?\n)', text, re.MULTILINE)
    if not m:
        return None
    nl = m.group(1)  # 原文件该行换行符
    insert = "".join(f"{tl}{nl}" for tl in tag_lines)
    return text[: m.end()] + insert + text[m.end():]


def main():
    changed, skipped = [], []
    for path in iter_final_files():
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        aid = extract_article_id(text)
        if aid not in TAGS:
            skipped.append(("未在映射", os.path.relpath(path, CONTENT_DIR)))
            continue
        if re.search(r'^audience:', text, re.MULTILINE) or re.search(r'^region:', text, re.MULTILINE):
            skipped.append(("已打标", os.path.relpath(path, CONTENT_DIR)))
            continue
        new_text = insert_tags(text, build_tag_lines(TAGS[aid]))
        if new_text is None:
            skipped.append(("无article锚点", os.path.relpath(path, CONTENT_DIR)))
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        changed.append((aid, os.path.relpath(path, CONTENT_DIR)))

    print(f"已回填标签：{len(changed)} 个文件")
    for aid, rel in sorted(changed):
        print(f"  [{aid}] {rel}")
    print(f"\n跳过：{len(skipped)} 个")
    for why, rel in skipped:
        print(f"  {why}: {rel}")


if __name__ == "__main__":
    main()
