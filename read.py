# Copied from: https://www.deviceplus.com/connect/integrate-rfid-module-raspberry-pi/
#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import RPi.GPIO as GPIO
import mfrc522
import signal
import time
 
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
 
# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

count = 0.0
charging_active = False

#Configure LED Output Pin
LED = 7
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # If a card is found
    if status == MIFAREReader.MI_OK:
        #print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue

    if status == MIFAREReader.MI_OK:
 
        # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
        # This is the default key for authentication
        #key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        #ENTER Your Card UID here
        my_uid = [130,202,95,9,30]
        
        #Check to see if card UID read matches your card UID
        if uid == my_uid:                #Open the Doggy Door if matching UIDs
            print("Access Granted")
            charging_active = True
            GPIO.output(LED, GPIO.HIGH)  #Turn on LED
            charging_uid = uid
            sleep(0.5)
            #GPIO.output(LED, GPIO.LOW)   #Turn off LED
        
        else:                            #Don't open if UIDs don't match
            print("Access Denied, YOU SHALL NOT PASS!")
    else:
        GPIO.output(LED, GPIO.LOW)
        # if charging_active == True and count > 0:
        #     print("UID: %s charged for %3.1f seconds" % (str(charging_uid),count))
        #     count = 0
        #     charging_active == False