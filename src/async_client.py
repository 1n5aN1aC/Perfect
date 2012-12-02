import asyncore
import socket
import json
import signal
import threading
import time
from time import sleep
from sys import stdout, exit

HOST = '127.0.0.1'   # The remote host
PORT = 2541          # The same port as used by the server. Default 2541

currNum = 0
maxNum = 0

#deal with signals
def signal_handler(signum, frame):
	print 'Signal handler called with signal:', signum
	exit()

class SClient(asyncore.dispatcher):
    buffer = ""
    t = None

    def __init__(self, host):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, PORT) )

        print "sending data from __init__"
        self.sendCommand("data_init")
        self.t = SenderThread(self)
        self.t.start()

    def sendCommand(self, command):
        self.buffer = command

    def handle_close(self):
        self.close()
        self.t.stop()

    def handle_read(self):
        print self.recv(8192)

    def handle_write(self):
        print "writing to socket"
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        print "wrote "+str(sent)+" to socket"

class SenderThread(threading.Thread):
    _stop = False

    def __init__(self, client):
        super(SenderThread,self).__init__()
        self.client = client

    def stop(self):
        self._stop = True

    def run(self):
        counter = 0
        while self._stop == False:
            counter += 1
            time.sleep(1)
            if counter == 2:
                print "sending data from thread"
                self.client.sendCommand("data_thread")
                counter = 0

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

client = SClient(HOST)
asyncore.loop(3)