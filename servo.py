import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)
servo1.start(0)

def open_mask():
    angle = 100
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    
def close_mask():
    angle = 140
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)