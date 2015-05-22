import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
 
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
uname = str(raw_input( 'username: ' ))
pwd = str(raw_input( 'password: '))

s.sendall(uname)
s.sendall(pwd)
