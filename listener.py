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


import select, socket 
import thread
from flask import Flask, render_template

ONLINE_LIST = []

MYPORT = 50000

def broadcast_query():
	s = socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	data = 'QUERY'
	s.sendto(data, ('<broadcast>', MYPORT))

def listener_thread():

	global ONLINE_LIST

	bufferSize = 1024 # whatever you need

	#BROADCAST = '10.6.15.255'
	MYPORT = 50000

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	s.bind(('<broadcast>', MYPORT))
	s.setblocking(0)

	while True:
	    result = select.select([s],[],[])
	    msg = result[0][0].recv(bufferSize) 
	    if(msg != "QUERY"):
		    status = msg.split(';')[0]
		    ip = msg.split(';')[1]
		    if(status == "ONLINE"):
		    	if(ip not in ONLINE_LIST):
		    		ONLINE_LIST.append(ip)
		    if(status == "CLOSED"):
		    	if(ip in ONLINE_LIST):
		    		ONLINE_LIST.remove(ip)
		    if(status == "STARTED"):
		    	if(ip not in ONLINE_LIST):
		    		ONLINE_LIST.append(ip)


app = Flask(__name__)

@app.route('/')
def display():
	return render_template('index.html', online=ONLINE_LIST)

if __name__ == '__main__':
	thread.start_new_thread(listener_thread, ())
	#app.run(debug=True)
	app.run(host='0.0.0.0')