import RPi.GPIO as GPIO
import time
import bluetooth
import cv2
import enum
from wheels import Wheel

class Direction(enum.Enum):
    forward = 1
    backward = 0

def forward():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(front_right_forward, GPIO.OUT)
    GPIO.setup(front_left_forward, GPIO.OUT)
    GPIO.output(front_right_forward, GPIO.HIGH)
    GPIO.output(front_left_forward, GPIO.HIGH)
    
def backward():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(front_right_backward, GPIO.OUT)
    GPIO.setup(front_left_backward, GPIO.OUT)
    GPIO.output(front_right_backward, GPIO.HIGH)
    GPIO.output(front_left_backward, GPIO.HIGH)
    
def camera():
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened() == False:
        print("Cannot open camera")
        return
    
    while(cv2.waitKey(16) != 27):
        ret, frame = cap.read()
        cv2.imshow("webcam", frame)
    
    cv2.destroyAllWindows()

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


direction = Direction.forward
while True:
    data = client_socket.recv(1024)
    print (data)
    if (data == b'w'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle < 100:
            frontRight.dutyCycle += 10
            frontLeft.dutyCycle += 10
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)

    elif (data == b's'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle > 0:
            frontRight.dutyCycle -= 10
            frontLeft.dutyCycle -= 10
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)
        
    elif (data == b'd'):
        if frontRight.dutyCycle > 0 and frontLeft.dutyCycle < 100:
            frontRight.dutyCycle -= 5
            frontLeft.dutyCycle += 5
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)

    elif (data == b'a'):
        if frontRight.dutyCycle < 100 and frontLeft.dutyCycle > 0:
            frontRight.dutyCycle += 5
            frontLeft.dutyCycle -= 5
            p.ChangeDutyCycle(frontRight.dutyCycle)
            r.ChangeDutyCycle(frontLeft.dutyCycle)
            print("Front right:")
            print(frontRight.dutyCycle)
            print("Front left:")
            print(frontLeft.dutyCycle)

    elif (data == b'self'):
        

    elif (data == b'stop'):
        frontRight.dutyCycle = 0
        frontLeft.dutyCycle = 0
        p.ChangeDutyCycle(frontRight.dutyCycle)
        r.ChangeDutyCycle(frontLeft.dutyCycle)
        
    elif (data == b'exit'):
        GPIO.cleanup()
        break
 
client_socket.close()
server_socket.close()

