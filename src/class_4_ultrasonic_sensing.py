import RPi.GPIO as GPIO
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

class Sensor:
  def __init__(self, trig, echo, num):
    self.trig = trig
    self.echo = echo
    self.num = num
    
  def distance(self):
    print("Distance Measurement in Progress")
    GPIO.setup(self.trig, GPIO.OUT)
    GPIO.setup(self.echo, GPIO.IN)
    GPIO.output(self.trig, False)
    
    print(f"Waiting For Sensor {self.num} To Send Signal")
    time.sleep(2)
    GPIO.output(self.trig, True)
    time.sleep(0.00001)
    GPIO.output(self.trig, False)
    
    print("Reading Sensor")
    while GPIO.input(self.echo)==0:
      pulse_start = time.time()
    while GPIO.input(self.echo)==1:
      pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print(f"Distance Sensor {num}: {distance}","cm")
 
try:
    i=1     # if f_string works, use f_string instead of if for simplicity
    while 1:
      i=i%4
      if i == 1:
        sensor = Sensor(TRIG1, ECHO1, i)
        distance = sensor.distance()
        i+=1
      if i == 2:
        sensor = Sensor(TRIG2, ECHO2, i)
        distance = sensor.distance()
        i+=1
      if i == 3:
        sensor = Sensor(TRIG3, ECHO3, i)
        distance = sensor.distance()
        i+=1
      if i == 0:
        sensor = Sensor(TRIG4, ECHO4, i)
        distance = sensor.distance()
        i+=1

except KeyboardInterrupt:   # if there is a keyboard interrupt such as ctrl+c, stop the code with cleaning up the gpio
    print ('KeyboardInterrupt exception is caught')
    GPIO.cleanup()
