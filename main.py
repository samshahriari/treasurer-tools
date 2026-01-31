"""Main entry point for PO3 file generation."""

import datetime

import pandas as pd

from config import Config
from constants import COL_PAID
from data_loader import load_data_from_csv, load_data_from_gsheets
from formatters import generate_end_line, generate_start_line
from payment_generator import generate_lines_for_expense, generate_lines_for_invoice
from validators import validate_expense, validate_invoice


def write_po3_file(file_name: str, lines: list[str]) -> None:
    """
    Write PO3 file with proper encoding.

    Args:
        file_name: Output file name
        lines: List of formatted lines
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


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
        expense = validate_expense(row)
        if expense:
            output_lines.extend(generate_lines_for_expense(expense))
            total_cost += expense.Belopp
            number_of_rows += 1

            if config.use_gsheets and ws_expenses:
                ws_expenses.update_cell(
                    i + 2,
                    expenses.columns.get_loc(COL_PAID) + 1,
                    True
                )

    # Process invoices
    for i, row in invoices[~invoices[COL_PAID]].iterrows():
        invoice = validate_invoice(row)
        if invoice:
            output_lines.extend(generate_lines_for_invoice(invoice))
            total_cost += invoice.Belopp
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

        # Convert string boolean columns to actual booleans for DataFrame filtering
        def parse_bool_col(series):
            return series.map(lambda x: str(x).strip().lower() == "true" if isinstance(x, str) else bool(x))

        expenses[COL_PAID] = parse_bool_col(expenses[COL_PAID])
        invoices[COL_PAID] = parse_bool_col(invoices[COL_PAID])

        # Process payments
        output_lines, number_of_rows, total_cost = process_payments(
            expenses, invoices, config, ws_expenses, ws_invoices
        )

        # Check if there are any payments
        if number_of_rows == 0:
            print("No new expenses to process.")
            return

        # Add header and trailer
        output_lines.insert(0, generate_start_line(config.org_number, config.account_number))
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
