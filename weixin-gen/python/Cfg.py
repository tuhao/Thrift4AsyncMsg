#coding=utf-8

import ConfigParser
import os

CFG_FILE = os.path.dirname(__file__) + '/mysql.cfg'
print CFG_FILE
CFG_SESSION = 'connect'

config = ConfigParser.ConfigParser()
cfg = lambda name:config.get(CFG_SESSION,name)
with open(CFG_FILE,'r') as f:
	config.readfp(f)
