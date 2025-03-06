# Stock Market Analysis Dashboard

A modern financial dashboard for stock analysis that leverages Yahoo Finance data and provides interactive visualization tools. The application offers comprehensive stock insights with multi-page navigation, light theme support, and user-friendly data exploration capabilities.

## Project Structure
```
stock_market_dashboard/
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── pages/
│   ├── 1_📈_Dashboard.py   # Stock analysis dashboard
│   └── 2_👤_Profile.py     # User profile page
├── styles/
│   └── style.css          # Custom CSS styles
├── utils/
│   ├── auth.py            # Authentication utilities
│   ├── data_handler.py    # Stock data management
│   ├── prediction.py      # ML prediction models
│   └── visualizations.py  # Chart creation utilities
├── main.py                # Main application file
├── README.md              # Project documentation
└── setup.sh              # Setup script
```

## Setup Instructions

1. **Prerequisites**
   - Python 3.11 or later
   - PostgreSQL database

2. **Installation**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd stock_market_dashboard

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install required packages
   pip install streamlit pandas yfinance plotly scikit-learn flask-login sqlalchemy psycopg2-binary werkzeug
   ```

3. **Database Setup**
   Create a PostgreSQL database and set the following environment variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/stockdb
   ```

4. **Running the Application**
   ```bash
   streamlit run main.py
   ```
   The application will be available at `http://localhost:5000`

## Features
- Real-time stock data analysis
- Price predictions using machine learning
- Interactive charts and visualizations
- User authentication system
- Light theme support
- Multi-page navigation

## Usage

1. **Authentication**
   - Create an account using the signup form
   - Login with your credentials
   - Access your profile page for account management

2. **Stock Analysis**
   - Enter a stock symbol (e.g., AAPL, GOOGL)
   - Select historical data period
   - Choose prediction timeframe (1-12 months)
   - Click "Generate Price Predictions" for ML-based forecasting
   - Download stock data as CSV

## Dependencies
- streamlit
- pandas
- yfinance
- plotly
- scikit-learn
- flask-login
- sqlalchemy
- psycopg2-binary
- werkzeug

## Development Notes
- The application uses Yahoo Finance API for real-time stock data
- Predictions are based on historical data using Linear Regression
- All data is cached for 5 minutes to optimize performance

## Files Description

### Main Application Files
1. `main.py`: The entry point of the application, handles authentication and landing page
2. `pages/1_📈_Dashboard.py`: Stock analysis dashboard with real-time data and predictions
3. `pages/2_👤_Profile.py`: User profile management page

### Utility Modules
1. `utils/auth.py`: User authentication and database management
2. `utils/data_handler.py`: Stock data fetching and processing
3. `utils/prediction.py`: Machine learning models for stock prediction
4. `utils/visualizations.py`: Chart creation and styling

### Configuration and Styling
1. `.streamlit/config.toml`: Streamlit configuration including theme settings
2. `styles/style.css`: Custom CSS for better UI/UX

## Local Development
1. Clone the repository
2. Install dependencies using `setup.sh` or pip
3. Set up PostgreSQL database
4. Set environment variables
5. Run the application using `streamlit run main.py`
