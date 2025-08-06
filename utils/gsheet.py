
import os
import base64
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1️⃣ Decode credentials
creds_b64 = os.environ.get("GSHEET_CRED_B64")
creds_json = base64.b64decode(creds_b64).decode("utf-8")

with open("temp_creds.json", "w") as f:
    f.write(creds_json)

# 2️⃣ Auth with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
client = gspread.authorize(creds)

# 3️⃣ Open spreadsheet by ID
sheet_id = os.environ.get("GSHEET_ID")
spreadsheet = client.open_by_key(sheet_id)

# 4️⃣ Get or create worksheet
try:
    sheet = spreadsheet.worksheet("LIVE_DATA")
except gspread.exceptions.WorksheetNotFound:
    sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

# 5️⃣ Clear sheet and set headers
sheet.clear()
sheet.append_row(["Symbol", "Price", "Time"])

# 6️⃣ Add data row
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
symbol = "NSDL"
price = "930"
sheet.append_row([symbol, price, now])

# 7️⃣ Clean up temp credentials file
os.remove("temp_creds.json")

# ✅ Print and notify
print("✅ update done")

# 8️⃣ Send Telegram message
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

message = f"📊 *GSheet Update Done*\n\n🟢 {symbol} @ ₹{price}\n🕒 {now}"

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown"
}

res = requests.post(url, data=payload)

if res.status_code == 200:
    print("📬 Telegram message sent")
else:
    print("❌ Telegram failed:", res.text)
