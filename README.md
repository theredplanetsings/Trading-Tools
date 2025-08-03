# Trading Tools Dashboard

A comprehensive Streamlit web application for trading analysis and strategy backtesting. This dashboard integrates multiple powerful trading tools into a single, interactive platform.

## Live Webapp

**[https://tradingtools.streamlit.app/](https://tradingtools.streamlit.app/)**

## Features

- **Stan Weinstein Strategy**: Backtest Stan's 30-week moving average strategy
- **SMA Backtesting**: Test short vs long-term moving average crossover strategies  
- **Risk vs Reward Analysis**: Analyse risk-return profiles of multiple stocks
- **Correlation Heatmap**: Visualise correlations between different stocks
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

## Project Structure

```
Trading-Tools/
├── trading_dashboard.py      # Main Streamlit dashboard application
├── StanWeinstein.py         # Stan Weinstein strategy backtesting class
├── mySMAbacktesting.py      # SMA crossover strategy backtesting class
├── riskvsreward.py          # Risk vs reward analysis script
├── correlationHeatMap.py    # Correlation heatmap generation script
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── LICENCE                 # Project licence
```

## Dependencies

- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `yfinance` - Stock data
- `plotly` - Interactive charts
- `matplotlib` - Additional plotting
- `seaborn` - Statistical visualisation

## Technical Features

- **Object-Oriented Design**: Modular backtesting classes for easy extension and maintenance
- **Interactive Visualisations**: Dynamic Plotly charts with zoom, pan, and hover functionality
- **Statistical Analysis**: Comprehensive performance metrics and correlation matrices
- **Responsive Web Interface**: Mobile-friendly Streamlit dashboard with intuitive navigation
- **Scalable Architecture**: Easily extensible codebase for adding new trading strategies

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
3. View heatmap for portfolio diversification insights

## Deployment

### Streamlit Cloud (Recommended)
1. Upload files to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy automatically

### Required Files for Deployment:
- `trading_dashboard.py` - Main application entry point
- `StanWeinstein.py` - Stan Weinstein strategy implementation
- `mySMAbacktesting.py` - SMA backtesting functionality
- `requirements.txt` - Python dependencies
- `README.md` - Documentation

### Optional Files:
- `riskvsreward.py` - Standalone risk analysis script
- `correlationHeatMap.py` - Standalone correlation analysis script

## Performance Metrics

The dashboard calculates key financial metrics:

- **Total Returns**: Strategy vs buy-and-hold comparison
- **Volatility Analysis**: Risk assessment through standard deviation
- **Sharpe Ratios**: Risk-adjusted return calculations
- **Maximum Drawdown**: Worst peak-to-trough decline analysis
- **Win Rate**: Percentage of profitable trades

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Licence

Creative Commons Zero v1.0 Universal (CC0) - Public domain dedication for maximum freedom

## Author

- GitHub: [@theredplanetsings](https://github.com/theredplanetsings)