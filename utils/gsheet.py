import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json
import base64

# --- Step 1: Auth with base64 credentials ---
creds_b64 = os.environ["GSHEET_CRED_B64"]
creds_json = base64.b64decode(creds_b64).decode("utf-8")
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# --- Step 2: Open sheet ---
sheet = client.open("AllinoneSheet")

# --- Step 3: Try to open LIVE_DATA sheet, else create it ---
try:
    ws = sheet.worksheet("LIVE_DATA")
except gspread.exceptions.WorksheetNotFound:
    ws = sheet.add_worksheet(title="LIVE_DATA", rows="1000", cols="10")

# --- Step 4: Add headers if not present ---
expected_headers = ["SYMBOL", "PRICE", "TIME"]
current_headers = ws.row_values(1)

if current_headers != expected_headers:
    ws.resize(rows=1)
    ws.update("A1", [expected_headers])

# --- Step 5: Add real or dummy row ---
symbol = "NSDL"
price = 930
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ws.append_row([symbol, price, now])

print("✅ LIVE_DATA sheet created or updated successfully.")
