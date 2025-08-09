utils/gsheet.py
import base64
import json
import gspread
from google.oauth2.service_account import Credentials
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def read_google_sheet(sheet_id, sheet_name):
    """Google Sheet से data पढ़ता है"""
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)

    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return sheet.get_all_values()

def update_signal(sheet_id, sheet_name, cell_range, values):
    """Google Sheet में data update करता है"""
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)

    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    sheet.update(cell_range, values)
