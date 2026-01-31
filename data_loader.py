"""Data loading from CSV and Google Sheets."""

import pandas as pd

from config import Config


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
