# -*- coding: utf-8 -*-
"""
头条「日更条数」A/B 对照结算工具（QA-005 09-10 双条实验）
================================================================
用法：
    python _tt_daily_ab.py                # 默认读脚本所在目录
    python _tt_daily_ab.py <数据目录>      # 指定目录

实验设计（09-10 定，见 00-问答专区-平台内容清单与发布登记表.md）：
    处理组 09-10 = 长文 ×2（P1-4 主线《投档规则》20:20 ＋ QA-005《未来学位》21:30）＋ 微头条 18:00
    对照组 09-11 = 长文 ×1（S1《志愿顺序》20:20）     ＋ 微头条
    基线   09-06~09-08 = 「长文×1＋微头条」常规节奏，净增粉 +11/2 天
    唯一变量 = 头条「多一条长文」

判读规则（见 20260911-09-10双条发布策略评估与同题对标.md §4.2）：
    展现 ≥ 25,000 且 涨粉 ≥ +4   → 双条有效
    展现 15,000~25,000 或 +2~+3   → 中性
    展现 < 15,000 且 涨粉 ≤ +1    → 双条无效/有害 → 回到严格 1 条/天

注：本仓头条导出的 xlsx 由 WPS 生成，openpyxl 读样式会报
    "Fill() takes no arguments"，故直接解压解析 XML。
"""
import sys, os, re, glob, zipfile
from xml.etree import ElementTree as ET

M = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
NS = {'m': M[1:-1]}

TREAT, CTRL = '2026-09-10', '2026-09-11'
BASELINE = ['2026-09-06', '2026-09-07', '2026-09-08']


def read_xlsx(path):
    """→ [[cell, ...], ...]（取第一个 sheet）"""
    z = zipfile.ZipFile(path)
    shared = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
            shared.append(''.join(t.text or '' for t in si.iter(M + 't')))
    sheet = sorted(n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml$', n))[0]
    rows = []
    for row in ET.fromstring(z.read(sheet)).iter(M + 'row'):
        cells = []
        for c in row:
            t, v, isn = c.get('t'), c.find('m:v', NS), c.find('m:is', NS)
            if t == 's' and v is not None:
                cells.append(shared[int(v.text)])
            elif t == 'inlineStr' and isn is not None:
                cells.append(''.join(x.text or '' for x in isn.iter(M + 't')))
            else:
                cells.append(v.text if v is not None else '')
        rows.append(cells)
    return rows


def newest(d, pat):
    hits = glob.glob(os.path.join(d, pat))
    if not hits:
        sys.exit(f'!! 未找到文件：{pat}')
    return max(hits, key=os.path.getmtime)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def load(d):
    """→ {date: {...}}"""
    trend = read_xlsx(newest(d, '今日头条数据趋势_*.xlsx'))
    fans = read_xlsx(newest(d, '今日头条粉丝趋势_*.xlsx'))

    hdr = trend[0]
    idx = {h: i for i, h in enumerate(hdr)}
    need = ['展现量', '粉丝展现量', '阅读(播放)量', '粉丝阅读(播放)量', '点赞量', '评论量']
    for k in need:
        if k not in idx:
            sys.exit(f'!! 趋势表缺列：{k}（实际表头 {hdr}）')

    data = {}
    for r in trend[1:]:
        if not r or not re.match(r'\d{4}-\d{2}-\d{2}', r[0] or ''):
            continue          # 跳过「总计」行与空行
        data[r[0]] = {k: num(r[idx[k]]) for k in need}

    for r in fans[1:]:
        if not r or not re.match(r'\d{4}-\d{2}-\d{2}', r[0] or ''):
            continue
        d = r[0]
        if d in data:
            data[d]['总粉丝数'] = num(r[1])
            data[d]['净增粉'] = num(r[2])
            data[d]['活跃粉丝'] = num(r[5]) if len(r) > 5 else 0
    return data


def ctr(v):
    return f"{v['阅读(播放)量'] / v['展现量'] * 100:.2f}%" if v['展现量'] else '—'


def line(d, v):
    return (f"{d}  展现{v['展现量']:>8,.0f}  阅读{v['阅读(播放)量']:>7,.0f}  "
            f"点击率{ctr(v):>7}  粉丝展现{v['粉丝展现量']:>6,.0f}  "
            f"净增粉{v.get('净增粉', 0):>+5.0f}  活跃{v.get('活跃粉丝', 0):>4,.0f}")


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    data = load(d)

    print('=' * 92)
    print('头条「日更条数」A/B 结算 · 数据目录：', d)
    print('=' * 92)
    for dt in sorted(data):
        print(line(dt, data[dt]))

    print('\n' + '=' * 92)
    print('对照组：09-06~09-08（长文×1 ＋ 微头条）')
    print('=' * 92)
    base = [data[x] for x in BASELINE if x in data]
    if base:
        n = len(base)
        for x in BASELINE:
            if x in data:
                print(line(x, data[x]))
        b_imp = sum(v['展现量'] for v in base) / n
        b_rd = sum(v['阅读(播放)量'] for v in base) / n
        b_f = sum(v.get('净增粉', 0) for v in base)
        print(f"  均值   展现{b_imp:>8,.0f}  阅读{b_rd:>7,.0f}  "
              f"净增粉合计{b_f:>+.0f}（{b_f / n:+.1f}/天）")

    if TREAT not in data:
        print(f'\n!! 缺 {TREAT} 数据行'); return
    if CTRL not in data:
        print(f'\n{"!" * 92}')
        print(f'!! {CTRL} 全天数据尚未导出 —— 实验无法结算。')
        print(f'!! 请于 {CTRL} 结束后（次日）从头条后台导出「数据趋势」+「粉丝趋势」')
        print(f'!! 覆盖到 {CTRL}，放入本目录后重跑本脚本。')
        print('!' * 92)
        return

    t, c = data[TREAT], data[CTRL]
    print('\n' + '=' * 92)
    print('结算：09-10（长文×2） vs 09-11（长文×1）—— 唯一变量 = 多一条长文')
    print('=' * 92)
    print(line(TREAT + ' [处理组·2条]', t))
    print(line(CTRL + ' [对照组·1条]', c))
    di = c['展现量'] - t['展现量']
    dr = c['阅读(播放)量'] - t['阅读(播放)量']
    df = c.get('净增粉', 0) - t.get('净增粉', 0)
    print(f"{'差异':>12}  展现{di:>+8,.0f}（{di / t['展现量'] * 100:+.1f}%）  "
          f"阅读{dr:>+7,.0f}（{dr / t['阅读(播放)量'] * 100:+.1f}%）  净增粉{df:>+5.0f}")

    imp, f = c['展现量'], c.get('净增粉', 0)
    if imp >= 25000 and f >= 4:
        verdict, act = '✅ 双条有效', '保留「重要节点加发一条」的弹性'
    elif imp < 15000 and f <= 1:
        verdict, act = '🔴 双条无效/有害', '回到严格 1 条/天，并复核「同账号日更互抢曝光池」假设'
    else:
        verdict, act = '⚠️ 中性', '维持 1 条/天，不加发'
    print(f"\n判读：{verdict}   （判定输入：09-11 展现 {imp:,.0f} / 净增粉 {f:+.0f}）")
    print(f"动作：{act}")

    # 归一化效率（剔除推荐量波动的影响）
    print(f"\n归一化：每万展现净增粉")
    for dt in BASELINE + [TREAT, CTRL]:
        if dt in data and data[dt]['展现量']:
            v = data[dt]
            print(f"  {dt}  {(v.get('净增粉', 0) / v['展现量'] * 10000):>+6.2f}")

    # 同向校验：若 09-11 展现仍在下行，单看绝对值会误判「双条有害」
    pre = [data[x]['展现量'] for x in ['2026-09-08', '2026-09-09'] if x in data]
    if pre and t['展现量'] < sum(pre) / len(pre) * 0.7:
        print("\n⚠️ 提醒：09-10 展现较前两日均值已跌 >30%，")
        print("   该下行趋势在 09-10 之前就开始了（见上文逐日表），")
        print("   故 09-11 的高低不能单独归因于「双条」。请对照归一化指标综合判断。")


if __name__ == '__main__':
    main()
