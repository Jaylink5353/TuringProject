# THIS IS NOT THE ACTUALL ONE, but it WILL need this stuff in it!!
import queue
import time
import threading
from piSocket import piSocketLib

cmd_queue = queue.Queue()


socketServer = piSocketLib(command_queue=cmd_queue)

server_thread = threading.Thread(target=socketServer.listen, daemon=True)

server_thread.start()
print("Networking Up")

while True:
    time.sleep(0.1)
    try:
        command = cmd_queue.get_nowait()
        print(f"Processing incoming command: {command}")
        if command == "W":
            #move forward
        elif command == "S":
            # backward
        elif command == "A":
            # left
        elif command == "D":
            #right
    except queue.Empty:
        pass
        