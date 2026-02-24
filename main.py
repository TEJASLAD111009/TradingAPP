"""Main entry point for the Trading App Streamlit application (Cross-platform compatible)."""
import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Configure page FIRST - must be before any other Streamlit commands
st.set_page_config(
    page_title="Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from controllers import PortfolioController
from views import (
    login_page,
    logout,
    check_login,
    wallet_page,
    get_wallet_summary,
    portfolio_page,
    stocks_page,
    stock_details_page
)
from utils import StockAPI
from models import UserManager
from utils.diagnostics import StockAPIDiagnostics

# Initialize data files on app startup (critical for Render deployment)
@st.cache_resource
def initialize_app():
    """Initialize app data files and run diagnostics."""
    try:
        UserManager.initialize_default_users()
        
        # Run diagnostics on startup (logs will be visible in Render logs)
        diagnostics = StockAPIDiagnostics.run_full_diagnostics()
        if diagnostics['overall_status'] == 'OK':
            st.write("✅ API connectivity: All systems operational")
        else:
            st.warning("⚠️ Some API connectivity issues detected. Check logs for details.")
            StockAPIDiagnostics.print_diagnostics_report()
    except Exception as e:
        st.warning(f"Warning during app initialization: {e}")

# Call initialization
initialize_app()

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Check login status
is_logged_in, username = check_login()

# Display main app
if not is_logged_in:
    # Show login page
    login_page()
else:
    # Type guard: ensure username is str (not None)
    assert isinstance(username, str), "Username must be a string"
    
    # Show main app interface
    # Sidebar navigation
    with st.sidebar:
        st.title("📈 Trading App")
        st.markdown(f"Welcome, **{username}**!")
        st.divider()
        
        # Get exchange rate
        exchange_rate = StockAPI.get_exchange_rate()
        
        # Show wallet summary in sidebar
        wallet_summary = get_wallet_summary(username)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="💵 Balance (USD)",
                value=wallet_summary['formatted_usd']
            )
        with col2:
            st.metric(
                label="💹 Rate",
                value=f"₹{exchange_rate:.2f}"
            )
        
        st.caption(f"In INR: {wallet_summary['formatted_inr']}")
        
        st.divider()
        
        # Navigation menu
        st.subheader("Navigation")
        page = st.radio(
            "Select Page",
            ["Dashboard", "Portfolio", "Stock Market", "Stock Details", "Wallet", "About"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Logout button
        if st.button("🔓 Logout", use_container_width=True):
            logout()
    
    # Main content
    if page == "Dashboard":
        st.title("📊 Dashboard")
        
        exchange_rate = StockAPI.get_exchange_rate()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Quick Stats")
            wallet_summary = get_wallet_summary(username)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(
                    label="💵 Available (USD)",
                    value=wallet_summary['formatted_usd']
                )
            
            portfolio_data = PortfolioController.get_portfolio(username)
            with col_b:
                st.metric(
                    label="📈 Portfolio (USD)",
                    value=f"${portfolio_data['total_value']:,.2f}"
                )
            
            st.caption(f"INR: {wallet_summary['formatted_inr']} | Portfolio: ₹{portfolio_data['total_value'] * exchange_rate:,.0f}")
        
        with col2:
            st.subheader("Quick Actions")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("💰 Deposit Funds", use_container_width=True):
                    st.session_state.current_page = "Wallet"
                    st.rerun()
            
            with col_b:
                if st.button("🛒 Buy Stock", use_container_width=True):
                    st.session_state.current_page = "Stock Market"
                    st.rerun()
        
        st.divider()
        
        # Display recent portfolio info
        st.subheader("Portfolio Overview")
        
        if portfolio_data['holdings']:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Total Invested (USD)",
                    value=f"${portfolio_data['total_invested']:,.2f}",
                    delta=f"₹{portfolio_data['total_invested'] * exchange_rate:,.0f}"
                )
            
            with col2:
                st.metric(
                    label="Current Value (USD)",
                    value=f"${portfolio_data['total_value']:,.2f}",
                    delta=f"₹{portfolio_data['total_value'] * exchange_rate:,.0f}"
                )
            
            with col3:
                pl = portfolio_data['total_profit_loss']
                delta_text = f"{(pl/portfolio_data['total_invested']*100):.2f}%" if portfolio_data['total_invested'] > 0 else "0%"
                st.metric(
                    label="Total P/L (USD)",
                    value=f"${pl:,.2f}",
                    delta=f"₹{pl * exchange_rate:,.0f} ({delta_text})"
                )
        else:
            st.info("👉 Start by buying some stocks to build your portfolio!")
    
    elif page == "Portfolio":
        portfolio_page(username)
    
    elif page == "Stock Market":
        stocks_page(username)
    
    elif page == "Stock Details":
        stock_details_page(username)
    
    elif page == "Wallet":
        wallet_page(username)
    
    elif page == "About":
        st.title("ℹ️ About Trading App")
        
        exchange_rate = StockAPI.get_exchange_rate()
        
        st.markdown(f"""
        ## Welcome to the Trading App! 📈
        
        This is a comprehensive stock trading application built with Streamlit and Python.
        
        ### Features:
        - 🔐 **Secure Login System** - Register and login with your credentials
        - 💰 **Wallet Management** - Deposit and withdraw funds in **US Dollars ($)**
        - 💹 **Live Currency Conversion** - Real-time USD to INR conversion (1 USD = ₹{exchange_rate:.2f})
        - 📊 **Stock Trading** - Buy and sell US stocks with real-time prices
        - 📈 **Portfolio Management** - Track your investments in both USD and INR
        - 💹 **Live Stock Data** - Real-time stock prices from Yahoo Finance API
        - 📉 **Historical Charts** - View stock price history with interactive charts
        
        ### Dual Currency Display:
        - Primary Currency: **USD (US Dollars)**
        - Conversion Currency: **INR (Indian Rupees)**
        - Live Exchange Rate: **1 USD = ₹{exchange_rate:.2f}**
        
        ### Demo Credentials:
        - Username: `demo` | Password: `demo123`
        - Username: `trader` | Password: `trader123`
        - Username: `user` | Password: `password123`
        
        ### Initial Balance:
        All new accounts start with **$1,000 USD** to get started trading!
        
        ### Technology Stack:
        - **Frontend**: Streamlit
        - **Backend**: Python
        - **Architecture**: MVC (Model-View-Controller)
        - **Stock Data**: YFinance API
        - **Exchange Rate**: exchangerate-api.com (free, live updates)
        - **Data Storage**: JSON-based local storage
        
        ### How to Use:
        1. **Login or Register** - Create an account or use demo credentials
        2. **Add Funds** - Deposit USD to your wallet
        3. **Browse Stocks** - View popular US stocks or search for specific ones
        4. **Buy Stocks** - Invest in stocks you like
        5. **Manage Portfolio** - Track your investments and performance in USD and INR
        6. **Sell Stocks** - Exit positions when you want
        
        ### Currency Features:
        - 💵 All stock prices shown in **USD**
        - 💹 Equivalent INR value always displayed
        - 📊 Portfolio values shown in both USD and INR
        - 📈 Transaction history shows both currencies
        - 🔄 Exchange rate updates every hour
        
        ### Disclaimer:
        This is a demo application for educational purposes. Always conduct thorough research
        before making real investments. Past performance is not indicative of future results.
        
        ---
        **Version**: 1.1 (USD Update) | **Last Updated**: February 2026
        """)
        
        st.divider()
        
        st.markdown("### Support & Documentation")
        st.info("""
        📖 For more information, check out the README.md file in the project root directory.
        """)

# Import Controllers for dashboard
from controllers import PortfolioController
