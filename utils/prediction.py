import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import streamlit as st

class StockPredictor:
    @staticmethod
    def prepare_data(data):
        """Prepare data for prediction"""
        try:
            df = data.copy()
            # Drop any rows with missing values
            df = df.dropna()

            if len(df) < 10:  # Require at least 10 data points
                st.error("Not enough historical data for prediction (minimum 10 days required)")
                return None, None

            # Create target variable (next day's closing price)
            df['Target'] = df['Close'].shift(-1)
            df = df.dropna()

            # Create features
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['RSI'] = StockPredictor.calculate_rsi(df['Close'])

            # Additional features
            df['Daily_Return'] = df['Close'].pct_change()
            df['Volatility'] = df['Daily_Return'].rolling(window=5).std()

            features = ['Close', 'Volume', 'SMA_5', 'SMA_20', 'RSI', 'Volatility']
            df = df.dropna()  # Remove any rows with NaN after feature creation

            if len(df) == 0:
                st.error("No valid data points after preparation")
                return None, None

            return df[features].values, df['Target'].values
        except Exception as e:
            st.error(f"Error preparing data: {str(e)}")
            return None, None

    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calculate RSI indicator"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        except Exception:
            return pd.Series(index=prices.index)

    @staticmethod
    def predict_future(data, periods):
        """Predict future stock prices"""
        try:
            X, y = StockPredictor.prepare_data(data)

            if X is None or y is None:
                return None

            if len(X) < 2:
                st.error("Not enough valid data points for prediction")
                return None

            # Train model
            model = LinearRegression()
            model.fit(X, y)

            # Prepare future prediction data
            last_data = X[-1:].copy()  # Use the last observation
            predictions = []
            dates = []

            # Predict for each future period
            current_data = last_data.copy()
            for i in range(periods):
                try:
                    pred = model.predict(current_data)[0]
                    predictions.append(pred)

                    # Generate future date
                    next_date = data.index[-1] + timedelta(days=i+1)
                    dates.append(next_date)

                    # Update features for next prediction
                    current_data[0][0] = pred  # Update Close price
                    # Update other features based on prediction
                    if i >= 4:  # Update SMA_5 after 5 predictions
                        current_data[0][2] = np.mean(predictions[-5:])
                    if i >= 19:  # Update SMA_20 after 20 predictions
                        current_data[0][3] = np.mean(predictions[-20:])
                except Exception as e:
                    st.error(f"Error in prediction loop: {str(e)}")
                    break

            if len(predictions) > 0:
                return pd.Series(predictions, index=dates)
            return None

        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")
            return None