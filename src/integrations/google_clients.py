import base64
import mimetypes
import os
from dataclasses import dataclass
from email.message import EmailMessage
from io import BytesIO
from pathlib import Path
from typing import Optional, Sequence

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GoogleAuthClient:
    """Base client for Google APIs with OAuth authentication."""

    # Define these as placeholders or force subclasses to override them
    SCOPES: list[str] = []
    TOKEN_FILE: str = ""
    service_name: str = ""
    service_version: str = ""

    def __init__(self):
        """Initialize the Google client with OAuth credentials."""
        if not self.SCOPES or not self.TOKEN_FILE:
            raise NotImplementedError("Subclasses must define SCOPES and TOKEN_FILE")

        creds = None
        if os.path.exists(self.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "google_client_secret.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        # Correctly maps to the subclass attributes
        self.service = build(self.service_name, self.service_version, credentials=creds)


class GoogleDriveClient(GoogleAuthClient):
    """Client for accessing Google Drive files using OAuth."""

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]  # Recommended to use readonly if just downloading
    TOKEN_FILE = ".google_drive_token.json"
    service_name = "drive"       # Fixed: Removed leading underscore
    service_version = "v3"     # Fixed: Removed leading underscore

    @staticmethod
    def extract_file_id(url: str) -> Optional[str]:
        if not url:
            return None
        if "id=" in url:
            return url.split("id=")[1].split("&")[0]
        if "/d/" in url:
            return url.split("/d/")[1].split("/")[0]
        return None

    def download_file(self, file_id: str) -> tuple[bytes, str]:
        try:
            file_metadata = self.service.files().get(
                fileId=file_id, fields="name, mimeType"
            ).execute()

            file_name = file_metadata.get("name", f"file_{file_id}")

            request = self.service.files().get_media(fileId=file_id)
            file_stream = BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            return file_stream.getvalue(), file_name

        except Exception as e:
            raise Exception(f"Failed to download file from Google Drive: {e}")

    def download_file_from_url(self, url: str) -> tuple[bytes, str]:
        file_id = self.extract_file_id(url)
        if not file_id:
            raise ValueError(f"Could not extract file ID from URL: {url}")
        return self.download_file(file_id)


@dataclass(frozen=True)
class EmailAttachment:
    """Attachment payload for an outbound email."""

    filename: str
    content: bytes
    mime_type: Optional[str] = None


class GmailClient(GoogleAuthClient):
    """Client for sending Gmail messages with optional attachments."""

    SCOPES = ["https://mail.google.com/"]
    TOKEN_FILE = "gmail_token.json"
    service_name = "gmail"
    service_version = "v1"

    @staticmethod
    def _guess_mime_type(filename: str) -> str:
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or "application/octet-stream"

    @staticmethod
    def _split_mime_type(filename: str, mime_type: Optional[str]) -> tuple[str, str]:
        resolved = mime_type or GmailClient._guess_mime_type(filename)
        if "/" not in resolved:
            return "application", "octet-stream"
        return resolved.split("/", 1)

    @staticmethod
    def _build_message(
        to: str,
        subject: str,
        body: str,
        attachments: Sequence[EmailAttachment] = (),
        sender: Optional[str] = None,
        cc: Optional[Sequence[str]] = None,
        bcc: Optional[Sequence[str]] = None,
    ) -> EmailMessage:
        message = EmailMessage()
        message["To"] = to
        message["Subject"] = subject
        if sender:
            message["From"] = sender
        if cc:
            message["Cc"] = ", ".join(cc)
        if bcc:
            message["Bcc"] = ", ".join(bcc)

        message.set_content(body)

        for attachment in attachments:
            maintype, subtype = GmailClient._split_mime_type(
                attachment.filename, attachment.mime_type
            )
            message.add_attachment(
                attachment.content,
                maintype=maintype,
                subtype=subtype,
                filename=attachment.filename,
            )

        return message

    @staticmethod
    def from_file(path: str | Path) -> EmailAttachment:
        """Load a file from disk for use as an attachment."""
        file_path = Path(path)
        return EmailAttachment(
            filename=file_path.name,
            content=file_path.read_bytes(),
            mime_type=GmailClient._guess_mime_type(file_path.name),
        )

    @staticmethod
    def from_bytes(
        content: bytes,
        filename: str,
        mime_type: Optional[str] = None,
    ) -> EmailAttachment:
        """Create an attachment from raw bytes."""
        return EmailAttachment(
            filename=filename,
            content=content,
            mime_type=mime_type or GmailClient._guess_mime_type(filename),
        )

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Sequence[EmailAttachment] = (),
        sender: Optional[str] = None,
        cc: Optional[Sequence[str]] = None,
        bcc: Optional[Sequence[str]] = None,
    ) -> dict:
        """Send an email message through Gmail."""
        message = self._build_message(to, subject, body, attachments, sender, cc, bcc)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": encoded_message})
            .execute()
        )

    @staticmethod
    def generate_html_table(data: list[list[str]], has_header: bool = True) -> str:
        """
        Converts a list of lists of strings into a styled HTML table
        compatible with Gmail API email bodies.
        """
        if not data:
            return ""

        # Container styling
        table_style = (
            'width: 100%; '
            'max-width: 600px; '
            'border-collapse: collapse; '
            'font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; '
            'font-size: 14px; '
            'color: #1e293b; '
            'margin: 16px 0;'
        )

        header_style = (
            'background-color: #0f172a; '
            'color: #ffffff; '
            'font-weight: 600; '
            'text-align: left; '
            'padding: 10px 14px; '
            'border: 1px solid #cbd5e1;'
        )

        cell_base_style = (
            'padding: 10px 14px; '
            'border: 1px solid #cbd5e1; '
            'text-align: left;'
        )

        rows_html = []

        # Process header if present
        start_idx = 0
        if has_header:
            header_cells = "".join(f'<th style="{header_style}">{cell}</th>' for cell in data[0])
            rows_html.append(f'  <thead>\n    <tr>{header_cells}</tr>\n  </thead>')
            start_idx = 1

        # Process body rows
        body_rows = []
        for row_idx, row in enumerate(data[start_idx:]):
            # Alternating background colors (#ffffff / #f8fafc)
            bg_color = '#ffffff' if row_idx % 2 == 0 else '#f8fafc'
            cell_style = f'{cell_base_style} background-color: {bg_color};'

            cells = "".join(f'<td style="{cell_style}">{cell}</td>' for cell in row)
            body_rows.append(f'    <tr>{cells}</tr>')

        rows_html.append('  <tbody>\n' + "\n".join(body_rows) + '\n  </tbody>')

        return f'<table style="{table_style}">\n' + "\n".join(rows_html) + '\n</table>'

    def _build_html_message(
        self,
        to: str,
        subject: str,
        html_body: str,
        attachments: Sequence[EmailAttachment] = (),
        sender: Optional[str] = None,
        cc: Optional[Sequence[str]] = None,
        bcc: Optional[Sequence[str]] = None,
    ) -> EmailMessage:
        message = EmailMessage()
        message["To"] = to
        message["Subject"] = subject

        if sender:
            message["From"] = sender
        if cc:
            message["Cc"] = ", ".join(cc)
        if bcc:
            message["Bcc"] = ", ".join(bcc)

        # Direct HTML setting with plain-text fallback
        message.set_content("Vänligen aktivera HTML-visning för att se detta mejl.")
        message.add_alternative(html_body, subtype="html")

        for attachment in attachments:
            message.add_attachment(
                attachment.data,
                maintype=attachment.maintype,
                subtype=attachment.subtype,
                filename=attachment.filename,
            )

        return message

    def send_html_message(
        self,
        to: str,
        subject: str,
        html_body: str,
        attachments: Sequence[EmailAttachment] = (),
        sender: Optional[str] = None,
        cc: Optional[Sequence[str]] = None,
        bcc: Optional[Sequence[str]] = None,
    ) -> dict:
        """Send an HTML email message through Gmail."""
        message = self._build_html_message(to, subject, html_body, attachments, sender, cc, bcc)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": encoded_message})
            .execute()
        )
