"""Controllers for trading app business logic."""
from models import UserManager, WalletManager, PortfolioManager
from utils import StockAPI
from typing import Dict, Tuple, Optional, List


class AuthController:
    """Handles authentication operations."""
    
    @staticmethod
    def register(username: str, password: str) -> Tuple[bool, str]:
        """Register a new user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Tuple of (success, message)
        """
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if UserManager.user_exists(username):
            return False, "Username already exists"
        
        if UserManager.create_user(username, password):
            # Initialize wallet for new user with $1000 USD
            WalletManager.initialize_wallet(username, 1000.0)
            PortfolioManager.initialize_portfolio(username)
            return True, "Registration successful"
        
        return False, "Error creating user"
    
    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Login a user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Tuple of (success, message)
        """
        if UserManager.authenticate(username, password):
            return True, "Login successful"
        
        return False, "Invalid username or password"


class WalletController:
    """Handles wallet operations."""
    
    @staticmethod
    def get_balance(username: str) -> float:
        """Get wallet balance.
        
        Args:
            username: Username
            
        Returns:
            Balance in rupees
        """
        wallet = WalletManager.get_wallet(username)
        return wallet.balance
    
    @staticmethod
    def add_funds(username: str, amount: float, description: str = "Deposit") -> Tuple[bool, str]:
        """Add funds to wallet.
        
        Args:
            username: Username
            amount: Amount in USD
            description: Transaction description
            
        Returns:
            Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        wallet = WalletManager.get_wallet(username)
        if wallet.add_funds(amount, description):
            WalletManager.save_wallet(wallet)
            return True, f"Successfully added ${amount:.2f}"
        
        return False, "Error adding funds"
    
    @staticmethod
    def withdraw_funds(username: str, amount: float, description: str = "Withdrawal") -> Tuple[bool, str]:
        """Withdraw funds from wallet.
        
        Args:
            username: Username
            amount: Amount in USD
            description: Transaction description
            
        Returns:
            Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        wallet = WalletManager.get_wallet(username)
        
        if amount > wallet.balance:
            return False, f"Insufficient balance. Available: ${wallet.balance:.2f}"
        
        if wallet.withdraw_funds(amount, description):
            WalletManager.save_wallet(wallet)
            return True, f"Successfully withdrew ${amount:.2f}"
        
        return False, "Error withdrawing funds"
    
    @staticmethod
    def get_transactions(username: str, limit: int = 10) -> List[Dict]:
        """Get transaction history.
        
        Args:
            username: Username
            limit: Limit number of transactions
            
        Returns:
            List of transactions
        """
        wallet = WalletManager.get_wallet(username)
        return wallet.get_transaction_history(limit)


class PortfolioController:
    """Handles portfolio operations."""
    
    @staticmethod
    def buy_stock(username: str, symbol: str, quantity: int) -> Tuple[bool, str]:
        """Buy stocks.
        
        Args:
            username: Username
            symbol: Stock symbol
            quantity: Number of shares
            
        Returns:
            Tuple of (success, message)
        """
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        
        # Get stock price
        stock_data = StockAPI.get_stock_price(symbol)
        if not stock_data:
            return False, f"Stock {symbol} not found"
        
        # Calculate cost in USD
        cost = stock_data['price_usd'] * quantity
        
        # Check wallet balance
        wallet = WalletManager.get_wallet(username)
        if cost > wallet.balance:
            return False, f"Insufficient balance. Required: ${cost:.2f}, Available: ${wallet.balance:.2f}"
        
        # Deduct from wallet
        wallet.deduct_for_purchase(cost, f"Buy {quantity} shares of {symbol}")
        WalletManager.save_wallet(wallet)
        
        # Add to portfolio
        portfolio = PortfolioManager.get_portfolio(username)
        portfolio.add_stock(symbol, quantity, stock_data['price_usd'])
        PortfolioManager.save_portfolio(portfolio)
        
        return True, f"Successfully bought {quantity} shares of {symbol} for ${cost:.2f}"
    
    @staticmethod
    def sell_stock(username: str, symbol: str, quantity: int) -> Tuple[bool, str]:
        """Sell stocks.
        
        Args:
            username: Username
            symbol: Stock symbol
            quantity: Number of shares
            
        Returns:
            Tuple of (success, message)
        """
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        
        # Get portfolio and check if stock exists
        portfolio = PortfolioManager.get_portfolio(username)
        stock = portfolio.get_stock(symbol)
        
        if not stock:
            return False, f"Stock {symbol} not found in portfolio"
        
        if quantity > stock.quantity:
            return False, f"Insufficient shares. You have {stock.quantity} shares"
        
        # Get current stock price in USD
        stock_data = StockAPI.get_stock_price(symbol)
        if not stock_data:
            return False, f"Cannot fetch current price for {symbol}"
        
        # Calculate proceeds in USD
        proceeds = stock_data['price_usd'] * quantity
        
        # Remove from portfolio
        portfolio.remove_stock(symbol, quantity)
        PortfolioManager.save_portfolio(portfolio)
        
        # Credit to wallet
        wallet = WalletManager.get_wallet(username)
        wallet.credit_from_sale(proceeds, f"Sell {quantity} shares of {symbol}")
        WalletManager.save_wallet(wallet)
        
        # Calculate profit/loss
        cost_basis = stock.purchase_price * quantity
        profit_loss = proceeds - cost_basis
        
        return True, f"Successfully sold {quantity} shares of {symbol} for ${proceeds:.2f} (P/L: ${profit_loss:.2f})"
    
    @staticmethod
    def get_portfolio(username: str) -> Dict:
        """Get complete portfolio information.
        
        Args:
            username: Username
            
        Returns:
            Portfolio data
        """
        portfolio = PortfolioManager.get_portfolio(username)
        holdings = portfolio.get_all_holdings()
        
        # Update current prices
        symbols = list(holdings.keys())
        if symbols:
            stock_data = StockAPI.get_multiple_stocks(symbols)
            for symbol, data in stock_data.items():
                if symbol in holdings:
                    holdings[symbol].current_price = data['price_inr']
        
        return {
            'holdings': holdings,
            'total_value': portfolio.get_total_value(),
            'total_invested': sum(stock.quantity * stock.purchase_price 
                                 for stock in holdings.values()),
            'total_profit_loss': portfolio.get_total_profit_loss()
        }
    
    @staticmethod
    def get_popular_stocks() -> Dict:
        """Get data for popular stocks.
        
        Returns:
            Dictionary of stock data
        """
        return StockAPI.get_popular_stocks_data()
    
    @staticmethod
    def get_stock_data(symbol: str) -> Optional[Dict]:
        """Get data for a specific stock.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Stock data or None
        """
        return StockAPI.get_stock_price(symbol)
    
    @staticmethod
    def get_stock_history(symbol: str, period: str = '1mo'):
        """Get historical data for a stock.
        
        Args:
            symbol: Stock symbol
            period: Time period
            
        Returns:
            DataFrame with historical data
        """
        return StockAPI.get_stock_history(symbol, period)
