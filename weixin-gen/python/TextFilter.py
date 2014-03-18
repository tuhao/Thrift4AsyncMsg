#coding=utf-8
from MySQLClient import *
import sys
reload(sys)
sys.setdefaultencoding='utf-8'
import re

#REGEX = re.compile(r'\&gt;|\&lt;|=|>|转发')
REGEX = re.compile(r'(转发)|=|>|\&[gl]t;?')
text = """转发=> 转发=&gt;真能扯~转发=>心寒！一个大学女生最恶毒的情书~刚扯蛋吧看到的。#一人一句来扯蛋#"""
print text
#for item in REGEX.findall(text):
#	print item
text = REGEX.sub('', text)
print text