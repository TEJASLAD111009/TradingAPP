"""Streamlit views for wallet management."""
import streamlit as st
from controllers import WalletController
from utils import StockAPI
import pandas as pd


def wallet_page(username: str):
    """Display wallet page."""
    st.title("💰 Wallet Management")
    
    # Get wallet balance
    balance = WalletController.get_balance(username)
    exchange_rate = StockAPI.get_exchange_rate()
    balance_inr = balance * exchange_rate
    
    # Display balance
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="💵 Current Balance", value=f"${balance:,.2f}")
    
    with col2:
        st.metric(label="💹 Exchange Rate", value=f"1 USD = ₹{exchange_rate:.2f}")
    
    with col3:
        st.metric(label="🇮🇳 Value in INR", value=f"₹{balance_inr:,.2f}")
    
    st.divider()
    
    # Add funds and withdraw funds tabs
    tab1, tab2, tab3 = st.tabs(["📥 Deposit Funds", "📤 Withdraw Funds", "📋 Transaction History"])
    
    with tab1:
        st.subheader("Deposit Funds")
        deposit_amount = st.number_input(
            "Amount to deposit (USD)",
            min_value=0.0,
            step=10.0,
            value=100.0,
            key="deposit_amount"
        )
        deposit_amount_inr = deposit_amount * exchange_rate
        st.info(f"💹 Equivalent: ₹{deposit_amount_inr:,.2f}")
        
        deposit_description = st.text_input(
            "Description (optional)",
            placeholder="e.g., Monthly investment",
            key="deposit_desc"
        )
        
        if st.button("✅ Deposit", use_container_width=True):
            if deposit_amount <= 0:
                st.error("Please enter a valid amount")
            else:
                success, message = WalletController.add_funds(
                    username,
                    deposit_amount,
                    deposit_description or "Deposit"
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.subheader("Withdraw Funds")
        
        st.info(f"Available Balance: ${balance:,.2f} (₹{balance_inr:,.2f})")
        
        withdraw_amount = st.number_input(
            "Amount to withdraw (USD)",
            min_value=0.0,
            step=10.0,
            value=50.0,
            key="withdraw_amount"
        )
        withdraw_amount_inr = withdraw_amount * exchange_rate
        st.info(f"💹 Equivalent: ₹{withdraw_amount_inr:,.2f}")
        
        withdraw_description = st.text_input(
            "Description (optional)",
            placeholder="e.g., Bank transfer",
            key="withdraw_desc"
        )
        
        if st.button("✅ Withdraw", use_container_width=True):
            if withdraw_amount <= 0:
                st.error("Please enter a valid amount")
            elif withdraw_amount > balance:
                st.error(f"Insufficient balance. Available: ${balance:,.2f}")
            else:
                success, message = WalletController.withdraw_funds(
                    username,
                    withdraw_amount,
                    withdraw_description or "Withdrawal"
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab3:
        st.subheader("Transaction History")
        
        transactions = WalletController.get_transactions(username)
        
        if transactions:
            # Create DataFrame
            df = pd.DataFrame([
                {
                    'Type': t['type'].upper(),
                    'Amount (USD)': f"${t['amount']:,.2f}",
                    'Amount (INR)': f"₹{t['amount'] * exchange_rate:,.2f}",
                    'Description': t['description'],
                    'Date & Time': t['timestamp'][:19]  # Remove microseconds
                }
                for t in reversed(transactions)  # Show latest first
            ])
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions yet")


def get_wallet_summary(username: str) -> dict:
    """Get wallet summary for sidebar.
    
    Args:
        username: Username
        
    Returns:
        Dictionary with wallet info
    """
    balance = WalletController.get_balance(username)
    exchange_rate = StockAPI.get_exchange_rate()
    balance_inr = balance * exchange_rate
    return {
        'balance_usd': balance,
        'balance_inr': balance_inr,
        'exchange_rate': exchange_rate,
        'formatted_usd': f"${balance:,.2f}",
        'formatted_inr': f"₹{balance_inr:,.2f}"
    }
