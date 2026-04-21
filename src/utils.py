from datetime import datetime

def get_current_date():
    """
    Returns the current date and time as a formatted string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
