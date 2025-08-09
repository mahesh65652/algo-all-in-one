def place_order(symbol, price, side="SELL"):
    # ✅ यहाँ real broker API call करें (AngelOne)
    print(f"🟢 Placing {side} order: {symbol} @ ₹{price}")

    # 🔄 Google Sheet + Telegram update
    from utils.gsheet import update_trade_log
    update_trade_log(symbol, price, side)

def get_live_data(symbol):
    """
    यह फंक्शन किसी symbol का live data (जैसे current price) fetch करेगा।
    अभी यहाँ dummy डेटा दे रहा हूँ ताकि रन हो सके।
    """
    print(f"Fetching live data for {symbol}")
    # असली API कॉल यहां होगी (Angel One API integration)
    return {"price": 123.45}  # dummy price

def place_order(symbol, price, side="SELL"):
    """
    यह फंक्शन order place करने का काम करेगा।
    अभी यहाँ सिर्फ print कर रहा हूँ ताकि पता चले कि call हुआ।
    """
    print(f"🟢 Placing {side} order: {symbol} @ ₹{price}")

    # Google Sheet या Telegram में trade log update करने के लिए import
    from utils.gsheet import update_trade_log
    update_trade_log(symbol, price, side)
