import socket

class piSocketLib:
    def __init__(self, command_queue):
        self.sock = socket.socket(socket.AF_INET, socket.SCOK_STREAM)
        self.sock.bind(('0.0.0.0', 5001))
        self.packet = ""
        self.command_queue = command_queue
    def listen(self):
        while True:
            conn, addr = self.sock.accept()
            print(f"Connection from {addr}")

            with conn:
                while True:
                    data = conn.recv(1024)

                    if not data:
                        print("Disconnected")
                        break

                    response = self.processPacket(data)
                    self.packet = response
                    self.sock.sendall(b"ACK")

    def processPacket(self, data):
        raw_text = data.decode('utf-8)').strip()
        return raw_text
    def returnPackets(self):
        return self.packet