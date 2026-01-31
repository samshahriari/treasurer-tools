"""Validation functions for expense and invoice data."""

from typing import Optional

import pandas as pd

from models import ExpenseRow, InvoiceRow


def validate_expense(row: pd.Series) -> Optional[ExpenseRow]:
    """
    Validate and convert an expense row to Pydantic model.

    Args:
        row: DataFrame row (Series)

    Returns:
        ExpenseRow object if valid, None otherwise
    """
    try:
        expense = ExpenseRow(**row.to_dict())
        if not expense.Godkänt:
            return None
        return expense
    except Exception as e:
        print(f"Warning: Failed to validate expense row - {e}")
        return None


def validate_invoice(row: pd.Series) -> Optional[InvoiceRow]:
    """
    Validate and convert an invoice row to Pydantic model.

    Args:
        row: DataFrame row (Series)

    Returns:
        InvoiceRow object if valid, None otherwise
    """
    try:
        invoice = InvoiceRow(**row.to_dict())
        if not invoice.Godkänt:
            return None
        return invoice
    except Exception as e:
        print(f"Warning: Failed to validate invoice row - {e}")
        return None
