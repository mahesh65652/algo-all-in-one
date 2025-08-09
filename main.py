
from utils.gsheet import read_google_sheet, update_signal
from utils.angel_api import get_live_data, place_order
from utils.indicators import calculate_indicators
from nse.cash_stocks import process_nse_cash
import os

if __name__ == "__main__":
    SHEET_ID = os.environ.get("GSHEET_ID")
    SHEET_NAME = "LIVE DATA"  # जरूरत हो तो बदल सकते हो

    print("📥 Reading data from Google Sheet...")
    sheet_data = read_google_sheet(SHEET_ID, SHEET_NAME)

    print("🧮 Calculating indicators...")
    sheet_data = calculate_indicators(sheet_data)

    print("📊 Processing NSE cash stocks...")
    nse_signals = process_nse_cash(sheet_data)

    print("📤 Updating Google Sheet with signals...")
    update_signal(SHEET_ID, SHEET_NAME, "J2", nse_signals)  
    # "J2" वो cell range है जहाँ से signals लिखने हैं

    print("✅ NSE strategy completed successfully
