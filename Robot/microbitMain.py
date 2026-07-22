from microbit import *

from piSerialLibmk3 import microPiSerial
# from keyes_mecanum_car_v2 import *

serial = microPiSerial()
# car = Mecanum_Car_Driver_V2()

def stop():
    return

while True:
    packet = serial.readUart()
    if packet is not None:
        command, speed = packet
        # put all commands here
    if packet is None:
        if serial.checkHeartbeat() == False:
            stop()
