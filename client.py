import socket   #for sockets
import sys  #for exit
from check import ip_checksum
import select
import time
import os
import getpass
import curses




def runMenu(s):

	#Start main useraccnt here!
	#msgNum = s.recv(1024)
	#time.sleep(1)
	#print 'You have ' + msgNum + ' unread messages.\n'


	print 'Menu:'
	print '\t1. See Offline Messages. '
	print '\t2. Edit subscriptions.  '
	print '\t3. Post new message. '
	print '\t4. Hashtag search. '
	print '\t5  See your subscriptions. '
	print '\t6. See followers.'
	print '\t7. logout. \n'

	sendInput = raw_input(	'Please select action: ' )
	print '='*80 + '\n\n'

	s.send( sendInput)
	if sendInput == '1':
		clientSeeOffline(s)
	elif sendInput == '2':
		clientEditSubs(s)
	elif sendInput == '3':
		tweet = postMessageRaw()
		s.sendall(tweet)
	elif sendInput == '4':
		clientFindHashtag(s)
	elif sendInput == '5':
		clientSeeSubscriptions(s)
	elif sendInput == '6':
		clientSeeFollowers(s)
	elif sendInput == '7':
		logOut(s)

	else:
		print "Invalid input.\n"

def seeAllOff(s):
	
	allOff = s.recv(4096)
	print allOff +  '\n'


def seeOneSubOff(s):

	print 'dasfasdf'
		
def clientSeeOffline(s):
	print '\t1. See all new posted messages.'
	print '\t2. See all messages of a user you are subscribed to.'
	print '\t3. Return to menu.'

	option = raw_input('Select an option: ')
	while 1:
		s.send(option)
		if option == '1':
			seeAllOff(s)
			return

		if option == '2':
			print 'babab'
			return
		if option =='3':
			return

		else:
			option = raw_input( 'Invalid input. Please slelect an option on the above menu: ')


def clientAddSub(s):
	os.system('clear')
	requestUser = raw_input('Type username of another user you would like to subscrible to: ')
	
	while 1:
		s.send(requestUser)
		userFound = s.recv(1024)
		time.sleep(1)

		#print userFound
		if userFound == 'found' :
			print 'Found ' + requestUser + '. Added to subscription list.'
			return None

		elif userFound == 'duplicate':
			requestUser = raw_input( 'User already exists in subscription list. Please Enter a new user: ')

		else:
			requestUser = raw_input( 'User not found. Please Enter an exisitng user: ' )

def clientDeleteSub(s):
	os.system('clear')

	subList = s.recv(1024)
	time.sleep(1)

	if subList == 'emptyList':
		print 'You have no subscriptions!\n'
		time.sleep(1)
		clientEditSubs(s)
		return None

	print 'Current list of subscriptions: \n'
	#get list of subs and print them
	print subList

	removeCanidate = raw_input( 'which subscription would you like to remove? ')
	
	while 1:
		
		s.send(removeCanidate)
		deleteStatus = s.recv(1024)
		time.sleep(1)

		if deleteStatus == 'ok':
			print 'User ' + removeCanidate + ' removed from subscription list. \n'
			return None

		else:
			removeCanidate = raw_input( 'User not found. Please enter a valid name from the list: ')



def clientEditSubs(s):
	
		os.system('clear')
		print '\t1. Add a new subscription. '
		print '\t2. Delete an existing subscription. '
		print '\t3. Return to menu'
		subInput = raw_input( 'Select an option: ')
			
		while 1:
			if subInput is '1':
				s.send(subInput)
				clientAddSub(s)
				return
			elif subInput is '2':
				s.send(subInput)
				clientDeleteSub(s)
				return
			elif subInput is '3':
				s.send(subInput)
				return
			else:
				subInput = raw_input( 'Invalid input. Please slelect an option on the above menu:  ')

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

def clientFindHashtag(s):
	tagString = raw_input( 'Enter name of hashtag without the "#": ' )
	s.send(tagString)

	allMatchingTweets = s.recv(4096)
	time.sleep(1)

	os.system('clear')

	if allMatchingTweets == 'noneFound':
		print '\tNo tweets with #' + tagString + ' found in database.'

	else:
		print allMatchingTweets
	return 

def clientSeeSubscriptions(s):
	subscriptions = s.recv(4096)
	print subscriptions
	return None

def clientSeeFollowers(s):

	followers = s.recv(4096)
	print followers
	return None


def logOut(s):
	os.system('clear')
	print 'Logging out...... You are now offline'
	s.close()
	time.sleep(3)
	os.system('clear')
	login() #clear screen and allow user to relogin using recursive call
	return


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
		uname = raw_input( 'username: ' )
		pwd = getpass.getpass()

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



	while 1:
		runMenu(s)
		#polling thread function goes here

#---------------------------------------------------------------------------------------------------------------------------------------------------------
login()

