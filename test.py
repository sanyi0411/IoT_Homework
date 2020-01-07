import RPi.GPIO as GPIO
import time
import bluetooth
import cv2
import enum
import numpy as np

trig = 11
echo = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.output(trig, 0)

try:
	while True:
		GPIO.output(trig, 1)
		time.sleep(0.00001)
		GPIO.output(trig, 0)

		while GPIO.input(echo) == 0:
			pulse_start = time.time()

		while GPIO.input(echo) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance + 1.15, 2)

		print("Distance: " + str(distance) + "cm")
		time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()