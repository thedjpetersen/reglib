"""
Ecampus catalog scraper for public course data.
"""

import time
from typing import List

import requests
from lxml import html

from reglib.models import Course, Term

from .base import APIClient


class EcampusScraper(APIClient):
    """Scraper for OSU Ecampus public catalog."""

    BASE_URL = "https://ecampus.oregonstate.edu/soc/ecatalog"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers[
            "User-Agent"
        ] = "OSU-CoursePlanner/2.0 (+https://github.com/thedjpetersen/reglib)"
        self._rate_limit = 1.0  # seconds between requests
        self._last_request = 0.0

    def _rate_limited_get(self, url: str) -> requests.Response:
        """Make a rate-limited GET request."""
        elapsed = time.time() - self._last_request
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)

        response = self.session.get(url, timeout=30)
        self._last_request = time.time()
        response.raise_for_status()
        return response

    def get_terms(self, open_only: bool = True) -> List[Term]:
        """
        Get available terms from Ecampus.

        Note: This is a placeholder implementation.
        Full implementation would scrape the term selection page.
        """
        # TODO: Implement actual scraping
        # For now, return current term as example
        from datetime import date

        return [
            Term(
                code="202501",
                description="Fall 2025",
                start_date=date(2025, 9, 24),
                end_date=date(2025, 12, 5),
                is_open_for_registration=True,
            ),
            Term(
                code="202502",
                description="Winter 2026",
                start_date=date(2026, 1, 6),
                end_date=date(2026, 3, 20),
                is_open_for_registration=False,
            ),
        ]

    def search_courses(
        self,
        term: str,
        subject: str | None = None,
        course_number: str | None = None,
        query: str | None = None,
    ) -> List[Course]:
        """
        Search for courses in Ecampus catalog.

        Note: This is a placeholder implementation.
        Full implementation would scrape course pages and parse HTML.
        """
        # TODO: Implement actual scraping
        # This would involve:
        # 1. Navigate to subject page for the term
        # 2. Parse HTML tables with course data
        # 3. Extract CRN, times, instructors, etc.
        # 4. Create Course objects from parsed data

        # Return empty list for now
        return []

    def get_subjects(self, term: str) -> List[str]:
        """
        Get list of subjects for a term.

        Note: This is a placeholder implementation.
        """
        # TODO: Implement actual scraping
        # Common OSU subjects as placeholder
        return [
            "ANTH",
            "ART",
            "BA",
            "BI",
            "CH",
            "COMM",
            "CS",
            "ECE",
            "ECON",
            "ENGR",
            "FW",
            "GEOG",
            "H",
            "HSTS",
            "MATH",
            "MTH",
            "MUS",
            "PH",
            "PSY",
            "SOIL",
            "STAT",
            "WR",
        ]
