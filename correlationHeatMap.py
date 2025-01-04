import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/01/2024"

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

# downloads stock data across a given date range
stocks = yf.download(tickers_sorted, start = "2020-01-01", end = "2023-01-01")['Adj Close']

# calculates the correlation matrix
corr_matrix = stocks.corr()

# plots the heatmap
plt.figure(figsize = (14, 10))
sns.heatmap(corr_matrix, annot = True, cmap='Reds', vmin = -1, vmax = 1,
            xticklabels = tickers_sorted, yticklabels = tickers_sorted)
plt.title('Stock Correlation Heatmap')
plt.xticks(rotation = 45, ha = 'right')
plt.yticks(rotation = 0)
plt.show()

# identifies stocks with more low correlation scores
low_corr_threshold = 0.4
# subtract 1 to exclude self-correlation
low_corr_counts = (np.abs(corr_matrix) < low_corr_threshold).sum(axis = 1) - 1 

# prints stocks with their low correlation counts
for ticker in tickers_sorted:
    low_corr_tickers = corr_matrix.index[(np.abs(corr_matrix[ticker]) < low_corr_threshold)
    & (corr_matrix.index != ticker)].tolist()
    count = len(low_corr_tickers)
    print(f"{ticker}: {count} low correlations with {low_corr_tickers}")
