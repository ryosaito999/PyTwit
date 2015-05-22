import time
from check import ip_checksum
import socket
import sys

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

prevMsg = []
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
   
     
    print data[3:]

    reply = data[0] + 'zz'       


    if  data not in prevMsg :
	#time.sleep(6)
	s.sendto(reply , addr)
    	print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
    	prevMsg.append(data)

    elif data in prevMsg : 
	print('duplicate msg recived - dumping')
	prevMsg.remove(data)   
 
close()
