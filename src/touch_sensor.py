import os
import time
import random

import RPi.GPIO as GPIO

TOUCH = (gpio num)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
  if GPIO.input(TOUCH) == True:
    print("Touch Detected")
    time.sleep(0.5)
    
  if GPIO.input(TOUCH) == True:
    print("No Touch Detected")
    time.sleep(0.5)
