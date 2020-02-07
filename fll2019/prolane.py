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
from proutility import *
from SevenSegmentDisplay import SevenSegmentDisplay

''' Sensors used:
    ultrasonic sensor for distance
    led for lighting up
'''
ledPin = 11    # define the ledPin GPIO17
buttonPin = 12    # define the buttonPinebtfdvhcrnigkigcubctjjkrunjihcbb

trigPin1 = 16 #GPIO23
echoPin1 = 18  #GPIO24
trigPin2 = 13 #GPIO27
echoPin2 = 15 #GPIO22
VEHICLE_DIST = 7

segmentDisplay = SevenSegmentDisplay()

def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
    #GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set buttonPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(trigPin1, GPIO.OUT)   #
    GPIO.setup(echoPin1, GPIO.IN)    #
    GPIO.setup(trigPin2, GPIO.OUT)   #
    GPIO.setup(echoPin2, GPIO.IN)    #
    segmentDisplay.setup()
    print("setup complete")

def destroy():
    GPIO.output(ledPin, GPIO.LOW)     # led off
    GPIO.cleanup()         #release resource

def reportDetection(camera, isViolation):
    # Light up the LED
    GPIO.output(ledPin,GPIO.HIGH)
    if (isViolation):
        print("Violation detected!")
        segmentDisplay.showDigit(1)
    else:
        print("No violation detected!")
        segmentDisplay.showDigit(0)

    # Show V on the violation if violation else print B for bus
    # Take a picture and show on the screen
    showImage(camera, 'prox.jpg')

def clearDisplay():
    GPIO.output(ledPin,GPIO.LOW)

def loop():
    # access the camera
    camera = picamera.PiCamera()
    farMode = True
    clearDisplay()
    while True:
        # check ultrasonic sensor to detect vehicle
        # getSonar function is used to get the distance 
        distance1 = getSonar(trigPin1, echoPin1)

        if (distance1 < VEHICLE_DIST) and (distance1 > 1) and farMode:
            print("detected object at distance1=" + str(distance1))
            farMode = False
            # Second sensor tells us if the vehicle is long or short
            distance2 = getSonar(trigPin2, echoPin2)
            # 
            if ((distance2 < VEHICLE_DIST) and (distance2 > 1)):
                print("detected object at distance2=" + str(distance2))
                # is a bus so not a violation
                reportDetection(camera, False)
            else:
                # is a car so a violation
                print("not detected object")
                reportDetection(camera, True)
        elif (distance1 >= VEHICLE_DIST) and not farMode:
            print("Vehicle is gone. Monitoring again. distance1=" + str(distance1))
            clearDisplay()
            farMode = True

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()