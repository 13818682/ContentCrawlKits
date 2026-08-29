"""HSEE 数据库查询封装（PostgreSQL）。

数据源视图：sz_v_school_scores_timeline（2023-2026 历年录取分数线）。
AC线/D线取值顺序：住宿线 → 走读线 → 合并线 → 兜底。
"""
import psycopg2

DSN = "postgresql://hsee:devpassword@localhost:5432/hsee"

# AC线/D线的字段取值优先级（先住宿、后走读、再合并/兜底）
_AC_COLS = "COALESCE(score_ac_boarding, score_ac_day, score_acd, score_ac)"
_D_COLS = "COALESCE(score_d_boarding, score_d_day, score_acd, score_d)"


def get_conn():
    return psycopg2.connect(DSN)


def query_ac_scores(years=("2025", "2026"), limit=20):
    """查询公办第一批学校的 AC 线，返回 [(school_name, ac_prev, ac_cur), ...]。

    ac_prev = 上一个年份的AC线，ac_cur = 当前年份的AC线（按 ac_cur 降序）。
    """
    y_prev, y_cur = years
    sql = f"""
    WITH ac AS (
      SELECT school_name,
        MAX(CASE WHEN score_year = %s THEN {_AC_COLS} END) AS ac_prev,
        MAX(CASE WHEN score_year = %s THEN {_AC_COLS} END) AS ac_cur
      FROM sz_v_school_scores_timeline
      WHERE code_batch = 'first' AND student_category = 'AC' AND public_private = '公办'
      GROUP BY school_name
    )
    SELECT school_name, ac_prev, ac_cur
    FROM ac
    WHERE ac_prev IS NOT NULL AND ac_cur IS NOT NULL
    ORDER BY ac_cur DESC NULLS LAST
    LIMIT %s
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (y_prev, y_cur, limit))
        return cur.fetchall()


def query_all_ac_lines(year="2026"):
    """查询公办第一批学校某年的 AC 线（全部学校），按 AC 线降序。

    返回 [(school_name, ac_line), ...]。用于梯队分布等全景图。
    """
    sql = f"""
    SELECT school_name, MAX({_AC_COLS}) AS ac_line
    FROM sz_v_school_scores_timeline
    WHERE code_batch = 'first' AND student_category = 'AC'
      AND public_private = '公办' AND score_year = %s
    GROUP BY school_name
    HAVING MAX({_AC_COLS}) IS NOT NULL
    ORDER BY ac_line DESC NULLS LAST
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (year,))
        return cur.fetchall()


def query_acd_diff(year="2026"):
    """查询公办第一批学校的 AC/D 分差（D线 - AC线），按 AC线 降序，返回全部学校。

    返回 [(school_name, ac_line, d_line, diff), ...]。
    由调用方自行决定取"顶尖校"（按AC线）还是"溢价最高校"（按diff）。
    """
    sql = f"""
    WITH d AS (
      SELECT school_name, MAX({_D_COLS}) AS d_line
      FROM sz_v_school_scores_timeline
      WHERE code_batch = 'first' AND student_category = 'D'
        AND public_private = '公办' AND score_year = %s
      GROUP BY school_name
    ),
    ac AS (
      SELECT school_name, MAX({_AC_COLS}) AS ac_line
      FROM sz_v_school_scores_timeline
      WHERE code_batch = 'first' AND student_category = 'AC'
        AND public_private = '公办' AND score_year = %s
      GROUP BY school_name
    )
    SELECT a.school_name, a.ac_line, d.d_line, (d.d_line - a.ac_line) AS diff
    FROM ac a JOIN d ON a.school_name = d.school_name
    WHERE a.ac_line IS NOT NULL AND d.d_line IS NOT NULL
    ORDER BY a.ac_line DESC NULLS LAST
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (year, year))
        return cur.fetchall()
