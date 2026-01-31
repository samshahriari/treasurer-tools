"""Pydantic models for expense and invoice data."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _parse_boolean(value):
    """Parse boolean from various formats (string, bool, int)."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


class ExpenseRow(BaseModel):
    """Model for expense data rows from CSV."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    Godkänt: bool
    Utbetalt: bool
    Belopp: float
    Verksamhet: str
    Clearingnummer: int
    Kontonummer: int
    Ditt_namn: str = Field(alias="Ditt namn")
    Kort_beskrivning_av_köp: str = Field(alias="Kort beskrivning av köp")

    @field_validator("Godkänt", "Utbetalt", mode="before")
    @classmethod
    def parse_booleans(cls, v):
        """Parse boolean fields from various formats."""
        return _parse_boolean(v)


class InvoiceRow(BaseModel):
    """Model for invoice data rows from CSV."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    Godkänt: bool
    Utbetalt: bool
    Belopp: float
    Verksamhet: str
    Mottagarkontotyp: Literal["Plusgiro", "Bankgiro"]
    Mottagarkontonummer: int
    OCR_meddelande: str = Field(alias="OCR/meddelande")
    Ditt_namn: str = Field(alias="Ditt namn")
    Kort_beskrivning_av_köp: str = Field(alias="Kort beskrivning av köp")
    Mottagare_namn: str = Field(alias="Mottagare (namn)")

    @field_validator("Godkänt", "Utbetalt", mode="before")
    @classmethod
    def parse_booleans(cls, v):
        """Parse boolean fields from various formats."""
        return _parse_boolean(v)

    @field_validator("Belopp", mode="before")
    @classmethod
    def parse_amount(cls, v):
        """Parse amount field as float."""
        if isinstance(v, (int, float)):
            return float(v)
        return float(str(v).replace(",", "."))
