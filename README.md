# AAP Streamlit Onboarding Portal

Files included:
- `app.py` — main Streamlit app
- `requirements.txt` — Python dependencies
- `AAP_API.PNG` — company logo used in the sidebar

## Expected Streamlit secrets

This app is designed to work with Streamlit secrets / environment-based deployment. It supports:
- `access_code` (optional fallback static code)
- `SPREADSHEET_ID` **or** `access_sheet_name`
- `access_worksheet` (default: `Access`)
- `progress_worksheet` (default: `Progress`)
- `gcp_service_account` (recommended service account block)

### Example `secrets.toml`
```toml
access_code = "YOUR_PORTAL_CODE"
SPREADSHEET_ID = "your_google_sheet_id"
access_worksheet = "Access"
progress_worksheet = "Progress"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

## Access worksheet
The access worksheet should contain at least:
- access code column (optional if using static `access_code` secret)
- employee number column
- full name column

Recognized header examples:
- `Access Code`
- `Employee Number`
- `Full Name`

Extra columns like `Department`, `Location`, and `Title` will display in the sidebar when present.

## Progress worksheet
The app can also store training progress in a worksheet named `Progress` (or your configured value).  
If the worksheet is missing, the app still works — progress just stays in the current session.
