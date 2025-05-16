from flask import Flask, request
import ctypes
import time
import win32gui
import win32con
import pynput._util.win32

app = Flask(__name__)

# --- Find game window ---
hwnd = win32gui.FindWindow(None, "RogueBlightDemo")
if hwnd:
    print("✅ Window found!")
else:
    print("❌ Window not found.")

# --- DirectInput Scancodes ---
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
SPACE = 0x39
ENTER = 0x1C
ESC = 0x01
LEFT_SHIFT = 0x2A
LEFT_CTRL = 0x1D
E = 0x12
F = 0x21
Q = 0x10
R = 0x13
UP_ARROW = 0xC8
DOWN_ARROW = 0xD0
LEFT_ARROW = 0xCB
RIGHT_ARROW = 0xCD
J = 0x24
L = 0x26
X = 0x2D
Z = 0x2C
P = 0x19
O = 0x18
M = 0x32

# --- SendInput setup ---
SendInput = ctypes.windll.user32.SendInput


def HoldKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def HoldAndReleaseKey(hexKeyCode, seconds=0.1):
    HoldKey(hexKeyCode)
    time.sleep(seconds)
    ReleaseKey(hexKeyCode)

# --- Input route ---
@app.route('/input', methods=['POST'])
def handle_input():
    data = request.json
    cmd = data.get('command')
    print(f"🔹 Command received: {cmd}")

    # Focus the window
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    
    toggle = False 
    if cmd.startswith("toggle"):
        toggle = True
        cmd = cmd.replace("toggle", "").strip()

    key_map = {
        'w': W,
        'a': A,
        's': S,
        'd': D,
        'e': E,
        'f': F,
        'q': Q,
        'j': J,
        'l': L,
        'r': R,
        'x': X,
        'z': Z,
        'p': P,
        'o': O,
        'm': M,
        'space': SPACE,
        'enter': ENTER,
        'esc': ESC,
        'ctrl': LEFT_CTRL,
        'shift': LEFT_SHIFT,
        'up': UP_ARROW,
        'down': DOWN_ARROW,
        'left': LEFT_ARROW,
        'right': RIGHT_ARROW
    }

    key = key_map.get(cmd.lower())
    if key is not None:
        if toggle:
            if toggle_key[cmd] == True:
                toggle_key[cmd] = False
                ReleaseKey(key)
            else:
                toggle_key[cmd] = True
                HoldKey(key)
        else:
            HoldAndReleaseKey(key)
       
        return {"status": f"Sent {cmd}"}

    return {"status": "Unknown command"}, 400

if __name__ == '__main__':
    app.run(port=8084)

