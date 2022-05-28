#!/usr/bin/python3
#//////////////////////////////////////
# 	btnWake.py
# 	Wiring:	
# 	Setup:	
# 	See:	
# ////////////////////////////////////////
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time

def LED():
    ADC.setup()
        
    #print("wake starting")
    #time.sleep(3)
        
    inputPin  = "AIN0";
    readingPin = "AIN1";
    outputPin = "P1_36";
    PWM.start(outputPin, 0)
        
    while True:
        value = ADC.read(inputPin)
        if (round(value, 2) == 0.0):
            PWM.set_duty_cycle(outputPin, 50)
            break
        else:
            PWM.set_duty_cycle(outputPin, 0)
