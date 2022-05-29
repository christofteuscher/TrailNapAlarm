

import time
import numpy as np

from smbus import SMBus
from scipy.io.wavfile import write as write_wavfile

from every import every

bus = SMBus(2)

adc_sample_config = [0x85, # Precision selection
                     0x83] # ???

def ads1115_read_a0(): # ads1115
    global bus, adc_sample_config
    
    # Sample I2C data.
    a = bus.write_i2c_block_data(0x48, 0x01, adc_sample_config)
    
    time.sleep(1/10000) # Wait for conversion
        
    # Read result of conversion.
    b = bus.read_i2c_block_data(0x48, 0x00, 2)
    raw = int(b[0]*256 + b[1])
    val = raw  * .0000625
    return (val, raw, b, a)


def sample_accumulate(sample_rate=200, epoch_seconds=30):
    epoch = np.zeros(epoch_seconds * sample_rate)
    epoch_i = 0
    epoch_num = 0
    
    def sample():
        nonlocal epoch, epoch_i, epoch_num
        
        val, raw, *_ = ads1115_read_a0()
        epoch[epoch_i] = raw
        if __debug__:
            print("\rSecond: {:4d} Sample: {:3d} Value: {:1.3f}  {:8f}".format(epoch_i // sample_rate, epoch_i % sample_rate, val, raw), end="", flush=True)
        
        
        epoch_i += 1
        if epoch_i == len(epoch):
            print("\nEpoch {:5d} Done.", epoch_num)
            epoch_num += 1
            epoch_i = 0
            
            path = "../res/data/sessions/currentsession"
            write_wavfile("{}/epoch{:02}.wav".format(path, epoch_num), sample_rate, epoch.astype(np.int16))
            
    every(1/sample_rate, sample)

if __name__ == "__main__":
    sample_accumulate()