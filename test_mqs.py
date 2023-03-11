# from Mq_135 import *
# from Mq_131 import *
# from Mq_9 import *
from Mq_8 import *
import sys, time

try:
    print("Press CTRL+C to abort.")
    
#     mq = MQ_135();
#     mq2 = MQ_131();
#     mq3 = MQ_9();
    mq4 = MQ_8();
    while True:
#         perc = mq.MQ_135Percentage()
#         print ("entro");
#         sys.stdout.write("\r")
#         sys.stdout.write("\033[K")
#         sys.stdout.write("H2: %g ppm, NH3: %g ppm, C7H8: %g ppm" % (perc["GAS_H2"], perc["GAS_NH3"], perc["GAS_C7H8"]))
#         sys.stdout.flush()
#         time.sleep(0.1)
#          perc = mq2.MQ_131Percentage()
#          print ("entro");
#          sys.stdout.write("\r")
#          sys.stdout.write("\033[K")
#          sys.stdout.write("O3: %g ppm" % (perc["GAS_O3"]))
#          sys.stdout.flush()
#          time.sleep(0.1)
#         perc = mq3.MQ_9Percentage()
#         print ("entro");
#         sys.stdout.write("\r")
#         sys.stdout.write("\033[K")
#         sys.stdout.write("LPG: %g ppm,CH4: %g ppm,CO: %g ppm" % (perc["GAS_LPG"],perc["GAS_CH4"],perc["GAS_CO"]))
#         sys.stdout.flush()
#         time.sleep(0.1)
       perc = mq4.MQ_8Percentage()
       print ("entro");
       sys.stdout.write("\r")
       sys.stdout.write("\033[K")
       sys.stdout.write("LPG: %g ppm,CH4: %g ppm,CO: %g ppm,ALCOHOL: %g ppm" % (perc["GAS_LPG"],perc["GAS_CH4"],perc["GAS_CO"],perc["ALCOHOL"]))
       sys.stdout.flush()
       time.sleep(0.1)

except:
    print("\nAbort by user")

