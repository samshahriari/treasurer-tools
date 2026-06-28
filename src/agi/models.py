"""Pydantic models for Skatteverket AGI XML generation."""

import re
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Employee(BaseModel):
    """Model representing an employee payroll record for Skatteverket AGI."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    namn: str = Field(alias="Namn")
    epost: str = Field(alias="Epost")
    personnummer: str = Field(alias="Personnummer")
    clearingnummer: str = Field(alias="Clearingnummer")
    kontonummer: str = Field(alias="Kontonummer")
    antal_timmar: float = Field(alias="Antal timmar")
    timlon: float = Field(alias="Timlön")
    skatteprocent: float = Field(alias="Skatteprocent")
    total_lon: float = Field(alias="Total lön")
    lon_utbetald: float = Field(alias="Lön som ska betalas ut")
    skatt: float = Field(alias="Skatt")
    verksamhet: str = Field(alias="Verksamhet")

    @field_validator("personnummer", mode="before")
    @classmethod
    def clean_personnummer(cls, v) -> str:
        """Clean personal number from spaces, hyphens, and validate."""
        cleaned = re.sub(r"\D", "", str(v))
        if len(cleaned) == 10:
            # Prefix 10-digit personnummer with 19 or 20
            # If the birth year is > 26 (current year), it's probably 19XX, else 20XX
            yy = int(cleaned[:2])
            prefix = "20" if yy <= 26 else "19"
            cleaned = prefix + cleaned
        elif len(cleaned) != 12:
            raise ValueError(
                f"Invalid Swedish personnummer: {v}. Must be 10 or 12 digits."
            )
        return cleaned

    @field_validator("clearingnummer", "kontonummer", mode="before")
    @classmethod
    def convert_to_str(cls, v) -> str:
        """Convert account and clearing numbers to clean strings."""
        if v is None:
            return ""
        s = str(v).strip()
        if s.endswith(".0"):
            s = s[:-2]
        return s

    @property
    def birth_year(self) -> int:
        """Extract birth year from 12-digit personnummer."""
        return int(self.personnummer[:4])

    def calculate_employer_contribution(self, year: int = 2026) -> int:
        """
        Calculate the employer contribution for this employee in SEK.

        Swedish standard rates for 2026 (including temporary youth nedsättning):
        - Born 1957 or earlier (age 68 or older in 2026): 10.21% (retirement pension contribution only)
        - Born 2003 to 2007 (age 19–23 in 2026):
          - 20.81% on compensation up to 25,000 SEK per calendar month
          - 31.42% on compensation exceeding 25,000 SEK
        - All others (standard rate): 31.42%
        """
        birth_year = self.birth_year

        if year == 2026 and 2003 <= birth_year <= 2007:
            # Youth reduction (born 2003-2007): 20.81% up to 25k, 31.42% above
            if self.total_lon <= 25000:
                contribution = self.total_lon * 0.2081
            else:
                contribution = (25000 * 0.2081) + ((self.total_lon - 25000) * 0.3142)
        else:
            # Standard rate: 31.42%
            contribution = self.total_lon * 0.3142

        # Round to nearest integer SEK as expected by Skatteverket
        return int(round(contribution))
