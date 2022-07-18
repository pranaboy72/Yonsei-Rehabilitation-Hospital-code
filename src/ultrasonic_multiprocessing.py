import RPi.GPIO as GPIO
import time
from multiprocessing import Process 

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
TOUCH = 16

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
GPIO.setup(TOUCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)

print(f"Waiting For Sensor To Send Signal")
time.sleep(2)
 

def trans_buzz(buz, per):
  pwm = GPIO.PWM(buz, 262)
  pwm.start(50.0)
  time.sleep(per)  
  pwm.stop()

def buzzer_distance(buz, dis):
  if 10 <= dis < 20:
    trans_buzz(buz, 1)
  elif 5 <= dis < 10:
    trans_buzz(buz, 1.5)
  elif dis < 5:
    trans_buzz(buz, 2)
  
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
    return (100)
  
  distance = (pulse_end - pulse_start) * 34300 / 2
  return (distance)

def ultrasonic1():
   distance = get_distance(TRIG1, ECHO1)
   print(f"Distance1 : {distance} cm")
   buzzer_distance(BUZZ1, distance)
   time.sleep(0.4)
      
def ultrasonic2():
   distance = get_distance(TRIG2, ECHO2)
   print(f"Distance2 : {distance} cm")
   buzzer_distance(BUZZ2, distance)
   time.sleep(0.4)
      
def ultrasonic3():
   distance = get_distance(TRIG3, ECHO3)
   print(f"Distance3 : {distance} cm")
   buzzer_distance(BUZZ3, distance)
   time.sleep(0.4)

def main(power):
  if GPIO.input(TOUCH) == True and power == 0:
   power = 1
   p_1 = Process(target=ultrasonic1)
   p_2 = Process(target=ultrasonic2)
   p_3 = Process(target=ultrasonic3)

   p_1.start()
   p_2.start()
   p_3.start()
   
   p_1.join()
   P_2.join()
   p_3.join()

   time.sleep(0.5)

  elif GPIO.input(TOUCH) == True and power == 1:
   power = 0
   p_1.join()
   P_2.join()
   p_3.join()
   
   time.sleep(0.5)
   
  elif GPIO.input(TOUCH) == False and power == 1:
   p_1.start()
   p_2.start()
   p_3.start()
   
   time.sleep(0.5)   
 
try:
 if __name__=='__main__':
  power =0
  while True:
   main() 

except KeyboardInterrupt:
  print ("KeyboardInterrupt exception is caught")
  p_1.join()
  P_2.join()
  p_3.join()
  GPIO.cleanup()    #GPIO clean up: all designated GPIO numbers are cleaned up. Use this before you end up the code
