"""Spiris API client for attachments and other operations."""

import os

import requests

from .auth import SpirisAuth


class SpirisClient:
    """Client for Spiris/Visma eAccounting API."""

    BASE_URL = "https://eaccountingapi.vismaonline.com/v2"

    def __init__(self, auth_code: str = None):
        """
        Initialize Spiris client.

        Args:
            auth_code: Optional authorization code for first-time authentication
        """
        self.auth = SpirisAuth()
        self.access_token = self.auth.get_access_token(auth_code)
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def upload_attachment(
        self,
        file_path: str,
        description: str = None,
        document_type: str = "Receipt"
    ) -> dict:
        """
        Upload an attachment to Spiris from a file path.

        Args:
            file_path: Path to file to upload
            description: Optional description for the attachment
            document_type: Type of document (e.g., "Receipt", "Invoice")

        Returns:
            API response with attachment details
        """

        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)
            file_data = f.read()

        return self.upload_attachment_binary(
            file_content=file_data,
            file_name=file_name,
            description=description,
            document_type=document_type
        )

    def upload_attachment_binary(
        self,
        file_content: bytes,
        file_name: str,
        description: str = None,
        document_type: str = "Receipt",
        content_type: str = None
    ) -> dict:
        """
        Upload an attachment to Spiris from binary content.

        Args:
            file_content: Binary file content
            file_name: Name for the file
            description: Optional description
            document_type: Type of document
            content_type: MIME type (e.g., 'image/jpeg', 'application/pdf')
                         If not provided, will try to guess from filename

        Returns:
            API response with attachment details
        """
        import base64
        import mimetypes

        # Determine content type if not provided
        if not content_type:
            content_type, _ = mimetypes.guess_type(file_name)
            if not content_type:
                # Default to PDF if can't determine
                content_type = "application/pdf"

        # Validate content type (API only accepts specific types)
        allowed_types = ['image/jpeg', 'image/png', 'image/tiff', 'application/pdf']
        if content_type not in allowed_types:
            # Default to PDF for unsupported types
            raise ValueError(
                f"Unsupported content type: {content_type}. Allowed types are: {allowed_types}"
            )

        # Convert to base64
        file_data = base64.b64encode(file_content).decode("utf-8")

        # Prepare JSON payload (using exact API field names)
        payload = {
            "FileName": file_name,
            "Data": file_data,
            "ContentType": content_type,
            "Comment": description or None,
        }

        # Use JSON headers
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        api_url = f"{self.BASE_URL}/attachments"
        response = requests.post(api_url, headers=headers, json=payload)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # Try to get detailed error message from API
            try:
                error_detail = response.json()
                raise requests.HTTPError(f"{e}\nAPI Error: {error_detail}", response=response)
            except Exception:
                raise e

        return response.json()

    def upload_attachment_from_url(
        self,
        url: str,
        file_name: str,
        description: str = None,
        document_type: str = "Receipt"
    ) -> dict:
        """
        Upload an attachment to Spiris from a URL.

        Args:
            url: URL of file to upload
            file_name: Name for the file in Spiris
            description: Optional description
            document_type: Type of document

        Returns:
            API response with attachment details
        """
        import base64

        # Download file from URL
        response = requests.get(url)
        response.raise_for_status()

        # Convert to base64
        file_data = base64.b64encode(response.content).decode("utf-8")

        # Prepare JSON payload
        payload = {
            "fileName": file_name,
            "fileData": file_data,
            "description": description or file_name,
            "documentType": document_type,
        }

        # Use JSON headers for this request
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        api_url = f"{self.BASE_URL}/attachments"
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()

    def get_attachment(self, attachment_id: str) -> dict:
        """
        Get attachment details.

        Args:
            attachment_id: ID of attachment

        Returns:
            Attachment details
        """
        url = f"{self.BASE_URL}/attachments/{attachment_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_attachment(self, attachment_id: str) -> bool:
        """
        Delete an attachment.

        Args:
            attachment_id: ID of attachment to delete

        Returns:
            True if successful
        """
        url = f"{self.BASE_URL}/attachments/{attachment_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code in [200, 204]

    def list_attachments(self, document_type: str = None) -> list:
        """
        List attachments.

        Args:
            document_type: Optional filter by document type

        Returns:
            List of attachments
        """
        url = f"{self.BASE_URL}/attachments"
        params = {}
        if document_type:
            params["documentType"] = document_type

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
