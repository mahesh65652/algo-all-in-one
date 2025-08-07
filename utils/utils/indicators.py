import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()

def calculate_indicators(sheet_data):
    df = pd.DataFrame(sheet_data)

    # Ensure price column is float
    df["Price"] = pd.to_numeric(df.get("Price", pd.Series([100]*len(df))), errors='coerce').fillna(100)

    # Dummy OI change (replace with real data if needed)
    df["OI Change"] = [5] * len(df)  # replace with live OI data if available

    df["rsi"] = calculate_rsi(df["Price"]).fillna(50)
    df["ema20"] = calculate_ema(df["Price"]).fillna(df["Price"])

    # Update back to list of dicts
    return df.to_dict(orient="records")
