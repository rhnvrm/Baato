import SocketServer
import BaseHTTPServer
import SimpleHTTPServer

class ThreadingSimpleServer(SocketServer.ThreadingMixIn,
                   BaseHTTPServer.HTTPServer):
    pass



MYPORT = 50000
SERVERPORT = 0
bufferSize = 1024

import sys, time
from socket import *
import select
import thread

def get_ip_address():
	s = socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	try:
		s.connect(('<broadcast>', 0))
		return s.getsockname()[0]  
	except :
		print 'error'


#BROADCAST = '10.6.15.255'


def broadcast_server_ip():
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	data = "ONLINE;" +get_ip_address() + ":" + repr(SERVERPORT)
	print "Server IP has been broadcasted."	  
	s.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	s.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	s.sendto(data, ('<broadcast>', MYPORT))  

def broadcast_end_session():
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	data = "CLOSED;" + get_ip_address() + ":" + repr(SERVERPORT)

	s.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	s.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	s.sendto(data, ('<broadcast>', MYPORT))  	

def listener_thread():
	print "Listening Service is now Running";
	listner = socket(AF_INET, SOCK_DGRAM)
	listner.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	listner.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	listner.bind(('<broadcast>', MYPORT))
	listner.setblocking(0)	

	while 1:
		result = select.select([listner],[],[])
		msg = result[0][0].recv(bufferSize) 
		if(msg == "QUERY"):
			broadcast_server_ip()

def server_thread():

	global SERVERPORT

	if sys.argv[1:]:
		port = int(sys.argv[1])
		SERVERPORT = port
	else:
		port = 8000
		SERVERPORT = port


	print "HTTP Server running at " + get_ip_address() + ":" + repr(SERVERPORT)


	server = ThreadingSimpleServer(('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)
	try:
	    while 1:
			sys.stdout.flush()
			server.handle_request()


	except KeyboardInterrupt:
	    print "Finished"

def displayManual():
	print "exit : End Program"
	print "man  : Print Manual Entries"

def main():

	thread.start_new_thread(listener_thread, ())
	thread.start_new_thread(server_thread, ())

	print "Welcome to Baato File Sharing Service"
	print "Type `man` for the Manual or `eXit` to Exit"

	inp = ""
	while(inp != "exit" and inp != "x"):
		inp = raw_input()

		if inp == "man":
			displayManual()

      
	broadcast_end_session()

if __name__ == "__main__":
    main()
