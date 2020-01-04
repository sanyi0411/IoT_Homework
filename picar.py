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
frontRight = Wheel(36, 32, 0)
frontLeft = Wheel(40, 38, 0)
rearRight = Wheel(35, 37, 0)
rearLeft = Wheel(31, 33, 0)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(frontRight.forwardPin, GPIO.OUT)
GPIO.setup(frontRight.backwardPin, GPIO.OUT)
GPIO.setup(frontLeft.forwardPin, GPIO.OUT)
GPIO.setup(frontLeft.backwardPin, GPIO.OUT)
GPIO.setup(rearRight.forwardPin, GPIO.OUT)
GPIO.setup(rearRight.backwardPin, GPIO.OUT)
GPIO.setup(rearLeft.forwardPin, GPIO.OUT)
GPIO.setup(rearLeft.backwardPin, GPIO.OUT)

frontRightForwPWM = GPIO.PWM(frontRight.forwardPin, 50)
frontRightBackPWM = GPIO.PWM(frontRight.backwardPin, 50)
frontLeftForwPWM = GPIO.PWM(frontLeft.forwardPin, 50)
frontLeftBackPWM = GPIO.PWM(frontLeft.backwardPin, 50)
rearRightForwPWM = GPIO.PWM(rearRight.forwardPin, 50)
rearRightBackPWM = GPIO.PWM(rearRight.backwardPin, 50)
rearLeftForwPWM = GPIO.PWM(rearLeft.forwardPin, 50)
rearLeftBackPWM = GPIO.PWM(rearLeft.backwardPin, 50)

frontRightForwPWM.start(0)
frontRightBackPWM.start(0)
frontLeftForwPWM.start(0)
frontLeftBackPWM.start(0)
rearRightForwPWM.start(0)
rearRightBackPWM.start(0)
rearLeftForwPWM.start(0)
rearLeftBackPWM.start(0)

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
        rearRight.dutyCycle = 0
        rearLeft.dutyCycle = 0
        frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
        frontRightBackPWM.ChangeDutyCycle(frontRight.dutyCycle)
        frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
        frontLeftBackPWM.ChangeDutyCycle(frontLeft.dutyCycle)
        rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
        rearRightBackPWM.ChangeDutyCycle(rearRight.dutyCycle)
        rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
        rearLeftBackPWM.ChangeDutyCycle(rearLeft.dutyCycle)
        if drive == "autonomous":
            cv2.destroyAllWindows()
        drive = "manual"
    
    elif (data == b'w'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle < 100  drive == "manual":
            frontRight.dutyCycle += 10
            frontLeft.dutyCycle += 10
            rearRight.dutyCycle += 10
            rearLeft.dutyCycle += 10
        else:
            continue
        
        if frontRight.dutyCycle >= 0 and frontLeft.dutyCycle >= 0
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
            frontRightBackPWM.ChangeDutyCycle(0)
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            frontLeftBackPWM.ChangeDutyCycle(0)
            rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
            rearRightBackPWM.ChangeDutyCycle(0)
            rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            rearLeftBackPWM.ChangeDutyCycle(0)
            print("Right side:" + str(frontRight.dutyCycle))
            print("Left side:" + str(frontLeft.dutyCycle))

        if frontRight.dutyCycle < 0 and frontLeft.dutyCycle < 0
            frontRightForwPWM.ChangeDutyCycle(0)
            frontRightBackPWM.ChangeDutyCycle(frontRight.dutyCycle)
            frontLeftForwPWM.ChangeDutyCycle(0)
            frontLeftBackPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            rearRightForwPWM.ChangeDutyCycle(0)
            rearRightBackPWM.ChangeDutyCycle(rearRight.dutyCycle)
            rearLeftForwPWM.ChangeDutyCycle(0)
            rearLeftBackPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            print("Right side:" + str(frontRight.dutyCycle))
            print("Left side:" + str(frontLeft.dutyCycle))

    elif (data == b's'):
        if frontRight.dutyCycle > -100 and frontLeft.dutyCycle > -100 and drive == "manual":
            frontRight.dutyCycle -= 10
            frontLeft.dutyCycle -= 10
            rearRight.dutyCycle -= 10
            rearLeft.dutyCycle -= 10
         else:
            continue
        
        if frontRight.dutyCycle >= 0 and frontLeft.dutyCycle >= 0
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
            frontRightBackPWM.ChangeDutyCycle(0)
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            frontLeftBackPWM.ChangeDutyCycle(0)
            rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
            rearRightBackPWM.ChangeDutyCycle(0)
            rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            rearLeftBackPWM.ChangeDutyCycle(0)
            print("Right side:" + str(frontRight.dutyCycle))
            print("Left side:" + str(frontLeft.dutyCycle))

        if frontRight.dutyCycle < 0 and frontLeft.dutyCycle < 0
            frontRightForwPWM.ChangeDutyCycle(0)
            frontRightBackPWM.ChangeDutyCycle(frontRight.dutyCycle)
            frontLeftForwPWM.ChangeDutyCycle(0)
            frontLeftBackPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            rearRightForwPWM.ChangeDutyCycle(0)
            rearRightBackPWM.ChangeDutyCycle(rearRight.dutyCycle)
            rearLeftForwPWM.ChangeDutyCycle(0)
            rearLeftBackPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            print("Right side:" + str(frontRight.dutyCycle))
            print("Left side:" + str(frontLeft.dutyCycle))
        
    elif (data == b'd'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle < 100 and drive == "manual":
            frontRight.dutyCycle -= 5
            rearRight.dutyCycle -= 5
            frontLeft.dutyCycle += 5
            rearLeft.dutyCycle += 5
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
            rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            print("Right side:" + str(frontRight.dutyCycle))
            print("Left side:" + str(frontLeft.dutyCycle))

    elif (data == b'a'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle > 0 and drive == "manual":
            frontRight.dutyCycle += 5
            rearRight.dutyCycle += 5
            frontLeft.dutyCycle -= 5
            rearLeft.dutyCycle -= 5
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
            rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            print("Right side:" + str(frontRight.dutyCycle))
            print("Left side:" + str(frontLeft.dutyCycle))
            
    elif (data == b'autodrive' or drive == "autonomous"):
        drive = "autonomous"
        ret, frame = cap.read()
        #cv2.imshow("webcam", frame)
        #cv2.waitKey(1)
        #dimensions = frame.shape
        height = frame.shape[0]
        width = frame.shape[1]
        channels = frame.shape[2]
        first_black_pixel = -1
        last_black_pixel = -1
        middlePixel = frame.item(int(width / 2), int(height / 2))
        print(middlePixel)
        #for x in range(width):
            #if frame.item(x, height / 2) == [0, 0]:
                #first_black_pixel = x
        #for x in range(width):
            #if frame.item(width - x, height / 2) == [0, 0]:
                #last_black_pixel = x
        line_middle = (first_black_pixel + last_black_pixel) / 2
        if first_black_pixel == -1 or last_black_pixel == -1 or first_black_pixel > last_black_pixel:
            #print("No line found")
        elif line_middle < (width / 2):
            frontLeft.dutyCycle += 1
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))
        elif line_middle > (width / 2):
            frontRight.dutyCycle += 1
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle))
     
     
client_socket.close()
server_socket.close()
