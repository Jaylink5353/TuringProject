# Write your code here :-)
from microbit import *

# Init UART FIRST, before anything that touches I2C/the motor board.
# That way, if the motor board isn't connected/powered, serial still works.
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin5, rx=pin6)

from keyes_mecanum_car_v2 import *  # <-- comment this out to test parsing in isolation

motor_ok = True
try:
    mecanumCar = Mecanum_Car_Driver_V2()  # <-- comment this out to test parsing in isolation
except OSError:
    # Motor board isn't responding on I2C (not powered / not wired / wrong address).
    # Don't let that crash the whole program - just disable movement and carry on.
    motor_ok = False
    display.show(Image.SAD)
    sleep(1500)
    display.clear()

correctionFactorR = 0
correctionFactorL = 0

timeout_ms = 1500
last_heard_time = running_time()
moving = False
packet = ""


def send_ack():
    sleep(10)
    uart.write("ACK\n")


def forward(speed):
    if not motor_ok:
        return
    LSpeed = speed + correctionFactorL
    RSpeed = speed + correctionFactorR
    mecanumCar.Motor_Lower_L(1, LSpeed)
    mecanumCar.Motor_Upper_L(1, LSpeed)
    mecanumCar.Motor_Lower_R(1, RSpeed)
    mecanumCar.Motor_Upper_R(1, RSpeed)


def left(speed):
    if not motor_ok:
        return
    LSpeed = speed + correctionFactorL
    RSpeed = speed + correctionFactorR
    mecanumCar.Motor_Upper_L(0, LSpeed)
    mecanumCar.Motor_Upper_R(1, RSpeed)
    mecanumCar.Motor_Lower_L(1, LSpeed)
    mecanumCar.Motor_Lower_R(0, RSpeed)


def stop():
    if not motor_ok:
        return
    mecanumCar.Motor_Upper_L(0, 0)
    mecanumCar.Motor_Lower_L(0, 0)
    mecanumCar.Motor_Upper_R(0, 0)
    mecanumCar.Motor_Lower_R(0, 0)


while True:
    # --- read a line, same shape as the working echo script ---
    if uart.any():
        raw_data = uart.readline()
        if raw_data is not None:
            text = raw_data.decode('utf-8').strip()
            if text != "":
                packet = text
                last_heard_time = running_time()

    # --- process whatever packet we have, then clear it immediately ---
    if packet != "":
        parts = packet.split(":")
        packet = ""  # clear right away so a bad/duplicate packet can't get reprocessed

        if len(parts) == 2:
            command = parts[0]
            try:
                speed = int(parts[1])
            except ValueError:
                speed = None

            if speed is not None:
                if "H" in command:
                    # Heartbeat: just ack and reset the timeout clock
                    send_ack()
                    last_heard_time = running_time()
                else:
                    send_ack()
                    if command == "F":
                        moving = True
                        forward(speed)
                    elif command == "SL":
                        moving = True
                        left(speed)
                    elif command == "S":
                        stop()
                        moving = False

    # --- timeout check: stop if we haven't heard anything recently ---
    if (running_time() - last_heard_time) > timeout_ms:
        if moving:
            stop()
            moving = False

    sleep(0.1)
