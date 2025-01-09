import psutil
import win32gui
import win32clipboard
from datetime import datetime

def get_active_window():
    """
    Get the title of the currently active window.
    Returns:
        str: The title of the active window or an error message.
    """
    try:
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except Exception as e:
        return f"Error: {e}"

def get_active_application():
    """
    Get the name of the currently active application.
    Returns:
        str: The name of the active application or an error message.
    """
    try:
        window = win32gui.GetForegroundWindow()
        process_id = win32gui.GetWindowThreadProcessId(window)[1]
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['pid'] == process_id:
                return proc.info['name']
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"

def get_clipboard_content():
    """
    Get the current content of the clipboard.
    Returns:
        str: The clipboard content or an error message.
    """
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    except Exception:
        return "Clipboard is empty or unsupported format."

def get_current_state():
    """
    Get the current state of system-level activities.
    Returns:
        dict: Contains active window, active application, clipboard content, and timestamp.
    """
    return {
        "active_window": get_active_window(),
        "active_application": get_active_application(),
        "clipboard_content": get_clipboard_content(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
