"""Views package for trading app."""
from .auth_view import login_page, logout, check_login
from .wallet_view import wallet_page, get_wallet_summary
from .trading_view import portfolio_page, stocks_page, stock_details_page

__all__ = [
    'login_page',
    'logout',
    'check_login',
    'wallet_page',
    'get_wallet_summary',
    'portfolio_page',
    'stocks_page',
    'stock_details_page'
]
