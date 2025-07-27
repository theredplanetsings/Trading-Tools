import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/01/2025"

class SMABacktester():
    """
    A class to backtest a short & long-term moving average strategy against a buying & holding strategy.

    Attributes
    ----------
    symbol : str
        The stock symbol to be tested.
    SMA_S : int
        The period for the short-term moving average.
    SMA_L : int
        The period for the long-term moving average.
    start : str
        The start date for the historical data.
    end : str
        The end date for the historical data.
    results : DataFrame
        The DataFrame containing the backtest results.
        
    Methods
    -------
    get_data():
        Downloads historical stock data and calculates the necessary columns for the strategy.
    test_results():
        Generates trading signals, calculates strategy returns, and compares them to a buy-and-hold strategy.
    plot_results():
        Plots the cumulative returns of the buy-and-hold strategy and the moving average crossover strategy.
    """
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        """
        Constructs all the necessary attributes for the SMABacktester object.
        
        Parameters
        ----------
        symbol : str
            The stock symbol to be tested.
        SMA_S : int
            The period for the short-term moving average.
        SMA_L : int
            The period for the long-term moving average.
        start : str
            The start date for the historical data.
        end : str
            The end date for the historical data.
        """
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        self.get_data()

    def get_data(self):
        """
        Downloads historical stock data and calculates the necessary columns for the strategy.

        Returns
        -------
        DataFrame
            A DataFrame containing the historical stock data, daily logarithmic returns, and moving averages.
        """
        # grab historical stock data for our date range
        df = yf.download(self.symbol, start = self.start, end = self.end)

        # yfinance can be a bit inconsistent with column names, so let's handle that
        if 'Close' in df.columns:
            close_col = 'Close'
        elif 'Adj Close' in df.columns:
            close_col = 'Adj Close'
        else:
            # if neither exists, just grab the first price column we can find
            price_cols = [col for col in df.columns if col in ['Open', 'High', 'Low', 'Close', 'Adj Close']]
            if price_cols:
                close_col = price_cols[0]
            else:
                raise ValueError("No price columns found in the data")

        # set up our dataframe with just the closing prices
        data = pd.DataFrame(df[close_col])
        data.columns = ['Close']  # make sure the column name is consistent
        
        # work out daily log returns
        data['returns'] = np.log(data['Close'].div(data['Close'].shift(1)))
        # calculate the short-term moving average
        data['SMA_S'] = data['Close'].rolling(int(self.SMA_S)).mean()
        # calculate the long-term moving average  
        data['SMA_L'] = data['Close'].rolling(int(self.SMA_L)).mean()

        # clean up any rows with missing data
        data.dropna(inplace = True)
        # save this data for later use
        self.data2 = data
        return data

    def test_results(self):
        """
        Generates trading signals, calculates strategy returns, and compares them to a buy-and-hold strategy.

        Returns
        -------
        tuple
            A tuple containing the performance of the strategy and its outperformance compared to the buy-and-hold strategy.
        """
        # work with a copy of our prepared data
        data = self.data2.copy().dropna()
        # create trading signals based on moving average crossovers:
        # 1 means buy (short MA above long MA)
        # -1 means sell (short MA below long MA)
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        # calculate how our strategy performs based on these positions
        data['strategy'] = data['returns'] * data['position'].shift(1)
        data.dropna(inplace=True)
        # work out cumulative returns for both buy & hold and our strategy
        data['returnsB&H'] = data['returns'].cumsum().apply(np.exp)
        data['returnstrategy'] = data['strategy'].cumsum().apply(np.exp)

        # see how well our strategy performed
        perf = data['returnstrategy'].iloc[-1]
        outperf = perf - data['returnsB&H'].iloc[-1]

        # save the results for plotting later
        self.results = data
        
        # calculate some extra stats we might need
        ret = np.exp(data['strategy'].sum())
        std = data['strategy'].std() * np.sqrt(252)
        # return how well we did compared to just buying and holding
        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        """
        Plots the cumulative returns of the buy-and-hold strategy and the moving average crossover strategy.
        """
        if self.results is None:
            print("Run the test please")
        else:
            title = "{} | SMA_S = {} | SMA_L{}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[['returnsB&H','returnstrategy']].plot(title = title, figsize = (12,8))
            plt.show()
            
def test_case():
    """
    A test case to demonstrate the functionality of the SMABacktester class.
    """
    # create an instance to test the strategy on NVIDIA with 1 vs 200 day moving averages
    test = SMABacktester('NVDA', 1, 200, "2000-01-01", "2025-01-04")
    test.test_results()
    test.plot_results()

if __name__ == '__main__':
    test_case()
