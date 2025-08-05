#RSI, EMA, OI calculation functions

def calculate_indicators(sheet_data):
     #Perform indicator calculations
    return sheet_data
tests/test_indicators.py

from utils.indicators import calculate_indicators

def test_calculate_indicators():
    dummy_data = [{"symbol": "RELIANCE"}]
    result = calculate_indicators(dummy_data)
    assert "rsi" in result[0]
    assert result[0]["rsi"] == 50
