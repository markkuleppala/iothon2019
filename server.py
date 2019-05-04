# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197 and https://gist.github.com/BenKnisley/5647884

#!/usr/bin/env python
import socket, time, datetime


f = open("log.txt", "a+") # Initalize log file

PORT = 6666
UID_accredited = [130,202,95,9,30] # Accredited user UID
UID_accredited = " ".join(str(x) for x in UID_accredited) # Format UID to string
charge_interval = 3.0 # Interval for charging

# Server waits for clients
def tcp_server_wait(numofclientwait, PORT):
	global s2
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s2.bind(('', PORT)) 
	s2.listen(numofclientwait) 

# Accepts connections
def tcp_server_next():
		global s
		s = s2.accept()[0]

# Writing to client
def tcp_write(D):
   s.send(D + '\r')
   return 
   
# Reading from client char by char until \r
def tcp_read():
	a = ' '
	b = ''
	a = s.recv(1)
	while a != '\r':
		b = b + a
		a = s.recv(1)
	return b

# Compare read UID to accredited UID
def check_accreditation(UID_received):
	if UID_received == UID_accredited:
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') # Create timestamp
		f.write("%s : UID [%s] used electricity for %.1f seconds\n" % (st, UID_received, charge_interval)) # Write usage to log
		return 1
	else:
		return 0

message = 0 # Placeholder
tcp_server_wait(5, PORT) # Wait for connections
print(".")
tcp_server_next()
while  message != '-1': # Loop until termination char -1
	print(". .")
	message = tcp_read() # Read message from client
	print(". . .")
	tcp_write(str(check_accreditation(message))) # Write result to client
	print(message)
print("Closing the server") # Shutting down the server
s.close()
f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
f.close()