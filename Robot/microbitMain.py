from microbit import *

from piSerialLibmk3 import microPiSerial
from keyes_mecanum_car_v2 import *

serial = microPiSerial()
car = Mecanum_Car_Driver_V2()
turnoffset = 40
offset = -2
def move_forward(speed):
    car.Motor_Upper_L(1, speed+offset)
    car.Motor_Lower_L(1, speed+offset)
    car.Motor_Upper_R(1, speed)
    car.Motor_Lower_R(1, speed)

def move_backward(speed):
    car.Motor_Upper_L(0, speed+offset)
    car.Motor_Lower_L(0, speed+offset)
    car.Motor_Upper_R(0, speed)
    car.Motor_Lower_R(0, speed)

def stop():
    car.Motor_Upper_L(0, 0)
    car.Motor_Lower_L(0, 0)
    car.Motor_Upper_R(0, 0)
    car.Motor_Lower_R(0, 0)

def move_left(speed):
    car.Motor_Upper_L(1, speed+offset)
    car.Motor_Lower_L(0, speed+offset)
    car.Motor_Upper_R(0, speed)
    car.Motor_Lower_R(1, speed)

def move_right(speed):
    car.Motor_Upper_L(0, speed+offset)
    car.Motor_Lower_L(1, speed+offset)
    car.Motor_Upper_R(1, speed)
    car.Motor_Lower_R(0, speed)

def turn_left(speed):
    car.Motor_Upper_L(0, 0)
    car.Motor_Lower_L(0, 0)
    car.Motor_Upper_R(1, speed-turnoffset)
    car.Motor_Lower_R(1, speed-turnoffset)

def turn_right(speed):
    car.Motor_Upper_L(1, speed-turnoffset)
    car.Motor_Lower_L(1, speed-turnoffset)
    car.Motor_Upper_R(0, 0)
    car.Motor_Lower_R(0, 0)

while True:
    packet = serial.readUart()
    if packet is not None:
        command, speed = packet
        if command == "F":
            move_forward(speed)
        elif command == "S":
            stop()
        elif command == "B":
            move_backward(speed)
        elif command == "TL":
            turn_left(speed)
        elif command == "TR":
            turn_right(speed)
        elif command == "SL":
            move_left(speed)
        elif command == "SR":
            move_right(speed)
"""
    if button_a.is_pressed():
        stop()
    if button_b.is_pressed():
        stop()


    # if packet is None:
        # if serial.checkHeartbeat() == False:
            # stop()
"""