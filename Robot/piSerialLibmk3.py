from microbit import *

BAUDRATE = 115200

timeout_ms = 10000

class microPiSerial:
    def __init__(self):
        self.uart = uart
        self.uart.init(baudrate=BAUDRATE)
        self.buffer = ""
        self.start_time = running_time()
        self.timeout_ms = timeout_ms

    def parse_packet(self, packet):
        """
        Parses a packet string of the form 'ID:VALUE'.
        Returns (id_str, value) on success, or (None, None) if the packet
        is malformed (missing colon, id not 1-2 chars, or value not an int).
        """
        if ":" not in packet:
            return None, None

        id_str, value_str = packet.split(":", 1)

        if not (1 <= len(id_str) <= 2):
            return None, None
        try:
            value = int(value_str)
        except ValueError:
            return None, None

        if id_str is "H" and value == 0:
            self.handleHeartbeat()
            return None, None
        else:
            return id_str, value


    def handle_packet(self, packet_id, value):
        # print("ID:", packet_id, "VALUE:", value)
        self.sendAck()
        return packet_id, value

    def sendAck(self):
        uart.write(b"ACK;\n")

    def write(self, string):
        writeMe = str(string)
        uart.write((writeMe.encode('utf-8')))

    def handle_bad_packet(self, raw_buffer):
        return None

    def handleHeartbeat(self):
        self.last_heard_time = running_time()
        self.sendAck()
        return

    def readUart(self):
        if uart.any():
            byte = uart.read(1)
            if not byte:
                return None

            try:
                char = byte.decode()
            except UnicodeDecodeError:
                # Got a stray non-UTF8 byte on the wire - ignore it.
                return None

            if char == ";":
                packet_id, value = self.parse_packet(self.buffer)
                raw_buffer = self.buffer
                self.buffer = ""

                if packet_id is not None:
                    return self.handle_packet(packet_id, value)
                else:
                    return self.handle_bad_packet(raw_buffer)

            elif char in ("\r", "\n"):
                # Ignore line-ending characters some terminals send alongside
                # keystrokes; they aren't part of the packet format.
                pass

            else:
                self.buffer += char
    def checkHeartbeat(self):
        if (running_time() - self.start_time) > timeout_ms:
            return False
        else:
            return True
