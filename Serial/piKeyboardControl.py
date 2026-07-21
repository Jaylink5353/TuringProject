import sys
import tty
import termios
import select
import time
from piSerialLib import piSerialLib  # Fixed the import statement


piSerial = piSerialLib()

# Fix global declaration syntax
active_command = None


def get_keypress_non_blocking():
    """Reads a single keypress from the SSH terminal without pausing the loop."""
    # Check if there is text waiting in the terminal input stream
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1).lower()
    return None


# Save the original terminal settings so we can restore them when we close
old_settings = termios.tcgetattr(sys.stdin)

print("Driver station ready! Use WASD to steer, X to stop. Press Ctrl+C to exit.")

try:
    # Switch the SSH terminal to "cbreak mode" (reads keys immediately without needing Enter)
    tty.setcbreak(sys.stdin.fileno())

    while True:
        # Ticks your heartbeat timer automatically
        piSerial.checkHeartTime()

        # Check for SSH terminal keypresses
        char = get_keypress_non_blocking()

        if char is not None:
            if char == 'w':
                active_command = ("F", 90)
            elif char == 's':
                active_command = ("B", 90)
            elif char == 'a':
                active_command = ("L", 90)
            elif char == 'd':
                active_command = ("R", 90)
            elif char == 'x':
                active_command = ("S", 0)

        # 1. Check if a key was captured
        if active_command is not None:
            cmd, spd = active_command
            active_command = None  # Clear it so we don't loop-spam it
            piSerial.sendCommand(cmd, spd)

        # Sleep a tiny bit to avoid melting the CPU core
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nShutting down controller.")

finally:
    # CRITICAL: Put the terminal back to normal, otherwise your SSH window will act broken
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)