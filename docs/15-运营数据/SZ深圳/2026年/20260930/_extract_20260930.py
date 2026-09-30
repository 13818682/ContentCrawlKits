# -*- coding: utf-8 -*-
"""20260930 运营数据抽取器（只读）

为什么不用 openpyxl：头条那 5 个 xlsx 是 WPS 导出的，样式表缺默认 Fill，
openpyxl 直接抛 `expected <class 'openpyxl.styles.fills.Fill'>`。
故**绕过样式层**，直接解 xlsx 的 XML（sharedStrings + sheet），数据一点不少。

微信公众号的 `user_analysis.xls` 实为 **HTML 表格**（不是真 xls），单独用 HTML 解析。

用法：python _extract_20260930.py [平台关键字]
     不带参数 = 全部dump
"""
import sys, os, re, glob, zipfile, html
from xml.etree import ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
HERE = os.path.dirname(os.path.abspath(__file__))


def col_idx(ref):
    """A1 -> 0, B1 -> 1 ..."""
    m = re.match(r"([A-Z]+)", ref or "")
    if not m:
        return 0
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def xlsx_sheets(path):
    """返回 [(sheet_name, [[cell,...],...]), ...]，纯 XML 解析，容忍 WPS 文件。"""
    out = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(f"{NS}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = {}
        if "xl/_rels/workbook.xml.rels" in names:
            rr = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
            for rel in rr:
                rels[rel.get("Id")] = rel.get("Target")
        for sh in wb.iter(f"{NS}sheet"):
            title = sh.get("name")
            rid = sh.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            tgt = rels.get(rid, "")
            p = "xl/" + tgt.lstrip("/").replace("xl/", "")
            if p not in names:
                continue
            root = ET.fromstring(z.read(p))
            rows = []
            for r in root.iter(f"{NS}row"):
                cells = {}
                for c in r.findall(f"{NS}c"):
                    i = col_idx(c.get("r"))
                    v = c.find(f"{NS}v")
                    if c.get("t") == "s" and v is not None:
                        val = shared[int(v.text)]
                    elif c.get("t") == "inlineStr":
                        val = "".join(t.text or "" for t in c.iter(f"{NS}t"))
                    else:
                        val = v.text if v is not None else None
                    cells[i] = val
                if cells:
                    w = max(cells) + 1
                    rows.append([cells.get(i) for i in range(w)])
            out.append((title, rows))
    return out


def html_tables(path):
    """user_analysis.xls 实为 HTML，抽 <table>。"""
    raw = open(path, "rb").read().decode("utf-8", "ignore")
    tables = []
    for t in re.findall(r"<table.*?</table>", raw, re.S | re.I):
        rows = []
        for tr in re.findall(r"<tr.*?</tr>", t, re.S | re.I):
            cells = [html.unescape(re.sub(r"<.*?>", "", c)).strip()
                     for c in re.findall(r"<t[dh].*?</t[dh]>", tr, re.S | re.I)]
            if any(cells):
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables


def show(name, rows, limit=None):
    print(f"--- {name}  rows={len(rows)}")
    for i, r in enumerate(rows[:limit] if limit else rows):
        print("  ", r)


def main():
    kw = sys.argv[1] if len(sys.argv) > 1 else ""
    for p in sorted(glob.glob(os.path.join(HERE, "*", "*"))):
        rel = os.path.relpath(p, HERE)
        if kw and kw not in rel:
            continue
        print("=" * 78)
        print("FILE:", rel)
        try:
            if p.lower().endswith(".xls") and not p.lower().endswith(".xlsx"):
                raw = open(p, "rb").read(8)
                if raw.startswith(b"<html") or b"<html" in raw:
                    for i, t in enumerate(html_tables(p)):
                        show(f"{os.path.basename(p)} [html table {i}]", t)
                else:
                    import xlrd
                    wb = xlrd.open_workbook(p)
                    for ws in wb.sheets():
                        show(f"{ws.name}", [ws.row_values(i) for i in range(ws.nrows)])
            else:
                for title, rows in xlsx_sheets(p):
                    show(title, rows)
        except Exception as e:
            print("  ERR:", type(e).__name__, e)


if __name__ == "__main__":
    main()
