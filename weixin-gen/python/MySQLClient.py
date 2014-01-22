#coding=utf-8
from Cfg import cfg
import MySQLdb
import MySQLdb.cursors

class WeixinDB:

	def __init__(self):
		host = cfg('host')
		user = cfg('user')
		passwd = cfg('passwd')
		db_name = cfg('db_name')
		self.conn = MySQLdb.connect(host,user,passwd,db_name,charset='utf8',cursorclass=MySQLdb.cursors.SSCursor)
		self.cursor = self.conn.cursor()

	def execute_insert(self,sql_str,*params):
		try:
			self.cursor.execute(sql_str,params[0])
		except Exception, e:
			print e
		return ()

	def execute_query(self,sql_str):
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

	def rollback(self):
		self.conn.rollback()

	def close(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()