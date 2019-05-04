# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197

import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IPADDRESS = "10.84.109.147"

try:
     while 1:
          data = raw_input("Enter Data :")

# 6666 = Number Port
          client_socket.sendto(data, (IPADDRESS,6666))
          print ("Sending request")

except Exception as ex:
    print ex
    raw_input()

client_socket.close()