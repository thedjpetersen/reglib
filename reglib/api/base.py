"""
Base API client interface.
"""

from abc import ABC, abstractmethod
from typing import List

from reglib.models import Course, Term


class APIClient(ABC):
    """Abstract base class for API clients."""

    @abstractmethod
    def get_terms(self, open_only: bool = True) -> List[Term]:
        """
        Get available terms.

        Args:
            open_only: If True, only return terms open for registration

        Returns:
            List of Term objects
        """
        pass

    @abstractmethod
    def search_courses(
        self,
        term: str,
        subject: str | None = None,
        course_number: str | None = None,
        query: str | None = None,
    ) -> List[Course]:
        """
        Search for courses.

        Args:
            term: Term code (e.g., '202501')
            subject: Subject code (e.g., 'CS')
            course_number: Course number (e.g., '161')
            query: Full-text search query

        Returns:
            List of Course objects
        """
        pass

    @abstractmethod
    def get_subjects(self, term: str) -> List[str]:
        """
        Get list of available subjects for a term.

        Args:
            term: Term code

        Returns:
            List of subject codes
        """
        pass
