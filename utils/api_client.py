"""
API Client - Handles stock data fetching from Alpha Vantage (Cross-platform compatible)
"""
import requests
import pandas as pd
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
BASE_URL = "https://www.alphavantage.co/query"

class StockAPIClient:
    """Client for fetching stock data from Alpha Vantage API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client
        
        Args:
            api_key: Alpha Vantage API key (uses env var if not provided)
        """
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY', API_KEY)
        self.base_url = "https://www.alphavantage.co/query"
    
    def fetch_intraday_data(self, symbol: str, interval: str = "5min") -> Optional[pd.DataFrame]:
        """
        Fetch intraday stock data
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            
        Returns:
            DataFrame with stock data or None if request fails
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key,
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "Time Series (5min)" in data:
                df = pd.DataFrame(data["Time Series (5min)"]).transpose()
                df.columns = ["Open", "High", "Low", "Close", "Volume"]
                df = df.astype(float)
                return df
            elif "Error Message" in data or "Note" in data:
                return None
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
    
    def fetch_daily_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Fetch daily stock data
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            DataFrame with stock data or None if request fails
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "Time Series (Daily)" in data:
                df = pd.DataFrame(data["Time Series (Daily)"]).transpose()
                df.columns = ["Open", "High", "Low", "Close", "Volume"]
                df = df.astype(float)
                return df
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
