# -*- coding: utf-8 -*-
"""检查各文件引号字符的实际码点分布"""
import os, collections

ROOT = r'E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿'
files = {
    '01': os.path.join(ROOT, '第01篇-一个妈妈的深夜提问', '01.公众号', '第01篇-一个妈妈的深夜提问-公众号-优化意见与改稿.md'),
    '03': os.path.join(ROOT, '第03篇-这个念头我放了很多年', '01.公众号', '第03篇-这个念头我放了很多年-公众号-优化意见与改稿.md'),
    '06': os.path.join(ROOT, '第06篇-为什么我们不直接抄网上的分数线', '01.公众号', '第06篇-为什么我们不直接抄网上的分数线-公众号-优化意见与改稿.md'),
    'html': os.path.join(ROOT, '第01篇-一个妈妈的深夜提问', '01.公众号', '第01篇-公众号图文样板.html'),
}
for k, p in files.items():
    txt = open(p, encoding='utf-8').read()
    cnt = collections.Counter(ch for ch in txt if ch in '\u0022\u201c\u201d\u2018\u2019\uff02\u300c\u300d')
    print(k, dict(cnt))
# 定位 06 篇 570 行实际字符
p = files['06']
txt = open(p, encoding='utf-8').read()
i = txt.find('570')
print('06 570 ctx:', repr(txt[i-30:i+30]))
