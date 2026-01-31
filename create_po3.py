import datetime
import os

import pandas as pd
from dotenv import load_dotenv


def write_file(file_name: str, lines: list[str]) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_start_line() -> str:
    return (
        "MH00"
        + " " * (12 - 5 + 1)
        + os.getenv("ORG_NUMBER")
        + " " * (34 - 23 + 1)
        + os.getenv("ACCOUNT_NUMBER").ljust(10)
        + "SEK"
        + " " * (53 - 48 + 1)
        + "SEK"
        + " " * (80 - 57 + 1)
    )


def generate_end_line(number_of_rows: int, total_cost: float) -> str:
    return (
        "MT00"
        + " " * (29 - 5 + 1)
        + str(number_of_rows).zfill(7)
        + format_amount(total_cost, 15)
        + " " * (80 - 52 + 1)
    )


def format_amount(amount: float, length=13):
    return str(round(amount * 100)).zfill(length)


def row_validation(row: pd.DataFrame) -> bool:
    # TODO more checks
    return row["Godkänt"]


def generate_pi00_expense(
    clearing_number: int, account_number: int, amount: float, message: str
) -> str:
    return (
        "PI00"
        + "09"
        + str(clearing_number).ljust(5)
        + str(account_number).ljust(11)
        + "  "
        + datetime.datetime.now().strftime("%Y%m%d")
        + format_amount(amount)
        + message.ljust(12)[:12]
        + " " * (8 + 80 - 66 + 1)
    )


def generate_pi00_giro(account_number: int, amount: float, ocr: str, giro_code: str) -> str:
    # giro_code is  "00" for plusgiro and "05" for bankgiro
    return (
        "PI00"
        + giro_code
        + " " * (11 - 7 + 1)
        + str(account_number).ljust(11)
        + "  "
        + datetime.datetime.now().strftime("%Y%m%d")
        + format_amount(amount)
        + str(ocr).ljust(70 - 46 + 1)
        + " " * (80 - 71 + 1)
    )


def generate_ba00(note: str) -> str:
    return (
        "BA00"
        + note.ljust(22 - 5 + 1)[:22 - 5 + 1]
        + " " * (31 - 23 + 1)
        + note.ljust(66 - 32 + 1)[:66 - 32 + 1]
        + " " * (80 - 67 + 1)
    )


def generate_be01(recipient: str) -> str:
    return "BE01" + " " * (22 - 5 + 1) + recipient.ljust(80 - 23 + 1)


def generate_lines_for_one_expense(row: pd.DataFrame) -> list[str] | None:
    if not row_validation(row):
        print(f"Row validation failed for row: {row}")
        return None
    out = []
    message = f"{row['Verksamhet']} {row['Kort beskrivning av köp']}"
    out.append(
        generate_pi00_expense(
            row["Clearingnummer"], row["Kontonummer"], row["Belopp"], message
        )
    )
    note = f"{row['Verksamhet']} {row['Kort beskrivning av köp']} {row['Ditt namn']}"
    out.append(generate_ba00(note))
    out.append(generate_be01(row["Ditt namn"]))
    return out


def generate_lines_for_one_invoice(row: pd.DataFrame) -> list[str] | None:
    if not row_validation(row):
        print(f"Row validation failed for row: {row}")
        return None
    out = []
    giro_code = "00" if row["Mottagarkontotyp"] == "Plusgiro" else "05"
    out.append(
        generate_pi00_giro(
            row["Mottagarkontonummer"], row["Belopp"], row["OCR/meddelande"], giro_code
        )
    )
    note = f"{row['Verksamhet']} {row['Kort beskrivning av köp']} {row['Ditt namn']}"
    out.append(generate_ba00(note))
    out.append(generate_be01(row["Mottagare (namn)"]))
    return out


def main():
    load_dotenv()

    number_of_rows = 0
    total_cost = 0

    output_lines = []
    if os.getenv("USE_GSHEETS") == "TRUE":
        import gspread

        gc = gspread.oauth()
        sheet = gc.open(os.getenv("SHEET_NAME"))
        ws_expenses = sheet.get_worksheet_by_id(int(os.getenv("EXPENSE_GSHEET_ID")))
        expenses_data = ws_expenses.get_all_records()
        expenses = pd.DataFrame(expenses_data)
        ws_invoices = sheet.get_worksheet_by_id(int(os.getenv("INVOICE_GSHEET_ID")))
        invoices_data = ws_invoices.get_all_records()
        invoices = pd.DataFrame(invoices_data)
        print("Data loaded from Google Sheets.")
    else:
        expenses = pd.read_csv(os.getenv("EXPENSE_PATH"))
        invoices = pd.read_csv(os.getenv("INVOICE_PATH"))
        print("Data loaded from CSV files.")

    invoices["Godkänt"] = invoices["Godkänt"].map(lambda x: str(x).strip().lower() == "true" if isinstance(x, str) else bool(x))
    invoices["Utbetalt"] = invoices["Utbetalt"].map(lambda x: str(x).strip().lower() == "true" if isinstance(x, str) else bool(x))
    expenses["Godkänt"] = expenses["Godkänt"].map(lambda x: str(x).strip().lower() == "true" if isinstance(x, str) else bool(x))
    expenses["Utbetalt"] = expenses["Utbetalt"].map(lambda x: str(x).strip().lower() == "true" if isinstance(x, str) else bool(x))

    for i, row in expenses[~expenses["Utbetalt"]].iterrows():
        payment = generate_lines_for_one_expense(row)
        if payment:
            output_lines.extend(payment)
            total_cost += row["Belopp"]
            number_of_rows += 1
            if os.getenv("USE_GSHEETS") == "TRUE":
                ws_expenses.update_cell(i + 2, expenses.columns.get_loc("Utbetalt") + 1, True)

    for i, row in invoices[~invoices["Utbetalt"]].iterrows():
        payment = generate_lines_for_one_invoice(row)
        if payment:
            output_lines.extend(payment)
            total_cost += row["Belopp"]
            number_of_rows += 1
            if os.getenv("USE_GSHEETS") == "TRUE":
                ws_invoices.update_cell(i + 2, invoices.columns.get_loc("Utbetalt") + 1, True)
    output_lines.append(generate_end_line(number_of_rows, total_cost))
    file_name = "utlägg_" + datetime.datetime.now().strftime("%Y%m%d") + "_po3.txt"
    if number_of_rows == 0:
        print("No new expenses to process.")
        return
    write_file(file_name, output_lines)
    print(f"{number_of_rows} expenses written to: {file_name}")


if __name__ == "__main__":
    main()
