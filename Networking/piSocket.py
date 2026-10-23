import socket

class piSocketLib:
    def __init__(self, command_queue):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('0.0.0.0', 5001))
        self.packet = ""
        self.command_queue = command_queue
    def listen(self):
        while True:
            data,addr = self.sock.recvfrom(1024)

            if not data:
                print("Disconnected")
                break

            response = self.processPacket(data)
            #connection test because it's UDP now
            if response == "PING":
                self.sock.sendto(b"PONG", addr)
                continue

            self.command_queue.put(response)
            # self.sock.sendto(b"ACK", addr)

    def processPacket(self, data):
        raw_text = data.decode('utf-8').strip()
        return raw_text
    def returnPackets(self):
        return self.packet