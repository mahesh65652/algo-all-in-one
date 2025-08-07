import pandas as pd

def process_option_chain(sheet_data):
    """
    Process options chain data and return strategy signals.
    Expects sheet_data as list of lists from Google Sheets.
    """
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])  # Skip header

    # Convert numeric fields
    numeric_cols = ['Strike Price', 'Call OI', 'Put OI', 'Call LTP', 'Put LTP']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    signals = []

    # Example Strategy: Max Pain / Highest OI on Call & Put
    call_max_oi = df.loc[df['Call OI'].idxmax()]
    put_max_oi = df.loc[df['Put OI'].idxmax()]

    signals.append({
        'type': 'Call',
        'strike': call_max_oi['Strike Price'],
        'oi': call_max_oi['Call OI'],
        'ltp': call_max_oi['Call LTP']
    })

    signals.append({
        'type': 'Put',
        'strike': put_max_oi['Strike Price'],
        'oi': put_max_oi['Put OI'],
        'ltp': put_max_oi['Put LTP']
    })

    return signals
