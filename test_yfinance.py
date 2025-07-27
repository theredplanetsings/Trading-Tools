#!/usr/bin/env python3
"""
Test script to verify yfinance data structure handling
"""

import yfinance as yf
import pandas as pd

def test_yfinance_structure():
    print("Testing yfinance data structures...")
    
    # Test single stock
    print("\n1. Testing single stock (AAPL):")
    single_data = yf.download("AAPL", start="2024-01-01", end="2024-01-10")
    print(f"Columns: {list(single_data.columns)}")
    print(f"Is MultiIndex: {isinstance(single_data.columns, pd.MultiIndex)}")
    
    # Test multiple stocks
    print("\n2. Testing multiple stocks (AAPL, MSFT):")
    multi_data = yf.download(["AAPL", "MSFT"], start="2024-01-01", end="2024-01-10")
    print(f"Columns: {list(multi_data.columns)}")
    print(f"Is MultiIndex: {isinstance(multi_data.columns, pd.MultiIndex)}")
    
    if isinstance(multi_data.columns, pd.MultiIndex):
        print(f"Level 0 (symbols): {list(multi_data.columns.get_level_values(0).unique())}")
        print(f"Level 1 (metrics): {list(multi_data.columns.get_level_values(1).unique())}")
        
        # Test accessing Close data
        if 'Close' in multi_data.columns.get_level_values(1):
            close_data = multi_data['Close']
            print(f"Close data shape: {close_data.shape}")
            print(f"Close columns: {list(close_data.columns)}")
        
        if 'Adj Close' in multi_data.columns.get_level_values(1):
            adj_close_data = multi_data['Adj Close']
            print(f"Adj Close data shape: {adj_close_data.shape}")
            print(f"Adj Close columns: {list(adj_close_data.columns)}")

def simulate_dashboard_logic():
    print("\n\n=== Simulating Dashboard Logic ===")
    
    # Simulate the risk vs reward logic
    stock_list = ["AAPL", "MSFT", "GOOGL"]
    raw_data = yf.download(stock_list, start="2024-01-01", end="2024-01-10")
    
    print(f"Raw data columns: {list(raw_data.columns)}")
    print(f"Is MultiIndex: {isinstance(raw_data.columns, pd.MultiIndex)}")
    
    # Apply our logic
    try:
        if isinstance(raw_data.columns, pd.MultiIndex):
            print("MultiIndex detected")
            if 'Adj Close' in raw_data.columns.get_level_values(1):
                stocks = raw_data['Adj Close']
                print("Using Adj Close")
            elif 'Close' in raw_data.columns.get_level_values(1):
                stocks = raw_data['Close']
                print("Using Close")
            else:
                print("ERROR: No price columns found")
                return
        else:
            print("Flat columns detected")
            if 'Adj Close' in raw_data.columns:
                stocks = raw_data[['Adj Close']]
                stocks.columns = stock_list
                print("Using Adj Close")
            elif 'Close' in raw_data.columns:
                stocks = raw_data[['Close']]
                stocks.columns = stock_list
                print("Using Close")
            else:
                print("ERROR: No price columns found")
                return
        
        print(f"Final stocks data shape: {stocks.shape}")
        print(f"Final stocks columns: {list(stocks.columns)}")
        print("SUCCESS: Data processing completed!")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_yfinance_structure()
    simulate_dashboard_logic()
