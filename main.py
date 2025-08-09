from utils.gsheet import read_google_sheet, update_signal
from utils.angel_api import get_live_data, place_order
from utils.indicators import calculate_indicators
from nse.cash_stocks import process_nse_cash
from mcx.mcx_data import process_mcx
from options.option_chain import process_options
import os

if __name__ == "__main__":
    SHEET_ID = os.environ.get("GSHEET_ID")
    SHEET_NAME = "Sheet1"  # जरूरत हो तो बदल सकते हो

    print("📥 Reading data from Google Sheet...")
    sheet_data = read_google_sheet(SHEET_ID, SHEET_NAME)

    print("🧮 Calculating indicators...")
    sheet_data = calculate_indicators(sheet_data)

    print("📊 Processing NSE cash stocks...")
    nse_signals = process_nse_cash(sheet_data)

    print("⚙️ Processing MCX data...")
    mcx_signals = process_mcx(sheet_data)

    print("📈 Processing options chain...")
    option_signals = process_options(sheet_data)

    print("🧾 Merging all signals...")
    all_signals = nse_signals + mcx_signals + option_signals

    print("📤 Updating Google Sheet with signals...")
    update_signal(SHEET_ID, SHEET_NAME, "J2", all_signals)  
    # "J2" वो cell range है जहाँ से signals लिखने हैं, adjust कर सकते हो

    print("✅ All tasks completed.")
