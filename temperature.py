import os
import pigpio
import DHT22
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep

    

class Temp():
    
    os.system('sudo pigpiod')
    pi = pigpio.pi()
    pin=4
    dht22 = DHT22.sensor(pi,pin) 
    dht22.trigger()
    sleepTime = 3
    
    def readDHT22(self):
        self.dht22.trigger()
        humidity = '%.2f' % (self.dht22.humidity())
        temp = '%.2f' % (self.dht22.temperature())
        return (humidity, temp)
