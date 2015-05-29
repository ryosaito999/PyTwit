import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
import time
import os


userOK = False

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
host = '';
port = 8888;
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
#Connect to remote server
s.connect((remote_ip , port))
print 'Welcome to pyTwit! Enter your username and password.\n' 

while userOK == False :  
	uname = str(raw_input( 'username: ' ))
	pwd = str(raw_input( 'password: '))

	s.send(uname)
	time.sleep(2)
	s.send(pwd)
	time.sleep(1)

	vMsg = s.recv(1024)
	time.sleep(1)


	if vMsg == str(1):
		userOK = True
		os.system('clear')
		print 'Welcome back, ' + uname + '!\n'

	else:
		print 'Incorrect username/password! Please reenter.\n'


#-----------------------------------------------------------------------------------------------
#Start main useraccnt here!
msgNum = s.recv(1024)
print 'You have ' + msgNum + ' unread messages.\n'

