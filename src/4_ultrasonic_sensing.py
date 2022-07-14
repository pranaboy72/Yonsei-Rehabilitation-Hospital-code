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
BUZZ1=5
BUZZ2=6
BUZZ3=26
#TRIG4=5
#ECHO4=6

print("Distance Measurement in Progress")
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG3,GPIO.OUT)
GPIO.setup(ECHO3,GPIO.IN)
GPIO.setup(BUZZ1, GPIO.OUT)
GPIO.setup(BUZZ2, GPIO.OUT)
GPIO.setup(BUZZ3, GPIO.OUT)
#GPIO.setup(TRIG4,GPIO.OUT)
#GPIO.setup(ECHO4,GPIO.IN)

GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)
#GPIO.output(TRIG4, False)

print(f"Waiting For Sensor To Send Signal")
time.sleep(2)
 

def trans_buzz(buz, per):
  pwm = GPIO.PWM(buz, 262)
  pwm.start(50.0)
  time.sleep(1.5)
  
  pwm.stop()
 
def buzzer(buz, per):
  GPIO.output(buz, GPIO.HIGH)
  print("beep")
  time.sleep(per)
  GPIO.output(buz, GPIO.LOW)
  print("stop beep")
  time.sleep(per)

def buzzer_distance(buz, dis):
  if dis<20:
    trans_buzz(buz, 1)
  elif dis <10:
    trans_buzz(buz, 0.5)
  elif dis < 5:
    transbuzz(buz, 0.1)
  
def get_distance(trig, echo):
  if GPIO.input(echo):
    return (100)
  
  distance = 0
  
  GPIO.output(trig, False)
  time.sleep(0.05)
  
  GPIO.output(trig, True)
  time.sleep(0.00001)
  GPIO.output(trig, False)
  pulse_start, pulse_end = time.time(), time.time()
  
  while not GPIO.input(echo):
    pulse_start = time.time()
    if pulse_start - pulse_end > 0.02:
      distance = 100
      break
  if distance == 100:
    return (distance)
  
  while GPIO.input(echo):
    pulse_end = time.time()
    if pulse_end - pulse_start > 0.02:
      distance = 100
      break
      
  if distance == 100:
    return(100)
  
  distance = (pulse_end - pulse_start) * 34300 / 2
  return (distance)

try:
  i=1
  while 1:
    i=i%3
      
    if i==1:
      distance = get_distance(TRIG1, ECHO1)
      print(f"Distance : {distance} cm")
      GPIO.output(BUZZ1, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(BUZZ1, GPIO.LOW)
      
      #buzzer_distance(BUZ1, distance)
      time.sleep(0.4)
      i+=1
      
    elif i==2:
      distance = get_distance(TRIG2, ECHO2)
      print(f"Distance : {distance} cm")
      buzzer_distance(BUZZ2, distance)
      time.sleep(0.4)
      i+=1
      
    elif i==0:
      distance = get_distance(TRIG3, ECHO3)
      print(f"Distance : {distance} cm")
      buzzer_distance(BUZZ3, distance)
      time.sleep(0.4)
      i+=1
      
    '''elif i==0:
      distance = get_distance(TRIG4, ECHO4)
      print(f"Distance : {distance} cm")
      time.sleep(0.4)
      i+=1'''
      
      
except KeyboardInterrupt:
  print ("KeyboardInterrupt exception is caught")
  GPIO.cleanup()    #GPIO clean up: all designated GPIO numbers are cleaned up. Use this before you end up the code
