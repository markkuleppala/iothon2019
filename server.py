# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197 and https://gist.github.com/BenKnisley/5647884

#!/usr/bin/env python
import socket, time, datetime

f = open("log.txt", "a+")

PORT = 6666
UID_accredited = [130,202,95,9,30] # Accredited user UID
UID_accredited = " ".join(str(x) for x in UID_accredited)
    
def tcp_server_wait(numofclientwait, PORT):
	global s2
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s2.bind(('', PORT)) 
	s2.listen(numofclientwait) 

def tcp_server_next():
		global s
		s = s2.accept()[0]
   
def tcp_write(D):
   s.send(D + '\r')
   return 
   
def tcp_read():
	a = ' '
	b = ''
	a = s.recv(1)
	while a != '\r':
		b = b + a
		a = s.recv(1)
	return b

def check_accreditation(UID_received):
	if UID_received == UID_accredited:
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		f.write("%s : UID [%s] used electricity for 0.5 seconds\n" % (st, UID_received))
		return 1
	else:
		return 0

message = 0 # Placeholder
tcp_server_wait(5, PORT)
print(".")
tcp_server_next()
while  message != '-1':
	print(". .")
	message = tcp_read()
	print(check_accreditation(message))
	print(". . .")
	tcp_write(str(check_accreditation(message)))
	print(message)
print("Closing the server")
s.close()
f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
f.close()