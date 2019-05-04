# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197, https://www.deviceplus.com/connect/integrate-rfid-module-raspberry-pi/ and https://gist.github.com/BenKnisley/5647884

#!/usr/bin/env python
import socket, time
import RPi.GPIO as GPIO
import mfrc522
import signal

IPADDRESS = "10.84.109.147" # Server IP address
PORT = 6666 # Port used
UID_accredited = [130,202,95,9,30] # Accredited RFID keycard
UID_accredited = " ".join(str(x) for x in UID_accredited) # Modify the format into string
#UID_accredited = str(UID_accredited)

continue_reading = True

def tcp_connect(IPADDRESS, PORT):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IPADDRESS, PORT))
    return
   
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

def tcp_close():
   s.close()
   return 

def initiate_connection(IPADDRESS, PORT): 
	tcp_connect(IPADDRESS, PORT)
	
def accreditation(UID_accredited):
	print(".")
	Tcp_Write(UID_accredited)
	print(". .")
	print(". . .")
	return Tcp_Read()

def close_connection # Closing the pipe
	tcp_write('-1')
	s.close()

