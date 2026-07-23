import webview
import os
import sys
from pynput import keyboard
import socket
import time

window_is_active = Trues
client_socket = None
ip = input("What is the IP? (r for recently visited, or q to quit) http://")
url = f"http://{ip}"
filename = "recently_visited.txt"
log_file = "keys.txt"
pressed_keys = set()
key_listener = None  # keep a reference so we only start it once


def on_press(key):
    try:
        k = key.char.lower()
    except AttributeError:
        return

    if k in ('w', 'a', 's', 'd') and k not in pressed_keys:
        pressed_keys.add(k)
        print(f"{k} down")
        if window_is_active:
            send_packet(f"{k}")
            print("Packet Sent: {k}")


def on_release(key):
    try:
        k = key.char.lower()
    except AttributeError:
        return

    if k in ('w', 'a', 's', 'd'):
        pressed_keys.discard(k)
        print(f"{k} up")
        if window_is_active:
            send_packet("x")
            print("Packet Sent:x")


def init_socket():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, 5001))
    except Exception as e:
        print("Connection failed")


def send_packet(data_string):
    global client_socket
    if client_socket is None:
        init_socket()
    if client_socket:
        try:
            client_socket.sendall(data_string.encode('utf-8'))
        except Exception as e:
            print("Packet send failed")
            client_socket = None
            init_socket()


def on_minimized():
    global window_is_active
    window_is_active = False


def on_restored():
    global window_is_active
    window_is_active = True


def start_key_listener():
    """Start the keyboard listener once, non-blocking."""
    global key_listener
    if key_listener is None:
        key_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        key_listener.start()  # NOT .join() — that would block everything


def on_shown():
    # Window shown; nothing special needed here now that the
    # listener is started once, up front.
    pass


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

window = webview.create_window(url, url + str(":5000"))

init_socket()
start_key_listener()
window.events.minimized += on_minimized
window.events.restored += on_restored
window.events.shown += on_shown

webview.start()

if client_socket:
    client_socket.close()


"""""
also u *should* make it so it can save it if the user wants it (later)

make a history feature
"""""