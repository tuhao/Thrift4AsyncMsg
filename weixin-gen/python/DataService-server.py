#- * - coding=utf-8  - * -
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import DataService
import ConfigParser
import MySQLdb
import sys
import time
import datetime

CFG_FILE = 'mysql.cfg'
CFG_SESSION = 'connect'

class WeixinDB:

	def __init__(self,host,user,passwd,db_name):
		self.conn = MySQLdb.connect(host,user,passwd,db_name)
		self.cursor = self.conn.cursor()

	def execute(self,sql_str):
		try:
			self.cursor.execute(sql_str)
			return self.cursor.fetchall()
		except Exception, e:
			print e
		return ()

	def last_record(self):
		return self.cursor.lastrowid

	def __exit__(self,*kw):
		self.conn.commit()

	def __enter__(self):
		pass

	def close(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()


class SyncDB(DataService.Iface):

	def pushMsg(self,data):
		try:
			start = time.localtime(time.time())
			create_time = datetime.datetime(*start[:6])
			with repo:
				for msg in data:
					sql = 'insert into signature_message (title,create_time,content) values ("%s","%s","%s")' % (msg.title,create_time,msg.content)
					repo.execute(sql)
		except Exception, e:
			print e
			return False
		else:
			return True

	def pushNews(self,data):
		try:
			with repo:
				start = time.localtime(time.time())
				create_time = datetime.datetime(*start[:6])
				for news in data:
					sql = 'insert into signature_news (title,create_time) values("%s","%s")' % (news.title,create_time)
					repo.execute(sql)
					news_id = repo.last_record()
					for article in news.articles:
						sql = 'insert into signature_article (news_id,title,description,pic,url) values (%d,"%s","%s","%s","%s")' % (news_id,
							article.title,article.description,article.imageurl,article.url)
						repo.execute(sql)
		except Exception, e:
			print e
			return False
		else:
			return True
		

	def pushString(self,data):
		print data
		return True

argi = 1
server_address = '192.168.1.101'
port = 9090

if len(sys.argv) > 1:
	if sys.argv[argi] == '-h':
		parts = sys.argv[argi+1].split(':')
  		server_address = parts[0]
  		argi = argi + 1
  		if len(parts) > 1:
    			port = int(parts[1])
    			argi = argi + 1

    	if sys.argv[argi] == '-cfg':
    		CFG_FILE = sys.argv[argi+1]

config = ConfigParser.ConfigParser()
s = lambda name:config.get(CFG_SESSION,name)
with open(CFG_FILE,'r') as cfg:
	config.readfp(cfg)
repo =  WeixinDB(s('host'),s('user'),s('passwd'),s('db_name'))

transport = TSocket.TServerSocket(server_address,port)
transportFactory = TTransport.TFramedTransportFactory()
protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()
handler = SyncDB()
processor = DataService.Processor(handler)
server = TServer.TThreadPoolServer(processor,transport,transportFactory,protocolFactory)
print "Starting thrift server in python..."
server.serve()