"""
PO3 File Generator for Bankgirot
Generates payment files in PO3 format for processing expenses and invoices.
"""

import datetime
import os
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

# ============================================================================
# CONSTANTS
# ============================================================================

# Giro type codes
PLUSGIRO_CODE = "00"
BANKGIRO_CODE = "05"
EXPENSE_CODE = "09"

# File format constants
CURRENCY = "SEK"
LINE_LENGTH = 80
RECORD_TYPE_HEADER = "MH00"
RECORD_TYPE_TRAILER = "MT00"
RECORD_TYPE_PAYMENT = "PI00"
RECORD_TYPE_NOTE = "BA00"
RECORD_TYPE_BENEFICIARY = "BE01"

# Column names
COL_APPROVED = "Godkänt"
COL_PAID = "Utbetalt"
COL_AMOUNT = "Belopp"
COL_NAME = "Ditt namn"
COL_ACTIVITY = "Verksamhet"
COL_DESCRIPTION = "Kort beskrivning av köp"


# ============================================================================
# CONFIGURATION
# ============================================================================

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


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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


def normalize_boolean_column(series: pd.Series) -> pd.Series:
    """
    Normalize boolean column from various formats (string "true", bool, etc.).

    Args:
        series: Pandas Series with boolean-like values

    Returns:
        Series with normalized boolean values
    """
    return series.map(
        lambda x: str(x).strip().lower() == "true" if isinstance(x, str) else bool(x)
    )


def create_note(activity: str, description: str, name: str) -> str:
    """Create standardized note from transaction details."""
    return f"{activity} {description} {name}"


def create_message(activity: str, description: str) -> str:
    """Create standardized message from transaction details."""
    return f"{activity} {description}"


# ============================================================================
# PO3 FORMAT GENERATORS
# ============================================================================

def generate_start_line(config: Config) -> str:
    """
    Generate MH00 header line for PO3 file.

    Args:
        config: Configuration object with org number and account number

    Returns:
        Formatted header line
    """
    return (
        RECORD_TYPE_HEADER
        + " " * 8
        + config.org_number
        + " " * 12
        + config.account_number.ljust(10)
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


# ============================================================================
# VALIDATION
# ============================================================================

def validate_row(row: pd.Series) -> bool:
    """
    Validate if a row should be processed.

    Args:
        row: DataFrame row (Series)

    Returns:
        True if row is valid and approved
    """
    if not row[COL_APPROVED]:
        return False

    # Additional validation checks can be added here
    required_fields = [COL_AMOUNT, COL_NAME, COL_ACTIVITY, COL_DESCRIPTION]
    for field in required_fields:
        if pd.isna(row.get(field)) or str(row.get(field)).strip() == "":
            print(f"Warning: Missing required field '{field}' in row")
            return False

    return True


# ============================================================================
# PAYMENT LINE GENERATORS
# ============================================================================

def generate_lines_for_expense(row: pd.Series) -> Optional[list[str]]:
    """
    Generate PO3 lines for a single expense (bank account payment).

    Args:
        row: DataFrame row with expense data

    Returns:
        List of formatted lines or None if validation fails
    """
    if not validate_row(row):
        return None

    lines = []
    message = create_message(row[COL_ACTIVITY], row[COL_DESCRIPTION])

    lines.append(generate_pi00_expense(
        row["Clearingnummer"],
        row["Kontonummer"],
        row[COL_AMOUNT],
        message
    ))

    note = create_note(row[COL_ACTIVITY], row[COL_DESCRIPTION], row[COL_NAME])
    lines.append(generate_ba00(note))
    lines.append(generate_be01(row[COL_NAME]))

    return lines


def generate_lines_for_invoice(row: pd.Series) -> Optional[list[str]]:
    """
    Generate PO3 lines for a single invoice (giro payment).

    Args:
        row: DataFrame row with invoice data

    Returns:
        List of formatted lines or None if validation fails
    """
    if not validate_row(row):
        return None

    lines = []
    giro_code = PLUSGIRO_CODE if row["Mottagarkontotyp"] == "Plusgiro" else BANKGIRO_CODE

    lines.append(generate_pi00_giro(
        row["Mottagarkontonummer"],
        row[COL_AMOUNT],
        row["OCR/meddelande"],
        giro_code
    ))

    note = create_note(row[COL_ACTIVITY], row[COL_DESCRIPTION], row[COL_NAME])
    lines.append(generate_ba00(note))
    lines.append(generate_be01(row["Mottagare (namn)"]))

    return lines


# ============================================================================
# DATA LOADING
# ============================================================================

def load_data_from_gsheets(config: Config) -> tuple[pd.DataFrame, pd.DataFrame, object, object]:
    """
    Load data from Google Sheets.

    Args:
        config: Configuration object

    Returns:
        Tuple of (expenses_df, invoices_df, expense_worksheet, invoice_worksheet)
    """
    import gspread

    gc = gspread.oauth()
    sheet = gc.open(config.sheet_name)

    ws_expenses = sheet.get_worksheet_by_id(int(config.expense_gsheet_id))
    expenses = pd.DataFrame(ws_expenses.get_all_records())

    ws_invoices = sheet.get_worksheet_by_id(int(config.invoice_gsheet_id))
    invoices = pd.DataFrame(ws_invoices.get_all_records())

    print("Data loaded from Google Sheets.")
    return expenses, invoices, ws_expenses, ws_invoices


def load_data_from_csv(config: Config) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load data from CSV files.

    Args:
        config: Configuration object

    Returns:
        Tuple of (expenses_df, invoices_df)
    """
    expenses = pd.read_csv(config.expense_path)
    invoices = pd.read_csv(config.invoice_path)
    print("Data loaded from CSV files.")
    return expenses, invoices


def normalize_dataframes(expenses: pd.DataFrame, invoices: pd.DataFrame) -> None:
    """
    Normalize boolean columns in-place.

    Args:
        expenses: Expenses DataFrame
        invoices: Invoices DataFrame
    """
    for df in [expenses, invoices]:
        df[COL_APPROVED] = normalize_boolean_column(df[COL_APPROVED])
        df[COL_PAID] = normalize_boolean_column(df[COL_PAID])


# ============================================================================
# FILE WRITING
# ============================================================================

def write_po3_file(file_name: str, lines: list[str]) -> None:
    """
    Write PO3 file with proper encoding.

    Args:
        file_name: Output file name
        lines: List of formatted lines
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_payments(
    expenses: pd.DataFrame,
    invoices: pd.DataFrame,
    config: Config,
    ws_expenses=None,
    ws_invoices=None
) -> tuple[list[str], int, float]:
    """
    Process all unpaid expenses and invoices.

    Args:
        expenses: DataFrame with expenses
        invoices: DataFrame with invoices
        config: Configuration object
        ws_expenses: Optional Google Sheets worksheet for expenses
        ws_invoices: Optional Google Sheets worksheet for invoices

    Returns:
        Tuple of (output_lines, number_of_rows, total_cost)
    """
    output_lines = []
    number_of_rows = 0
    total_cost = 0.0

    # Process expenses
    for i, row in expenses[~expenses[COL_PAID]].iterrows():
        payment_lines = generate_lines_for_expense(row)
        if payment_lines:
            output_lines.extend(payment_lines)
            total_cost += row[COL_AMOUNT]
            number_of_rows += 1

            if config.use_gsheets and ws_expenses:
                ws_expenses.update_cell(
                    i + 2,
                    expenses.columns.get_loc(COL_PAID) + 1,
                    True
                )

    # Process invoices
    for i, row in invoices[~invoices[COL_PAID]].iterrows():
        payment_lines = generate_lines_for_invoice(row)
        if payment_lines:
            output_lines.extend(payment_lines)
            total_cost += row[COL_AMOUNT]
            number_of_rows += 1

            if config.use_gsheets and ws_invoices:
                ws_invoices.update_cell(
                    i + 2,
                    invoices.columns.get_loc(COL_PAID) + 1,
                    True
                )

    return output_lines, number_of_rows, total_cost


def main():
    """Main entry point for PO3 file generation."""
    try:
        config = Config()

        # Load data
        if config.use_gsheets:
            expenses, invoices, ws_expenses, ws_invoices = load_data_from_gsheets(config)
        else:
            expenses, invoices = load_data_from_csv(config)
            ws_expenses = ws_invoices = None

        # Normalize data
        normalize_dataframes(expenses, invoices)

        # Process payments
        output_lines, number_of_rows, total_cost = process_payments(
            expenses, invoices, config, ws_expenses, ws_invoices
        )

        # Check if there are any payments
        if number_of_rows == 0:
            print("No new expenses to process.")
            return

        # Add header and trailer
        output_lines.insert(0, generate_start_line(config))
        output_lines.append(generate_end_line(number_of_rows, total_cost))

        # Write file
        file_name = f"utlägg_{datetime.datetime.now().strftime('%Y%m%d')}_po3.txt"
        write_po3_file(file_name, output_lines)

        print(f"✓ {number_of_rows} payments written to: {file_name}")
        print(f"✓ Total amount: {total_cost:.2f} SEK")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
