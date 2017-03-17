# -*- coding: utf-8 -*-
import jieba
import codecs, string, cStringIO
import re
jieba.load_userdict('/text/newword.txt')

re_float = re.compile('([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
stoplist = "/text/cstop.dic"
fstop1 = codecs.open(stoplist,'r',encoding='utf8')
cstop=[]
for aline in fstop1:
    aline = aline.strip()
    atoken = aline.split(' ')[0]
    cstop.append(atoken)    
fstop1.close()

asent = u"民進黨立委林岱樺日前在主持動保法修法協商時，一席「放生論」引起爭議，就連黨內同志都嚴厲批評，林岱樺因此被網友戲稱「放生立委」。"
words =jieba.cut(asent, cut_all = False)

res=[]
for at in words:
	at = at.strip(' ;=.-,/()%:"[]*\n')
	if len(at) == 0:
		continue
	if at in cstop:
		continue
	rem1 = re_float.findall(at)
	if len(rem1) > 0:
		continue
	res.append(at)

tmp1 = "/".join(res)
print tmp1
