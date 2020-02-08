import RPi.GPIO as GPIO
import time
import picamera
import subprocess

MAX_DISTANCE = 500          #define the maximum measured distance in cm
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance
                            # this is in micro seconds. factor = (1/100) * (1/340)    * 10^6  ~=60
                            #                                     cm->m   sound_speed    s->microsecond

def showImage(camera, pic):
    if (pic == None):
        pic = 'temppic.jpg'
    camera.capture(pic)
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
