# Google Drive Integration

This project includes a Google Drive client for downloading files referenced by Google Drive URLs.

## Setup Instructions

### 1. Create OAuth Credentials in Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select an existing one
3. Enable Google Drive API
4. Go to Credentials and create an OAuth 2.0 Client ID
5. Choose "Desktop application"
6. Download credentials and save them as `google_client_secret.json` in the project root

### 2. Run OAuth Setup

```bash
python scripts/setup_google_oauth.py
```

This opens a browser, asks for Drive read-only permission, and stores your token in `.google_drive_token.json`.

## Usage Example

```python
from src.integrations.google_drive import GoogleDriveClient

drive = GoogleDriveClient()
content, filename = drive.download_file_from_url("https://drive.google.com/file/d/<FILE_ID>/view")
print(filename, len(content))
```

## What It Supports

- OAuth token caching and refresh
- Download by file ID
- Download directly from common Drive URL formats
- Clear errors for invalid URLs or missing auth setup

