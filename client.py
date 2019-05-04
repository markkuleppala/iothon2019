# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197 and https://gist.github.com/BenKnisley/5647884

import socket, time
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IPADDRESS = "10.84.109.147"
UID_accredited = [130,202,95,9,30]
UID_accredited = " ".join(str(x) for x in UID_accredited)
UID_accredited = str(UID_accredited)


def Tcp_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
   
def Tcp_Write(D):
   s.send(D + '\r')
   return 
   
def Tcp_Read():
	a = ' '
	b = ''
	a = s.recv(1)
	while a != '\r':
		b = b + a
		a = s.recv(1)
	return b

def Tcp_Close():
   s.close()
   return 
   
Tcp_connect(IPADDRESS, 6666)
print("yksi")
Tcp_Write(UID_accredited)
print("kaksi")
#print("---%s---" % (Tcp_Read())
print("kolme")
Tcp_Write('hi')
print Tcp_Read()
Tcp_Close()

# try:
#      while 1:
#           data = raw_input("Enter Data :")

# 6666 = Number Port
#           client_socket.sendto(data, (IPADDRESS,6666))
#           print ("Sending request")

# except Exception as ex:
#     print ex
#     raw_input()

# client_socket.close()