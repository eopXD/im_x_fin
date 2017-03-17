# -*- coding: utf-8 -*-
import jieba
jieba.load_userdict('/text/newword.txt')
asent = u"民進黨立委林岱樺日前在主持動保法修法協商時，一席「放生論」引起爭議，就連黨內同志都嚴厲批評，林岱樺因此被網友戲稱「放生立委」。"
words =jieba.cut(asent, cut_all = False)
tmp1 = "/".join(words)
print tmp1
