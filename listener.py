import select, socket 

bufferSize = 1024 # whatever you need

BROADCAST = '10.6.15.255'
MYPORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((BROADCAST, MYPORT))
s.setblocking(0)

while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize) 
    print msg
