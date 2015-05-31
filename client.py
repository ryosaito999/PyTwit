import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
import time
import os

def runMenu(s):

	sendInput = 9999

	print 
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


	if sendInput == 2:
		editSubClient(s)

	elif sendInput == 3:
		tweet = postMessageRaw()
		s.sendall(tweet)

	elif sendInput == 4:
		logOut(s)
		
def addNewSub(s):
	os.system('clear')
	requestUser = raw_input('Type userName of user you would like to subscrible to: ')
	
	while 1:
		s.send(requestUser)
		userFound = s.recv(1024)
		time.sleep(1)

		if userFound == 'found' :
			print 'Found ' + requestUser + '. Added to subscription list.'
			return None

		else:
			requestUser = raw_input( 'User not found. Please Enter an exisitng user:' )

def deleteSubClient(s):
	os.system('clear')
	print 'Current list of subscriptions: \n'
	#get list of subs and print them

	subList = s.recv(1024)
	time.sleep(1)

	print subList




def editSubClient(s):

	validInput = False

	while  validInput is False: 
		os.system('clear')
		print ''
		print '\t1. Add a new subscription. '
		print '\t2. Delete an existing subscription. '
		subInput = raw_input( 'Select an option:')
		s.send(subInput)

		if int(subInput) is 1:
			addNewSub(s)
			validInput = True



		elif int(subInput) is 2:
			validInput = True
			deleteSubClient(s)


		else:
			print 'invalid input! Please select a valid option: \n'

def postMessageRaw():

	print 'Type a tweet under 140 characters! Press Enter twice to post.\n'
	msgLen = False

	while msgLen is False:
		
		text = ""
		stopword = ""
		while True:
		    line = raw_input()
		    if line.strip() == stopword:
		        break
		    text += "%s\n" % line
		
		if len(text) > 140:
			print 'Tweet is too long. Please retype: \n'
		
		else:
			msgLen = True
			return text

def logOut(s):
	os.system('clear')
	print 'Logging out. You are now offline'
	s.close()
	time.sleep(2)
	login()


def login():

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

	#Start main useraccnt here!
	msgNum = s.recv(1024)
	print 'You have ' + msgNum + ' unread messages.\n'

	while 1:
		runMenu(s)


#---------------------------------------------------------------------------------------------------------------------------------------------------------

login()

