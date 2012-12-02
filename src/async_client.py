import asyncore
import socket
import json
import signal
import threading
import time
from sys import stdout, exit

HOST = '127.0.0.1'   # The remote host
PORT = 2541          # The same port as used by the server. Default 2541

currNum = 0
maxNum = 0

#deal with signals
def signal_handler(signum, frame):
	print 'Signal handler called with signal:', signum
	client.t.stop()
	exit()

class AsyncClient(asyncore.dispatcher):
	buffer = ""
	t = None

	def __init__(self, host):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, PORT) )

		#print "sending data from __init__"
		#self.sendCommand("data_init")
		self.t = SenderThread(self)
		self.t.start()

	def sendJson(self, id, payload):
		self.buffer = json.dumps( {"id":id, "payload":payload} )

	def handle_close(self):
		self.close()
		self.t.stop()

	def handle_read(self):
		print self.recv(8192)

	#whenever we have a chance to write to the socket
	#Go ahead and send the data
	#Caveots:  forces us to write the entire json string imediently,
	#Else bad things will happen (sending half the data, then the other half)
	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
		if sent != 0:
			print "sent "+str(sent)+" bytes to server!"

class SenderThread(threading.Thread):
	_stop = False

	def __init__(self, client):
		super(SenderThread,self).__init__()
		self.client = client

	#We received the signal to stop from the parent class
	#or from the signal handler.  Stop what we are doing now
	def stop(self):
		self._stop = True

	def run(self):
		counter = 0
		while self._stop == False:
			time.sleep(3)
			print "sending data from thread"
			self.client.sendJson(0, "data_thread")

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

client = AsyncClient(HOST)
asyncore.loop(3)