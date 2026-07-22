import serial
import time

class piSerialLib:
    def __init__(self):
        self.lastHeartbeatTime = time.time()

        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)

    def sendCommand(self,command:str, speed:int):
        for i in range(5):
            packet = f"{command}:{speed};\n"
            self.ser.reset_input_buffer()
            self.ser.write(packet.encode('utf-8'))
            print(f"Packet Sent: {packet}")
            ack = self.waitForAck()
            if ack == True:
                break



    def waitForAck(self):
        startTime:float = time.time()

        while (time.time() - startTime) < 0.5:
            raw_data = self.ser.read(self.ser.in_waiting)
            incoming_text = raw_data.decode('utf-8', errors='ignore')
            if "ACK;" in incoming_text:
                print("ACK Recived")
                return True

        print("No ACK Recived, resending command")
        return False


    def checkHeartTime(self):
        currentTime = time.time()

        #Heartbeat
        if (currentTime - self.lastHeartbeatTime) >= 1.0:
            self.sendCommand("H",0)
            self.lastHeartbeatTime = currentTime
