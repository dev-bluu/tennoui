import asyncio
import tkinter as tk
from warpy import warpy
import win32gui
import win32api
import win32con
from styles import enable_clickthrough
from timers import Timer

X_POS_WIN_OFFSET = 8
Y_POS_WIN_OFFSET = 31

# DEFINE BASE TK WINDOW SETTINGS
root = tk.Tk()
root.title("TennoUI")
root.wm_attributes("-topmost", True)  # Keep at the top most layer (needs change)
root.wm_attributes("-disabled", True)  # Disable interactions with the window
root.wm_attributes("-transparent", '#2e3440')  # Used to make window transparent
root.overrideredirect(True)  # Remove the title bar

root.after(1, lambda: enable_clickthrough(root))  # Make overlay click through.
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

timers = tk.Frame(master=root, width=340, height=160, cursor="none")

loop = asyncio.get_event_loop()
warframe = warpy.Worldstate("pc", loop=loop)

# TIMERS
timers.grid(row=0, column=0)

tk.Label(timers, text="Cetus", fg="#FFFFFF").grid(row=0, column=0)
tk.Label(timers, text="Deimos", fg="#FFFFFF").grid(row=0, column=3)
tk.Label(timers, text="Vallis", fg="#FFFFFF").grid(row=0, column=6)

# String state indicators
cetus_timer = Timer(tk.StringVar(timers), tk.StringVar(timers), root, loop)
vallis_timer = Timer(tk.StringVar(timers), tk.StringVar(timers), root, loop)
cambion_timer = Timer(tk.StringVar(timers), tk.StringVar(timers), root, loop)

cetus_state_label = tk.Label(timers, textvariable=cetus_timer.state)
vallis_state_label = tk.Label(timers, textvariable=vallis_timer.state)
cambion_state_label = tk.Label(timers, textvariable=cambion_timer.state)

cetus_state_label.grid(row=0, column=1)
cambion_state_label.grid(row=0, column=4)
vallis_state_label.grid(row=0, column=7)

cetus_timer_label = tk.Label(timers, textvariable=cetus_timer.timer)
vallis_timer_label = tk.Label(timers, textvariable=vallis_timer.timer)
cambion_timer_label = tk.Label(timers, textvariable=cambion_timer.timer)

cetus_timer_label.grid(row=0, column=2)
cambion_timer_label.grid(row=0, column=5)
vallis_timer_label.grid(row=0, column=8)


# Asynchronous functions
async def cetus_state_widget():
    json = await warframe.cetus_status()
    next_attempt, remaining_time = cetus_timer.set_state(json, cetus_timer.cetus_handler)
    cetus_timer.update_timer(remaining_time)
    root.after(next_attempt, lambda: loop.run_until_complete(cetus_state_widget()))


async def vallis_state_widget():
    json = await warframe.vallis_status()
    next_attempt, remaining_time = vallis_timer.set_state(json, vallis_timer.vallis_handler)
    vallis_timer.update_timer(remaining_time)
    root.after(next_attempt, lambda: loop.run_until_complete(vallis_state_widget()))


async def cambion_state_widget():
    json = await warframe.cambion_status()
    next_attempt, remaining_time = cambion_timer.set_state(json, cambion_timer.cambion_handler)
    cambion_timer.update_timer(remaining_time)
    root.after(next_attempt, lambda: loop.run_until_complete(cambion_state_widget()))

loop.run_until_complete(cetus_state_widget())
loop.run_until_complete(vallis_state_widget())
loop.run_until_complete(cambion_state_widget())

root.mainloop()
