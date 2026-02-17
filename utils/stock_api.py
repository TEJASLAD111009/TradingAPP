"""Utility module for fetching stock data using yfinance API."""
import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Tuple
import requests
from datetime import datetime, timedelta


class StockAPI:
    """Handles stock data fetching from free APIs."""
    
    # Popular US stocks for demo
    POPULAR_STOCKS = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'AMZN': 'Amazon.com Inc.',
        'TSLA': 'Tesla Inc.',
        'META': 'Meta Platforms Inc.',
        'NVDA': 'NVIDIA Corporation',
        'JPM': 'JPMorgan Chase & Co.',
        'V': 'Visa Inc.',
        'WMT': 'Walmart Inc.',
        'JNJ': 'Johnson & Johnson',
        'PG': 'Procter & Gamble',
        'KO': 'The Coca-Cola Company',
        'DIS': 'The Walt Disney Company',
        'NFLX': 'Netflix Inc.'
    }
    
    # Exchange rate cache (will be updated dynamically)
    _exchange_rate_cache = None
    _last_update = None
    
    @classmethod
    def get_exchange_rate(cls, force_refresh: bool = False) -> float:
        """Get live USD to INR exchange rate.
        
        Args:
            force_refresh: Force update from API (ignore cache)
            
        Returns:
            Exchange rate (1 USD = X INR)
        """
        # Use cache if available and less than 1 hour old
        if cls._exchange_rate_cache and cls._last_update:
            if not force_refresh and (datetime.now() - cls._last_update).seconds < 3600:
                return cls._exchange_rate_cache
        
        try:
            # Try primary API: exchangerate-api.com (free tier)
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
            if response.status_code == 200:
                data = response.json()
                rate = data.get('rates', {}).get('INR', 83.0)
                cls._exchange_rate_cache = rate
                cls._last_update = datetime.now()
                return rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
        
        # Fallback to cached or default value
        if cls._exchange_rate_cache:
            return cls._exchange_rate_cache
        return 83.0  # Default fallback
    
    @classmethod
    def get_stock_price(cls, symbol: str) -> Optional[Dict]:
        """Get current stock price in USD with INR conversion.
        
        Args:
            symbol: Stock symbol (e.g., AAPL)
            
        Returns:
            Dictionary with stock data or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')
            
            if data.empty:
                return None
            
            info = ticker.info
            
            current_price_usd = data['Close'].iloc[-1]
            exchange_rate = cls.get_exchange_rate()
            current_price_inr = current_price_usd * exchange_rate
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'price_usd': round(current_price_usd, 2),
                'price_inr': round(current_price_inr, 2),
                'currency': 'USD',
                'exchange_rate': round(exchange_rate, 2),
                'change': round(info.get('regularMarketChange', 0), 2),
                'change_percent': round(info.get('regularMarketChangePercent', 0), 2),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'divi_yield': info.get('dividendYield', 'N/A'),
                'updated_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching stock {symbol}: {e}")
            return None
    
    @classmethod
    def get_multiple_stocks(cls, symbols: List[str]) -> Dict[str, Dict]:
        """Get stock prices for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dictionary of symbol: stock_data
        """
        results = {}
        for symbol in symbols:
            data = cls.get_stock_price(symbol)
            if data:
                results[symbol] = data
        return results
    
    @classmethod
    def get_stock_history(cls, symbol: str, period: str = '1mo') -> Optional[pd.DataFrame]:
        """Get historical stock data in USD.
        
        Args:
            symbol: Stock symbol
            period: Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame with historical data (in USD) or None
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            # Data is already in USD, no conversion needed
            return data
        except Exception as e:
            print(f"Error fetching history for {symbol}: {e}")
            return None
    
    @classmethod
    def get_popular_stocks_data(cls) -> Dict[str, Dict]:
        """Get data for all popular stocks.
        
        Returns:
            Dictionary of stock data
        """
        return cls.get_multiple_stocks(list(cls.POPULAR_STOCKS.keys()))
    
    @classmethod
    def get_stock_by_name(cls, name: str) -> Optional[Dict]:
        """Search for a stock by company name or symbol.
        
        Args:
            name: Company name or symbol
            
        Returns:
            Stock data or None
        """
        # Try exact symbol match first
        symbol = name.upper()
        if symbol in cls.POPULAR_STOCKS or len(symbol) <= 5:
            return cls.get_stock_price(symbol)
        
        # Search in POPULAR_STOCKS values
        for symbol, company_name in cls.POPULAR_STOCKS.items():
            if name.lower() in company_name.lower():
                return cls.get_stock_price(symbol)
        
        return None
    
    @classmethod
    def calculate_investment_cost(cls, symbol: str, quantity: int) -> Optional[float]:
        """Calculate total cost to buy a stock (in USD).
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            
        Returns:
            Total cost in USD or None
        """
        stock_data = cls.get_stock_price(symbol)
        if not stock_data:
            return None
        return stock_data['price_usd'] * quantity
    
    @classmethod
    def calculate_sale_proceeds(cls, symbol: str, quantity: int) -> Optional[float]:
        """Calculate proceeds from selling a stock (in USD).
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            
        Returns:
            Total proceeds in USD or None
        """
        stock_data = cls.get_stock_price(symbol)
        if not stock_data:
            return None
        return stock_data['price_usd'] * quantity
