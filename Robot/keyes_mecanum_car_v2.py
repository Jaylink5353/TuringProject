# from microbit import pin1, pin2, sleep, i2c
from microbit import *
import ustruct
import machine
from time import sleep_us, ticks_us
distance = 0

class Mecanum_Car_Driver_V2(object):
    def __init__(self):
        self.add = 0x30
        self.set_all_pwm(0)
        self.left_led(0)
        self.right_led(0)
        self.lastEchoDuration = -1
        i2c.init(freq=100000)
        #sleep(5)
    # Jaylink5353 - Manually added the servo code here
    class Servo:
        def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
            self.min_us = min_us
            self.max_us = max_us
            self.us = 0
            self.freq = freq
            self.angle = angle
            self.analog_period = 0
            self.pin = pin
            analog_period = round((1 / self.freq) * 1000)  # hertz to miliseconds
            self.pin.set_analog_period(analog_period)

        # The write_us method writes a pulse of the specified duration in microseconds to the servo motor.
        def write_us(self, us):
            us = min(self.max_us, max(self.min_us, us))
            duty = round(us * 1024 * self.freq // 1000000)
            self.pin.write_analog(duty)
            sleep(100)
            self.pin.write_analog(0)

        # The write_angle method moves the servo to the specified angle.
        def write_angle(self, degrees=None):
            if degrees is None:
                degrees = math.degrees(radians)
            degrees = degrees % 360
            total_range = self.max_us - self.min_us
            us = self.min_us + total_range * degrees // self.angle
            self.write_us(us)
    def set_pwm(self, channel, value):
        i2c.write(self.add, bytearray([channel, value & 0xFF]), repeat=False)

    def set_all_pwm(self, value):
        i2c.write(self.add, bytearray([0x01, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x02, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x03, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x04, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x05, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x06, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x07, value & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x08, value & 0xFF]), repeat=False)

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

    # 七彩灯
    def left_led(self, state):
        self.set_pwm(0x09, state)

    def right_led(self, state):
        self.set_pwm(0x0A, state)

    # 电机
    def Motor_Upper_L(self, stateL, left1):
        if (stateL == 1):
            self.set_pwm(3, 0)
            self.set_pwm(4, left1)
        elif (stateL == 0):
            self.set_pwm(3, left1)
            self.set_pwm(4, 0)

    def Motor_Lower_L(self, stateL, left1):
        if (stateL == 1):
            self.set_pwm(7, 0)
            self.set_pwm(8, left1)
        elif (stateL == 0):
            self.set_pwm(7, left1)
            self.set_pwm(8, 0)

    def Motor_Upper_R(self, stateR, right1):
        if (stateR == 1):
            self.set_pwm(1, 0)
            self.set_pwm(2, right1)
        elif (stateR == 0):
            self.set_pwm(1, right1)
            self.set_pwm(2, 0)

    def Motor_Lower_R(self, stateR, right1):
        if (stateR == 1):
            self.set_pwm(5, 0)
            self.set_pwm(6, right1)
        elif (stateR == 0):
            self.set_pwm(5, right1)
            self.set_pwm(6, 0)

    # 超声波
    def get_distance(self):
        pin15.write_digital(0)
        sleep_us(2)
        pin15.write_digital(1)
        sleep_us(15)
        pin15.write_digital(0)

        t = machine.time_pulse_us(pin16,1,35000)
        if (t <= 0 and self.lastEchoDuration >= 0) :
            t = self.lastEchoDuration

        self.lastEchoDuration = t
        return round(t * 0.017)

