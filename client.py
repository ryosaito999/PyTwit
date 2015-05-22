import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;
seqBit = 0 
resend =False

while(1) :
    d = ""

    if resend is False:
   	 msg = raw_input(' Enter message to send : ')
    
   	 check = ip_checksum(msg)
    	 msg = str(seqBit) +str(check) + msg  

    try :
        #Set the whole string 
	s.sendto(msg, (host, port))
         
        # receive data from client (data, addr)
        
	readable, writeable, exceptional = select.select( [s] , [] , [s],5)
	
	for tempSock in readable:
		d  =  tempSock.recvfrom(1024)
	
	if not readable:
		print "message timed out-resending\n"
		resend = True	

	else:

		 resend = False
       		 reply = d[0]
       		 addr = d[1]
         
        	 print 'Server reply : ' + reply


		 #compare seqBit and checksum of server w/ reciver		
		 comp = str(seqBit) + str(check) 
	
		 if comp  is not reply:
			print 'sent = ' + comp +  ":recived  " +  reply
			print "invalid seq"
			
		 else:		
		
		 	if seqBit is 0:
				seqBit = 1
		 	else:
				seqBit = 0

			 
    except socket.error, msg:
        	 print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        	 sys.exit()
