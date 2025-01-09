import psutil
from datetime import datetime


def get_system_info():
    """
    Fetch system performance metrics and environment details.
    Returns:
        dict: Contains CPU, memory, disk usage, and time of day.
    """
    try:
        system_info = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "time_of_day": datetime.now().strftime("%H:%M:%S"),
            "uptime": get_system_uptime()
        }
        return system_info
    except Exception as e:
        return {"error": str(e)}

def get_system_uptime():
    """
    Calculate system uptime.
    Returns:
        str: Uptime in days, hours, minutes.
    """
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        current_time = datetime.now()
        uptime = current_time - boot_time
        days, hours, minutes = uptime.days, uptime.seconds // 3600, (uptime.seconds // 60) % 60
        return f"{days}d {hours}h {minutes}m"
    except Exception as e:
        return f"Error calculating uptime: {e}"
