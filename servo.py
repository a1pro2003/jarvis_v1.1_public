import RPi.GPIO as GPIO
from time import sleep
from speak import *

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
servo1 = GPIO.PWM(7,50)
servo1.start(0)

def open_mask():
    speak('Opening mask')
    angle = 100
    servo1.ChangeDutyCycle(2+(angle/18))
    sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    
def close_mask():
    speak('Closing mask')
    angle = 140
    servo1.ChangeDutyCycle(2+(angle/18))
    sleep(0.5)
    servo1.ChangeDutyCycle(0)