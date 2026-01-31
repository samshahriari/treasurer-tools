"""Integration of Spiris attachments with PO3 payment processing."""

from typing import Optional

import pandas as pd

from src.po3.models import ExpenseRow, InvoiceRow

from .google_drive import GoogleDriveClient
from .spiris import SpirisClient

# Cache Google Drive client
_google_drive_client = None


def get_google_drive_client() -> Optional[GoogleDriveClient]:
    """Get or initialize Google Drive client."""
    global _google_drive_client

    if _google_drive_client is None:
        try:
            _google_drive_client = GoogleDriveClient()
        except FileNotFoundError as e:
            print(f"Warning: Google Drive not configured - {e}")
            return None

    return _google_drive_client


def upload_expense_attachments(
    expense: ExpenseRow,
    attachment_url: Optional[str] = None,
    spiris_client: Optional[SpirisClient] = None,
    drive_client: Optional[GoogleDriveClient] = None
) -> dict:
    """
    Upload attachment for an expense to Spiris.

    Args:
        expense: Expense row with attachment URL
        attachment_url: Override URL from expense data
        spiris_client: Spiris API client (will create one if not provided)
        drive_client: Google Drive client (will create one if not provided)

    Returns:
        Spiris attachment response
    """
    if not spiris_client:
        spiris_client = SpirisClient()

    if not drive_client:
        drive_client = get_google_drive_client()

    url = attachment_url or getattr(expense, "Ladda upp bild på kvitto", None)
    if not url:
        print(f"No attachment URL for expense: {expense.Ditt_namn}")
        return None

    if not drive_client:
        print(f"⊘ Skipping attachment for {expense.Ditt_namn} (Google Drive not configured)")
        return None

    try:
        # Download from Google Drive
        file_content, file_name = drive_client.download_file_from_url(url)

        description = f"{expense.Verksamhet} - {expense.Kort_beskrivning_av_köp}"
        result = spiris_client.upload_attachment_binary(
            file_content=file_content,
            file_name=file_name,
            description=description,
            document_type="Receipt"
        )
        print(f"✓ Uploaded attachment for {expense.Ditt_namn}")
        return result
    except Exception as e:
        import traceback
        print(f"✗ Failed to upload attachment for {expense.Ditt_namn}")
        print(f"   Error: {e}")
        traceback.print_exc()
        return None


def upload_invoice_attachments(
    invoice: InvoiceRow,
    attachment_url: Optional[str] = None,
    spiris_client: Optional[SpirisClient] = None,
    drive_client: Optional[GoogleDriveClient] = None
) -> dict:
    """
    Upload attachment for an invoice to Spiris.

    Args:
        invoice: Invoice row with attachment URL
        attachment_url: Override URL from invoice data
        spiris_client: Spiris API client (will create one if not provided)
        drive_client: Google Drive client (will create one if not provided)

    Returns:
        Spiris attachment response
    """
    if not spiris_client:
        spiris_client = SpirisClient()

    if not drive_client:
        drive_client = get_google_drive_client()

    url = attachment_url or getattr(invoice, "Ladda upp fakturan", None)
    if not url:
        print(f"No attachment URL for invoice: {invoice.Mottagare_namn}")
        return None

    if not drive_client:
        print(f"⊘ Skipping attachment for {invoice.Mottagare_namn} (Google Drive not configured)")
        return None

    try:
        # Download from Google Drive
        file_content, file_name = drive_client.download_file_from_url(url)

        description = f"{invoice.Verksamhet} - {invoice.Kort_beskrivning_av_köp}"
        result = spiris_client.upload_attachment_binary(
            file_content=file_content,
            file_name=file_name,
            description=description,
            document_type="Invoice"
        )
        print(f"✓ Uploaded attachment for {invoice.Mottagare_namn}")
        return result
    except Exception as e:
        print(f"✗ Failed to upload attachment for {invoice.Mottagare_namn} - {e}")
        return None


def upload_attachments_for_dataframe(
    dataframe: pd.DataFrame,
    attachment_column: str,
    is_expense: bool = True,
    spiris_client: Optional[SpirisClient] = None,
    drive_client: Optional[GoogleDriveClient] = None
) -> list:
    """
    Upload attachments for all rows in a dataframe.

    Args:
        dataframe: DataFrame with rows to process
        attachment_column: Name of column containing attachment URLs
        is_expense: True for expenses, False for invoices
        spiris_client: Spiris API client (will create one if not provided)
        drive_client: Google Drive client (will create one if not provided)

    Returns:
        List of upload results
    """
    if not spiris_client:
        spiris_client = SpirisClient()

    if not drive_client:
        drive_client = get_google_drive_client()

    results = []

    for index, row in dataframe.iterrows():
        try:
            if is_expense:
                from src.po3.validators import validate_expense
                model = validate_expense(row)
                if model:
                    result = upload_expense_attachments(
                        model, spiris_client=spiris_client, drive_client=drive_client
                    )
                    results.append(result)
            else:
                from src.po3.validators import validate_invoice
                model = validate_invoice(row)
                if model:
                    result = upload_invoice_attachments(
                        model, spiris_client=spiris_client, drive_client=drive_client
                    )
                    results.append(result)
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            results.append(None)

    return results
