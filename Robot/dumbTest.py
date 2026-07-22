from microbit import *
from piSerialLibmk3 import microPiSerial

serial = microPiSerial()

while True:
    packet  = serial.readUart()
    if packet is not None:
        command, speed = packet
        serial.write("Packet:{}:{};\n".format(command, speed))
        serial.write("Command:{}. YAP YAP Packet:{}".format(command, speed))
    sleep(10)
