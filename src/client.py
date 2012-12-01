# Echo client program
import socket
import json
import sys
from StringIO import StringIO
from random import randrange
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DEBUG = True

def connectToServer():
	HOST = '127.0.0.1'   # The remote host
	PORT = 8080          # The same port as used by the server
	s.connect((HOST, PORT))
	if DEBUG:
		print 'connected to server'

def sendData(id, dataSend):
	dataToSend = StringIO()
	json.dump({"id":id, "payload":dataSend}, dataToSend)
	s.sendall( dataToSend.getvalue() )
	if DEBUG:
		print 'sent to server: ', dataToSend.getvalue()

def shutDown():
	s.close()
	if DEBUG:
		print 'closed socket.  exiting now'
	sys.exit(0)

connectToServer()
sendData(1, 1456)

data = s.recv(1024)

jdata = json.loads(data)
if DEBUG:
	print 'got data:  id: ', jdata['id'], ' payload: ', jdata['payload']

shutDown()