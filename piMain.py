import queue
import time
import threading
from Networking.piSocket import piSocketLib
from Serial.piSerialLib import piSerialLib
from CamServer.camserver import CamServer

spd = 100

cmd_queue = queue.Queue()
CamServer.run(host='0.0.0.0', port=5000)

socketServer = piSocketLib(command_queue=cmd_queue)
server_thread = threading.Thread(target=socketServer.listen, daemon=True)
server_thread.start()
print("Networking Up")

serial_hw = piSerialLib()1

stop = True
moving = False
while True:
    time.sleep(0.01)
    serial_hw.checkHeartTime()

    try:
        command = cmd_queue.get_nowait()
        print(f"Processing incoming command: {command}")
        if command == "w":
           serial_hw.sendCommand(command="F", speed=spd)
           moving = True
        elif command == "s":
            serial_hw.sendCommand(command="B", speed=spd)
            moving = True
        elif command == "a":
            serial_hw.sendCommand(command="TL", speed=spd)
            moving = True
        elif command == "d":
            serial_hw.sendCommand(command="TR", speed=spd)
            moving = True
        elif command == "x":
            serial_hw.sendCommand(command="S", speed=0)
            moving = False
        else:
            print("Already Moving!!")
    except queue.Empty:
        """
        if stop == False:
            serial_hw.sendCommand(command="S", speed=0)
            stop = True
        if moving == True:
            serial_hw.sendCommand(command="S", speed=0)
            moving = False
        """
        pass
