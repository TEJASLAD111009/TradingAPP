"""
Dashboard View - Handles main dashboard UI display
"""
import streamlit as st
import pandas as pd
from models.portfolio import PortfolioModel

class DashboardView:
    """View for displaying the main dashboard"""
    
    def __init__(self, portfolio_model: PortfolioModel):
        """
        Initialize dashboard view
        
        Args:
            portfolio_model: The portfolio model instance
        """
        self.portfolio_model = portfolio_model
    
    def show_header(self, username: str) -> None:
        """
        Display header with user balance
        
        Args:
            username: The current username
        """
        st.title("📈 Trading App")
        balance = self.portfolio_model.get_balance(username)
        st.header(f"💰 Your Balance: Rs {balance:.2f}")
    
    def show_stock_data_section(self) -> str:
        """
        Display section for stock data lookup
        
        Returns:
            The stock symbol entered by user, or empty string
        """
        st.header("📊 View Stock Data")
        symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, TSLA)")
        return symbol
    
    def display_stock_chart(self, data: pd.DataFrame, symbol: str) -> None:
        """
        Display stock chart and data table
        
        Args:
            data: DataFrame with stock data
            symbol: The stock symbol
        """
        if data is not None:
            st.subheader(f"{symbol} - Close Price")
            st.line_chart(data["Close"])
            
            st.subheader(f"{symbol} - Price Data")
            st.dataframe(data, use_container_width=True)
        else:
            st.error("Failed to fetch data. Check the stock symbol or API limits.")
    
    def show_buy_sell_section(self) -> dict:
        """
        Display buy/sell form
        
        Returns:
            Dictionary with form data: {action, symbol, quantity, price}
        """
        st.header("🤝 Buy/Sell Stocks")
        
        with st.form("buy_sell_form"):
            action = st.selectbox("Action", ["Buy", "Sell"])
            stock_symbol = st.text_input("Stock Symbol")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            price = st.number_input("Price per Share (Rs)", min_value=1.0, step=0.1)
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            return {
                "action": action,
                "symbol": stock_symbol,
                "quantity": int(quantity),
                "price": float(price),
                "submitted": True
            }
        
        return {"submitted": False}
    
    def display_portfolio(self, username: str) -> None:
        """
        Display user's portfolio
        
        Args:
            username: The current username
        """
        st.header("📋 Your Portfolio")
        user_portfolio = self.portfolio_model.get_portfolio(username)
        
        if user_portfolio:
            df = pd.DataFrame(user_portfolio)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Your portfolio is empty. Start trading!")
    
    def show_success_message(self, action: str, quantity: int, symbol: str, amount: float) -> None:
        """
        Display success message for transaction
        
        Args:
            action: 'Buy' or 'Sell'
            quantity: Quantity of shares
            symbol: Stock symbol
            amount: Amount in Rs
        """
        st.success(f"✅ Successfully {action.lower()}ed {quantity} shares of {symbol} for Rs {amount:.2f}")
    
    def show_error_message(self, message: str) -> None:
        """
        Display error message
        
        Args:
            message: Error message to display
        """
        st.error(f"❌ {message}")
