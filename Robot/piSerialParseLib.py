from microbit import *

class commandParser:
    def __init__(self, timeout_ms=1500):
        self.start_time = running_time()
        self.buffer = ""
        self.timeout_ms = timeout_ms
        self.packet = ""
        self.last_heard_time = 0
        uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin5, rx=pin6)  #
        uart.write("init")
    def read(self):
        print("reading line")
        if uart.any():
            raw_data = uart.readline()
            text = raw_data.decode('utf-8').strip()
            self.last_heard_time = running_time()
            self.packet = text
            uart.write(text)

    def sendAck(self):
        sleep(10)
        uart.write("ACK\n")
    def parseCommand(self):
        self.read()
        try:
            parts = self.packet.split(":")
            if len(parts) == 2:
                command = str(parts[0])
                speed = int(parts[1])
                if "H" in command:
                    # This is the Heartbeat
                    self.sendAck()
                    self.last_heard_time = running_time()
                    return None
                self.sendAck()
                self.packet = ""
                return command, speed
            else:
                # print("Invalid packet structure")
                self.packet = ""
                return None
        except Exception as e:
            # print(e)
            return None
    def checkHeartbeat(self):
        if (running_time() - self.start_time) > 1500:
            # print("TimeOut")
            return False
        else:
            return True
