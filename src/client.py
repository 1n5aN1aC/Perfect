# Echo client program
import socket
import json
from StringIO import StringIO
def as_complex(dct):
    return complex(dct['packet'], dct['data'])
    return dct
dataToSend = StringIO()

json.dump([{"id":1, "stuff":"streaming API"}], dataToSend)

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall( dataToSend.getvalue() )
data = s.recv(1024)
s.close()

print 'Received', repr(data)
jdata = json.loads(data)

print 'Parsed', repr(jdata)