"""Get authorization code for Spiris API."""

import urllib.parse
import webbrowser
import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPIRIS_CLIENT_ID")
REDIRECT_URI = os.getenv("SPIRIS_REDIRECT_URI", "https://localhost:44300/callback")

if not CLIENT_ID:
    print("Error: SPIRIS_CLIENT_ID not found in .env")
    exit(1)

AUTH_URL = "https://identity.vismaonline.com/connect/authorize"

params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": "ea:api offline_access ea:accounting ea:sales",
}

url = AUTH_URL + "?" + urllib.parse.urlencode(params)

print("Opening browser for authentication...")
webbrowser.open(url)

print("\nAfter login, copy the ?code=XXXX from the redirect URL")
print("and paste it below:\n")

auth_code = input("Authorization code: ").strip()

if auth_code:
    print(f"\nYour authorization code: {auth_code}")
    print("\nTo use this code, run:")
    print("  from spiris import SpirisClient")
    print(f'  client = SpirisClient(auth_code="{auth_code}")')
    print("\nOr set it in the auth function and it will be cached for future use.")
else:
    print("No code provided.")

