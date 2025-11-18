# OSU Course Planner

**A course planning and schedule building tool for Oregon State University students**

> **⚠️ Important Notice:** Version 1.x of this library (targeting Banner 8) is **no longer functional** with current OSU systems. See [COMPATIBILITY_ANALYSIS.md](COMPATIBILITY_ANALYSIS.md) for details.
>
> **🚀 Version 2.0 is in development!** We're rebuilding this as a modern course planning tool. See [ROADMAP.md](ROADMAP.md) for the plan.

---

## Project Status

| Version | Status | Description |
|---------|--------|-------------|
| **v1.x** | ❌ Deprecated | Banner 8 scraper (2011-2019) - **No longer works** |
| **v2.0** | 🚧 In Development | Modern course planner using public APIs |

### What Happened to v1?

Oregon State upgraded from Banner 8 to Banner 9 in 2019, and the authentication system changed completely in 2025 (PIN system eliminated). The old scraping approach no longer works and cannot be fixed. See [COMPATIBILITY_ANALYSIS.md](COMPATIBILITY_ANALYSIS.md) for a detailed technical analysis.

### What's Coming in v2?

A **complete rewrite** focused on course planning, not registration automation:

**Core Features:**
- 📚 **Course Search** - Explore OSU course offerings
- 📅 **Schedule Builder** - Generate conflict-free schedules automatically
- 🎯 **Multi-Term Planning** - Plan your path to graduation
- 📊 **Course Analysis** - Analyze availability patterns and trends
- 📤 **Export** - iCal, PDF, JSON formats for your schedules

**Key Improvements:**
- ✅ Modern Python 3.8+ (type hints, async support)
- ✅ Uses official OSU APIs where available
- ✅ Respectful of university resources (caching, rate limiting)
- ✅ No authentication hacks - public data only
- ✅ Beautiful CLI with rich output
- ✅ Comprehensive documentation and examples

See [ARCHITECTURE_V2.md](ARCHITECTURE_V2.md) for the complete design.

---

## Quick Start (v2.0 - Coming Soon)

```bash
# Install (when released)
pip install osu-course-planner

# Search for courses
osu-planner search --term 202501 --subject CS

# Build a schedule
osu-planner build --term 202501 \
    --courses "CS 361" "CS 362" "MTH 231" \
    --prefer-online \
    --avoid-friday

# Export to calendar
osu-planner export schedule.json --format ical
```

**Python API:**
```python
from osu_planner import ScheduleBuilder

# Build conflict-free schedules
builder = ScheduleBuilder(term='202501')
builder.add_course_preference('CS 361')
builder.add_course_preference('CS 362')
builder.add_course_preference('MTH 231')

# Generate schedules ranked by your preferences
schedules = builder.generate_schedules(
    max_results=10,
    prefer_online=True,
    avoid_friday=True
)

# Export top schedule
schedules[0].export_ical('my-schedule.ics')
```

---

## Development Status

We're currently in the design phase. Want to help? See [ROADMAP.md](ROADMAP.md) for our implementation plan.

**Current Phase:** Phase 1 - Foundation
**Progress:** Design complete, implementation starting
**ETA:** Beta release in 4-6 weeks

### Contributing

We welcome contributions! This is an open-source project built by OSU students for OSU students.

**How to help:**
1. ⭐ Star this repo to show support
2. 🐛 Report issues or suggest features
3. 💻 Contribute code (see [ROADMAP.md](ROADMAP.md) for tasks)
4. 📖 Improve documentation
5. 🧪 Test beta releases and provide feedback

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines (coming soon).

---

## Documentation

- **[COMPATIBILITY_ANALYSIS.md](COMPATIBILITY_ANALYSIS.md)** - Why v1 no longer works
- **[ARCHITECTURE_V2.md](ARCHITECTURE_V2.md)** - Technical design for v2
- **[ROADMAP.md](ROADMAP.md)** - Implementation plan and timeline

---

## For Historical Reference: v1.x Documentation

<details>
<summary>Click to expand original v1 documentation (deprecated)</summary>

### OSU-Registration Library (v1.x - DEPRECATED)

***⚠️ This module no longer works with current OSU systems.***

Library to work as API to Oregon State's registration system (Banner 8, 2011-2019). This documentation is preserved for historical reference only.

#### Installation (v1 - DO NOT USE)

```bash
git clone git@github.com:thedjpetersen/OSU-Registration.git
cd OSU-Registration
sudo python setup.py install
```

#### Usage (v1 - DO NOT USE)

```python
import reglib

# This no longer works - authentication changed
registration_class = reglib.infosu(sid, pin)

# These features are no longer functional:
# - registration_class.transcript
# - registration_class.schedule
# - registration_class.class_search()
# - registration_class.add_class()
# - registration_class.make_schedule()
```

#### What Still Works from v1?

The **schedule conflict detection logic** was excellent and is being preserved in v2:

```python
# v1 code (preserved in v2)
from reglib.utilities.utilities import time_conflict

# Check if two time slots conflict
conflicts = time_conflict(
    ['13:00', '13:50'],  # 1:00 PM - 1:50 PM
    ['13:30', '14:20']   # 1:30 PM - 2:20 PM
)
# Returns: True (30-minute overlap)
```

The `make_schedule()` combinatorial algorithm for generating conflict-free schedules is also being modernized and improved in v2.

</details>

---

## Current OSU Resources

**Official OSU Tools:**
- **MyOregonState:** https://my.oregonstate.edu - Official student portal
- **Class Search:** https://classes.oregonstate.edu - Browse courses
- **Schedule Planner:** https://registrar.oregonstate.edu/scheduler - Official schedule builder
- **Ecampus Catalog:** https://ecampus.oregonstate.edu/soc - Online course listings

**For Developers:**
- **OSU Developer Portal:** https://developer.oregonstate.edu - API access
- **Course API Design:** https://github.com/osu-mist/courses-api-design - OpenAPI specs

---

## Timeline

- **2011-2015:** Original library developed for Banner 8
- **January 2019:** OSU upgraded to Banner 9 (breaking changes)
- **October 2020:** MyOSU → my.oregonstate.edu migration
- **Fall 2025:** PIN system eliminated, registration process overhauled
- **November 2025:** Modernization project started, v2 designed
- **Q1 2026 (Planned):** v2.0 beta release
- **Q2 2026 (Planned):** v2.0 public release

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Credits

**Original Author (v1):** David Petersen (@thedjpetersen)
**v2 Modernization:** Community-driven rewrite

**Special Thanks:**
- Oregon State University for providing public course data
- The OSU student community
- All contributors to v1 and v2

---

## Questions?

- **For v2 development:** Open a GitHub Issue or Discussion
- **For current OSU registration:** Visit https://my.oregonstate.edu or contact OSU Registrar
- **For API access:** Contact https://developer.oregonstate.edu

---

**Built with 🧡 by OSU students, for OSU students** 🦫

