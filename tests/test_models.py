"""
Tests for core data models.
"""

from datetime import date, time

import pytest

from reglib.models import Course, MeetingTime, Schedule, Term


class TestMeetingTime:
    """Tests for MeetingTime model."""

    def test_meeting_time_creation(self):
        """Test creating a meeting time."""
        mt = MeetingTime(
            days=["M", "W", "F"],
            start_time=time(10, 0),
            end_time=time(10, 50),
            location="KEARNEY 212",
            instructor="Smith, Jane",
        )
        assert mt.days == ["M", "W", "F"]
        assert mt.start_time == time(10, 0)
        assert mt.location == "KEARNEY 212"

    def test_meeting_time_overlap_same_days(self):
        """Test overlap detection for same days."""
        mt1 = MeetingTime(
            days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
        )
        mt2 = MeetingTime(
            days=["M", "W", "F"], start_time=time(10, 30), end_time=time(11, 20)
        )
        assert mt1.overlaps_with(mt2)
        assert mt2.overlaps_with(mt1)

    def test_meeting_time_no_overlap_different_days(self):
        """Test no overlap for different days."""
        mt1 = MeetingTime(days=["M", "W"], start_time=time(10, 0), end_time=time(10, 50))
        mt2 = MeetingTime(days=["T", "R"], start_time=time(10, 0), end_time=time(10, 50))
        assert not mt1.overlaps_with(mt2)

    def test_meeting_time_no_overlap_different_times(self):
        """Test no overlap for different times."""
        mt1 = MeetingTime(
            days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
        )
        mt2 = MeetingTime(
            days=["M", "W", "F"], start_time=time(11, 0), end_time=time(11, 50)
        )
        assert not mt1.overlaps_with(mt2)

    def test_meeting_time_tba(self):
        """Test TBA meeting times don't overlap."""
        mt1 = MeetingTime(days=["M", "W", "F"])
        mt2 = MeetingTime(
            days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
        )
        assert not mt1.overlaps_with(mt2)


class TestCourse:
    """Tests for Course model."""

    def test_course_creation(self):
        """Test creating a course."""
        course = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Introduction to Computer Science I",
            credits=4.0,
            seats_total=100,
            seats_available=25,
        )
        assert course.crn == "12345"
        assert course.course_code == "CS 161"
        assert course.full_name == "CS 161 - Introduction to Computer Science I"

    def test_course_is_full(self):
        """Test course full detection."""
        course = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course",
            credits=4.0,
            seats_available=0,
        )
        assert course.is_full

    def test_course_conflicts_same_crn(self):
        """Test courses with same CRN conflict."""
        course1 = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course",
            credits=4.0,
        )
        course2 = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course",
            credits=4.0,
        )
        assert course1.conflicts_with(course2)

    def test_course_conflicts_overlapping_times(self):
        """Test courses with overlapping times conflict."""
        course1 = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course 1",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
                )
            ],
        )
        course2 = Course(
            crn="67890",
            term="202501",
            subject="MTH",
            course_number="111",
            section="001",
            title="Test Course 2",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["M", "W", "F"], start_time=time(10, 30), end_time=time(11, 20)
                )
            ],
        )
        assert course1.conflicts_with(course2)

    def test_course_no_conflict(self):
        """Test courses with no overlap don't conflict."""
        course1 = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course 1",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
                )
            ],
        )
        course2 = Course(
            crn="67890",
            term="202501",
            subject="MTH",
            course_number="111",
            section="001",
            title="Test Course 2",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["T", "R"], start_time=time(14, 0), end_time=time(15, 20)
                )
            ],
        )
        assert not course1.conflicts_with(course2)


class TestSchedule:
    """Tests for Schedule model."""

    def test_schedule_creation(self):
        """Test creating a schedule."""
        schedule = Schedule(term="202501")
        assert schedule.term == "202501"
        assert schedule.course_count == 0
        assert schedule.total_credits == 0.0

    def test_schedule_add_course(self):
        """Test adding courses to schedule."""
        schedule = Schedule(term="202501")
        course = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course",
            credits=4.0,
        )
        assert schedule.add_course(course)
        assert schedule.course_count == 1
        assert schedule.total_credits == 4.0

    def test_schedule_conflict_detection(self):
        """Test schedule conflict detection."""
        schedule = Schedule(term="202501")
        course1 = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course 1",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
                )
            ],
        )
        course2 = Course(
            crn="67890",
            term="202501",
            subject="MTH",
            course_number="111",
            section="001",
            title="Test Course 2",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["M", "W", "F"], start_time=time(10, 30), end_time=time(11, 20)
                )
            ],
        )

        schedule.add_course(course1)
        result = schedule.add_course(course2)  # Should fail due to conflict

        assert not result
        assert schedule.course_count == 1

    def test_schedule_remove_course(self):
        """Test removing course from schedule."""
        schedule = Schedule(term="202501")
        course = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course",
            credits=4.0,
        )
        schedule.add_course(course)
        assert schedule.remove_course("12345")
        assert schedule.course_count == 0

    def test_schedule_weekly_schedule(self):
        """Test weekly schedule generation."""
        schedule = Schedule(term="202501")
        course = Course(
            crn="12345",
            term="202501",
            subject="CS",
            course_number="161",
            section="001",
            title="Test Course",
            credits=4.0,
            meeting_times=[
                MeetingTime(
                    days=["M", "W", "F"], start_time=time(10, 0), end_time=time(10, 50)
                )
            ],
        )
        schedule.add_course(course)
        weekly = schedule.get_weekly_schedule()

        assert len(weekly["M"]) == 1
        assert len(weekly["W"]) == 1
        assert len(weekly["F"]) == 1
        assert len(weekly["T"]) == 0


class TestTerm:
    """Tests for Term model."""

    def test_term_creation(self):
        """Test creating a term."""
        term = Term(
            code="202501",
            description="Fall 2025",
            start_date=date(2025, 9, 24),
            end_date=date(2025, 12, 5),
        )
        assert term.code == "202501"
        assert term.year == 2025
        assert term.quarter_code == "01"
        assert term.quarter_name == "Fall"

    def test_term_short_name(self):
        """Test term short name generation."""
        term = Term(
            code="202501",
            description="Fall 2025",
            start_date=date(2025, 9, 24),
            end_date=date(2025, 12, 5),
        )
        assert term.short_name == "F25"

    def test_term_quarters(self):
        """Test all quarter names."""
        quarters = [
            ("202501", "Fall", "F25"),
            ("202502", "Winter", "W25"),
            ("202503", "Spring", "Sp25"),
            ("202504", "Summer", "Su25"),
        ]

        for code, name, short in quarters:
            term = Term(
                code=code,
                description=f"{name} 2025",
                start_date=date(2025, 1, 1),
                end_date=date(2025, 3, 31),
            )
            assert term.quarter_name == name
            assert term.short_name == short
