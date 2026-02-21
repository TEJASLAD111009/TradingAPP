"""Trading App Configuration - Cross-platform compatible."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Currency Settings
BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USD")
CONVERSION_CURRENCY = os.getenv("CONVERSION_CURRENCY", "INR")

# Initial Wallet Balance for New Users (in USD)
INITIAL_WALLET_BALANCE = float(os.getenv("INITIAL_WALLET_BALANCE", "1000.0"))

# App Settings
APP_NAME = os.getenv("APP_NAME", "Trading App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.1")

# API Keys (from environment variables for security)
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
YFINANCE_ENABLED = os.getenv("YFINANCE_ENABLED", "true").lower() == "true"

# Popular Stocks (can be customized)
POPULAR_STOCKS = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
}
