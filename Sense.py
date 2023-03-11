from Mq_135 import *
from Mq_131 import *
from Mq_9 import *
from Mq_8 import *
from temperature import *
import sys, time
from datetime import date

try:
    print("Press CTRL+C to abort.")
    
    mq  = MQ_135();
    mq2 = MQ_131();
    mq3 = MQ_9();
    mq4 = MQ_8();
    temp = Temp();
    today = date.today()
    url="./data/sense"+str(today)
    file = open(url,"w")
    while True:
       perc = mq.MQ_135Percentage()
       print ("entro MQ_135");
       sys.stdout.write("\r")
       sys.stdout.write("\033[K")
       sys.stdout.write("H2: %g ppm, NH3: %g ppm, C7H8: %g ppm" % (perc["GAS_H2"], perc["GAS_NH3"], perc["GAS_C7H8"]))
       sys.stdout.flush()
       f = open(url,"a")
       f.write("H2: %g ppm, NH3: %g ppm, C7H8: %g ppm" % (perc["GAS_H2"], perc["GAS_NH3"], perc["GAS_C7H8"]))
       time.sleep(60)
       perc = mq2.MQ_131Percentage()
       print ("\nentro MQ_131");
       sys.stdout.write("\r")
       sys.stdout.write("\033[K")
       sys.stdout.write("O3: %g ppm" % (perc["GAS_O3"]))
       sys.stdout.flush()
       f.write("\nO3: %g ppm" % (perc["GAS_O3"]))
       time.sleep(60)
       perc = mq3.MQ_9Percentage()
       print ("\nentro_MQ_9");
       sys.stdout.write("\r")
       sys.stdout.write("\033[K")
       sys.stdout.write("LPG: %g ppm,CH4: %g ppm,CO: %g ppm" % (perc["GAS_LPG"],perc["GAS_CH4"],perc["GAS_CO"]))
       sys.stdout.flush()
       f.write("\nLPG: %g ppm,CH4: %g ppm,CO: %g ppm" % (perc["GAS_LPG"],perc["GAS_CH4"],perc["GAS_CO"]))
       time.sleep(60)
       perc = mq4.MQ_8Percentage()
       print ("\nentro MQ_8");
       sys.stdout.write("\r")
       sys.stdout.write("\033[K")
       sys.stdout.write("LPG: %g ppm,CH4: %g ppm,CO: %g ppm,ALCOHOL: %g ppm" % (perc["GAS_LPG"],perc["GAS_CH4"],perc["GAS_CO"],perc["ALCOHOL"]))
       sys.stdout.flush()
       f.write("\nLPG: %g ppm,CH4: %g ppm,CO: %g ppm,ALCOHOL: %g ppm" % (perc["GAS_LPG"],perc["GAS_CH4"],perc["GAS_CO"],perc["ALCOHOL"]))
       time.sleep(60)
       humidity, temperature= temp.readDHT22()
       print("\nHumidity is: " + humidity + "%")
       f.write("\nHumidity is: " + humidity + "%")
       print("Temperature is: " + temperature + "C")
       f.write("\nTemperature is: " + temperature + "C")
       f.close()
       time.sleep(60)

except:
    print("\nAbort by user")
