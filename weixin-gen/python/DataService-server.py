#coding=utf-8

from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from ttypes import *
from MySQLClient import WeixinDB
import DataService
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding='utf-8'

class ThriftHandler(DataService.Iface):

	def pushMsg(self,data):
		count = 0
		create_time =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with repo:
			for msg in data:
				try:
					sql = 'insert into signature_message (title,create_time,content,reason,sort_id) values ("%s","%s","%s","%s",%d)' % (msg.title,create_time,msg.content,None,1)
					repo.execute_insert(sql)
					count = count + 1
				except Exception, e:
					print e
					print ' at %s' % (create_time)
		print 'insert %d messages at %s' % (count,create_time)
		if count > 0:
			return True
		else:
			return False

	def pushNews(self,data):
		try:
			with repo:
				start = time.localtime(time.time())
				create_time = datetime.datetime(*start[:6])
				for news in data:
					sql = 'insert into signature_news (title,create_time) values("%s","%s")' % (news.title,create_time)
					repo.execute_insert()(sql)
					news_id = repo.last_record()
					for article in news.articles:
						sql = 'insert into signature_article (news_id,title,description,pic,url) values (%d,"%s","%s","%s","%s")' % (news_id,
							article.title,article.description,article.imageurl,article.url)
						repo.execute_insert(sql)
		except Exception, e:
			print e
			print ' at %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			return False
		else:
			return True
		

	def pushString(self,data):
		print data
		return True

	def pullMsg(self,size):
		count = 0
		create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		result = list()
		with repo:
			sql = "select * from signature_message order by id desc limit %d " % (int(size))
			try:
				query_tuple = repo.execute_query(sql)
			except Exception,e:
				print e
				print ' at %s' % (create_time)
			else:
				for item in query_tuple:
					try:
						reason = item[4]
						if reason is None:
							reason = 'None'
						result.append(Message(title=item[1].encode('utf-8'),create_time=str(item[2]),content=item[3].encode('utf-8'),reason=reason.encode('utf-8')))
						count = count + 1
					except Exception, e:
						print e
						print ' at %s' % (create_time)
					except MemoryError,er:
							print er
							print ' at %s' % (create_time)
		print 'pull %d messages at %s' % (count,create_time)
		return result


	def pullMsgBySort(self,size,sort_id):
		result = list()
		count = 0
		create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with repo:
				try:
					sql = "select * from signature_message where sort_id = %d order by id desc limit %d " % (int(sort_id),int(size))
					query_tuple = repo.execute_query(sql)
				except Exception,e:
					print e
					print ' at %s' % (create_time)
				else:
					for item in query_tuple:
						try:
							reason = item[4]
							if reason is None:
								reason = 'None'
							result.append(Message(id=int(item[0]),title=item[1].encode('utf-8'),create_time=str(item[2]),content=item[3].encode('utf-8'),reason=reason.encode('utf-8'),sort_id=int(item[5])))
							count = count + 1
						except Exception, e:
							print e
							print ' at %s' % (create_time)
						except MemoryError,er:
							print er
							print ' at %s' % (create_time)
		print 'pull %d messages at %s' % (count,create_time)
		return result

argi = 1
server_address = '192.168.1.103'
port = 9090

if len(sys.argv) > 1:
	if sys.argv[argi] == '-h':
		parts = sys.argv[argi+1].split(':')
  		server_address = parts[0]
  		argi = argi + 2
  		if len(parts) > 1:
    			port = int(parts[1])

    	if sys.argv[argi] == '-cfg':
    		CFG_FILE = sys.argv[argi+1]


repo =  WeixinDB()
transport = TSocket.TServerSocket(server_address,port)
transportFactory = TTransport.TFramedTransportFactory()
protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()
handler = ThriftHandler()
processor = DataService.Processor(handler)
server = TServer.TThreadPoolServer(processor,transport,transportFactory,protocolFactory)
print "Starting thrift server in python..."
server.serve()
