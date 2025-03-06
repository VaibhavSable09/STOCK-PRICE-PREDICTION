import streamlit as st
import pandas as pd
from utils.data_handler import StockDataHandler
from utils.visualizations import StockVisualizer
from utils.prediction import StockPredictor
from utils.auth import get_user_by_username
import os

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access the dashboard")
    st.stop()

# Page config
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3,1])
with col1:
    st.title("📈 Stock Analysis Dashboard")
    st.markdown(f"Welcome back, {st.session_state.username}!")

# Input section
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL)", value="AAPL").upper()
with col2:
    period = st.selectbox(
        "Historical Data Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )
with col3:
    prediction_months = st.number_input("Prediction Period (months)", min_value=1, max_value=12, value=6)

# Fetch data
if symbol:
    data = StockDataHandler.get_stock_data(symbol, period)

    if data and not data["history"].empty:
        # Display company info
        info = data["info"]
        st.markdown(f"### {info.get('longName', symbol)}")
        st.markdown(f"*{info.get('sector', '')} | {info.get('industry', '')}*")

        # Current price and change
        historical_data = data["history"]
        if len(historical_data) >= 2:  # Check if we have enough data points
            current_price = historical_data["Close"].iloc[-1]
            price_change = current_price - historical_data["Close"].iloc[-2]
            price_change_pct = (price_change / historical_data["Close"].iloc[-2]) * 100

            metrics_container = st.container()
            with metrics_container:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${current_price:.2f}", 
                            f"{price_change:+.2f} ({price_change_pct:+.2f}%)")

            # Key metrics
            st.subheader("Key Metrics")
            metrics = StockDataHandler.get_key_metrics(info)
            cols = st.columns(3)
            for i, (metric, value) in enumerate(metrics.items()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{metric}</h4>
                        <p>{value}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Stock chart with predictions
            st.subheader("Price Chart & Predictions")

            # Add prediction button
            if st.button("Generate Price Predictions"):
                with st.spinner("Generating predictions..."):
                    # Generate predictions
                    prediction_days = int(prediction_months * 30.44)  # Average days per month
                    predictions = StockPredictor.predict_future(historical_data, prediction_days)

                    # Create combined chart
                    chart = StockVisualizer.create_stock_chart(historical_data, predictions)
                    st.plotly_chart(chart, use_container_width=True)
            else:
                # Show chart without predictions
                chart = StockVisualizer.create_stock_chart(historical_data)
                st.plotly_chart(chart, use_container_width=True)

            # Download data
            st.subheader("Download Data")
            csv = data["history"].to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{symbol}_stock_data.csv",
                mime="text/csv"
            )

        else:
            st.warning("Not enough historical data available for this stock.")
    else:
        st.error("Failed to fetch stock data. Please check the symbol and try again.")