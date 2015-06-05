import socket   #for sockets
from socket import AF_INET, SOCK_STREAM
import errno
import sys  #for exit
from check import ip_checksum
import select
import time
import os
import getpass
from getCh import *
import curses
from thread import *



def custPrompt(s, prompt):

	# if prompt == 'password:':
	# 	return getpass.getpass()
	# try:

		if prompt:
			print prompt
		socket_list = [sys.stdin, s]
		read_sockets,write_sockets,error_sockets = select.select(socket_list , [], [] )		
		
		for sock in read_sockets:
			if sock == s:
				data = sock.recv(4096)
				#time.sleep(1)
				if data:

					sys.stdout.write("\x1B[2K\r")
					sys.stdout.write(data + '\n')
					sys.stdout.write(prompt)
					return 	sys.stdin.readline().strip() 
			else:
				return 	sys.stdin.readline().strip() 

	# except KeyboardInterrupt:
	# 	print '\n'
	# 	return '-1'

def custRecv(s) :

#add expecting 
	socket_list = [sys.stdin, s]
	read_sockets,write_sockets,error_sockets = select.select(socket_list , [], [] )		
	
	for sock in read_sockets:
		if sock == s:
			data = s.recv(4096)

			if data:

				return data
			



def checkOnlineTweet(s): #create new thread that accepts a specific flag
	
	while 1:
		
		realtTimeFlag = ''
		try:
			s.settimeout(1)
			realtTimeFlag = custRecv(s)
		except (socket.timeout, socket.error, errno.errorcode[11]):
			pass
			
		s.settimeout(None)
		if realtTimeFlag == '__realTime__':

			print 'found new msg'
		 	s.send('readyRecv')
		 	tweet = s.recv(4906)
		 	print tweet

def runMenu(s):

	#Start main useraccnt here!
	print '='*80 + '\n'

	print 'Menu:'
	print '\t1. See Offline Messages. '
	print '\t2. Edit subscriptions.  '
	print '\t3. Post new message. '
	print '\t4. Hashtag search. '
	print '\t5  See your subscriptions. '
	print '\t6. See followers.'
	print '\t7. logout. \n'

	#sendInput = custPrompt(s,	'Please select action: ' )
	sendInput = custPrompt(s, 'Please select action: ')
	print '\n' + '='*80 + '\n\n'

	s.send(sendInput)

	if sendInput == '1':
		clientSeeOffline(s)
	elif sendInput == '2':
		clientEditSubs(s)
	elif sendInput == '3':
		tweet = postMessageRaw(s)
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
	
	allOff = custRecv(s)
	print allOff +  '\n'

def seeOneSubOff(s):
	subs = custRecv(s)
	print subs

	if subs == '\tYou are not subscribed to anyone! \n':
		clientSeeOffline(s)
		return

	else:
		usermsg = custPrompt(s,'select which user\'s new messages you would like to see: ')
		s.send(usermsg)

		tweetsUser = custRecv(s)
		print tweetsUser



		
def clientSeeOffline(s):
	os.system('clear')
	print '\t1. See all new posted messages.'
	print '\t2. See all messages of a user you are subscribed to.'
	print '\t3. Return to menu.'

	option = custPrompt(s,'Select an option: ')
	while 1:
		s.send(option)
		if option == '1':
			seeAllOff(s)
			return

		if option == '2':
			seeOneSubOff(s)
			return
		if option =='3':
			return

		else:
			option = custPrompt(s, 'Invalid input. Please slelect an option on the above menu: ')


def clientAddSub(s):
	os.system('clear')
	requestUser = custPrompt(s,'Type username of another user you would like to subscrible to: ')
	
	while 1:
		s.send(requestUser)
		if requestUser == '-1':
			return

		userFound = custRecv(s)
		time.sleep(1)

		#print userFound
		if userFound == 'found' :
			print 'Found ' + requestUser + '. Added to subscription list.'
			return None

		elif userFound == 'duplicate':
			requestUser = custPrompt(s, 'User already exists in subscription list. Please Enter a new user: ')

		else:
			requestUser = custPrompt(s, 'User not found. Please Enter an exisitng user: ' )

def clientDeleteSub(s):
	os.system('clear')

	subList = custRecv(s)
	time.sleep(1)

	if subList == 'emptyList':
		print 'You have no subscriptions!\n'
		time.sleep(1)
		clientEditSubs(s)
		return None

	print 'Current list of subscriptions: \n'
	#get list of subs and print them
	print subList

	removeCanidate = custPrompt(s, 'which subscription would you like to remove? Cntrl + C to go back to menu. ')
	
	while 1:
		s.send(removeCanidate)
		deleteStatus = custRecv(s)
		time.sleep(1)

		print deleteStatus
		if deleteStatus == 'ok':
			print 'User ' + removeCanidate + ' removed from subscription list. \n'
			return None

		else:
			removeCanidate = custPrompt(s, 'User not found. Please enter a valid name from the list: ')



def clientEditSubs(s):
	
		os.system('clear')
		print '\t1. Add a new subscription. '
		print '\t2. Delete an existing subscription. '
		print '\t3. Return to menu'
		subInput = custPrompt(s,'Select an option: ')
			
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
				subInput = custPrompt( s, 'Invalid input. Please slelect an option on the above menu:  ')

def postMessageRaw(s):

	print 'Type a tweet under 140 characters! Press Enter twice to post. Hit cntrl + c at anytime to cancel. \n'
	msgLen = False

	while msgLen is False:
		text = ""
		stopword = ""
		while True:
		    line = custPrompt(s,'')

		    if line == '-1':
		    	return '-1'

		    if line.strip() == stopword:
		        break
		    text += "%s\n" % line
		
		if len(text) > 140:
			print 'Tweet is too long. Please retype: \n'
		
		else:
			msgLen = True
			return text

def clientFindHashtag(s):
	tagString = custPrompt(s, 'Enter name of hashtag without the "#": Cntrl + C to go back to menu' )
	s.send(tagString)

	if tagString == '-1':
		return

	allMatchingTweets = custRecv(s)
	time.sleep(1)

	os.system('clear')
	if allMatchingTweets == 'noneFound':
		print '\tNo tweets with #' + tagString + ' found in database.'

	else:
		print allMatchingTweets
	return 

def clientSeeSubscriptions(s):
	subscriptions = custRecv(s)
	print subscriptions
	return None

def clientSeeFollowers(s):

	followers = custRecv(s)
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
		uname = custPrompt( s, 'username: ' )
		s.send( uname)

		pwd = custPrompt(s, 'password:')
		
		
		s.send( pwd)
		vMsg = custRecv(s)

		print vMsg

		if vMsg == str(1):
			userOK = True
			os.system('clear')
			print 'Welcome back, ' + uname + '!\n'
			msgNum = custRecv(s)
			time.sleep(1)
			print 'You have ' + msgNum + ' unread messages.\n\n'

		else:
			print 'Incorrect username/password! Please reenter.\n'

	while 1:
		runMenu(s)

#---------------------------------------------------------------------------------------------------------------------------------------------------------
login()
