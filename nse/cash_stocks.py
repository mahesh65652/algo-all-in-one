TEST_MODE = True

def fetch_gsheet_data():
    if TEST_MODE:
        return [
            ["Symbol", "Open", "High", "Low", "Close", "Time"],
            ["INFY",  1500, 1510, 1495, 1508, "2025-08-09 09:20:00"],
            ["INFY",  1508, 1515, 1500, 1516, "2025-08-09 09:25:00"],
            ["TCS",   3450, 3465, 3440, 3438, "2025-08-09 09:20:00"],
            ["TCS",   3438, 3445, 3420, 3418, "2025-08-09 09:25:00"]
        ]
    else:
        # यहां Google Sheets से data लाने का असली code होगा
        pass

if __name__ == "__main__":
    sheet_data = fetch_gsheet_data()
    signals = process_nse_cash(sheet_data)
    print(signals)


process_nse_cash(sheet_data)

def process_nse_cash(sheet_data):
    """
    NSE cash stocks के लिए simple breakout strategy लागू करता है।
    Input: sheet_data (list of lists)
    Output: signals (list of dicts)
    """
    import pandas as pd

    # Convert to DataFrame
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])  # skip header

    # Ensure numeric columns
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    signals = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        # Basic breakout logic
        if row['Close'] > prev['High']:
            signals.append({
                'symbol': row['Symbol'],
                'signal': 'BUY',
                'price': row['Close'],
                'time': row.get('Time', 'NA')
            })
        elif row['Close'] < prev['Low']:
            signals.append({
                'symbol': row['Symbol'],
                'signal': 'SELL',
                'price': row['Close'],
                'time': row.get('Time', 'NA')
            })

    return signals
