# Trading Tools Dashboard

Streamlit web app for trading analysis and strategy backtesting. Dashboard integrates multiple trading tools into a single platform.

## Live Webapp

**[https://tradingtools.streamlit.app/](https://tradingtools.streamlit.app/)**

## Features

- **Stan Weinstein Strategy**: Backtest the famous 30-week moving average strategy
- **SMA Backtesting**: Test short vs long-term moving average crossover strategies  
- **Risk vs Reward Analysis**: Analyse risk-return profiles of multiple stocks
- **Correlation Heatmap**: Visualise correlations between different stocks
- **Interactive Charts**: Beautiful, interactive plots powered by Plotly
- **Real-time Data**: Live stock data from Yahoo Finance

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/theredplanetsings/Trading-Tools.git
   cd Trading-Tools
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run trading_dashboard.py
   ```

4. **Open your browser** to `http://localhost:8501`

## Dependencies

- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `yfinance` - Stock data
- `plotly` - Interactive charts
- `matplotlib` - Additional plotting
- `seaborn` - Statistical visualisation

## Usage

### Stan Weinstein Strategy
1. Enter a stock symbol (e.g., AAPL, TSLA)
2. Select your date range
3. Click "Run Analysis" to see strategy performance vs buy & hold

### SMA Backtesting
1. Enter stock symbol and moving average periods
2. Choose date range
3. View performance comparison and trading signals

### Risk vs Reward
1. Enter multiple stock symbols (one per line)
2. Set analysis period
3. Explore risk-return scatter plot and statistics

### Correlation Analysis
1. Input stock symbols for correlation analysis
2. Adjust correlation threshold
3. View heatmap and diversification insights

## Deployment

### Streamlit Cloud (Recommended)
1. Upload files to GitHub
2. Connect repo to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy automatically

### Required Files for Deployment:
- `trading_dashboard.py`
- `StanWeinstein.py`
- `mySMAbacktesting.py`  
- `requirements.txt`
- `README.md`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Licence

This project is licensed under the MIT Licence - see the [LICENSE](LICENSE) file for details.

## Author

- GitHub: [@theredplanetsings](https://github.com/theredplanetsings)

## Acknowledgements

- Yahoo Finance for providing free stock data
- Streamlit team for the amazing framework
- Plotly for interactive visualisations

**Instructions**

1. Open the riskvsreward.py file.
2. Modify the stocks, start, and end variables to specify the list of stocks and the date range.
3. Run the script to see the risk vs reward plot.

### `correlationHeatMap.py`

This script produces a correlational heatmap for a given list of stocks.

**Instructions**

1. Open the correlationHeatMap.py file.
2. Modify the stocks, start, and end variables to specify the list of stocks and the date range.
3. Run the script to see the correlation heatmap.

# License

This project is licensed under the Creative Commons Zero v1.0 Universal. See the LICENSE file for details.
