# PO3 Payment File Generator

Automated tool for generating Swedish PO3 (Plusgiro/Bankgiro) payment files from expense and invoice data.

## Features

- Generate PO3-format payment files for Swedish banks
- Load data from CSV files or Google Sheets
- Validate rows with Pydantic models before output generation
- Mark processed rows as paid in Google Sheets mode

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
│       └── google_drive.py
├── scripts/
│   └── setup_google_oauth.py
├── docs/
│   ├── MODULE_STRUCTURE.md
│   └── GOOGLE_DRIVE_INTEGRATION.md
├── data/
└── output/
```

## Documentation

- Google Drive setup: [docs/GOOGLE_DRIVE_INTEGRATION.md](docs/GOOGLE_DRIVE_INTEGRATION.md)
- Module overview: [docs/MODULE_STRUCTURE.md](docs/MODULE_STRUCTURE.md)

## Troubleshooting

- Module import errors: ensure the virtual environment is activated and dependencies are installed.
- Google OAuth errors: run `python scripts/setup_google_oauth.py` again.
- Unicode errors on Windows: output is configured to UTF-8 in `main.py`.

## References

- [PO3 Format Specification](https://kontoutdrag.plusgirot.se/KU/CPYA011/CF)
- [gspread-dataframe](https://github.com/robin900/gspread-dataframe)
