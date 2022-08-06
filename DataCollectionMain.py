
import WebcamModule as wM
import DataCollectionModule as dcM
#from adafruit_servokit import ServoKit
from time import sleep
import JoyStickModule as jsM
import cv2
import time
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

pca.channels[8].duty_cycle = 40000
time.sleep(1)
pca.channels[8].duty_cycle = 0
time.sleep(1)
servo1 = servo.Servo(pca.channels[0])
#kit = ServoKit(channels =16)
#kit.frequency = 50
record = 0

while True:    
    joyVal = jsM.getJS()
    steering = servo1.angle
    if joyVal['axis3'] > 0 and joyVal['axis3'] <=1:
        #kit.servo[0].angle = 90 - ((joyVal['axis3']/1)*90)
        servo1.angle = 90 - ((joyVal['axis3']/1)*90)     
    elif joyVal['axis3'] < 0 and joyVal['axis3'] >= -1:
        #kit.servo[0].angle = 90 + ((abs(joyVal['axis3']))/1*90)
        servo1.angle = 90 + ((abs(joyVal['axis3']))/1*90)
    elif joyVal['axis3'] == 0:
        #kit.servo[0].angle = 90
        servo1.angle = 90
    #if kit.servo[0].angle >= 160:
            #kit.servo[0].angle = 160
    #if kit.servo[0].angle <= 30:
            #kit.servo[0].angle = 30
    if servo1.angle >= 150:
            servo1.angle = 150
    if servo1.angle <= 50:
            servo1.angle = 50
    
   # throttle = joyVal['axis2']
    #throttle = kit.continuous_servo[1].throttle
    if joyVal['axis2'] == -1:
        #kit.continuous_servo[1].throttle = 0.45
        #throttle = 0.045
        pca.channels[1].duty_cycle = 3850
    elif joyVal['axis2'] == 1:
        #kit.continuous_servo[1].throttle = -1
        #throttle = -1
        pca.channels[1].duty_cycle = 0
        
    
    if joyVal['L1'] == 1:
        if record ==0: print('Recording Started ...')
        record +=1
        sleep(0.500)
    if record == 1:
        img = wM.getImg(True,size=[480,360])
        dcM.saveData(img,steering)
    elif record == 2:
        dcM.saveLog()
        record = 0

    cv2.waitKey(1)
