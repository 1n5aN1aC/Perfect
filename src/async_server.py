import asyncore
import socket
import json
import signal
import threading
from time import sleep
from sys import stdout
from StringIO import StringIO

DEBUG = True
connectionClassList = []
connectionSocketList = []

def signal_handler(signum, frame):
	print 'Signal handler called with signal', signum
	os.kill(pid, sig)

def dealKeepAlive(address):
	print 'received keep-alive from:', address
	#echo the ping back
	self.send(data)

def dealRangeReq(socket, quantity):
	print 'received request for', quantity, 'numbers from:', socket
	socket.send(data)

def dealNumberFound(address, numberFound):
	print 'client', address[0],':',address[1], 'claims that', numberFound, 'is a perfect number!'

class EchoHandler(asyncore.dispatcher_with_send):
	def setAddr(self, addr):
		self.addr = addr
		
	def setSock(self, sock):
		self.sock = sock

	def handle_read(self):
		data = self.recv(8192)
		#assuming we actually received SOMETHING.....
		if data:
			#lets load up that json!  (DOES NOT DEAL WITH INVALID JSON!)
			jdata = json.loads(data)
			if jdata['id'] == 0:
				dealKeepAlive(self.addr)
			elif jdata['id'] == 1:
				quantity = jdata['payload']
				dealRangeReq(self.sock, quantity)
			elif jdata['id'] == 3:
				numberFound = jdata['payload']
				dealNumberFound(self.addr, numberFound)
			else:
				print 'something went wrong.'
				
			#for testing, send everything back to client
			self.send(data)

class EchoServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	def handle_accept(self):
		pair = self.accept()
		if pair is None:
			print 'something is messed up'
			pass
		else:
			sock, addr = pair
			if DEBUG:
				print 'Incoming connection from %s' % repr(addr)
			handler = EchoHandler(sock)
			handler.setAddr(addr)
			handler.setSock(sock)
			connectionClassList.append(self)
			connectionSocketList.append(sock)
			

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

server = EchoServer('localhost', 8080)
asyncore.loop()