"""

Baato
    Copyright (C) 2015 Rohan Verma

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""



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

def broadcast_start_session():
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	data = "STARTED;" + get_ip_address() + ":" + repr(SERVERPORT)

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
	
	broadcast_start_session()

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
