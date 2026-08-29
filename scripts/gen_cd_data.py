"""查询 C区（区域分层）+ D区（指标生校内竞争）所需数据。

用法：python gen_cd_data.py
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg2  # noqa: E402

DSN = "postgresql://hsee:devpassword@localhost:5432/hsee"

conn = psycopg2.connect(DSN)
cur = conn.cursor()

# === C区：各区公办高中分布（第一批 AC/D 线） ===
cur.execute("""
SELECT district, school_name,
       MAX(COALESCE(score_ac_boarding, score_ac_day, score_acd, score_ac)) AS ac,
       MAX(COALESCE(score_d_boarding, score_d_day, score_acd, score_d)) AS d
FROM sz_v_school_scores_timeline
WHERE code_batch='first' AND public_private='公办' AND score_year='2026'
GROUP BY district, school_name
HAVING MAX(COALESCE(score_ac_boarding, score_ac_day, score_acd, score_ac)) IS NOT NULL
ORDER BY district, ac DESC
""")
by_district = defaultdict(list)
for dist, name, ac, d in cur.fetchall():
    by_district[dist].append((name, ac, d))

print("=== C区：各区公办高中分布（第一批）===")
print(f"{'区':<8} {'学校数':>5} {'AC线区间':>18}")
for dist in sorted(by_district, key=lambda x: -len(by_district[x])):
    rows = by_district[dist]
    acs = [r[1] for r in rows]
    print(f"{dist:<8} {len(rows):>5} {min(acs):>4}~{max(acs)}")

print("\n=== 各区学校明细（AC线降序）===")
for dist in sorted(by_district, key=lambda x: -len(by_district[x])):
    print(f"\n【{dist}】{len(by_district[dist])}所")
    for name, ac, d in by_district[dist]:
        print(f"  {name:<20} AC {ac:>4} D {d if d else '-':>4}")

# === D区：指标生校内竞争（各初中分到的名额） ===
cur.execute("""
SELECT COUNT(DISTINCT junior_high_name) FROM sz_quota_allocations WHERE year = 2026
""")
total_jh = cur.fetchone()[0]
cur.execute("""
SELECT junior_high_name, SUM(quota_count) AS total
FROM sz_quota_allocations
WHERE year = 2026
GROUP BY junior_high_name
ORDER BY total DESC
LIMIT 20
""")
print(f"\n=== D区：指标生校内竞争（共 {total_jh} 所初中，Top20 按分到名额）===")
for name, total in cur.fetchall():
    print(f"  {name:<24} {total} 个名额")

conn.close()
