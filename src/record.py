

import time, signal, os, sys
from datetime import datetime
from optparse import OptionParser
from queue import Queue

import numpy as np
from scipy.io.wavfile import write as write_wavfile

from smbus import SMBus
import Adafruit_BBIO.GPIO as GPIO

pin_alert = "P2_8" # Pin to recieve RDY interrupt from i2c ADC.
#bus = SMBus(2) # Breadboard # Select I2C bus.
bus = SMBus(1) # PCB
bounce = 0          # Bounce detection for interrupt pin.

GPIO.remove_event_detect(pin_alert)
GPIO.setup(pin_alert, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_signal(*args):
    print("handle_signal", *args, file=sys.stderr)
    global record
    record = False # Cancel recording. On next sample program cleanly finishes.

def handle_disconnect(*args):
    print("handle_disconnect", *args, file=sys.stderr)
    global record
    record = False # Cancel recording. On next sample program cleanly finishes.
    
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGPIPE, handle_disconnect) # Check if analysis program crashes.

    
def isr_clear():
    if __debug__:
        print('isr_clr', file=sys.stderr)
    GPIO.remove_event_detect(pin_alert)
    
def isr_prime():
    if __debug__:
        print('isr_set', file=sys.stderr)
    GPIO.add_event_detect(pin_alert, GPIO.FALLING, callback=isr_handle, bouncetime=bounce)
    
def isr_handle(channel):
    # Read whenever conversion is done.
    ads1115_read()

#adc_confg = { conversion: [0xB1, 0x83], scale: (2*6.144 / 2**16) }
#adc_confg = { conversion: [0xB3 0x83], scale: (2*4.096 / 2**16) }
#adc_confg = { conversion: [0xB5 0x83], scale: (2*2.048 / 2**16) }
#adc_confg = { conversion: [0xB7, 0x83], scale: (2*1.024 / 2**16) }

class adc_config:
    # Needs 5 + 1.65 rail since bbb is at 5
    #  ±1.024 V, A2 rel A3, 128sps
    #conversion = [0b00110110, 0b10000000]
    #rate = 128
    #scale = (2*1.024 / 2**16)
    
    #  ±1.024 V, A2 rel A3, 250sps
    conversion = [0b00110110, 0b10100000]
    rate = 242
    scale = (1.024 / 2**15)

def ads1115_continuous():
    if __debug__:
        print("ads1115_continuous", file=sys.stderr)
    # Enable Interrupt first.
    isr_prime()
    
    # Enable Ready interrupt by writing MSB 1 to high threshold register and
    # writing 0 to msb1 of low threashold register.
    bus.write_i2c_block_data(0x48, 0x03, [0b10000000, 0])
    bus.write_i2c_block_data(0x48, 0x02, [0, 0])
    
    # Start Conversion of A2C
    bus.write_i2c_block_data(0x48, 0x01, adc_config.conversion)
    
    #ads1115_show_config()
    
def ads1115_show_config():
    cfg = int.from_bytes(bus.read_i2c_block_data(0x48, 0x01, 2), byteorder='big', signed=False)
    if __debug__:
        print(f"cfg: {cfg:#018b}", file=sys.stderr)
    
    ltr = int.from_bytes(bus.read_i2c_block_data(0x48, 0x02, 2), byteorder='big', signed=False)
    if __debug__:
        print(f"ltr: {ltr:#018b}", file=sys.stderr)
    htr = int.from_bytes(bus.read_i2c_block_data(0x48, 0x03, 2), byteorder='big', signed=False)
    if __debug__:
        print(f"htr: {htr:#018b}", file=sys.stderr)
    

def ads1115_poweroff():
    if __debug__:
        print("ads1115_poweroff", file=sys.stderr)
    # Disable Continuous mode by writing bit: 8 high
    bytes = adc_config.conversion.copy()
    bytes[0] |= 0x1
    bus.write_i2c_block_data(0x48, 0x01, bytes)
    #ads1115_show_config()

def ads1115_read(): # ads1115
    # Read result of conversion.
    bytes = bus.read_i2c_block_data(0x48, 0x00, 2)
    raw = int.from_bytes(bytes, byteorder='big', signed=True) # Read as int16 two's compliment
    val = raw * adc_config.scale
    
    global queue
    queue.put((raw, val, bytes))


record = True
queue = Queue(128)

# Look for next session directory in data location.
def next_session_dir():
    max_id = 0 # Next session id is this + 1.
    if os.path.isdir("../data"):
        with os.scandir("../data/") as dirs:
            for entry in dirs:
                if entry.is_dir() and entry.name.startswith("session_"):
                    id = int(entry.name.split("_")[1])
                    if id > max_id:
                        max_id = id
    return "../data/session_{:04d}".format(max_id+1)

def date_session_dir(): 
    # Build directory name with ISO 8601 format. Note: No RTC on Pocket Beagle.
    start = datetime.now()
    return "../data/{}".format(start.strftime("%Y-%m-%dT%H%M%s"))

def accumulate_start(opts = None):
    rate = adc_config.rate
    epoch = np.zeros(opts.epoch_seconds * rate, dtype=np.int16)
    epoch_i = 0
    epoch_num = 0
    path = next_session_dir()
    rate = adc_config.rate
    pipe_analysis = sys.stdout
    
    if opts.wav or opts.csv:
        os.makedirs(path, exist_ok=True)
        # Make Symlink for access to latest data. Replace existing link.
        try:
            os.unlink("../current_data")
        except FileNotFoundError:
            pass
        os.symlink(os.path.abspath(path), "../current_data", True, )
        print("Recording to '{}'".format(path), file=sys.stderr)
    
    # Enable ADC sampling in continuous mode.
    ads1115_continuous()
    start = time.time()
    
    while record:
        # Wait on samples to arrive in queue. Blocks.
        raw, val, bytes = queue.get(timeout=10)
        if raw is None:
            break
        
        # Store sample into epoch array. When full save and send to analysis.
        epoch[epoch_i] = raw
        epoch_i += 1

        if opts.show_samples and (epoch_i % (rate / 2)) == 0: # Print 2 times per second
            print("\r@ {:4} Hz : {:4d} s  {:3d} samples  {:+1.3f} V ({:+8d})".format(rate, epoch_i // rate, epoch_i, val, raw), end="", flush=True, file=sys.stderr)
        
        if epoch_i == len(epoch):
            epoch_num += 1
            epoch_i = 0
            finished = time.time()
            elapsed = finished - start
            start = finished
            print("\nEpoch {:5d} Done in {:2.3f} seconds.".format(epoch_num, elapsed), file=sys.stderr)
            
            if opts.wav:
                filename = "{}/epoch{:02}.wav".format(path, epoch_num)
                write_wavfile(filename, rate, epoch.astype(np.int16))
                print("FILE {}".format(filename), flush=True, file=pipe_analysis)
        
        if opts.num_epochs > 0 and opts.num_epochs <= epoch_num:
            # Finish recording.
            break
    
    print("DONE", flush=True, file=pipe_analysis)
        
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
    parser.add_option('-n', '--num_epochs', dest='num_epochs', action='store', type='int', default=0,
        help="Number of epochs to record.")
    parser.add_option('-v', '--view_samples', dest='show_samples', action='store_true', default=False,
        help="Display samples at a reduced rate.")
    (opts, args) = parser.parse_args()
    accumulate_start(opts=opts)
