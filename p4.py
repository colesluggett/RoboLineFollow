# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import tkinter as tk
import time
import cv2
import imutils
import maestro                                                     

MOTORS = 1
TURN = 2
BODY = 0
HEADTILT = 4
HEADTURN = 3

def brighten(img, value = 70):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

##def sendCommand(x):
##    if(x == '8'):
##        tango.setTarget(MOTOR, 6800)
class KeyControl():
    def __init__(self,win):
        self.root = win
        self.tango = maestro.Controller()
        self.body = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.motors = 6000
        self.turn = 6000
        
    def head(self,key):
        if key == 'u':
            self.headTilt = 5500
            if(self.headTilt > 7900):
                self.headTilt = 7900
            self.tango.setTarget(HEADTILT, self.headTilt)
        elif key == 'd':
            self.headTilt = 1510
            if(self.headTilt < 1510):
                self.headTilt = 1510
            self.tango.setTarget(HEADTILT, self.headTilt)
            
   
    
    def arrow(self, key):
        #print(key.keycode)
        if key == 'f':
            self.turn = 6000
            self.motors = 5200
            if(self.motors > 7900):
                self.motors = 7900
            print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
            self.tango.setTarget(TURN, self.turn)
        elif key == 'l':
            self.turn = 5100
            if(self.turn > 7400):
                self.turn = 7400
            print(self.turn)
            self.tango.setTarget(TURN, self.turn)
        elif key == 'r':
            self.turn = 6900
            if(self.turn <2110):
                self.turn = 2110
            print(self.turn)
            self.tango.setTarget(TURN, self.turn)
        
        elif key == 's':
            self.motors = 6000
            self.turn = 6000
            self.tango.setTarget(MOTORS, self.motors)
            self.tango.setTarget(TURN, self.turn)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

kernel = np.ones((5,5), np.uint8)

# allow the camera to warmup
time.sleep(0.1)

win = "Frame"
keys = KeyControl(win)

#keys.head('u')
keys.head('d')

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    pic = brighten(image)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(pic,127,255,0)
    pic = cv2.blur(pic, (3,3))
    pic = pic[120:330,160:480]
    pic = cv2.Canny(pic, 100, 170)
    pic = cv2.dilate(pic, kernel, iterations=1)
    pixels = np.argwhere(pic == 255)
    mean = np.mean(pixels,axis=0)
    floor = mean.astype(int)
    y = floor[0]
    x = floor[1]
    mid = 160
    print(x)

    #cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", pic)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    win = "Frame"
    keys = KeyControl(win)
        
    if x >= 140 and x <= 180:
        keys.arrow('f')
    if x < 140:
        keys.arrow('r')
    if x > 180:
        keys.arrow('l')
    if x < 20:
        keys.arrow('s')
        keys.head('u')
        break

    keys = KeyControl(win)
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

