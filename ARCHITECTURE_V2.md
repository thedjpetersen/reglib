# OSU Course Planning System - Architecture Design

**Date:** November 18, 2025
**Project:** reglib v2.0 - Course Planning Library
**Status:** 🔄 Design Phase

## Executive Summary

Transform `reglib` from a deprecated Banner 8 scraper into a modern **course planning and scheduling tool** using publicly available OSU course data. Focus on helping students plan their schedules before registration opens, not attempting authenticated registration operations.

## Design Goals

### Primary Goals
1. ✅ Help students explore available courses
2. ✅ Build conflict-free schedule combinations
3. ✅ Plan multi-term academic paths
4. ✅ Analyze course offerings and availability patterns
5. ✅ Export schedules in multiple formats

### Non-Goals
❌ Automated registration (requires authentication)
❌ Grade access (private student data)
❌ Transcript retrieval (private student data)
❌ Bypassing authentication systems

## Data Sources

### Option 1: OSU Public APIs (Preferred)

**Developer Portal:** https://developer.oregonstate.edu

**Available APIs** (from GitHub specifications):
- **Class Search API:** `/class-search?term={code}&subject={dept}&courseNumber={num}`
- **Terms API:** `/terms` and `/terms/open`
- **Course Subjects API:** Subject/department listings

**Authentication:**
- Appears to require API key from developer portal
- Free for students/developers (needs verification)
- Rate limiting likely in place

**Benefits:**
- Structured JSON data
- Official, maintained by OSU
- Pagination support
- Comprehensive course details

**Implementation:**
```python
import requests

class OSUCoursesAPI:
    BASE_URL = "https://api.oregonstate.edu/v1"  # TBD - needs verification

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    def get_terms(self, open_only=True):
        """Get available academic terms"""
        endpoint = '/terms/open' if open_only else '/terms'
        return self._get(endpoint)

    def search_classes(self, term, subject=None, course_number=None,
                      query=None, page_size=25):
        """Search for classes in a specific term"""
        params = {'term': term, 'page[size]': page_size}
        if subject:
            params['subject'] = subject
        if course_number:
            params['courseNumber'] = course_number
        if query:
            params['q'] = query
        return self._get('/class-search', params=params)
```

### Option 2: Ecampus Public Catalog (Fallback)

**Base URL:** https://ecampus.oregonstate.edu/soc/ecatalog/

**Available Pages:**
- `/subjectcourses.htm?term=all` - All subjects and courses
- `/esubjects.htm?termcode={term}` - Subjects by term
- `/ecatalog/` - Term selection

**Benefits:**
- No authentication required
- Public data
- Covers all courses (Corvallis + Ecampus)

**Challenges:**
- HTML parsing (structure may change)
- Less structured than API
- Requires respectful scraping (rate limiting, caching)

**Implementation:**
```python
import requests
from lxml import html
from typing import List, Dict
import time

class EcampusCatalogScraper:
    BASE_URL = "https://ecampus.oregonstate.edu/soc/ecatalog"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'OSU-CoursePlanner/2.0'
        self._rate_limit = 1.0  # seconds between requests
        self._last_request = 0

    def _rate_limited_get(self, url):
        """Respect rate limits"""
        elapsed = time.time() - self._last_request
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)
        response = self.session.get(url)
        self._last_request = time.time()
        return response

    def get_subjects(self, term='all'):
        """Get list of subjects/departments"""
        url = f'{self.BASE_URL}/esubjects.htm?termcode={term}'
        response = self._rate_limited_get(url)
        # Parse HTML and extract subjects
        return self._parse_subjects(response.text)
```

### Option 3: OSU Scheduler Tool Integration

**URL:** https://registrar.oregonstate.edu/scheduler

**Features:**
- Official OSU schedule builder
- Time conflict detection
- Cart/basket management
- Exports to registration

**Approach:**
- Complement rather than replace
- Our library can generate schedules offline
- Export format compatible with Scheduler import (if available)

## Core Features Design

### 1. Course Search & Discovery

```python
from reglib import CoursePlanner

planner = CoursePlanner()  # or CoursePlanner(api_key='...')

# Search for courses
courses = planner.search_courses(
    term='202501',  # Winter 2025
    subject='CS',
    course_number='161',
    include_full=False,  # exclude full courses
    campus=['Corvallis', 'Online']
)

# Get all open CS courses
cs_courses = planner.get_courses_by_subject(
    term='202501',
    subject='CS',
    level='upper'  # 300-400 level
)

# Full-text search
data_science = planner.search(
    term='202501',
    query='data science machine learning'
)
```

### 2. Schedule Building (Keep Existing Logic!)

The existing schedule conflict detection is excellent - modernize it:

```python
from reglib import ScheduleBuilder

builder = ScheduleBuilder(term='202501')

# Add desired courses
builder.add_course_preference('CS 361')
builder.add_course_preference('CS 362')
builder.add_course_preference('MTH 231')

# Set time constraints
builder.add_time_block(
    days=['M', 'W', 'F'],
    start='08:00',
    end='09:00',
    reason='Work schedule'
)

# Generate all valid schedule combinations
schedules = builder.generate_schedules(
    max_schedules=50,
    prefer_online=True,
    prefer_morning=False,
    avoid_friday=True
)

# Rank schedules
for schedule in schedules[:5]:
    print(f"Schedule {schedule.rank}")
    print(f"  Rating: {schedule.score}/100")
    print(f"  Courses: {schedule.course_count}")
    print(f"  Credits: {schedule.total_credits}")
    print(f"  Conflicts: {schedule.conflicts}")
    for course in schedule.courses:
        print(f"    - {course}")
```

### 3. Multi-Term Planning

```python
from reglib import DegreePlanner

planner = DegreePlanner()

# Load degree requirements (from catalog or manual)
planner.load_requirements('computer-science-bs.yaml')

# Plan next 4 quarters
plan = planner.plan_quarters(
    starting_term='202503',  # Spring 2025
    num_quarters=4,
    completed_courses=['CS 161', 'CS 162', 'MTH 111', 'MTH 112'],
    credits_per_term=16
)

for term_plan in plan:
    print(f"\n{term_plan.term_name}:")
    for course in term_plan.recommended_courses:
        print(f"  {course.code} - {course.title}")
    print(f"  Prerequisites met: {term_plan.prereqs_satisfied}")
```

### 4. Course Analysis

```python
from reglib import CourseAnalyzer

analyzer = CourseAnalyzer()

# Historical availability
history = analyzer.get_offering_history(
    subject='CS',
    number='344',
    num_terms=8
)

print(f"CS 344 offered: {history.availability_percentage}% of terms")
print(f"Average seats: {history.avg_seats}")
print(f"Typically offered: {history.common_terms}")  # e.g., ["Fall", "Spring"]

# Find alternatives
alternatives = analyzer.find_similar_courses(
    course='CS 361',
    criteria=['same_subject', 'same_level', 'similar_credits']
)
```

### 5. Export & Integration

```python
# Export to various formats
schedule.export_ical('my-schedule.ics')  # Import to Google Calendar
schedule.export_pdf('my-schedule.pdf')   # Print-friendly
schedule.export_json('my-schedule.json') # Backup/share

# Generate registration checklist
checklist = schedule.generate_registration_plan(
    registration_time='2025-05-15 08:00:00'
)
print(checklist.markdown())
```

## Data Models

### Course Model

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import time, date

@dataclass
class MeetingTime:
    days: List[str]  # ['M', 'W', 'F']
    start_time: time
    end_time: time
    location: str
    instructor: Optional[str] = None

@dataclass
class Course:
    crn: str
    term: str
    subject: str
    course_number: str
    section: str
    title: str
    credits: float

    # Enrollment
    seats_total: int
    seats_available: int
    seats_waitlist: int

    # Schedule
    meeting_times: List[MeetingTime]

    # Details
    description: Optional[str] = None
    prerequisites: Optional[str] = None
    instructors: List[str] = None
    campus: str = 'Corvallis'
    delivery_mode: str = 'In-Person'  # or 'Online', 'Hybrid'

    def conflicts_with(self, other: 'Course') -> bool:
        """Check if this course has time conflicts with another"""
        for my_time in self.meeting_times:
            for other_time in other.meeting_times:
                if self._times_overlap(my_time, other_time):
                    return True
        return False

    @staticmethod
    def _times_overlap(time1: MeetingTime, time2: MeetingTime) -> bool:
        """Check if two meeting times overlap"""
        # Check if they share any days
        shared_days = set(time1.days) & set(time2.days)
        if not shared_days:
            return False

        # Check time overlap
        return (time1.start_time < time2.end_time and
                time1.end_time > time2.start_time)

@dataclass
class Schedule:
    term: str
    courses: List[Course]
    score: float = 0.0

    @property
    def total_credits(self) -> float:
        return sum(c.credits for c in self.courses)

    @property
    def has_conflicts(self) -> bool:
        for i, course1 in enumerate(self.courses):
            for course2 in self.courses[i+1:]:
                if course1.conflicts_with(course2):
                    return True
        return False

    def get_weekly_schedule(self) -> Dict[str, List[MeetingTime]]:
        """Organize schedule by day of week"""
        schedule = {'M': [], 'T': [], 'W': [], 'R': [], 'F': []}
        for course in self.courses:
            for meeting in course.meeting_times:
                for day in meeting.days:
                    schedule[day].append(meeting)
        # Sort by start time
        for day in schedule:
            schedule[day].sort(key=lambda m: m.start_time)
        return schedule
```

### Term Model

```python
@dataclass
class Term:
    code: str  # '202501'
    description: str  # 'Winter 2025'
    start_date: date
    end_date: date
    is_open_for_registration: bool = False

    @property
    def year(self) -> int:
        return int(self.code[:4])

    @property
    def quarter(self) -> str:
        quarter_map = {'01': 'Fall', '02': 'Winter',
                      '03': 'Spring', '04': 'Summer'}
        return quarter_map.get(self.code[4:], 'Unknown')
```

## Implementation Plan

### Phase 1: Foundation (Week 1)
- [x] Research and design (completed)
- [ ] Set up new module structure
- [ ] Implement data models (Course, Term, Schedule)
- [ ] Create base API client with error handling
- [ ] Implement caching layer (reduce API calls)

### Phase 2: Data Access (Week 2)
- [ ] Implement OSU API client (if keys available)
- [ ] Implement Ecampus scraper (fallback)
- [ ] Add data normalization (API + scraper → common format)
- [ ] Implement local caching (SQLite or JSON)
- [ ] Add rate limiting and retry logic

### Phase 3: Core Features (Week 3)
- [ ] Port and modernize schedule conflict detection
- [ ] Implement schedule builder/generator
- [ ] Add constraint system (time blocks, preferences)
- [ ] Implement schedule scoring/ranking algorithm
- [ ] Add course search and filtering

### Phase 4: Advanced Features (Week 4)
- [ ] Multi-term planning
- [ ] Course analysis and recommendations
- [ ] Export functionality (iCal, PDF, JSON)
- [ ] CLI interface
- [ ] Web UI (optional, future)

### Phase 5: Documentation & Testing (Week 5)
- [ ] Unit tests (pytest)
- [ ] Integration tests
- [ ] API documentation
- [ ] Usage examples
- [ ] Tutorial notebook (Jupyter)

## File Structure

```
reglib/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── client.py          # Base API client
│   ├── osu_api.py         # OSU official API
│   └── ecampus.py         # Ecampus scraper
├── models/
│   ├── __init__.py
│   ├── course.py
│   ├── schedule.py
│   ├── term.py
│   └── constraints.py
├── planning/
│   ├── __init__.py
│   ├── schedule_builder.py
│   ├── conflict_detector.py
│   ├── degree_planner.py
│   └── analyzer.py
├── export/
│   ├── __init__.py
│   ├── ical.py
│   ├── pdf.py
│   └── json_export.py
├── cache/
│   ├── __init__.py
│   └── local_cache.py
└── utils/
    ├── __init__.py
    ├── time_utils.py
    └── validators.py

examples/
├── basic_search.py
├── schedule_builder.py
├── multi_term_plan.py
└── course_analysis.ipynb

tests/
├── test_models.py
├── test_api.py
├── test_planning.py
└── test_exports.py

docs/
├── api_usage.md
├── schedule_building.md
├── examples.md
└── faq.md
```

## Migration from Old Code

### Keep and Modernize:
- ✅ `utilities/utilities.py` - Time conflict detection logic
- ✅ `schedule/schedule_class.py` - Schedule representation
- ✅ `utilities/make_schedule.py` - Combinatorial schedule generation

### Deprecated (Remove):
- ❌ All authentication code
- ❌ Banner-specific scrapers
- ❌ transcript/grade access
- ❌ Registration/add-drop functionality

### Transform:
- 🔄 Course search → Use API/Ecampus
- 🔄 Schedule building → Keep logic, new data source
- 🔄 Term handling → Use new Term API

## API Access Strategy

### Getting API Access:

1. **For Students:**
   ```bash
   # Visit developer portal
   open https://developer.oregonstate.edu

   # Sign in with ONID
   # Create application
   # Request API key for academic APIs
   ```

2. **For Development:**
   ```python
   # Option 1: API key from environment
   export OSU_API_KEY='your-key-here'

   # Option 2: Config file
   # ~/.osu/config.yaml
   api_key: your-key-here
   cache_enabled: true
   cache_ttl: 3600

   # Option 3: Fallback to scraping
   planner = CoursePlanner()  # Auto-detects available methods
   ```

3. **Rate Limiting:**
   ```python
   # Respect API limits
   MAX_REQUESTS_PER_MINUTE = 60
   CACHE_TTL = 3600  # 1 hour for course data

   # Use exponential backoff
   from tenacity import retry, wait_exponential

   @retry(wait=wait_exponential(multiplier=1, min=2, max=10))
   def api_call(...):
       ...
   ```

## Success Metrics

1. **Functionality:**
   - Successfully fetch course data for current term
   - Generate conflict-free schedules
   - Export to standard formats

2. **Performance:**
   - API response < 2 seconds
   - Schedule generation < 5 seconds for 5 courses
   - Cache hit rate > 80%

3. **Reliability:**
   - Graceful fallback when API unavailable
   - Clear error messages
   - No rate limit violations

4. **Usability:**
   - Simple CLI: `reglib search --term 202501 --subject CS`
   - Python API: `planner.search_courses(term='202501', subject='CS')`
   - Documentation with examples

## Ethical Guidelines

1. **Respect OSU Resources:**
   - Use official APIs when available
   - Implement rate limiting
   - Cache aggressively
   - Scrape only public data

2. **Terms of Service:**
   - Read and comply with OSU's acceptable use policy
   - Don't bypass authentication
   - Don't scrape private student data
   - Don't automate registration

3. **Attribution:**
   - Credit OSU for data
   - Open source the tool
   - Share with OSU community

## Next Steps

1. **Immediate:**
   - [ ] Request API access from developer.oregonstate.edu
   - [ ] Test Ecampus scraping on sample pages
   - [ ] Set up new project structure

2. **This Week:**
   - [ ] Implement data models
   - [ ] Create API client skeleton
   - [ ] Port time conflict logic

3. **This Month:**
   - [ ] Complete Phase 1-3
   - [ ] Beta release to a few users
   - [ ] Gather feedback

Would you like me to start implementing any specific component?
