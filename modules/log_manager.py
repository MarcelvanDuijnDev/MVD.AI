import os

LOGS_DIR = "app/logs/"

os.makedirs(LOGS_DIR, exist_ok=True)

def log_message(log_type, message):
    """
    Append a message to the specified log file.
    Args:
        log_type (str): The type of log (e.g., "ai_usage", "blocked_messages").
        message (str): The message to log.
    """
    log_file = os.path.join(LOGS_DIR, f"{log_type}.log")
    with open(log_file, "a") as file:
        file.write(f"{message}\n")

def read_logs(log_type):
    """
    Read all messages from a specified log file.
    Args:
        log_type (str): The type of log (e.g., "ai_usage", "blocked_messages").
    Returns:
        list: A list of log messages or an error message if the log doesn't exist.
    """
    log_file = os.path.join(LOGS_DIR, f"{log_type}.log")
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            return file.readlines()
    else:
        return [f"No logs found for {log_type}."]

def clear_logs(log_type):
    """
    Clear all messages from a specified log file.
    Args:
        log_type (str): The type of log (e.g., "ai_usage", "blocked_messages").
    Returns:
        dict: A message indicating the result.
    """
    log_file = os.path.join(LOGS_DIR, f"{log_type}.log")
    if os.path.exists(log_file):
        open(log_file, "w").close()
        return {"message": f"{log_type} logs cleared successfully."}
    else:
        return {"error": f"No logs found for {log_type}."}
