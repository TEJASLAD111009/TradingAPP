"""Utility module for fetching stock data using Alpha Vantage (Primary) and yfinance (Fallback)."""
import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Tuple
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import Alpha Vantage client
from utils.api_client import StockAPIClient


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
                logger.info(f"Successfully fetched exchange rate: 1 USD = ₹{rate:.2f}")
                return rate
        except Exception as e:
            logger.warning(f"Error fetching exchange rate: {e}")
        
        # Fallback to cached or default value
        if cls._exchange_rate_cache:
            logger.info(f"Using cached exchange rate: 1 USD = ₹{cls._exchange_rate_cache:.2f}")
            return cls._exchange_rate_cache
        logger.info("Using default exchange rate: 1 USD = ₹83.0")
        return 83.0  # Default fallback
    
    @classmethod
    def get_stock_price(cls, symbol: str) -> Optional[Dict]:
        """Get current stock price in USD with INR conversion.
        
        Uses Alpha Vantage as primary. On Render, uses demo data if both APIs fail.
        
        Args:
            symbol: Stock symbol (e.g., AAPL)
            
        Returns:
            Dictionary with stock data or None if error
        """
        try:
            logger.info(f"Fetching stock data for: {symbol}")
            
            # Try Alpha Vantage first (if API key is available and not 'demo')
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
            if api_key and api_key != 'demo':
                logger.info(f"Attempting Alpha Vantage for {symbol}")
                result = cls._get_stock_price_from_alpha_vantage(symbol, api_key)
                if result:
                    logger.info(f"Successfully fetched {symbol} from Alpha Vantage: ${result['price_usd']}")
                    return result
                logger.warning(f"Alpha Vantage failed for {symbol}, trying fallback")
            
            # On Render, yfinance is usually blocked - try demo data as fallback
            on_render = os.getenv('RENDER', False)
            if on_render:
                logger.warning(f"On Render: yfinance typically blocked, using demo data for {symbol}")
                return cls._get_demo_stock_data(symbol)
            
            # Fall back to yfinance (for local development)
            logger.info(f"Attempting yfinance for {symbol}")
            result = cls._get_stock_price_from_yfinance(symbol)
            if result:
                logger.info(f"Successfully fetched {symbol} from yfinance: ${result['price_usd']}")
                return result
            
            logger.error(f"All sources failed for {symbol}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching stock {symbol}: {str(e)}")
            return None
    
    @classmethod
    def _get_demo_stock_data(cls, symbol: str) -> Optional[Dict]:
        """Get demo stock data when APIs are unavailable.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Demo stock data with realistic prices
        """
        # Demo data with approximate real prices
        demo_prices = {
            'AAPL': 185.42,
            'MSFT': 330.05,
            'GOOGL': 139.25,
            'AMZN': 173.10,
            'TSLA': 242.84,
            'META': 501.25,
            'NVDA': 875.30,
            'JPM': 198.50,
            'V': 258.75,
            'WMT': 82.45,
            'JNJ': 156.30,
            'PG': 164.20,
            'KO': 60.35,
            'DIS': 92.50,
            'NFLX': 215.45
        }
        
        try:
            symbol_upper = symbol.upper()
            price_usd = demo_prices.get(symbol_upper)
            
            if not price_usd:
                # Random-ish price for unknown symbols (for testing)
                price_usd = 100.0 + (hash(symbol_upper) % 200)
                logger.info(f"Demo: Using generated price for {symbol}")
            
            exchange_rate = cls.get_exchange_rate()
            current_price_inr = price_usd * exchange_rate
            
            result = {
                'symbol': symbol_upper,
                'name': cls.POPULAR_STOCKS.get(symbol_upper, f"{symbol_upper} Inc."),
                'price_usd': round(price_usd, 2),
                'price_inr': round(current_price_inr, 2),
                'currency': 'USD',
                'exchange_rate': round(exchange_rate, 2),
                'change': round((hash(symbol_upper) % 10 - 5) / 10, 2),
                'change_percent': round((hash(symbol_upper) % 5 - 2.5) / 10, 2),
                'market_cap': 'Demo Data',
                'pe_ratio': 'Demo Data',
                'divi_yield': 'Demo Data',
                'updated_at': datetime.now().isoformat()
            }
            logger.info(f"Demo data for {symbol}: ${price_usd} (APIs unavailable on Render)")
            return result
        except Exception as e:
            logger.error(f"Error generating demo data for {symbol}: {str(e)}")
            return None
    
    @classmethod
    def _get_stock_price_from_alpha_vantage(cls, symbol: str, api_key: str) -> Optional[Dict]:
        """Fetch stock price from Alpha Vantage API.
        
        Args:
            symbol: Stock symbol
            api_key: Alpha Vantage API key
            
        Returns:
            Stock data or None
        """
        try:
            client = StockAPIClient(api_key)
            data = client.fetch_daily_data(symbol)
            
            if data is None or data.empty:
                return None
            
            # Get the latest price
            latest_data = data.iloc[0]  # Most recent is first
            current_price_usd = float(latest_data['Close'])
            
            # Fetch additional info from yfinance (for name, market cap, etc.)
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
            except:
                info = {}
            
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
            logger.warning(f"Alpha Vantage error for {symbol}: {str(e)}")
            return None
    
    @classmethod
    def _get_stock_price_from_yfinance(cls, symbol: str) -> Optional[Dict]:
        """Fetch stock price from yfinance API (fallback).
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Stock data or None
        """
        try:
            logger.info(f"yfinance: Fetching {symbol} with 5s timeout")
            ticker = yf.Ticker(symbol)
            # Add timeout to prevent hanging on Render
            data = ticker.history(period='1d', timeout=5)
            
            if data.empty:
                logger.warning(f"yfinance: No data returned for {symbol} (empty response)")
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
            logger.error(f"yfinance error for {symbol}: {str(e)}")
            return None
    
    @classmethod
    def get_multiple_stocks(cls, symbols: List[str]) -> Dict[str, Dict]:
        """Get stock prices for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dictionary of symbol: stock_data
        """
        logger.info(f"Fetching data for {len(symbols)} stocks...")
        results = {}
        for symbol in symbols:
            data = cls.get_stock_price(symbol)
            if data:
                results[symbol] = data
        logger.info(f"Successfully fetched {len(results)}/{len(symbols)} stocks")
        return results
    
    @classmethod
    def get_stock_history(cls, symbol: str, period: str = '1mo') -> Optional[pd.DataFrame]:
        """Get historical stock data in USD.
        
        Tries Alpha Vantage first, falls back to yfinance, then demo data on Render.
        
        Args:
            symbol: Stock symbol
            period: Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame with historical data (in USD) or None
        """
        try:
            logger.info(f"Fetching {period} history for {symbol}")
            
            # Try Alpha Vantage first (if API key is available and not 'demo')
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
            if api_key and api_key != 'demo':
                logger.info(f"Attempting Alpha Vantage history for {symbol}")
                try:
                    client = StockAPIClient(api_key)
                    data = client.fetch_daily_data(symbol)
                    if data is not None and not data.empty:
                        logger.info(f"Successfully fetched {len(data)} records from Alpha Vantage")
                        return data
                except Exception as e:
                    logger.warning(f"Alpha Vantage history failed: {str(e)}")
            
            # On Render, yfinance is usually blocked - use demo data
            on_render = os.getenv('RENDER', False)
            if on_render:
                logger.warning(f"On Render: yfinance typically blocked, using demo history for {symbol}")
                return cls._get_demo_stock_history(symbol)
            
            # Fall back to yfinance (for local development)
            logger.info(f"Attempting yfinance history for {symbol}")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, timeout=5)
            
            if data.empty:
                logger.warning(f"yfinance: No history returned for {symbol}")
                return None
            
            logger.info(f"Successfully fetched history for {symbol}: {len(data)} records")
            return data
        except Exception as e:
            logger.error(f"Error fetching history for {symbol}: {str(e)}")
            return None
    
    @classmethod
    def _get_demo_stock_history(cls, symbol: str) -> Optional[pd.DataFrame]:
        """Generate demo historical stock data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with demo historical data or None
        """
        try:
            from datetime import timedelta
            
            # Generate 30 days of demo data
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            prices = []
            
            base_price = 100 + (hash(symbol) % 200)
            for i in range(30):
                variation = (hash(symbol + str(i)) % 20 - 10) / 100  # ±10%
                price = base_price * (1 + variation)
                prices.append(price)
            
            data = pd.DataFrame({
                'Open': prices,
                'High': [p * 1.02 for p in prices],
                'Low': [p * 0.98 for p in prices],
                'Close': prices,
                'Volume': [1000000] * 30
            }, index=dates)
            
            logger.info(f"Demo: Generated 30-day history for {symbol}")
            return data
        except Exception as e:
            logger.error(f"Error generating demo history: {str(e)}")
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
