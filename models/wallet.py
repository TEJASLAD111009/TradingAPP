"""Wallet model for managing user funds and transactions."""
import json
import os
from typing import List, Dict
from datetime import datetime


class Transaction:
    """Represents a transaction in the wallet."""
    
    def __init__(self, transaction_type: str, amount: float, description: str = ""):
        """Initialize a transaction.
        
        Args:
            transaction_type: Type of transaction (deposit, withdrawal, buy, sell)
            amount: Amount in rupees
            description: Description of the transaction
        """
        self.type = transaction_type
        self.amount = amount
        self.description = description
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            'type': self.type,
            'amount': self.amount,
            'description': self.description,
            'timestamp': self.timestamp
        }


class Wallet:
    """Wallet model to manage user funds."""
    
    def __init__(self, username: str, initial_balance: float = 0.0):
        """Initialize a wallet.
        
        Args:
            username: Username who owns the wallet
            initial_balance: Initial balance in USD
        """
        self.username = username
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
        self.currency = "USD"  # United States Dollars
    
    def add_funds(self, amount: float, description: str = "Deposit") -> bool:
        """Add funds to wallet.
        
        Args:
            amount: Amount to add in USD
            description: Description of the deposit
            
        Returns:
            True if successful
        """
        if amount <= 0:
            return False
        
        self.balance += amount
        self.transactions.append(Transaction("deposit", amount, description))
        return True
    
    def withdraw_funds(self, amount: float, description: str = "Withdrawal") -> bool:
        """Withdraw funds from wallet.
        
        Args:
            amount: Amount to withdraw in USD
            description: Description of the withdrawal
            
        Returns:
            True if successful
        """
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        self.transactions.append(Transaction("withdrawal", amount, description))
        return True
    
    def deduct_for_purchase(self, amount: float, description: str) -> bool:
        """Deduct funds for stock purchase.
        
        Args:
            amount: Amount to deduct
            description: Description of the purchase
            
        Returns:
            True if sufficient balance
        """
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        self.transactions.append(Transaction("buy", amount, description))
        return True
    
    def credit_from_sale(self, amount: float, description: str) -> bool:
        """Credit funds from stock sale.
        
        Args:
            amount: Amount to credit
            description: Description of the sale
            
        Returns:
            True if successful
        """
        if amount <= 0:
            return False
        
        self.balance += amount
        self.transactions.append(Transaction("sell", amount, description))
        return True
    
    def get_transaction_history(self, limit: int = None) -> List[Dict]:
        """Get transaction history.
        
        Args:
            limit: Limit number of transactions
            
        Returns:
            List of transactions
        """
        transactions = [t.to_dict() for t in self.transactions]
        if limit:
            return transactions[-limit:]
        return transactions
    
    def to_dict(self) -> dict:
        """Convert wallet to dictionary."""
        return {
            'username': self.username,
            'balance': self.balance,
            'currency': self.currency,
            'transactions': [t.to_dict() for t in self.transactions]
        }


class WalletManager:
    """Manages wallet persistence and operations."""
    
    WALLETS_FILE = 'd:\\trading\\data\\wallets.json'
    
    @classmethod
    def initialize_wallet(cls, username: str, initial_balance: float = 1000.0):
        """Initialize or get wallet for a user.
        
        Args:
            username: Username
            initial_balance: Initial balance if creating new wallet (in USD)
            
        Returns:
            Wallet object
        """
        os.makedirs(os.path.dirname(cls.WALLETS_FILE), exist_ok=True)
        
        # Load existing wallets
        wallets_data = cls._load_wallets()
        
        if username in wallets_data:
            # Load existing wallet
            wallet_data = wallets_data[username]
            wallet = Wallet(username, wallet_data['balance'])
            # Restore transactions
            for trans_data in wallet_data.get('transactions', []):
                trans = Transaction(
                    trans_data['type'],
                    trans_data['amount'],
                    trans_data.get('description', '')
                )
                trans.timestamp = trans_data['timestamp']
                wallet.transactions.append(trans)
            return wallet
        else:
            # Create new wallet
            wallet = Wallet(username, initial_balance)
            wallet.transactions.append(
                Transaction("deposit", initial_balance, "Initial Balance")
            )
            return wallet
    
    @classmethod
    def save_wallet(cls, wallet: Wallet):
        """Save wallet to file.
        
        Args:
            wallet: Wallet object to save
        """
        os.makedirs(os.path.dirname(cls.WALLETS_FILE), exist_ok=True)
        wallets_data = cls._load_wallets()
        wallets_data[wallet.username] = wallet.to_dict()
        
        with open(cls.WALLETS_FILE, 'w') as f:
            json.dump(wallets_data, f, indent=4)
    
    @classmethod
    def _load_wallets(cls) -> Dict:
        """Load all wallets from file.
        
        Returns:
            Dictionary of wallets
        """
        if os.path.exists(cls.WALLETS_FILE):
            try:
                with open(cls.WALLETS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    @classmethod
    def get_wallet(cls, username: str) -> Wallet:
        """Get wallet for a user.
        
        Args:
            username: Username
            
        Returns:
            Wallet object
        """
        return cls.initialize_wallet(username)
