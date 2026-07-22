from microbit import *

from piSerialLibmk3 import microPiSerial
from keyes_mecanum_car_v2 import *

serial = microPiSerial()
car = Mecanum_Car_Driver_V2()

def move_forward(speed):
    car.Motor_Upper_L(1, speed)
    car.Motor_Lower_L(1, speed)
    car.Motor_Upper_R(1, speed)
    car.Motor_Lower_R(1, speed)

def move_backward(speed):
    car.Motor_Upper_L(0, speed)
    car.Motor_Lower_L(0, speed)
    car.Motor_Upper_R(0, speed)
    car.Motor_Lower_R(0, speed)

def stop():
    car.Motor_Upper_L(0, 0)
    car.Motor_Lower_L(0, 0)
    car.Motor_Upper_R(0, 0)
    car.Motor_Lower_R(0, 0)

def move_left(speed):
    car.Motor_Upper_L(1, speed)
    car.Motor_Lower_L(0, speed)
    car.Motor_Upper_R(0, speed)
    car.Motor_Lower_R(1, speed)

def move_right(speed):
    car.Motor_Upper_L(0, speed)
    car.Motor_Lower_L(1, speed)
    car.Motor_Upper_R(1, speed)
    car.Motor_Lower_R(0, speed)

def turn_left(speed):
    car.Motor_Upper_L(0, 0)
    car.Motor_Lower_L(0, 0)
    car.Motor_Upper_R(1, speed)
    car.Motor_Lower_R(1, speed)

def turn_right(speed):
    car.Motor_Upper_L(1, speed)
    car.Motor_Lower_L(1, speed)
    car.Motor_Upper_R(0, 0)
    car.Motor_Lower_R(0, 0)

while True:
    packet = serial.readUart()
    if packet is not None:
        command, speed = packet
        if command == "F":
            move_forward(speed)
        if command == "S":
            stop()
        if command == "B":
            move_backward(speed)
        if command == "TL":
            turn_left(speed)
        if command == "TR":
            turn_right(speed)


    # if packet is None:
        # if serial.checkHeartbeat() == False:
            # stop()
