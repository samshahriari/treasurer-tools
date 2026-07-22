

import os

from dotenv import load_dotenv

from src.po3.formatters import generate_end_line, generate_start_line
from src.po3.payment_generator import (
    generate_lines_for_salary,
)
from src.salary.models import load_employees_from_csv


def main():
    employees = load_employees_from_csv("Löner Bruket - Juli.csv")
    output_lines = []
    total_cost = 0
    number_of_rows = 0
    output_lines.append(generate_start_line(os.getenv("ORG_NUMBER"), os.getenv("ACCOUNT_NUMBER")))
    for employee in employees:
        # client = GmailClient()
        # client.send_html_message(
        #     to=employee.email,
        #     subject="Lönespecifikation Bruket - juli 2026",
        #     html_body=generate_salary_specification(employee, 2026, "juli", "2026-07-24"),
        # )
        output_lines.extend(generate_lines_for_salary(employee))
        total_cost += employee.payed_salary
        number_of_rows += 1
    output_lines.append(generate_end_line(number_of_rows, total_cost))

    with open("salary.txt", "w") as f:
        f.write("\n".join(output_lines))


if __name__ == "__main__":
    load_dotenv()
    main()
