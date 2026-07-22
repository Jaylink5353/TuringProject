import queue
import time
import threading
from Networking.piSocket import piSocketLib
from Serial.piSerialLib import piSerialLib

spd = 100

cmd_queue = queue.Queue()

socketServer = piSocketLib(command_queue=cmd_queue)
server_thread = threading.Thread(target=socketServer.listen, daemon=True)
server_thread.start()
print("Networking Up")

serial_hw = piSerialLib()

stop = True
while True:
    time.sleep(0.01)
    serial_hw.checkHeartTime()

    try:
        command = cmd_queue.get_nowait()
        print(f"Processing incoming command: {command}")
        if command == "W":
           serial_hw.sendCommand(command="F", speed=spd)
        elif command == "S":
            serial_hw.sendCommand(command="B", speed=spd)
        elif command == "A":
            serial_hw.sendCommand(command="TL", speed=spd)
        elif command == "D":
            serial_hw.sendCommand(command="TR", speed=spd)
        elif command == "X":
            serial_hw.sendCommand(command="S", speed=0)
    except queue.Empty:
        if stop == False:
            serial_hw.sendCommand(command="S", speed="0")
            stop = True
        pass
        