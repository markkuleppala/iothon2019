# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197 and https://gist.github.com/BenKnisley/5647884

#!/usr/bin/env python
import socket, time
import RPi.GPIO as GPIO
# GPIO Setting Up

UID_accredited = [130,202,95,9,30] # Accredited user UID
UID_accredited = " ".join(str(x) for x in UID_accredited)

# # Create a Server Socket and wait for a client to connect
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.bind(('', 6666))
# print ("UDPServer Waiting for client on port 6666")

# # Define moving functions

# def FW():
#     GPIO.output(17,True)
#     GPIO.output(27,True)
#     print ("Forward")


# def STOP():
#     GPIO.output(17,False)
#     GPIO.output(27,False)
#     print ("Stop")

# options = {    "1" : FW,
#                "0" : STOP,
# }

# # Recive data from client and decide which function to call
# charging_status = False # Charging not currently active
# while True:
#     dataFromClient, address = server_socket.recvfrom(256)
#     dataFromClient = dataFromClient.rstrip()
#     dataFromClient = str(dataFromClient)
#     print(dataFromClient)
#     if dataFromClient in users:
#     	print("Client %s is authorized. Starting charging.", dataFromClient)
#     	charging_status = True


def Tcp_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
    
def Tcp_server_wait(numofclientwait, port):
	global s2
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s2.bind(('',port)) 
	s2.listen(numofclientwait) 

def Tcp_server_next():
		global s
		s = s2.accept()[0]
   
def Tcp_Write(D):
   s.send(D) + '\r')
   return 
   
def Tcp_Read():
	a = ' '
	b = ''
	while a != '\r':
		a = s.recv(1)
		b = b + a
	return b

def Tcp_Close():
   s.close()
   return

def check_accreditation(UID_received):
	if UID_received == UID_accredited:
		return True
	else:
		return False


Tcp_server_wait(5, 6666)
print("yksi")
Tcp_server_next()
print("kaksi")
message = Tcp_Read()
print(check_accreditation(message))
print("kolme")
Tcp_Write(check_accreditation(message))
print(message)
while  message != -1:
	print Tcp_Read()
print("Closing the server")
Tcp_Close()