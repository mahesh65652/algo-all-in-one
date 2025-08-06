import os
import base64
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def update_signal(data):
    print("📤 Sheet update data:", data)

    # 1️⃣ Decode credentials
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")

    with open("temp_creds.json", "w") as f:
        f.write(creds_json)

    # 2️⃣ Auth with Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    # 3️⃣ Open spreadsheet
    sheet_id = os.environ.get("GSHEET_ID")
    spreadsheet = client.open_by_key(sheet_id)

    # 4️⃣ Access or create LIVE_DATA sheet
    try:
        sheet = spreadsheet.worksheet("LIVE_DATA")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

    # 5️⃣ Clear & write headers
    sheet.clear()
    sheet.append_row(["Symbol", "Signal", "Price", "Time"])

    # 6️⃣ Fill data rows
    for row in data:
        sheet.append_row([
            row.get("Symbol"),
            row.get("Signal"),
            row.get("Price"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    # 7️⃣ Clean up
    os.remove("temp_creds.json")

    # 8️⃣ Telegram notification
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"📊 *GSheet Updated*\n\n✅ Rows: {len(data)}\n🕒 {now}"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    res = requests.post(url, data=payload)
    if res.status_code == 200:
        print("📬 Telegram sent")
    else:
        print("❌ Telegram failed:", res.text)

