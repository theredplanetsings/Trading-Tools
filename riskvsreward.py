import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/01/2025"

# list of stock tickers
stock_tickers = [
    "SPY",   # SPDR S&P 500 ETF Trust
    "AMZN",  # Amazon.com, Inc.
    "GOOGL", # Alphabet Inc. (Class A)
    "BABA",  # Alibaba Group Holding Limited.
    "TSLA",  # Tesla, Inc.
    "BRK-B", # Berkshire Hathaway Inc. (Class B)
    "NVDA",  # NVIDIA Corporation
    "JPM",   # JPMorgan Chase & Co.
    "JNJ",   # Johnson & Johnson
    "V",     # Visa Inc.
    "PG",    # Procter & Gamble Co.
    "UNH",   # UnitedHealth Group Incorporated
    "HD",    # The Home Depot, Inc.
    "MA",    # Mastercard Incorporated
    "ORCL",  # Oracle Corporation
    "PYPL",  # PayPal Holdings, Inc.
    "NFLX",  # Netflix, Inc.
    "INTC",  # Intel Corporation
    "IBM",   # International Business Machines Corporation
    "ADBE"   # Adobe Inc.
]

# sorts tickers alphabetically
tickers_sorted = sorted(stock_tickers)

# download stock data
stocks = yf.download(tickers_sorted, start="2020-01-01", end="2023-01-01")['Adj Close']

# normalises the stock prices
norm_close = stocks.div(stocks.iloc[0]).mul(100)
norm_close.plot(figsize=(15, 8), fontsize=12)
plt.legend(fontsize=12)
plt.show()

# calculates daily returns
returns = stocks.pct_change().dropna()

# initialises a summary DataFrame
summary = returns.describe().T.loc[:, ["mean", "std"]]

# annualises the mean return and standard deviation
summary["mean"] = summary["mean"] * 252
summary["std"] = summary["std"] * np.sqrt(252)

# plots the risk vs reward
summary.plot.scatter(x = 'std', y = 'mean', figsize = (15, 8), fontsize = 12)
for i in summary.index:
    plt.annotate(i, xy = (summary.loc[i, "std"] + 0.002, summary.loc[i, "mean"] + 0.002), size = 11)
plt.xlabel("Annual risk (std)", fontsize = 15)
plt.ylabel("Annual return", fontsize = 15)
plt.title("Risk/return", fontsize = 25)
plt.show()
