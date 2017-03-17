#encoding=utf-8
import os
import re
import csv
import copy
import random
import jieba
import codecs 
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Build ctop(終止符號) list=============================
re_float = re.compile('([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
cstop = ['NumWord', u'\u3000', '~', '!', '?']
stoplist = "cstop.dic"
fstop1 = codecs.open(stoplist,'r',encoding='utf8')
for aline in fstop1:
    aline = aline.strip()
    atoken = aline.split(' ')[0]
    cstop.append(atoken)
    #print aline

fstop1.close()
#End Build============================================

jieba.load_userdict('/text/newword.txt')
asent = u"台泥、台塑鐵橋案澳盛銀登聯貸六強,湯森路透旗下基點雜誌昨（30）日公布最新聯貸統計，今年前三季，\
台灣銀行蟬聯聯貸主辦與管理行雙料冠軍。其中，台銀主辦聯貸市占率達11.94%，擔任管理行的市占率為16.03%，領先銀行同業。\
值得注意的是，名列第六的澳盛銀，是唯一擠入前十名的外銀。據了解，澳盛銀主辦台泥、台塑鐵橋等美元聯貸，\
激烈的聯貸市場上搶贏國銀，引起市場矚目。統計顯示，不包括日本在內的亞太區，今年前三季聯貸主辦龍頭為中國工商銀行，\
市占率為7.7%。積極進軍聯貸市場的澳盛銀行高居第二，市占率為7%。根據湯森路透提供資料顯示，今年前三季，\
不包含日本的亞太區聯貸總額為3,367億美元、1,056筆，金額較去年同期長5.6%。國內銀行過度競爭，企業金融業務競爭激烈，\
聯貸名列前茅的業者，多是資金雄厚的大型公股銀行。第3季台銀主辦南茂科技、中租控股集團海外子公司、威剛科技、\
馥御建設等多起聯貸案；累計前三季主辦48件聯貸案，金額28.37億美元。"
asent=asent.decode('utf8')
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


#Fetch postive list===================================
poslist = []
posfile='text/NTUSD_positive_utf8.txt'
fhp1 = codecs.open(posfile,'r',encoding='utf8')
for aline in fhp1:
    aline = aline.strip()
    poslist.append(aline)
fhp1.close()
#End Build============================================

#Fetch negative list==================================
neglist = []
negfile='text/NTUSD_negative_utf8.txt'
fhp1 = codecs.open(negfile,'r',encoding='utf8')
for aline in fhp1:
    aline = aline.strip()
    neglist.append(aline)
fhp1.close()
#End Build============================================

pos=[x for x in res if x in poslist]
neg=[x for x in res if x in neglist]
print "========================="
print "|    POSITIVE FOUND     |"
print "========================="
for x in pos:
	print x
print "========================="
print "|    NEGATIVE FOUND     |"
print "========================="
for x in neg:
	print x
print "========================="
