# -*- coding: utf-8 -*-
import re
p = r'E:\1.HSEE\6.ContentCrawlKits\docs\03-内容创作\_跨城系列-小洁查志愿\第01篇-一个妈妈的深夜提问\01.公众号\第01篇-公众号图文样板.html'
txt = open(p, encoding='utf-8').read()
LQ, RQ = '\u201c', '\u201d'

def convert_html(txt):
    blocks = re.findall(r'<style.*?</style>', txt, re.S)
    masked = re.sub(r'<style.*?</style>', '\x00', txt, flags=re.S)
    out = []
    in_tag = False
    q = 0
    for ch in masked:
        if ch == '<':
            in_tag = True
            out.append(ch)
        elif ch == '>':
            in_tag = False
            out.append(ch)
        elif ch == '"' and not in_tag:
            q += 1
            out.append(LQ if q % 2 == 1 else RQ)
        else:
            out.append(ch)
    result = ''.join(out)
    for i, b in enumerate(blocks):
        result = result.replace('\x00', b, 1)
    return result, q, masked

# 重建"转换前"状态：当前文件已是转换后；先看当前是否含直引号
print('当前直引号数:', txt.count('"'), '弯引号对数:', txt.count(LQ))
i = txt.find('只认')
print('当前只认 ctx:', repr(txt[i-20:i+40]))
# 尝试把当前弯引号还原为直引号（模拟转换前）再重跑转换
restored = txt.replace(LQ, '"').replace(RQ, '"')
new, q, masked = convert_html(restored)
j = new.find('只认')
print('重跑后只认 ctx:', repr(new[j-20:j+40]))
print('重跑 q =', q)
