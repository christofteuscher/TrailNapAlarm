

import time, signal, os
from datetime import datetime
from optparse import OptionParser
from queue import Queue

import numpy as np
from scipy.io.wavfile import write as write_wavfile

from smbus import SMBus
import Adafruit_BBIO.GPIO as GPIO

from every import every

pin_alert = "P2_10"
bus = SMBus(2)
bounce = 5

GPIO.remove_event_detect(pin_alert)
GPIO.setup(pin_alert, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_signal(*args):
    print("handle_signal")
    global record
    record = False
    
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

    
def isr_clear():
    print('isr_clr')
    GPIO.remove_event_detect(pin_alert)
    
def isr_prime():
    print('isr_set')
    GPIO.add_event_detect(pin_alert, GPIO.FALLING, callback=isr_handle, bouncetime=bounce)
    
def isr_handle(channel):
    # Read whenever conversion is done.
    ads1115_read()

#adc_confg = { conversion: [0xB1, 0x83], scale: (2*6.144 / 2**16) }
#adc_confg = { conversion: [0xB3 0x83], scale: (2*4.096 / 2**16) }
#adc_confg = { conversion: [0xB5 0x83], scale: (2*2.048 / 2**16) }
#adc_confg = { conversion: [0xB7, 0x83], scale: (2*1.024 / 2**16) }

class adc_config:
    conversion = [0b01110100, 0b10000000]
    # os:0    No Effect
    # mux:111 (GND - AIN3)   mux:011 (AIN3 - AIN2)
    # pga:010 ±2.048 V
    # mode:0   continuous
    
    # DR:100        128 sps
    # COMP_MODE:0
    # COMP_POL: 0   Alert Active Low
    # COMP_LAT: 0   RDY non-latching
    # COMP_QUE: 00  Each conversion
    rate = 128
    scale = (2*2.048 / 2**16)

def ads1115_continuous():
    if __debug__:
        print("ads1115_continuous")
    # Enable Interrupt first.
    isr_prime()
    
    # Enable Ready interrupt by writing MSB 1 to high threshold register and
    # writing 0 to msb1 of low threashold register.
    bus.write_i2c_block_data(0x48, 0x03, [0b10000000, 0])
    bus.write_i2c_block_data(0x48, 0x02, [0, 0])
    
    # Start Conversion of A2C
    bus.write_i2c_block_data(0x48, 0x01, adc_config.conversion)
    
    if __debug__:
        ads1115_show_config()
    
def ads1115_show_config():
    cfg = int.from_bytes(bus.read_i2c_block_data(0x48, 0x01, 2), byteorder='big', signed=False)
    print(f"cfg: {cfg:#018b}")
    
    ltr = int.from_bytes(bus.read_i2c_block_data(0x48, 0x02, 2), byteorder='big', signed=False)
    print(f"ltr: {ltr:#018b}")
    htr = int.from_bytes(bus.read_i2c_block_data(0x48, 0x03, 2), byteorder='big', signed=False)
    print(f"htr: {htr:#018b}")
    

def ads1115_poweroff():
    if __debug__:
        print("ads1115_poweroff")
    # 
    bus.write_i2c_block_data(0x48, 0x01, [0b00110101, 0b10000000])
    if __debug__:
        ads1115_show_config()

def ads1115_read(): # ads1115
    # Read result of conversion.
    bytes = bus.read_i2c_block_data(0x48, 0x00, 2)
    raw = int.from_bytes(bytes, byteorder='big', signed=True) # Read as int16 two's compliment
    val = raw * adc_config.scale
    
    global queue
    queue.put((raw, val, bytes))


record = True
queue = Queue(128)

def accumulate_start(opts = None):
    rate = adc_config.rate
    epoch = np.zeros(opts.epoch_seconds * rate, dtype=np.int16)
    epoch_i = 0
    epoch_num = 0
    start = datetime.now()
    path = "../data/{}/".format(start.strftime("%Y-%m-%dT%H:%M:%s"))
    rate = adc_config.rate
    
    if opts.wav or opts.csv:
        os.makedirs(path, exist_ok=True)
    
    ads1115_continuous()
    
    while record:
        raw, val, bytes = queue.get(timeout=10)
        if raw is None:
            break
        
        if __debug__:
            if (epoch_i % rate / 2) == 0: # Print 2 times per second
                print("\rSecond: {:4d} {:8d} Sample: {:3d} Value: {:1.3f}  {:8d} {}     ".format(epoch_i // rate, epoch_i, epoch_i % rate, val, raw, bytes), end="", flush=True)
        
        epoch[epoch_i] = raw
        epoch_i += 1
        if epoch_i == len(epoch):
            print("\nEpoch {:5d} Done.".format(epoch_num))
            epoch_num += 1
            epoch_i = 0
            
            if opts.wav:
                write_wavfile("{}/epoch{:02}.wav".format(path, epoch_num), rate, epoch.astype(np.int16))
    
    # Clean up
    isr_clear()
    ads1115_poweroff()
    
if __name__ == "__main__":
    parser = OptionParser(description='Record sampled EEG data.')
    parser.add_option('--wav', dest='wav', action='store_true', default=False,
        help="Save epoch as wav file format.")
    parser.add_option('--csv', dest='csv', action='store_true', default=False,
        help="Save epoch as csv file format. (Not Implemented)")
    parser.add_option('-s', '--seconds', dest='epoch_seconds', action='store', type='int', default=30,
        help="Number of seconds in each epoch.")
    (opts, args) = parser.parse_args()
    accumulate_start(opts=opts)