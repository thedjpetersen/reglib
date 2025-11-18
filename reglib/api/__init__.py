"""
API clients for fetching course data from OSU systems.
"""

from .base import APIClient
from .ecampus import EcampusScraper

__all__ = ["APIClient", "EcampusScraper"]


def get_client(api_key: str | None = None) -> APIClient:
    """
    Get an API client (auto-detects available method).

    Args:
        api_key: Optional API key for OSU Developer Portal

    Returns:
        An instance of APIClient (either OSU API or Ecampus scraper)
    """
    # For now, return Ecampus scraper
    # TODO: Implement OSU API client when keys are available
    return EcampusScraper()
