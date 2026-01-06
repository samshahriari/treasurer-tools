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
    return str(int(amount * 100)).zfill(length)


def row_validation(row: pd.DataFrame) -> bool:
    # TODO more checks
    return row["Godkänt"]


def generate_pi00(
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
        + message.ljust(20)
        + " " * (80 - 66 + 1)
    )


def generate_ba00(note: str) -> str:
    return (
        "BA00"
        + " " * (22 - 5 + 1)
        + " " * (31 - 23 + 1)
        + note.ljust(66 - 32 + 1)
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
        generate_pi00(
            row["Clearingnummer"], row["Kontonummer"], row["Kostnad"], message
        )
    )
    note = f"{row['Verksamhet']} {row['Kort beskrivning av köp']} {row['Ditt namn']}"
    out.append(generate_ba00(note))
    out.append(generate_be01(row["Ditt namn"]))
    return out


def main():
    load_dotenv()

    number_of_rows = 0
    total_cost = 0

    output_lines = []
    output_lines.append(generate_start_line())
    content = pd.read_csv(os.getenv("EXPENSE_PATH"))
    for _, row in content.iterrows():
        payment = generate_lines_for_one_expense(row)
        if payment:
            output_lines.extend(payment)
            total_cost += row["Kostnad"]
            number_of_rows += 1
    output_lines.append(generate_end_line(number_of_rows, total_cost))
    file_name = "utlägg_" + datetime.datetime.now().strftime("%Y%m%d") + "_po3.txt"
    write_file(file_name, output_lines)


if __name__ == "__main__":
    main()
