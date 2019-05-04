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

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
 
# Create an object of the class MFRC522
MIFAREReader = mfrc522.MFRC522()

print ("Press Ctrl-C to stop.")

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
	tcp_write(UID_accredited)
	print(". .")
	print(". . .")
	return tcp_read()

def close_connection(): # Closing the pipe
	tcp_write('-1')
	s.close()

initiate_connection(IPADDRESS, PORT)


count = 0.0
charging_active = False

GPIO.setwarnings(False)
#Configure LED Output Pin
BUZZ = 7
GPIO.setup(BUZZ, GPIO.OUT)
GPIO.output(BUZZ, GPIO.LOW)
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # If a card is found
    if status == MIFAREReader.MI_OK:
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue

    if status == MIFAREReader.MI_OK:
 
        # Print UID
        print ("Card read with UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
        # This is the default key for authentication
        #key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        #ENTER Your Card UID here
        #my_uid = [130,202,95,9,30]

        uid_check = " ".join(str(x) for x in uid)
        
        #Check to see if card UID read matches your card UID
        if accreditation(uid_check) == '1':
        #if uid == my_uid:                #Open the Doggy Door if matching UIDs
            print("Access Granted")
            charging_active = True
            GPIO.output(BUZZ, GPIO.HIGH)  #Turn on LED
            charging_uid = uid
            time.sleep(0.5)
            #GPIO.output(LED, GPIO.LOW)   #Turn off LED
        
        else:                            #Don't open if UIDs don't match
            print("Access Denied")
    else:
        GPIO.output(BUZZ, GPIO.LOW)
        # if charging_active == True and count > 0:
        #     print("UID: %s charged for %3.1f seconds" % (str(charging_uid),count))
        #     count = 0
        #     charging_active == False



#print(accreditation(UID_accredited))
close_connection()
