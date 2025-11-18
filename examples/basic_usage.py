"""
Basic usage example for OSU Course Planner.

This demonstrates the core functionality of the library.
"""

from datetime import date, time

from reglib.api import get_client
from reglib.models import Course, MeetingTime, Schedule, Term
from reglib.planning import ScheduleBuilder

# ============================================================================
# Example 1: Working with Course Models
# ============================================================================

print("=" * 70)
print("Example 1: Creating Course Objects")
print("=" * 70)

# Create a course
cs161 = Course(
    crn="12345",
    term="202501",
    subject="CS",
    course_number="161",
    section="001",
    title="Introduction to Computer Science I",
    credits=4.0,
    seats_total=100,
    seats_available=25,
    meeting_times=[
        MeetingTime(
            days=["M", "W", "F"],
            start_time=time(10, 0),
            end_time=time(10, 50),
            location="KEARNEY 212",
            instructor="Smith, Jane",
        )
    ],
)

print(f"Course: {cs161.full_name}")
print(f"CRN: {cs161.crn}")
print(f"Credits: {cs161.credits}")
print(f"Seats Available: {cs161.seats_available}/{cs161.seats_total}")
print(f"Is Full: {cs161.is_full}")

# ============================================================================
# Example 2: Conflict Detection
# ============================================================================

print("\n" + "=" * 70)
print("Example 2: Detecting Time Conflicts")
print("=" * 70)

mth111 = Course(
    crn="67890",
    term="202501",
    subject="MTH",
    course_number="111",
    section="001",
    title="College Algebra",
    credits=4.0,
    meeting_times=[
        MeetingTime(
            days=["M", "W", "F"],
            start_time=time(10, 30),
            end_time=time(11, 20),
        )
    ],
)

conflicts = cs161.conflicts_with(mth111)
print(f"\nCS 161 (MWF 10:00-10:50)")
print(f"MTH 111 (MWF 10:30-11:20)")
print(f"Conflicts: {conflicts}")

# ============================================================================
# Example 3: Building a Schedule
# ============================================================================

print("\n" + "=" * 70)
print("Example 3: Building a Schedule")
print("=" * 70)

schedule = Schedule(term="202501")

# Create non-conflicting course
cs162 = Course(
    crn="11111",
    term="202501",
    subject="CS",
    course_number="162",
    section="001",
    title="Introduction to Computer Science II",
    credits=4.0,
    meeting_times=[
        MeetingTime(
            days=["T", "R"],
            start_time=time(14, 0),
            end_time=time(15, 20),
        )
    ],
)

schedule.add_course(cs161)
schedule.add_course(cs162)

print(f"\nSchedule Summary:")
print(f"  Courses: {schedule.course_count}")
print(f"  Total Credits: {schedule.total_credits}")
print(f"  Has Conflicts: {schedule.has_conflicts}")

print(f"\nWeekly Schedule:")
weekly = schedule.get_weekly_schedule()
for day, meetings in weekly.items():
    if meetings:
        print(f"  {day}: {len(meetings)} class(es)")


# ============================================================================
# Example 4: Using the Schedule Builder
# ============================================================================

print("\n" + "=" * 70)
print("Example 4: Schedule Builder (Conceptual)")
print("=" * 70)

# In a real scenario, you would fetch course sections from the API
# builder = ScheduleBuilder(term='202501')

# # Add different sections of each desired course
# builder.add_course_options([cs161_sec1, cs161_sec2, cs161_sec3])
# builder.add_course_options([cs162_sec1, cs162_sec2])
# builder.add_course_options([mth111_sec1, mth111_sec2])

# # Generate schedules
# schedules = builder.generate_schedules(
#     max_results=10,
#     prefer_online=False,
#     avoid_friday=True
# )

# # Print top schedules
# for i, sched in enumerate(schedules[:3]):
#     print(f"\nSchedule {i+1} (Score: {sched.score:.1f})")
#     for course in sched.courses:
#         print(f"  - {course.full_name}")

print("\n(Schedule builder requires actual course data)")
print("Run with API access to see full functionality")


# ============================================================================
# Example 5: Working with Terms
# ============================================================================

print("\n" + "=" * 70)
print("Example 5: Term Information")
print("=" * 70)

term = Term(
    code="202501",
    description="Fall 2025",
    start_date=date(2025, 9, 24),
    end_date=date(2025, 12, 5),
    is_open_for_registration=True,
)

print(f"Term: {term.description}")
print(f"Code: {term.code}")
print(f"Short Name: {term.short_name}")
print(f"Quarter: {term.quarter_name}")
print(f"Dates: {term.start_date} to {term.end_date}")
print(f"Registration Open: {term.is_open_for_registration}")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
print("\nFor more examples, see:")
print("  - examples/schedule_builder.py")
print("  - examples/api_usage.py")
print("  - Documentation: https://github.com/thedjpetersen/reglib")
