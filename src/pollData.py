#!/usr/bin/python3
#//////////////////////////////////////
# 	pollData.py
# 	Setup:	
# 	See:	
# ////////////////////////////////////////
import time
import wave
from smbus import SMBus
import subprocess
import numpy as np
import math
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

filename = "test.wav"
channels = 1
sample_rate = 100
adcData = [0] * (100 * 300)

# Open i2c bus 1 and read one byte from address 80, offset 0
bus = SMBus(1)
data1 = [0x85, 0x83]
raw = 0
out = 0
#while(1):
for x in range(1000):
    a = bus.write_i2c_block_data(0x48, 0x01, data1)
    time.sleep(.01)
    b = bus.read_i2c_block_data(0x48, 0x00, 2)
    raw = b[0]*256 + b[1]    
    out = raw * .0000625
    #print(out)
    adcData[x] = out;
adcData = np.array(adcData)
write("Fz.wav",sample_rate,adcData.astype(np.int16))
fs,data = read(Fz.wav)
N = len(data)
ts = 1/fs
t = np.arange(0,ts*N,ts)
plt.plot(t,data)
plt.show()


#../res/data/yasaDatasets/
bus.close()
