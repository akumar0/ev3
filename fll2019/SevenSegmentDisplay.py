#!/usr/bin/env python3
#############################################################################
# Filename    : SevenSegmentDisplay.py
# Description : Control SevenSegmentDisplay by 74HC595
# Author      : freenove
# modification: 2018/08/02
########################################################################
import RPi.GPIO as GPIO
import time

class SevenSegmentDisplay:
    LSBFIRST = 1
    MSBFIRST = 2
    # fine the pins connect to 74HC595
    dataPin   = 29		#DS Pin of 74HC595(Pin14)
    latchPin  = 31		#ST_CP Pin of 74HC595(Pin12)
    clockPin = 33		#CH_CP Pin of 74HC595(Pin11)
    #SevenSegmentDisplay display the character "0"- "F"successively
    num = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e]
    def setup(self):
        GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
        GPIO.setup(self.dataPin, GPIO.OUT)
        GPIO.setup(self.latchPin, GPIO.OUT)
        GPIO.setup(self.clockPin, GPIO.OUT)
        
    def shiftOut(self, dPin,cPin,order,val):
        for i in range(0,8):
            GPIO.output(cPin,GPIO.LOW);
            if(order == self.LSBFIRST):
                GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
            elif(order == self.MSBFIRST):
                GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
            GPIO.output(cPin,GPIO.HIGH);

    def showDigit(self, i):
        GPIO.output(self.latchPin, GPIO.LOW)
        self.shiftOut(self.dataPin, self.clockPin, self.MSBFIRST, self.num[i])#Output the figures and the highest level is transfered preferentially.
        GPIO.output(self.latchPin, GPIO.HIGH)

    def loop(self):
        while True:
            for i in range(0,len(num)):
                GPIO.output(self.latchPin,GPIO.LOW)
                shiftOut(self.dataPin, self.clockPin, self.MSBFIRST, num[i])#Output the figures and the highest level is transfered preferentially.
                GPIO.output(self.latchPin, GPIO.HIGH)
                time.sleep(0.5)
            for i in range(0,len(num)):
                GPIO.output(self.latchPin,GPIO.LOW)
                shiftOut(self.dataPin, self.clockPin, self.MSBFIRST, num[i]&0x7f)#Use "&0x7f"to display the decimal point.
                GPIO.output(self.latchPin, GPIO.HIGH)
                time.sleep(0.5)

    def destroy(self):   # When 'Ctrl+C' is pressed, the function is executed. 
        GPIO.cleanup()

if __name__ == '__main__': # Program starting from here 
    print ('Program is starting...' )
    sgd = SevenSegmentDisplay()
    sgd.setup() 
    try:
        sgd.loop()  
    except KeyboardInterrupt:  
        sgd.destroy()  
