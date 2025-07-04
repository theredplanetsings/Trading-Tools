import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

__author__ = "https://github.com/theredplanetsings"
__date__ = "04/07/2025"

# Import your existing classes with error handling
try:
    from StanWeinstein import StanWeinsteinTester
except ImportError:
    st.error("StanWeinstein module not found. Please ensure all files are in the same directory.")
    StanWeinsteinTester = None
try:
    from mySMAbacktesting import SMABacktester
except ImportError:
    st.error("mySMAbacktesting module not found. Please ensure all files are in the same directory.")
    SMABacktester = None

# Configure Streamlit page
st.set_page_config(
    page_title="Trading Tools Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📈 Trading Tools Dashboard")
page = st.sidebar.radio(
    "Choose a Tool",
    ["🏠 Home", "📊 Stan Weinstein Strategy", "📈 SMA Backtesting", "⚖️ Risk vs Reward", "🔥 Correlation Heatmap"]
)

def get_stock_info(symbol):
    """Get basic stock information"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A')
        }
    except:
        return {'name': symbol, 'sector': 'N/A', 'industry': 'N/A', 'market_cap': 'N/A'}

def format_currency(value):
    """Format large numbers as currency"""
    if isinstance(value, (int, float)) and value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif isinstance(value, (int, float)) and value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif isinstance(value, (int, float)):
        return f"${value:,.2f}"
    else:
        return str(value)

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🏠 Trading Tools Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to your comprehensive trading analysis dashboard! This application combines multiple powerful 
    trading tools to help you analyze stocks, backtest strategies, and make informed investment decisions.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛠️ Available Tools")
        st.markdown("""
        - **📊 Stan Weinstein Strategy**: Backtest the famous 30-week moving average strategy
        - **📈 SMA Backtesting**: Test short vs long-term moving average crossover strategies  
        - **⚖️ Risk vs Reward**: Analyze risk-return profiles of multiple stocks
        - **🔥 Correlation Heatmap**: Visualize correlations between different stocks
        """)
    
    with col2:
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. Select a tool from the sidebar
        2. Enter your stock symbols and parameters
        3. Choose your date range
        4. Run the analysis and view results
        5. Download or save your charts and data
        """)
    
    # Quick market overview
    st.markdown("### 📊 Quick Market Overview")
    major_indices = ['SPY', 'QQQ', 'DIA', 'IWM']
    
    try:
        data = yf.download(major_indices, period="1d", interval="1d")['Close']
        prev_data = yf.download(major_indices, period="2d", interval="1d")['Close']
        
        cols = st.columns(len(major_indices))
        for i, symbol in enumerate(major_indices):
            with cols[i]:
                current_price = data[symbol].iloc[-1]
                prev_price = prev_data[symbol].iloc[-2]
                change = current_price - prev_price
                change_pct = (change / prev_price) * 100
                
                color = "success-metric" if change >= 0 else "danger-metric"
                st.markdown(f"""
                <div class="metric-card {color}">
                    <h4>{symbol}</h4>
                    <p><strong>${current_price:.2f}</strong></p>
                    <p>{change:+.2f} ({change_pct:+.2f}%)</p>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.info("Market data temporarily unavailable")

# STAN WEINSTEIN STRATEGY PAGE
elif page == "📊 Stan Weinstein Strategy":
    st.markdown('<h1 class="main-header">📊 Stan Weinstein Strategy Backtester</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    The Stan Weinstein strategy uses a 30-week (150-day) moving average to determine market trends.
    When the stock price is above the 30-week MA, it's a buy signal. When below, it's a sell signal.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Strategy Parameters")
        
        symbol = st.text_input("Stock Symbol", "NVDA", help="Enter a valid stock ticker (e.g., AAPL, TSLA)")
        
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Start Date", date(2020, 1, 1))
        with col_date2:
            end_date = st.date_input("End Date", date.today())
        
        if st.button("🚀 Run Stan Weinstein Analysis", type="primary"):
            if symbol and start_date < end_date:
                with st.spinner("Analyzing strategy performance..."):
                    try:
                        # Get stock info
                        stock_info = get_stock_info(symbol)
                        
                        # Run the analysis
                        tester = StanWeinsteinTester(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                        perf, outperf = tester.test_results()
                        
                        # Display stock info
                        st.markdown("### 📋 Stock Information")
                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.write(f"**Company:** {stock_info['name']}")
                            st.write(f"**Sector:** {stock_info['sector']}")
                        with info_col2:
                            st.write(f"**Industry:** {stock_info['industry']}")
                            st.write(f"**Market Cap:** {format_currency(stock_info['market_cap'])}")
                        
                        # Display results
                        st.markdown("### 📊 Strategy Performance")
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            buy_hold_return = tester.results['returnsB&H'].iloc[-1]
                            st.metric("Buy & Hold Return", f"{buy_hold_return:.2%}", f"{buy_hold_return-1:.2%}")
                        
                        with metric_col2:
                            st.metric("Strategy Return", f"{perf:.2%}", f"{perf-1:.2%}")
                        
                        with metric_col3:
                            color = "normal" if outperf >= 0 else "inverse"
                            st.metric("Outperformance", f"{outperf:.2%}", f"{outperf:.2%}", delta_color=color)
                        
                        # Success/failure indicator
                        if outperf > 0:
                            st.success(f"🎉 Strategy outperformed buy & hold by {outperf:.2%}!")
                        else:
                            st.warning(f"⚠️ Strategy underperformed buy & hold by {abs(outperf):.2%}")
                        
                        # Store results in session state for plotting
                        st.session_state['weinstein_results'] = tester.results
                        st.session_state['weinstein_symbol'] = symbol
                        
                    except Exception as e:
                        st.error(f"Error running analysis: {str(e)}")
            else:
                st.error("Please enter a valid symbol and date range")
    
    with col2:
        st.markdown("### 📈 Performance Chart")
        
        if 'weinstein_results' in st.session_state:
            results = st.session_state['weinstein_results']
            symbol = st.session_state['weinstein_symbol']
            
            # Create interactive plot with Plotly
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=results.index,
                y=results['returnsB&H'],
                mode='lines',
                name='Buy & Hold',
                line=dict(color='blue', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=results.index,
                y=results['returnstrategy'],
                mode='lines',
                name='Weinstein Strategy',
                line=dict(color='red', width=2)
            ))
            
            fig.update_layout(
                title=f"{symbol} - Stan Weinstein Strategy vs Buy & Hold",
                xaxis_title="Date",
                yaxis_title="Cumulative Returns",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show recent signals
            st.markdown("### 📡 Recent Trading Signals")
            recent_signals = results.tail(10)[['Close', 'SMA_30', 'position']].copy()
            recent_signals['Signal'] = recent_signals['position'].map({1: '🟢 Long', -1: '🔴 Short'})
            recent_signals['Close'] = recent_signals['Close'].round(2)
            recent_signals['SMA_30'] = recent_signals['SMA_30'].round(2)
            recent_signals = recent_signals[['Close', 'SMA_30', 'Signal']]
            st.dataframe(recent_signals, use_container_width=True)
        else:
            st.info("👆 Run an analysis to see the performance chart and trading signals")

# SMA BACKTESTING PAGE
elif page == "📈 SMA Backtesting":
    st.markdown('<h1 class="main-header">📈 SMA Crossover Strategy Backtester</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Test moving average crossover strategies by comparing short-term vs long-term moving averages.
    When the short MA crosses above the long MA, it's a buy signal. When it crosses below, it's a sell signal.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Strategy Parameters")
        
        symbol = st.text_input("Stock Symbol", "AAPL", help="Enter a valid stock ticker")
        
        sma_col1, sma_col2 = st.columns(2)
        with sma_col1:
            sma_short = st.number_input("Short MA Period", min_value=1, max_value=200, value=20, step=1)
        with sma_col2:
            sma_long = st.number_input("Long MA Period", min_value=1, max_value=500, value=50, step=1)
        
        if sma_short >= sma_long:
            st.error("Short MA period must be less than Long MA period")
        
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Start Date", date(2020, 1, 1), key="sma_start")
        with col_date2:
            end_date = st.date_input("End Date", date.today(), key="sma_end")
        
        if st.button("🚀 Run SMA Analysis", type="primary"):
            if symbol and start_date < end_date and sma_short < sma_long:
                with st.spinner("Analyzing SMA crossover strategy..."):
                    try:
                        # Get stock info
                        stock_info = get_stock_info(symbol)
                        
                        # Run the analysis
                        tester = SMABacktester(symbol, sma_short, sma_long, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                        perf, outperf = tester.test_results()
                        
                        # Display stock info
                        st.markdown("### 📋 Stock Information")
                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.write(f"**Company:** {stock_info['name']}")
                            st.write(f"**Sector:** {stock_info['sector']}")
                        with info_col2:
                            st.write(f"**Industry:** {stock_info['industry']}")
                            st.write(f"**Market Cap:** {format_currency(stock_info['market_cap'])}")
                        
                        # Display results
                        st.markdown("### 📊 Strategy Performance")
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            buy_hold_return = tester.results['returnsB&H'].iloc[-1]
                            st.metric("Buy & Hold Return", f"{buy_hold_return:.2%}", f"{buy_hold_return-1:.2%}")
                        
                        with metric_col2:
                            st.metric("Strategy Return", f"{perf:.2%}", f"{perf-1:.2%}")
                        
                        with metric_col3:
                            color = "normal" if outperf >= 0 else "inverse"
                            st.metric("Outperformance", f"{outperf:.2%}", f"{outperf:.2%}", delta_color=color)
                        
                        # Success/failure indicator
                        if outperf > 0:
                            st.success(f"🎉 Strategy outperformed buy & hold by {outperf:.2%}!")
                        else:
                            st.warning(f"⚠️ Strategy underperformed buy & hold by {abs(outperf):.2%}")
                        
                        # Store results in session state for plotting
                        st.session_state['sma_results'] = tester.results
                        st.session_state['sma_symbol'] = symbol
                        st.session_state['sma_short'] = sma_short
                        st.session_state['sma_long'] = sma_long
                        
                    except Exception as e:
                        st.error(f"Error running analysis: {str(e)}")
            else:
                st.error("Please check your inputs and ensure short MA < long MA")
    
    with col2:
        st.markdown("### 📈 Performance Chart")
        
        if 'sma_results' in st.session_state:
            results = st.session_state['sma_results']
            symbol = st.session_state['sma_symbol']
            sma_short = st.session_state['sma_short']
            sma_long = st.session_state['sma_long']
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📊 Returns Comparison", "📈 Price & Moving Averages"])
            
            with tab1:
                # Performance comparison chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=results.index,
                    y=results['returnsB&H'],
                    mode='lines',
                    name='Buy & Hold',
                    line=dict(color='blue', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=results.index,
                    y=results['returnstrategy'],
                    mode='lines',
                    name=f'SMA Strategy ({sma_short}/{sma_long})',
                    line=dict(color='red', width=2)
                ))
                
                fig.update_layout(
                    title=f"{symbol} - SMA Strategy vs Buy & Hold",
                    xaxis_title="Date",
                    yaxis_title="Cumulative Returns",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Price and moving averages chart
                fig2 = go.Figure()
                
                fig2.add_trace(go.Scatter(
                    x=results.index,
                    y=results['Close'],
                    mode='lines',
                    name='Price',
                    line=dict(color='black', width=1)
                ))
                
                fig2.add_trace(go.Scatter(
                    x=results.index,
                    y=results['SMA_S'],
                    mode='lines',
                    name=f'SMA {sma_short}',
                    line=dict(color='orange', width=1)
                ))
                
                fig2.add_trace(go.Scatter(
                    x=results.index,
                    y=results['SMA_L'],
                    mode='lines',
                    name=f'SMA {sma_long}',
                    line=dict(color='green', width=1)
                ))
                
                fig2.update_layout(
                    title=f"{symbol} - Price and Moving Averages",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            # Show recent signals
            st.markdown("### 📡 Recent Trading Signals")
            recent_signals = results.tail(10)[['Close', 'SMA_S', 'SMA_L', 'position']].copy()
            recent_signals['Signal'] = recent_signals['position'].map({1: '🟢 Long', -1: '🔴 Short'})
            recent_signals['Close'] = recent_signals['Close'].round(2)
            recent_signals['SMA_S'] = recent_signals['SMA_S'].round(2)
            recent_signals['SMA_L'] = recent_signals['SMA_L'].round(2)
            recent_signals = recent_signals[['Close', 'SMA_S', 'SMA_L', 'Signal']]
            st.dataframe(recent_signals, use_container_width=True)
        else:
            st.info("👆 Run an analysis to see the performance charts and trading signals")

# RISK VS REWARD PAGE
elif page == "⚖️ Risk vs Reward":
    st.markdown('<h1 class="main-header">⚖️ Risk vs Reward Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze the risk-return profile of multiple stocks to make informed portfolio decisions.
    This tool calculates annualized returns and volatility for each stock.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Analysis Parameters")
        
        # Default stock list
        default_stocks = ["SPY", "AMZN", "GOOGL", "TSLA", "NVDA", "AAPL", "MSFT", "JPM", "JNJ", "V"]
        
        stock_input = st.text_area(
            "Stock Symbols (one per line)",
            value="\n".join(default_stocks),
            height=200,
            help="Enter stock symbols, one per line"
        )
        
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Start Date", date(2020, 1, 1), key="risk_start")
        with col_date2:
            end_date = st.date_input("End Date", date.today(), key="risk_end")
        
        if st.button("📊 Analyze Risk vs Reward", type="primary"):
            stock_list = [stock.strip().upper() for stock in stock_input.split('\n') if stock.strip()]
            
            if len(stock_list) < 2:
                st.error("Please enter at least 2 stock symbols")
            elif start_date >= end_date:
                st.error("Start date must be before end date")
            else:
                with st.spinner("Downloading data and calculating metrics..."):
                    try:
                        # Download stock data
                        stocks = yf.download(stock_list, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))['Adj Close']
                        
                        if stocks.empty:
                            st.error("No data found for the specified stocks and date range")
                            st.stop()
                        
                        # Handle single stock case
                        if len(stock_list) == 1:
                            stocks = stocks.to_frame()
                            stocks.columns = stock_list
                        
                        # Calculate daily returns
                        returns = stocks.pct_change().dropna()
                        
                        # Calculate summary statistics
                        summary = returns.describe().T.loc[:, ["mean", "std"]]
                        summary["mean"] = summary["mean"] * 252  # Annualize
                        summary["std"] = summary["std"] * np.sqrt(252)  # Annualize
                        summary["sharpe"] = summary["mean"] / summary["std"]  # Sharpe ratio
                        
                        # Store in session state
                        st.session_state['risk_summary'] = summary
                        st.session_state['risk_stocks'] = stocks
                        st.session_state['risk_returns'] = returns
                        
                        st.success(f"✅ Analysis complete for {len(stock_list)} stocks!")
                        
                    except Exception as e:
                        st.error(f"Error downloading data: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Risk vs Reward Chart")
        
        if 'risk_summary' in st.session_state:
            summary = st.session_state['risk_summary']
            
            # Create interactive scatter plot
            fig = px.scatter(
                summary,
                x='std',
                y='mean',
                hover_name=summary.index,
                hover_data={'sharpe': ':.3f'},
                title="Risk vs Return Analysis",
                labels={'std': 'Annual Risk (Standard Deviation)', 'mean': 'Annual Return'}
            )
            
            # Add text annotations
            for i, ticker in enumerate(summary.index):
                fig.add_annotation(
                    x=summary.loc[ticker, 'std'],
                    y=summary.loc[ticker, 'mean'],
                    text=ticker,
                    showarrow=True,
                    arrowhead=1,
                    yshift=10
                )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display summary table
            st.markdown("### 📋 Summary Statistics")
            summary_display = summary.copy()
            summary_display['mean'] = summary_display['mean'].apply(lambda x: f"{x:.2%}")
            summary_display['std'] = summary_display['std'].apply(lambda x: f"{x:.2%}")
            summary_display['sharpe'] = summary_display['sharpe'].round(3)
            summary_display.columns = ['Annual Return', 'Annual Risk', 'Sharpe Ratio']
            
            # Color coding based on Sharpe ratio
            def color_sharpe(val):
                if val > 1:
                    return 'background-color: #d4edda'  # Green
                elif val > 0.5:
                    return 'background-color: #fff3cd'  # Yellow
                else:
                    return 'background-color: #f8d7da'  # Red
            
            styled_df = summary_display.style.applymap(color_sharpe, subset=['Sharpe Ratio'])
            st.dataframe(styled_df, use_container_width=True)
            
        else:
            st.info("👆 Run an analysis to see the risk vs reward chart and statistics")
        
        # Best/Worst performers
        if 'risk_summary' in st.session_state:
            summary = st.session_state['risk_summary']
            
            col_best, col_worst = st.columns(2)
            
            with col_best:
                st.markdown("### 🏆 Best Performers")
                best_return = summary.loc[summary['mean'].idxmax()]
                best_sharpe = summary.loc[summary['sharpe'].idxmax()]
                
                st.write(f"**Highest Return:** {best_return.name} ({best_return['mean']:.2%})")
                st.write(f"**Best Sharpe Ratio:** {best_sharpe.name} ({best_sharpe['sharpe']:.3f})")
            
            with col_worst:
                st.markdown("### ⚠️ Highest Risk")
                highest_risk = summary.loc[summary['std'].idxmax()]
                lowest_sharpe = summary.loc[summary['sharpe'].idxmin()]
                
                st.write(f"**Highest Risk:** {highest_risk.name} ({highest_risk['std']:.2%})")
                st.write(f"**Lowest Sharpe:** {lowest_sharpe.name} ({lowest_sharpe['sharpe']:.3f})")

# CORRELATION HEATMAP PAGE
elif page == "🔥 Correlation Heatmap":
    st.markdown('<h1 class="main-header">🔥 Stock Correlation Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze correlations between different stocks to understand how they move together.
    High correlations suggest stocks move in similar directions, while low correlations indicate diversification benefits.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Analysis Parameters")
        
        # Default stock list
        default_stocks = ["SPY", "AMZN", "GOOGL", "BABA", "TSLA", "NVDA", "JPM", "JNJ", "V", "PG", "UNH", "HD", "MA", "ORCL", "NFLX", "INTC", "IBM", "ADBE"]
        
        stock_input = st.text_area(
            "Stock Symbols (one per line)",
            value="\n".join(default_stocks),
            height=250,
            help="Enter stock symbols, one per line"
        )
        
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Start Date", date(2020, 1, 1), key="corr_start")
        with col_date2:
            end_date = st.date_input("End Date", date.today(), key="corr_end")
        
        low_corr_threshold = st.slider("Low Correlation Threshold", 0.0, 1.0, 0.4, 0.1)
        
        if st.button("🔥 Generate Correlation Analysis", type="primary"):
            stock_list = [stock.strip().upper() for stock in stock_input.split('\n') if stock.strip()]
            
            if len(stock_list) < 2:
                st.error("Please enter at least 2 stock symbols")
            elif start_date >= end_date:
                st.error("Start date must be before end date")
            else:
                with st.spinner("Downloading data and calculating correlations..."):
                    try:
                        # Download stock data
                        stocks = yf.download(stock_list, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))['Adj Close']
                        
                        if stocks.empty:
                            st.error("No data found for the specified stocks and date range")
                            st.stop()
                        
                        # Calculate correlation matrix
                        corr_matrix = stocks.corr()
                        
                        # Calculate low correlation counts
                        low_corr_counts = (np.abs(corr_matrix) < low_corr_threshold).sum(axis=1) - 1
                        
                        # Store in session state
                        st.session_state['corr_matrix'] = corr_matrix
                        st.session_state['corr_stocks'] = stocks
                        st.session_state['low_corr_counts'] = low_corr_counts
                        st.session_state['low_corr_threshold'] = low_corr_threshold
                        
                        st.success(f"✅ Correlation analysis complete for {len(stock_list)} stocks!")
                        
                    except Exception as e:
                        st.error(f"Error downloading data: {str(e)}")
    
    with col2:
        st.markdown("### 🔥 Correlation Heatmap")
        
        if 'corr_matrix' in st.session_state:
            corr_matrix = st.session_state['corr_matrix']
            
            # Create interactive heatmap with Plotly
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdYlBu_r',
                title="Stock Correlation Heatmap"
            )
            
            fig.update_layout(
                height=600,
                xaxis_title="",
                yaxis_title="",
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("👆 Generate a correlation analysis to see the heatmap")
    
    # Low correlation analysis
    if 'corr_matrix' in st.session_state:
        st.markdown("### 📊 Diversification Analysis")
        
        col_div1, col_div2 = st.columns(2)
        
        with col_div1:
            st.markdown("#### 🎯 Best Diversifiers")
            low_corr_counts = st.session_state['low_corr_counts']
            threshold = st.session_state['low_corr_threshold']
            
            # Sort by most low correlations
            best_diversifiers = low_corr_counts.sort_values(ascending=False).head(5)
            
            for ticker, count in best_diversifiers.items():
                st.write(f"**{ticker}:** {count} low correlations (< {threshold})")
        
        with col_div2:
            st.markdown("#### 🔗 Highest Correlations")
            corr_matrix = st.session_state['corr_matrix']
            
            # Find highest correlations (excluding self-correlations)
            mask = np.triu(np.ones_like(corr_matrix), k=1).astype(bool)
            high_corr = corr_matrix.where(mask).stack().sort_values(ascending=False).head(5)
            
            for (stock1, stock2), corr_val in high_corr.items():
                st.write(f"**{stock1} - {stock2}:** {corr_val:.3f}")
        
        # Detailed correlation table
        st.markdown("### 📋 Detailed Correlation Analysis")
        
        # Create a summary of low correlations for each stock
        threshold = st.session_state['low_corr_threshold']
        summary_data = []
        
        for ticker in corr_matrix.index:
            low_corr_tickers = corr_matrix.index[
                (np.abs(corr_matrix[ticker]) < threshold) & (corr_matrix.index != ticker)
            ].tolist()
            count = len(low_corr_tickers)
            summary_data.append({
                'Stock': ticker,
                'Low Correlations Count': count,
                'Low Correlation Partners': ', '.join(low_corr_tickers[:5]) + ('...' if len(low_corr_tickers) > 5 else '')
            })
        
        summary_df = pd.DataFrame(summary_data).sort_values('Low Correlations Count', ascending=False)
        st.dataframe(summary_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    📈 Trading Tools Dashboard | Built with Streamlit | 
    <a href='https://github.com/theredplanetsings' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
