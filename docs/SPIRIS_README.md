# Spiris API Integration

This module provides integration with Visma eAccounting's Spiris API for uploading and managing attachments.

## Setup

### 1. Register Your Application

1. Go to [Visma Developer Portal](https://developer.vismaonline.com/)
2. Create a new application
3. Register the redirect URI: `https://localhost:44300/callback`
4. Note your Client ID and Client Secret

### 2. Configure Environment Variables

Add to your `.env` file:

```env
SPIRIS_CLIENT_ID=your_client_id
SPIRIS_CLIENT_SECRET=your_client_secret
SPIRIS_REDIRECT_URI=https://localhost:44300/callback
```

### 3. Get Initial Authorization Code

Run the authentication flow:

```bash
python spiris/auth_code.py
```

This will open your browser. After logging in, copy the authorization code from the redirect URL.

## Usage

### Basic Attachment Upload

```python
from spiris import SpirisClient

# Initialize client (uses cached tokens or provide auth code)
client = SpirisClient()

# Upload from file
result = client.upload_attachment(
    file_path="path/to/receipt.pdf",
    description="Receipt for office supplies",
    document_type="Receipt"
)

# Upload from URL
result = client.upload_attachment_from_url(
    url="https://example.com/document.pdf",
    file_name="document.pdf",
    description="Expense receipt",
    document_type="Receipt"
)

# Delete attachment
client.delete_attachment(result["id"])

# List attachments
attachments = client.list_attachments(document_type="Receipt")
```

### Integration with PO3 Processing

```python
from spiris_attachments import upload_expense_attachments, upload_invoice_attachments
from spiris import SpirisClient
from validators import validate_expense

# Create Spiris client once
spiris_client = SpirisClient()

# Upload attachment for an expense
expense = validate_expense(expense_row)
if expense:
    upload_expense_attachments(expense, spiris_client=spiris_client)

# Upload attachment for an invoice
invoice = validate_invoice(invoice_row)
if invoice:
    upload_invoice_attachments(invoice, spiris_client=spiris_client)
```

### Batch Upload

```python
from spiris_attachments import upload_attachments_for_dataframe
from data_loader import load_data_from_csv
from config import Config

config = Config()
expenses, invoices = load_data_from_csv(config)

# Upload all expense attachments
results = upload_attachments_for_dataframe(
    expenses,
    attachment_column="Ladda upp bild på kvitto",
    is_expense=True
)
```

## Features

- **OAuth2 Authentication** - Secure token-based authentication
- **Token Caching** - Automatically caches and refreshes tokens
- **URL Downloads** - Download and upload attachments from URLs
- **Batch Operations** - Upload multiple attachments efficiently
- **Error Handling** - Graceful error handling with detailed messages

## API Endpoints

The module wraps these Visma eAccounting API endpoints:

- `POST /v2/attachments` - Upload attachment
- `GET /v2/attachments` - List attachments
- `GET /v2/attachments/{attachmentId}` - Get attachment details
- `DELETE /v2/attachments/{attachmentId}` - Delete attachment

## Documentation

- [Visma eAccounting API Docs](https://eaccountingapi.vismaonline.com/scalar/v2)
- [OAuth2 Flow](https://developer.vismaonline.com/docs/authentication/)

## Troubleshooting

### Invalid Authorization Code
Make sure the code is fresh (usually valid for a few minutes) and copied completely.

### Token Expiration
Tokens are automatically refreshed using the refresh token. If you see authentication errors, delete `.spiris_tokens.json` and re-authorize.

### Upload Failures
- Check that the file URL is accessible
- Ensure proper document type is specified
- Verify network connectivity
