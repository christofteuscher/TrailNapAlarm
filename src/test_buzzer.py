
import Adafruit_BBIO.PWM as PWM 
import time
import signal, os

# https://adafruit-bbio.readthedocs.io/en/latest/PWM.html
# https://pages.mtu.edu/~suits/notefreqs.html

pin_buzzer = "P2_1" # "EHRPWM1A"

class TestBuzzer():
    def __init__(self):
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
    def cleanup(self, *args):
        print("cleanup", *args)
        PWM.start(pin_buzzer, 0)
        exit(0)
    def loop(self):
        PWM.start(pin_buzzer, 0)
        time.sleep(1)
        
        PWM.start(pin_buzzer, 50, 261.63)
        time.sleep(1)
        
        PWM.start(pin_buzzer, 0)
        time.sleep(1)
        
        PWM.start(pin_buzzer, 50, 440)
        time.sleep(1)
        
        self.cleanup()

if __name__ == '__main__':
    TestBuzzer().loop()
