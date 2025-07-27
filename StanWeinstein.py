import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/01/2025"

class StanWeinsteinTester():
    """
    A class for backtesting Stan Weinstein's strategy against a buying & holding strategy.
    
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
        # grab historical stock data for our date range
        frame = yf.download(self.symbol, start = self.start, end = self.end)

        # yfinance can return data in different formats, so let's sort that out
        if 'Close' in frame.columns:
            close_col = 'Close'
        elif 'Adj Close' in frame.columns:
            close_col = 'Adj Close'
        else:
            # if neither exists, just grab the first price column we can find
            price_cols = [col for col in frame.columns if col in ['Open', 'High', 'Low', 'Close', 'Adj Close']]
            if price_cols:
                close_col = price_cols[0]
            else:
                raise ValueError("No price columns found in the data")

        # set up our dataframe with just the closing prices
        dataSW = pd.DataFrame(frame[close_col])
        dataSW.columns = ['Close']  # make sure the column name is consistent

        # work out daily log returns (fancy way of calculating percentage changes)
        dataSW['returns'] = np.log(dataSW['Close'].div(dataSW['Close'].shift(1)))
        # calculate the 30-week moving average (30 weeks × 5 trading days = 150 days)
        dataSW['SMA_30'] = dataSW['Close'].rolling(window = 30 * 5).mean()
        # get rid of any rows with missing data
        dataSW.dropna(inplace = True)

        # save this data so we can use it later
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
        # create our trading signals: 1 means buy (price above 30-week average)
        # -1 means sell (price below 30-week average) 
        dataSW['position'] = np.where(dataSW['Close'] > dataSW['SMA_30'], 1, -1)
        # work out how our strategy performs based on these positions
        dataSW['strategy'] = dataSW['returns'] * dataSW['position'].shift(1)
        dataSW.dropna(inplace = True)

        # calculate cumulative returns - both for buy & hold and our strategy
        dataSW['returnsB&H'] = dataSW['returns'].cumsum().apply(np.exp)
        dataSW['returnstrategy'] = dataSW['strategy'].cumsum().apply(np.exp)

        # see how well our strategy did
        perf = dataSW['returnstrategy'].iloc[-1]
        outperf = perf - dataSW['returnsB&H'].iloc[-1]

        # save this data for plotting later
        self.results = dataSW

        # calculate some extra stats we might need
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
    # create an instance to test the strategy on NVIDIA
    test = StanWeinsteinTester('NVDA', "2000-01-01", "2025-01-04")
    test.test_results()
    test.plot_results()

if __name__ == '__main__':
    test_case()
