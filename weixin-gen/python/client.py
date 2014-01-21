#coding=utf-8
from ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import DataService

def msg():
	msg1 = Message(title='what',content='coding...')
	msg2 = Message(title='Sunday',content='enjoy...')
	return [msg1,msg2]

def news():
	a11 = Article('title11', 'description11', 'imageurl11', 'url11')
	a12 = Article('title12','description12','imageurl12','url12')
	title1 = 'weibo'
	a21 = Article( 'title21', 'description21', 'imageurl21', 'url21')
	a22 = Article( 'title22', 'description22', 'imageurl22', 'url22')
	title2 = 'test'
	return [News(title=title1, articles=[a11,a12]),News(title=title2,articles=[a21,a22])]

host = '192.168.1.102'
port = 9090
socket = TSocket.TSocket(host,port)
transport = TTransport.TFramedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = DataService.Client(protocol)
transport.open()
#data = msg()
#print client.pushMsg(data)
print client.pullMsg(10)
#data = news()
#print client.pushNews(data)
transport.close()

