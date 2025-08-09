utils/gsheet.py
import gsheet
import os
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

def get_gsheet_client():
    """Google Sheets API client बनाता है (Base64 creds से)"""
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    if not creds_b64:
        raise ValueError("❌ Missing GSHEET_CRED_B64 environment variable")

    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    return client


def read_google_sheet(sheet_id, sheet_name):
    """Google Sheet से data पढ़ता है"""
    if TEST_MODE:
        print("🧪 TEST_MODE ON - Dummy data वापिस कर रहा हूँ")
        return [
            ["Symbol", "Open", "High", "Low", "Close", "Time"],
            ["INFY",  1500, 1510, 1495, 1508, "2025-08-09 09:20:00"],
            ["INFY",  1508, 1515, 1500, 1516, "2025-08-09 09:25:00"],
            ["TCS",   3450, 3465, 3440, 3438, "2025-08-09 09:20:00"],
            ["TCS",   3438, 3445, 3420, 3418, "2025-08-09 09:25:00"]
        ]

    client = get_gsheet_client()
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return sheet.get_all_values()


def update_signal(sheet_id, sheet_name, start_cell, signals):
    """Signals को Google Sheet में update करता है"""
    if TEST_MODE:
        print("🧪 TEST_MODE ON - Signals update simulate हो रहा है")
        print(signals)
        return

    client = get_gsheet_client()
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

    # Signals को 2D list में बदलना
    values = [["Symbol", "Signal", "Price", "Time"]]
    for s in signals:
        values.append([s.get("symbol"), s.get("signal"), s.get("price"), s.get("time")])

    sheet.update(start_cell, values)

