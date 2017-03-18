# -*- coding: utf-8 -*-

import csv, codecs, string, cStringIO
import codecs
import re
from datetime import datetime
#load known Chinese phrase
import jieba
jieba.load_userdict('text/words.dic')

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

#Count Chinese Phrase Frequency
class gen_feature:
    def __init__(self):
        self.all_tokens = dict()
        self.para_count = 0
        self.total_wc = 0
        self.cstop = []
        self.re_float = re.compile('([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
    def addcstop(self, stoplist):
        self.cstop.extend(stoplist)
    
    def process_tokens(self, tokens):
        for at  in tokens:
            at = at.strip(' ;=.-,/()%:"[]*\n')
            if len(at) == 0:
                continue            
            if at in self.cstop:                
                continue
            rem1 = self.re_float.findall(at)
            if len(rem1) > 0:
                continue
                
            self.total_wc +=  1            
            
            if self.all_tokens.has_key(at):
                self.all_tokens[at] += 1
            else:
                self.all_tokens[at] = 1
                
                
feat1 = gen_feature()
feat1.addcstop([u'\u3000', '~', '!', '?'])
stoplist = "text/cstop.dic"
fstop1 = codecs.open(stoplist,'r',encoding='utf8')
cstop=[]
for aline in fstop1:
    aline = aline.strip()
    atoken = aline.split(' ')[0]
    cstop.append(atoken)    
fstop1.close()
feat1.addcstop(cstop)


infile = "text/samplenews_500.csv"
fh1=codecs.open(infile,'rb',encoding='utf8')
reader = unicode_csv_reader(fh1)
cid_title = 4 #title column
cid_content=5 #content column

header= reader.next()
cc=0
for arow in reader:    
    cc=cc+1    
    strall = arow[cid_title] + "\n" + arow[cid_content]    
    words =jieba.cut(strall, cut_all = False)    
    feat1.process_tokens(words)    
fh1.close()

tmpkeys=sorted(feat1.all_tokens, key=feat1.all_tokens.get, reverse=True)
topn=30
c1=0

res=[]
for atoken in tmpkeys:
    c1=c1+1    
    if c1 < topn:
        res.append("%s ->%d\n" % (atoken, feat1.all_tokens[atoken]))
    else:
        break

outcsv="out/output_freq.csv"
fh = codecs.open(outcsv, 'wb')
writer = UnicodeWriter(fh)

writer.writerow(res)

fh.close()