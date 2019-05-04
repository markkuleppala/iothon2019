# Base for the project copied from https://www.raspberrypi.org/forums/viewtopic.php?t=205197, https://www.deviceplus.com/connect/integrate-rfid-module-raspberry-pi/ and https://gist.github.com/BenKnisley/5647884

#!/usr/bin/env python
import socket, time
import RPi.GPIO as GPIO
import mfrc522
import signal

IPADDRESS = "10.84.109.147" # Server IP address
PORT = 6666 # Port used 
UID_accredited = [130,202,95,9,30] # Accredited RFID keycard
UID_accredited = " ".join(str(x) for x in UID_accredited) # Modify the format into string

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("\nCtrl+C captured, ending read.")
    tcp_write("-1")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
 
# Create an object of the class MFRC522
MIFAREReader = mfrc522.MFRC522()

print ("Press Ctrl-C to stop.")

# Connect to server
def tcp_connect(IPADDRESS, PORT):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IPADDRESS, PORT))
    return

# Write to server  
def tcp_write(D):
   s.send(D + '\r')
   return 

# Read from server   
def tcp_read():
	a = ' '
	b = ''
	a = s.recv(1)
	while a != '\r':
		b = b + a
		a = s.recv(1)
	return b

# Close connection to server
def tcp_close():
   s.close()
   return 

# Check accreditation of keycard inserted	
def accreditation(UID_accredited):
	tcp_write(UID_accredited)
	return tcp_read()

# Closing the pipe and server
def close_connection(): 
	tcp_write('-1')
	s.close()

# Initiate connection to server
tcp_connect(IPADDRESS, PORT)

# Interval for charging
charge_interval = 3.0

# Ignore pin warning
GPIO.setwarnings(False)

#Configure buzzer output pin
BUZZ = 7

#  Set up the buzzer
GPIO.setup(BUZZ, GPIO.OUT)
GPIO.output(BUZZ, GPIO.LOW)
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
 
        # Print UID
        print ("Card read with UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Format UID
        uid_check = " ".join(str(x) for x in uid)
        
        #Check to see if card UID read matches your card UID
        if obj.decrypt(accreditation(uid_check)) == '1':
            print("Access granted for %.1f seconds\n. . ." % charge_interval)
            GPIO.output(BUZZ, GPIO.HIGH)  # Turn on charging (buzzer)
            time.sleep(charge_interval/3) # Time indicators
            print(". .")
            time.sleep(charge_interval/3)
            print(".")
            time.sleep(charge_interval/3)
        
        else: # UID not accredited by server
            print("Access denied\n")
    else:
        GPIO.output(BUZZ, GPIO.LOW) # Turn off the charging (buzzer)

close_connection() # Close connection gracefully
