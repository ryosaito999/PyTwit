import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
import time
import os

def runMenu(s):

	sendInput = 9999

	print '1. See Offline Messages. \n'
	print '2. Edit subscriptions. \n '
	print '3. Post new message. \n'
	print '4. logout. \n'
	print '5. Hashtag search. \n'

	while sendInput > 6:
		sendInput = int(raw_input(	'Please select action: ' ))
		
		if sendInput > 6:
			print "Invalid input.\n"

	s.send(str(sendInput))

	if sendInput == 3:
		tweet = postMessageRaw()
		s.sendall(tweet)



def postMessageRaw():

	print 'Type a tweet under 140 characters! Press Enter twice to post.\n'

	text = ""
	stopword = ""
	while True:
	    line = raw_input()
	    if line.strip() == stopword:
	        break
	    text += "%s\n" % line
	return text


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

while 1:
	runMenu(s)

s.close()

