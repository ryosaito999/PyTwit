import time
from check import ip_checksum
import socket
import sys
from thread import *


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port


class User:
	def __init__(self, u, p):
		self.uname = u;
		self.pwd =  p;
		self.msgList = []
		self.subList = []
		self.status = 'offline'

	def userVerify(self, u, p):
		if u == self.uname and p == self.pwd:
			return True
		else:
			return False


	def getMsgAmnt(self):
		return len(self.msgList)

	def addMessage(self, submittedMsg):
		self.msgList.append(submittedMsg)
		return None

	def logOut(self):
		return None

#Define functions here!

def checkUserList(ulist, userTemp, pwdTemp): 
	for user in ulist:
		if user.userVerify(userTemp , pwdTemp) is True:
			user.status = 'online'
			return user

	return None

def userNameDeclare():
	#Declare User List Here!
	userlist = []
	user1 = User("gintoki", "ichigo")
	user2 = User("kagura", "sadaharu")
	user3 = User("shinpachi", "glasses")
	user4 = User("fruitspunchsamurai", "otae")
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


def editSub(conn, curUser):

	subSelection = conn.recv(1024)
	time.sleep(1)
	
	if subSelection == '1':

		while 1:
			dup = False
			requestedUser = conn.recv(4096)

			print requestedUser
			time.sleep(1)
			for user in userlist:
				if user.uname == requestedUser and  user.uname != curUser.uname:

					if DuplicateSub(curUser,requestedUser):
						dup = True

					else:
						curUser.subList.append(user)
						conn.send( 'found')
						return None

			if dup is True:
				conn.send('duplicate')

			else:
				conn.send('bad')

	elif subSelection == '2':

		#end early if empty subList on server
		if len(curUser.subList) == 0:
			conn.send('emptyList')
			editSub(conn, curUser)
			return 


		subList = ''
		#grab all useres in sublist and add ther names into 1 string
		for user in curUser.subList:
			subList += '\t' + user.uname + '\n'

		conn.send(subList)

		while 1:

			deleteCanidate = conn.recv(1024)
			time.sleep(1)

			#search for delete canidate


			for user in curUser.subList:
			#print user. uname
				if deleteCanidate == user.uname:
					print 'user found \n'
					curUser.subList.remove(user) #remove from sublist and send msg deleted
					conn.send('ok')
					return None

			conn.send('notFound')


	else:
		print 'not correct input'
	return None

def postMsg(conn, curUser):
	#wait for message to be tweeted
	tweet = conn.recv(4096)
	curUser.addMessage(tweet)
	return None

def seeOfflineMsg(conn, curUser):


	return None

def searchHashtag():
	return None


def runAction(conn, curUser):
	n = int(conn.recv(1024))
	time.sleep(1)
	if n == 1:
		seeOfflineMsg(conn, curUser)
	elif n == 2: 
		editSub(conn, curUser)
	elif n == 3:
		postMsg(conn, curUser)
	elif n == 4:
		return -1
	elif n == 5:
		searchHashtag()

	else:
		return None

def connNewClient(conn):
	userVerify = False

	while userVerify is False:
		
		userTemp = conn.recv(1024)
		print userTemp

		pwdTemp = conn.recv(1024)
		print pwdTemp

		curUser = checkUserList(userlist,userTemp, pwdTemp) 
		if curUser:
			msg = str(1)
			userVerify = True

		else:
			msg = str(0)


		conn.send(msg)
		time.sleep(1)

	conn.send(str(sendUserMsgNum(curUser)))

	while 1:
		if runAction(conn, curUser) is -1:
			return None

	

#-----------------------------------------------------------------------------------------
#Main Code
userlist = userNameDeclare()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'


#create new thread here
while 1:

	conn, addr = s.accept()
	start_new_thread(connNewClient ,(conn,))





