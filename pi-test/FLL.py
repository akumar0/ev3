#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import os
import picamera
import subprocess

ledPin = 11    # define the ledPin
trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

def showImage(pic):
    imgshow = subprocess.Popen(["gpicview", pic])
    time.sleep(5)
    imgshow.kill()

def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance
    
def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       #numbers GPIOs by physical location
    GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
    GPIO.setup(trigPin, GPIO.OUT)   #
    GPIO.setup(echoPin, GPIO.IN)    #

def loop():
    camera = picamera.PiCamera()
    farState=True
    while(True):
        distance = getSonar()
        #print ("The distance is : %.2f cm"%(distance))
        if (distance < 6.0) and farState:
            print ("Detected some near object at %.2f cm"%(distance) )
            farState=False
            GPIO.output(ledPin,GPIO.HIGH)
            # camera.vflip # flips the camera
            camera.capture('prox.jpg')
            showImage('prox.jpg')
        else:
            if (not farState):
              print("Object is gone away")
            farState=True
            GPIO.output(ledPin,GPIO.LOW)
        #time.sleep(0.1)
        
if __name__ == '__main__':     #program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
        GPIO.output(ledPin, GPIO.LOW)     # led off
        GPIO.cleanup()         #release resource

