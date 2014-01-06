#coding=utf-8
import MySQLdb
import ConfigParser
import sys
from ttypes import *
reload(sys)
sys.setdefaultencoding='utf-8'
CFG_FILE = 'mysql.cfg'
CFG_SESSION = 'connect'

class WeixinDB:

	def __init__(self,host,user,passwd,db_name,charset):
		self.conn = MySQLdb.connect(host,user,passwd,db_name,charset=charset)
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

config = ConfigParser.ConfigParser()
s = lambda name:config.get(CFG_SESSION,name)
with open(CFG_FILE,'r') as cfg:
	config.readfp(cfg)
repo =  WeixinDB(s('host'),s('user'),s('passwd'),s('db_name'),s('charset'))

pagesize = 100
sql = """select * from signature_message order by id desc limit """ + str(pagesize)
result = list()
for item in repo.execute(sql):
	if item[4] is None:
		result.append(Message(title=item[1],create_time=item[2],content=item[3],reason=str(item[4]).encode('utf-8')))
	else:
		result.append(Message(title=item[1],create_time=item[2],content=item[3],reason=item[4].encode('utf-8')))
	
