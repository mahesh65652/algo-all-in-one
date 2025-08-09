import os
import base64
import gspread
import requests
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


# 1️⃣ Google Sheet से market data पढ़ने का function
def fetch_gsheet_data():
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
        sheet = spreadsheet.worksheet("MARKET_DATA")
    except gspread.exceptions.WorksheetNotFound:
        raise Exception("❌ MARKET_DATA sheet नहीं मिली")

    data = sheet.get_all_values()

    os.remove("temp_creds.json")
    return data


# 2️⃣ NSE Cash Strategy
def process_nse_cash(sheet_data):
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])  # skip header

    # Ensure numeric columns
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    signals = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        if row['Close'] > prev['High']:
            signals.append({
                'symbol': row['Symbol'],
                'signal': 'BUY',
                'price': row['Close'],
                'time': row.get('Time', 'NA')
            })
        elif row['Close'] < prev['Low']:
            signals.append({
                'symbol': row['Symbol'],
                'signal': 'SELL',
                'price': row['Close'],
                'time': row.get('Time', 'NA')
            })

    return signals


# 3️⃣ Signals को LIVE_DATA में लिखना + Telegram Notify
def update_signal(data):
    print("📤 Sheet update data:", data)

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
            row.get("symbol"),
            row.get("signal"),
            row.get("price"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    os.remove("temp_creds.json")

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


# 4️⃣ Main Run
if __name__ == "__main__":
    print("🚀 Fetching MARKET_DATA from Google Sheets...")
    sheet_data = fetch_gsheet_data()

    print("📈 Running NSE Cash Strategy...")
    signals = process_nse_cash(sheet_data)

    print("📝 Updating LIVE_DATA & Sending Telegram...")
    update_signal(signals)

    print("✅ Done!")
