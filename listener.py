import select, socket 
import thread
from flask import Flask

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
	    print msg
	    if(msg != "QUERY"):
		    status = msg.split(';')[0]
		    ip = msg.split(';')[1]

		    if(status == "ONLINE"):
		    	if(ip not in ONLINE_LIST):
		    		ONLINE_LIST.append(ip)



app = Flask(__name__)

@app.route('/')
def hello_world():
	return repr(ONLINE_LIST)

if __name__ == '__main__':
	thread.start_new_thread(listener_thread, ())
	#app.run(debug=True)
	app.run(host='0.0.0.0')