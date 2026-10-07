# -*- coding: utf-8 -*-
p = r'E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\第01篇-一个妈妈的深夜提问\01.公众号\第01篇-公众号图文样板.html'
txt = open(p, encoding='utf-8').read()
lines = txt.splitlines()
for no in (189, 190, 245, 246):
    if no - 1 < len(lines):
        print(f'--- line {no} ---')
        print(repr(lines[no-1]))
