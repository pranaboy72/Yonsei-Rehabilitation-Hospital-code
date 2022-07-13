import RPI.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG1=20
ECHO1=21
TRIG2=23
ECHO2=24
TRIG3=19
ECHO3=13
TRIG4=5
ECHO4=6

print("Distance Measurement in Progress")
GPIO.setup(TRIG1.GPIO.OUT)
GPIO.setup(ECHO1.GPIO.IN)
GPIO.setup(TRIG2.GPIO.OUT)
GPIO.setup(ECHO2.GPIO.IN)
GPIO.setup(TRIG3.GPIO.OUT)
GPIO.setup(ECHO3.GPIO.IN)
GPIO.setup(TRIG4.GPIO.OUT)
GPIO.setup(ECHO4.GPIO.IN)
GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)
GPIO.output(TRIG4, False)

for i in range(4):
  print(f"Waiting For Sensor {i+1} To Send Signal")
  time.sleep(2)
  GPIO.output(f"TRIG{i+1}", True) # if f_string doesn't work, type 1~4 Trig and Echo manually
  time.sleep(0.00001)
  GPIO.output(f"TRIG{i+1}", False)
  print("Reading Sensor")
  while GPIO.input(f"ECHO{i+1}")==0:
    pulse_start = time.time()
  while GPIO.input(f"ECHO{i+1}")==1:
    pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  print(f"Distance Sensor {i+1}: {distance}","cm")

GPIO.cleanup()    #GPIO clean up: all designated GPIO numbers are cleaned up. Use this before you end up the code
