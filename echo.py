import time
from check import ip_checksum
import socket
import sys

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port


class User:
	def __init__(self, u, p):
		self.uname = u;
		self.pwd =  p;


	def userVerify(self, u, p):
		if u == self.uname and p == self.pwd:
			return True

		else:
			return False


#Define functions here!

def checkUserList(ulist, userTemp, pwdTemp): 
	for user in ulist:
		if user.userVerify(userTemp , pwdTemp) is True:
			return "Welcome back! " + user.uname + ".\n"

	return "User/Password is incorrect! Re-Enter information. \n"

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


#Main Code

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

conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])     
userTemp = conn.recv(1024)
pwdTemp = conn.recv(1024)

msg = checkUserList(userlist,userTemp, pwdTemp) 
s.sendall(msg)
#conn.close()
#s.close()



