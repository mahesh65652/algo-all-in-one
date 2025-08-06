import os
import base64
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def read_google_sheet():
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")

    with open("temp_creds.json", "w") as f:
        f.write(creds_json)

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    sheet_id = os.environ.get("GSHEET_ID")
    spreadsheet = client.open_by_key(sheet_id)
    sheet = spreadsheet.worksheet("LIVE_DATA")
    data = sheet.get_all_records()

    os.remove("temp_creds.json")
    return data

def update_signal(data):
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")

    with open("temp_creds.json", "w") as f:
        f.write(creds_json)

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    sheet_id = os.environ.get("GSHEET_ID")
    spreadsheet = client.open_by_key(sheet_id)
    
    try:
        sheet = spreadsheet.worksheet("LIVE_DATA")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

    sheet.clear()
    sheet.append_row(["Symbol", "Signal", "Price", "Time"])

    for row in data:
        sheet.append_row([
            row.get("Symbol"),
            row.get("Signal"),
            row.get("Price"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    os.remove("temp_creds.json")

def update_trade_log(symbol, price, side="SELL"):
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    sheet_id = os.environ.get("GSHEET_ID")
    if not creds_b64 or not sheet_id:
        print("⚠️ Credentials missing")
        return

    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    with open("temp_creds.json", "w") as f:
        f.write(creds_json)

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(sheet_id)
    try:
        sheet = spreadsheet.worksheet("TRADES")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="TRADES", rows="100", cols="10")
        sheet.append_row(["Time", "Symbol", "Side", "Price"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, symbol, side, price])
    os.remove("temp_creds.json")

    # Telegram
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        message = f"✅ *Order Executed*\n\n🟥 {side} {symbol} @ ₹{price}\n🕒 {now}"
        res = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        )
        if res.status_code == 200:
            print("📬 Trade notification sent")
        else:
            print("❌ Telegram failed:", res.text)

