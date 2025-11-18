# OSU Course Planner - Implementation Roadmap

**Project:** reglib → OSU Course Planner v2.0
**Goal:** Transform deprecated Banner 8 scraper into modern course planning tool
**Timeline:** 4-6 weeks (development) + ongoing maintenance

## Vision

Build a **student-first course planning tool** that helps OSU students:
- 📚 Explore course offerings across multiple terms
- 📅 Build conflict-free schedules automatically
- 🎯 Plan their academic path toward graduation
- 📊 Analyze course availability patterns
- 📤 Export schedules to calendars and planners

**What makes this different:**
- ✅ Focus on **planning**, not registration automation
- ✅ Uses **public data** only (no authentication hacks)
- ✅ **Respectful** of OSU systems (rate limiting, caching)
- ✅ **Open source** and community-driven
- ✅ **Modern Python** (3.8+, type hints, async support)

## Project Phases

### Phase 0: Preparation ✅ (Completed)

- [x] Analyze current codebase
- [x] Research OSU systems and APIs
- [x] Document compatibility issues
- [x] Modernize Python 2 → Python 3
- [x] Design new architecture
- [x] Create roadmap

**Deliverables:**
- ✅ COMPATIBILITY_ANALYSIS.md
- ✅ ARCHITECTURE_V2.md
- ✅ ROADMAP.md (this document)

### Phase 1: Foundation (Week 1-2)

**Goal:** Set up project infrastructure and core data models

#### Tasks:

1. **Project Setup**
   - [ ] Create new branch: `feature/v2-course-planner`
   - [ ] Update `pyproject.toml` with new dependencies
   - [ ] Set up development environment (venv, pre-commit hooks)
   - [ ] Configure testing framework (pytest, coverage)
   - [ ] Set up linting (ruff, mypy)

2. **Dependencies:**
   ```toml
   dependencies = [
       "requests>=2.31.0",
       "lxml>=4.9.0",
       "python-dateutil>=2.8.0",
       "pydantic>=2.0.0",  # Data validation
       "tenacity>=8.0.0",  # Retry logic
       "rich>=13.0.0",     # Beautiful CLI output
       "typer>=0.9.0",     # CLI framework
   ]

   [project.optional-dependencies]
   export = [
       "icalendar>=5.0.0",
       "reportlab>=4.0.0",  # PDF generation
   ]
   dev = [
       "pytest>=7.4.0",
       "pytest-cov>=4.1.0",
       "pytest-asyncio>=0.21.0",
       "mypy>=1.5.0",
       "ruff>=0.1.0",
   ]
   ```

3. **Core Data Models**
   - [ ] Implement `Course` model with Pydantic
   - [ ] Implement `MeetingTime` model
   - [ ] Implement `Schedule` model
   - [ ] Implement `Term` model
   - [ ] Add conflict detection to `Course.conflicts_with()`
   - [ ] Write unit tests for models

4. **Utilities (Port from v1)**
   - [ ] Port `time_conflict()` function
   - [ ] Port `format_course()` function
   - [ ] Port `format_term()` functions
   - [ ] Modernize with type hints
   - [ ] Add comprehensive tests

**Deliverables:**
- New module structure in `reglib/`
- Working data models with tests
- 90%+ test coverage on models

**Success Criteria:**
```python
# This should work:
from reglib.models import Course, MeetingTime, Schedule

course1 = Course(
    crn='12345',
    subject='CS',
    course_number='161',
    title='Introduction to Computer Science I',
    credits=4.0,
    meeting_times=[...]
)

course2 = Course(...)

assert not course1.conflicts_with(course2)
```

### Phase 2: Data Access Layer (Week 2-3)

**Goal:** Implement robust data fetching from OSU sources

#### Option A: Official API (If Available)

1. **API Client**
   - [ ] Request API key from developer.oregonstate.edu
   - [ ] Implement `OSUAPIClient` class
   - [ ] Add authentication handling
   - [ ] Implement rate limiting (60 req/min)
   - [ ] Add retry logic with exponential backoff
   - [ ] Implement pagination handling

2. **API Endpoints**
   - [ ] `get_terms()` - Fetch available terms
   - [ ] `search_classes()` - Search courses
   - [ ] `get_subjects()` - Get subject list
   - [ ] Parse responses into models

#### Option B: Ecampus Scraper (Fallback/Primary if no API)

1. **Scraper Implementation**
   - [ ] Implement `EcampusScraper` class
   - [ ] Add respectful request handling
     - User-Agent: 'OSU-CoursePlanner/2.0 (+github.com/...)'
     - Rate limit: 1 req/second
     - Respect robots.txt
   - [ ] Parse subject listing page
   - [ ] Parse course detail pages
   - [ ] Parse term selection
   - [ ] Error handling for missing/changed HTML

2. **Data Normalization**
   - [ ] Create `DataAdapter` interface
   - [ ] Implement API → Model adapter
   - [ ] Implement Scraper → Model adapter
   - [ ] Ensure consistent output format

3. **Caching Layer**
   - [ ] Implement SQLite cache
   - [ ] Cache course data (TTL: 1 hour)
   - [ ] Cache term data (TTL: 24 hours)
   - [ ] Implement cache invalidation
   - [ ] Add cache statistics

**Deliverables:**
- Working data fetcher (API or scraper)
- Caching system
- Integration tests

**Success Criteria:**
```python
from reglib.api import get_client

client = get_client()  # Auto-detects API/scraper
terms = client.get_terms(open_only=True)
courses = client.search_classes(
    term=terms[0].code,
    subject='CS'
)

assert len(courses) > 0
assert isinstance(courses[0], Course)
```

### Phase 3: Schedule Building (Week 3-4)

**Goal:** Implement core planning features

1. **Conflict Detection**
   - [ ] Implement time overlap detection
   - [ ] Handle TBA times gracefully
   - [ ] Detect same-course conflicts
   - [ ] Add conflict reporting

2. **Schedule Generator**
   - [ ] Port `make_schedule()` logic
   - [ ] Implement constraint system
   - [ ] Add preference handling
   - [ ] Implement schedule scoring
   - [ ] Optimize algorithm performance

3. **Constraints System**
   ```python
   # Time blocks (work, other commitments)
   builder.add_time_block(
       days=['M', 'W', 'F'],
       start='08:00',
       end='10:00'
   )

   # Preferences
   builder.add_preferences(
       prefer_online=True,
       prefer_morning=False,
       avoid_friday=True,
       max_courses_per_day=3,
       lunch_break=True  # 12:00-13:00
   )
   ```

4. **Schedule Ranking**
   - [ ] Implement scoring algorithm
   - [ ] Factors: compactness, preferences, instructor ratings
   - [ ] Customizable weights

**Deliverables:**
- Working schedule builder
- Constraint system
- Ranking algorithm

**Success Criteria:**
```python
from reglib import ScheduleBuilder

builder = ScheduleBuilder(term='202501')
builder.add_course_preference('CS 361')
builder.add_course_preference('CS 362')
builder.add_course_preference('MTH 231')

schedules = builder.generate_schedules(max_results=10)

assert len(schedules) > 0
assert all(not s.has_conflicts for s in schedules)
assert schedules[0].score >= schedules[-1].score  # Sorted
```

### Phase 4: Advanced Features (Week 4-5)

1. **Multi-Term Planning**
   - [ ] Implement degree requirement parser
   - [ ] Create prerequisite tracker
   - [ ] Build term-by-term planner
   - [ ] Suggest course sequences

2. **Course Analysis**
   - [ ] Historical availability tracking
   - [ ] Find alternative courses
   - [ ] Seat availability predictions
   - [ ] Popular time slot analysis

3. **Export Functionality**
   - [ ] iCalendar (.ics) export
   - [ ] PDF schedule export
   - [ ] JSON export
   - [ ] Plain text export
   - [ ] Markdown export

**Success Criteria:**
```python
schedule.export_ical('fall-2025.ics')  # Import to Google Calendar
schedule.export_pdf('schedule.pdf')     # Print-friendly
```

### Phase 5: User Interface (Week 5-6)

1. **Command Line Interface**
   ```bash
   # Search courses
   osu-planner search --term 202501 --subject CS

   # Build schedule
   osu-planner build --term 202501 \
       --courses "CS 361" "CS 362" "MTH 231" \
       --avoid-friday \
       --prefer-online

   # Export
   osu-planner export schedule.json --format ical

   # Multi-term plan
   osu-planner plan --major "Computer Science BS" \
       --completed courses.txt \
       --starting 202503 \
       --quarters 4
   ```

2. **Interactive Mode**
   ```bash
   osu-planner interactive
   > search CS 361
   > add to cart
   > build schedule
   > export to calendar
   ```

3. **Web UI (Future/Optional)**
   - Simple Flask/FastAPI app
   - Vue.js/React frontend
   - Visual schedule builder
   - Drag-and-drop interface

**Deliverables:**
- Fully functional CLI
- Interactive mode
- Documentation

### Phase 6: Testing & Documentation (Week 6)

1. **Testing**
   - [ ] Unit tests (90%+ coverage)
   - [ ] Integration tests
   - [ ] End-to-end tests
   - [ ] Performance tests
   - [ ] Load tests (caching, rate limiting)

2. **Documentation**
   - [ ] API reference (Sphinx)
   - [ ] User guide
   - [ ] Tutorial (Jupyter notebook)
   - [ ] Contributing guide
   - [ ] FAQ

3. **Examples**
   ```
   examples/
   ├── 01_basic_search.py
   ├── 02_build_schedule.py
   ├── 03_multi_term_plan.py
   ├── 04_export_formats.py
   └── tutorial.ipynb
   ```

4. **README Update**
   - Clear feature list
   - Quick start guide
   - Installation instructions
   - Screenshots/examples
   - Link to documentation

**Success Criteria:**
- All tests passing
- Documentation complete
- Examples working
- README compelling

### Phase 7: Release & Community (Ongoing)

1. **Beta Release (v2.0.0-beta.1)**
   - [ ] Tag release on GitHub
   - [ ] Publish to PyPI (test.pypi.org first)
   - [ ] Share with OSU subreddit
   - [ ] Gather feedback

2. **Public Release (v2.0.0)**
   - [ ] Address beta feedback
   - [ ] Final testing
   - [ ] Publish to PyPI
   - [ ] Create release announcement
   - [ ] Share with OSU community

3. **Community Building**
   - [ ] Set up GitHub Discussions
   - [ ] Create contribution guidelines
   - [ ] Label good first issues
   - [ ] Respond to issues/PRs
   - [ ] Regular releases

## Migration Strategy

### For Existing Users

**Option 1: Side-by-Side**
```bash
# Install v2 alongside v1
pip install osu-course-planner  # New package name

# Old code still works
import reglib  # v1 (deprecated)

# New code
import osu_planner  # v2
```

**Option 2: Breaking Change**
```bash
# Upgrade to v2
pip install --upgrade reglib

# Update imports
from reglib import ScheduleBuilder  # New API
```

### Deprecation Plan

1. **Immediate (Nov 2025):**
   - Add deprecation warnings to v1 code
   - Update README with v2 timeline

2. **Q1 2026:**
   - Release v2.0.0
   - Maintain v1 security fixes only

3. **Q3 2026:**
   - End v1 support
   - Archive v1 branch

## Success Metrics

### Technical Metrics
- **Performance:** Search < 2s, Schedule generation < 5s
- **Reliability:** 99% uptime (caching helps)
- **Cache Hit Rate:** > 80%
- **Test Coverage:** > 90%

### User Metrics
- **Adoption:** 100+ users in first month
- **Satisfaction:** Positive feedback
- **Issues:** < 5 open bugs at any time
- **Community:** 10+ contributors

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API access denied | High | Use Ecampus scraper |
| HTML structure changes | Medium | Version checks, alerts |
| Rate limiting issues | Low | Aggressive caching |
| Legal/ToS concerns | High | Only public data, clear attribution |

## Open Questions

1. **API Access:**
   - Can we get API keys from developer.oregonstate.edu?
   - What are the rate limits?
   - Is it free for students?

2. **Data Freshness:**
   - How often do course offerings change?
   - What's acceptable cache TTL?

3. **Community:**
   - Where should we host discussions? (GitHub, Discord, Slack?)
   - How to engage with OSU IT?

## Resources Needed

### Development
- **Time:** 80-120 hours (1-2 months part-time)
- **Skills:** Python, web scraping, API design
- **Tools:** GitHub, PyPI, documentation hosting

### Infrastructure
- **Hosting:** GitHub Pages (docs), PyPI (package)
- **CI/CD:** GitHub Actions
- **Testing:** pytest, coverage.io

### Community
- **Support:** GitHub Issues/Discussions
- **Documentation:** ReadTheDocs or GitHub Pages

## Next Steps

**This Week:**
1. Request API access from OSU
2. Set up development environment
3. Implement core models
4. Port time conflict logic

**This Month:**
5. Complete data access layer
6. Implement schedule builder
7. Beta release to small group

**Next Month:**
8. Add advanced features
9. Build CLI
10. Public release

---

**Ready to start?** Let's begin with Phase 1!

```bash
# Create development branch
git checkout -b feature/v2-course-planner

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run initial tests
pytest
```

Let's build something amazing for the OSU community! 🦫
