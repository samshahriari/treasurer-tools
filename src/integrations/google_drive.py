"""Google Drive API integration for downloading files."""

import json
import os
from io import BytesIO
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveClient:
    """Client for accessing Google Drive files using OAuth."""

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    TOKEN_FILE = ".google_drive_token.json"

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Google Drive client with OAuth token.

        Args:
            access_token: OAuth access token for Google Drive
                         If not provided, uses stored token from .google_drive_token.json
        """
        if access_token:
            # Use provided access token
            credentials = Credentials(token=access_token)
        else:
            # Try to load cached token
            if os.path.exists(self.TOKEN_FILE):
                with open(self.TOKEN_FILE, "r") as f:
                    token_data = json.load(f)
                    credentials = Credentials.from_authorized_user_info(token_data, scopes=self.SCOPES)
            else:
                raise FileNotFoundError(
                    f"Google Drive OAuth token not found at {self.TOKEN_FILE}. "
                    f"Run setup_google_oauth() first or pass access_token parameter."
                )

        # Refresh token if needed
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        self.service = build("drive", "v3", credentials=credentials)

    @staticmethod
    def extract_file_id(url: str) -> Optional[str]:
        """
        Extract file ID from Google Drive URL.

        Args:
            url: Google Drive URL (various formats supported)

        Returns:
            File ID or None if not found
        """
        if not url:
            return None

        # Format: https://drive.google.com/open?id=FILE_ID
        if "id=" in url:
            return url.split("id=")[1].split("&")[0]

        # Format: https://drive.google.com/file/d/FILE_ID/view
        if "/d/" in url:
            return url.split("/d/")[1].split("/")[0]

        return None

    def download_file(self, file_id: str) -> tuple[bytes, str]:
        """
        Download file from Google Drive.

        Args:
            file_id: Google Drive file ID

        Returns:
            Tuple of (file_content, file_name)
        """
        try:
            # Get file metadata
            file_metadata = self.service.files().get(
                fileId=file_id, fields="name, mimeType"
            ).execute()

            file_name = file_metadata.get("name", f"file_{file_id}")

            # Download file content
            request = self.service.files().get_media(fileId=file_id)
            file_stream = BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            file_content = file_stream.getvalue()
            return file_content, file_name

        except Exception as e:
            raise Exception(f"Failed to download file from Google Drive: {e}")

    def download_file_from_url(self, url: str) -> tuple[bytes, str]:
        """
        Download file from Google Drive URL.

        Args:
            url: Google Drive URL

        Returns:
            Tuple of (file_content, file_name)
        """
        file_id = self.extract_file_id(url)
        if not file_id:
            raise ValueError(f"Could not extract file ID from URL: {url}")

        return self.download_file(file_id)
