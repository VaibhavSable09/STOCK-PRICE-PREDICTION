import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class StockDataHandler:
    @staticmethod
    @st.cache_data(ttl=300)  # Cache data for 5 minutes
    def get_stock_data(symbol: str, period: str = "1y"):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            hist_data = stock.history(period=period)

            if hist_data.empty:
                st.error(f"No data available for {symbol}")
                return None

            info = stock.info

            return {
                "history": hist_data,
                "info": info
            }
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return None

    @staticmethod
    def format_number(number):
        """Format large numbers with K, M, B suffixes"""
        if number is None:
            return "N/A"

        if number >= 1_000_000_000:
            return f"{number/1_000_000_000:.2f}B"
        elif number >= 1_000_000:
            return f"{number/1_000_000:.2f}M"
        elif number >= 1_000:
            return f"{number/1_000:.2f}K"
        else:
            return f"{number:.2f}"

    @staticmethod
    def get_key_metrics(stock_info):
        """Extract key metrics from stock info"""
        metrics = {
            "Market Cap": stock_info.get("marketCap"),
            "P/E Ratio": stock_info.get("trailingPE"),
            "52 Week High": stock_info.get("fiftyTwoWeekHigh"),
            "52 Week Low": stock_info.get("fiftyTwoWeekLow"),
            "Volume": stock_info.get("volume"),
            "Avg Volume": stock_info.get("averageVolume"),
        }

        return {k: StockDataHandler.format_number(v) for k, v in metrics.items()}