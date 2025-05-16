from flask import Flask, request
import ctypes
import time

# Constants
PUL = ctypes.POINTER(ctypes.c_ulong)

# C struct redefinitions
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _INPUT_UNION)]

# Constants for flags
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

# ctypes setup
SendInput = ctypes.windll.user32.SendInput

# Helper functions
def press_key(hexKeyCode, delay=0.1):
    scan_code = ctypes.windll.user32.MapVirtualKeyW(hexKeyCode, 0)
    
    # Key down
    ki_down = KEYBDINPUT(wVk=0, wScan=scan_code, dwFlags=KEYEVENTF_SCANCODE, time=0, dwExtraInfo=None)
    input_down = INPUT(type=INPUT_KEYBOARD, ki=ki_down)
    
    # Key up
    ki_up = KEYBDINPUT(wVk=0, wScan=scan_code, dwFlags=KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, time=0, dwExtraInfo=None)
    input_up = INPUT(type=INPUT_KEYBOARD, ki=ki_up)

    SendInput(1, ctypes.byref(input_down), ctypes.sizeof(INPUT))
    time.sleep(delay)
    SendInput(1, ctypes.byref(input_up), ctypes.sizeof(INPUT))

def key_down(hexKeyCode):
    scan_code = ctypes.windll.user32.MapVirtualKeyW(hexKeyCode, 0)
    ki = KEYBDINPUT(wVk=0, wScan=scan_code, dwFlags=KEYEVENTF_SCANCODE, time=0, dwExtraInfo=None)
    input = INPUT(type=INPUT_KEYBOARD, ki=ki)
    SendInput(1, ctypes.byref(input), ctypes.sizeof(INPUT))

def key_up(hexKeyCode):
    scan_code = ctypes.windll.user32.MapVirtualKeyW(hexKeyCode, 0)
    ki = KEYBDINPUT(wVk=0, wScan=scan_code, dwFlags=KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, time=0, dwExtraInfo=None)
    input = INPUT(type=INPUT_KEYBOARD, ki=ki)
    SendInput(1, ctypes.byref(input), ctypes.sizeof(INPUT))

# Flask app
app = Flask(__name__)
shiftDown = False

@app.route('/input', methods=['POST'])
def handle_input():
    global shiftDown
    data = request.json
    cmd = data.get('command')
    print("Command: " + cmd)

    if cmd == "enter":
        press_key(0x0D)

    elif cmd == "space":
        press_key(0x20)

    elif cmd == "ctrl":
        key_down(0x11)
        time.sleep(1)
        key_up(0x11)

    elif cmd == "toggleshiftdown":
        if shiftDown:
            key_up(0x10)  # Shift up
            shiftDown = False
        else:
            key_down(0x10)  # Shift down
            shiftDown = True

    elif cmd in ["up", "down", "left", "right"]:
        arrows = {"up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27}
        key = arrows[cmd]
        press_key(key)

    elif len(cmd) == 1:  # Single character
        vk = ord(cmd.upper())
        press_key(vk)

    elif cmd in ['e', 'f', 'q', 'r']:
        press_key(ord(cmd.upper()))

    return {"status": "ok"}

if __name__ == '__main__':
    app.run(port=8084)

