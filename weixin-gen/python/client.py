from ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import DataService

host = 'yasir.cn'
port = 9090
socket = TSocket.TSocket(host,port)
transport = TTransport.TBufferedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = DataService.Client(protocol)
transport.open()
msg1 = Message(title='what',content='coding...')
msg2 = Message(title='Sunday',content='enjoy...')
print client.pushMsg([msg1,msg2])
transport.close()

