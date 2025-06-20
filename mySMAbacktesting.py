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
        # downloads historical stock data across a given date range
        df = yf.download(self.symbol, start = self.start, end = self.end)

        #initialise dataframe with the closing price of the stock
        data = pd.DataFrame(df['Close'])
        # calculate daily logarithmic returns
        data['returns'] = np.log(df['Close'].div(data['Close'].shift(1)))

        # shorter-term moving average (SMA_S)
        data['SMA_S'] = df['Close'].rolling(int(self.SMA_S)).mean()
        # longer-term moving average (SMA_L)
        data['SMA_L'] = df['Close'].rolling(int(self.SMA_L)).mean()

        # drop any rows with 'NaN' values
        data.dropna(inplace = True)
        # store the data in an instance variable & return
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
        # copy the previously-prepared data
        data = self.data2.copy().dropna()
        # generate trading signals:
        # 1 for long (SMA_S > SMA_L)
        # -1 for short (SMA_S < SMA_L)
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        # calculate strategy returns based on position
        data['strategy'] = data['returns'] * data['position'].shift(1)
        data.dropna(inplace=True)
        # calculate the cumulative returns for buying and holding vs strategy
        data['returnsB&H'] = data['returns'].cumsum().apply(np.exp)
        data['returnstrategy'] = data['strategy'].cumsum().apply(np.exp)

        # calculate the performance of the strategy
        perf = data['returnstrategy'].iloc[-1]
        outperf = perf - data['returnsB&H'].iloc[-1]

        # store data in an instance variable
        self.results = data
        
        # calculate total return & stdev of the strategy
        ret = np.exp(data['strategy'].sum())
        std = data['strategy'].std() * np.sqrt(252)
        # return the performance and outperformance of the strategy
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
    # instance of the class to test the strategy
    test = SMABacktester('NVDA', 1, 200, "2000-01-01", "2025-01-04")
    test.test_results()
    test.plot_results()

if __name__ == '__main__':
    test_case()
