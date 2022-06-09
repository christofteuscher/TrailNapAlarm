#!/usr/bin/python3
#//////////////////////////////////////
# 	pollStart.py
# 	Wiring:
# 	Setup:	
# 	See:	
# ////////////////////////////////////////
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
import btnWake as wake
import collectData as data
import subprocess
import sys
import threading 

ADC.setup()

inputPin  = "AIN0";
outputPin = "P1_36";
PWM.start(outputPin, 0)

PWM.set_duty_cycle(outputPin, 50)
time.sleep(1)
PWM.set_duty_cycle(outputPin, 0)
time.sleep(2)
    
#print("Press button to start.")

while True:
    value = ADC.read(inputPin)
    if (round(value, 2) == 0.0):
        break
    time.sleep(.25)

t1 = threading.Thread(target=wake.LED,)
t2 = threading.Thread(target=data.scan, args=(100,5,"unread_Faz.wav"))

t1.start()
t2.start()
