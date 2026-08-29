"""查询 D类分数线地图所需数据并打印，供文章撰写使用。

用法：python gen_d_class_data.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsee_charts import db  # noqa: E402

rows = db.query_acd_diff(year="2026")
print(f"共 {len(rows)} 所学校（公办第一批，AC/D 线齐全）\n")

# 分差统计
diffs = [r[3] for r in rows]
print(f"D类-AC分差：范围 {min(diffs)} ~ {max(diffs)} 分，均值 {sum(diffs)/len(diffs):.1f} 分")
low = [r for r in rows if r[3] <= 4]
mid = [r for r in rows if 4 < r[3] <= 15]
high = [r for r in rows if r[3] > 15]
print(f"  分差≤4（友好/顶尖）: {len(low)} 所")
print(f"  分差5-15: {len(mid)} 所")
print(f"  分差>15（D类溢价高）: {len(high)} 所\n")

# 梯队分布（按 AC 线，对齐 P3-3 划分）
TIERS = [
    ("第一梯队·四大(AC≥587)", 587, 999),
    ("第二梯队·八大/十大(AC 570-586)", 570, 586),
    ("第三梯队·二十大/三十强(AC 540-569)", 540, 569),
    ("第四梯队·五十强(AC 500-539)", 500, 539),
    ("第五梯队·百强/新校(AC<500)", 0, 499),
]
print("=== 梯队分布（按 AC 线） ===")
for label, lo, hi in TIERS:
    tier = [r for r in rows if lo <= r[1] <= hi]
    d_lines = [r[2] for r in tier]
    if tier:
        print(f"{label}: {len(tier)} 所，D线 {min(d_lines)}~{max(d_lines)}，平均分差 {sum(r[3] for r in tier)/len(tier):.1f}")
    else:
        print(f"{label}: 0 所")

print("\n=== 全表（按 AC 线降序） ===")
print(f"{'学校':<12} {'AC':>5} {'D':>5} {'差':>4}")
for name, ac, d, diff in rows:
    print(f"{name:<12} {ac:>5} {d:>5} {diff:>+4}")

print("\n=== D类线最高的20所（按 D线降序） ===")
for name, ac, d, diff in sorted(rows, key=lambda r: -r[2])[:20]:
    print(f"{name:<12} D线 {d:>4} (AC {ac:>4}, 差 {diff:+d})")

print("\n=== D类最友好（分差最小）的15所 ===")
for name, ac, d, diff in sorted(rows, key=lambda r: r[3])[:15]:
    print(f"{name:<12} AC {ac:>4} D {d:>4} 差 {diff:+d}")

print("\n=== D类溢价最高（分差最大）的15所 ===")
for name, ac, d, diff in sorted(rows, key=lambda r: -r[3])[:15]:
    print(f"{name:<12} AC {ac:>4} D {d:>4} 差 {diff:+d}")
