import time
from check import ip_checksum
import socket
import sys
from thread import *

#-------------------------------------------------------------------------------------------------------------

class User:
	def __init__(self, u, p):
		self.uname = u; #username
		self.pwd =  p; #password
		self.tweetList = [] #contains list of tweets
		self.subList = [] #who you are subscribed to
		self.status = 'offline' #status -> offline or online
		self.offlineQueue = [] #your offline tweet queue -> flush on logout
		self.followersList = [] #your followers
		self.onlineQueue = []

	def userVerify(self, u, p):
		if u == self.uname and p == self.pwd:
			return True
		else:
			return False

	def getMsgAmnt(self):
		return len(self.offlineQueue)

	def addTweet(self, submittedTweet, conn):  #append new tweet to tweetList, containing msg and hashtags
		self.tweetList.append(submittedTweet)
		for user in self.followersList:
			if user.status == 'offline':
				user.offlineQueue.append(submittedTweet)
			elif user.status == 'online' :
				#start background thread that sends tweet to client without interrrupting server
				#threadOnlineSender(user, conn, submittedTweet)
				user.onlineQueue.append(submittedTweet)

		return None	


	def logOutUser(self):
		self.offlineQueue = [] #flush
		self.status = 'offline'
		return



def appendTagsList(message):

	hashtagList = []
	splitString = message.split() 
	for word in splitString:
		if word.startswith('#') is True:
			hashtagList.append(word[1:]) #remove hashtag and append to the list	
	return hashtagList

class Tweet:
	def __init__(self,message, user):
		self.message = message
		self.hashtagList = appendTagsList(message)
		self.timestamp = time.time()
		self.owner = user

	def __lt__(self, other) : #comparator function to sort from greatest -> least
		return self.timestamp > other.timestamp

	def serachForTag(self,requestedTag):

		for tag in self.hashtagList:
			if tag == requestedTag:
				return True
		return False

#Define main functions here!


def checkUserList(ulist, userTemp, pwdTemp): 
	for user in ulist:
		if user.userVerify(userTemp , pwdTemp) is True:
			user.status = 'online'
			return user
	return None

def userNameDeclare():
	#Declare User List Here!
	userlist = []
	user1 = User("stephanie", "tong")
	user2 = User("naruto", "nina")
	user3 = User("ryota", "saito")
	user4 = User("hello", "world")
	userlist.append(user1);
	userlist.append(user2);
	userlist.append(user3);
	userlist.append(user4);
	return userlist

def sendUserMsgNum(curUser):
	return curUser.getMsgAmnt()

def DuplicateSub(curUser, username):
	for user in curUser.subList:
		if user.uname == username:
			return True
	return False

def runAction(conn, curUser):

	n = conn.recv(1024)
	time.sleep(1)
	if n == '1':
		serverSeeOffline(conn, curUser)
	elif n == '2': 
		serverEditSub(conn, curUser)
	elif n == '3':
		serverPostMsg(conn, curUser)
	elif n == '4':
		serverSearchHashtag(conn, curUser)
	elif n == '5':
		serverGetSubs(conn, curUser)
	elif n == '6':
		serverGetFollowers(conn, curUser)
	elif n == '7':
		return serverLogout(curUser) #returns -1
	else:
		return 0

def printTweet(tweet_list):

	tweet_list.sort()
	messageOutput = ''
	for tweet in tweet_list:
		messageOutput += '='*80 + '\n' + tweet.owner.uname + '   ' + time.asctime(time.localtime(tweet.timestamp ) )+ ' : \n\n\t' +  tweet.message + '\n'

	return messageOutput

def getUser(userWanted, user_list):

	for user in user_list:
		if userWanted == user.uname:
			return user
	return -1


def serverSeeOffline(conn, curUser):

	while 1:
		offlineSelect = conn.recv(1024)
		time.sleep(1)

		if offlineSelect == '1':

			if len(curUser.offlineQueue) == 0:
				msg = 'You have no unread messages to display. \n'
			else:
				msg =printTweet(curUser.offlineQueue)	

			conn.send(msg)
			return 

		elif offlineSelect == '2':

			conn.send(listSubscriptions(curUser))
			userSelect = conn.recv(1024)
			time.sleep(1)

			userWanted = getUser(userSelect, curUser.subList)

			if userWanted == -1:
				msg = "Select a valid user from the list. \n"

			singleUserTweets = []
			for tweet in curUser.offlineQueue:
				if tweet.owner == userWanted: 
					
					singleUserTweets.append(tweet)

			if len(singleUserTweets) == 0:
				msg = 'No tweets available from the user\n'

			else:
				msg = printTweet(singleUserTweets)

			conn.send(msg)
			return

		elif offlineSelect == '3':

			return


def addSub(conn, curUser):
	
	while 1:
		dup = False
		requestedUser = conn.recv(4096)

		for user in USERLIST:
			if user.uname == requestedUser and  user.uname != curUser.uname:

				if DuplicateSub(curUser,requestedUser):
					dup = True

				else:
					curUser.subList.append(user)
					user.followersList.append(curUser)

					conn.send( 'found')
					return None

		if dup is True:
			conn.send('duplicate')

		else:
			conn.send('bad')

def listSubscriptions(curUser):
	subs = ''

	if len(curUser.subList) == 0:
		subs = '\tYou are not subscribed to anyone! \n'

	#grab all useres in sublist and add ther names into 1 string
	
	else:
		for user in curUser.subList:
			subs += '\t' + user.uname + '\n'

	return subs

def delSub(conn, curUser):

#end early if empty subList on server

	if len(curUser.subList) == 0:
		conn.send('emptyList')
		serverEditSub(conn, curUser)
		return 

	conn.send(listSubscriptions(curUser))

	while 1:
		delCan = conn.recv(1024)
		time.sleep(1)
		for u in curUser.subList:
			
			tmp = u.uname 
			if tmp == delCan:
				conn.send('ok')
				curUser.subList.remove(u) #remove from sublist and send msg deleted
				u.followersList.remove(curUser)
				return None

		conn.send('notFound')	

def serverEditSub(conn, curUser):

	subSelection = conn.recv(1024)
	time.sleep(1)
	
	if subSelection == '1':
		addSub(conn, curUser)

	elif subSelection == '2':
		delSub(conn, curUser)
		
	elif subSelection == '3':
		return None
	else:
		print 'not correct input'
	return None


def updateSTOREDCOUNT():

	global STOREDCOUNT
	for user in USERLIST:
		for tweet in user.offlineQueue:
			STOREDCOUNT+= 1



def serverPostMsg(conn, curUser):
	#wait for message to be tweeted
	msg = conn.recv(4096)
	time.sleep(1)
	newTweet = Tweet(msg, curUser)
	curUser.addTweet(newTweet, conn)

	global MSGCOUNT
	MSGCOUNT += 1
	updateSTOREDCOUNT()
	return None

def getTweetsAllUsers(requsetedTag):

	matchingTweetsMsg = []

	for user in USERLIST:
		for tweet in user.tweetList:
			if tweet.serachForTag(requsetedTag):
				matchingTweetsMsg.append(tweet)

	messageOutput = ''

	if len(matchingTweetsMsg) == 0:
		return 'noneFound' 

	matchingTweetsMsg.sort() #sort tweet from newest to oldest
	matchingTweetsMsg = matchingTweetsMsg[:10] #grab 10 newest

	return printTweet(matchingTweetsMsg)


def serverSearchHashtag(conn, curUser):

	requsetedTag = conn.recv(1024)
	time.sleep(1)
	allTweets  = getTweetsAllUsers(requsetedTag)
	conn.sendall(allTweets)
	return None

def serverGetSubs(conn, curUser):
	
	subs = 'Current subscriptions: \n'
	subs += listSubscriptions(curUser)
	print '\n'
	conn.send(subs)
	return None

def listFollowers(curUser):
	follow = ''
	#grab all useres in sublist and add ther names into 1 string

	if len(curUser.followersList) == 0:
		follow = '\tNo one is following you!'
	else:
		for user in curUser.followersList:
			follow += '\t' + user.uname + '\n'

	return follow

def serverGetFollowers(conn, curUser):

	followers = 'Current followers: \n'
	followers += listFollowers(curUser)
	print '\n'

	conn.send(followers)
	return None

def serverLogout(curUser):
	curUser.logOutUser()
	updateSTOREDCOUNT()
	global ONLINEUSERS 
	ONLINEUSERS -= 1

	return -1

def checkOnlineQueue(curUser,conn):

	while 1:
		if len(curUser.onlineQueue) != 0: 
			print 'sending msg'
			tweet = curUser.onlineQueue[0] 
			msg =''
			
			s.send('__realTime__')
			ack = conn.recv(1024)
			if ack == 'readyRecv':

			 	msg += '\n' +' ='*80 + '\n' + tweet.owner.uname + '   ' + time.asctime(time.localtime(tweet.timestamp ) )+ ' : \n\n\t' +  tweet.message + '\n' + '='*80 + '\n'
				conn.send( msg)
				curUser.onlineQueue = []
				time.sleep(2)
			

def connNewClient(conn):
	userVerify = False

	while userVerify is False:
		
		userTemp = conn.recv(1024)
		pwdTemp = conn.recv(1024)

		print userTemp
		print pwdTemp

		userOK = checkUserList(USERLIST,userTemp, pwdTemp) 
		if userOK:
			msg = str(1)
			userVerify = True
			userOK.status = 'online'


		else:
			msg = str(0)

		conn.send(msg)
		time.sleep(1)


	conn.send(str(sendUserMsgNum(userOK)))
	global ONLINEUSERS 
	ONLINEUSERS += 1


	while 1:
		if runAction(conn, userOK) is -1:
			return None

	

def commandLine():

	global MSGCOUNT 
	global ONLINEUSERS 

	while 1:
		cmd = raw_input(':')

		if cmd == 'messagecount' :
			print 'Total # off messages: ' + str(MSGCOUNT) + '\n'

		elif cmd == 'usercount':
			print 'Users online: ' + str(ONLINEUSERS )+ '\n'

		elif cmd == 'usercount':
			print 'Users online: ' + str(STOREDCOUNT )+ '\n'

		elif cmd == 'newuser':
			username = raw_input('\ttype a username:')
			password = raw_input('\ttype a password:')
			newUsr = User(username,password)
			USERLIST.append(newUsr)
			print 'added user ' + username +'.\n'

		else:
			pass



def setupSock():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 
	try:
	    s.bind((HOST, PORT))
	except socket.error , msg:
	    sys.exit()	 
	s.listen(10)

	#create new thread here
	while 1:

		conn, addr = s.accept()
		start_new_thread(connNewClient ,(conn,))


#-----------------------------------------------------------------------------------------
#Main Code

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port


global MSGCOUNT 
global ONLINEUSERS
global STOREDCOUNT 
global USERLIST
MSGCOUNT = 0
ONLINEUSERS = 0 
STOREDCOUNT = 0
USERLIST = []


USERLIST = userNameDeclare()
start_new_thread(setupSock, ())
#commandLine()
