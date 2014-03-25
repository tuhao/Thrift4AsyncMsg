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
		repo =  WeixinDB()
		count = 0
		create_time =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with repo:
			for msg in data:
				try:
					sql = 'insert into approve_metadata (title,create_time,content,reason,sort_id) values (%s,%s,%s,%s,%s)' 
					repo.execute_insert(sql,(msg.title,create_time,msg.content,'None',1))
					count = count + 1
				except Exception, e:
					print e
					print ' at %s' % (create_time)
		print 'insert %d messages at %s to approve_metadata' % (count,create_time)
		if count == len(data):
			return True
		else:
			return False

	def pushNews(self,data):
		repo = WeixinDB()
		with repo:
			start = time.localtime(time.time())
			create_time = datetime.datetime(*start[:6])
			for news in data:
				try:
					sql = 'insert into signature_news (title,create_time) values(%s,%s)'
					repo.execute_insert(sql,(news.title,create_time))
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

	def gen_query_tuple(self,sql_str,*param):
		count = 0
		result = list()
		create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		repo = WeixinDB()
		with repo:
			try:
				query_tuple = repo.execute_query(sql_str,param[0]) 
			except Exception, e:
				print e
				print ' at %s' % (create_time)
			else:
				for item in query_tuple:
					try:
						reason = item[4]
						if reason is None:
							reason = 'None'
						result.append(Message(id=item[0],title=item[1].encode('utf-8'),create_time=str(item[2]),content=item[3].encode('utf-8'),reason=reason.encode('utf-8'),sort_id=item[5]))
						count = count + 1
					except Exception, e:
						print e
						print ' at %s' % (create_time)
					except MemoryError,er:
						print er
						print ' at %s' % (create_time)
		print 'pull %d messages at %s ' % (count,create_time)
		return result

	def gen_query_number(self,sql_str):
		result = 0
		create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		repo = WeixinDB()
		with repo:
			try:
				query_tuple = repo.execute_query(sql_str)
			except Exception, e:
				print e
				print 'at %s ' % (create_time)
			else:
				for item in query_tuple:
					try:
						result = int(item[0])
						break
					except Exception, e:
						print e
						print ' at %s' % (create_time)
		return result

	def gen_push_msg(self,sql_str,data):
		repo =  WeixinDB()
		count = 0
		create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with repo:
			for msg in data:
				try:
					repo.execute_insert(sql_str,(msg.title,create_time,msg.content,msg.reason,msg.sort_id))
					count = count + 1
				except Exception, e:
					print e
					print ' at %s' % (create_time)
		print 'insert %d messages at %s to WeixinDB'  % (count,create_time)
		return count

	def gen_delete_msg(self,sql_str,ids):
		action_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		repo = WeixinDB()
		count = 0
		with repo:
			for msg_id in ids:
				try:
					if repo.execute_delete(sql_str,(int(msg_id))):
						count = count + 1
				except Exception, e:
					print e
					print ' at %s' % (action_time)
			print 'delete %d messages at %s from WeixinDB' %(count,action_time)
			if count == len(ids):
				return True
			else:
				return False

	def pullMsg(self,size):
		sql_str = "select * from approve_metadata order by id desc limit %s "
		return self.gen_query_tuple(sql_str, (size))

	def pullMsgBySort(self,size,sort_id):
		sql_str = "select * from approve_metadata where sort_id = %s order by id desc limit %s "
		return self.gen_query_tuple(sql_str, (sort_id,size))

	def pullPaginateMsg(self,start_index,item_num):
		sql_str = "select * from approve_metadata order by id desc limit %s,%s "
		return self.gen_query_tuple(sql_str, (start_index,item_num))

	def pullPaginateMsgBySort(self,start_index,item_num,sort_id):
		sql_str = "select * from approve_metadata where sort_id = %s order by id desc limit %s,%s "
		return self.gen_query_tuple(sql_str,(sort_id,start_index,item_num))

	def getMsgCount(self):
		sql_str = "select count(*) from approve_metadata "
		return self.gen_query_number(sql_str)

	def getMsgCountBySort(self,sort_id):
		sql_str = "select count(*) from approve_metadata where sort_id = %d " % (sort_id)
		return self.gen_query_number(sql_str)

	def pushApprove(self,data):
		sql_str = 'insert into signature_message (title,create_time,content,reason,sort_id) values (%s,%s,%s,%s,%s)' 
		return self.gen_push_msg(sql_str,data)

	def pushDelicious(self,data):
		sql_str = 'insert into approve_deliciousdata (title,create_time,content,reason,sort_id) values (%s,%s,%s,%s,%s)' 
		return self.gen_push_msg(sql_str, data)

	def pushHealthy(self,data):
		sql_str = 'insert into approve_healthydata  (title,create_time,content,reason,sort_id) values (%s,%s,%s,%s,%s)' 
		return self.gen_push_msg(sql_str, data)

	def pullApprove(self,start_index,item_num):
		sql_str = "select * from signature_message order by id desc limit %s,%s "
		return self.gen_query_tuple(sql_str, (start_index,item_num))

	def pullDelicious(self,start_index,item_num):
		sql_str = "select * from approve_deliciousdata order by id desc limit %s,%s "
		return self.gen_query_tuple(sql_str, (start_index,item_num))

	def pullHealthy(self,start_index,item_num):
		sql_str = "select * from approve_healthydata order by id desc limit %s,%s "
		return self.gen_query_tuple(sql_str,(start_index,item_num))

	def getApproveCount(self):
		sql_str = "select count(*) from signature_message "
		return self.gen_query_number(sql_str)

	def getDeliciousCount(self):
		sql_str = "select count(*) from approve_deliciousdata "
		return self.gen_query_number(sql_str)
	
	def getHealthyCount(self):
		sql_str = "select count(*) from approve_healthydata "
		return self.gen_query_number(sql_str)

	def msgSortMark(self,ids,sort_id):
		repo = WeixinDB()
		create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		count = 0
		with repo:
			for msg_id in ids:
				try:
					sql_str = 'update approve_metadata set sort_id = %d where id = %d ' % (sort_id,msg_id)
					repo.execute_query(sql_str)
					count = count + 1
				except Exception, e:
					print e
					print ' at %s' % (create_time)
		print 'update %d messages sort_id to %d at %s in approve_metadata' %(count,sort_id,create_time)
		if count == len(ids) :
			return True
		else:
			return False


	def deleteMsgs(self,ids):
		sql_str = "delete from signature_message where id = '%s' "
		return self.gen_delete_msg(sql_str, ids)

	def deleteMeta(self,ids):
		sql_str = "delete from approve_metadata where id = '%s' "
		return self.gen_delete_msg(sql_str, ids)

	def deleteDelicious(self,ids):
		sql_str = "delete from approve_deliciousdata where id = '%s' "
		return self.gen_delete_msg(sql_str, ids)

	def deleteHealthy(self,ids):
		sql_str = "delete from approve_healthydata where id = '%s' "
		return self.gen_delete_msg(sql_str,ids)



argi = 1
server_address = '192.168.1.102'
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

transport = TSocket.TServerSocket(server_address,port)
transportFactory = TTransport.TFramedTransportFactory()
protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()
handler = ThriftHandler()
processor = DataService.Processor(handler)
server = TServer.TThreadPoolServer(processor,transport,transportFactory,protocolFactory)
print "Starting thrift server in python..."
server.serve()
