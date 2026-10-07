# -*- coding: utf-8 -*-
p = r'E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\第01篇-一个妈妈的深夜提问\01.公众号\第01篇-公众号图文样板.html'
txt = open(p, encoding='utf-8').read()
LQ, RQ = '\u201c', '\u201d'
old1 = '<div class="quote"><strong>' + LQ + '查了两周中考志愿攻略，越看心里没底。' + RQ + '</strong></div>'
print('old1 repr:', repr(old1))
# 找所有 查了两周 的位置
import re
for m in re.finditer('查了两周', txt):
    s = m.start()
    print('occurrence at', s, ':', repr(txt[max(0,s-60):s+60]))
