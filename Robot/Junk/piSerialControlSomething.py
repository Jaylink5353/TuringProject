from microbit import *
from keyes_mecanum_car_v2 import *
from piSerialParseLib import *

correctionFactorR = 0
correctionFactorL = 0
parser = commandParser(timeout_ms=1500)
mecanumCar = Mecanum_Car_Driver_V2()


moving:bool = False


def forward(speed):

    LSpeed = speed + correctionFactorL
    RSpeed = speed + correctionFactorR

    mecanumCar.Motor_Lower_L(1, LSpeed)
    mecanumCar.Motor_Upper_L(1, LSpeed)
    mecanumCar.Motor_Lower_R(1, RSpeed)
    mecanumCar.Motor_Upper_R(1, RSpeed)

def left(speed):
    LSpeed = speed + correctionFactorL
    RSpeed = speed + correctionFactorR
    mecanumCar.Motor_Upper_L(0, LSpeed)
    mecanumCar.Motor_Upper_R(1, RSpeed)
    mecanumCar.Motor_Lower_L(1, LSpeed)
    mecanumCar.Motor_Lower_R(0, RSpeed)


def stop():
    mecanumCar.Motor_Upper_L(0, 0)
    mecanumCar.Motor_Lower_L(0, 0)
    mecanumCar.Motor_Upper_R(0, 0)
    mecanumCar.Motor_Lower_R(0, 0)
while True:

    if parser.checkHeartbeat() is False:
        if moving is True:
            stop()
            moving = False

    result = parser.parseCommand()

    if result is not None:
        cmd, speed = result
        if cmd == "F":
            moving = True
            forward(speed)
        if cmd == "SL":
            moving = True
            left(speed)
        if cmd == "S":
            stop()
            moving = False

