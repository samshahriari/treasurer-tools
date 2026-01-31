"""Main entry point for PO3 file generation."""

import datetime
import os
import sys

# Set UTF-8 encoding for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd

from src.po3 import (
    COL_PAID,
    Config,
    generate_end_line,
    generate_lines_for_expense,
    generate_lines_for_invoice,
    generate_start_line,
    load_data_from_csv,
    load_data_from_gsheets,
    validate_expense,
    validate_invoice,
)


def write_po3_file(file_name: str, lines: list[str]) -> None:
    """
    Write PO3 file with proper encoding.

    Args:
        file_name: Output file name
        lines: List of formatted lines
    """
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    file_path = os.path.join("output", file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return file_path


def upload_attachments_to_spiris(expenses: pd.DataFrame, invoices: pd.DataFrame) -> None:
    """
    Upload attachments to Spiris if enabled.

    Args:
        expenses: DataFrame with expenses
        invoices: DataFrame with invoices
    """
    if not os.getenv("UPLOAD_TO_SPIRIS", "FALSE").upper() == "TRUE":
        return

    try:
        from src.integrations import (
            SpirisClient,
            get_google_drive_client,
            upload_expense_attachments,
            upload_invoice_attachments,
        )

        print("\nUploading attachments to Spiris...")
        spiris_client = SpirisClient()
        drive_client = get_google_drive_client()

        # Upload expense attachments
        for _, row in expenses[~expenses[COL_PAID]].iterrows():
            expense = validate_expense(row)
            if expense and hasattr(expense, "Ladda upp bild på kvitto"):
                upload_expense_attachments(
                    expense,
                    spiris_client=spiris_client,
                    drive_client=drive_client
                )

        # Upload invoice attachments
        for _, row in invoices[~invoices[COL_PAID]].iterrows():
            invoice = validate_invoice(row)
            if invoice and hasattr(invoice, "Ladda upp fakturan"):
                upload_invoice_attachments(
                    invoice,
                    spiris_client=spiris_client,
                    drive_client=drive_client
                )

        print("✓ Attachment upload complete")

    except ImportError:
        print("Warning: Spiris modules not available. Skipping attachment uploads.")
    except Exception as e:
        print(f"Warning: Failed to upload attachments to Spiris - {e}")


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
    for index, row in expenses[~expenses[COL_PAID]].iterrows():
        expense = validate_expense(row)
        if expense:
            output_lines.extend(generate_lines_for_expense(expense))
            total_cost += expense.Belopp
            number_of_rows += 1

            if config.use_gsheets and ws_expenses:
                ws_expenses.update_cell(
                    index + 2,
                    expenses.columns.get_loc(COL_PAID) + 1,
                    True
                )

    # Process invoices
    for index, row in invoices[~invoices[COL_PAID]].iterrows():
        invoice = validate_invoice(row)
        if invoice:
            output_lines.extend(generate_lines_for_invoice(invoice))
            total_cost += invoice.Belopp
            number_of_rows += 1

            if config.use_gsheets and ws_invoices:
                ws_invoices.update_cell(
                    index + 2,
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
        file_path = write_po3_file(file_name, output_lines)

        print(f"✓ {number_of_rows} payments written to: {file_path}")
        print(f"✓ Total amount: {total_cost:.2f} SEK")

        # Upload attachments to Spiris if enabled
        upload_attachments_to_spiris(expenses, invoices)

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
