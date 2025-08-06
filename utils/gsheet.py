import os
import base64
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def update_signal(data):
    # Decode credentials
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")

    with open("temp_creds.json", "w") as f:
        f.write(creds_json)

    # Auth
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    # Sheet
    sheet_id = os.environ.get("GSHEET_ID")
    spreadsheet = client.open_by_key(sheet_id)

    try:
        sheet = spreadsheet.worksheet("LIVE_DATA")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

    # Clear and write header
    sheet.clear()
    sheet.append_row(["Symbol", "Price", "Time"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for row in data:
        symbol = row.get("symbol") or "N/A"
        price = row.get("price") or "N/A"
        sheet.append_row([symbol, price, now])

    os.remove("temp_creds.json")
    print("✅ Google Sheet updated.")

    # Telegram notification
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    message = f"📊 *GSheet Update Done*\n🟢 Rows: {len(data)}\n🕒 {now}"
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
