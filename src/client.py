# Echo client program
import socket
import json
import sys
from StringIO import StringIO
from random import randrange
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DEBUG = True

#Connection details for connecting to server
#Edit these if you wish to use your own server or port
def connectToServer():
	HOST = '127.0.0.1'   # The remote host
	PORT = 2541          # The same port as used by the server. Default 2541
	s.connect((HOST, PORT))
	if DEBUG:
		print 'connected to server', HOST, 'on port', PORT

def dealKeepAlive():
	print 'received keep-alive from server'

def sendData(id, dataSend):
	dataToSend = json.dumps( {"id":id, "payload":dataSend} )
	s.sendall( dataToSend )
	if DEBUG:
		print 'sent to server: ', dataToSend

def shutDown():
	s.close()
	sys.exit(0)
	
#ok now connect to the server.
connectToServer()
sendData(1, 1456)

jdata = s.recv(1024)
data = json.loads(jdata)
if DEBUG:
	print 'got data:  id: ', data['id'], ' payload: ', data['payload']

shutDown()