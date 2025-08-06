import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Load and decode credentials
creds_b64 = os.environ.get("GSHEET_CRED_B64")
creds_json = base64.b64decode(creds_b64).decode("utf-8")

# Save to a temporary file
with open("temp_creds.json", "w") as f:
    f.write(creds_json)

# Auth scopes
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
client = gspread.authorize(creds)

# Open sheet
spreadsheet = client.open("AllinoneSheet")

# Create or open LIVE_DATA sheet
try:
    sheet = spreadsheet.worksheet("LIVE_DATA")
except gspread.exceptions.WorksheetNotFound:
    sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

# Clear & setup headers
sheet.clear()
sheet.append_row(["Symbol", "Price", "Time"])

# Add dummy row
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sheet.append_row(["NSDL", "930", now])

