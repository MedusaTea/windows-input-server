from flask import Flask, request
import pyvjoy
import time
import win32gui
import win32con
import win32api

hwnd = win32gui.FindWindow(None, "Binding of Isaac: Rebirth")
if hwnd:
    print("Window found")
else:
    print("Window not found!")

app = Flask(__name__)

def press_key(hexKeyCode, delay=0.05):
    win32api.keybd_event(hexKeyCode, 0,0,0)
    time.sleep(delay)
    win32api.keybd_event(hexKeyCode,0, win32con.KEYEVENTF_KEYUP,0)


@app.route('/input', methods=['POST'])
def handle_input():
    data = request.json
    cmd = data.get('command')
    print("Command: " + cmd)
    # Restore the window if it's minimized
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    # Bring it to the foreground
    win32gui.SetForegroundWindow(hwnd)

    if cmd == "enter":
        press_key(0x0D)

    if cmd == "a" or cmd == "s" or cmd == "w" or cmd == "d": 
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord(cmd.upper()), 0)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, ord(cmd.upper()), 0)
 
    if cmd == "up":
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x25, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x27, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x28, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x26, 0)
    
    if cmd == "down":
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x25, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x27, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x26, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x28, 0)
        
    if cmd == "left":
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x28, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x27, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x26, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x25, 0)
   
   if cmd == "right":
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x25, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x26, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x28, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x27, 0)

    elif cmd == "b":
        press_key(0x45)

    elif cmd == "q":
        press_key(0x51)

    elif cmd == "i":
        press_key(win32con.VK_SPACE)

    elif cmd == "ctrl":
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LCONTROL, 0)
        time.sleep(1)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LCONTROL, 0)

#    elif cmd == "left":
#        j.set_axis(pyvjoy.HID_USAGE_X, 0)

    # Reset or release logic...
    return {"status": "ok"}

app.run(port=8084)

