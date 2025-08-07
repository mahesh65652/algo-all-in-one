import pandas as pd

def process_mcx(sheet_data):
    """
    MCX strategy to generate BUY/SELL signal based on breakout logic.
    Input: sheet_data (list of lists from Google Sheet)
    Returns: List of signals (dict)
    """
    # Convert to DataFrame
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])  # Skip header

    # Convert price columns to numeric
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    signals = []

    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i - 1]

        if current['Close'] > previous['High']:
            signals.append({
                'symbol': current.get('Symbol', 'MCX'),
                'signal': 'BUY',
                'price': current['Close'],
                'time': current.get('Time', 'NA')
            })
        elif current['Close'] < previous['Low']:
            signals.append({
                'symbol': current.get('Symbol', 'MCX'),
                'signal': 'SELL',
                'price': current['Close'],
                'time': current.get('Time', 'NA')
            })

    return signals
