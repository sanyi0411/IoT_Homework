import RPi.GPIO as GPIO
import time
import bluetooth
import cv2
import enum
import numpy as np
from wheels import Wheel

class Direction(enum.Enum):
    forward = 1
    backward = 2
    
class driveMode(enum.Enum):
    manual = 1
    autonomous = 2

#Establishing bluetooth connection
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
client_socket,address = server_socket.accept()
print ("Accepted connection from ",address)

#Setting up GPIO pins
frontRight = Wheel(16, 18, 0)
frontLeft = Wheel(13, 15, 0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(frontRight.forwardPin, GPIO.OUT)
GPIO.setup(frontRight.backwardPin, GPIO.OUT)
GPIO.setup(frontLeft.forwardPin, GPIO.OUT)
GPIO.setup(frontLeft.backwardPin, GPIO.OUT)

p = GPIO.PWM(frontRight.forwardPin, 50)
q = GPIO.PWM(frontRight.backwardPin, 50)
r = GPIO.PWM(frontLeft.forwardPin, 50)
s = GPIO.PWM(frontLeft.backwardPin, 50)
p.start(0)
q.start(0)
r.start(0)
s.start(0)

#Opening camera
cap = cv2.VideoCapture(0)
    
if cap.isOpened() == False:
    print("Cannot open camera")
    return
    
direction = Direction.forward
drive = driveMode.manual

while True:
    data = client_socket.recv(1024)
    print (data)
    if (data == b'w'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle < 100 and drive = driveMode.manual:
            frontRight.dutyCycle += 10
            frontLeft.dutyCycle += 10
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)

    elif (data == b's'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle > 0 and drive = driveMode.manual:
            frontRight.dutyCycle -= 10
            frontLeft.dutyCycle -= 10
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)
        
    elif (data == b'd'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle < 100 and drive = driveMode.manual:
            frontRight.dutyCycle -= 5
            frontLeft.dutyCycle += 5
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)

    elif (data == b'a'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle > 0 and drive = driveMode.manual:
            frontRight.dutyCycle += 5
            frontLeft.dutyCycle -= 5
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)

    elif (data == b'autodrive' or drive == driveMode.autonomous):
        drive = driveMode.autonomous
        ret, frame = cap.read()
        cv2.imshow("webcam", frame)
        dimensions = frame.shape
        height = frame.shape[0]
        width = frame.shape[1]
        channels = frame.shape[2]
        first_black_pixel = -1
        last_black_pixel = -1
        for x in range(width):
            if frame.item(x, height / 2) == [0, 0]:
                first_black_pixel = x
        for x in range(width):
            if frame.item(width - x, height / 2) == [0, 0]:
                last_black_pixel = x
        if first_black_pixel == -1 or last_black_pixel == -1 or first_black_pixel > last_black_pixel:
            print("No line found")
            return
        

    elif (data == b'stop'):
        frontRight.dutyCycle = 0
        frontLeft.dutyCycle = 0
        p.ChangeDutyCycle(frontRight.dutyCycle)
        r.ChangeDutyCycle(frontLeft.dutyCycle)
        drive = driveMode.manual
        
    elif (data == b'exit'):
        GPIO.cleanup()
        cv2.destroyAllWindows()
        break
 
client_socket.close()
server_socket.close()
