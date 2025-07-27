#!/usr/bin/env python3
"""
Debug script to test yfinance data fetching for market overview
"""

import yfinance as yf
import pandas as pd

def test_market_data():
    symbols = ['SPY', 'QQQ', 'DIA', 'IWM']
    
    print("Testing yfinance data fetching...")
    print(f"Symbols: {symbols}")
    
    try:
        # Test the exact same call as in the dashboard
        raw_data = yf.download(symbols, period="5d", interval="1d")
        
        print(f"\nData shape: {raw_data.shape}")
        print(f"Columns: {raw_data.columns}")
        print(f"Column type: {type(raw_data.columns)}")
        print(f"Is MultiIndex: {isinstance(raw_data.columns, pd.MultiIndex)}")
        
        if isinstance(raw_data.columns, pd.MultiIndex):
            print(f"Level 0 (symbols): {raw_data.columns.get_level_values(0).unique()}")
            print(f"Level 1 (metrics): {raw_data.columns.get_level_values(1).unique()}")
        
        print(f"\nFirst few rows:")
        print(raw_data.head())
        
        # Test accessing data for each symbol
        for symbol in symbols:
            print(f"\n--- Testing {symbol} ---")
            try:
                if isinstance(raw_data.columns, pd.MultiIndex):
                    if 'Close' in raw_data.columns.get_level_values(1):
                        symbol_data = raw_data[(symbol, 'Close')]
                        print(f"{symbol} Close data (MultiIndex): {symbol_data.tail(2).values}")
                    elif 'Adj Close' in raw_data.columns.get_level_values(1):
                        symbol_data = raw_data[(symbol, 'Adj Close')]
                        print(f"{symbol} Adj Close data (MultiIndex): {symbol_data.tail(2).values}")
                else:
                    # Single symbol case or flat structure
                    if 'Close' in raw_data.columns:
                        symbol_data = raw_data['Close']
                        print(f"{symbol} Close data (flat): {symbol_data.tail(2).values}")
                    elif 'Adj Close' in raw_data.columns:
                        symbol_data = raw_data['Adj Close']
                        print(f"{symbol} Adj Close data (flat): {symbol_data.tail(2).values}")
                
                # Calculate change
                symbol_data = symbol_data.dropna()
                if len(symbol_data) >= 2:
                    current_price = symbol_data.iloc[-1]
                    prev_price = symbol_data.iloc[-2]
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100
                    print(f"{symbol}: ${current_price:.2f} ({change:+.2f}, {change_pct:+.2f}%)")
                else:
                    print(f"{symbol}: Insufficient data")
                    
            except Exception as e:
                print(f"{symbol}: ERROR - {str(e)}")
        
    except Exception as e:
        print(f"Error downloading data: {str(e)}")

if __name__ == "__main__":
    test_market_data()
