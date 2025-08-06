import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json
import base64

# --- Setup credentials from B64 Secret ---
creds_b64 = os.environ["GSHEET_CRED_B64"]
creds_json = base64.b64decode(creds_b64).decode("utf-8")
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# --- Open Sheet and Worksheet ---
sheet = client.open("AllinoneSheet")
ws = sheet.worksheet("LIVE_DATA")

# --- Define expected headers ---
headers = ["SYMBOL", "PRICE", "TIME"]

# --- Check if headers exist, if not insert them ---
existing = ws.row_values(1)
if existing != headers:
    ws.resize(rows=1)  # clear previous junk rows
    ws.update("A1", [headers])  # insert headers in 1st row

# --- Sample Data (replace with real-time data later) ---
symbol = "NSDL"
price = 930.00
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

row = [symbol, price, time_now]
ws.append_row(row)

print("✅ LIVE_DATA updated with real entry")
