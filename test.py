import time
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

import cv2
#from adafruit_servokit import *
import JoyStickModule as jsM



i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

pca.channels[1].duty_cycle = 40000
time.sleep(1)
pca.channels[1].duty_cycle = 0
time.sleep(1)

#kit = ServoKit(channels =16)
#kit.continuous_servo[1].throttle = -1
#cam = cv2.VideoCapture(0)
#kit.frequency = 

servo1 = servo.Servo(pca.channels[0])
cam = cv2.VideoCapture(0)


while True:
    joyVal = jsM.getJS()
    if joyVal['axis3'] > 0 and joyVal['axis3'] <=1:
        #kit.servo[0].angle = 90 - ((joyVal['axis3']/1)*90)
        servo1.angle = 90 - ((joyVal['axis3']/1)*90)    
    elif joyVal['axis3'] < 0 and joyVal['axis3'] >= -1:
        #kit.servo[0].angle = 90 + ((abs(joyVal['axis3']))/1*90)
        servo1.angle = 90 + ((abs(joyVal['axis3']))/1*90)
    elif joyVal['axis3'] == 0:
        #kit.servo[0].angle = 90
        servo1.angle = 90
    #if kit.servo[0].angle >= 150:
            #kit.servo[0].angle = 150
    if servo1.angle >= 170:
            servo1.angle = 170
    #if kit.servo[0].angle <= 50:
            #kit.servo[0].angle = 50
    if servo1.angle <= 10:
            servo1.angle = 10
    #print(kit.servo[0].angle)
    print(servo1.angle)
    if joyVal['axis2'] == -1:
        pca.channels[1].duty_cycle = 3800
    elif joyVal['axis2'] == 1:
        pca.channels[1].duty_cycle = 0

    ret, image = cam.read()
    cv2.imshow('Imagetest',image)
    k = cv2.waitKey(1)
    if k != -1:
        break
cv2.imwrite('/home/pi/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()
