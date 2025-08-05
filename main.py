🟩 main.py

from utils.gsheet import read_google_sheet, update_signal
from utils.angel_api import get_live_data, place_order
from utils.indicators import calculate_indicators
from nse.cash_stocks import process_nse_cash
from mcx.mcx_data import process_mcx
from options.option_chain import process_options

if __name__ == "__main__":
    sheet_data = read_google_sheet()
    sheet_data = calculate_indicators(sheet_data)

    process_nse_cash(sheet_data)
    process_mcx(sheet_data)
    process_options(sheet_data)

    update_signal(sheet_data)

