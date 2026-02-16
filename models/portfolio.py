"""
Portfolio Model - Handles portfolio and balance management
"""
from datetime import datetime
from typing import List, Dict, Any, Optional

class PortfolioModel:
    """Model for managing user portfolios and balances"""
    
    def __init__(self):
        # In production, replace with a real database
        self.portfolio = {
            "user1": [],
            "user2": []
        }
        self.balances = {
            "user1": 10000,
            "user2": 10000
        }
    
    def get_balance(self, username: str) -> float:
        """
        Get user's current balance
        
        Args:
            username: The username
            
        Returns:
            The user's balance
        """
        return self.balances.get(username, 0)
    
    def set_balance(self, username: str, amount: float) -> None:
        """
        Set user's balance
        
        Args:
            username: The username
            amount: The balance amount
        """
        if username not in self.balances:
            self.balances[username] = 0
        self.balances[username] = amount
    
    def get_portfolio(self, username: str) -> List[Dict[str, Any]]:
        """
        Get user's portfolio
        
        Args:
            username: The username
            
        Returns:
            List of stocks in user's portfolio
        """
        if username not in self.portfolio:
            self.portfolio[username] = []
        return self.portfolio[username]
    
    def add_to_portfolio(self, username: str, symbol: str, quantity: int, price: float) -> bool:
        """
        Add stock to portfolio (when buying)
        
        Args:
            username: The username
            symbol: Stock symbol
            quantity: Quantity to buy
            price: Price per share
            
        Returns:
            True if successful, False if insufficient balance
        """
        cost = quantity * price
        
        if self.balances.get(username, 0) < cost:
            return False
        
        self.balances[username] -= cost
        
        if username not in self.portfolio:
            self.portfolio[username] = []
        
        self.portfolio[username].append({
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return True
    
    def remove_from_portfolio(self, username: str, symbol: str, quantity: int, price: float) -> bool:
        """
        Remove stock from portfolio (when selling)
        
        Args:
            username: The username
            symbol: Stock symbol
            quantity: Quantity to sell
            price: Price per share
            
        Returns:
            True if successful, False if insufficient shares
        """
        if username not in self.portfolio:
            return False
        
        user_stocks = self.portfolio[username]
        
        for stock in user_stocks:
            if stock["symbol"] == symbol:
                if stock["quantity"] >= quantity:
                    stock["quantity"] -= quantity
                    self.balances[username] += quantity * price
                    
                    if stock["quantity"] == 0:
                        user_stocks.remove(stock)
                    
                    return True
        
        return False
    
    def initialize_user(self, username: str, initial_balance: float = 10000) -> None:
        """
        Initialize a new user's balance and portfolio
        
        Args:
            username: The username
            initial_balance: Initial balance amount
        """
        if username not in self.balances:
            self.balances[username] = initial_balance
        if username not in self.portfolio:
            self.portfolio[username] = []
