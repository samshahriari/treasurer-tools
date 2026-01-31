import urllib.parse
import webbrowser
import os

CLIENT_ID = os.environ.get("SPIRIS_CLIENT_ID")
if not CLIENT_ID:
    raise RuntimeError(
        "Environment variable SPIRIS_CLIENT_ID must be set with the OAuth client ID."
    )
REDIRECT_URI = "https://localhost:44300/callback"
SCOPES = "ea:api offline_access ea:accounting ea:sales"

AUTH_URL = "https://identity.vismaonline.com/connect/authorize"

params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": SCOPES,
}

url = AUTH_URL + "?" + urllib.parse.urlencode(params)

print("Opening browser for authentication...")
webbrowser.open(url)

print("After login, copy the ?code=XXXX from the redirect URL")

# https: // localhost: 44300/callback?code = C9A8682248E5E3F019D9CD05A9D4F3D1BD65276DBEB7D364AF891B68A07158EA-1 & scope = ea % 3Aapi % 20offline_access & iss = https % 3A % 2F % 2Fidentity.vismaonline.com
# https: // localhost: 44300/callback?code = 364BE20665E9F5031221B92BA2669460E8BA28D853AFDDEA2E23DE275B867F9C-1 & scope = ea % 3Aapi % 20offline_access % 20ea % 3Aaccounting % 20ea % 3Asales & iss = https % 3A % 2F % 2Fidentity.vismaonline.com
