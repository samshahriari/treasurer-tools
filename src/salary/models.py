"""Pydantic models for Skatteverket AGI XML generation."""

import re

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Employee(BaseModel):
    """Model representing an employee payroll record for Skatteverket AGI."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = Field(alias="Namn")
    email: str = Field(alias="Epost")
    personnummer: str = Field(alias="Personnummer")
    clearing_number: str = Field(alias="Clearingnummer")
    account_number: str = Field(alias="Kontonummer")
    salary_rows: list["SalaryRow"] = Field(alias="Löneuppgifter")

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

    @field_validator("clearing_number", "account_number", mode="before")
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

    @property
    def total_salary(self) -> float:
        """Calculate the total salary for this employee."""
        return sum(row.total_salary for row in self.salary_rows)

    def calculate_employer_contribution(self, year: int = 2026) -> int:
        """
        Calculate the employer contribution for this employee in SEK.

        Swedish standard rates for 2026 (including temporary youth nedsättning):
        - Born 2003 to 2007 (age 19–23 in 2026):
          - 20.81% on compensation up to 25,000 SEK per calendar month
          - 31.42% on compensation exceeding 25,000 SEK
        - All others (standard rate): 31.42%
        """
        birth_year = self.birth_year

        if year != 2026:
            raise ValueError(
                f"Employer contribution calculation is only implemented for the year 2026, not {year}."
            )

        if year == 2026 and 2003 <= birth_year <= 2007:
            # Youth reduction (born 2003-2007): 20.81% up to 25k, 31.42% above

            if self.total_salary <= 25000:
                contribution = self.total_salary * 0.2081
            else:
                contribution = (25000 * 0.2081) + ((self.total_salary - 25000) * 0.3142)
        else:
            # Standard rate: 31.42%
            contribution = self.total_salary * 0.3142

        # Round to nearest integer SEK as expected by Skatteverket
        return int(round(contribution))


class SalaryRow(BaseModel):
    number_of_hours: float = Field(alias="Antal timmar")
    hourly_wage: float = Field(alias="Timlön")
    tax_percentage: float = Field(alias="Skatteprocent")
    total_salary: float = Field(alias="Total lön")
    salary_to_be_paid: float = Field(alias="Lön som ska betalas ut")
    tax: float = Field(alias="Skatt")
    verksamhet: str = Field(alias="Verksamhet")


def load_employees_from_csv(csv_path: str) -> list[Employee]:
    """Load and validate employees from the salary CSV file."""
    # Read the CSV with pandas
    df = pd.read_csv(csv_path)

    employee_info_cols = [
        "Namn",
        "Epost",
        "Personnummer",
        "Clearingnummer",
        "Kontonummer",
    ]
    salary_cols = [
        "Antal timmar",
        "Timlön",
        "Skatteprocent",
        "Total lön",
        "Lön som ska betalas ut",
        "Skatt",
        "Verksamhet",
    ]

    grouped = (
        df.groupby(employee_info_cols)[salary_cols]
        .apply(lambda g: g.to_dict(orient="records"))
        .reset_index(name="Löneuppgifter")
    )

    # 3. Convert records directly into Pydantic models
    return [Employee.model_validate(record) for record in grouped.to_dict("records")]
