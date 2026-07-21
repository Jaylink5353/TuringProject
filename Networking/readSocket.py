import time

from piSocket import *
import queue
import threading

cmd_queue = queue.Queue()

socketServer = piSocketLib(command_queue=cmd_queue)
server_thread = threading.Thread(target=socketServer.listen, daemon=True)
server_thread.start()
print("Networking Up")

while True:
    time.sleep(0.1)
    try:
        command = cmd_queue.get_nowait()
        print(command)

    except queue.Empty:
        pass