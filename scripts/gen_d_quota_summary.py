"""查询 A-② D类指标生机会 所需汇总数据。

用法：python gen_d_quota_summary.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg2  # noqa: E402

DSN = "postgresql://hsee:devpassword@localhost:5432/hsee"

conn = psycopg2.connect(DSN)
cur = conn.cursor()

cur.execute("""
SELECT
  SUM("AC类名额分配") AS ac_total,
  SUM("D类名额分配") AS d_total,
  COUNT(*) FILTER (WHERE "D类名额分配" > 0) AS schools_with_d,
  COUNT(*) AS total_schools
FROM sz_v_quota_summary_readable
WHERE 年度 = 2026 AND 是否公办 = true
""")
ac_total, d_total, schools_with_d, total_schools = cur.fetchone()
print(f"全市公办指标生名额：AC类 {ac_total} 人，D类 {d_total} 人")
print(f"有D类名额的学校：{schools_with_d} / {total_schools} 所")
print(f"D类占全部指标生名额：{d_total / (ac_total + d_total) * 100:.1f}%")

cur.execute("""
SELECT "学校名称", "AC类名额分配", "D类名额分配", "名额分配总数", "所在区域"
FROM sz_v_quota_summary_readable
WHERE 年度 = 2026 AND 是否公办 = true AND "D类名额分配" > 0
ORDER BY "D类名额分配" DESC
LIMIT 15
""")
print("\n=== D类指标生名额 Top15 ===")
for name, ac, d, total, region in cur.fetchall():
    print(f"{name:<20} AC {ac:>4} D {d:>4} 总 {total:>4} (D占{d / total * 100:.0f}%) {region}")

cur.execute("""
SELECT "学校名称", "AC类名额分配", "D类名额分配", "名额分配总数"
FROM sz_v_quota_summary_readable
WHERE 年度 = 2026 AND 是否公办 = true AND "D类名额分配" > 0 AND "名额分配总数" > 100
ORDER BY ("D类名额分配"::float / "名额分配总数") DESC
LIMIT 10
""")
print("\n=== D类名额占比最高的10所（D类机会相对大）===")
for name, ac, d, total in cur.fetchall():
    print(f"{name:<20} AC {ac:>4} D {d:>4} D占{d / total * 100:.0f}%")

conn.close()
