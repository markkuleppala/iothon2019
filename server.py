# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197

import socket
import RPi.GPIO as GPIO
# GPIO Setting Up
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

GPIO.output(17,False)
GPIO.output(27,False)

users = ['1'] # List of accredited users

# Create a Server Socket and wait for a client to connect
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 6666))
print ("UDPServer Waiting for client on port 6666")

# Define moving functions

def FW():
    GPIO.output(17,True)
    GPIO.output(27,True)
    print ("Forward")


def STOP():
    GPIO.output(17,False)
    GPIO.output(27,False)
    print ("Stop")

options = {    "1" : FW,
               "0" : STOP,
}

# Recive data from client and decide which function to call
charging_status = False # Charging not currently active
while True:
    dataFromClient, address = server_socket.recvfrom(256)
    dataFromClient = dataFromClient.rstrip()
    dataFromClient = str(dataFromClient)
    print(dataFromClient)
    if dataFromClient in users:
    	print("Client ", dataFromClient, " is authorized. Starting charging.")
    	charging_status = True


#    options[dataFromClient]() # Is this needed