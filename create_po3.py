import datetime
import os
from dotenv import load_dotenv
import pandas as pd


def write_file(file_name, lines):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_header_row() -> str:
    return "MH00" + " " * (12 - 5 + 1) + os.getenv("ORG_NUMBER") + " " * (34 - 23 + 1) + os.getenv("ACCOUNT_NUMBER").ljust(10) + "SEK" + " " * (53 - 48 + 1) + "SEK" + " " * (80 - 57 + 1)


def generate_footer_row(number_of_rows: int, total_cost: float) -> str:
    def format_kostnad(kostnad, length=15):
        return str(int(kostnad * 100)).zfill(length)

    return "MT00" + " " * (29 - 5 + 1) + str(number_of_rows).zfill(7) + format_kostnad(total_cost, 15) + " " * (80 - 52 + 1)


def format_kostnad(kostnad, length=13):
    return str(int(kostnad * 100)).zfill(length)


def row_validation(row) -> bool:
    # TODO implement
    return True


def main():
    load_dotenv()

    number_of_rows = 0  # update if multiple rows
    total_cost = 0

    content = [1]

    output_lines = []
    output_lines.append(generate_header_row())
    content = pd.read_csv("./data/example_expense.csv")
    for _, row in content.iterrows():
        if not row_validation(row):
            print(f"Row validation failed for row: {row}")
            continue
        row_validation(row)
        output_lines.append(
            "PI00"
            + "09"
            + str(row["clearing"]).ljust(5)
            + str(row["account_number"]).ljust(11)
            + "  "
            + datetime.datetime.now().strftime("%Y%m%d")
            + format_kostnad(row["amount"])
            + (row["project"]+row["account"]).ljust(20)
            + " " * (80 - 66 + 1)
        )  # meddelande kan också vara i BM99
        output_lines.append(
            "BA00"
            + " " * (22 - 5 + 1)
            + " " * (31 - 23 + 1)
            + (row["project"]+row["account"]+row["name"]).ljust(66 - 32 + 1)
            + " " * (80 - 67 + 1)
        )  # egen notering # bra om det är samma för samma bokföringspost och konto
        output_lines.append(
            "BE01" + " " * (22 - 5 + 1) + str(row["amount"]).ljust(80 - 23 + 1)  # max 30
        )  # denna läses inte in
        total_cost += row["amount"]
        number_of_rows += 1
    output_lines.append(generate_footer_row(number_of_rows, total_cost))
    file_name = "utlägg_" + datetime.datetime.now().strftime("%Y%m%d") + "_po3.txt"
    write_file(file_name, output_lines)


if __name__ == "__main__":
    main()
