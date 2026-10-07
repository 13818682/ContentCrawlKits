# -*- coding: utf-8 -*-
"""按《00-创作规范与背景》§4.1 口径统计 8 篇改稿正文字数（非空白字符，含前情行，不含标题/分隔线/署名/来源/配图标注）"""
import re, os
root = r'E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿'
dirs = {
    '01': ('第01篇-一个妈妈的深夜提问', '第01篇-一个妈妈的深夜提问-公众号-优化意见与改稿.md'),
    '02': ('第02篇-家长最常卡住的五个地方', '第02篇-家长最常卡住的五个地方-公众号-优化意见与改稿.md'),
    '03': ('第03篇-这个念头我放了很多年', '第03篇-这个念头我放了很多年-公众号-优化意见与改稿.md'),
    '04': ('第04篇-说干就干我们是怎么开始的', '第04篇-说干就干我们是怎么开始的-公众号-优化意见与改稿.md'),
    '05': ('第05篇-四座城市我们一座一座来', '第05篇-四座城市我们一座一座来-公众号-优化意见与改稿.md'),
    '06': ('第06篇-为什么我们不直接抄网上的分数线', '第06篇-为什么我们不直接抄网上的分数线-公众号-优化意见与改稿.md'),
    '07': ('第07篇-初二家长现在做这三件事', '第07篇-初二家长现在做这三件事-公众号-优化意见与改稿.md'),
    '08': ('第08篇-四座城市都齐了', '第08篇-四座城市都齐了-公众号-优化意见与改稿.md'),
}
for k, (d, f) in dirs.items():
    p = os.path.join(root, d, '01.公众号', f)
    txt = open(p, encoding='utf-8').read()
    m = txt.find('## 二、改后全文')
    body = txt[m:] if m >= 0 else ''
    cnt = 0
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith('#'):
            continue
        if re.fullmatch(r'-{3,}', s):
            continue
        if s.startswith('*小洁｜'):
            continue
        if s.startswith('本文涉及'):
            continue
        if s.startswith('【配图建议'):
            continue
        if '配图建议' in s:
            continue
        cnt += len(re.sub(r'\s', '', s))
    print(f'第{k}篇: {cnt} 非空白字符')
