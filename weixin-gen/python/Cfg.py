#coding=utf-8

import ConfigParser

CFG_FILE = 'mysql.cfg'
CFG_SESSION = 'connect'

config = ConfigParser.ConfigParser()
cfg = lambda name:config.get(CFG_SESSION,name)
with open(CFG_FILE,'r') as f:
	config.readfp(f)