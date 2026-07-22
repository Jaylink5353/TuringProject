from microbit import *
from piSerialLibmk2 import serialParserv2

serial = serialParserv2()

def packetHandle(cmd, speed):
    serial.write("Command:", cmd, " Speed:", speed, "\n")

while True:
    serial.update(handler=packetHandle)
    sleep(10)
