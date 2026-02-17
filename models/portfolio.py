"""Portfolio model for managing user's stock holdings."""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class Stock:
    """Represents a stock holding in the portfolio."""
    
    def __init__(self, symbol: str, quantity: int, purchase_price: float):
        """Initialize a stock holding.
        
        Args:
            symbol: Stock symbol (e.g., AAPL)
            quantity: Number of shares
            purchase_price: Purchase price per share in rupees
        """
        self.symbol = symbol
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.purchase_date = datetime.now().isoformat()
        self.current_price = purchase_price  # Will be updated dynamically
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date,
            'current_price': self.current_price
        }
    
    def get_total_value(self) -> float:
        """Get current total value of holdings.
        
        Returns:
            Total value in rupees
        """
        return self.quantity * self.current_price
    
    def get_profit_loss(self) -> float:
        """Calculate profit or loss.
        
        Returns:
            Profit/loss in rupees
        """
        return (self.current_price - self.purchase_price) * self.quantity
    
    def get_profit_loss_percentage(self) -> float:
        """Calculate profit or loss percentage.
        
        Returns:
            Percentage change
        """
        if self.purchase_price == 0:
            return 0
        return ((self.current_price - self.purchase_price) / self.purchase_price) * 100


class Portfolio:
    """Portfolio model to manage user's stock holdings."""
    
    def __init__(self, username: str):
        """Initialize a portfolio.
        
        Args:
            username: Username who owns the portfolio
        """
        self.username = username
        self.holdings: Dict[str, Stock] = {}
        self.created_at = datetime.now().isoformat()
    
    def add_stock(self, symbol: str, quantity: int, purchase_price: float) -> bool:
        """Add stock to portfolio.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            purchase_price: Purchase price per share
            
        Returns:
            True if successful
        """
        if quantity <= 0 or purchase_price <= 0:
            return False
        
        if symbol in self.holdings:
            # Add to existing holding
            old_stock = self.holdings[symbol]
            total_cost = (old_stock.quantity * old_stock.purchase_price + 
                         quantity * purchase_price)
            average_price = total_cost / (old_stock.quantity + quantity)
            old_stock.quantity += quantity
            old_stock.purchase_price = average_price
        else:
            # Create new holding
            self.holdings[symbol] = Stock(symbol, quantity, purchase_price)
        
        return True
    
    def remove_stock(self, symbol: str, quantity: int) -> bool:
        """Remove stock from portfolio.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to sell
            
        Returns:
            True if successful
        """
        if symbol not in self.holdings:
            return False
        
        stock = self.holdings[symbol]
        if quantity > stock.quantity:
            return False
        
        stock.quantity -= quantity
        if stock.quantity == 0:
            del self.holdings[symbol]
        
        return True
    
    def get_stock(self, symbol: str) -> Optional[Stock]:
        """Get a specific stock holding.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Stock object or None
        """
        return self.holdings.get(symbol)
    
    def get_all_holdings(self) -> Dict[str, Stock]:
        """Get all holdings.
        
        Returns:
            Dictionary of holdings
        """
        return self.holdings.copy()
    
    def get_total_value(self) -> float:
        """Get total portfolio value.
        
        Returns:
            Total value in rupees
        """
        return sum(stock.get_total_value() for stock in self.holdings.values())
    
    def get_total_profit_loss(self) -> float:
        """Get total profit/loss.
        
        Returns:
            Total profit/loss in rupees
        """
        return sum(stock.get_profit_loss() for stock in self.holdings.values())
    
    def to_dict(self) -> dict:
        """Convert portfolio to dictionary."""
        return {
            'username': self.username,
            'created_at': self.created_at,
            'holdings': {symbol: stock.to_dict() 
                        for symbol, stock in self.holdings.items()}
        }


class PortfolioManager:
    """Manages portfolio persistence and operations."""
    
    PORTFOLIOS_FILE = 'd:\\trading\\data\\portfolios.json'
    
    @classmethod
    def initialize_portfolio(cls, username: str) -> Portfolio:
        """Initialize or get portfolio for a user.
        
        Args:
            username: Username
            
        Returns:
            Portfolio object
        """
        os.makedirs(os.path.dirname(cls.PORTFOLIOS_FILE), exist_ok=True)
        
        portfolios_data = cls._load_portfolios()
        
        if username in portfolios_data:
            # Load existing portfolio
            portfolio_data = portfolios_data[username]
            portfolio = Portfolio(username)
            for symbol, stock_data in portfolio_data.get('holdings', {}).items():
                stock = Stock(
                    stock_data['symbol'],
                    stock_data['quantity'],
                    stock_data['purchase_price']
                )
                stock.current_price = stock_data.get('current_price', stock_data['purchase_price'])
                stock.purchase_date = stock_data.get('purchase_date', datetime.now().isoformat())
                portfolio.holdings[symbol] = stock
            return portfolio
        else:
            # Create new portfolio
            return Portfolio(username)
    
    @classmethod
    def save_portfolio(cls, portfolio: Portfolio):
        """Save portfolio to file.
        
        Args:
            portfolio: Portfolio object to save
        """
        os.makedirs(os.path.dirname(cls.PORTFOLIOS_FILE), exist_ok=True)
        portfolios_data = cls._load_portfolios()
        portfolios_data[portfolio.username] = portfolio.to_dict()
        
        with open(cls.PORTFOLIOS_FILE, 'w') as f:
            json.dump(portfolios_data, f, indent=4)
    
    @classmethod
    def _load_portfolios(cls) -> Dict:
        """Load all portfolios from file.
        
        Returns:
            Dictionary of portfolios
        """
        if os.path.exists(cls.PORTFOLIOS_FILE):
            try:
                with open(cls.PORTFOLIOS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    @classmethod
    def get_portfolio(cls, username: str) -> Portfolio:
        """Get portfolio for a user.
        
        Args:
            username: Username
            
        Returns:
            Portfolio object
        """
        return cls.initialize_portfolio(username)
