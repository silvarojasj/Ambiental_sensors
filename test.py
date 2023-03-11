import os
import pigpio
import DHT22
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep


def readDHT22():

    dht22.trigger()
    humidity = '%.2f' % (dht22.humidity())
    temp = '%.2f' % (dht22.temperature())
    return (humidity, temp)

def getData(OData,OHData):
    while True:
        humidity, temperature = readDHT22()
        print("Humidity is: " + humidity + "%")
        print("Temperature is: " + temperature + "C")
        sleep(sleepTime)
        OData[1].append(float(temperature))
        OHData[1].append(float(humidity))
        if(len(OData[1])>20):
            OData[1].pop(0)
            OHData[1].pop(0)
            
def init_func():
    ax1.clear()
    ax2.clear()
    ax1.set_title('Temperatura')
    ax2.set_title('Humedad')
    ax1.set_xlim(0,20)
    ax1.set_ylim(-5,40)
    ax2.set_xlim(0,20)
    ax2.set_ylim(0,100)
    
def Update_line(num,data1,data2):
    dx1=np.asarray(range(len(data1[1])))
    dy1=np.asarray(data1[1])
    dx2=np.asarray(range(len(data2[1])))
    dy2=np.asarray(data2[1])
    ax1.plot(dx1,dy1)
    ax2.plot(dx2,dy2)

os.system('sudo pigpiod')
pi = pigpio.pi()
pin=4
TData=[]
TData.append([0.0])
TData.append([0.0])
HData=[]
HData.append([0.0])
HData.append([0.0])
dht22 = DHT22.sensor(pi,pin) 
dht22.trigger()
#print('hola mundo')
sleepTime = 3
fig=plt.figure()
ax1=plt.subplot(1,2,1)
ax2=plt.subplot(1,2,2)
dataC=threading.Thread(target=getData,args=(TData,HData,))
dataC.start()
line_A=animation.FuncAnimation(fig,Update_line,fargs=(TData,HData),frames=200,init_func=init_func,interval=3)
plt.show()
dataC.join()