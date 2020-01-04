#import serial

#bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate = 9600)
#print("Bluetooth connected")
#data = bluetoothSerial.readLine()
#if not data:
#    print("No data")
#else:
#    data = data.decode()
#    print("Received data: ", + data)
from bluetooth import *
sock = BluetoothSocket( RFCOMM )
sock.connect(('B4:86:55:6A:B0:83', 1))