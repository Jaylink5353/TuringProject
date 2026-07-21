import webview
import os
import sys
from pynput import keyboard
import socket
import threading
import time

window_is_active = True
ip = input("What is the IP? (r for recently visited, or q to quit) http://")
url = f"http://{ip}"
filename = "recently_visited.txt"
log_file = "keys.txt"


def log_to_file(text):
    try:
        with open(log_file, "a") as f:
            f.write(text)
    except IOError as e:
        print(f"An error occured: {e}")

def on_press(key):
    global window_is_active
    if not window_is_active:
        return
    try:
        key_char = key.char.lower()

        if key_char in ['w', 'a', 's', 'd']:
            log_to_file(key.char)
    except AttributeError:
        pass

def on_minimized():
    global window_is_active
    window_is_active = False

def on_restored():
    global window_is_active
    window_is_active = True

def on_shown():
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()

def init_socket():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, 5001))
    except Exception as e:
        print("Connection failed")

def send_packet(data_string):
    global client_socket
    if client_socket:
        try:
            client_socket.sendall(data_string.encode('utf-8'))
        except Exception as e:
            print("Packet send failed")
            init_socket()

def send_tcp_packet():
    while True:
        host = ip
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, 5001))
                packet_data = "Hello!".encode('utf-8')
                sock.sendall(packet_data)
            except ConnectionRefusedError:
                print("Failed to conect")
        time.sleep(0.1)

if ip == "r":
    with open(filename, "r") as file:
        all_lines = [line.strip() for line in file if line.strip()]
    recent_lines = all_lines[-5:]
    print("\n--- 5 Most Recent URLs Visited ---")
    for index, line in enumerate(recent_lines, start=1):
        print(f"{index}. {line}")
    print("-----------------------------------\n")
    while True:
        try:
            choice = input(f"Select an option (1-{len(recent_lines)}) or 'q' to quit: ")

            if choice.lower() == "q":
                print("Exiting")
                sys.exit()

            choice_num = int(choice)

            if 1 <= choice_num <= len(recent_lines):
                selected_item = recent_lines[choice_num - 1]
                print(f"\nYou Selected: '{selected_item}'")
                break
            else:
                print("Invalid range")
        except ValueError:
            print("Invalid input")
    url = (selected_item)

elif url == "q":
  print("Exiting")
  sys.exit()  

else:
    already_exists = False

    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_lines = [line.strip() for line in file.readlines()]
            if url in existing_lines:
                already_exists = True

    if already_exists is True:
        pass
    else:
        with open("recently_visited.txt", "a") as file:
            file.write(url + "\n")

window = webview.create_window(url, url)

window.events.minimized += on_minimized
window.events.restored += on_restored
window.events.shown += on_shown

send_thread = threading.Thread(target=send_tcp_packet, daemon=True)
send_thread.start()
webview.start()

if client_socket:
    client_socket.close()



"""""
also u *should* make it so it can save it if the user wants it (later)

make a history feature
"""""