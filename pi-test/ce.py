import os
import picamera
import time

# utilities raspistill -o image.jpg
# raspivid -o vid.h264 -t 5000

# capture an image
camera = picamera.PiCamera()
# camera.vflip # flips the camera
camera.capture('test.jpg')

# capture a video - omxplayer to see it
camera.start_recording('test.h264')
time.sleep(5)
camera.stop_recording()
 
