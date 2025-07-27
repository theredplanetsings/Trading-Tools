import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

# put them in alphabetical order to make the chart cleaner
tickers_sorted = sorted(stock_tickers)
# grab stock data from yfinance for our date range - just need adjusted close prices
stocks = yf.download(tickers_sorted, start = "2020-01-01", end = "2023-01-01")['Adj Close']

# work out how correlated each stock is with every other stock
corr_matrix = stocks.corr()

# create a nice heatmap to visualise the correlations
plt.figure(figsize = (14, 10))
sns.heatmap(corr_matrix, annot = True, cmap='Reds', vmin = -1, vmax = 1,
            xticklabels = tickers_sorted, yticklabels = tickers_sorted)
plt.title('Stock Correlation Heatmap')
plt.xticks(rotation = 45, ha = 'right')
plt.yticks(rotation = 0)
plt.show()

# find stocks that don't move together much (good for diversification)
low_corr_threshold = 0.4
# take away 1 because each stock is perfectly correlated with itself (obviously!)
low_corr_counts = (np.abs(corr_matrix) < low_corr_threshold).sum(axis = 1) - 1 

# show which stocks have the most low correlations (best for diversifying)
for ticker in tickers_sorted:
    low_corr_tickers = corr_matrix.index[(np.abs(corr_matrix[ticker]) < low_corr_threshold)
    & (corr_matrix.index != ticker)].tolist()
    count = len(low_corr_tickers)
    print(f"{ticker}: {count} low correlations with {low_corr_tickers}")
