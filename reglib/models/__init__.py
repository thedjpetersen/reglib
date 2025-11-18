"""
Core data models for the OSU Course Planner.
"""

from .course import Course, MeetingTime
from .schedule import Schedule
from .term import Term

__all__ = ["Course", "MeetingTime", "Schedule", "Term"]
