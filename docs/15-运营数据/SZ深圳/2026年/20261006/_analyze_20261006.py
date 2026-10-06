# -*- coding: utf-8 -*-
"""20261006 四平台运营数据分析器（只读）

复用 _extract_20261006.py 的解析层（头条 xlsx 为 WPS 导出，openpyxl 打不开，直读 XML）。

本脚本相对 20260930 的**关键差异**：
  本批导出**没有 `流量分析_{ID}` 单篇逐日文件**，而 §3.2 的钉死口径是
  「一律取发布后 D1 + D2，且头条必须用 `流量分析` 的逐日值相加」。
  → 故本脚本**不计算 D1+D2**，改算两条**可严格成立**的东西：
    ① `作品列表` 累计值 = D1+D2 的**上界**（累计 ≥ 任意前缀和）
    ② 与 20260930 那批 `作品列表` 做差 = 老帖的**长尾增量**（09-30 → 10-06）

用法：python _analyze_20261006.py
"""
import os, sys, re, datetime as dt
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _extract_20261006 import xlsx_sheets, html_tables  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = os.path.dirname(HERE)                 # .../2026年
PREV = os.path.join(YEAR, "20260930")

P = lambda *a: os.path.join(HERE, *a)
Q = lambda *a: os.path.join(PREV, *a)


def rows_of(path, sheet=None):
    if path.lower().endswith(".xls"):
        import xlrd
        wb = xlrd.open_workbook(path)
        out = []
        for ws in wb.sheets():
            out += [[("" if v == "" else v) for v in ws.row_values(i)]
                    for i in range(ws.nrows)]
        return out
    for name, rows in xlsx_sheets(path):
        if sheet is None or name == sheet:
            return rows
    raise SystemExit(f"sheet not found: {sheet} in {path}")


def as_f(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


# ---------------------------------------------------------------- 头条 微头条
def parse_tt_weitt(rows):
    """作品列表 → {ID: dict}，按发布时间升序。"""
    hdr = rows[0]
    ci = {h: i for i, h in enumerate(hdr)}
    out = []
    for r in rows[1:]:
        if not r or not r[ci["发布时间"]]:
            continue
        out.append({
            "title": (r[ci["标题"]] or "").replace("\n", " ")[:34],
            "pub": r[ci["发布时间"]],
            "id": r[ci["ID"]],
            "imp": as_f(r[ci["展现量"]]),
            "fans_imp": as_f(r[ci["粉丝展现量"]]),
            "read": as_f(r[ci["阅读量"]]),
            "ctr": r[ci["点击率"]],
            "dwell": as_f(r[ci["平均阅读时长"]]),
            "like": as_f(r[ci["点赞量"]]),
            "cmt": as_f(r[ci["评论量"]]),
            "share": as_f(r[ci["分享量"]]),
            "fav": as_f(r[ci["收藏量"]]),
        })
    out.sort(key=lambda x: x["pub"])
    return out


NOW = parse_tt_weitt(rows_of(P("2.今日头条", "微头条_-_1-38.xlsx")))
OLD = {r["id"]: r for r in parse_tt_weitt(rows_of(Q("2.今日头条", "微头条_-_1-33.xlsx")))}

IDS = [r["id"] for r in NOW]
assert len(IDS) == len(set(IDS)), "微头条 ID 有重复"
assert len(NOW) == 38, f"本批微头条应为 38 条，实为 {len(NOW)}"

# 阶段 I 起点：09-26（首条日更）
PHASE1 = [r for r in NOW if r["pub"] >= "2026-09-26"]
assert len(PHASE1) == 11, f"阶段 I 微头条应为 11 条，实为 {len(PHASE1)}"

print("=" * 100)
print("A. 今日头条 · 微头条：阶段 I 全表（作品列表 = 累计，含导出当日实时）")
print(f"   导出时点：2026-10-06 15:1x（由文件落盘时间推定）")
print("=" * 100)
print(f"{'发布时间':<17}{'展现':>7}{'粉丝展现':>8}{'阅读':>6}{'CTR':>7}{'时长':>5}  {'标题':<30}{'09-30累计':>10}")
for r in PHASE1:
    o = OLD.get(r["id"])
    prev = f"{o['imp']:.0f}" if o else "—（新）"
    print(f"{r['pub']:<17}{r['imp']:>7.0f}{r['fans_imp']:>8.0f}{r['read']:>6.0f}"
          f"{r['ctr']:>7}{r['dwell']:>5.0f}  {r['title']:<30}{prev:>10}")

n_new = sum(1 for r in PHASE1 if r["id"] not in OLD)
print(f"\n   → 本批新增（09-30 导出时还不存在的）：{n_new} 条")

# ------------------------------------------------- B. 上界论证（代替 D1+D2）
print("\n" + "=" * 100)
print("B. ⚠️ D1+D2 无法计算；改用【严格上界】—— 作品列表累计 ≥ D1+D2")
print("=" * 100)
NEW5 = [r for r in PHASE1 if r["id"] not in OLD]
print(f"{'发布时间':<17}{'累计展现(上界)':>14}   {'标题'}")
ub = []
for r in NEW5:
    ub.append(r["imp"])
    print(f"{r['pub']:<17}{r['imp']:>14.0f}   {r['title']}")
ub_sorted = sorted(ub)
med_ub = ub_sorted[len(ub_sorted) // 2]
print(f"\n   10-01~10-05 五条的【上界】排序：{ub_sorted}")
print(f"   → 上界中位 = {med_ub:.0f}")
print(f"   → 上界最大值 = {max(ub):.0f}   （若最大上界都 < 2,500，则真值必然 < 2,500）")
assert med_ub <= 2500, "上界中位不再低于 2500 —— 本节论证失效，需重写"
assert max(ub) <= 2500, f"上界最大 {max(ub)} 已 ≥2500 —— 不能用上界一刀切"

# ------------------------------------------------- C. 老帖长尾（09-30 → 10-06）
print("\n" + "=" * 100)
print("C. 老帖长尾：同一条帖子，09-30 17:03 → 10-06 15:1x（5.9 天）的累计增量")
print("=" * 100)
print(f"{'发布时间':<17}{'09-30累计':>10}{'10-06累计':>10}{'增量':>9}{'增幅':>8}  {'标题'}")
shared = [r for r in PHASE1 if r["id"] in OLD]
deltas = []
for r in shared:
    o = OLD[r["id"]]
    d = r["imp"] - o["imp"]
    deltas.append((r, d, d / o["imp"] * 100 if o["imp"] else 0))
for r, d, pct in deltas:
    print(f"{r['pub']:<17}{OLD[r['id']]['imp']:>10.0f}{r['imp']:>10.0f}{d:>9.0f}{pct:>7.0f}%  {r['title']}")
assert all(d >= -1 for _, d, _ in deltas), "出现负增量 —— 口径不一致，先查再继续"

qd = next((d for r, d, _ in deltas if "跳绳" in r["title"]), None)
print(f"\n   ⚠️ 09-30《跳绳》那次「被压制」判定要复议：它本批已累计 {[r['imp'] for r in PHASE1 if '跳绳' in r['title']][0]:.0f}，"
      f"\n      而 §3.3 记它 D1+D2 只有 218 —— 说明它不是「死掉」，是「起步慢」。")

# ------------------------------------------------- D. 头条 每日账号总量
print("\n" + "=" * 100)
print("D. 今日头条 · 数据趋势（**账号当日总量**，只报完整日；末位 = 10-05）")
print("=" * 100)
sy = rows_of(P("2.今日头条", "数据趋势_445751330880180_2026-09-06-2026-10-05.xlsx"))
art = rows_of(P("2.今日头条", "数据趋势_445751330880180_2026-09-06-2026-10-05 （文章).xlsx"))
wt = rows_of(P("2.今日头条", "数据趋势_445751330880180_2026-09-06-2026-10-05 (微头条).xlsx"))


def daily(rows):
    d = {}
    for r in rows[1:]:
        if r and r[0] and re.match(r"\d{4}-\d{2}-\d{2}", str(r[0])):
            d[str(r[0])] = (as_f(r[1]), as_f(r[3]))
    return d


D_all, D_art, D_wt = daily(sy), daily(art), daily(wt)
assert len(D_wt) == 30 and len(D_art) == 30 and len(D_all) == 30
resid = {k: D_all[k][0] - D_art[k][0] - D_wt[k][0] for k in D_all}
assert all(v >= -1.5 for v in resid.values()), "出现负残差 —— 口径不一致"
print("   ⚠️ 恒等式**不成立**：合计 − 图文 − 微头条 有一个稳定的正残差 =")
print("      既不是图文、也不是微头条的那一体裁（账号自带 / 抖音同步过来的**小视频**）。")
print(f"\n{'日期':<12}{'微头条展现':>10}{'微头条阅读':>10}{'文章展现':>10}{'合计展现':>10}{'残差(小视频)':>13}")
for k in sorted(D_wt)[-15:]:
    print(f"{k:<12}{D_wt[k][0]:>10.0f}{D_wt[k][1]:>10.0f}{D_art[k][0]:>10.0f}"
          f"{D_all[k][0]:>10.0f}{resid[k]:>13.0f}")
first10 = sorted(D_all)[:10]
last10 = sorted(D_all)[-10:]
print(f"\n   残差前 10 天均值 = {sum(resid[k] for k in first10)/10:.0f}"
      f" / 后 10 天均值 = {sum(resid[k] for k in last10)/10:.0f}")
print("   → 残差占比在缩小 = 同步小视频的长尾在自然衰减，不是又发了新视频")

# ------------------------------------------------- E. 小红书
print("\n" + "=" * 100)
print("E. 小红书 · 笔记列表（累计曝光；导出时点 10-06）")
print("=" * 100)
xr = rows_of(P("3.小红书", "笔记列表明细表.xlsx"))
h = xr[1]
xi = {k: i for i, k in enumerate(h)}
XHS = []
for r in xr[2:]:
    if not r or not r[xi["首次发布时间"]]:
        continue
    XHS.append({
        "t": r[xi["笔记标题"]],
        "pub": r[xi["首次发布时间"]],
        "kind": r[xi["体裁"]],
        "imp": as_f(r[xi["曝光"]]),
        "view": as_f(r[xi["观看量"]]),
        "ctr": as_f(r[xi["封面点击率"]]),
        "fav": as_f(r[xi["收藏"]]),
        "fans": as_f(r[xi["涨粉"]]),
        "dwell": as_f(r[xi["人均观看时长"]]),
    })
XHS.sort(key=lambda x: x["pub"])
assert len(XHS) == 32, f"小红书笔记应为 32 条，实为 {len(XHS)}"
X_NEW = [x for x in XHS if x["pub"] >= "2026年10月01日"]
assert len(X_NEW) == 5, f"10-01~10-05 小红书应为 5 条，实为 {len(X_NEW)}"
print(f"{'发布时间':<22}{'曝光':>7}{'观看':>6}{'CTR':>8}{'收藏':>5}{'涨粉':>5}{'时长':>5}  {'标题'}")
for x in X_NEW + [y for y in XHS if "2026年09月" in y["pub"]][-6:]:
    print(f"{x['pub']:<22}{x['imp']:>7.0f}{x['view']:>6.0f}{x['ctr']:>8.3f}{x['fav']:>5.0f}"
          f"{x['fans']:>5.0f}{x['dwell']:>5.0f}  {x['t'][:28]}")

# 小红书 30 日趋势表
view30 = rows_of(P("3.小红书", "近30日观看数据.xlsx"))
tabs = {}
cur = None
for name, rows in xlsx_sheets(P("3.小红书", "近30日观看数据.xlsx")):
    tabs[name] = rows
OV = {r[0]: r[1] for r in tabs["账号总体观看数据"][1:]}
EXP = {re.sub(r"[年月]", "-", r[0]).replace("日", ""): as_f(r[1]) for r in tabs["曝光趋势"][1:]}
VIEW = {re.sub(r"[年月]", "-", r[0]).replace("日", ""): as_f(r[1]) for r in tabs["观看趋势"][1:]}
print("\n   账号总体（近 30 日）：")
for k in ["曝光", "观看", "封面点击率(%)", "平均观看时长(s)", "总完播率(%)",
          "曝光环比(%)", "观看环比(%)", "封面点击率环比(%)", "总完播率环比(%)"]:
    print(f"     {k:<20}{OV.get(k)}")
assert len(EXP) == 30, len(EXP)
print(f"\n   近 10 日 曝光 / 观看：")
for k in sorted(EXP, reverse=True)[:10]:
    ctr = VIEW[k] / EXP[k] if EXP[k] else 0
    print(f"     {k}  曝光{EXP[k]:>7.0f}  观看{VIEW[k]:>6.0f}  CTR {ctr:.3f}")

# ------------------------------------------------- F. 公众号
print("\n" + "=" * 100)
print("F. 微信公众号")
print("=" * 100)
ua = html_tables(P("1.微信公众号", "user_analysis.xls"))[0]
cur_fans = ua[-1][-1]
rows_ua = [r for r in ua[2:] if r and re.match(r"\d{4}-\d{2}-\d{2}", str(r[0]))]
zero_run = 0
for r in reversed(rows_ua):
    if r[3] == "0":
        zero_run += 1
    else:
        break
since = rows_ua[len(rows_ua) - zero_run - 1][0] if zero_run < len(rows_ua) else "—"
print(f"   累积关注 = {cur_fans}；{since} 起连续 {zero_run} 天净增 0"
      f"（覆盖 {rows_ua[-1][0]}）")
assert cur_fans == "26", cur_fans

td = rows_of(P("1.微信公众号", "tendency_1788678582_1791184182.xls"))
pub_days, chan, chan_month, posts = {}, {}, {}, {}
for r in td:
    if len(r) < 15:
        continue
    d, c, v = r[1], r[2], r[3]
    if d and re.match(r"\d{4}-\d{2}-\d{2}", str(d)) and isinstance(v, (int, float)):
        (pub_days if c == "全部" else chan.setdefault(str(d), {}))[str(d)] = float(v)
    src, ttl, rv = r[11], r[13], r[14]
    if src and ttl and isinstance(rv, (int, float)):
        chan_month[src] = chan_month.get(src, 0.0) + float(rv)
        posts[ttl] = posts.get(ttl, 0.0) + float(rv)
assert len(pub_days) == 30, len(pub_days)
print(f"\n   日阅读人数（全部渠道），末 12 天：")
for k in sorted(pub_days)[-12:]:
    bar = "█" * int(pub_days[k])
    print(f"     {k}  {pub_days[k]:>3.0f}  {bar}")
w = sum(pub_days[k] for k in pub_days if k >= "2026-09-26")
print(f"   09-26 ~ 10-05 合计阅读 = {w:.0f}（10 天，日均 {w/10:.1f}）")
print(f"\n   渠道占比（近 30 日）：")
tot_src = sum(chan_month.values())
for k, v in sorted(chan_month.items(), key=lambda x: -x[1]):
    print(f"     {k:<10}{v:>7.0f}   {v/tot_src*100:>5.1f}%")
print(f"\n   单篇阅读 top 6（近 30 日，全部渠道合计）：")
for k, v in sorted(posts.items(), key=lambda x: -x[1])[:6]:
    print(f"     {v:>5.0f}  {k[:44]}")

# ------------------------------------------------- G. 抖音
print("\n" + "=" * 100)
print("G. 抖音")
print("=" * 100)
dy = rows_of(P("4.抖音", "作品列表导出.xlsx"))
hi = {k: i for i, k in enumerate(dy[0])}
works = [r for r in dy[1:] if r and r[hi["发布时间"]]]
works.sort(key=lambda r: r[hi["发布时间"]])
last = works[-1]
print(f"   作品总数 = {len(works)}；末条 = {last[hi['发布时间']]}（体裁 {last[hi['体裁']]}）")
gap = (dt.date(2026, 10, 6) - dt.date(*map(int, last[hi["发布时间"]][:10].split("-")))).days
print(f"   → 距 10-06 已停更 {gap} 天")
assert gap >= 14, f"停更天数 {gap} 异常"
tot = sum(as_f(r[hi["播放量"]]) for r in works)
print(f"   全期播放合计 = {tot:.0f}；完播率非零条数 = "
      f"{sum(1 for r in works if as_f(r[hi['完播率']]) > 0)}/{len(works)}")

# ------------------------------------------------- H. 承接基线（2026-10-06 17:50/17:52 补导）
print("\n" + "=" * 100)
print("H. 承接基线（§八 必填项）—— 三平台粉丝 + 小红书主页漏斗")
print("=" * 100)
FA = rows_of(P("2.今日头条", "粉丝趋势_2026-09-06-2026-10-05.xlsx"))
fi = {k: i for i, k in enumerate(FA[0])}
fans = {r[fi["时间"]]: (as_f(r[fi["总粉丝数"]]), as_f(r[fi["粉丝变化数"]]))
        for r in FA[1:] if r and r[fi["时间"]]}
last_rise = max(k for k, v in fans.items() if v[1] != 0)
zero_run = sum(1 for k in fans if last_rise < k <= "2026-10-05")
print(f"   今日头条：{fans[last_rise][0]:.0f} 人；最后一次增长 = {last_rise}，此后 {zero_run} 天净增 0")
assert zero_run == 13, zero_run

XG = P("3.小红书", "近30日涨粉数据.xlsx")
xt = {n: r for n, r in xlsx_sheets(XG)}


def series(name):
    return {r[0].replace("年", "-").replace("月", "-").replace("日", ""): as_f(r[1])
            for r in xt[name][1:] if r and r[0]}


def blk(d, a, b):
    ks = [k for k in d if a <= k <= b]
    return sum(d[k] for k in ks)


print(f"\n   小红书 30 日总览：")
for r in xt["账号总体涨粉数据"][1:]:
    print(f"     {r[0]:<16}{r[1]}")
fans_s, visit = series("净涨粉趋势"), series("主页访客趋势")
for lab, d in [("净涨粉", fans_s), ("主页访客", visit)]:
    a, b = blk(d, "2026-09-26", "2026-09-30"), blk(d, "2026-10-01", "2026-10-05")
    print(f"     {lab:<8} 09-26~09-30 = {a:>3.0f}   10-01~10-05 = {b:>3.0f}   "
          f"{(b/a-1)*100:+.0f}%")
assert blk(fans_s, "2026-10-01", "2026-10-05") == 0, "10-01~10-05 小红书净涨粉不再是 0"

PB = {n: r for n, r in xlsx_sheets(P("3.小红书", "近30日发布数据.xlsx"))}
pub = {r[0].replace("年", "-").replace("月", "-").replace("日", ""): as_f(r[1])
       for r in PB["总发布趋势"][1:] if r and r[0]}
gap = [k for k in pub if "2026-09-26" <= k <= "2026-10-05" and pub[k] == 0]
print(f"\n   小红书 发布执行：09-26~10-05 共 {blk(pub,'2026-09-26','2026-10-05'):.0f} 条，"
      f"空档 {len(gap)} 天  → {'✅ 零空档' if not gap else '❌ ' + str(gap)}")
assert not gap, gap

print("\n" + "=" * 100)
print("✅ 全部断言通过")
print("=" * 100)
