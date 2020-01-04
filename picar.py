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
client_socket.setblocking(0)
print ("Accepted connection from ",address)
client_socket.send("Connected")

#Setting up GPIO pins
frontRight = Wheel(16, 18, 0)
frontLeft = Wheel(13, 15, 0)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
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
else:
    client_socket.send("Camera good")
    
direction = Direction.forward
drive = "manual"
data = "a"
while True:
    try:
        data = client_socket.recv(1024)
        print (data)
    except:
        pass
    
    if (data == b'exit'):
        GPIO.cleanup()
        cv2.destroyAllWindows()
        break
    
    elif (data == b'stop'):
        frontRight.dutyCycle = 0
        frontLeft.dutyCycle = 0
        p.ChangeDutyCycle(frontRight.dutyCycle)
        r.ChangeDutyCycle(frontLeft.dutyCycle)
        cv2.destroyAllWindows()
        drive = "manual"
    
    elif (data == b'w'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle < 100 and drive == driveMode.manual:
            frontRight.dutyCycle += 10
            frontLeft.dutyCycle += 10
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))

    elif (data == b's'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle > 0 and drive == driveMode.manual:
            frontRight.dutyCycle -= 10
            frontLeft.dutyCycle -= 10
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))
        
    elif (data == b'd'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle < 100 and drive == driveMode.manual:
            frontRight.dutyCycle -= 5
            frontLeft.dutyCycle += 5
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))

    elif (data == b'a'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle > 0 and drive == driveMode.manual:
            frontRight.dutyCycle += 5
            frontLeft.dutyCycle -= 5
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))
            
    elif (data == b'autodrive' or drive == "autonomous"):
        drive = "autonomous"
        ret, frame = cap.read()
        cv2.imshow("webcam", frame)
        cv2.waitKey(1)
        dimensions = frame.shape
        height = frame.shape[0]
        width = frame.shape[1]
        channels = frame.shape[2]
        first_black_pixel = -1
        last_black_pixel = -1
        middleB = frame.item(int(width / 2), int(height / 2), 0)
        print(middleB)
        #for x in range(width):
            #if frame.item(x, height / 2) == [0, 0]:
                #first_black_pixel = x
        #for x in range(width):
            #if frame.item(width - x, height / 2) == [0, 0]:
                #last_black_pixel = x
        line_middle = (first_black_pixel + last_black_pixel) / 2
        if first_black_pixel == -1 or last_black_pixel == -1 or first_black_pixel > last_black_pixel:
            print("No line found")
        elif line_middle < (width / 2):
            frontLeft.dutyCycle += 1
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))
        elif line_middle > (width / 2):
            frontRight.dutyCycle += 1
            p.ChangeDutyCycle(frontRight.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))
     
     
client_socket.close()
server_socket.close()
