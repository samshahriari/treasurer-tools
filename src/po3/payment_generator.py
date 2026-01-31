"""Payment line generation for expenses and invoices."""

from .constants import (
    BANKGIRO_CODE,
    PLUSGIRO_CODE,
)
from .formatters import (
    create_message,
    create_note,
    generate_ba00,
    generate_be01,
    generate_pi00_expense,
    generate_pi00_giro,
)
from .models import ExpenseRow, InvoiceRow


def generate_lines_for_expense(expense: ExpenseRow) -> list[str]:
    """
    Generate PO3 lines for a single expense (bank account payment).

    Args:
        expense: Validated expense row model

    Returns:
        List of formatted lines
    """
    lines = []
    message = create_message(expense.Verksamhet, expense.Kort_beskrivning_av_köp)

    lines.append(generate_pi00_expense(
        expense.Clearingnummer,
        expense.Kontonummer,
        expense.Belopp,
        message
    ))

    note = create_note(expense.Verksamhet, expense.Kort_beskrivning_av_köp, expense.Ditt_namn)
    lines.append(generate_ba00(note))
    lines.append(generate_be01(expense.Ditt_namn))

    return lines


def generate_lines_for_invoice(invoice: InvoiceRow) -> list[str]:
    """
    Generate PO3 lines for a single invoice (giro payment).

    Args:
        invoice: Validated invoice row model

    Returns:
        List of formatted lines
    """
    lines = []
    giro_code = PLUSGIRO_CODE if invoice.Mottagarkontotyp == "Plusgiro" else BANKGIRO_CODE

    lines.append(generate_pi00_giro(
        invoice.Mottagarkontonummer,
        invoice.Belopp,
        invoice.OCR_meddelande,
        giro_code
    ))

    note = create_note(invoice.Verksamhet, invoice.Kort_beskrivning_av_köp, invoice.Ditt_namn)
    lines.append(generate_ba00(note))
    lines.append(generate_be01(invoice.Mottagare_namn))

    return lines
