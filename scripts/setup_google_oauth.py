#!/usr/bin/env python3
"""Set up Google Drive OAuth authentication."""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Drive API scopes
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
TOKEN_FILE = ".google_drive_token.json"


def setup_google_oauth():
    """
    Set up Google OAuth authentication for Google Drive.
    
    Follow the prompts to:
    1. Log in with your Google account
    2. Grant permissions to access Google Drive
    3. Token will be saved to .google_drive_token.json
    """
    # Check if credentials.json exists (from Google Cloud Console)
    if not os.path.exists("google_client_secret.json"):
        print("Error: google_client_secret.json not found!")
        print("\nTo set up Google Drive OAuth:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create or select a project")
        print("3. Enable Google Drive API")
        print("4. Go to Credentials → Create OAuth 2.0 Client ID (Desktop app)")
        print("5. Download the credentials and save as google_client_secret.json")
        return False

    try:
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file(
            "google_client_secret.json", SCOPES
        )
        
        # Run the local server authentication
        credentials = flow.run_local_server(port=0)
        
        # Save the token for future use
        token_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
        
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f, indent=2)
        
        print(f"\n✓ OAuth token saved to {TOKEN_FILE}")
        print("You can now use GoogleDriveClient to download files from Google Drive!")
        return True
        
    except Exception as e:
        print(f"Error during OAuth setup: {e}")
        return False


if __name__ == "__main__":
    setup_google_oauth()
