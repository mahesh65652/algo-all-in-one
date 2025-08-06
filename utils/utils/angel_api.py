def place_order(symbol, price, side="SELL"):
    # ✅ यहाँ real broker API call करें (AngelOne)
    print(f"🟢 Placing {side} order: {symbol} @ ₹{price}")

    # 🔄 Google Sheet + Telegram update
    from utils.gsheet import update_trade_log
    update_trade_log(symbol, price, side)
