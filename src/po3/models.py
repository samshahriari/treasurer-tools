"""Pydantic models for expense and invoice data."""

from datetime import date, datetime
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
    kvitto_url: str | None = Field(default=None, alias="Ladda upp bild på kvitto")
    Ditt_namn: str = Field(alias="Ditt namn")
    Kort_beskrivning_av_köp: str = Field(alias="Kort beskrivning av köp")

    @field_validator("Godkänt", "Utbetalt", mode="before")
    @classmethod
    def parse_booleans(cls, v):
        """Parse boolean fields from various formats."""
        return _parse_boolean(v)

    @field_validator("kvitto_url", mode="before")
    @classmethod
    def normalize_kvitto_url(cls, v):
        """Treat blank attachment cells as missing values."""
        if v is None:
            return None
        value = str(v).strip()
        return value or None


class InvoiceRow(BaseModel):
    """Model for invoice data rows from CSV."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    Godkänt: bool
    Utbetalt: bool
    Belopp: float
    Verksamhet: str
    faktura_url: str | None = Field(default=None, alias="Ladda upp fakturan")
    Mottagarkontotyp: Literal["Plusgiro", "Bankgiro"]
    Mottagarkontonummer: int
    OCR_meddelande: str = Field(alias="OCR/meddelande")
    Ditt_namn: str = Field(alias="Ditt namn")
    Kort_beskrivning_av_köp: str = Field(alias="Kort beskrivning av köp")
    Mottagare_namn: str = Field(alias="Mottagare (namn)")
    Payment_date: date = Field(alias="Sista betalningsdatum")

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

    @field_validator("OCR_meddelande", mode="before")
    @classmethod
    def make_str(cls, v):
        """Convert OCR_meddelande to string."""
        return str(v)

    @field_validator("faktura_url", mode="before")
    @classmethod
    def normalize_faktura_url(cls, v):
        """Treat blank attachment cells as missing values."""
        if v is None:
            return None
        value = str(v).strip()
        return value or None

    @field_validator("Payment_date", mode="before")
    @classmethod
    def parse_payment_date(cls, v):
        """Parse payment date from string."""
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            return date.fromisoformat(v.strip())
        raise ValueError(f"Invalid payment date value: {v!r}")
