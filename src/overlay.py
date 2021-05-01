import tkinter as tk
import warframe_api as warpy
import win32gui
import win32api
import win32con
import requests
from ctypes import windll

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

X_POS_WIN_OFFSET = 8
Y_POS_WIN_OFFSET = 31

# DEFINE BASE TK WINDOW SETTINGS
root = tk.Tk()
root.title("TennoUI")
root.wm_attributes("-topmost", True)  # Keep at the top most layer (needs change)
root.wm_attributes("-disabled", True)  # Disable interactions with the window
root.wm_attributes("-transparent", '#2e3440')  # Used to make window transparent
root.overrideredirect(True)  # Remove the title bar


def enable_clickthrough(_root):
    """
    Sets the app window to be click through.
    :param _root: Tkinter parent
    :return:
    """
    _hwnd = windll.user32.GetParent(_root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(_hwnd, GWL_EXSTYLE)
    style |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(_hwnd, win32con.GWL_EXSTYLE, style)


def disable_clickthrough(_root):
    """
    TODO: Properly implement this so it can undo click-through transparency
    :param _root: Tkinter parent
    :return:
    """
    _hwnd = windll.user32.GetParent(_root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(_hwnd, GWL_EXSTYLE)
    style |= win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(_hwnd, win32con.GWL_EXSTYLE, style)


root.after(10, lambda: enable_clickthrough(root))  # Make overlay click through.
# Define the root's geometry based on the geometry of specified application.
# List of Warframe class names:
#   - WarframePublicEvolutionGfxD3D12
#   - WarframePublicEvolutionGfxD3D11 (NEED TO TEST THIS VALUE)
hwnd = win32gui.FindWindow("WarframePublicEvolutionGfxD3D12", None)
fullscreen = borderless = False
if hwnd:
    # Window rectangle includes title bar which results in a mismatch when applying the overlay.
    # Client rectangle provides the correct dimensions but does not provide the x and y positions
    # of the window relative to the screen space, hence their retrieval with GetWindowRect().
    x_pos, y_pos, _, _ = win32gui.GetWindowRect(hwnd)
    _, _, width, height = win32gui.GetClientRect(hwnd)

    if win32gui.GetWindowPlacement(hwnd)[1] == win32con.SW_SHOWMAXIMIZED:
        # Checks to see if the window is fullscreen.
        fullscreen = True
    if width == win32api.GetSystemMetrics(0) and height == win32api.GetSystemMetrics(1):
        # Compares screen space to client dimensions. The window is likely borderless if
        # the width and height match the screen space and fullscreen is not detected.
        borderless = True

else:
    # Assume fullscreen
    x_pos, y_pos, width, height, fullscreen = 0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1), True

if fullscreen:
    # root.wm_attributes("-fullscreen", True)
    print("Fullscreen is not supported")  # Currently unable to display above fullscreen apps
    exit()
elif borderless:
    root.geometry('%dx%d+%d+%d' % (width, height, x_pos, y_pos))
    print("Borderless")
else:
    # Offset required to properly place the window on-top of client rectangle
    root.geometry('%dx%d+%d+%d' % (width, height, x_pos + X_POS_WIN_OFFSET, y_pos + Y_POS_WIN_OFFSET))
    print("Windowed")

timers = tk.Frame(master=root, bg="#FFFFFF", width=340, height=160, cursor="none")

warframe = warpy.WarframeAPI("pc", requests.session())

timers.grid(row=0, column=0)

tk.Label(timers, text="Cetus", fg="#FFFFFF").grid(row=0, column=0)
tk.Label(timers, text="Deimos", fg="#FFFFFF").grid(row=0, column=2)
tk.Label(timers, text="Vallis", fg="#FFFFFF").grid(row=0, column=4)

cetus_timer = tk.Label(timers)
vallis_timer = tk.Label(timers)
cambion_timer = tk.Label(timers)
cetus_timer.grid(row=0, column=1)
cambion_timer.grid(row=0, column=3)
vallis_timer.grid(row=0, column=5)


def current_cycles():
    cetus_status = warframe.cetus_status()
    vallis_status = warframe.vallis_status()
    cambion_status = warframe.cambion_status()
    if cetus_status["isDay"]:
        cetus_timer.config(text="Day")
    else:
        cetus_timer.config(text="Night")
    if vallis_status["isWarm"]:
        vallis_timer.config(text="Warm")
    else:
        vallis_timer.config(text="Cold")
    cambion_timer.config(text=cambion_status["active"].capitalize())
    root.after(300000, current_cycles)


current_cycles()

root.mainloop()
