import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/01/2025"

# bunch of stock tickers to analyse
stock_tickers = [
    "SPY",   # S&P 500 ETF
    "AMZN",  # Amazon
    "GOOGL", # Google (Alphabet Class A)
    "BABA",  # Alibaba
    "TSLA",  # Tesla
    "BRK-B", # Berkshire Hathaway Class B
    "NVDA",  # NVIDIA
    "JPM",   # JPMorgan Chase
    "JNJ",   # Johnson & Johnson
    "V",     # Visa
    "PG",    # Procter & Gamble
    "UNH",   # UnitedHealth Group
    "HD",    # Home Depot
    "MA",    # Mastercard
    "ORCL",  # Oracle
    "PYPL",  # PayPal
    "NFLX",  # Netflix
    "INTC",  # Intel
    "IBM",   # IBM
    "ADBE"   # Adobe
]

# put them in alphabetical order to keep things tidy
tickers_sorted = sorted(stock_tickers)
# grab stock data from yfinance - just need adjusted close prices
stocks = yf.download(tickers_sorted, start="2020-01-01", end="2023-01-01")['Adj Close']

# normalise all prices to start at 100 so we can compare them fairly
norm_close = stocks.div(stocks.iloc[0]).mul(100)
norm_close.plot(figsize=(15, 8), fontsize=12)
plt.legend(fontsize=12)
plt.show()

# work out daily returns for each stock
returns = stocks.pct_change().dropna()

# create a summary table with mean and standard deviation
summary = returns.describe().T.loc[:, ["mean", "std"]]

# scale up to annual figures (252 trading days per year)
summary["mean"] = summary["mean"] * 252
summary["std"] = summary["std"] * np.sqrt(252)

# create a scatter plot showing risk vs reward
summary.plot.scatter(x = 'std', y = 'mean', figsize = (15, 8), fontsize = 12)
for i in summary.index:
    plt.annotate(i, xy = (summary.loc[i, "std"] + 0.002, summary.loc[i, "mean"] + 0.002), size = 11)
plt.xlabel("Annual risk (std)", fontsize = 15)
plt.ylabel("Annual return", fontsize = 15)
plt.title("Risk/return", fontsize = 25)
plt.show()
