from microbit import *

class serialParserv2:
    def __init__(self):
        uart.init(baudrate=115200, bits=8, parity=None, stop=1)  #tx=pin5, rx=pin6
        self.buffer = ""

    def processPacket(self, cmd, speed):
        print("")
        # Processing Logic Coming soon

    def readPacket(self):
        if uart.any():
            raw = uart.read(1)
            if not raw:
               return None

            try:
                char = raw.decode()

                if char == ";":
                    packet = self.buffer
                    self.buffer = ""
                    return packet
                else:
                    buffer = self.buffer + char
            except:
                return None
        else:
            return None
    def write(self, string):
        uart.write(string.encode())

    def parsePacket(self, packet):
        if ":" not in packet:
            return None
        cmd, speed = packet.split(":", 1)

        if not (1 <= len(cmd) <=2):
            return None

        if not speed.isdigit():
            return None

        return cmd, int(speed)

    def sendAck(self):
        uart.write("ACK\n".encode())

    def update(self, handler=None):
        packet = self.readPacket()
        if not packet:
            return

        parsed = self.parsePacket(packet)
        if parsed:
            cmd, speed = parsed
            if handler:
                handler(cmd, speed)
            self.sendAck()
