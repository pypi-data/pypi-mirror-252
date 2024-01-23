from datetime import datetime


def get_formatted_time():
    """
    Get formatted time.
    :return: formatted time
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
