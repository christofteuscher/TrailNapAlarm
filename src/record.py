
import Adafruit_BBIO.ADC as ADC
import time
from datetime import datetime

from optparse import OptionParser
import numpy as np
from scipy.io.wavfile import write as write_wavfile

parser = OptionParser(description='Record sampled EEG data.')
parser.add_option('-s', '--save', action='store_true',
    help="Save read values as CSV")
parser.add_option('--rate', dest='rate', type=int, default=200,
    help="Samples per second to record.")
parser.add_option('--wav', dest='wav', action='store_true', default=False,
    help="Save epoch as wav file format.")
parser.add_option('--pin', default='AIN1', choices=["AIN{}".format(x) for x in range(0,7)],
    help="Pin to sample.")
(opts, args) = parser.parse_args()

if __debug__:
    print(opts)

pin = opts.pin
pin_range = 3.3 if pin in {"AIN5", "AIN6"} else 1.8
rate = opts.rate
epoch_s = 30
samples_count = 0
epoch = 0

samples = []

epoch_samples = rate * epoch_s
samples = np.zeros(epoch_samples)

if __debug__:
    print(pin, pin_range)


ADC.setup()


file = None
if opts.save:
    file = open(datetime.now().strftime("%Y-%m-%d_%H:%M:%S.csv"), "w")
    print("Recording to ", file.name)
    

while True:
    value = ADC.read(pin)
    
    voltage = pin_range * value
    samples_count += 1
    epoch_elapsed = samples_count % epoch_samples
    epoch_seconds = int(epoch_elapsed / rate)
    epoch_percent = 100 * epoch_elapsed / epoch_samples
    
    samples[epoch_elapsed] = value
    
    print("{:s}: {:0.2f} {:0.2f}V   {:02}s {:2}%".format(pin, value, voltage, epoch_seconds, int(epoch_percent)), end="\r")
    if epoch_elapsed == 0:
        
        if opts.wav:
            write_wavfile("epoch{:02}.wav".format(epoch), rate, samples.astype(np.int16))
            
        epoch += 1
        print("\033[K", "Epoch {} Ended".format(epoch))
    
    if file:
        print("{:0.2f}".format(value), file=file)
    
    time.sleep(1/rate) # TODO: Use more accurate sampling scheme. Timer or signal package.