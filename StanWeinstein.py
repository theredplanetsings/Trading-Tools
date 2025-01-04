import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/01/2024"

class StanWeinsteinTester():
    """
    A class to backtest Stan Weinstein's strategy against a buying & holding strategy.

    Attributes
    ----------
    symbol : str
        The stock symbol to be tested.
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
        Plots the cumulative returns of the buy-and-hold strategy and Stan Weinstein's strategy.
    """
    def __init__(self, symbol, start, end):
        """
        Constructs all the necessary attributes for the StanWeinsteinTester object.

        Parameters
        ----------
        symbol : str
            The stock symbol to be tested.
        start : str
            The start date for the historical data.
        end : str
            The end date for the historical data.
        """
        self.symbol = symbol
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
            A DataFrame containing the historical stock data, daily logarithmic returns, and the 30-week moving average.
        """
        # download historical stock data across a given date range
        frame = yf.download(self.symbol, start = self.start, end = self.end)

        # initialise dataframe with the closing price of the stock
        dataSW = pd.DataFrame(frame['Close'])

        # calculate daily logarithmic returns
        dataSW['returns'] = np.log(frame['Close'].div(frame['Close'].shift(1)))
        # 30 week moving avg (30 weeks * 5 trading days)
        dataSW['SMA_30'] = frame['Close'].rolling(window = 30 * 5).mean()
        # drop any rows with 'NaN' values
        dataSW.dropna(inplace = True)

        #store the data in an instance variable
        self.data2 = dataSW
        return dataSW
    
    def test_results(self):
        """
        Generates trading signals, calculates strategy returns, and compares them to a buy-and-hold strategy.

        Returns
        -------
        tuple
            A tuple containing the performance of the strategy and its outperformance compared to the buy-and-hold strategy.
        """
        dataSW = self.data2.copy().dropna()
        #trading signal: 1 for long (closing price > 30-week SMA)
        # -1 for short (closing price < 30-week SMA)
        dataSW['position'] = np.where(dataSW['Close'] > dataSW['SMA_30'], 1, -1)
        #calculate strategy returns based on position
        dataSW['strategy'] = dataSW['returns'] * dataSW['position'].shift(1)
        dataSW.dropna(inplace = True)

        #calculate the cumulative returns for buying and holding vs strategy
        dataSW['returnsB&H'] = dataSW['returns'].cumsum().apply(np.exp)
        dataSW['returnstrategy'] = dataSW['strategy'].cumsum().apply(np.exp)

        # calculates the performance of the strategy
        perf = dataSW['returnstrategy'].iloc[-1]
        outperf = perf - dataSW['returnsB&H'].iloc[-1]

        #store data in an instance variable
        self.results = dataSW

        #calculate total return & stdev of the strategy
        ret = np.exp(dataSW['strategy'].sum())
        std = dataSW['strategy'].std() * np.sqrt(252)

        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        """
        Plots the cumulative returns of the buy-and-hold strategy and Stan Weinstein's strategy.
        """
        if self.results is None:
            print("Run the test!")
        else:
            title = "{} | Weinstein Strategy".format(self.symbol)
            self.results[['returnsB&H', 'returnstrategy']].plot(title = title, figsize = (12,8))
            plt.show()

def test_case():
    """
    A test case to demonstrate the functionality of the StanWeinsteinTester class.
    """
    # instance of the class to test the strategy
    test = StanWeinsteinTester('NVDA', "2000-01-01", "2025-01-04")
    test.test_results()
    test.plot_results()

if __name__ == '__main__':
    test_case()
