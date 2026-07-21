import os

from ...integrations.google_clients import GmailClient
from ..models import Employee


def generate_salary_specification_table(employee: Employee) -> list[list[str]]:
    rows = [["Verksamhet", "Timlön", "Antal timmar", "Total lön"]]
    for row in employee.salary_rows:
        rows.append([
            str(row.verksamhet),
            str(row.hourly_wage),
            str(row.number_of_hours),
            str(row.total_salary)
        ])
    return rows


def generate_salary_specification(employee: Employee, year: int, month: str) -> str:
    # Organization header block
    org_name = os.getenv('ORG_NAME', '')
    org_number = os.getenv('ORG_NUMBER', '')
    org_address = os.getenv('ORG_ADDRESS', '')

    table_html = GmailClient.generate_html_table(generate_salary_specification_table(employee))
    net_payout = employee.total_salary - employee.deducted_tax

    return f"""<!DOCTYPE html>
<html>
  <body style="font-family: Arial, sans-serif; font-size: 14px; color: #1e293b; line-height: 1.5; padding: 20px;">
    
    <!-- Header info -->
    <div style="margin-bottom: 24px; color: #475569; font-size: 13px;">
      <strong>{org_name}</strong><br>
      Org.nr: {org_number}<br>
      {org_address}
    </div>

    <!-- Title -->
    <h2 style="color: #0f172a; margin-bottom: 16px;">
      Lönespecifikation för {employee.name} ({employee.personnummer}) – {month} {year}
    </h2>

    <!-- Table -->
    {table_html}

    <!-- Summary Box -->
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin: 20px 0; max-width: 600px;">
      <p style="margin: 4px 0;"><strong>Total lön:</strong> {employee.total_salary} kr</p>
      <p style="margin: 4px 0; color: #dc2626;"><strong>Avdragen skatt:</strong> {employee.deducted_tax} kr</p>
      <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 10px 0;">
      <p style="margin: 4px 0; font-size: 16px;"><strong>Betalas ut:</strong> {net_payout} kr till {employee.clearing_number} {employee.account_number}</p>
    </div>

    <!-- Footer -->
    <p style="font-size: 12px; color: #64748b; margin-top: 24px;">
      Något som inte stämmer? Svara på detta mejl snarast.
    </p>

  </body>
</html>
"""
