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
#=============def csv read
import csv, codecs, string, cStringIO

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
#==============end csv read and write

#Build ctop(終止符號) list=============================
re_float = re.compile('([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
cstop = ['NumWord', u'\u3000', '~', '!', '?']
stoplist = "text/cstop.dic"
fstop1 = codecs.open(stoplist,'r',encoding='utf8')
for aline in fstop1:
    aline = aline.strip()
    atoken = aline.split(' ')[0]
    cstop.append(atoken)
    #print aline

fstop1.close()
#End Build============================================

jieba.load_userdict('text/newword.txt')
infile = "text/samplenews_500.csv"
fh1=codecs.open(infile,'rb',encoding='utf8')
reader = unicode_csv_reader(fh1)
cid_title = 4 #title column
cid_content=5 #content column
header= reader.next()

words=[]
for x in reader:
	strall=x[cid_title] + "\n" + x[cid_content]
	tmp=jieba.cut(strall,cut_all=False)
	for y in tmp:
		words.append(y)
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

outcsv="out/output_pos_neg.csv"
fh = codecs.open(outcsv, 'wb')
writer = UnicodeWriter(fh)

writer.writerow("=========================")
writer.writerow("|    POSITIVE FOUND     |")
writer.writerow("=========================")
writer.writerow(pos)

writer.writerow("=========================")
writer.writerow("|    NEGATIVE FOUND     |")
writer.writerow("=========================")
writer.writerow(neg)

fh.close()