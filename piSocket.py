import socket

class piSocketLib:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SCOK_STREAM)
        sock.bind(('0.0.0.0', 5001))
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

    def processPacket(self, data):
        raw_text = data.decode('utf-8)').strip()
        return raw_text