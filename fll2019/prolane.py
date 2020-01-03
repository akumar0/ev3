#!/usr/bin/env python3
########################################################################
# Filename    : prolane.py
# Description : Basic program for protector lane
# Author      : Wall e worker
# modification: 2019/12/10
########################################################################
import RPi.GPIO as GPIO
import time
import picamera
import subprocess
from SevenSegmentDisplay import SevenSegmentDisplay

''' Sensors used:
    ultrasonic sensor for distance
    led for lighting up
    button(s) for monitoring press
    rfid for detecting valid vehicles
'''
ledPin = 11    # define the ledPin GPIO17
buttonPin = 12    # define the buttonPin
trigPin1 = 16 #GPIO23
echoPin1 = 18  #GPIO24
trigPin2 = 13 #GPIO27
echoPin2 = 15 #GPIO22
MAX_DISTANCE = 100          #define the maximum measured distance in cm
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance
                            # this is in micro seconds. factor = (1/100) * (1/340)    * 10^6  ~=60
                            #                                     cm->m   sound_speed    s->microsecond
VEHICLE_DIST = 7

camera = None
segmentDisplay = SevenSegmentDisplay()

def showImage(pic):
    if (pic == None):
        pic = 'temppic.jpg'

    camera.capture(pic)
    imgshow = subprocess.Popen(["gpicview", pic])
    time.sleep(5)
    imgshow.kill()

def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set buttonPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(trigPin1, GPIO.OUT)   #
    GPIO.setup(echoPin1, GPIO.IN)    #
    camera = picamera.PiCamera()
    segmentDisplay.setup()

def destroy():
    GPIO.output(ledPin, GPIO.LOW)     # led off
    GPIO.cleanup()         #release resource

def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar(trigPin, echoPin):     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance

def testButton():
	while True:
		if GPIO.input(buttonPin)==GPIO.LOW:
			GPIO.output(ledPin,GPIO.HIGH)
			print ('led on ...')
		else :
			GPIO.output(ledPin,GPIO.LOW)
			print ('led off ...')	

def reportDetection(isViolation):
    # Light up the LED
    GPIO.output(ledPin,GPIO.HIGH)
    if (isViolation):
        print("Violation detected!")
        segmentDisplay.showDigit(1)
    else:
        segmentDisplay.shiftDigit(0)

    # Show V on the violation if violation else print B for bus
    # Take a picture and show on the screen
    showImage('prox.jpg')

def clearDisplay():
    GPIO.output(ledPin,GPIO.LOW)

def loop():
    farMode = True
    clearDisplay()
    while True:
        # check ultrasonic sensor to detect vehicle
        distance = getSonar(trigPin1, echoPin1)
        if (distance < VEHICLE_DIST) and farMode:
            farMode = False
            distance1 = getSonar(trigPin2, echoPin2)
            if (distance1 < VEHICLE_DIST):
                # is a bus so not a violation
                reportDetection(False)
            else:
                reportDetection(True)
        else:
            if (not farMode):
                print("Vehicle is gone. Monitoring again.")
                clearDisplay()
            farMode = True

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()