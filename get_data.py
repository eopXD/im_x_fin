import psycopg2
import psycopg2.extras

try:
	conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % 
		('ana.lu.im.ntu.edu.tw', 'im_fin', 'imfin_read1', 'read998811'))
	conn.set_client_encoding('UTF8')
	cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
except psycopg2.DatabaseError, dbnamee:
	print 'DatabaseError in open connection: %s' % dbe

cur.execute("select title,content from twnews where stock_id=2311 limit 10")
res=cur.fetchall()

for x in res:
	for y in x:
		print y
