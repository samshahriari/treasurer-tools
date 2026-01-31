"""Utility functions for formatting and data transformation."""

import datetime

from constants import (
    CURRENCY,
    EXPENSE_CODE,
    RECORD_TYPE_BENEFICIARY,
    RECORD_TYPE_HEADER,
    RECORD_TYPE_NOTE,
    RECORD_TYPE_PAYMENT,
    RECORD_TYPE_TRAILER,
)


def format_amount(amount: float, length: int = 13) -> str:
    """
    Format amount as öre (1 SEK = 100 öre), zero-padded.

    Args:
        amount: Amount in SEK
        length: Total length of output string

    Returns:
        Zero-padded string representation of amount in öre
    """
    return str(round(amount * 100)).zfill(length)


def create_note(activity: str, description: str, name: str) -> str:
    """Create standardized note from transaction details."""
    return f"{activity} {description} {name}"


def create_message(activity: str, description: str) -> str:
    """Create standardized message from transaction details."""
    return f"{activity} {description}"


# ============================================================================
# PO3 FORMAT GENERATORS
# ============================================================================


def generate_start_line(org_number: str, account_number: str) -> str:
    """
    Generate MH00 header line for PO3 file.

    Args:
        org_number: Organization number
        account_number: Account number

    Returns:
        Formatted header line
    """
    return (
        RECORD_TYPE_HEADER
        + " " * 8
        + org_number
        + " " * 12
        + account_number.ljust(10)
        + CURRENCY
        + " " * 6
        + CURRENCY
        + " " * 24
    )


def generate_end_line(number_of_rows: int, total_cost: float) -> str:
    """
    Generate MT00 trailer line for PO3 file.

    Args:
        number_of_rows: Total number of payment records
        total_cost: Total amount in SEK

    Returns:
        Formatted trailer line
    """
    return (
        RECORD_TYPE_TRAILER
        + " " * 25
        + str(number_of_rows).zfill(7)
        + format_amount(total_cost, 15)
        + " " * 29
    )


def generate_pi00_expense(
    clearing_number: int,
    account_number: int,
    amount: float,
    message: str
) -> str:
    """
    Generate PI00 payment line for bank account expense.

    Args:
        clearing_number: Bank clearing number
        account_number: Bank account number
        amount: Amount in SEK
        message: Payment message

    Returns:
        Formatted payment line
    """
    return (
        RECORD_TYPE_PAYMENT
        + EXPENSE_CODE
        + str(clearing_number).ljust(5)
        + str(account_number).ljust(11)
        + "  "
        + datetime.datetime.now().strftime("%Y%m%d")
        + format_amount(amount)
        + message.ljust(12)[:12]
        + " " * 23
    )


def generate_pi00_giro(
    account_number: int,
    amount: float,
    ocr: str,
    giro_code: str
) -> str:
    """
    Generate PI00 payment line for giro payment (Plusgiro/Bankgiro).

    Args:
        account_number: Giro account number
        amount: Amount in SEK
        ocr: OCR number or message
        giro_code: "00" for Plusgiro, "05" for Bankgiro

    Returns:
        Formatted payment line
    """
    return (
        RECORD_TYPE_PAYMENT
        + giro_code
        + " " * 5
        + str(account_number).ljust(11)
        + "  "
        + datetime.datetime.now().strftime("%Y%m%d")
        + format_amount(amount)
        + str(ocr).ljust(25)
        + " " * 10
    )


def generate_ba00(note: str) -> str:
    """
    Generate BA00 note line.

    Args:
        note: Note text

    Returns:
        Formatted note line
    """
    return (
        RECORD_TYPE_NOTE
        + note.ljust(18)[:18]
        + " " * 9
        + note.ljust(35)[:35]
        + " " * 14
    )


def generate_be01(recipient: str) -> str:
    """
    Generate BE01 beneficiary line.

    Args:
        recipient: Recipient name

    Returns:
        Formatted beneficiary line
    """
    return RECORD_TYPE_BENEFICIARY + " " * 18 + recipient.ljust(58)
