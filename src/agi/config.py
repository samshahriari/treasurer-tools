"""Configuration management for AGI XML generation."""

import os
from datetime import datetime
from dotenv import load_dotenv


class AGIConfig:
    """Configuration loaded from environment variables or defaults for AGI."""

    def __init__(self):
        load_dotenv()

        org_env = (os.getenv("ORG_NUMBER") or "").replace("-", "").strip()
        self.org_number = f"16{org_env}" if org_env else "161234567890"
        org_name_env = (os.getenv("ORG_NAMN") or "").strip()
        self.org_namn = org_name_env if org_name_env else "Orgnamn"

        # Dynamically default reporting period to the previous month (standard filing period)
        now = datetime.now()
        year = now.year
        month = now.month - 1
        if month == 0:
            month = 12
            year -= 1
        self.reporting_period = f"{year}{month:02d}"

        # Unified Contact Person details for both Sender (Avsändare) and Employer (Blankettgemensamt)
        # Handle empty/blank environment variables gracefully
        contact_name = (os.getenv("AGI_CONTACT_NAME") or "").strip()
        self.contact_name = contact_name if contact_name else "Anna Andersson"

        contact_phone = (os.getenv("AGI_CONTACT_PHONE") or "").strip()
        self.contact_phone = contact_phone if contact_phone else "087654321"

        contact_email = (os.getenv("AGI_CONTACT_EMAIL") or "").strip()
        self.contact_email = (
            contact_email if contact_email else "anna.andersson@foretaget.se"
        )

        contact_subj = (os.getenv("AGI_CONTACT_SUBJECT_AREA") or "").strip()
        self.contact_subject_area = contact_subj if contact_subj else "Lön"

        # Both sender and employer identities and contact details are unified
        self.sender_id = self.org_number
        self.sender_name = self.contact_name
        self.sender_phone = self.contact_phone
        self.sender_email = self.contact_email
