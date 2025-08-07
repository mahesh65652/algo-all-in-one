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
