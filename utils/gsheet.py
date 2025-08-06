import os
import json
import base64
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Decode base64 credentials
creds_b64 = os.environ.get("GSHEET_CRED_B64")
creds_json = base64.b64decode(creds_b64).decode("utf-8")
creds_dict = json.loads(creds_json)

# Step 2: Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Step 3: Open your Google Sheet
sheet = client.open("AllInOneSheet")

# Step 4: Dummy entry in LIVE_DATA
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_row = [now, "TCS", 3870.50, "+0.52%", 175000]

sheet.worksheet("LIVE_DATA").append_row(data_row)

# Also log in DEBUG_LOGS
sheet.worksheet("DEBUG_LOGS").append_row([now, "TEST_PUSH", "Dummy LTP pushed successfully"])

