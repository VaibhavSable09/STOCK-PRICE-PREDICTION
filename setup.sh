#!/bin/bash

echo "Setting up Stock Market Analysis Dashboard..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing required packages..."
pip install streamlit pandas yfinance plotly scikit-learn flask-login sqlalchemy psycopg2-binary werkzeug

# Create necessary directories
echo "Creating project directories..."
mkdir -p .streamlit pages styles utils

# Create .streamlit config if it doesn't exist
if [ ! -d ".streamlit" ]; then
    mkdir .streamlit
    echo "Creating Streamlit configuration..."
    cat > .streamlit/config.toml << EOL
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
EOL
fi

echo "Setup completed successfully!"
echo "To start the application:"
echo "1. Make sure PostgreSQL is running"
echo "2. Set up your database environment variables"
echo "3. Run: streamlit run main.py"