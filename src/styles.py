import win32gui
import win32con
from ctypes import windll

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


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