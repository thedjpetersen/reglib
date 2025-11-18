"""
Course model representing a single course offering.
"""

from datetime import time
from typing import List, Optional

from pydantic import BaseModel, Field


class MeetingTime(BaseModel):
    """Represents a single meeting time for a course."""

    days: List[str] = Field(description="Days of the week (M, T, W, R, F)")
    start_time: Optional[time] = Field(None, description="Start time")
    end_time: Optional[time] = Field(None, description="End time")
    location: str = Field(default="TBA", description="Building and room")
    instructor: Optional[str] = Field(None, description="Instructor name")

    def overlaps_with(self, other: "MeetingTime") -> bool:
        """Check if this meeting time overlaps with another."""
        # No overlap if no common days
        if not set(self.days) & set(other.days):
            return False

        # No overlap if either time is TBA
        if (
            self.start_time is None
            or self.end_time is None
            or other.start_time is None
            or other.end_time is None
        ):
            return False

        # Check time overlap
        return self.start_time < other.end_time and self.end_time > other.start_time

    class Config:
        json_schema_extra = {
            "example": {
                "days": ["M", "W", "F"],
                "start_time": "10:00:00",
                "end_time": "10:50:00",
                "location": "LINC 200",
                "instructor": "Smith, John",
            }
        }


class Course(BaseModel):
    """Represents a single course offering."""

    # Identifiers
    crn: str = Field(description="Course Registration Number")
    term: str = Field(description="Term code (e.g., 202501)")
    subject: str = Field(description="Subject code (e.g., CS)")
    course_number: str = Field(description="Course number (e.g., 161)")
    section: str = Field(description="Section number")

    # Course info
    title: str = Field(description="Course title")
    credits: float = Field(description="Credit hours")

    # Enrollment
    seats_total: int = Field(default=0, description="Total seats")
    seats_available: int = Field(default=0, description="Available seats")
    seats_waitlist: int = Field(default=0, description="Waitlist count")
    waitlist_capacity: int = Field(default=0, description="Waitlist capacity")

    # Schedule
    meeting_times: List[MeetingTime] = Field(
        default_factory=list, description="Meeting times"
    )

    # Additional details
    description: Optional[str] = Field(None, description="Course description")
    prerequisites: Optional[str] = Field(None, description="Prerequisites")
    instructors: List[str] = Field(default_factory=list, description="Instructors")
    campus: str = Field(default="Corvallis", description="Campus location")
    delivery_mode: str = Field(
        default="In-Person", description="Delivery mode (In-Person, Online, Hybrid)"
    )
    restrictions: Optional[str] = Field(None, description="Enrollment restrictions")

    @property
    def course_code(self) -> str:
        """Get the full course code (e.g., CS 161)."""
        return f"{self.subject} {self.course_number}"

    @property
    def full_name(self) -> str:
        """Get the full course name with title."""
        return f"{self.course_code} - {self.title}"

    @property
    def is_full(self) -> bool:
        """Check if the course is full."""
        return self.seats_available <= 0

    @property
    def is_online(self) -> bool:
        """Check if the course is online."""
        return self.delivery_mode.lower() in ["online", "ecampus"]

    def conflicts_with(self, other: "Course") -> bool:
        """Check if this course has time conflicts with another course."""
        # Can't take the same course twice
        if self.crn == other.crn:
            return True

        # Check meeting time conflicts
        for my_time in self.meeting_times:
            for other_time in other.meeting_times:
                if my_time.overlaps_with(other_time):
                    return True

        return False

    def __str__(self) -> str:
        """String representation."""
        return f"{self.course_code}-{self.section} ({self.crn})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"Course(crn={self.crn}, code={self.course_code}, "
            f"section={self.section}, title={self.title!r})"
        )

    class Config:
        json_schema_extra = {
            "example": {
                "crn": "12345",
                "term": "202501",
                "subject": "CS",
                "course_number": "161",
                "section": "001",
                "title": "Introduction to Computer Science I",
                "credits": 4.0,
                "seats_total": 100,
                "seats_available": 25,
                "seats_waitlist": 5,
                "waitlist_capacity": 20,
                "meeting_times": [
                    {
                        "days": ["M", "W", "F"],
                        "start_time": "10:00:00",
                        "end_time": "10:50:00",
                        "location": "KEARNEY 212",
                        "instructor": "Smith, Jane",
                    }
                ],
                "instructors": ["Smith, Jane"],
                "campus": "Corvallis",
                "delivery_mode": "In-Person",
            }
        }
