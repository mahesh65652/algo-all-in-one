import os
import base64
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


def update_signal(data):
    # 1️⃣ Decode Google service account creds
    creds_b64 = os.environ.get("GSHEET_CRED_B64")
    if not creds_b64:
        print("❌ GSHEET_CRED_B64 not set")
        return

    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    with open("temp_creds.json", "w") as f:
        f.write(creds_json)

    # 2️⃣ Authorize and connect
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("temp_creds.json", scope)
    client = gspread.authorize(creds)

    # 3️⃣ Open the spreadsheet and worksheet
    sheet_id = os.environ.get("GSHEET_ID")
    if not sheet_id:
        print("❌ GSHEET_ID not set")
        return

    spreadsheet = client.open_by_key(sheet_id)
    try:
        sheet = spreadsheet.worksheet("LIVE_DATA")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="LIVE_DATA", rows="100", cols="10")

    # 4️⃣ Clear and add headers
    sheet.clear()
    sheet.append_row(["Symbol", "Price", "Time"])

    # 5️⃣ Append data rows
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for row in data:
        sheet.append_row([row["symbol"], row["price"], now])

    print("✅ Google Sheet updated.")

    # 6️⃣ Clean up
    os.remove("temp_creds.json")

    # 7️⃣ Telegram notification
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        message = f"📊 *GSheet Update Done*\n\n" + "\n".join(
            [f"🟢 {r['symbol']} @ ₹{r['price']}" for r in data]
        ) + f"\n🕒 {now}"

        res = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        )

        if res.status_code == 200:
            print("📬 Telegram message sent")
        else:
            print("❌ Telegram failed:", res.text)
    else:
        print("⚠️ Telegram credentials not set")

