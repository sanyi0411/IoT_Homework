import RPi.GPIO as GPIO
import time
import bluetooth
import cv2
import enum
import numpy as np

front_right_forw = 36
front_right_back = 32
front_left_back = 38
front_left_forw = 40

rear_right_forw = 35
rear_right_back = 37
rear_left_forw = 31
rear_left_back = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(rear_left_back, GPIO.OUT)
p = GPIO.PWM(rear_left_back, 50)
p.start(0)

p.ChangeDutyCycle(20)
time.sleep(1)
p.ChangeDutyCycle(40)
time.sleep(1)
p.ChangeDutyCycle(60)
time.sleep(1)
GPIO.cleanup()