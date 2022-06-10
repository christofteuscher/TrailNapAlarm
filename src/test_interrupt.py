
import Adafruit_BBIO.GPIO as GPIO
import time
import signal, os

pin = "P2_2"
bounce = 40
times = 0

class TestInterrupt():
    def __init__(self):
        self.times = 0
        self.isr_set = 0
        self.isr_processing = 0
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        self.enable()
        
    def cleanup(self, *args):
        self.clear()
        print("\ncleanup")
        print(f"Interrupts: {self.time}")
        exit(0)
        
    def isr(self, channel):
        self.isr_processing += 1
        self.times += 1
        print("isr", self.times, channel)
        
        self.clear()
        time.sleep(1)
        self.enable()
        self.isr_processing -= 1
        
    def clear(self):
        GPIO.remove_event_detect(pin)
        self.isr_set = 0
        
    def enable(self):
        self.isr_set = 1
        GPIO.remove_event_detect(pin)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.isr, bouncetime=bounce)
        
if __name__ == '__main__':
    isr = TestInterrupt()
    isr.enable()
    
    print(f"Read on pin '{pin}' for interrupts.")
    print("Pin is pulled_up. Connect to ground in order to trigger.")
    
    i = 0
    while True:
        time.sleep(1);
        print(f"Wait {i:4}s set: {isr.isr_set}  depth: {isr.isr_processing}")