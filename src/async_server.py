import asyncore
import socket
import json
import signal
from StringIO import StringIO
DEBUG = True
connectionList = []

class EchoHandler(asyncore.dispatcher_with_send):
	def setAddr(self, addr):
		self.addr = addr

	def handle_read(self):
		data = self.recv(8192)
		if data:
			print 'received %s from %s' % (data, self.addr)
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
			connectionList.append(self)

server = EchoServer('localhost', 8080)
asyncore.loop()