import cv2
import numpy as np
from adafruit_servokit import ServoKit
import WebcamModule as wM
from openvino.inference_engine import IECore


kit = ServoKit(channels =16)
ie_core= IECore()

#######################################
steeringSen = 1  # Steering Sensitivity
kit.continuous_servo[1].throttle = 0.08  # Forward Speed %
 
net = ie_core_handler.read_network(model="saved_model.xml", weights="saved_model.bin") 
exec_net = ie_core_handler.load_network(network=net, device_name='MYRIAD', num_requests=1)
######################################


def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

while True:

    img = wM.getImg(True, size=[240, 120])
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    steering = float(net.predict(img))
    

        
    kit.continuous_servo[1].throttle = 0.08
    
    cv2.waitKey(1)