import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Alpha Vantage API Key (Get your own free API key from https://www.alphavantage.co)
API_KEY = ' MQIKXBO3Y2CVGMXX'

# Backend simulation for user accounts (replace with a database in production)
users_db = {"user1": "password1", "user2": "password2"}
portfolio = {"user1": [], "user2": []}
balances = {"user1": 10000, "user2": 10000}  # Initial balance for each user

# Function to fetch stock data
def fetch_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "Time Series (5min)" in data:
        df = pd.DataFrame(data["Time Series (5min)"]).transpose()
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df = df.astype(float)
        return df
    else:
        st.error("Failed to fetch data. Check the stock symbol or API limits.")
        return None

# Function to simulate buying a stock
def buy_stock(username, symbol, quantity, price):
    global portfolio, balances
    cost = quantity * price
    if balances[username] >= cost:
        balances[username] -= cost
        portfolio[username].append({
            "symbol": symbol, 
            "quantity": quantity, 
            "price": price,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        st.success(f"Successfully bought {quantity} shares of {symbol} for Rs {cost:.2f}")
    else:
        st.error("Insufficient balance to complete this transaction.")

# Function to simulate selling a stock
def sell_stock(username, symbol, quantity, price):
    global portfolio, balances
    user_stocks = portfolio.get(username, [])
    for stock in user_stocks:
        if stock["symbol"] == symbol and stock["quantity"] >= quantity:
            stock["quantity"] -= quantity
            balances[username] += quantity * price
            if stock["quantity"] == 0:
                user_stocks.remove(stock)
            st.success(f"Successfully sold {quantity} shares of {symbol} for Rs {quantity * price:.2f}")
            return
    st.error("You do not own enough shares of this stock.")

# Login system
def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username in users_db and users_db[username] == password:
            st.sidebar.success("Login Successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.sidebar.error("Invalid username or password.")
    if "logged_in" not in st.session_state:
        st.stop()

# Logout system
def logout():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.sidebar.success("Logged out successfully!")
        st.experimental_rerun()

# Main app
def main_app():
    st.title("Streamlit Trading App")
    username = st.session_state["username"]
    
    # Show balance
    st.header(f"Your Balance: Rs {balances[username]:.2f}")
    
    # Stock symbol input
    st.header("View Stock Data")
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, TSLA)")
    if st.button("Fetch Stock Data"):
        data = fetch_stock_data(symbol)
        if data is not None:
            st.line_chart(data["Close"])
            st.write(data)

    # Buy/Sell functionality
    st.header("Buy/Sell Stocks")
    with st.form("buy_sell_form"):
        action = st.selectbox("Action", ["Buy", "Sell"])
        stock_symbol = st.text_input("Stock Symbol")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Price per Share (Rs)", min_value=1.0, step=0.1)
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if action == "Buy":
                buy_stock(username, stock_symbol, quantity, price)
            elif action == "Sell":
                sell_stock(username, stock_symbol, quantity, price)

    # Portfolio view
    st.header("Your Portfolio")
    user_portfolio = portfolio.get(username, [])
    st.write(pd.DataFrame(user_portfolio))
    
    # Logout button
    logout()

# Streamlit Entry Point
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login()
