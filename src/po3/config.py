"""Configuration management for PO3 file generation."""

import os

from dotenv import load_dotenv


class Config:
    """Configuration loaded from environment variables."""

    def __init__(self):
        load_dotenv()
        self.org_number = self._get_required("ORG_NUMBER")
        self.account_number = self._get_required("ACCOUNT_NUMBER")
        self.use_gsheets = os.getenv("USE_GSHEETS", "FALSE").upper() == "TRUE"

        if self.use_gsheets:
            self.sheet_name = self._get_required("SHEET_NAME")
            self.expense_gsheet_id = self._get_required("EXPENSE_GSHEET_ID")
            self.invoice_gsheet_id = self._get_required("INVOICE_GSHEET_ID")
        else:
            self.expense_path = self._get_required("EXPENSE_PATH")
            self.invoice_path = self._get_required("INVOICE_PATH")

    @staticmethod
    def _get_required(key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' not set")
        return value
