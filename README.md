# Trading-Tools

This repository contains Python programs to produce a correlational heatmap, calculate the risk vs reward of a given list of stocks, and backtest both a short & long-term moving average strategy and Stan Weinstein's strategy against a buying & holding strategy.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [StanWeinstein.py](#stanweinsteinpy)
  - [riskvsreward.py](#riskvsrewardpy)
  - [mySMAbacktesting.py](#mysmabacktestingpy)
  - [correlationHeatMap.py](#correlationheatmappy)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/theredplanetsings/Trading-Tools.git
   cd Trading-Tools

2. Install the required packages:
    ```bash
    pip install requirements.txt

# Usage

### `StanWeinstein.py`

This script backtests Stan Weinstein's strategy against a buying & holding strategy

**Instructions**

1. Open the StanWeinstein.py file.
2. Modify the test_case() function to specify the stock symbol, start date, and end date.
3. Run the script to see the backtest results and plot

### `mySMAbacktesting.py`

This script backtests a short & long-term moving average strategy against a buying & holding strategy.

**Instructions**

1. Open the mySMAbacktesting.py file.
2. Modify the test_case() function to specify the stock symbol, short-term SMA period, long-term SMA period, start date, and end date.
3. Run the script to see the backtest results and plot.

### `riskvsreward.py`

This script calculates the risk vs reward of a given list of stocks.

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

# Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

# License

This project is licensed under the Creative Commons Zero v1.0 Universal. See the LICENSE file for details.
