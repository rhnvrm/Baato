from socket import *

#BROADCAST = '10.6.15.255'
MYPORT = 50000

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
data = 'QUERY'
s.sendto(data, ('<broadcast>', MYPORT))