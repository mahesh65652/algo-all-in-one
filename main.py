from utils.gsheet import read_google_sheet, update_signal
from utils.angel_api import get_live_data, place_order
from utils.indicators import calculate_indicators
from nse.cash_stocks import process_nse_cash
from mcx.mcx_data import process_mcx
from options.option_chain import process_options

if __name__ == "__main__":
    print("📥 Reading data from Google Sheet...")
    sheet_data = read_google_sheet()

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
    update_signal(all_signals)

    print("✅ All tasks completed.")
