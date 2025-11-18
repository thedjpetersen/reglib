"""
Time utility functions (ported and modernized from v1).
"""

from datetime import time
from typing import List


def time_conflict(time1: List[str], time2: List[str]) -> bool:
    """
    Determine whether two time ranges conflict.

    This function is preserved from v1 - it was excellent!

    Args:
        time1: Time range ['HH:MM', 'HH:MM'] (start, end)
        time2: Time range ['HH:MM', 'HH:MM'] (start, end)

    Returns:
        True if times overlap, False otherwise

    Example:
        >>> time_conflict(['13:00', '13:50'], ['13:30', '14:20'])
        True
        >>> time_conflict(['10:00', '10:50'], ['11:00', '11:50'])
        False
    """
    if (time1[0] >= time2[0] and time1[0] <= time2[1]) or (
        time1[1] >= time2[0] and time1[1] <= time2[1]
    ):
        return True
    return False


def format_time_range(start: time, end: time) -> str:
    """
    Format a time range for display.

    Args:
        start: Start time
        end: End time

    Returns:
        Formatted string (e.g., '10:00 AM - 10:50 AM')
    """
    return f"{start.strftime('%-I:%M %p')} - {end.strftime('%-I:%M %p')}"


def parse_time(time_str: str) -> time:
    """
    Parse a time string to datetime.time.

    Args:
        time_str: Time string (HH:MM format)

    Returns:
        datetime.time object
    """
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]))
