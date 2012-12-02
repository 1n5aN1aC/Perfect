import asyncore
import socket
import json
import signal
import threading
from time import sleep
from sys import stdout, exit

#change these values only
HOST = '127.0.0.1'   # The remote host
PORT = 2541          # The same port as used by the server. Default 2541
#change these values only

currNum = 0

connectionClassList = []
connectionSocketList = []

#deal with signals
def signal_handler(signum, frame):
	print 'Signal handler called with signal:', signum
	server.sendKill();
	exit()

#Returns a json-formated string based on the packet ID and packet payload
def createJson(self, id, payload):
	lol = json.dumps( {"id":id, "payload":payload} )
	return lol

#If client sends us a packet ID 0 (keepalive)
#Then just pong one back to the client
def dealKeepAlive(self, payload):
	print 'received keep-alive from:', self.addr
	self.send( createJson(self, 0, payload) )

#Cliet asked for a range of numbers they should check
#Send them however many they asked for
def dealRangeReq(self, quantity):
	print 'received request for', quantity, 'numbers from:', self.addr
	self.send( createJson(self, 2, "this will normally be the range of numbers") )

#The Client sent us a number that they say is a perfect number!
#Amazing!  Make a note of this!
def dealNumberFound(self, address, numberFound):
	print 'client', address[0],':',address[1], 'claims that', numberFound, 'is a perfect number!'
	self.send( createJson(self, 0, "yup I got that") )

#Class For handling the event-driven server
class PacketHandler(asyncore.dispatcher_with_send):
	def setAddr(self, address):
		self.addr = address

	#probably not needed anymore
	def setSock(self, sock2):
		self.sock = sock2

	def handle_read(self):
		jdata = self.recv(8192)
		print jdata
		#assuming we actually received SOMETHING.....
		if jdata:
			#lets load up that json!  (DOES NOT DEAL WITH INVALID JSON!)
			data = json.loads(jdata)
			if data['id'] == 0:
				lol = data['payload']
				dealKeepAlive(self, lol)
			elif data['id'] == 1:
				quantity = data['payload']
				dealRangeReq(self, quantity)
			elif data['id'] == 3:
				numberFound = data['payload']
				dealNumberFound(self.addr, numberFound)
			else:
				print 'something went wrong.'

#Class that sets up the event-drivin server
#and passes data it receives to the PacketHandler() class
class AsyncServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	#We have been told to shutdown!
	#Make sure we send the shutdown packet first!
	def sendKill(self):
		for _socketobject in connectionSocketList:
			_socketobject.send( createJson(self, 9, 'Server says SHUTDOWN!') )
			print str( _socketobject.getpeername()[0] ) + ':' + str( _socketobject.getpeername()[1] ) + ' was sent the shutdown signal!'

	#We got a client connection!
	def handle_accept(self):
		pair = self.accept()
		if pair is None:
			print 'something is messed up'
			pass
		else:
			sock, addr = pair
			handler = PacketHandler(sock)
			handler.setAddr(addr)
			handler.setSock(sock)
			connectionClassList.append(self)
			connectionSocketList.append(sock)

	def handle_close():
		self.close()
		for _socketobject in connectionSocketList:
		

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#Run the event-driven server
server = AsyncServer(HOST, PORT)
asyncore.loop(1)