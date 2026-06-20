"""Main entry point for PO3 file generation."""

import datetime
import os
import sys

# Set UTF-8 encoding for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd

from src.integrations import EmailAttachment, GmailClient, GoogleDriveClient
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


def _send_drive_attachment(
    gmail_client: GmailClient,
    drive_client: GoogleDriveClient,
    recipient: str,
    subject: str,
    body: str,
    drive_url: str,
) -> dict:
    """Download a Drive file and send it as a Gmail attachment."""
    content, filename = drive_client.download_file_from_url(drive_url)
    attachment = EmailAttachment(filename=filename, content=content)
    return gmail_client.send_message(
        to=recipient,
        subject=subject,
        body=body,
        attachments=[attachment],
    )


def _has_attachment_urls(frame: pd.DataFrame, column_name: str) -> bool:
    """Return True when a dataframe contains at least one Drive URL."""
    if column_name not in frame.columns:
        return False
    return frame[column_name].fillna("").astype(str).str.strip().ne("").any()


def process_payments(
    expenses: pd.DataFrame,
    invoices: pd.DataFrame,
    config: Config,
    ws_expenses=None,
    ws_invoices=None,
    gmail_client: GmailClient | None = None,
    drive_client: GoogleDriveClient | None = None,
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

            if gmail_client and drive_client and expense.kvitto_url:
                _send_drive_attachment(
                    gmail_client,
                    drive_client,
                    config.attachment_email_recipient,
                    f"PO3 kvitto: {expense.Ditt_namn}",
                    (
                        f"Automatisk vidarebefordran av kvitto för {expense.Ditt_namn} "
                        f"({expense.Verksamhet})"
                    ),
                    expense.kvitto_url,
                )

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

            if gmail_client and drive_client and invoice.faktura_url:
                _send_drive_attachment(
                    gmail_client,
                    drive_client,
                    config.attachment_email_recipient,
                    f"PO3 faktura: {invoice.Mottagare_namn}",
                    (
                        f"Automatisk vidarebefordran av faktura för {invoice.Mottagare_namn} "
                        f"({invoice.Verksamhet})"
                    ),
                    invoice.faktura_url,
                )

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

        gmail_client = GmailClient() if (
            _has_attachment_urls(expenses, "Ladda upp bild på kvitto")
            or _has_attachment_urls(invoices, "Ladda upp fakturan")
        ) else None
        drive_client = GoogleDriveClient() if gmail_client else None

        # Process payments
        output_lines, number_of_rows, total_cost = process_payments(
            expenses,
            invoices,
            config,
            ws_expenses,
            ws_invoices,
            gmail_client,
            drive_client,
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

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
