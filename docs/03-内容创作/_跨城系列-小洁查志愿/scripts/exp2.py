# -*- coding: utf-8 -*-
p = r'E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\第01篇-一个妈妈的深夜提问\01.公众号\第01篇-公众号图文样板.html'
txt = open(p, encoding='utf-8').read()
LQ, RQ = '\u201c', '\u201d'
old1 = '<div class="quote"><strong>' + LQ + '查了两周中考志愿攻略，越看心里没底。' + RQ + '</strong></div>'
old2 = '我的想法是：<strong>' + LQ + '只认最新的官方正式文件，不听道听途说。' + RQ + '</strong>'
print('old1 count:', txt.count(old1))
print('old2 count:', txt.count(old2))
# 找 190 行引号码点
lines = txt.splitlines()
for ln in lines:
    if 'quote' in ln and '<strong>' in ln:
        for ch in ln:
            if ch in '\u0022\u201c\u201d\u2018\u2019\uff02':
                print('line char:', hex(ord(ch)), repr(ch))
# 检查是否有不可见字符干扰（全角空格等）
i = txt.find('查了两周')
print('before:', [hex(ord(c)) for c in txt[i-8:i]])
print('after :', [hex(ord(c)) for c in txt[i+len('查了两周中考志愿攻略，越看心里没底。'):i+len('查了两周中考志愿攻略，越看心里没底。')+8]])
