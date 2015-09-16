import SocketServer
import BaseHTTPServer
import SimpleHTTPServer

class ThreadingSimpleServer(SocketServer.ThreadingMixIn,
                   BaseHTTPServer.HTTPServer):
    pass


BROADCAST = '10.6.15.255'
MYPORT = 5000
bufferSize = 1024

import sys, time
from socket import *
import select
import thread

def get_ip_address():
	s = socket(AF_INET, SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]  

def broadcast_server_ip():
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	MYIPADDR = get_ip_address();
	data = repr(MYIPADDR)
	s.sendto(data, (BROADCAST, MYPORT))
	time.sleep(2)
	s.sendto(data, (BROADCAST, MYPORT))
	time.sleep(2)
	s.sendto(data, (BROADCAST, MYPORT))  

def listner_thread():
	print "LISTENER RUNNING";
	listner = socket(AF_INET, SOCK_DGRAM)
	listner.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	listner.bind((BROADCAST, MYPORT))
	listner.setblocking(0)	

	while 1:
		result = select.select([listner],[],[])
		msg = result[0][0].recv(bufferSize) 
		if(msg == "QUERY"):
			broadcast_server_ip()	  


def main():

	thread.start_new_thread(listner_thread, ())


	if sys.argv[1:]:
		port = int(sys.argv[1])
	else:
		port = 8000

	server = ThreadingSimpleServer(('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)
	try:
	    while 1:
			sys.stdout.flush()
			server.handle_request()


	except KeyboardInterrupt:
	    print "Finished"

      


if __name__ == "__main__":
    main()
