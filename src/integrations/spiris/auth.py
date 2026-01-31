"""Spiris API authentication and token management."""

import os
import json
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


class SpirisAuth:
    """Handle Spiris/Visma eAccounting OAuth2 authentication."""

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPIRIS_CLIENT_ID")
        self.client_secret = os.getenv("SPIRIS_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPIRIS_REDIRECT_URI", "https://localhost:44300/callback")
        self.token_url = "https://identity.vismaonline.com/connect/token"
        self.tokens_file = ".spiris_tokens.json"
        
        if not self.client_id or not self.client_secret:
            raise ValueError("SPIRIS_CLIENT_ID and SPIRIS_CLIENT_SECRET must be set in .env")
        
        self.tokens = self._load_tokens()

    def _load_tokens(self) -> dict:
        """Load cached tokens from file."""
        if os.path.exists(self.tokens_file):
            try:
                with open(self.tokens_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load cached tokens - {e}")
        return {}

    def _save_tokens(self, tokens: dict) -> None:
        """Save tokens to file for reuse."""
        try:
            with open(self.tokens_file, "w") as f:
                json.dump(tokens, f)
        except Exception as e:
            print(f"Warning: Could not save tokens - {e}")

    def get_access_token(self, auth_code: str = None) -> str:
        """
        Get or refresh access token.

        Args:
            auth_code: Authorization code from OAuth flow (only needed for first time)

        Returns:
            Access token string
        """
        # Check if we have a valid cached refresh token
        if "refresh_token" in self.tokens and "expires_at" in self.tokens:
            expires_at = datetime.fromisoformat(self.tokens["expires_at"])
            if datetime.now() < expires_at:
                return self.tokens["access_token"]
            
            # Try to refresh
            if self._refresh_access_token():
                return self.tokens["access_token"]

        # If no auth code provided, raise error
        if not auth_code:
            raise ValueError(
                "No valid cached tokens and no auth_code provided. "
                "Run spiris/auth_code.py to get an authorization code."
            )

        # Get new tokens using auth code
        return self._get_tokens_from_code(auth_code)

    def _get_tokens_from_code(self, auth_code: str) -> str:
        """Exchange authorization code for tokens."""
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(self.token_url, data=data)
        response.raise_for_status()

        tokens = response.json()
        self._store_tokens(tokens)
        return tokens["access_token"]

    def _refresh_access_token(self) -> bool:
        """Refresh access token using refresh token."""
        if "refresh_token" not in self.tokens:
            return False

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.tokens["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()
            tokens = response.json()
            self._store_tokens(tokens)
            return True
        except Exception as e:
            print(f"Warning: Token refresh failed - {e}")
            return False

    def _store_tokens(self, tokens: dict) -> None:
        """Store tokens with expiration time."""
        self.tokens = {
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_at": (datetime.now() + timedelta(seconds=tokens.get("expires_in", 3600))).isoformat(),
        }
        self._save_tokens(self.tokens)
