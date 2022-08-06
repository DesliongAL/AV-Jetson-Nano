import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
#from adafruit_servokit import ServoKit
import time
from time import sleep
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from datetime import datetime
import WebcamModule as wM
import JoyStickModule as jsM
import pandas as pd

global imgList, steeringList, steering2List
countFolder = 0
count = 0
dateList = []
steeringList = []
#steering2List = []

myDirectory = os.path.join(os.getcwd(), 'DataObserved')
while os.path.exists(os.path.join(myDirectory,f'log_{str(countFolder)}.csv')):
    countFolder += 1
def saveData(ct,steering):
    global imgList, steeringList, steering2List
    dateList.append(ct)
    steeringList.append(steering)
    #steering2List.append(steering2)
def saveLog():
    global dateList, steeringList, steering2List
    rawData = {'Date': dateList,
                'Steering': steeringList}                #'Steering2':steering2List}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Data: ',len(dateList))
    print('Total Data: ',len(steeringList))
   # print('Total Data: ',len(steering2List))

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

acar = 0
pca.channels[1].duty_cycle = 40000
time.sleep(1)
pca.channels[1].duty_cycle = 0
time.sleep(1)

#kit = ServoKit(channels = 16)
#kit.frequency = 50
#######################################


servo1 = servo.Servo(pca.channels[0])

model = load_model("/home/des/project/car/rcmod/jetson2.h5")
######################################

def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

while True:
    joyVal = jsM.getJS()
    if joyVal['L1'] == 1:
        if acar ==0: print('Recording Started ...')
        acar +=1
        sleep(0.500)
    if acar == 1:
        img = wM.getImg(True, size=[240, 120])
        img = np.asarray(img)
        img = preProcess(img)
        img = np.array([img])
        ct = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        steering = float(model.predict(img))
        
        print(steering)
    
        if steering >= 150 :
           servo1.angle = 150
        elif steering <= 30 :
           servo1.angle = 30
        else:
           servo1.angle = steering

        saveData(ct,steering)
    #kit.continuous_servo[1].throttle = -1
        pca.channels[1].duty_cycle = 3580
        

    elif acar == 2:
        saveLog()
        acar = 0
        pca.channels[1].duty_cycle = 0
    cv2.waitKey(1)

