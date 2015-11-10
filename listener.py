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

import sys
import select, socket
import time
import thread
import argparse
from flask import Flask, render_template

ONLINE_LIST = []
ONLINE_IP_LIST =[]
RESET = 1

MYPORT = 50000
DEFAULT_FLASK_PORT = 5000
flaskPORT = DEFAULT_FLASK_PORT

def get_ip_address():
	ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	try:
		ip.connect(('<broadcast>', 0))
		return ip.getsockname()[0]  
	except :
		print 'error'

def broadcast_query():

	global RESET
	if(RESET == 0):
		time.sleep(10*60)
		RESET = 1

	
	query = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	query.bind(('', 0))
	query.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	data = 'QUERY;http://' + get_ip_address() + ":" + repr(flaskPORT) + ";"
	query.sendto(data, ('<broadcast>', MYPORT))
	print "Sent Refresh QUERY"

def broadcast_connected():
	sb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sb.bind(('', 0))
	sb.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	data = "CONNECTED;http://" + get_ip_address() + ":" + repr(flaskPORT) + ";"

	sb.sendto(data, ('<broadcast>', MYPORT))	

def listener_thread():

	global ONLINE_LIST
	global ONLINE_IP_LIST
	global RESET

	bufferSize = 1024 # whatever you need

	#BROADCAST = '10.6.15.255'

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	s.bind(('<broadcast>', MYPORT))
	s.setblocking(0)


	while True:
	    result = select.select([s],[],[])
	    msg = result[0][0].recv(bufferSize) 

	    if(RESET == 1):
	    	ONLINE_LIST = []
	    	ONLINE_IP_LIST = []
	    	RESET = 0
	    	thread.start_new_thread(broadcast_query, ())

	    msg_split = msg.split(';');
	    if(msg_split[0] != "QUERY"):
		    status = msg.split(';')[0]
		    ip = msg.split(';')[1]
		    name = msg.split(';')[2]
		    #print name
		    if(status == "ONLINE"):
		    	if(ip not in ONLINE_IP_LIST):
		    		ONLINE_LIST.append([ip,name])
		    		ONLINE_IP_LIST.append(ip)
		    		broadcast_connected()
		    if(status == "CLOSED"):
		    	if(ip in ONLINE_IP_LIST):
		    		ONLINE_LIST.remove([ip,name])
		    		ONLINE_IP_LIST.remove(ip)
		    if(status == "STARTED"):
		    	if(ip not in ONLINE_IP_LIST):
		    		ONLINE_LIST.append([ip,name])
		    		ONLINE_IP_LIST.append(ip)
		    		broadcast_connected()



app = Flask(__name__)

@app.route('/')
def display():
	return render_template('index.html', online=ONLINE_LIST)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--port", default=DEFAULT_FLASK_PORT,	help="Specify to use a custom port for flask. Default port: 5000.")
	
	args = parser.parse_args()
	
	flaskPORT = args.port

	thread.start_new_thread(listener_thread, ())
	thread.start_new_thread(broadcast_query, ())
	app.run(host = '0.0.0.0', port = flaskPORT)
