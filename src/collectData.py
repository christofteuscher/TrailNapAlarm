#!/usr/bin/python3
#//////////////////////////////////////
# 	collectData.py
# 	Setup:	
# 	See:	
# ////////////////////////////////////////
import time
import wave
from smbus import SMBus
import subprocess
import numpy as np
import math
import os
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM 

def scan(sampleRate, wavFileDuration, fileName):
    ADC.setup()
        
    #print("collect starting")
    #time.sleep(3)
    
    adcData = [0] * (sampleRate * wavFileDuration)
    inputPin  = "AIN0";
    PWMReadPin = "AIN1"
    outputPin = "P1_36";
                
    # Open i2c bus 2 and read one byte from address 48, offset 0
    bus = SMBus(2)
    data1 = [0x85, 0x83]
    raw = 0
    out = 0
    #begin = time.perf_counter()
    while(ADC.read(PWMReadPin) < 0.01):
        
        for x in range(sampleRate * wavFileDuration):
            a = bus.write_i2c_block_data(0x48, 0x01, data1)
            time.sleep((sampleRate ** -1 + 0.008))
            b = bus.read_i2c_block_data(0x48, 0x00, 2)
            raw = b[0]*256 + b[1]
            out = raw  * .0000625
            adcData[x] = out;
            
        adcData = np.array(adcData, dtype=np.float32)
        write(fileName, sampleRate, adcData.astype(np.float32))
        #print("Writing Data...")
        time.sleep(3)
        #print(fileName + " has been written.")
        
    #../res/data/yasaDatasets/
    PWM.set_duty_cycle(outputPin, 0)
    bus.close()
    #print("Shutting down...")
    #os.system('sudo shutdown -P now')
