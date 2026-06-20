# PO3 Payment File Generator

Automated tool for generating Swedish PO3 (Plusgiro/Bankgiro) payment files from expense and invoice data.

## Features

- Generate PO3-format payment files for Swedish banks
- Load data from CSV files or Google Sheets
- Validate rows with Pydantic models before output generation
- Mark processed rows as paid in Google Sheets mode
- Download files from Google Drive and attach them to Gmail messages

## Quick Start

### 1. Installation

```bash
# Clone repository and install dependencies
git clone <your-repo-url>
cd utlägg

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and fill in your details:

```bash
# Required - PO3 file generation
ORG_NUMBER=your-org-number
ACCOUNT_NUMBER=your-account-number

# Optional - Data source (default: CSV)
USE_GSHEETS=FALSE
EXPENSE_PATH=data/Verifikat 2026 - Utlägg.csv
INVOICE_PATH=data/Verifikat 2026 - Faktura.csv
```

### 3. Run

```bash
python main.py
```

This will:
1. Load expense/invoice data from CSV or Google Sheets
2. Generate a PO3 payment file in `output/`
3. Print payment count and total amount

## Gmail attachments

When PO3 runs, it will automatically forward Drive files found in:

- expenses: `Ladda upp bild på kvitto`
- invoices: `Ladda upp fakturan`

The files are emailed to `ATTACHMENT_EMAIL_RECIPIENT`.

Use the Drive and Gmail integration clients together if you need the same behavior in your own code:

```python
from src.integrations import GmailClient, GoogleDriveClient

drive = GoogleDriveClient()
gmail = GmailClient()

content, filename = drive.download_file_from_url("https://drive.google.com/file/d/<FILE_ID>/view")
attachment = GmailClient.from_bytes(content, filename)

gmail.send_message(
    to="recipient@example.com",
    subject="Attached file",
    body="See attached.",
    attachments=[attachment],
)
```

To authenticate Gmail sending, run:

```bash
python scripts/setup_gmail_oauth.py
```

## Project Structure

```
utlägg/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── po3/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── validators.py
│   │   ├── data_loader.py
│   │   ├── formatters.py
│   │   └── payment_generator.py
│   └── integrations/
│       ├── __init__.py
│       ├── google_clients.py
├── data/
└── output/
```


## Troubleshooting

- Module import errors: ensure the virtual environment is activated and dependencies are installed.
- Google OAuth errors: run `python scripts/setup_google_oauth.py` again.
- Unicode errors on Windows: output is configured to UTF-8 in `main.py`.

## References

- [PO3 Format Specification](https://kontoutdrag.plusgirot.se/KU/CPYA011/CF)
- [gspread-dataframe](https://github.com/robin900/gspread-dataframe)
