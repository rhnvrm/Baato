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



import argparse
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer

class ThreadingSimpleServer(SocketServer.ThreadingMixIn,
                   BaseHTTPServer.HTTPServer):
    pass



MYPORT = 50000
SERVERPORT = 8000
SERVERNAME = "New Baato Server"
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
	sb = socket(AF_INET, SOCK_DGRAM)
	sb.bind(('', 0))
	sb.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	data = "ONLINE;http://" + get_ip_address() + ":" + repr(SERVERPORT) + ";" +SERVERNAME
	#print "Server IP has been broadcasted."	  
	sb.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	#sb.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	#sb.sendto(data, ('<broadcast>', MYPORT))  

def broadcast_end_session():
	sb = socket(AF_INET, SOCK_DGRAM)
	sb.bind(('', 0))
	sb.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	data = "CLOSED;http://" + get_ip_address() + ":" + repr(SERVERPORT) + ";" +SERVERNAME

	sb.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	#sb.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	#sb.sendto(data, ('<broadcast>', MYPORT))  	

def broadcast_start_session():
	sb = socket(AF_INET, SOCK_DGRAM)
	sb.bind(('', 0))
	sb.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	data = "STARTED;http://" + get_ip_address() + ":" + repr(SERVERPORT) + ";" +SERVERNAME

	sb.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	#sb.sendto(data, ('<broadcast>', MYPORT))
	#time.sleep(2)
	#sb.sendto(data, ('<broadcast>', MYPORT))  		

def listener_thread():
	print "Listening Service is now Running";
	listener = socket(AF_INET, SOCK_DGRAM)
	listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	listener.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	listener.bind(('0.0.0.0', MYPORT))
	listener.setblocking(0)	

	while 1:
		result = select.select([listener],[],[])
		msg = result[0][0].recv(bufferSize) 
		msg_split = msg.split(';');
		if(msg_split[0] == "QUERY" or msg_split[0] == "CONNECTED"):
			print "Connected with a Listener Running on: " + msg_split[1] #+ msg_split[0];
			broadcast_server_ip()

def server_thread():

	print "HTTP Server running at " + get_ip_address() + ":" + repr(SERVERPORT)


	server = ThreadingSimpleServer(('', SERVERPORT), SimpleHTTPServer.SimpleHTTPRequestHandler)
	
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

	print """......................................................	   
	Welcome to Baato :: Host Service
......................................................

order of args <port> <server name>

created by: rhnvrm
  
Type `man` for the Manual or `exit` `x` to Exit

"""

	inp = ""
	while(inp != "exit" and inp != "x"):
		inp = raw_input()

		if inp == "man":
			displayManual()

      
	broadcast_end_session()

if __name__ == "__main__":
  	parser = argparse.ArgumentParser()
  	
   	parser.add_argument("-p", "--port", default=SERVERPORT,	help="Specify to use a custom server port. Default port: " + str(SERVERPORT))
   	parser.add_argument("-n", "--name", nargs="*", default=[SERVERNAME], help="Specify to use a custom server name. Default name: " + SERVERNAME)
   	args = parser.parse_args()
   	SERVERPORT = int(args.port)
   	SERVERNAME = ' '.join(args.name)
   	main()
