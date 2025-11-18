"""
Schedule builder for generating conflict-free schedules.

This module preserves and modernizes the excellent schedule building logic
from v1, which generated all possible non-conflicting course combinations.
"""

from itertools import product
from typing import List, Optional

from rich.console import Console
from rich.progress import track

from reglib.models import Course, Schedule

console = Console()


class ScheduleBuilder:
    """Builds conflict-free schedules from a list of desired courses."""

    def __init__(self, term: str):
        """
        Initialize the schedule builder.

        Args:
            term: Term code (e.g., '202501')
        """
        self.term = term
        self.desired_courses: List[List[Course]] = []
        self.preferences = {}
        self.constraints = []

    def add_course_options(self, courses: List[Course]) -> None:
        """
        Add course options (e.g., different sections of CS 161).

        Args:
            courses: List of course sections to choose from
        """
        if courses:
            self.desired_courses.append(courses)

    def add_preference(self, key: str, value: any) -> None:
        """
        Add a scheduling preference.

        Args:
            key: Preference key (e.g., 'prefer_online', 'prefer_morning')
            value: Preference value
        """
        self.preferences[key] = value

    def generate_schedules(
        self,
        max_results: int = 100,
        prefer_online: bool = False,
        prefer_morning: bool = False,
        avoid_friday: bool = False,
    ) -> List[Schedule]:
        """
        Generate all possible conflict-free schedules.

        Args:
            max_results: Maximum number of schedules to return
            prefer_online: Prefer online courses
            prefer_morning: Prefer morning classes
            avoid_friday: Avoid Friday classes

        Returns:
            List of Schedule objects, sorted by score
        """
        if not self.desired_courses:
            return []

        # Generate all possible combinations
        all_combinations = list(product(*self.desired_courses))

        schedules = []
        for combination in track(
            all_combinations,
            description="Building schedules...",
            console=console,
            transient=True,
        ):
            schedule = Schedule(term=self.term, courses=list(combination))

            # Skip if has conflicts
            if schedule.has_conflicts:
                continue

            # Calculate score based on preferences
            score = self._score_schedule(
                schedule, prefer_online, prefer_morning, avoid_friday
            )
            schedule.score = score

            schedules.append(schedule)

            # Stop if we have enough
            if len(schedules) >= max_results:
                break

        # Sort by score (highest first)
        schedules.sort(key=lambda s: s.score, reverse=True)

        return schedules[:max_results]

    def _score_schedule(
        self,
        schedule: Schedule,
        prefer_online: bool,
        prefer_morning: bool,
        avoid_friday: bool,
    ) -> float:
        """
        Calculate a quality score for a schedule.

        Score is 0-100, with 100 being perfect.
        """
        score = 50.0  # Base score

        # Online preference
        if prefer_online:
            online_count = sum(1 for c in schedule.courses if c.is_online)
            score += (online_count / len(schedule.courses)) * 20

        # Morning preference (classes before 12pm)
        if prefer_morning:
            morning_count = 0
            total_meetings = 0
            for course in schedule.courses:
                for meeting in course.meeting_times:
                    if meeting.start_time and meeting.start_time.hour < 12:
                        morning_count += 1
                    total_meetings += 1
            if total_meetings > 0:
                score += (morning_count / total_meetings) * 15

        # Avoid Friday
        if avoid_friday:
            friday_count = 0
            for course in schedule.courses:
                for meeting in course.meeting_times:
                    if "F" in meeting.days:
                        friday_count += 1
            score -= friday_count * 5

        # Compactness bonus (fewer gaps between classes)
        weekly = schedule.get_weekly_schedule()
        for day_schedule in weekly.values():
            if len(day_schedule) > 1:
                # Sort by start time
                sorted_times = sorted(
                    [m for m in day_schedule if m.start_time],
                    key=lambda m: m.start_time,
                )
                # Check for gaps
                for i in range(len(sorted_times) - 1):
                    gap = (
                        sorted_times[i + 1].start_time.hour * 60
                        + sorted_times[i + 1].start_time.minute
                    ) - (
                        sorted_times[i].end_time.hour * 60 + sorted_times[i].end_time.minute
                    )
                    # Penalize gaps > 60 minutes
                    if gap > 60:
                        score -= 2

        # Ensure score is in valid range
        return max(0.0, min(100.0, score))


# Preserve v1 style function for backward compatibility
def make_schedule(
    courses_list: List[List[Course]], term: str, max_schedules: int = 100
) -> List[Schedule]:
    """
    Generate conflict-free schedules (v1-style function).

    Args:
        courses_list: List of course option lists
        term: Term code
        max_schedules: Maximum schedules to generate

    Returns:
        List of valid schedules
    """
    builder = ScheduleBuilder(term=term)
    for course_options in courses_list:
        builder.add_course_options(course_options)
    return builder.generate_schedules(max_results=max_schedules)
