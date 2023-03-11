# adapted from sandboxelectronics.com/?p=165

import time
import math
from MCP3008 import MCP3008

class MQ_8():

    ######################### Hardware Related Macros #########################
    MQ_8_PIN                       = 3        # define which analog input channel you are going to use (MCP3008)
    RL_VALUE                     = 5        # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 9.83     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_LPG                      = 0
    GAS_CH4                      = 1
    GAS_CO                       = 2
    ALCOHOL                       =3

    def __init__(self, Ro=10, analogPin=3):
        self.Ro = Ro
        self.MQ_8_PIN = analogPin
        self.adc = MCP3008()
        
        self.LPGCurve = [2.3,51,-18.25]    # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent"
                                            # to the original curve. 
                                            # data format:{ x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 
        self.CH4Curve = [2.30,80,-18.25]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.72), point2: (lg10000,  0.15)
        self.COCurve = [2.3,2.1,-2.25]   # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.53), point2: (lg10000,  -0.22)  
        self.ALCOHOLCurve =  [2.3,40,-30]
        
        print("Calibrating...")
        self.Ro = self.MQ_8Calibration(self.MQ_8_PIN)
        print("Calibration is done...\n")
        print("Ro=%f kohm" % self.Ro)
    
    
    def MQ_8Percentage(self):
        val = {}
        read = self.MQ_8Read(self.MQ_8_PIN)
        val["GAS_LPG"]  = self.MQ_8GetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["GAS_CH4"]  = self.MQ_8GetGasPercentage(read/self.Ro, self.GAS_CH4)
        val["GAS_CO"]   = self.MQ_8GetGasPercentage(read/self.Ro, self.GAS_CO)
        val["ALCOHOL"]  = self.MQ_8GetGasPercentage(read/self.Ro, self.ALCOHOL)
        return val
        
    ######################### MQ_8ResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQ_8ResistanceCalculation(self, raw_adc):
        return float(self.RL_VALUE*(1023.0-raw_adc)/float(raw_adc));
     
     
    ######################### MQ_8Calibration ####################################
    # Input:   MQ_8_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQ_8ResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          10, which differs slightly between different sensors.
    ############################################################################ 
    def MQ_8Calibration(self, MQ_8_pin):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):          # take multiple samples
            val += self.MQ_8ResistanceCalculation(self.adc.read(MQ_8_pin))
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBARAION_SAMPLE_TIMES                 # calculate the average value

        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 

        return val;
      
      
    #########################  MQ_8Read ##########################################
    # Input:   MQ_8_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQ_8ResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def MQ_8Read(self, MQ_8_pin):
        rs = 0.0

        for i in range(self.READ_SAMPLE_TIMES):
            rs += self.MQ_8ResistanceCalculation(self.adc.read(MQ_8_pin))
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs/self.READ_SAMPLE_TIMES

        return rs
     
    #########################  MQ_8GetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQ_8GetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQ_8GetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_LPG ):
            return self.MQ_8GetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == self.GAS_CH4 ):
            return self.MQ_8GetPercentage(rs_ro_ratio, self.CH4Curve)
        elif ( gas_id == self.GAS_CO ):
            return self.MQ_8GetPercentage(rs_ro_ratio, self.COCurve)
        elif (gas_id == self.ALCOHOL):
            return self.MQ_8GetPercentage(rs_ro_ratio, self.ALCOHOLCurve)
        return 0
     
    #########################  MQ_8GetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def MQ_8GetPercentage(self, rs_ro_ratio, pcurve):
        return (math.pow(10,( ((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))

