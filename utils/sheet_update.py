import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Credentials decode
creds_b64 = os.environ.get("GSHEET_CRED_B64")
creds_json = base64.b64decode(creds_b64).decode("utf-8")

with open("temp_creds.json", "w") as f:
    f.write(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
client = gspread.authorize(creds)

# Open by exact name
spreadsheet = client.open("AllinoneSheet")

# Create or open sheet
try:
    sheet = spreadsheet.worksheet("LIVE_DATA")
except gspread.exceptions.WorksheetNotFound:
    sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

# Clear & set headers
sheet.clear()
sheet.append_row(["Symbol", "Price", "Time"])

# Add sample row
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sheet.append_row(["NSDL", "930", now])
print("✅ update done")
