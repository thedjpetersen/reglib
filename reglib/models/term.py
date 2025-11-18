"""
Term model representing an academic term.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Term(BaseModel):
    """Represents an academic term."""

    code: str = Field(description="Term code (e.g., 202501)")
    description: str = Field(description="Human-readable term (e.g., Winter 2025)")
    start_date: date = Field(description="Term start date")
    end_date: date = Field(description="Term end date")
    is_open_for_registration: bool = Field(
        default=False, description="Whether registration is open"
    )
    registration_start: Optional[date] = Field(
        None, description="Registration start date"
    )

    @property
    def year(self) -> int:
        """Get the year from the term code."""
        return int(self.code[:4])

    @property
    def quarter_code(self) -> str:
        """Get the quarter code (01-04)."""
        return self.code[4:]

    @property
    def quarter_name(self) -> str:
        """Get the quarter name."""
        quarter_map = {
            "01": "Fall",
            "02": "Winter",
            "03": "Spring",
            "04": "Summer",
        }
        return quarter_map.get(self.quarter_code, "Unknown")

    @property
    def short_name(self) -> str:
        """Get short name (e.g., F25, W25)."""
        quarter_abbrev = {"01": "F", "02": "W", "03": "Sp", "04": "Su"}
        year_short = str(self.year)[2:]
        return f"{quarter_abbrev.get(self.quarter_code, '')}{year_short}"

    def __str__(self) -> str:
        """String representation."""
        return self.description

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"Term(code={self.code!r}, description={self.description!r})"

    class Config:
        json_schema_extra = {
            "example": {
                "code": "202501",
                "description": "Fall 2025",
                "start_date": "2025-09-24",
                "end_date": "2025-12-05",
                "is_open_for_registration": True,
                "registration_start": "2025-05-01",
            }
        }
