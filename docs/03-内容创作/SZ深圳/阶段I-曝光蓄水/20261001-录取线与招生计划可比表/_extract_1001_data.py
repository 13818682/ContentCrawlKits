# -*- coding: utf-8 -*-
"""20261001 · 数据抽取与 JOIN 核验（**只读、不产图**）

目的：把两份**官方原件级**数据拼成一张「各校可比表」，并逐条核验。
  源 A（招生计划·官方原件 xlsx）：
      E:/1.HSEE/1.HSEE-Prj/0GD.深圳资料/3.政策文件资料/
      1.深圳市2026年公办普通高中学校招生计划表.xlsx
      → 101 所 × 招生总人数 / 住宿 / 走读 / D 类生名额
  源 B（录取线·仓内终稿 md）：
      docs/03-内容创作/SZ深圳/P3-数据择校地图/P3-2-AC-D分差排行/
      01-P3-2-AC类vsD类分差排行榜…-公众号-终稿.md
      → 81 所 AC/D 住宿线（该稿自带一处列错位 bug，见 09-26 合规清单）

用法：python _extract_1001_data.py
"""
import io, os, re, sys

XLSX = ("E:/1.HSEE/1.HSEE-Prj/0GD.深圳资料/3.政策文件资料/"
        "1.深圳市2026年公办普通高中学校招生计划表.xlsx")
P32 = ("E:/1.HSEE/6.ContentCrawlKits/docs/03-内容创作/SZ深圳/P3-数据择校地图/"
       "P3-2-AC-D分差排行/01-P3-2-AC类vsD类分差排行榜：哪些学校对D类最友好-公众号-终稿.md")


def norm(s):
    """校名归一：全/半角括号统一、去空白、去校区后缀噪音。"""
    if s is None:
        return ""
    s = str(s)
    for a, b in [("（", "("), ("）", ")"), ("　", ""), (" ", ""), ("\n", "")]:
        s = s.replace(a, b)
    return s.strip()


def base_name(s):
    """去掉括号里的别名/校区说明，便于兜底匹配。"""
    return re.sub(r"\(.*?\)", "", norm(s))


# 两表校名不一致的人工别名表（P3-2 终稿 → 官方计划表）。
# 归一化只能解决全/半角括号与空格，**缩写与全称必须人工对齐**。
ALIAS = {
    "深大附中中心校区": "深圳大学附属中学中心校区(深大附中中心校区)",
    "北师大南山附属学校": "北京师范大学南山附属学校",
    "西交利物浦大学基础教育集团外国语高中": "西交利物浦大学基础教育集团外国语高级中学",
    "中科附高": "中国科学院深圳理工大学附属实验高级中学(中科附高)",
}


# ---------- 源 B：P3-2 终稿表格 ----------
def load_scores():
    txt = io.open(P32, encoding="utf-8").read()
    out = {}
    for line in txt.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        name = cells[0]
        if name in ("学校", "") or set(name) <= set("-: "):
            continue
        # 期望：学校|区域|等级|AC住宿|D住宿|分差|友好度
        def num(x):
            m = re.search(r"-?\d+", x.replace("*", ""))
            return int(m.group()) if m else None
        ac, dd = num(cells[3]), num(cells[4])
        if ac is None and dd is None:
            continue
        out[norm(name)] = {"name_md": name, "area": cells[1], "level": cells[2],
                           "ac": ac, "d": dd}
    return out


# ---------- 源 A：官方招生计划 xlsx ----------
def load_plan():
    import openpyxl
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb.worksheets[0]
    rows, total = [], 0
    for r in ws.iter_rows(min_row=2, values_only=True):
        no, name, lvl, nature, tot, board, day, scope, memo, area = (list(r) + [None] * 10)[:10]
        name = (name or "").strip()
        if not name or not isinstance(tot, (int, float)):
            continue
        m = re.search(r"D类生\s*(\d+)\s*人", str(scope or "").replace("\n", ""))
        d_qty = int(m.group(1)) if m else None
        if str(scope or "").startswith("面向深汕"):
            d_qty = 0
        rows.append({"no": no, "name": name, "lvl": lvl, "tot": int(tot),
                     "board": board, "day": day, "d_qty": d_qty,
                     "scope": str(scope or "").replace("\n", ""), "area": area})
        total += int(tot)
    return rows, total


def main():
    scores = load_scores()
    plan, grand = load_plan()
    print(f"[源B] P3-2 终稿有分数学校: {len(scores)} 所")
    print(f"[源A] 官方计划表数据行: {len(plan)} 行，招生总人数合计 = {grand:,}")

    by_full, by_base = {}, {}
    for p in plan:
        by_full.setdefault(norm(p["name"]), p)
        by_base.setdefault(base_name(p["name"]), p)

    joined, miss = [], []
    for k, s in scores.items():
        alias = norm(ALIAS.get(s["name_md"], ""))
        p = (by_full.get(alias) or by_base.get(alias)
             or by_full.get(k) or by_base.get(k)
             or by_full.get(base_name(k)) or by_base.get(base_name(k)))
        if p:
            joined.append((s, p))
        else:
            miss.append(s["name_md"])

    print(f"\n[JOIN] 成功 {len(joined)} / 失败 {len(miss)}")
    if miss:
        print("  未匹配:", "、".join(miss))

    print("\n[按 AC 住宿线降序 · 全部命中行]")
    print(f"{'学校':<26}{'区域':<6}{'AC':>5}{'D':>5}{'招生':>7}{'住宿':>7}{'走读':>7}{'D类名额':>9}")
    for s, p in sorted(joined, key=lambda x: -(x[0]["ac"] or 0)):
        print(f"{s['name_md'][:24]:<26}{s['area']:<6}{s['ac'] or '—':>5}",
              f"{s['d'] or '—':>5}{p['tot']:>7}{str(p['board']):>7}{str(p['day']):>7}"
              f"{str(p['d_qty'] if p['d_qty'] is not None else '—'):>9}")

    # 校验：官方 D 类名额合计 vs 录取线表里 D 类生的口径
    dsum = sum(p["d_qty"] for _, p in joined if p["d_qty"])
    print(f"\n[校验] 命中行 D 类生名额合计 = {dsum:,}")
    print(f"[校验] 全表 D 类生名额合计 = "
          f"{sum(p['d_qty'] for p in plan if p['d_qty']):,}")

    # ---------- 找「海报数字」候选：规模 × 门槛 的可比关系 ----------
    print("\n[分析 1] 招生总人数 Top 10（规模最大的是不是门槛最低？）")
    for s, p in sorted(joined, key=lambda x: -x[1]["tot"])[:10]:
        print(f"  {s['name_md']:<22} 招生{p['tot']:>5}  AC{s['ac']:>4}  D{s['d']:>4}"
              f"  D类名额{p['d_qty']:>4}  走读{p['day']}")

    print("\n[分析 2] AC 住宿线分档 × 学校数 / 招生人数合计")
    bands = [(580, 999, "580+"), (560, 579, "560-579"), (540, 559, "540-559"),
             (520, 539, "520-539"), (500, 519, "500-519"), (0, 499, "≤499")]
    for lo, hi, lab in bands:
        grp = [(s, p) for s, p in joined if s["ac"] and lo <= s["ac"] <= hi]
        print(f"  {lab:<9} {len(grp):>3} 所   招生合计 {sum(p['tot'] for _, p in grp):>6}"
              f"   D类名额合计 {sum(p['d_qty'] or 0 for _, p in grp):>5}")

    print("\n[分析 3] 走读生占比 Top 8（走读 = 不住校，家远就得排除）")
    for s, p in sorted(joined, key=lambda x: -(x[1]["day"] if isinstance(x[1]["day"], (int, float)) else 0))[:8]:
        d = p["day"]
        if isinstance(d, (int, float)) and p["tot"]:
            print(f"  {s['name_md']:<22} 走读{d:>4} / 招生{p['tot']:>5}"
                  f" = {d / p['tot'] * 100:.0f}%   AC{s['ac']}")

    print("\n[分析 4] D 类名额 Top 8（非深户最该看的数）")
    for s, p in sorted(joined, key=lambda x: -(x[1]["d_qty"] or 0))[:8]:
        print(f"  {s['name_md']:<22} D类名额{p['d_qty']:>4}  招生{p['tot']:>5}"
              f"  占 {p['d_qty'] / p['tot'] * 100:.0f}%   AC{s['ac']} D{s['d']}")

    # ---------- 落盘：给配图脚本直接 import 的中间数据 ----------
    import json
    out = {"rows": [
        {"name": s["name_md"], "area": s["area"], "ac": s["ac"], "d": s["d"],
         "tot": p["tot"], "board": p["board"], "day": p["day"],
         "d_qty": p["d_qty"], "plan_name": p["name"]}
        for s, p in sorted(joined, key=lambda x: -(x[0]["ac"] or 0))]}
    with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "_rows_1001.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\n[落盘] _rows_1001.json（{len(out['rows'])} 行，按 AC 线降序）")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
