"""
Schedule model representing a collection of courses.
"""

from datetime import time
from typing import Dict, List

from pydantic import BaseModel, Field

from .course import Course, MeetingTime


class Schedule(BaseModel):
    """Represents a student's course schedule."""

    term: str = Field(description="Term code")
    courses: List[Course] = Field(default_factory=list, description="Courses in schedule")
    score: float = Field(default=0.0, description="Schedule quality score (0-100)")
    metadata: Dict[str, any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @property
    def total_credits(self) -> float:
        """Calculate total credit hours."""
        return sum(course.credits for course in self.courses)

    @property
    def has_conflicts(self) -> bool:
        """Check if schedule has any time conflicts."""
        for i, course1 in enumerate(self.courses):
            for course2 in self.courses[i + 1 :]:
                if course1.conflicts_with(course2):
                    return True
        return False

    @property
    def course_count(self) -> int:
        """Get number of courses."""
        return len(self.courses)

    def get_conflicts(self) -> List[tuple[Course, Course]]:
        """Get list of conflicting course pairs."""
        conflicts = []
        for i, course1 in enumerate(self.courses):
            for course2 in self.courses[i + 1 :]:
                if course1.conflicts_with(course2):
                    conflicts.append((course1, course2))
        return conflicts

    def get_weekly_schedule(self) -> Dict[str, List[MeetingTime]]:
        """Organize schedule by day of week."""
        schedule = {"M": [], "T": [], "W": [], "R": [], "F": []}

        for course in self.courses:
            for meeting in course.meeting_times:
                for day in meeting.days:
                    if day in schedule:
                        schedule[day].append(meeting)

        # Sort each day by start time
        for day in schedule:
            schedule[day].sort(key=lambda m: m.start_time if m.start_time else time.max)

        return schedule

    def add_course(self, course: Course) -> bool:
        """
        Add a course to the schedule.

        Returns:
            True if added successfully, False if conflicts exist
        """
        # Check for conflicts
        for existing in self.courses:
            if existing.conflicts_with(course):
                return False

        self.courses.append(course)
        return True

    def remove_course(self, crn: str) -> bool:
        """
        Remove a course by CRN.

        Returns:
            True if removed, False if not found
        """
        for i, course in enumerate(self.courses):
            if course.crn == crn:
                self.courses.pop(i)
                return True
        return False

    def get_course_by_crn(self, crn: str) -> Course | None:
        """Get a course by its CRN."""
        for course in self.courses:
            if course.crn == crn:
                return course
        return None

    def __str__(self) -> str:
        """String representation."""
        return (
            f"Schedule({self.course_count} courses, "
            f"{self.total_credits} credits, score={self.score:.1f})"
        )

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"Schedule(term={self.term!r}, courses={self.course_count}, "
            f"credits={self.total_credits}, conflicts={self.has_conflicts})"
        )

    class Config:
        json_schema_extra = {
            "example": {
                "term": "202501",
                "courses": [],
                "score": 85.5,
                "metadata": {"preferences": {"prefer_morning": True}},
            }
        }
