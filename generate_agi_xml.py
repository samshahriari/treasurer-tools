#!/usr/bin/env python3
"""CLI script to generate Skatteverket AGI XML files from employee salary CSV."""

import argparse
import os
import sys
import pandas as pd

from src.agi import AGIConfig, Employee, generate_agi_xml


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Skatteverket AGI XML file from salary CSV."
    )

    # File paths
    parser.add_argument(
        "-i",
        "--csv-path",
        default="Löner Bruket - exempel.csv",
        help="Path to the input employee salary CSV file.",
    )

    # AGI Configurations
    parser.add_argument(
        "-p",
        "--period",
        help="Reporting period in YYYYMM format (e.g., 202606).",
    )

    return parser.parse_args()


def load_employees_from_csv(csv_path: str) -> list[Employee]:
    """Load and validate employees from the salary CSV file."""
    # Read the CSV with pandas
    df = pd.read_csv(csv_path)

    employees = []
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        employee = Employee(**row_dict)
        employees.append(employee)

    return employees


def main() -> None:
    """Main execution function."""
    args = parse_args()

    # Load defaults from configuration class / environment
    config = AGIConfig()

    # Override config with command-line arguments if provided
    if args.period:
        config.reporting_period = args.period

    # Validate org numbers format (should be 12 digits)
    for name, num in [
        ("Org Number", config.org_number),
        ("Sender ID", config.sender_id),
    ]:
        if not num.isdigit() or len(num) != 12:
            print(f"Error: {name} must be a 12-digit number (got '{num}').")
            sys.exit(1)

    # Validate reporting period format (YYYYMM)
    if not config.reporting_period.isdigit() or len(config.reporting_period) != 6:
        raise ValueError(
            f"Error: Period must be in YYYYMM format (got '{config.reporting_period}')."
        )

    print("Loading salary CSV...")
    employees = load_employees_from_csv(args.csv_path)

    print(f"Loaded and validated {len(employees)} employee record(s).")

    # Generate XML
    print("Generating Skatteverket AGI XML...")
    xml_content = generate_agi_xml(employees, config)

    # Determine output path
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join(
        "output",
        f"agi_declaration_{config.reporting_period}.xml",
    )

    # Ensure parent directory of output path exists
    parent_dir = os.path.dirname(output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    # Print beautiful summary
    print("\n" + "=" * 50)
    print("AGI XML GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 50)
    print(f"Reporting Period:       {config.reporting_period}")
    print(f"Employer Org Number:    {config.org_number}")
    print(f"Saved to:               {output_path}")
    print("-" * 50)

    # Summary calculations for display
    total_salary = sum(emp.total_lon for emp in employees)
    total_tax = sum(int(round(emp.skatt)) for emp in employees)
    period_year = int(config.reporting_period[:4])
    total_contrib = sum(
        emp.calculate_employer_contribution(period_year) for emp in employees
    )

    print(f"Total Employees:        {len(employees)}")
    print(f"Total Gross Salary:     {total_salary:,.2f} SEK")
    print(f"Total Tax Withheld:     {total_tax:,.2f} SEK (FK001)")
    print(f"Total Employer Contrib: {total_contrib:,.2f} SEK (FK487)")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
