#coding=utf-8
from Cfg import cfg
import MySQLdb
import MySQLdb.cursors

class WeixinDB:

	def __init__(self):
		self.host = cfg('host')
		self.user = cfg('user')
		self.passwd = cfg('passwd')
		self.db_name = cfg('db_name')

	def execute_insert(self,sql_str,*params):
		try:
			self.cursor.execute(sql_str,params[0])
		except Exception, e:
			print e
		return ()

	def execute_delete(self,sql_str):
		try:
			self.cursor.execute(sql_str)
		except Exception, e:
			print e
			return False
		else:
			return True

	def execute_query(self,sql_str):
		try:
			self.cursor.execute(sql_str)
			return self.cursor.fetchall()
		except Exception, e:
			print e
		return ()

	def last_record(self):
		return self.cursor.lastrowid


	def __enter__(self):
		self.conn = MySQLdb.connect(self.host,self.user,self.passwd,self.db_name,charset='utf8',cursorclass=MySQLdb.cursors.SSCursor)
		self.cursor = self.conn.cursor()

	def __exit__(self,*kw):
		try:
			self.cursor.close()
			self.conn.commit()
			self.conn.close()
		except Exception, e:
			print e
