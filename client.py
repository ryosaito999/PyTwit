import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
import time
import os


def runMenu(s):

	print '1. See Offline Messages. \n'
	print '2. Edit subscriptions. \n '
	print '3. Post new message. \n'
	print '4. logout. \n'
	print '5. Hashtag search. \n'


	sendInput = raw_input(	'Please select action: ' )
	s.send( sendInput)

	if sendInput == '1':
		seeOfflineClient(s)
	elif sendInput == '2':
		editSubClient(s)
	elif sendInput == '3':
		tweet = postMessageRaw()
		s.sendall(tweet)
	elif sendInput == '4':
		logOut(s)

	elif sendInput == '5':
		print 'findMsg'

	else:
		print "Invalid input.\n"
		


def seeOfflineClient(s):
	print '\t1. See all new posted messages.'
	print '\t2. See all messages of a user you are subscribed to.'
	print '\t3. Return to menu.'

	option = raw_input('Select an option: ')
	s.send(option)
	if option == '1':
		print 'bbadfadsf'
		return
	if option == '2':
		print 'babab'
		return
	if option =='3':
		return



def addNewSub(s):
	os.system('clear')
	requestUser = raw_input('Type userName of another user you would like to subscrible to: ')
	
	while 1:
		s.send(requestUser)
		userFound = s.recv(1024)
		time.sleep(1)
		if userFound == 'found' :
			print 'Found ' + requestUser + '. Added to subscription list.'
			return None

		elif userFound == 'duplicate':
			requestUser = raw_input( 'User already exists in subscription list. Please Enter a new user: ')

		else:
			requestUser = raw_input( 'User not found. Please Enter an exisitng user: ' )

def deleteSubClient(s):
	os.system('clear')

	subList = s.recv(1024)
	time.sleep(1)

	if subList == 'emptyList':
		print 'You have no subscriptions!\n'
		time.sleep(2)
		editSubClient(s)
		return None

	print 'Current list of subscriptions: \n'
	#get list of subs and print them

	print subList

	removeCanidate = raw_input( 'which subscription would you like to remove? ')
	
	while 1:
		
		s.send(removeCanidate)

		deleteStatus = s.recv(1024)

		if deleteStatus == 'ok':
			print 'User ' + removeCanidate + ' removed from subscription list. \n'
			return None

		else:
			raw_input( 'User not found. Please enter a valid name from the list: ')



def editSubClient(s):

	validInput = False

	while  validInput is False: 
		os.system('clear')
		print '\t1. Add a new subscription. '
		print '\t2. Delete an existing subscription. '
		print '\t3. Return to menu'
		subInput = raw_input( 'Select an option: ')
			
		while 1:
			
			if subInput is '1':
				s.send(subInput)
				addNewSub(s)
				validInput = True
				return
			elif subInput is '2':
				s.send(subInput)
				validInput = True
				deleteSubClient(s)
				return
			elif subInput is '3':
				s.send(subInput)
				return
			else:
				subInput = raw_input( 'invalid input! Please select a valid option: ')

def postMessageRaw():

	print 'Type a tweet under 140 characters! Press Enter twice to post. Hit esc at anytime to cancel. \n'
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
	print 'Logging out...... You are now offline'
	s.close()
	time.sleep(2)
	os.system('clear')
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
		time.sleep(1)
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

