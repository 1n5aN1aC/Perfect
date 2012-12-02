import asyncore
import socket
import json
import signal
import threading
import time
from random import randrange
from sys import stdout, exit

#change these values only
HOST = '127.0.0.1'   # The remote host
PORT = 2541          # The same port as used by the server. Default 2541
#change these values only

each = 0
currNum = 0
maxNum = 0

#deal with signals
def signal_handler(signum, frame):
	print 'SHUTDOWN!  Reason:', signum
	client.t.stop()
	exit()

#Returns a json-formated string based on the packet ID and packet payload
def createJson(self, id, payload):
	lol = json.dumps( {"id":id, "payload":payload} )
	return lol

def dealFoundPerfect(self, num):
	print 'found perfect.  need to send'

def findPerfectNumbers(self, min, max):
	n = min
	while n < max:
		factors = [1]
		[factors.append(i) for i in range(2,n+1) if n%i == 0]
		if sum(factors) == 2*n: dealFoundPerfect(self, n)
		n += 1

#yup, server is still there!
def dealKeepAlive(self, payload):
	print 'got keep-alive back from server!'

def dealRangeAggignment(self, beginning):
	print 'derp'

#main class which handles the async part of the client.
#It then calls out, and starts up the actuall processing thread
class AsyncClient(asyncore.dispatcher):
	buffer = ""
	t = None

	def __init__(self, host):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, PORT) )
		self.t = SenderThread(self)
		self.t.start()

	#adds the requested json to the send buffer
	def sendJson(self, id, payload):
		self.buffer = json.dumps( {"id":id, "payload":payload} )

	#got the message to kill self
	#Also, make sure we kill the child thread too
	def handle_close(self):
		self.close()
		self.t.stop()

	#Deals with any packets received
	#Delegates them out to be processed
	def handle_read(self):
		jdata = self.recv(8192)
		#assuming we actually received SOMETHING.....
		if jdata:
			#lets load up that json!  (DOES NOT DEAL WITH INVALID JSON!)
			data = json.loads(jdata)
			if data['id'] == 0:
				lol = data['payload']
				dealKeepAlive(self, lol)
			elif data['id'] == 2:
				beginning = data['payload']
				dealRangeAggignment(self, beginning)
			elif data['id'] == 9:
				reason = data['payload']
				signal_handler(reason, 2)
			else:
				print 'something went wrong.'

	#whenever we have a chance to write to the socket
	#Go ahead and send the data
	#Caveots:  forces us to write the entire json string imediently,
	#Else bad things will happen (sending half the data, then the other half)
	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
		if sent != 0:
			print "sent "+str(sent)+" bytes to server!"

#Thread that actually does all the processing
class SenderThread(threading.Thread):
	_stop = False

	def __init__(self, client):
		super(SenderThread,self).__init__()
		self.client = client

	#We received the signal to stop from the parent class
	#or from the signal handler.  Stop what we are doing now
	def stop(self):
		self._stop = True

	#What the thread actually does
	def run(self):
		counter = 0
		while self._stop == False:
			self.client.sendJson(1, 43)
			time.sleep(3)

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

findPerfectNumbers('derp' ,0, 1000)

#ok, now actually start up the client!
client = AsyncClient(HOST)
asyncore.loop(1)