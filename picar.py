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
    client_socket.send("\nCamera good")
    
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
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle < 100 and drive == "manual":
            frontRight.dutyCycle += 10
            frontLeft.dutyCycle += 10
            rearRight.dutyCycle += 10
            rearLeft.dutyCycle += 10
        else:
            continue
        
        if frontRight.dutyCycle >= 0 and frontLeft.dutyCycle >= 0:
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

        if frontRight.dutyCycle < 0 and frontLeft.dutyCycle < 0:
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
        
        if frontRight.dutyCycle >= 0 and frontLeft.dutyCycle >= 0:
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

        if frontRight.dutyCycle < 0 and frontLeft.dutyCycle < 0:
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
        #cv2.waitKey(16)
        #dimensions = frame.shape
        height = frame.shape[0]
        width = frame.shape[1]
        #channels = frame.shape[2]
        first_black_pixel = -1
        last_black_pixel = -1
        #middleBlue = frame.item(int(width / 2), int(height / 2), 0)
        #middleGreen = frame.item(int(width / 2), int(height / 2), 1)
        #middleRed = frame.item(int(width / 2), int(height / 2), 2)
        #print(middleBlue)
        #print(middleGreen)
        #print(middleRed)
        frontRight.dutyCycle = 20
        rearRight.dutyCycle = 20
        frontLeft.dutyCycle = 20
        rearLeft.dutyCycle = 20
        frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
        rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
        frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
        rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
        for x in range(width - 1):
            if frame.item(int(height / 2), x, 0) < 15 and frame.item(int(height / 2), x, 1) < 15 and frame.item(int(height / 2), x, 2) < 15:
                first_black_pixel = x
        for x in range(width - 1):
            if frame.item(int(height / 2), width - 1 - x, 0) < 15 and frame.item(int(height / 2), width - 1 - x, 1) < 15 and frame.item(int(height / 2), width - 1 - x, 2) < 15:
                last_black_pixel = width - 1 - x
        line_middle = (first_black_pixel + last_black_pixel) / 2
        difference = int(width / 2) - line_middle
        turnPWM = 0
        print("width: " + str(width))
        print("line_middle: " + str(line_middle))
        print("difference: " + str(difference))
        if line_middle == -1 or first_black_pixel > last_black_pixel:
            print("No line found")
        elif difference >= 0:
            """We have to turn left"""
            turnPWM = int(line_middle / (width / 2)) * 10
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle + turnPWM)
            rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle + turnPWM)
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle)
            rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle)
            print("Front right:" + str(frontRight.dutyCycle) + str(turnPWM))
            print("Front left:" + str(frontLeft.dutyCycle))
        elif difference < 0:
            """We have to turn right"""
            turnPWM = int(abs(difference) / (width / 2)) * 10
            frontRightForwPWM.ChangeDutyCycle(frontRight.dutyCycle)
            rearRightForwPWM.ChangeDutyCycle(rearRight.dutyCycle)
            frontLeftForwPWM.ChangeDutyCycle(frontLeft.dutyCycle + turnPWM)
            rearLeftForwPWM.ChangeDutyCycle(rearLeft.dutyCycle + turnPWM)
            print("Front right:" + str(frontRight.dutyCycle))
            print("Front left:" + str(frontLeft.dutyCycle + turnPWM))
        time.sleep(0.2)     

client_socket.close()
server_socket.close()