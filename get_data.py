import os
import re
import csv
import copy
import random
import jieba
import codecs 
from datetime import datetime

import psycopg2
import psycopg2.extras

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
	conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % 
		('ana.lu.im.ntu.edu.tw', 'im_fin', 'imfin_read1', 'read998811'))
	conn.set_client_encoding('UTF8')
	cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
except psycopg2.DatabaseError, dbnamee:
	print 'DatabaseError in open connection: %s' % dbe

cur.execute("select title,content from twnews where stock_id=2707  limit 10")
res=cur.fetchall()

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
#==============end csv read and write

outcsv="out/output_data.csv"
fh = codecs.open(outcsv, 'wb')
writer = UnicodeWriter(fh)
writer.writerows(res)
fh.close()
