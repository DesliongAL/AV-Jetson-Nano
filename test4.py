import time
from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA)

pca = PCA9685(i2c_bus)
pca.frequency = 60

input("press enter")

pca.channels[1].duty_cycle = 40000
time.sleep(1)
pca.channels[1].duty_cycle = 0
time.sleep(1)
pca.channels[1].duty_cycle = 3900
time.sleep(7)
pca.channels[1].duty_cycle = 0
