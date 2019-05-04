# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197

import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
     data = input("Enter Data :")
# IPADDRESS = RPi IP address
# 6666 = Number Port
     client_socket.sendto(data, ("IPADDRESS",6666))
     print ("Sending request")

except Exception as ex:
    print ex
    raw_input()

client_socket.close()