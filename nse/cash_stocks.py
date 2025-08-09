import pandas as pd
import gspread
import requests
from google.oauth2.service_account import Credentials

# ===== CONFIG =====
TEST_MODE = False   # Local test के लिए True करो
GSHEET_ID = "YOUR_SHEET_ID_HERE"
SHEET_NAME = "Sheet1"

# Telegram Config
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# Google API Scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# ===== FUNCTIONS =====

def send_telegram_message(message):
    """Telegram पर signal भेजता है"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

def fetch_gsheet_data():
    """Google Sheets से data लाता है या TEST_MODE में dummy data देता है"""
    if TEST_MODE:
        return [
            ["Symbol", "Open", "High", "Low", "Close", "Time"],
            ["INFY", 1500, 1510, 1495, 1508, "2025-08-09 09:20:00"],
            ["INFY", 1508, 1515, 1500, 1516, "2025-08-09 09:25:00"],
            ["TCS",  3450, 3465, 3440, 3438, "2025-08-09 09:20:00"],
            ["TCS",  3438, 3445, 3420, 3418, "2025-08-09 09:25:00"]
        ]
    else:
        creds = Credentials.from_service_account_file(
            "service_account.json", scopes=SCOPES
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GSHEET_ID).worksheet(SHEET_NAME)
        return sheet.get_all_values()

def process_nse_cash(sheet_data):
    """Simple breakout strategy"""
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

    # Ensure numeric
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    signals = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        if row['Close'] > prev['High']:
            signals.append(f"BUY {row['Symbol']} at {row['Close']} ({row.get('Time', 'NA')})")
        elif row['Close'] < prev['Low']:
            signals.append(f"SELL {row['Symbol']} at {row['Close']} ({row.get('Time', 'NA')})")

    return signals

# ===== MAIN =====
if __name__ == "__main__":
    sheet_data = fetch_gsheet_data()
    signals = process_nse_cash(sheet_data)

    if signals:
        for sig in signals:
            print(sig)
            send_telegram_message(sig)
    else:
        print("No signals found.")

