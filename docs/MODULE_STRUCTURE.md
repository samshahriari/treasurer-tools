# PO3 File Generator Module Structure

This project has been refactored into separate modules for better maintainability and reusability.

## Module Overview

### Core Entry Point
- **`create_po3.py`** - Main entry point for the script. Can be run directly: `python create_po3.py`
- **`main.py`** - Contains the main processing logic and orchestration

### Configuration & Constants
- **`constants.py`** - All constants including giro codes, record types, and field names
- **`config.py`** - Configuration management via environment variables

### Data Models
- **`models.py`** - Pydantic models for data validation
  - `ExpenseRow` - Validated expense data
  - `InvoiceRow` - Validated invoice data

### Data Processing
- **`data_loader.py`** - Data loading from CSV or Google Sheets
  - `load_data_from_csv()` - Load from local CSV files
  - `load_data_from_gsheets()` - Load from Google Sheets
  - `normalize_dataframes()` - Normalize boolean columns

- **`validators.py`** - Data validation
  - `validate_expense()` - Validates and converts expense rows
  - `validate_invoice()` - Validates and converts invoice rows

### PO3 File Generation
- **`formatters.py`** - PO3 format generators and utility functions
  - `generate_start_line()` - Generate MH00 header
  - `generate_end_line()` - Generate MT00 trailer
  - `generate_pi00_expense()` - Payment line for bank transfers
  - `generate_pi00_giro()` - Payment line for giro transfers
  - `generate_ba00()` - Note line
  - `generate_be01()` - Beneficiary line
  - Utility functions: `format_amount()`, `normalize_boolean_column()`, etc.

- **`payment_generator.py`** - High-level payment line generation
  - `generate_lines_for_expense()` - Generate full payment entry for expense
  - `generate_lines_for_invoice()` - Generate full payment entry for invoice

## Usage

### Running the Script
```bash
python create_po3.py
```

Or directly:
```bash
python main.py
```

### Using as a Library
You can import individual modules and use them in your own code:

```python
from config import Config
from data_loader import load_data_from_csv
from validators import validate_expense
from payment_generator import generate_lines_for_expense

config = Config()
expenses, invoices = load_data_from_csv(config)

for _, row in expenses.iterrows():
    expense = validate_expense(row)
    if expense:
        lines = generate_lines_for_expense(expense)
        print(lines)
```

## Dependencies
- `pandas` - Data manipulation
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management
- `gspread` - Google Sheets API (optional, only if using `USE_GSHEETS=TRUE`)

## Environment Variables

Required:
- `ORG_NUMBER` - Organization number
- `ACCOUNT_NUMBER` - Bank account number

For CSV mode:
- `EXPENSE_PATH` - Path to expense CSV file
- `INVOICE_PATH` - Path to invoice CSV file

For Google Sheets mode (set `USE_GSHEETS=TRUE`):
- `SHEET_NAME` - Name of Google Sheet
- `EXPENSE_GSHEET_ID` - Worksheet ID for expenses
- `INVOICE_GSHEET_ID` - Worksheet ID for invoices

## Design Benefits

1. **Modularity** - Each module has a single responsibility
2. **Reusability** - Modules can be imported and used independently
3. **Testability** - Easier to write unit tests for individual modules
4. **Maintainability** - Clear structure makes code easier to modify
5. **Type Safety** - Pydantic models ensure data validity
6. **Documentation** - Each module and function is well-documented
