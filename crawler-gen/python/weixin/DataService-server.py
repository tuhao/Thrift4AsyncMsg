#- * - coding=utf-8  - * -
from db import *
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import DataService
import ConfigParser
import MySQLdb

CFG_FILE = 'mysql.cfg'
CFG_SESSION = 'connect'

class WeixinDB:

	def __init__(self,host,user,passwd,db_name):
		self.conn = MySQLdb.connect(host,user,passwd,db_name)
		self.cursor = self.conn.cursor()

	def query(self,sql_str):
		try:
			self.cursor.execute(sql_str)
			return self.cursor.fetchall()
		except Exception, e:
			print e
		return ()

	def __exit__(self,*kw):
		try:
			self.cursor.close()
			self.conn.commit()
			self.conn.close()
		except Exception, e:
			raise e

	def __enter__(self):
		pass

config = ConfigParser.ConfigParser()
s = lambda name:config.get(CFG_SESSION,name)
with open(CFG_FILE,'r') as cfg:
	config.readfp(cfg)
repo =  WeixinDB(s('host'),s('user'),s('passwd'),s('db_name'))

with repo:
	print repo.query("""show tables""")


class SyncDB(DataService.Iface):

	def pushMsg(self,data):
		for item in data:
			print item.title
		return True

	def pushNews(self,data):
		print data

	def pushString(self,data):
		print data
		return True

def run():
	server_address = 'localhost'
	port = 9090
	transport = TSocket.TServerSocket(server_address,port)
	#transport = TTransport.TFramedTransport(transport)
	transportFactory = TTransport.TBufferedTransportFactory()
	protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()
	handler = SyncDB()
	processor = DataService.Processor(handler)
	server = TServer.TThreadPoolServer(processor,transport,transportFactory,protocolFactory)
	print "Starting thrift server in python..."
	server.serve()

#run()