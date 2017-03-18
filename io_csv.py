# -*- coding: utf-8 -*-
import csv, codecs
#=======Define CSV Reader and Writer for UTF-8 encoding
import csv, codecs, string, cStringIO

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),dialect=dialect, **kwargs)
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

infile = "text/samplenews_500.csv"
fh1=codecs.open(infile,'rb',encoding='utf8')
reader = unicode_csv_reader(fh1)
cid_title = 4 #title column
cid_content=5 #content column

header= reader.next()

res=[]
cc=0
for arow in reader:    
    cc=cc+1    
    strall = arow[cid_title] + "\n" + arow[cid_content]    
    res.append(strall)
    if cc>10:
        break
fh1.close()

outcsv="out/output_io.csv"
fh = codecs.open(outcsv, 'wb')
writer = UnicodeWriter(fh)

writer.writerow(res)

fh.close()