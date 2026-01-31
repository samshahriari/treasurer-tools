# Google Drive Integration Complete ✓
## Setup Instructions

### 1. Create OAuth Credentials in Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google Drive API
4. Go to Credentials → Create OAuth 2.0 Client ID
   - Choose "Desktop application"
   - Download the credentials
   - Save as `google_client_secret.json` in project root

### 2. Run OAuth Setup
```bash
python setup_google_oauth.py
```

This will:
- Open browser for you to log in with your Google account
- Ask for permission to access Google Drive (read-only)
- Save token to `.google_drive_token.json` for future use

### 3. Configure environment
Add to `.env`:
```
UPLOAD_TO_SPIRIS=TRUE
```

That's it! The OAuth token is automatically cached and refreshed.

## Workflow
```
CSV/Sheets → PO3 Generation → Mark as paid
         ↓
  Google Drive Download (OAuth)
  (if UPLOAD_TO_SPIRIS=TRUE)
         ↓
  Spiris Upload
  (base64 encoded binary)
```

## Testing
```bash
python test_google_drive_integration.py
```

This verifies:
- ✓ GoogleDriveClient initialization
- ✓ SpirisClient initialization  
- ✓ File ID extraction from URLs
- ✓ All required packages installed

## Full Workflow Example
```python
from google_drive import GoogleDriveClient
from spiris import SpirisClient

# Download from Google Drive (uses cached OAuth token)
drive = GoogleDriveClient()
content, filename = drive.download_file_from_url("https://drive.google.com/file/d/...")

# Upload to Spiris
spiris = SpirisClient()
result = spiris.upload_attachment_binary(
    file_content=content,
    file_name=filename,
    description="Receipt for expense",
    document_type="Receipt"
)
```

## Key Features
- ✅ OAuth authentication (user's own Google account)
- ✅ Automatic token caching and refresh
- ✅ Supports multiple Google Drive URL formats
- ✅ Binary file uploads to Spiris (base64 encoded JSON)
- ✅ Graceful error handling and user feedback
- ✅ Client caching to avoid repeated initialization
- ✅ Optional feature - disabled by default

