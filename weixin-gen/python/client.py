from ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import DataService

host = '192.168.1.101'
port = 9090
socket = TSocket.TSocket(host,port)
transport = TTransport.TFramedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = DataService.Client(protocol)
transport.open()
msg1 = Message(title='what',content='coding...')
msg2 = Message(title='Sunday',content='enjoy...')
print client.pushMsg([msg1,msg2])
transport.close()