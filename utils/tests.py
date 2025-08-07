def test_calculate_indicators():
    dummy_data = [
        {"Symbol": "INFY", "Price": 100},
        {"Symbol": "INFY", "Price": 102},
        {"Symbol": "INFY", "Price": 104},
        {"Symbol": "INFY", "Price": 106},
        {"Symbol": "INFY", "Price": 108},
        {"Symbol": "INFY", "Price": 110},
        {"Symbol": "INFY", "Price": 112},
        {"Symbol": "INFY", "Price": 114},
        {"Symbol": "INFY", "Price": 116},
        {"Symbol": "INFY", "Price": 118},
        {"Symbol": "INFY", "Price": 120},
        {"Symbol": "INFY", "Price": 122},
        {"Symbol": "INFY", "Price": 124},
        {"Symbol": "INFY", "Price": 126},
        {"Symbol": "INFY", "Price": 128},
    ]
    result = calculate_indicators(dummy_data)
    assert "rsi" in result[0]
    assert "ema20" in result[0]
