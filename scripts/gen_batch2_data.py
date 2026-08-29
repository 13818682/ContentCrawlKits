"""查询 A-② D类指标生 + B-① 公办线边缘 所需数据。

用法：python gen_batch2_data.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg2  # noqa: E402

from hsee_charts import db  # noqa: E402

DSN = "postgresql://hsee:devpassword@localhost:5432/hsee"

# === B-① 公办线边缘：低AC线公办校 ===
rows = db.query_acd_diff(year="2026")
low = [r for r in rows if r[1] <= 520]
low.sort(key=lambda r: r[1])
print("=== B-① 公办线边缘公办校（AC线 ≤ 520，按AC升序）===")
print(f"共 {len(low)} 所")
print(f"{'学校':<18} {'AC':>5} {'D':>5} {'差':>4}")
for name, ac, d, diff in low:
    print(f"{name:<18} {ac:>5} {d:>5} {diff:>+4}")

if low:
    print(f"\n最低公办AC线：{low[0][1]} 分（{low[0][0]}）")
    print(f"最低公办D线：{min(r[2] for r in low)} 分")

# === A-② D类指标生：quota/allocation 表探查 ===
conn = psycopg2.connect(DSN)
cur = conn.cursor()
cur.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema='public' AND table_name LIKE 'sz_%'
    ORDER BY table_name
""")
tables = [r[0] for r in cur.fetchall()]
quota_tables = [t for t in tables if "quota" in t or "allocation" in t]
print(f"\n=== quota/allocation 表: {quota_tables} ===")
for qt in quota_tables:
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name=%s ORDER BY ordinal_position
    """, (qt,))
    cols = [r[0] for r in cur.fetchall()]
    print(f"  {qt}: {cols}")
    try:
        cur.execute(f"SELECT * FROM {qt} LIMIT 3")
        for r in cur.fetchall():
            print(f"    样例: {r}")
    except Exception as e:
        print(f"    查询失败: {e}")

conn.close()
