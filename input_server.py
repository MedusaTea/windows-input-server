from flask import Flask, request
import pyvjoy
import time
import win32gui
import win32con
import win32api

hwnd = win32gui.FindWindow(None, "Legends Of Idleon")
if hwnd:
    print("Window found")
else:
    print("Window not found!")

app = Flask(__name__)

@app.route('/input', methods=['POST'])
def handle_input():
    data = request.json
    cmd = data.get('command')
    # Restore the window if it's minimized
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Bring it to the foreground
    win32gui.SetForegroundWindow(hwnd)

    print("Command: " + cmd)
    if cmd == "a":
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('A'), 0)
        time.sleep(2)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, ord('A'), 0)

    elif cmd == "left":
        j.set_axis(pyvjoy.HID_USAGE_X, 0)

    # Reset or release logic...
    return {"status": "ok"}

app.run(port=8084)

