# PO3 Payment File Generator

Automated tool for generating Swedish PO3 (Plusgiro/Bankgiro) payment files with integrated expense tracking and attachment management through Visma eAccounting (Spiris).

## Features

- ✅ Generate PO3-format payment files for Swedish banks
- ✅ Load data from CSV files or Google Sheets
- ✅ Automatic data validation with Pydantic models
- ✅ Upload receipts/invoices to Visma eAccounting (Spiris)
- ✅ Google Drive integration for attachment downloads
- ✅ OAuth2 authentication for all external services
- ✅ Automatic marking of processed payments

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

# Optional - Spiris integration
UPLOAD_TO_SPIRIS=FALSE
SPIRIS_CLIENT_ID=your-client-id
SPIRIS_CLIENT_SECRET=your-client-secret
SPIRIS_REDIRECT_URI=https://localhost:44300/callback
```

### 3. Run

```bash
python main.py
```

This will:
1. Load expense/invoice data from CSV or Google Sheets
2. Generate PO3 payment file in `output/` directory
3. Upload attachments to Spiris (if enabled)

## Project Structure

```
utlägg/
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration (not in git)
├── .env.example                 # Example environment configuration
├── README.md                    # Project documentation
│
├── src/                         # Source code
│   ├── po3/                     # PO3 file generation module
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── constants.py         # Constants and column names
│   │   ├── models.py            # Pydantic data models
│   │   ├── validators.py        # Data validation
│   │   ├── data_loader.py       # CSV/Google Sheets loading
│   │   ├── formatters.py        # PO3 format generators
│   │   └── payment_generator.py # Payment line generation
│   │
│   └── integrations/            # External service integrations
│       ├── __init__.py
│       ├── spiris/              # Spiris/Visma API client
│       │   ├── __init__.py
│       │   ├── auth.py          # OAuth2 authentication
│       │   └── client.py        # API client
│       ├── google_drive.py      # Google Drive API client
│       └── spiris_attachments.py # Spiris attachment upload logic
│
├── scripts/                     # Setup and utility scripts
│   └── setup_google_oauth.py   # Google Drive OAuth setup
│
├── tests/                       # Test files
│   ├── test.py
│   ├── test_drive_access.py
│   └── test_google_drive_integration.py
│
├── data/                        # Input data files
│   ├── Verifikat 2026 - Utlägg.csv
│   ├── Verifikat 2026 - Faktura.csv
│   └── example_expense.csv
│
├── output/                      # Generated PO3 files
│   └── utlägg_YYYYMMDD_po3.txt
│
├── docs/                        # Documentation
│   ├── MODULE_STRUCTURE.md
│   ├── SPIRIS_README.md
│   └── GOOGLE_DRIVE_INTEGRATION.md
│
└── inskickade/                  # Submitted files archive
```

## Setup Guides

### Google Drive (for downloading attachments)

1. Create OAuth credentials in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Drive API
3. Download credentials as `google_client_secret.json`
4. Run authentication:
   ```bash
   python scripts/setup_google_oauth.py
   ```

See [docs/GOOGLE_DRIVE_INTEGRATION.md](docs/GOOGLE_DRIVE_INTEGRATION.md) for details.

### Spiris/Visma eAccounting

1. Register app at [Visma Developer Portal](https://developer.vismaonline.com/)
2. Get client ID and secret
3. Add credentials to `.env`
4. Run authentication:
   ```bash
   python src/integrations/spiris/auth_code.py
   ```

See [docs/SPIRIS_README.md](docs/SPIRIS_README.md) for details.

## Module Organization

### src/po3/
Core PO3 payment file generation functionality:
- **config.py**: Environment variable loading and configuration
- **constants.py**: PO3 format constants and column mappings
- **models.py**: Pydantic models for expenses and invoices with validation
- **validators.py**: DataFrame → Pydantic model conversion
- **data_loader.py**: Load data from CSV or Google Sheets
- **formatters.py**: Generate PO3 formatted strings (MH00, PI00, BA00, BE01, MT00)
- **payment_generator.py**: Combine formatters to create complete payment records

### src/integrations/
External API integrations:
- **spiris/**: Visma eAccounting (Spiris) API client
  - **auth.py**: OAuth2 token management with caching
  - **client.py**: Attachment upload/download operations
- **google_drive.py**: Google Drive API client for downloading attachments
- **spiris_attachments.py**: Glue code connecting payment processing to Spiris uploads

## Data Format

### Expected CSV Columns (Expenses)
- `Ditt namn` - Name
- `Belopp` - Amount (SEK)
- `Konto` - Account number (Bankgiro/Plusgiro)
- `Kontoinnehavare namn` - Account holder name
- `Ladda upp bild på kvitto` - Receipt URL (Google Drive)
- `Verksamhet` - Department/Activity
- `Kort beskrivning av köp` - Description
- `Betald` - Payment status (TRUE/FALSE)

### Expected CSV Columns (Invoices)
Similar structure with invoice-specific fields.

## Development

### Adding New Features

1. **New PO3 record types**: Add formatters to `src/po3/formatters.py`
2. **New integrations**: Create new module in `src/integrations/`
3. **Data validation rules**: Update models in `src/po3/models.py`
4. **Configuration options**: Add to `src/po3/config.py` and `.env.example`

### Testing

```bash
# Test Google Drive integration
python tests/test_google_drive_integration.py

# Test Spiris connection
python tests/test.py
```

## Troubleshooting

**ModuleNotFoundError**: Make sure virtual environment is activated and dependencies installed.

**Google Drive authentication error**: Run `python scripts/setup_google_oauth.py` to refresh OAuth token.

**Spiris API errors**: Check that credentials in `.env` are correct and run `python src/integrations/spiris/auth_code.py` to get new access token.

**Unicode errors on Windows**: The script automatically sets UTF-8 encoding for console output.

## References

- [PO3 Format Specification](https://kontoutdrag.plusgirot.se/KU/CPYA011/CF)
- [gspread Documentation](https://github.com/robin900/gspread-dataframe)
- [Visma eAccounting API](https://developer.vismaonline.com/)

## License

[Your License Here]
