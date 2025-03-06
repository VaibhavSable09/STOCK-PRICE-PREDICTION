import streamlit as st

# Reminder to run the app using the command: streamlit run main.py [ARGUMENTS]
from utils.auth import create_user, get_user_by_username
import pandas as pd
from utils.data_handler import StockDataHandler
from utils.visualizations import StockVisualizer
from utils.prediction import StockPredictor
import os

# Page config
st.set_page_config(
    page_title="Stock Market Analysis Platform",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None

# Main content
if not st.session_state.logged_in:
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1>Welcome to Stock Market Analysis Platform</h1>
        <p class="hero-subtitle">Your Advanced Tool for Stock Market Analysis and Predictions</p>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("### 📊 Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>Real-Time Analysis</h4>
            <p>Get instant access to real-time stock data and market trends</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>AI-Powered Predictions</h4>
            <p>Advanced machine learning models for price prediction</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>Interactive Charts</h4>
            <p>Visualize market data with interactive charts and indicators</p>
        </div>
        """, unsafe_allow_html=True)

    # Authentication tabs
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                user = get_user_by_username(username)
                if user and user.check_password(password):
                    st.success("Login successful!")
                    st.session_state.username = username
                    login()
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")

            if submit:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    try:
                        create_user(new_username, new_email, new_password)
                        st.success("Account created successfully! Please login.")
                    except Exception as e:
                        st.error("Username or email already exists")

else:
    # Header
    col1, col2 = st.columns([3,1])
    with col1:
        st.title("📈 Stock Market Analysis Dashboard")
        st.markdown(f"Welcome back, {st.session_state.username}!")
    with col2:
        if st.button("Logout"):
            logout()
            st.rerun()

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

        if data:
            # Display company info
            info = data["info"]
            st.markdown(f"### {info.get('longName', symbol)}")
            st.markdown(f"*{info.get('sector', '')} | {info.get('industry', '')}*")

            # Current price and change
            current_price = data["history"]["Close"].iloc[-1]
            price_change = current_price - data["history"]["Close"].iloc[-2]
            price_change_pct = (price_change / data["history"]["Close"].iloc[-2]) * 100

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
            historical_data = data["history"]

            # Generate predictions
            prediction_days = int(prediction_months * 30.44)  # Average days per month
            predictions = StockPredictor.predict_future(historical_data, prediction_days)

            # Create combined chart
            chart = StockVisualizer.create_stock_chart(historical_data, predictions)
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
            st.error("Failed to fetch stock data. Please check the symbol and try again. Ensure that the stock symbol is valid and try again later.")
