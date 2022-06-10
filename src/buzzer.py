
import Adafruit_BBIO.PWM as PWM 
import time
import signal, os
from queue import Queue

# https://adafruit-bbio.readthedocs.io/en/latest/PWM.html
# https://pages.mtu.edu/~suits/notefreqs.html

class Note():
    C = [ 16.35, 32.70,  65.41, 130.81, 261.63, 523.25, 1046.50, 2093.00, 4186.01]
    Db= [ 17.32, 34.65,  69.30, 138.59, 277.18, 554.37, 1108.73, 2217.46, 4434.92]
    D = [ 18.35, 36.71,  73.42, 146.83, 293.66, 587.33, 1174.66, 2349.32, 4698.63]
    Eb= [ 19.45, 38.89,  77.78, 155.56, 311.13, 622.25, 1244.51, 2489.02, 4978.03]
    E = [ 20.60, 41.20,  82.41, 164.81, 329.63, 659.25, 1318.51, 2637.02, 5274.04]
    F = [ 21.83, 43.65,  87.31, 174.61, 349.23, 698.46, 1396.91, 2793.83, 5587.65]
    Gb= [ 23.12, 46.25,  92.50, 185.00, 369.99, 739.99, 1479.98, 2959.96, 5919.91]
    G = [ 24.50, 49.00,  98.00, 196.00, 392.00, 783.99, 1567.98, 3135.96, 6271.93]
    Ab= [ 25.96, 51.91, 103.83, 207.65, 415.30, 830.61, 1661.22, 3322.44, 6644.88]
    A = [ 27.50, 55.00, 110.00, 220.00, 440.00, 880.00, 1760.00, 3520.00, 7040.00]
    Bb= [ 29.14, 58.27, 116.54, 233.08, 466.16, 932.33, 1864.66, 3729.31, 7458.62]
    B = [ 30.87, 61.74, 123.47, 246.94, 493.88, 987.77, 1975.53, 3951.07, 7902.13]
    

class Buzzer():
    #pin_buzzer = "P2_1" # "EHRPWM1A" Breadboard Pin
    pin_buzzer = "P1_36" # "EHRPWM0A" Milled-board Pin

    def __init__(self):
        signal.signal(signal.SIGINT, self.cleanup) # Cleanup when closed.
        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGALRM, self.tick)   # Trigger timer, alarm

        self.queue = Queue(128)
        
    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0, 0) # Turn off Timer.
        PWM.stop(self.pin_buzzer)
        while not self.queue.empty():
            self.queue.get_nowait()

    def cleanup(self, *args):
        print("cleanup", file=sys.stderr)
        self.stop()
        PWM.cleanup()
        exit(0)
        
    def tick(self, *args):
        print("tick", file=sys.stderr)
        if self.queue.empty():
            self.stop()
        else:
            duty, hz = self.queue.get()
            PWM.start(self.pin_buzzer, duty, hz)
    
    def ready(self):
        self.queue.put((50, 261.63))
        self.queue.put(( 0,   100))
        self.queue.put((50, 440))
        signal.setitimer(signal.ITIMER_REAL, 0.02, 0.2) # Turn on Timer.

    def test(self):
        for hz in [Note.C[0], Note.C[1], Note.C[2], Note.C[3], Note.C[4], Note.C[5], Note.C[6], Note.C[7]]:
            self.queue.put((50, hz))
            self.queue.put(( 0, hz))
        signal.setitimer(signal.ITIMER_REAL, 0.02, 0.5) # Turn on Timer.


    def wake(self):
        for i in range(4):
            for hz in [Note.C[4], Note.Db[4]]:
                self.queue.put((50, hz))
                self.queue.put(( 0, hz))
        for i in range(10):
            for hz in [Note.C[5], Note.Db[5]]:
                self.queue.put((50, hz))
                self.queue.put(( 0, hz))
        signal.setitimer(signal.ITIMER_REAL, 0.02, 0.2) # Turn on Timer.
    

if __name__ == '__main__':
    import sys, os

    os.environ["PYTHONUNBUFFERED"] = "1"
    
    buzzer = Buzzer()
    for line in sys.stdin:
        cmd = line.strip().upper()
        print("Command: \"{}\"".format(cmd), file=sys.stderr)
        if cmd == "":
            pass
        elif cmd == "Q" or cmd == "DONE" or cmd == "QUIT":
            buzzer.cleanup()
        elif cmd == "S" or cmd == "STOP":
            buzzer.stop()
        elif cmd =="T" or cmd == "TEST":
            buzzer.test()
        elif cmd =="R" or cmd == "READY":
            buzzer.ready()
        elif cmd =="W" or cmd == "WAKE" or cmd == "WAKEUP":
            buzzer.wake()
    
