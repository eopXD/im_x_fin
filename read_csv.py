# -*- coding: utf-8 -*-
import csv, codecs
#=======Define CSV Reader and Writer for UTF-8 encoding
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

infile = "/text/samplenews_500.csv"
fh1=codecs.open(infile,'rb',encoding='utf8')
reader = unicode_csv_reader(fh1)
cid_title = 4 #title column
cid_content=5 #content column

header= reader.next()
cc=0
for arow in reader:    
    cc=cc+1    
    strall = arow[cid_title] + "\n" + arow[cid_content]    
    print "%d:%s" % (cc, arow[cid_title])
    if cc>10:
        break
fh1.close()

    
