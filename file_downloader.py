"""Download files from Google Drive URLs."""

import os
import re
from pathlib import Path
from typing import Optional

import gspread


def extract_file_id_from_url(url: str) -> Optional[str]:
    """
    Extract Google Drive file ID from various URL formats.
    
    Args:
        url: Google Drive URL (can be various formats)
        
    Returns:
        File ID if found, None otherwise
        
    Examples:
        - https://drive.google.com/file/d/FILE_ID/view
        - https://drive.google.com/open?id=FILE_ID
        - https://docs.google.com/spreadsheets/d/FILE_ID/edit
    """
    if not url or not isinstance(url, str):
        return None
        
    # Pattern 1: /d/FILE_ID/ or /d/FILE_ID?
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Pattern 2: ?id=FILE_ID or &id=FILE_ID
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # If it's just a file ID (no URL format)
    if re.match(r'^[a-zA-Z0-9_-]+$', url):
        return url
        
    return None


def download_file_from_drive(file_url: str, output_dir: str, filename: str) -> Optional[str]:
    """
    Download a file from Google Drive.
    
    Args:
        file_url: Google Drive file URL or ID
        output_dir: Directory to save the file
        filename: Name for the downloaded file
        
    Returns:
        Path to downloaded file if successful, None otherwise
    """
    file_id = extract_file_id_from_url(file_url)
    if not file_id:
        print(f"  ⚠️  Could not extract file ID from URL: {file_url}")
        return None
    
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Use gspread to authenticate
        gc = gspread.oauth()
        
        # Download file using Google Drive API
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        import io
        
        # Build Drive API service using the same credentials
        drive_service = build('drive', 'v3', credentials=gc.auth)
        
        # Get file metadata to determine the correct extension
        file_metadata = drive_service.files().get(fileId=file_id, fields='name,mimeType').execute()
        original_name = file_metadata.get('name', filename)
        
        # Use original extension if filename doesn't have one
        if '.' not in filename and '.' in original_name:
            ext = original_name.split('.')[-1]
            filename = f"{filename}.{ext}"
        
        output_path = os.path.join(output_dir, filename)
        
        # Download file content
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        # Write to file
        with open(output_path, 'wb') as f:
            f.write(fh.getvalue())
        
        print(f"  ✓ Downloaded: {filename}")
        return output_path
        
    except Exception as e:
        print(f"  ⚠️  Failed to download file {file_id}: {e}")
        return None


def download_processed_files(
    expenses_with_files: list[tuple[int, str, str]],
    invoices_with_files: list[tuple[int, str, str]],
    output_dir: str = "downloaded_documents"
) -> dict[str, list[str]]:
    """
    Download all files from processed expenses and invoices.
    
    Args:
        expenses_with_files: List of (index, name, file_url) tuples for expenses
        invoices_with_files: List of (index, name, file_url) tuples for invoices
        output_dir: Base directory for downloaded files
        
    Returns:
        Dictionary with 'expenses' and 'invoices' keys containing lists of downloaded file paths
    """
    downloaded = {'expenses': [], 'invoices': []}
    
    if not expenses_with_files and not invoices_with_files:
        return downloaded
    
    print(f"\n📥 Downloading attached documents to '{output_dir}'...")
    
    # Download expense receipts
    if expenses_with_files:
        expense_dir = os.path.join(output_dir, "receipts")
        print(f"\nDownloading {len(expenses_with_files)} expense receipt(s)...")
        
        for idx, name, file_url in expenses_with_files:
            # Create safe filename from name and index
            safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
            filename = f"expense_{idx}_{safe_name}"
            
            downloaded_path = download_file_from_drive(file_url, expense_dir, filename)
            if downloaded_path:
                downloaded['expenses'].append(downloaded_path)
    
    # Download invoices
    if invoices_with_files:
        invoice_dir = os.path.join(output_dir, "invoices")
        print(f"\nDownloading {len(invoices_with_files)} invoice(s)...")
        
        for idx, name, file_url in invoices_with_files:
            # Create safe filename from name and index
            safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
            filename = f"invoice_{idx}_{safe_name}"
            
            downloaded_path = download_file_from_drive(file_url, invoice_dir, filename)
            if downloaded_path:
                downloaded['invoices'].append(downloaded_path)
    
    # Summary
    total = len(downloaded['expenses']) + len(downloaded['invoices'])
    print(f"\n✓ Downloaded {total} document(s) successfully")
    
    return downloaded
