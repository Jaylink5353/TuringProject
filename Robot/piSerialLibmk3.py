"""
micro:bit UART packet receiver
================================
Packet format:   <id>:<value>;
  - id    = 1 or 2 characters (e.g. "1", "M1")
  - value = integer speed (can be negative, e.g. -75)
  - ';'   = end-of-packet marker

Usage modes
-----------
1) TESTING NOW over USB (MobaXterm / minicom / PuTTY):
   Flash this exactly as-is. uart.init() below does NOT specify tx/rx pins,
   which means it uses the micro:bit's USB serial connection (the same one
   used for the REPL). Open a serial terminal to the micro:bit's COM/tty
   port at 115200 baud and just type packets, e.g.:

       1:150;

   Type it out char by char (most terminal apps send each keystroke
   immediately) and you should see the micro:bit react and print a
   confirmation back over the same serial connection.

2) LATER over the edge connector (talking to a Raspberry Pi):
   Change the uart.init() call to specify physical pins, e.g.:

       uart.init(baudrate=BAUDRATE, tx=pin0, rx=pin1)

   Wire it to the Raspberry Pi like this:
       micro:bit pin0 (TX) -> Raspberry Pi UART RX (GPIO15 / pin 10)
       micro:bit pin1 (RX) -> Raspberry Pi UART TX (GPIO14 / pin 8)
       micro:bit GND       -> Raspberry Pi GND
   No level shifting needed - both run UART logic at 3.3V.
   Use raspi_uart_sender.py (the companion script) on the Pi side.
"""

from microbit import *

BAUDRATE = 115200

# --- Mode 1 (default): USB serial, works with MobaXterm/minicom right now.
uart.init(baudrate=BAUDRATE)

# --- Mode 2 (edge connector, for later): uncomment the line below and
#     comment out the uart.init() line above.
# from microbit import pin0, pin1
# uart.init(baudrate=BAUDRATE, tx=pin0, rx=pin1)

buffer = ""


def parse_packet(packet):
    """
    Parses a packet string of the form 'ID:VALUE'.
    Returns (id_str, value) on success, or (None, None) if the packet
    is malformed (missing colon, id not 1-2 chars, or value not an int).
    """
    if ":" not in packet:
        return None, None

    id_str, value_str = packet.split(":", 1)

    if not (1 <= len(id_str) <= 2):
        return None, None

    try:
        value = int(value_str)
    except ValueError:
        return None, None

    return id_str, value


def handle_packet(packet_id, value):
    """
    Called whenever a full, valid packet has been received.
    Replace the body of this function with whatever you actually want
    to do (e.g. drive a motor at `value` speed based on `packet_id`).
    """
    print("ID:", packet_id, "VALUE:", value)
    display.show(Image.YES)


def handle_bad_packet(raw_buffer):
    """Called whenever a terminated packet failed to parse."""
    print("Bad packet:", raw_buffer)
    display.show(Image.NO)


while True:
    if uart.any():
        byte = uart.read(1)
        if not byte:
            continue

        try:
            char = byte.decode()
        except UnicodeDecodeError:
            # Got a stray non-UTF8 byte on the wire - ignore it.
            continue

        if char == ";":
            packet_id, value = parse_packet(buffer)
            raw_buffer = buffer
            buffer = ""

            if packet_id is not None:
                handle_packet(packet_id, value)
            else:
                handle_bad_packet(raw_buffer)

        elif char in ("\r", "\n"):
            # Ignore line-ending characters some terminals send alongside
            # keystrokes; they aren't part of the packet format.
            pass

        else:
            buffer += char
