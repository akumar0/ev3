import os
import time
import picamera

camera = picamera.PiCamera()

#ans = input("Please enter to take a picture")

for i in range(5):
  print("Taking picture number " + str(i))
  picname = 'pipic' + str(i) + ".jpg"
  camera.capture(picname)
time.sleep(3)
print("start recording")
camera.start_recording('pipic.h264')
time.sleep(10)
camera.stop_recording()
print("done recording")


